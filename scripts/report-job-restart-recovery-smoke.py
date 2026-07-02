#!/usr/bin/env python3
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
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "report-jobs" / "restart-recovery-smoke.json"
)


class RestartRecoverySmokeError(RuntimeError):
    """本地 report job restart recovery smoke 未满足预期。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from report_jobs import ReportJobEvent, ReportJobManager, SQLiteReportJobStore, _ReportJob  # noqa: PLC0415

    return ReportJobManager, SQLiteReportJobStore, ReportJobEvent, _ReportJob


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise RestartRecoverySmokeError(f"{name}: {details}")


def run_smoke() -> dict[str, Any]:
    ReportJobManager, SQLiteReportJobStore, ReportJobEvent, StoredJob = _load_runtime()
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="fatecat-restart-recovery-") as tmpdir:
        db_path = Path(tmpdir) / "report-jobs.sqlite"
        original_store = SQLiteReportJobStore(db_path)
        created_at = datetime.now(UTC)
        expires_at = created_at + timedelta(seconds=120)
        job_id = "restart-recovery-smoke-job"
        stale_job = StoredJob(
            job_id=job_id,
            kind="markdown",
            report_system="bazi",
            task=None,
            input_summary={"name": "测试样本", "birthPlace": "北京"},
            idempotency_key="restart-recovery-smoke",
            webhook_config=None,
            created_monotonic=time.monotonic(),
            expires_monotonic=time.monotonic() + 120,
            created_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
            status="running",
            started_at=created_at.isoformat(),
            attempts=1,
            max_attempts=1,
        )
        original_store.save_job(stale_job)
        original_store.append_job_event(
            ReportJobEvent(
                event_id=f"{job_id}:queued",
                job_id=job_id,
                event_type="job.queued",
                status="queued",
                created_at=created_at.isoformat(),
                message="报告任务已进入队列",
                metadata={"seededBy": "restart_recovery_smoke"},
            )
        )
        original_store.append_job_event(
            ReportJobEvent(
                event_id=f"{job_id}:running",
                job_id=job_id,
                event_type="job.running",
                status="running",
                created_at=created_at.isoformat(),
                message="报告任务开始执行",
                metadata={"seededBy": "restart_recovery_smoke"},
            )
        )
        persisted_before_rebuild = original_store.load_jobs()[0]
        _check(
            persisted_before_rebuild.status == "running",
            "job_running_before_rebuild",
            f"status={persisted_before_rebuild.status}",
            checks,
        )

        rebuilt = ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=SQLiteReportJobStore(db_path),
        )
        recovered = rebuilt.get(job_id)

        event_types = [event.event_type for event in recovered.events]
        _check(recovered.status == "failed", "job_failed_after_rebuild", f"status={recovered.status}", checks)
        _check(
            recovered.error == "任务执行器已重启，未完成任务已终止",
            "recovery_error_message",
            "expected restart termination message",
            checks,
        )
        _check("job.recovered_failed" in event_types, "recovered_failed_event", ",".join(event_types), checks)
        _check(recovered.result is None, "result_not_persisted", "result omitted", checks)

        duplicate = rebuilt.submit(
            kind="markdown",
            report_system="bazi",
            idempotency_key="restart-recovery-smoke",
            task=lambda: {"reportSystem": "bazi", "markdown": "should-not-run"},
        )
        _check(duplicate.job_id == job_id, "idempotency_reuses_recovered_job", "same job id", checks)
        _check(duplicate.status == "failed", "idempotency_returns_failed_job", f"status={duplicate.status}", checks)
        persisted_after_duplicate = SQLiteReportJobStore(db_path).load_jobs()[0]
        _check(
            persisted_after_duplicate.status == "failed",
            "persisted_status_remains_failed",
            f"status={persisted_after_duplicate.status}",
            checks,
        )

    event_text = json.dumps(event_types, ensure_ascii=False)
    checks_text = json.dumps(checks, ensure_ascii=False)
    _check("测试样本" not in checks_text, "no_name_in_summary", "name omitted", checks)
    _check("北京" not in checks_text, "no_birth_place_in_summary", "birth place omitted", checks)
    _check("should-not-run" not in checks_text, "no_markdown_in_summary", "markdown omitted", checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.report_job_restart_recovery_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "eventTypes": event_types,
        "eventTypeSummary": event_text,
        "privacyBoundary": "本地 smoke 使用临时 SQLite，不访问公网，不读取真实 .env；summary 不包含 Markdown 正文、姓名、出生地区、token、secret、DSN 或生产路径。",
        "boundary": "该 smoke 证明 restart-safe failure 和事件可审计，不证明任务跨进程继续执行、external backend 或多副本 worker。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job restart recovery smoke，并输出机器可读 JSON。")
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
    except RestartRecoverySmokeError as exc:
        print(f"report job restart recovery smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
