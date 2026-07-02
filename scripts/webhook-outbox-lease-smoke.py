#!/usr/bin/env python3
"""本地 webhook outbox lease smoke。

验证 SQLite failed webhook outbox record 必须先 claim lease 才能重投，避免本地多个 manager
同时扫描同一 outbox 时重复投递。
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
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "webhook" / "outbox-lease-smoke.json"
)


class WebhookOutboxLeaseSmokeError(RuntimeError):
    """本地 webhook outbox lease smoke 未满足预期。"""


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
        raise WebhookOutboxLeaseSmokeError(f"{name}: {details}")


def _wait_for_event(manager: Any, job_id: str, event_type: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    snapshot = None
    while time.monotonic() < deadline:
        snapshot = manager.get(job_id)
        if any(event.event_type == event_type for event in snapshot.events):
            return snapshot
        time.sleep(0.05)
    raise WebhookOutboxLeaseSmokeError(f"job did not reach event {event_type}: {snapshot}")


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

    with tempfile.TemporaryDirectory(prefix="fatecat-webhook-outbox-lease-") as tmpdir:
        db_path = Path(tmpdir) / "outbox-lease.sqlite"
        codec = FernetWebhookConfigCodec(keys={"v1": Fernet.generate_key().decode("ascii")}, active_key_id="v1")

        def failing_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            return 500

        failing_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=failing_transport)
        first_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(db_path, webhook_config_codec=codec),
            **{"webhook_dispatcher": failing_dispatcher.deliver},
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
        )
        created = first_manager.submit(
            kind="markdown",
            report_system="bazi",
            input_summary={"name": "测试样本", "birthPlace": "北京"},
            webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="lease-smoke-secret"),
            task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
        )
        failed = _wait_for_event(first_manager, created.job_id, "webhook.delivery_failed")
        record = failed.callback_outbox[0]
        _check(checks, "seed_failed_outbox", record.status == "failed", record.status)

        store = SQLiteReportJobStore(db_path, webhook_config_codec=codec)
        claimed_by_a = store.claim_webhook_outbox_record(record, lease_owner="worker-a", lease_seconds=30)
        _check(checks, "worker_a_claims", claimed_by_a is not None, "claimed")
        _check(
            checks,
            "leased_record_hidden_from_redelivery_scan",
            not store.load_redeliverable_webhook_outbox_records(),
            "hidden",
        )
        _check(
            checks,
            "worker_b_cannot_double_claim",
            store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30) is None,
            "blocked",
        )
        store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-b")
        _check(
            checks,
            "wrong_owner_release_noop",
            store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30) is None,
            "still blocked",
        )
        store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-a")
        claimed_by_b = store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30)
        _check(checks, "worker_b_claims_after_release", claimed_by_b is not None, "claimed")
        store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-b")

        delivery_calls: list[int] = []

        def success_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            delivery_calls.append(len(delivery_calls) + 1)
            return 204

        success_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=success_transport)
        rebuilt = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(db_path, webhook_config_codec=codec),
            **{"webhook_dispatcher": success_dispatcher.deliver},
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
            webhook_redelivery_lease_seconds=30,
        )
        redelivered = _wait_for_event(rebuilt, created.job_id, "webhook.redelivery_succeeded")
        event_types = [event.event_type for event in redelivered.events]
        _check(checks, "manager_redelivery_attempt_once", delivery_calls == [1], str(delivery_calls))
        _check(
            checks,
            "manager_redelivery_outbox_succeeded",
            redelivered.callback_outbox[0].status == "succeeded",
            redelivered.callback_outbox[0].status,
        )
        _check(
            checks,
            "encrypted_config_deleted_after_success",
            SQLiteReportJobStore(db_path, webhook_config_codec=codec).count_webhook_delivery_configs() == 0,
            "deleted",
        )

    serialized = json.dumps(
        {
            "checks": checks,
            "events": event_types,
            "outboxStatus": redelivered.callback_outbox[0].status,
        },
        ensure_ascii=False,
    )
    forbidden_markers = (
        "callback.example",
        "lease-smoke-secret",
        "worker-a",
        "worker-b",
        "测试样本",
        "北京",
        "# 命理排盘报告",
    )
    for index, marker in enumerate(forbidden_markers, start=1):
        _check(checks, f"summary_excludes_forbidden_{index}", marker not in serialized, "omitted")

    return {
        "schemaVersion": 1,
        "kind": "fatecat.webhook_outbox_lease_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "redeliveryOutboxStatus": redelivered.callback_outbox[0].status,
        "redeliveryEventTypes": event_types,
        "encryptedConfigRemaining": 0,
        "privacyBoundary": "本地 smoke 使用临时 SQLite、运行时生成 Fernet key 和可注入 transport，不访问公网；summary 不包含 webhook URL、webhook secret、lease owner、报告正文、姓名、出生地区、token、DSN、密文正文或生产路径。",
        "boundary": "该 smoke 证明 SQLite webhook outbox lease claim/release baseline 可阻止本地重复 claim 并支持 manager 重建 redelivery；不证明 external backend、生产级分布式 worker lease、多副本锁、真实公网 live callback、外部 Vault/KMS 或 exactly-once。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job webhook outbox lease smoke。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
    except WebhookOutboxLeaseSmokeError as exc:
        print(f"webhook outbox lease smoke error: {exc}", file=sys.stderr)
        return 1
    write_summary(summary, args.output_json)
    print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
