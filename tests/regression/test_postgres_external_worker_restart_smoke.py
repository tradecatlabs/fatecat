from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "postgres-external-worker-restart-smoke.py"
SMOKE_SH = ROOT / "scripts" / "postgres-external-worker-restart-smoke.sh"
LOCAL_CI_PATH = ROOT / "scripts" / "local-ci.sh"
REPORT_JOBS_PATH = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src" / "report_jobs.py"
RUNTIME_BACKENDS_PATH = ROOT / "contracts" / "fate" / "delivery" / "runtime-backends.json"
OPERATIONS_DOC_PATH = ROOT / "docs" / "reference-materials" / "operations" / "测算基础设施 API 接入.md"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_postgres_external_worker_restart_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_postgres_external_worker_restart_allow_missing_writes_blocked_summary(tmp_path, monkeypatch):
    smoke = _load_smoke_module()
    output_json = tmp_path / "postgres-external-worker-restart.json"
    monkeypatch.delenv("FATE_REPORT_JOB_DATABASE_URL", raising=False)

    result = smoke.main(["--allow-missing", "--output-json", str(output_json)])

    assert result == 0
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    assert summary["kind"] == "fatecat.postgres_external_worker_restart_smoke"
    assert summary["status"] == "blocked"
    assert summary["shipGate"]["status"] == "blocked"
    assert "does_not_connect_to_postgres" in summary["nonClaims"]
    assert "does_not_verify_external_worker_restart" in summary["nonClaims"]
    assert not re.search(r"postgres(?:ql)?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]", serialized, re.I)


def test_postgres_external_worker_restart_script_and_contract_are_wired():
    smoke_text = SMOKE_PATH.read_text(encoding="utf-8")
    wrapper_text = SMOKE_SH.read_text(encoding="utf-8")
    local_ci_text = LOCAL_CI_PATH.read_text(encoding="utf-8")
    report_jobs_text = REPORT_JOBS_PATH.read_text(encoding="utf-8")
    backends = json.loads(RUNTIME_BACKENDS_PATH.read_text(encoding="utf-8"))
    postgres = next(item for item in backends["backends"] if item["id"] == "backend.postgres")

    assert "ReportJobManager" in smoke_text
    assert "executionCount" in smoke_text
    assert "duplicateExecutionBlocked" in smoke_text
    assert "fatecat.postgres_external_worker_restart_smoke" in smoke_text
    assert "does_not_prove_exactly_once" in smoke_text
    assert "postgres-external-worker-restart-smoke.py" in wrapper_text
    assert "postgres-external-worker-restart-smoke.sh" in local_ci_text
    assert "postgresExternalWorkerRestartSmoke" in local_ci_text
    assert "_job_execution_lease_owner" in report_jobs_text
    assert "claim_job_for_execution(" in report_jobs_text
    assert "release_job_execution_lease(" in report_jobs_text
    assert postgres["implementationStatus"] == "external_worker_restart_smoke_baseline"
    assert postgres["capabilities"]["workerRestart"] == "expired_lease_external_worker_restart_smoke_baseline"
    assert postgres["capabilities"]["exactlyOnceClaim"] is False
    assert "bash scripts/postgres-external-worker-restart-smoke.sh" in postgres["externalVerification"]
    assert "bash scripts/postgres-external-worker-restart-smoke.sh --allow-missing" in postgres["localVerification"]
    assert "exactly_once" in postgres["migration"]["blockedClaims"]
    assert "public_webhook_live" in postgres["migration"]["blockedClaims"]
    assert "external_vault_kms" in postgres["migration"]["blockedClaims"]


def test_postgres_external_worker_restart_python_and_shell_syntax():
    subprocess.run(
        [
            str(ROOT / ".venv" / "bin" / "python"),
            "-m",
            "py_compile",
            str(SMOKE_PATH),
            str(REPORT_JOBS_PATH),
        ],
        check=True,
    )
    subprocess.run(["bash", "-n", str(SMOKE_SH), str(LOCAL_CI_PATH)], check=True)


def test_postgres_external_worker_restart_operations_docs_do_not_overclaim():
    docs = OPERATIONS_DOC_PATH.read_text(encoding="utf-8")

    assert "postgres-external-worker-restart-smoke.sh" in docs
    assert "external worker restart smoke" in docs or "crash/restart" in docs
    assert "exactly-once" in docs
    assert "不证明" in docs
