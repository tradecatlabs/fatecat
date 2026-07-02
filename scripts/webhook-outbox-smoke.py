#!/usr/bin/env python3
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
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "webhook" / "outbox-smoke.json"


class WebhookOutboxSmokeError(RuntimeError):
    """本地 webhook outbox smoke 未满足预期。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from report_jobs import ReportJobManager, ReportJobWebhookPolicy, SQLiteReportJobStore  # noqa: PLC0415
    from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig  # noqa: PLC0415

    return ReportJobManager, ReportJobWebhookPolicy, SQLiteReportJobStore, HttpWebhookDispatcher, WebhookConfig


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise WebhookOutboxSmokeError(f"{name}: {details}")


def _wait_for_event(manager: Any, job_id: str, event_type: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    snapshot = None
    while time.monotonic() < deadline:
        snapshot = manager.get(job_id)
        if any(event.event_type == event_type for event in snapshot.events):
            return snapshot
        time.sleep(0.05)
    raise WebhookOutboxSmokeError(f"job did not reach event {event_type}: {snapshot}")


def _dispatcher_arg(dispatcher: Any) -> dict[str, Any]:
    return {"webhook_dispatcher": dispatcher}


def run_smoke() -> dict[str, Any]:
    ReportJobManager, ReportJobWebhookPolicy, SQLiteReportJobStore, HttpWebhookDispatcher, WebhookConfig = (
        _load_runtime()
    )
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="fatecat-webhook-outbox-") as tmpdir:
        success_db = Path(tmpdir) / "success.sqlite"

        def success_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            return 204

        success_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=success_transport)
        success_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(success_db),
            callback_policy=ReportJobWebhookPolicy(max_attempts=2),
            **_dispatcher_arg(success_dispatcher.deliver),
        )
        success_created = success_manager.submit(
            kind="markdown",
            report_system="bazi",
            input_summary={"name": "测试样本", "birthPlace": "北京"},
            webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="outbox-secret"),
            task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
        )
        success_snapshot = _wait_for_event(success_manager, success_created.job_id, "webhook.delivery_succeeded")
        _check(len(success_snapshot.callback_outbox) == 1, "success_outbox_created", "one record", checks)
        success_record = success_snapshot.callback_outbox[0]
        _check(success_record.status == "succeeded", "success_outbox_status", success_record.status, checks)
        _check(success_record.attempts == 1, "success_outbox_attempts", str(success_record.attempts), checks)
        _check(success_record.result_status_code == 204, "success_outbox_status_code", "204", checks)
        _check(bool(success_record.target_host_hash), "success_target_host_hash", "present", checks)

        rebuilt_success = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(success_db),
        )
        loaded_success = rebuilt_success.get(success_created.job_id)
        _check(
            loaded_success.callback_outbox[0].status == "succeeded",
            "success_outbox_persisted_after_rebuild",
            loaded_success.callback_outbox[0].status,
            checks,
        )

        failure_db = Path(tmpdir) / "failure.sqlite"

        def failure_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            return 500

        failure_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=failure_transport)
        failure_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(failure_db),
            callback_policy=ReportJobWebhookPolicy(max_attempts=2),
            **_dispatcher_arg(failure_dispatcher.deliver),
        )
        failure_created = failure_manager.submit(
            kind="markdown",
            report_system="bazi",
            input_summary={"name": "测试样本", "birthPlace": "北京"},
            webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="outbox-secret"),
            task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
        )
        failure_snapshot = _wait_for_event(failure_manager, failure_created.job_id, "webhook.delivery_failed")
        _check(len(failure_snapshot.callback_outbox) == 1, "failure_outbox_created", "one record", checks)
        failure_record = failure_snapshot.callback_outbox[0]
        _check(failure_record.status == "failed", "failure_outbox_status", failure_record.status, checks)
        _check(failure_record.attempts == 2, "failure_outbox_attempts", str(failure_record.attempts), checks)
        _check(
            failure_record.last_error_type == "WebhookDeliveryError",
            "failure_outbox_error_type",
            "WebhookDeliveryError",
            checks,
        )

        rebuilt_failure = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(failure_db),
        )
        loaded_failure = rebuilt_failure.get(failure_created.job_id)
        _check(
            loaded_failure.callback_outbox[0].status == "failed",
            "failure_outbox_persisted_after_rebuild",
            loaded_failure.callback_outbox[0].status,
            checks,
        )

    serialized = json.dumps(
        {
            "checks": checks,
            "successStatus": success_record.status,
            "failureStatus": failure_record.status,
            "successHostHash": success_record.target_host_hash,
            "failureHostHash": failure_record.target_host_hash,
        },
        ensure_ascii=False,
    )
    _check("callback.example" not in serialized, "no_callback_url_in_summary", "url omitted", checks)
    _check("outbox-secret" not in serialized, "no_secret_in_summary", "secret omitted", checks)
    _check("测试样本" not in serialized, "no_name_in_summary", "name omitted", checks)
    _check("北京" not in serialized, "no_birth_place_in_summary", "birth place omitted", checks)
    _check("# 命理排盘报告" not in serialized, "no_markdown_in_summary", "markdown omitted", checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.webhook_outbox_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "outboxStatuses": {"success": success_record.status, "failure": failure_record.status},
        "privacyBoundary": "本地 smoke 使用临时 SQLite 和可注入 transport，不访问公网；summary 不包含 webhook URL、webhook secret、报告正文、姓名、出生地区、token、DSN 或生产路径。",
        "boundary": "该 smoke 证明 SQLite persistent webhook outbox record 可审计且跨 manager 重建可读，不证明公网 live callback、跨进程自动重投、external backend 或多副本 worker。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job webhook outbox smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
        return 0
    except WebhookOutboxSmokeError as exc:
        print(f"webhook outbox smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
