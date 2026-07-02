#!/usr/bin/env python3
"""本地 webhook encrypted config vault smoke。

验证 SQLite webhook delivery config 可加密持久化、manager 重建后解密重投、成功后删除，并支持 key rotation。
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "webhook" / "config-vault-smoke.json"
)


class WebhookConfigVaultSmokeError(RuntimeError):
    """本地 webhook encrypted config vault smoke 未满足预期。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from cryptography.fernet import Fernet  # noqa: PLC0415

    from report_jobs import ReportJobManager, ReportJobWebhookPolicy, SQLiteReportJobStore  # noqa: PLC0415
    from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig  # noqa: PLC0415
    from webhook_config_store import FernetWebhookConfigCodec  # noqa: PLC0415

    return (
        ReportJobManager,
        ReportJobWebhookPolicy,
        SQLiteReportJobStore,
        HttpWebhookDispatcher,
        WebhookConfig,
        Fernet,
        FernetWebhookConfigCodec,
    )


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise WebhookConfigVaultSmokeError(f"{name}: {details}")


def _wait_for_event(manager: Any, job_id: str, event_type: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    snapshot = None
    while time.monotonic() < deadline:
        snapshot = manager.get(job_id)
        if any(event.event_type == event_type for event in snapshot.events):
            return snapshot
        time.sleep(0.05)
    raise WebhookConfigVaultSmokeError(f"job did not reach event {event_type}: {snapshot}")


def _raw_db_text(path: Path) -> str:
    return path.read_bytes().decode("latin1", errors="ignore")


def run_smoke() -> dict[str, Any]:
    (
        ReportJobManager,
        ReportJobWebhookPolicy,
        SQLiteReportJobStore,
        HttpWebhookDispatcher,
        WebhookConfig,
        Fernet,
        FernetWebhookConfigCodec,
    ) = _load_runtime()
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="fatecat-webhook-config-vault-") as tmpdir:
        db_path = Path(tmpdir) / "config-vault.sqlite"
        old_key = Fernet.generate_key().decode("ascii")
        new_key = Fernet.generate_key().decode("ascii")
        old_codec = FernetWebhookConfigCodec(keys={"old": old_key}, active_key_id="old")

        def failing_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            return 500

        failing_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=failing_transport)
        first_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(db_path, webhook_config_codec=old_codec),
            **{"webhook_dispatcher": failing_dispatcher.deliver},
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
        )
        created = first_manager.submit(
            kind="markdown",
            report_system="bazi",
            input_summary={"name": "测试样本", "birthPlace": "北京"},
            webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="vault-smoke-secret"),
            task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
        )
        failed = _wait_for_event(first_manager, created.job_id, "webhook.delivery_failed")
        _check(
            checks, "seed_failed_outbox", failed.callback_outbox[0].status == "failed", failed.callback_outbox[0].status
        )

        store_with_old_key = SQLiteReportJobStore(db_path, webhook_config_codec=old_codec)
        _check(
            checks,
            "encrypted_config_record_exists",
            store_with_old_key.count_webhook_delivery_configs() == 1,
            str(store_with_old_key.count_webhook_delivery_configs()),
        )
        raw_text = _raw_db_text(db_path)
        forbidden_markers = (
            "callback.example",
            "vault-smoke-secret",
            "测试样本",
            "北京",
            "# 命理排盘报告",
        )
        for index, marker in enumerate(forbidden_markers, start=1):
            _check(checks, f"raw_sqlite_excludes_forbidden_{index}", marker not in raw_text, "omitted")

        with SQLiteReportJobStore(db_path)._connect() as conn:
            row = conn.execute("SELECT key_id FROM report_job_webhook_delivery_config").fetchone()
        _check(checks, "initial_key_id_old", str(row["key_id"]) == "old", str(row["key_id"]))

        new_codec = FernetWebhookConfigCodec(keys={"old": old_key, "new": new_key}, active_key_id="new")
        rotated_store = SQLiteReportJobStore(db_path, webhook_config_codec=new_codec)
        _check(
            checks,
            "rotation_count",
            rotated_store.rotate_webhook_delivery_configs() == 1,
            "rotated",
        )
        with SQLiteReportJobStore(db_path)._connect() as conn:
            rotated_row = conn.execute("SELECT key_id FROM report_job_webhook_delivery_config").fetchone()
        _check(checks, "rotated_key_id_new", str(rotated_row["key_id"]) == "new", str(rotated_row["key_id"]))

        delivery_calls: list[int] = []

        def success_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            delivery_calls.append(len(delivery_calls) + 1)
            return 204

        success_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=success_transport)
        rebuilt = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(db_path, webhook_config_codec=new_codec),
            **{"webhook_dispatcher": success_dispatcher.deliver},
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
        )
        redelivered = _wait_for_event(rebuilt, created.job_id, "webhook.redelivery_succeeded")
        event_types = [event.event_type for event in redelivered.events]
        _check(checks, "redelivery_attempt_once", delivery_calls == [1], str(delivery_calls))
        _check(
            checks,
            "redelivery_outbox_succeeded",
            redelivered.callback_outbox[0].status == "succeeded",
            redelivered.callback_outbox[0].status,
        )
        final_store = SQLiteReportJobStore(db_path, webhook_config_codec=new_codec)
        _check(
            checks,
            "encrypted_config_deleted_after_success",
            final_store.count_webhook_delivery_configs() == 0,
            str(final_store.count_webhook_delivery_configs()),
        )

    serialized = json.dumps(
        {
            "checks": checks,
            "events": event_types,
            "outboxStatus": redelivered.callback_outbox[0].status,
        },
        ensure_ascii=False,
    )
    for index, marker in enumerate(forbidden_markers, start=1):
        _check(checks, f"summary_excludes_forbidden_{index}", marker not in serialized, "omitted")

    return {
        "schemaVersion": 1,
        "kind": "fatecat.webhook_config_vault_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "redeliveryOutboxStatus": redelivered.callback_outbox[0].status,
        "redeliveryEventTypes": event_types,
        "encryptedConfigRemaining": 0,
        "rotation": {"fromKey": "old", "toKey": "new", "rotated": 1},
        "privacyBoundary": "本地 smoke 使用临时 SQLite、运行时生成 Fernet keys 和可注入 transport，不访问公网；summary 不包含 webhook URL、webhook secret、报告正文、姓名、出生地区、token、DSN、密文正文或生产路径。",
        "boundary": "该 smoke 证明 SQLite encrypted webhook config vault 可支持本地 manager 重建 redelivery 和 key rotation；不证明外部 Vault/KMS、external backend、分布式 worker lease、多副本锁、真实公网 live callback 或 exactly-once。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job webhook encrypted config vault smoke。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
    except WebhookConfigVaultSmokeError as exc:
        print(f"webhook config vault smoke error: {exc}", file=sys.stderr)
        return 1
    write_summary(summary, args.output_json)
    print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
