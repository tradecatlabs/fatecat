from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKER_LEASE_PATH = ROOT / "scripts" / "postgres-job-worker-lease-smoke.py"
WORKER_LEASE_SH = ROOT / "scripts" / "postgres-job-worker-lease-smoke.sh"
LOCAL_CI_PATH = ROOT / "scripts" / "local-ci.sh"
RUNTIME_BACKENDS_PATH = ROOT / "contracts" / "fate" / "delivery" / "runtime-backends.json"
OPERATIONS_DOC_PATH = ROOT / "docs" / "reference-materials" / "operations" / "测算基础设施 API 接入.md"


def _load_job_worker_lease_module():
    spec = importlib.util.spec_from_file_location("fatecat_postgres_job_worker_lease_smoke", WORKER_LEASE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_postgres_job_worker_lease_allow_missing_writes_blocked_summary(tmp_path, monkeypatch):
    worker_lease = _load_job_worker_lease_module()
    output_json = tmp_path / "postgres-job-worker-lease.json"
    monkeypatch.delenv("FATE_REPORT_JOB_DATABASE_URL", raising=False)

    result = worker_lease.main(["--allow-missing", "--output-json", str(output_json)])

    assert result == 0
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    assert summary["kind"] == "fatecat.postgres_job_worker_lease_smoke"
    assert summary["status"] == "blocked"
    assert summary["shipGate"]["status"] == "blocked"
    assert "does_not_verify_job_worker_lease" in summary["nonClaims"]
    assert not re.search(r"postgres(?:ql)?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]", serialized, re.I)


def test_postgres_job_worker_lease_script_and_contract_are_wired():
    script_text = WORKER_LEASE_PATH.read_text(encoding="utf-8")
    wrapper_text = WORKER_LEASE_SH.read_text(encoding="utf-8")
    local_ci_text = LOCAL_CI_PATH.read_text(encoding="utf-8")
    backends = json.loads(RUNTIME_BACKENDS_PATH.read_text(encoding="utf-8"))
    postgres = next(item for item in backends["backends"] if item["id"] == "backend.postgres")

    assert "claim_job_for_execution" in script_text
    assert "duplicate_job_claim_negative" in script_text
    assert "terminal_job_unclaimable" in script_text
    assert '"duplicateClaimRaceCount": race_total' in script_text
    assert '"leaseEvidence": {' in script_text
    assert "fatecat.postgres_job_worker_lease_smoke" in script_text
    assert "postgres-job-worker-lease-smoke.py" in wrapper_text
    assert "postgres-job-worker-lease-smoke.sh" in local_ci_text
    assert "postgresJobWorkerLeaseSmoke" in local_ci_text
    assert postgres["implementationStatus"] == "public_webhook_live_smoke_gate_baseline"
    assert postgres["capabilities"]["workerLease"] == "transactional_job_and_outbox_claim_with_restart_smoke_baseline"
    assert postgres["capabilities"]["workerRestart"] == "expired_lease_external_worker_restart_smoke_baseline"
    assert "bash scripts/postgres-job-worker-lease-smoke.sh" in postgres["externalVerification"]
    assert "bash scripts/postgres-job-worker-lease-smoke.sh --allow-missing" in postgres["localVerification"]
    assert "exactly_once" in postgres["migration"]["blockedClaims"]


def test_postgres_job_worker_lease_python_and_shell_syntax():
    subprocess.run([str(ROOT / ".venv" / "bin" / "python"), "-m", "py_compile", str(WORKER_LEASE_PATH)], check=True)
    subprocess.run(["bash", "-n", str(WORKER_LEASE_SH), str(LOCAL_CI_PATH)], check=True)


def test_postgres_job_worker_lease_operations_docs_do_not_overclaim():
    docs = OPERATIONS_DOC_PATH.read_text(encoding="utf-8")

    assert "postgres-job-worker-lease-smoke.sh" in docs
    assert "job execution worker lease" in docs
    assert "exactly-once" in docs
    assert "不证明" in docs
