from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "external-secret-provider-gate.py"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_secret_provider_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_external_secret_provider_gate_validates_contract_and_negative_cases(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "external-secret-provider-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.external_secret_provider_gate_summary"
    assert stored["status"] == "passed"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert stored["controls"] == ["control.external_secret_provider_kms"]
    assert {
        "fake.local_fernet_as_external",
        "fake.placeholder_vault",
        "fake.rotation_without_audit",
    } == set(stored["negativeEvidenceRejected"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["contract_external_pending"]["ok"] is True
    assert checks["registry_external_secret_provider_gate_command"]["ok"] is True
    assert checks["policy_secret_provider_contract"]["ok"] is True


def test_external_secret_provider_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "external-secret-provider-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert len(stored["negativeEvidenceRejected"]) == 3


def test_external_secret_provider_gate_rejects_local_fernet_as_external():
    gate = _load_gate_module()
    contract = json.loads((SECURITY_DIR / "external-secret-provider-contract.json").read_text(encoding="utf-8"))
    fake_case = next(
        case for case in contract["negativeEvidenceCases"] if case["id"] == "fake.local_fernet_as_external"
    )

    try:
        gate.validate_external_secret_evidence(fake_case["evidence"], contract)
    except gate.GateFailure as exc:
        assert "secretProvider" in str(exc)
    else:
        raise AssertionError("local Fernet evidence must be rejected")


def test_external_secret_provider_gate_rejects_placeholder_vault():
    gate = _load_gate_module()
    contract = json.loads((SECURITY_DIR / "external-secret-provider-contract.json").read_text(encoding="utf-8"))
    fake_case = next(case for case in contract["negativeEvidenceCases"] if case["id"] == "fake.placeholder_vault")

    try:
        gate.validate_external_secret_evidence(fake_case["evidence"], contract)
    except gate.GateFailure as exc:
        assert "secretProvider" in str(exc)
    else:
        raise AssertionError("placeholder Vault evidence must be rejected")


def test_external_secret_provider_gate_accepts_redacted_live_evidence(tmp_path):
    gate = _load_gate_module()
    evidence_json = tmp_path / "external-secret-provider-evidence.json"
    evidence_json.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.external_secret_provider_evidence",
                "status": "external_live_passed",
                "secretProvider": {
                    "mode": "external_secret_provider",
                    "providerType": "hashicorp_vault",
                    "verificationStatus": "passed_external_secret_provider_check",
                    "keyReferenceProofRef": "evidence://secret-provider/key-reference",
                    "rotationProofRef": "evidence://secret-provider/rotation",
                    "accessAuditProofRef": "evidence://secret-provider/access-audit",
                    "applicationInjectionProofRef": "evidence://secret-provider/application-injection",
                    "redactionBoundary": "redacted_no_secret_values",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_json = tmp_path / "external-secret-provider-live.json"

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["liveEvidenceStatus"] == "external_live_passed"


def test_external_secret_provider_gate_summary_does_not_expose_sensitive_values(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "external-secret-provider-gate.json"

    gate.write_summary(gate.run_gate(), output_json)
    serialized = output_json.read_text(encoding="utf-8")

    assert not re.search(
        r"postgres(?:ql)?://|https?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]|BEGIN (?:RSA|OPENSSH)",
        serialized,
        re.I,
    )
