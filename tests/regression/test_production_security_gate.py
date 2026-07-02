from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "production-security-gate.py"
EXTERNALIZATION_GATE_PATH = ROOT / "scripts" / "security-externalization-gate.py"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_gate_module():
    return _load_module("fatecat_production_security_gate", GATE_PATH)


def _load_externalization_gate_module():
    return _load_module("fatecat_security_externalization_gate", EXTERNALIZATION_GATE_PATH)


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


def test_security_externalization_gate_validates_contract_and_negative_cases(tmp_path):
    gate = _load_externalization_gate_module()
    output_json = tmp_path / "security-externalization-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.security_externalization_gate_summary"
    assert stored["status"] == "passed"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert {
        "control.production_identity_oidc",
        "control.external_siem_immutable_audit",
        "control.retention_cleanup_plan",
    } == set(stored["controls"])
    assert {
        "fake.local_token_as_oidc",
        "fake.placeholder_siem",
        "fake.retention_without_smoke",
    } == set(stored["negativeEvidenceRejected"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["production_security_gate"]["ok"] is True
    assert checks["contract_external_pending"]["ok"] is True
    assert checks["registry_externalization_gate_command"]["ok"] is True
    assert checks["policy_externalization_contract"]["ok"] is True


def test_security_externalization_gate_cli_writes_summary(tmp_path):
    gate = _load_externalization_gate_module()
    output_json = tmp_path / "security-externalization-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert len(stored["negativeEvidenceRejected"]) == 3


def test_security_externalization_gate_rejects_local_token_as_oidc():
    gate = _load_externalization_gate_module()
    contract = json.loads((SECURITY_DIR / "externalization-evidence-contract.json").read_text(encoding="utf-8"))
    fake_case = next(case for case in contract["negativeEvidenceCases"] if case["id"] == "fake.local_token_as_oidc")

    try:
        gate.validate_external_evidence(fake_case["evidence"], contract)
    except gate.GateFailure as exc:
        assert "identity" in str(exc)
    else:
        raise AssertionError("local scoped token evidence must be rejected")


def test_security_externalization_gate_rejects_placeholder_siem():
    gate = _load_externalization_gate_module()
    contract = json.loads((SECURITY_DIR / "externalization-evidence-contract.json").read_text(encoding="utf-8"))
    fake_case = next(case for case in contract["negativeEvidenceCases"] if case["id"] == "fake.placeholder_siem")

    try:
        gate.validate_external_evidence(fake_case["evidence"], contract)
    except gate.GateFailure as exc:
        assert "siem" in str(exc)
    else:
        raise AssertionError("placeholder SIEM evidence must be rejected")


def test_security_externalization_gate_accepts_redacted_live_evidence(tmp_path):
    gate = _load_externalization_gate_module()
    evidence_json = tmp_path / "external-security-evidence.json"
    evidence_json.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.security_externalization_evidence",
                "status": "external_live_passed",
                "identity": {
                    "mode": "external_oidc_or_idp",
                    "provider": "company-idp",
                    "verificationStatus": "passed_external_oidc_check",
                    "issuerProofRef": "evidence://identity/issuer",
                    "jwksVerificationProofRef": "evidence://identity/jwks",
                    "audienceVerificationProofRef": "evidence://identity/audience",
                    "scopesVerificationProofRef": "evidence://identity/scopes",
                },
                "siem": {
                    "mode": "worm",
                    "verificationStatus": "passed_external_siem_check",
                    "externalExportProofRef": "evidence://siem/export",
                    "immutabilityProofRef": "evidence://siem/immutability",
                    "retentionProofRef": "evidence://siem/retention",
                    "payloadBoundary": "redacted_no_payload",
                },
                "retentionCleaner": {
                    "mode": "time_based_cleanup_with_audit",
                    "verificationStatus": "passed_retention_cleaner_smoke",
                    "smokeSummaryRef": "evidence://retention/cleaner-smoke",
                    "deleteMode": "tombstone_then_purge",
                    "auditAction": "retention.cleanup.dry_run",
                    "dryRun": True,
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_json = tmp_path / "security-externalization-live.json"

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["liveEvidenceStatus"] == "external_live_passed"
