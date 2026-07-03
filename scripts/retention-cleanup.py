#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "retention-cleanup.json"
DEFAULT_RECORD_DB = REPO_ROOT / "infra" / "runtime" / "local-state" / "databases" / "bazi.sqlite"
DEFAULT_REPORT_JOB_DB = REPO_ROOT / "infra" / "runtime" / "local-state" / "databases" / "report_jobs.sqlite"

if str(DELIVERY_SRC) not in sys.path:
    sys.path.insert(0, str(DELIVERY_SRC))

from retention_cleanup import (  # noqa: E402
    RetentionCleanupConfig,
    assert_no_sensitive_payload,
    run_retention_cleanup,
)


def env_int(name: str, default: int, *, minimum: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(minimum, value)


def parse_now(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local FateCat retention cleanup.")
    parser.add_argument("--record-db", default=os.getenv("FATE_RECORD_DB_PATH", str(DEFAULT_RECORD_DB)))
    parser.add_argument("--report-job-db", default=os.getenv("FATE_REPORT_JOB_DB_PATH", str(DEFAULT_REPORT_JOB_DB)))
    parser.add_argument(
        "--record-retention-days",
        type=int,
        default=env_int("FATE_RECORD_RETENTION_DAYS", 0, minimum=0),
    )
    parser.add_argument(
        "--audit-event-retention-days",
        type=int,
        default=env_int("FATE_AUDIT_EVENT_RETENTION_DAYS", 30, minimum=1),
    )
    parser.add_argument(
        "--report-job-ttl-seconds",
        type=int,
        default=env_int("FATE_REPORT_JOB_TTL_SECONDS", 1800, minimum=60),
    )
    parser.add_argument(
        "--delete-mode",
        default=os.getenv("FATE_RECORD_RETENTION_DELETE_MODE", "hard_delete"),
        choices=("hard_delete", "tombstone_then_purge"),
    )
    parser.add_argument("--execute", action="store_true", help="真实执行删除；默认只 dry-run。")
    parser.add_argument("--now", help="测试用当前时间 ISO8601；默认使用当前 UTC。")
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_retention_cleanup(
        RetentionCleanupConfig(
            record_db_path=Path(args.record_db),
            report_job_db_path=Path(args.report_job_db),
            record_retention_days=args.record_retention_days,
            audit_event_retention_days=args.audit_event_retention_days,
            report_job_ttl_seconds=args.report_job_ttl_seconds,
            delete_mode=args.delete_mode,
            dry_run=not args.execute,
            now=parse_now(args.now),
        )
    )
    assert_no_sensitive_payload(summary)
    output_path = Path(args.output_json)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            summary if args.pretty else {"status": summary["status"], "outputJson": str(output_path)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
