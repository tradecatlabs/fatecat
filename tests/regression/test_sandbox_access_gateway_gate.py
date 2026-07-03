from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from fastapi.testclient import TestClient

import main

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "sandbox-access-gateway-gate.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_sandbox_access_gateway_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _almanac_payload() -> dict:
    sandbox = json.loads((ROOT / "contracts/fate/developer/sandbox.json").read_text(encoding="utf-8"))
    fixture = next(item for item in sandbox["fixtures"] if item["capabilityId"] == "almanac")
    return fixture["request"]


def test_sandbox_access_gateway_gate_writes_redacted_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "sandbox-access-gateway-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["kind"] == "fatecat.sandbox_access_gateway_gate"
    assert stored["status"] == "passed"
    assert stored["localGatewayExecutable"] is True
    assert stored["livePublicTokenService"] is False
    assert stored["rateLimitEvidence"]["secondStatus"] == 429
    assert stored["auditEvidence"]["redacted"] is True
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "local-sandbox-credential" not in serialized
    assert "sandbox-smoke-subject" not in serialized


def test_sandbox_access_gateway_contract_is_linked_from_developer_platform():
    platform = json.loads((ROOT / "contracts/fate/developer/developer-platform.json").read_text(encoding="utf-8"))
    gateway = json.loads((ROOT / "contracts/fate/developer/sandbox-access-gateway.json").read_text(encoding="utf-8"))
    token_contract = json.loads(
        (ROOT / "contracts/fate/developer/sandbox-token-contract.json").read_text(encoding="utf-8")
    )

    assert platform["sandbox"]["accessGatewayContract"] == "contracts/fate/developer/sandbox-access-gateway.json"
    assert platform["validation"]["sandboxGatewayGateCommand"] == "bash scripts/sandbox-access-gateway-gate.sh"
    assert gateway["livePublicTokenServiceStatus"] == "not_implemented"
    assert gateway["validation"]["gateCommand"] == "bash scripts/sandbox-access-gateway-gate.sh"
    assert token_contract["localGatewayContract"] == "contracts/fate/developer/sandbox-access-gateway.json"
    assert token_contract["liveServiceStatus"] == "not_implemented"


def test_sandbox_access_gateway_endpoint_enforces_scope(monkeypatch):
    client = TestClient(main.app)
    payload = _almanac_payload()
    sample_bearer = "endpoint-smoke-test-credential"

    monkeypatch.setenv("FATE_SANDBOX_TOKENS", f"sandbox-user:{sample_bearer}:capability:calculate:meihua")
    wrong_scope = client.post(
        "/sandbox/capabilities/almanac/calculate",
        json=payload,
        headers={"Authorization": f"Bearer {sample_bearer}"},
    )
    assert wrong_scope.status_code == 403

    monkeypatch.setenv("FATE_SANDBOX_TOKENS", f"sandbox-user:{sample_bearer}:capability:calculate:almanac")
    allowed = client.post(
        "/sandbox/capabilities/almanac/calculate",
        json=payload,
        headers={"Authorization": f"Bearer {sample_bearer}"},
    )
    assert allowed.status_code == 200
    body = allowed.json()
    assert body["success"] is True
    assert body["capabilityId"] == "almanac"
    assert body["sandbox"]["scope"] == "capability:calculate:almanac"
    assert body["sandbox"]["liveServiceStatus"] == "local_gateway_only"
    assert sample_bearer not in json.dumps(body, ensure_ascii=False)
