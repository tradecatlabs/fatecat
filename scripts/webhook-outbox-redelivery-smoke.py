#!/usr/bin/env python3
"""本地 webhook outbox redelivery smoke。

验证 SQLite 中 failed webhook outbox record 能在 manager 重建后通过运行时 resolver 自动重投；
同时验证 resolver 缺失时不会误投。
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
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "webhook" / "redelivery-smoke.json"


class WebhookOutboxRedeliverySmokeError(RuntimeError):
    """本地 webhook outbox redelivery smoke 未满足预期。"""


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
        raise WebhookOutboxRedeliverySmokeError(f"{name}: {details}")


def _wait_for_event(manager: Any, job_id: str, event_type: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    snapshot = None
    while time.monotonic() < deadline:
        snapshot = manager.get(job_id)
        if any(event.event_type == event_type for event in snapshot.events):
            return snapshot
        time.sleep(0.05)
    raise WebhookOutboxRedeliverySmokeError(f"job did not reach event {event_type}: {snapshot}")


def _failed_outbox_fixture(
    report_manager_cls: Any,
    policy_cls: Any,
    sqlite_store_cls: Any,
    dispatcher: Any,
    config_cls: Any,
    db_path: Path,
):
    manager = report_manager_cls(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=sqlite_store_cls(db_path),
        webhook_dispatcher=dispatcher,
        callback_policy=policy_cls(max_attempts=1),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=config_cls(url="https://callback.example/webhook", secret="redelivery-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    return manager, _wait_for_event(manager, created.job_id, "webhook.delivery_failed")


def run_smoke() -> dict[str, Any]:
    ReportJobManager, ReportJobWebhookPolicy, SQLiteReportJobStore, HttpWebhookDispatcher, WebhookConfig = (
        _load_runtime()
    )
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="fatecat-webhook-redelivery-") as tmpdir:
        redelivery_db = Path(tmpdir) / "redelivery.sqlite"

        def failing_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            return 500

        failing_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=failing_transport)
        _failure_manager, failed_snapshot = _failed_outbox_fixture(
            ReportJobManager,
            ReportJobWebhookPolicy,
            SQLiteReportJobStore,
            failing_dispatcher.deliver,
            WebhookConfig,
            db_path=redelivery_db,
        )
        failed_record = failed_snapshot.callback_outbox[0]
        _check(failed_record.status == "failed", "seed_failed_outbox", failed_record.status, checks)

        redelivery_calls: list[int] = []

        def success_transport(_url: str, _body: bytes, _headers: dict[str, str], _timeout_seconds: int) -> int:
            redelivery_calls.append(len(redelivery_calls) + 1)
            return 204

        success_dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=success_transport)

        def resolver(record: Any, _snapshot: Any):
            _check(record.outbox_id == failed_record.outbox_id, "resolver_record_match", "matched", checks)
            return WebhookConfig(url="https://callback.example/webhook", secret="redelivery-secret")

        redelivery_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(redelivery_db),
            **{
                "webhook_dispatcher": success_dispatcher.deliver,
                "delivery_resolver": resolver,
            },
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
        )
        redelivered = _wait_for_event(
            redelivery_manager,
            failed_snapshot.job_id,
            "webhook.redelivery_succeeded",
        )
        redelivered_events = [event.event_type for event in redelivered.events]
        _check(redelivery_calls == [1], "redelivery_attempt_once", str(redelivery_calls), checks)
        _check(
            redelivered.callback_outbox[0].status == "succeeded",
            "redelivery_outbox_succeeded",
            redelivered.callback_outbox[0].status,
            checks,
        )
        _check(
            "webhook.redelivery_scheduled" in redelivered_events,
            "redelivery_scheduled_event",
            ",".join(redelivered_events),
            checks,
        )
        _check(
            "webhook.delivery_succeeded" in redelivered_events,
            "redelivery_delivery_succeeded_event",
            ",".join(redelivered_events),
            checks,
        )

        missing_db = Path(tmpdir) / "missing-config.sqlite"
        _missing_manager, missing_failed = _failed_outbox_fixture(
            ReportJobManager,
            ReportJobWebhookPolicy,
            SQLiteReportJobStore,
            failing_dispatcher.deliver,
            WebhookConfig,
            db_path=missing_db,
        )
        missing_dispatch_called = False

        def should_not_dispatch(_snapshot: Any, _config: Any):
            nonlocal missing_dispatch_called
            missing_dispatch_called = True
            raise WebhookOutboxRedeliverySmokeError("resolver returned None but dispatcher was called")

        missing_config_manager = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(missing_db),
            **{
                "webhook_dispatcher": should_not_dispatch,
                "delivery_resolver": lambda _record, _snapshot: None,
            },
            callback_policy=ReportJobWebhookPolicy(max_attempts=1),
        )
        skipped = _wait_for_event(
            missing_config_manager,
            missing_failed.job_id,
            "webhook.redelivery_skipped",
        )
        skipped_events = [event.event_type for event in skipped.events]
        _check(not missing_dispatch_called, "missing_resolver_no_dispatch", "not called", checks)
        _check(
            skipped.callback_outbox[0].status == "failed",
            "missing_resolver_outbox_stays_failed",
            skipped.callback_outbox[0].status,
            checks,
        )

    serialized = json.dumps(
        {
            "checks": checks,
            "events": redelivered_events + skipped_events,
            "redeliveryStatus": redelivered.callback_outbox[0].status,
            "skippedStatus": skipped.callback_outbox[0].status,
        },
        ensure_ascii=False,
    )
    _check("callback.example" not in serialized, "no_callback_url_in_summary", "url omitted", checks)
    _check("redelivery-secret" not in serialized, "no_secret_in_summary", "secret omitted", checks)
    _check("测试样本" not in serialized, "no_name_in_summary", "name omitted", checks)
    _check("北京" not in serialized, "no_birth_place_in_summary", "birth place omitted", checks)
    _check("# 命理排盘报告" not in serialized, "no_markdown_in_summary", "markdown omitted", checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.webhook_outbox_redelivery_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "redeliveryOutboxStatus": redelivered.callback_outbox[0].status,
        "missingResolverOutboxStatus": skipped.callback_outbox[0].status,
        "redeliveryEventTypes": redelivered_events,
        "missingResolverEventTypes": skipped_events,
        "privacyBoundary": "本地 smoke 使用临时 SQLite 和运行时 resolver，不访问公网；summary 不包含 webhook URL、webhook secret、报告正文、姓名、出生地区、token、DSN 或生产路径。",
        "boundary": "该 smoke 证明 SQLite webhook outbox failed record 可在 manager 重建后通过 resolver 自动重投；不证明公网 live callback、external backend、分布式 worker lease、多副本锁、持久明文 secret 或 exactly-once。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job webhook outbox redelivery smoke。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
    except WebhookOutboxRedeliverySmokeError as exc:
        print(f"webhook outbox redelivery smoke error: {exc}", file=sys.stderr)
        return 1
    write_summary(summary, args.output_json)
    print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
