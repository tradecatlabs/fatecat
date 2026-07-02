#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import inspect
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-job-store-dry-run.json"

SENSITIVE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)


class PostgresJobStoreDryRunError(RuntimeError):
    """Postgres ReportJobStore dry-run failed."""


def _load_runtime() -> Any:
    if str(DELIVERY_SRC) not in sys.path:
        sys.path.insert(0, str(DELIVERY_SRC))
    import report_jobs  # noqa: PLC0415

    return report_jobs


def _append_check(checks: list[dict[str, Any]], check_id: str, ok: bool, details: str) -> None:
    checks.append({"id": check_id, "status": "passed" if ok else "failed", "details": details})
    if not ok:
        raise PostgresJobStoreDryRunError(f"{check_id}: {details}")


def _sql_blob(statements: tuple[str, ...], claim_sql: str) -> str:
    return "\n\n".join((*statements, claim_sql))


def run_dry_run() -> dict[str, Any]:
    report_jobs = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []

    schema_sql = report_jobs.postgres_report_job_schema_sql()
    claim_sql = report_jobs.POSTGRES_WEBHOOK_OUTBOX_CLAIM_SQL
    adapter_source = inspect.getsource(report_jobs.PostgresReportJobStore)
    sql_text = f"{_sql_blob(schema_sql, claim_sql)}\n\n{adapter_source}"
    sql_lower = sql_text.lower()
    psycopg_available = importlib.util.find_spec("psycopg") is not None

    _append_check(checks, "store_class", hasattr(report_jobs, "PostgresReportJobStore"), "class exists")
    _append_check(
        checks,
        "store_interface",
        issubclass(report_jobs.PostgresReportJobStore, report_jobs.ReportJobStore),
        "PostgresReportJobStore implements ReportJobStore",
    )
    _append_check(
        checks,
        "backend_name",
        report_jobs.PostgresReportJobStore.backend_name == "postgres",
        report_jobs.PostgresReportJobStore.backend_name,
    )
    for table in report_jobs.POSTGRES_REPORT_JOB_REQUIRED_TABLES:
        _append_check(checks, f"table:{table}", f"create table if not exists {table}" in sql_lower, table)
    for index in report_jobs.POSTGRES_REPORT_JOB_REQUIRED_INDEXES:
        _append_check(checks, f"index:{index}", index.lower() in sql_lower, index)
    _append_check(checks, "job_upsert", "on conflict(job_id) do update" in sql_lower, "job upsert present")
    _append_check(
        checks, "event_idempotency", "on conflict(event_id) do nothing" in sql_lower, "event idempotency present"
    )
    _append_check(
        checks,
        "outbox_upsert",
        "on conflict(outbox_id) do update" in sql_lower,
        "webhook outbox upsert present",
    )
    _append_check(
        checks,
        "claim_returning",
        "returning outbox_id" in claim_sql.lower(),
        "claim sql returns claimed row",
    )
    _append_check(
        checks,
        "claim_owner_condition",
        "lease_owner = %(lease_owner)s" in claim_sql and "or lease_owner = %(lease_owner)s" in claim_sql.lower(),
        "claim sql is owner-aware",
    )
    _append_check(
        checks,
        "claim_expiry_condition",
        "lease_expires_at <= %(now)s" in claim_sql,
        "claim sql respects lease expiry",
    )
    _append_check(checks, "privacy:no_sensitive_values", not SENSITIVE_PATTERN.search(sql_text), "no inline DSN/secret")

    elapsed = round((time.perf_counter() - started) * 1000, 3)
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_job_store_dry_run",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": elapsed,
        "backend": {
            "id": "backend.postgres",
            "storeClass": "PostgresReportJobStore",
            "backendName": "postgres",
            "psycopgAvailable": psycopg_available,
            "requiresEnv": ["FATE_REPORT_JOB_STORE=postgres", "FATE_REPORT_JOB_DATABASE_URL"],
        },
        "schema": {
            "statementCount": len(schema_sql),
            "requiredTables": list(report_jobs.POSTGRES_REPORT_JOB_REQUIRED_TABLES),
            "requiredIndexes": list(report_jobs.POSTGRES_REPORT_JOB_REQUIRED_INDEXES),
            "claimSqlHasReturning": True,
            "claimSqlHasOwnerAndExpiry": True,
        },
        "checks": checks,
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "external Postgres migration/job smoke not executed",
                "production multi-replica worker lease not verified",
                "public webhook live delivery not verified",
            ],
        },
        "privacyBoundary": (
            "Dry-run 只检查 tracked SQL 和 class metadata，不读取或输出真实 DSN、数据库用户名、密码、"
            "token、webhook URL、webhook secret、用户输入或报告正文。"
        ),
        "nonClaims": [
            "does_not_connect_to_postgres",
            "does_not_verify_external_live",
            "does_not_prove_multi_replica_worker_lease",
            "does_not_prove_exactly_once",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres ReportJobStore dry-run，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="dry-run summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_dry_run()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "backend": summary["backend"]["id"],
                    "checks": len(summary["checks"]),
                    "shipGate": summary["shipGate"]["status"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except PostgresJobStoreDryRunError as exc:
        print(f"postgres job store dry-run error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
