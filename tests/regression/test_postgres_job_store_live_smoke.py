from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE_SMOKE_PATH = ROOT / "scripts" / "postgres-job-store-live-smoke.py"
LIVE_SMOKE_SH = ROOT / "scripts" / "postgres-job-store-live-smoke.sh"
PRODUCTION_READINESS_PATH = ROOT / "scripts" / "production-readiness.sh"
LOCAL_CI_PATH = ROOT / "scripts" / "local-ci.sh"
RUNTIME_BACKENDS_PATH = ROOT / "contracts" / "fate" / "delivery" / "runtime-backends.json"
OPERATIONS_DOC_PATH = ROOT / "docs" / "reference-materials" / "operations" / "测算基础设施 API 接入.md"


def _load_live_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_postgres_job_store_live_smoke", LIVE_SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_postgres_live_smoke_allow_missing_writes_blocked_summary(tmp_path, monkeypatch):
    live_smoke = _load_live_smoke_module()
    output_json = tmp_path / "postgres-live-smoke.json"
    monkeypatch.delenv("FATE_REPORT_JOB_DATABASE_URL", raising=False)

    result = live_smoke.main(["--allow-missing", "--output-json", str(output_json)])

    assert result == 0
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    assert summary["kind"] == "fatecat.postgres_job_store_live_smoke"
    assert summary["status"] == "blocked"
    assert summary["shipGate"]["status"] == "blocked"
    assert "does_not_connect_to_postgres" in summary["nonClaims"]
    assert not re.search(r"postgres(?:ql)?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]", serialized, re.I)


def test_postgres_live_smoke_script_and_contract_are_wired():
    script_text = LIVE_SMOKE_PATH.read_text(encoding="utf-8")
    wrapper_text = LIVE_SMOKE_SH.read_text(encoding="utf-8")
    readiness_text = PRODUCTION_READINESS_PATH.read_text(encoding="utf-8")
    local_ci_text = LOCAL_CI_PATH.read_text(encoding="utf-8")
    backends = json.loads(RUNTIME_BACKENDS_PATH.read_text(encoding="utf-8"))
    postgres = next(item for item in backends["backends"] if item["id"] == "backend.postgres")

    assert "PostgresReportJobStore" in script_text
    assert "FATE_REPORT_JOB_DATABASE_URL" in script_text
    assert "fatecat.postgres_job_store_live_smoke" in script_text
    assert "postgres-job-store-live-smoke.py" in wrapper_text
    assert "FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE" in readiness_text
    assert "不得只靠布尔变量声明通过" in readiness_text
    assert "postgres-job-store-live-smoke.sh" in local_ci_text
    assert "postgresJobStoreLiveSmoke" in local_ci_text
    assert "bash scripts/postgres-job-store-live-smoke.sh" in postgres["externalVerification"]


def test_postgres_live_smoke_python_and_shell_syntax():
    subprocess.run([str(ROOT / ".venv" / "bin" / "python"), "-m", "py_compile", str(LIVE_SMOKE_PATH)], check=True)
    subprocess.run(["bash", "-n", str(LIVE_SMOKE_SH), str(PRODUCTION_READINESS_PATH)], check=True)


def test_postgres_live_smoke_operations_docs_do_not_overclaim():
    docs = OPERATIONS_DOC_PATH.read_text(encoding="utf-8")

    assert "postgres-job-store-live-smoke.sh" in docs
    assert "FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE" in docs
    assert "不证明 production ready" in docs or "不证明生产" in docs
