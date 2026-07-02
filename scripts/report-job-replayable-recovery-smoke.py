#!/usr/bin/env python3
"""本地 replayable report job recovery smoke。

验证 SQLite 中可序列化 task payload + factory 的 active job 能在 manager 重建后重新入队执行；
同时验证缺少 payload/factory 的 active job 仍按安全失败处理。
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

DEFAULT_OUTPUT = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "report-jobs" / "replayable-recovery-smoke.json"
)


class ReplayableRecoverySmokeError(RuntimeError):
    """本地 replayable recovery smoke 未满足预期。"""


def _load_runtime():
    from report_jobs import ReportJobEvent, ReportJobManager, SQLiteReportJobStore, _ReportJob  # noqa: PLC0415

    return ReportJobManager, SQLiteReportJobStore, ReportJobEvent, _ReportJob


def _check(checks: list[dict[str, Any]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})
    if not ok:
        raise ReplayableRecoverySmokeError(f"{name}: {detail}")


def _wait_for_terminal(manager: Any, job_id: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    last_snapshot = None
    while time.monotonic() < deadline:
        last_snapshot = manager.get(job_id)
        if last_snapshot.status in {"succeeded", "failed", "cancelled", "expired"}:
            return last_snapshot
        time.sleep(0.05)
    raise ReplayableRecoverySmokeError(f"job did not finish: {last_snapshot}")


def _seed_active_job(
    store: Any, event_cls: Any, stored_job_cls: Any, *, job_id: str, payload: dict[str, Any] | None
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    expires = (datetime.now(UTC) + timedelta(seconds=120)).isoformat(timespec="seconds").replace("+00:00", "Z")
    store.save_job(
        stored_job_cls(
            job_id=job_id,
            kind="markdown",
            report_system="bazi",
            task=None,
            input_summary={"kind": "replayable-smoke"},
            idempotency_key=job_id,
            webhook_config=None,
            created_monotonic=time.monotonic(),
            expires_monotonic=time.monotonic() + 120,
            created_at=now,
            expires_at=expires,
            status="running",
            started_at=now,
            task_payload=payload,
        )
    )
    store.append_job_event(
        event_cls(
            event_id=f"{job_id}:queued",
            job_id=job_id,
            event_type="job.queued",
            status="queued",
            created_at=now,
            message="seeded queued event",
            metadata={"seededBy": "replayable_recovery_smoke"},
        )
    )
    store.append_job_event(
        event_cls(
            event_id=f"{job_id}:running",
            job_id=job_id,
            event_type="job.running",
            status="running",
            created_at=now,
            message="seeded running event",
            metadata={"seededBy": "replayable_recovery_smoke"},
        )
    )


def run_smoke() -> dict[str, Any]:
    report_manager_cls, sqlite_store_cls, event_cls, stored_job_cls = _load_runtime()
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="fatecat-replayable-recovery-") as tmpdir:
        replayable_db = Path(tmpdir) / "replayable.sqlite"
        replayable_job_id = "replayable-recovery-smoke-job"
        replayable_payload = {"taskType": "markdown", "fixture": "recoverable"}
        _seed_active_job(
            sqlite_store_cls(replayable_db),
            event_cls,
            stored_job_cls,
            job_id=replayable_job_id,
            payload=replayable_payload,
        )

        def markdown_factory(payload: dict[str, Any]):
            return lambda: {"reportSystem": "bazi", "markdown": f"# recovered {payload['fixture']}"}

        replayable_manager = report_manager_cls(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=sqlite_store_cls(replayable_db),
            task_factories={"markdown": markdown_factory},
        )
        replayed = _wait_for_terminal(replayable_manager, replayable_job_id)
        replayed_events = [event.event_type for event in replayed.events]
        _check(checks, "replayable_job_succeeded", replayed.status == "succeeded", f"status={replayed.status}")
        _check(
            checks,
            "recovered_requeued_event",
            "job.recovered_requeued" in replayed_events,
            ",".join(replayed_events),
        )
        _check(
            checks,
            "replayable_result_persisted",
            isinstance(replayed.result, dict) and replayed.result.get("markdown") == "# recovered recoverable",
            "result persisted",
        )

        failed_db = Path(tmpdir) / "non-replayable.sqlite"
        failed_job_id = "non-replayable-recovery-smoke-job"
        _seed_active_job(sqlite_store_cls(failed_db), event_cls, stored_job_cls, job_id=failed_job_id, payload=None)
        failed_manager = report_manager_cls(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=sqlite_store_cls(failed_db),
            task_factories={"markdown": markdown_factory},
        )
        failed = failed_manager.get(failed_job_id)
        failed_events = [event.event_type for event in failed.events]
        _check(checks, "non_replayable_failed", failed.status == "failed", f"status={failed.status}")
        _check(checks, "recovered_failed_event", "job.recovered_failed" in failed_events, ",".join(failed_events))

    serialized = json.dumps({"checks": checks, "events": replayed_events + failed_events}, ensure_ascii=False)
    _check(checks, "no_secret_in_summary", "secret" not in serialized.lower(), "secret omitted")
    _check(checks, "no_webhook_url_in_summary", "callback.example" not in serialized, "webhook url omitted")
    _check(checks, "no_markdown_body_in_summary", "# recovered" not in serialized, "markdown omitted")

    return {
        "schemaVersion": 1,
        "kind": "fatecat.report_job_replayable_recovery_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "replayableStatus": replayed.status,
        "nonReplayableStatus": failed.status,
        "replayableEventTypes": replayed_events,
        "nonReplayableEventTypes": failed_events,
        "privacyBoundary": "summary 不包含 webhook URL、webhook secret、报告正文、token、DSN 或生产路径。",
        "boundary": "该 smoke 证明本地 SQLite task payload + factory 可在 manager 重建后重新入队执行，不证明 external backend、分布式 worker lease、多副本锁或 exactly-once。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="执行本地 replayable report job recovery smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        summary = run_smoke()
    except Exception as exc:  # noqa: BLE001 - CLI smoke 必须输出明确失败原因。
        print(f"report job replayable recovery smoke error: {exc}", file=sys.stderr)
        return 1
    write_summary(summary, args.output_json)
    print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
