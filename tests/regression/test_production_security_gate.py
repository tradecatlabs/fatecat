from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "production-security-gate.py"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_production_security_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_production_security_gate_validates_identity_siem_retention_and_owasp(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "production-security-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["owaspCoverageCount"] == 10
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert "token" in stored["privacyBoundary"]
    assert {
        "control.production_identity_oidc",
        "control.external_siem_immutable_audit",
        "control.retention_cleanup_plan",
        "control.owasp_api_security_regression",
    } == set(stored["controls"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["identity_external_pending"]["ok"] is True
    assert checks["siem_external_pending"]["ok"] is True
    assert checks["retention_current_mode_explicit_delete"]["ok"] is True
    assert checks["owasp_top10_complete"]["ok"] is True
    assert checks["policy_blocks_without_external_evidence"]["ok"] is True


def test_production_security_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "production-security-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"


def test_production_security_policy_maps_all_owasp_api_top10_items():
    policy = json.loads((SECURITY_DIR / "production-security-policy.json").read_text(encoding="utf-8"))

    assert policy["identity"]["requiredForPublicMultiTenant"] is True
    assert policy["siem"]["immutableAuditRequired"] is True
    assert policy["retention"]["currentRecordMode"] == "explicit_delete"
    assert policy["retention"]["targetRecordMode"] == "time_based_cleanup_with_audit"
    assert {item["id"] for item in policy["owaspApiSecurityTop10_2023"]} == {
        "API1",
        "API2",
        "API3",
        "API4",
        "API5",
        "API6",
        "API7",
        "API8",
        "API9",
        "API10",
    }
    assert all(item["name"] and item["localCoverage"] for item in policy["owaspApiSecurityTop10_2023"])
