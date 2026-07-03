#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
SCHEMA_PATH = REPO_ROOT / "infra" / "databases" / "bazi" / "schema_v2.sql"
DEFAULT_OUTPUT = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "retention-cleanup-smoke.json"
FIXED_NOW = datetime(2026, 7, 3, 0, 0, tzinfo=UTC)

if str(DELIVERY_SRC) not in sys.path:
    sys.path.insert(0, str(DELIVERY_SRC))

from report_jobs import SQLiteReportJobStore  # noqa: E402
from retention_cleanup import (  # noqa: E402
    RetentionCleanupConfig,
    assert_no_sensitive_payload,
    run_retention_cleanup,
)


def _init_record_db(path: Path) -> None:
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.execute(
            """
            INSERT INTO records (
                user_id, biz_type, name, gender, calendar_type, birth_date, birth_time,
                birth_place, longitude, latitude, biz_data, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "old-user",
                "bazi",
                "旧样本",
                "male",
                "solar",
                "1990-01-01",
                "08:00",
                "北京",
                116.4,
                39.9,
                "{}",
                "2026-05-01 00:00:00",
            ),
        )
        conn.execute(
            """
            INSERT INTO records (
                user_id, biz_type, name, gender, calendar_type, birth_date, birth_time,
                birth_place, longitude, latitude, biz_data, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "fresh-user",
                "bazi",
                "新样本",
                "male",
                "solar",
                "1990-01-01",
                "08:00",
                "北京",
                116.4,
                39.9,
                "{}",
                "2026-07-02 00:00:00",
            ),
        )


def _insert_job_fixture(path: Path) -> None:
    SQLiteReportJobStore(path)
    with sqlite3.connect(path) as conn:
        rows = [
            ("old-terminal", "succeeded", "2026-05-01T00:00:00+00:00", "2026-05-02T00:00:00+00:00"),
            ("fresh-terminal", "succeeded", "2026-07-02T00:00:00+00:00", "2026-07-04T00:00:00+00:00"),
            ("old-running", "running", "2026-05-01T00:00:00+00:00", "2026-05-02T00:00:00+00:00"),
        ]
        for job_id, status, created_at, expires_at in rows:
            conn.execute(
                """
                INSERT INTO report_jobs (
                    job_id, kind, status, report_system, created_at, expires_at,
                    input_summary_json, updated_at, attempts, max_attempts, retry_backoff_seconds
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (job_id, "markdown_report", status, "bazi", created_at, expires_at, "{}", created_at, 1, 1, 0),
            )
        conn.execute(
            """
            INSERT INTO report_job_events (event_id, job_id, event_type, status, created_at, message, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("event-old-terminal", "old-terminal", "job.succeeded", "succeeded", "2026-05-01T00:00:00+00:00", "", "{}"),
        )
        conn.execute(
            """
            INSERT INTO report_job_webhook_outbox (
                outbox_id, job_id, event_type, job_status, status, attempts,
                max_attempts, signature_mode, target_host_hash, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "outbox-old-terminal",
                "old-terminal",
                "report.job.terminal",
                "succeeded",
                "failed",
                1,
                1,
                "hmac_sha256",
                "target-hash",
                "2026-05-01T00:00:00+00:00",
                "2026-05-01T00:00:00+00:00",
            ),
        )
        conn.execute(
            """
            INSERT INTO report_job_webhook_delivery_config (
                outbox_id, job_id, cipher_suite, key_id, ciphertext,
                target_host_hash, signature_mode, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "outbox-old-terminal",
                "old-terminal",
                "fernet",
                "fixture-key",
                "redacted-ciphertext",
                "target-hash",
                "hmac_sha256",
                "2026-05-01T00:00:00+00:00",
                "2026-05-01T00:00:00+00:00",
            ),
        )


def _count(path: Path, table: str) -> int:
    with sqlite3.connect(path) as conn:
        row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0] or 0)


def _job_exists(path: Path, job_id: str) -> bool:
    with sqlite3.connect(path) as conn:
        row = conn.execute("SELECT 1 FROM report_jobs WHERE job_id = ?", (job_id,)).fetchone()
    return row is not None


def run_smoke() -> dict:
    with tempfile.TemporaryDirectory(prefix="fatecat-retention-cleanup-") as tmp:
        tmpdir = Path(tmp)
        record_db = tmpdir / "records.sqlite"
        report_job_db = tmpdir / "report_jobs.sqlite"
        _init_record_db(record_db)
        _insert_job_fixture(report_job_db)
        config = RetentionCleanupConfig(
            record_db_path=record_db,
            report_job_db_path=report_job_db,
            record_retention_days=30,
            audit_event_retention_days=30,
            report_job_ttl_seconds=1800,
            delete_mode="hard_delete",
            dry_run=True,
            now=FIXED_NOW,
        )
        dry_run = run_retention_cleanup(config)
        execute = run_retention_cleanup(RetentionCleanupConfig(**{**config.__dict__, "dry_run": False}))
        checks = [
            {"name": "dry_run_passed", "ok": dry_run["status"] == "passed"},
            {"name": "execute_passed", "ok": execute["status"] == "passed"},
            {"name": "old_record_removed", "ok": _count(record_db, "records") == 1},
            {"name": "old_terminal_job_removed", "ok": not _job_exists(report_job_db, "old-terminal")},
            {"name": "fresh_terminal_job_kept", "ok": _job_exists(report_job_db, "fresh-terminal")},
            {"name": "old_running_job_kept", "ok": _job_exists(report_job_db, "old-running")},
            {"name": "related_event_removed", "ok": _count(report_job_db, "report_job_events") == 0},
            {"name": "related_outbox_removed", "ok": _count(report_job_db, "report_job_webhook_outbox") == 0},
            {
                "name": "related_delivery_config_removed",
                "ok": _count(report_job_db, "report_job_webhook_delivery_config") == 0,
            },
        ]
        summary = {
            "schemaVersion": 1,
            "kind": "fatecat.retention_cleanup_smoke",
            "status": "passed" if all(item["ok"] for item in checks) else "failed",
            "fixedNow": FIXED_NOW.isoformat().replace("+00:00", "Z"),
            "dryRun": dry_run,
            "execute": execute,
            "checks": checks,
            "privacyBoundary": "smoke 只使用北京/测试合成 fixture，summary 不输出 recordId、jobId、userId、报告正文、token、secret、DSN 或 webhook URL。",
            "externalConnectivity": "外部 SIEM/不可变审计存储 retention 仍为外部连通验证待执行。",
        }
        assert_no_sensitive_payload(summary)
        return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run retention cleanup synthetic smoke.")
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_smoke()
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
