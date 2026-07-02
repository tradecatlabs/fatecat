from __future__ import annotations

import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DRY_RUN_PATH = ROOT / "scripts" / "postgres-job-store-dry-run.py"
MAIN_PATH = DELIVERY_SRC / "main.py"
PRODUCTION_READINESS_PATH = ROOT / "scripts" / "production-readiness.sh"
LOCAL_CI_PATH = ROOT / "scripts" / "local-ci.sh"


def _load_dry_run_module():
    spec = importlib.util.spec_from_file_location("fatecat_postgres_job_store_dry_run", DRY_RUN_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_report_jobs():
    if str(DELIVERY_SRC) not in sys.path:
        sys.path.insert(0, str(DELIVERY_SRC))
    import report_jobs  # noqa: PLC0415

    return report_jobs


def test_postgres_schema_contains_required_tables_indexes_and_claim_conditions():
    report_jobs = _load_report_jobs()
    job_claim_sql = report_jobs.POSTGRES_JOB_EXECUTION_CLAIM_SQL
    outbox_claim_sql = report_jobs.POSTGRES_WEBHOOK_OUTBOX_CLAIM_SQL
    adapter_source = inspect.getsource(report_jobs.PostgresReportJobStore)
    schema_text = "\n".join(
        (
            *report_jobs.postgres_report_job_schema_sql(),
            *report_jobs.POSTGRES_REPORT_JOB_LEASE_MIGRATION_SQL,
            report_jobs.POSTGRES_REPORT_JOB_LEASE_INDEX_SQL,
        )
    )
    combined = f"{schema_text}\n{job_claim_sql}\n{outbox_claim_sql}\n{adapter_source}".lower()

    for table in report_jobs.POSTGRES_REPORT_JOB_REQUIRED_TABLES:
        assert f"create table if not exists {table}" in combined
    for index in report_jobs.POSTGRES_REPORT_JOB_REQUIRED_INDEXES:
        assert index.lower() in combined
    assert "on conflict(job_id) do update" in combined
    assert "on conflict(outbox_id) do update" in combined
    assert "returning outbox_id" in outbox_claim_sql.lower()
    assert "returning job_id" in job_claim_sql.lower()
    assert "lease_owner = %(lease_owner)s" in outbox_claim_sql
    assert "lease_owner = %(lease_owner)s" in job_claim_sql
    assert "lease_expires_at <= %(now)s" in outbox_claim_sql
    assert "lease_expires_at <= %(now)s" in job_claim_sql
    assert "status in ('queued', 'running')" in job_claim_sql.lower()
    assert not re.search(r"postgres(?:ql)?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]", combined, re.I)


def test_postgres_store_is_optional_and_requires_explicit_dsn():
    report_jobs = _load_report_jobs()

    assert issubclass(report_jobs.PostgresReportJobStore, report_jobs.ReportJobStore)
    assert report_jobs.PostgresReportJobStore.backend_name == "postgres"
    with pytest.raises(ValueError, match="FATE_REPORT_JOB_DATABASE_URL"):
        report_jobs.PostgresReportJobStore("", connect_factory=lambda: None, initialize_schema=False)

    store = report_jobs.PostgresReportJobStore(
        "__FATE_REPORT_JOB_DATABASE_URL__",
        connect_factory=lambda: None,
        initialize_schema=False,
    )
    assert store.backend_name == "postgres"


def test_postgres_job_store_dry_run_writes_safe_summary(tmp_path):
    dry_run = _load_dry_run_module()
    output_json = tmp_path / "postgres-job-store-dry-run.json"

    summary = dry_run.run_dry_run()
    dry_run.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    serialized = json.dumps(stored, ensure_ascii=False, sort_keys=True)

    assert stored["kind"] == "fatecat.postgres_job_store_dry_run"
    assert stored["status"] == "passed"
    assert stored["backend"]["id"] == "backend.postgres"
    assert stored["shipGate"]["status"] == "blocked"
    assert "does_not_connect_to_postgres" in stored["nonClaims"]
    assert "FATE_REPORT_JOB_DATABASE_URL" in stored["backend"]["requiresEnv"]
    assert not re.search(r"postgres(?:ql)?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]", serialized, re.I)


def test_postgres_config_and_local_ci_are_wired_without_silent_fallback():
    main_text = MAIN_PATH.read_text(encoding="utf-8")
    readiness_text = PRODUCTION_READINESS_PATH.read_text(encoding="utf-8")
    local_ci_text = LOCAL_CI_PATH.read_text(encoding="utf-8")

    assert "PostgresReportJobStore" in main_text
    assert 'elif REPORT_JOB_STORE == "postgres"' in main_text
    assert "REPORT_JOB_DATABASE_URL" in main_text
    assert "只支持 memory、sqlite 或 postgres" in main_text
    assert "FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED" in readiness_text
    assert "不得在日志中输出 DSN 值" in readiness_text
    assert "postgres-job-store-dry-run.sh" in local_ci_text
    assert "postgresJobStoreDryRun" in local_ci_text
