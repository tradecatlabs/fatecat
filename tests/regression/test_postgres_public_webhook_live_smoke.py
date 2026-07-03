from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "postgres-public-webhook-live-smoke.py"
SMOKE_SH = ROOT / "scripts" / "postgres-public-webhook-live-smoke.sh"
LOCAL_CI_PATH = ROOT / "scripts" / "local-ci.sh"
RUNTIME_BACKENDS_PATH = ROOT / "contracts" / "fate" / "delivery" / "runtime-backends.json"
OPERATIONS_DOC_PATH = ROOT / "docs" / "reference-materials" / "operations" / "测算基础设施 API 接入.md"
SCRIPTS_AGENTS_PATH = ROOT / "scripts" / "AGENTS.md"
DELIVERY_AGENTS_PATH = ROOT / "contracts" / "fate" / "delivery" / "AGENTS.md"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_postgres_public_webhook_live_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_postgres_public_webhook_live_allow_missing_writes_blocked_summary(tmp_path, monkeypatch):
    smoke = _load_smoke_module()
    output_json = tmp_path / "postgres-public-webhook-live.json"
    monkeypatch.delenv("FATE_REPORT_JOB_DATABASE_URL", raising=False)
    monkeypatch.delenv("FATE_WEBHOOK_LIVE_URL", raising=False)
    monkeypatch.delenv("FATE_WEBHOOK_LIVE_SECRET", raising=False)

    result = smoke.main(["--allow-missing", "--output-json", str(output_json)])

    assert result == 0
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    assert summary["kind"] == "fatecat.postgres_public_webhook_live_smoke"
    assert summary["status"] == "blocked"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["database"]["databaseUrlEnv"] == "FATE_REPORT_JOB_DATABASE_URL"
    assert summary["webhook"]["urlEnv"] == "FATE_WEBHOOK_LIVE_URL"
    assert "does_not_connect_to_postgres" in summary["nonClaims"]
    assert "does_not_verify_public_webhook_live" in summary["nonClaims"]
    assert not re.search(
        r"postgres(?:ql)?://|https?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]",
        serialized,
        re.I,
    )


def test_postgres_public_webhook_live_script_and_contract_are_wired():
    smoke_text = SMOKE_PATH.read_text(encoding="utf-8")
    wrapper_text = SMOKE_SH.read_text(encoding="utf-8")
    local_ci_text = LOCAL_CI_PATH.read_text(encoding="utf-8")
    backends = json.loads(RUNTIME_BACKENDS_PATH.read_text(encoding="utf-8"))
    postgres = next(item for item in backends["backends"] if item["id"] == "backend.postgres")

    assert "ReportJobManager" in smoke_text
    assert "HttpWebhookDispatcher" in smoke_text
    assert "WebhookConfig" in smoke_text
    assert "fatecat.postgres_public_webhook_live_smoke" in smoke_text
    assert "does_not_prove_exactly_once" in smoke_text
    assert "does_not_verify_public_webhook_live" in smoke_text
    assert "postgres-public-webhook-live-smoke.py" in wrapper_text
    assert "postgres-public-webhook-live-smoke.sh" in local_ci_text
    assert "postgresPublicWebhookLiveSmoke" in local_ci_text
    assert postgres["implementationStatus"] == "worker_heartbeat_polling_smoke_baseline"
    assert postgres["status"] == "planned"
    assert postgres["capabilities"]["publicWebhookLive"] == "external_smoke_gate_ready_evidence_pending"
    assert postgres["capabilities"]["exactlyOnceClaim"] is False
    assert "bash scripts/postgres-public-webhook-live-smoke.sh" in postgres["externalVerification"]
    assert "bash scripts/postgres-public-webhook-live-smoke.sh --allow-missing" in postgres["localVerification"]
    assert "public_webhook_live" in postgres["migration"]["blockedClaims"]
    assert "external_vault_kms" in postgres["migration"]["blockedClaims"]


def test_postgres_public_webhook_live_python_and_shell_syntax():
    subprocess.run([str(ROOT / ".venv" / "bin" / "python"), "-m", "py_compile", str(SMOKE_PATH)], check=True)
    subprocess.run(["bash", "-n", str(SMOKE_SH), str(LOCAL_CI_PATH)], check=True)


def test_postgres_public_webhook_live_docs_do_not_overclaim():
    operations_docs = OPERATIONS_DOC_PATH.read_text(encoding="utf-8")
    scripts_agents = SCRIPTS_AGENTS_PATH.read_text(encoding="utf-8")
    delivery_agents = DELIVERY_AGENTS_PATH.read_text(encoding="utf-8")

    assert "postgres-public-webhook-live-smoke.sh" in operations_docs
    assert "公网 webhook live" in operations_docs
    assert "不证明" in operations_docs
    assert "exactly-once" in operations_docs
    assert "postgres-public-webhook-live-smoke.py" in scripts_agents
    assert "public webhook live smoke gate" in delivery_agents
