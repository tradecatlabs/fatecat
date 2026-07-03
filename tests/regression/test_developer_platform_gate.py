from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEVELOPER_PLATFORM_GATE_PATH = ROOT / "scripts" / "developer-platform-gate.py"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_developer_platform_gate_locks_sdk_sandbox_and_changelog_contracts(tmp_path):
    gate = _load_module("fatecat_developer_platform_gate_test", DEVELOPER_PLATFORM_GATE_PATH)
    output_json = tmp_path / "developer-platform-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["kind"] == "fatecat.developer_platform_gate"
    assert stored["status"] == "passed"
    assert stored["summary"]["sdkPackageCandidates"] >= 4
    assert stored["summary"]["sandboxFixtures"] >= 2
    assert stored["summary"]["publishedSdkPackages"] == 0
    assert stored["summary"]["liveSandboxTokenService"] is False
    assert stored["summary"]["localSandboxGateway"] is True
    assert stored["sandboxTokenContract"] == "contracts/fate/developer/sandbox-token-contract.json"
    assert stored["sandboxAccessGateway"] == "contracts/fate/developer/sandbox-access-gateway.json"
    assert stored["apiChangelog"] == "contracts/fate/developer/api-changelog.json"
    assert any("PyPI/npm" in item for item in stored["limitations"])
    assert any("sandbox token" in item for item in stored["limitations"])


def test_developer_platform_contract_explicitly_disclaims_live_public_sdk_and_token():
    platform = json.loads((ROOT / "contracts/fate/developer/developer-platform.json").read_text(encoding="utf-8"))
    token_contract = json.loads(
        (ROOT / "contracts/fate/developer/sandbox-token-contract.json").read_text(encoding="utf-8")
    )
    changelog = json.loads((ROOT / "contracts/fate/developer/api-changelog.json").read_text(encoding="utf-8"))

    assert platform["sdkPackageBaseline"]["releaseStatus"] == "baseline_not_published"
    assert platform["sdkPackageBaseline"]["packageRegistryStatus"] == "not_published"
    assert platform["sandbox"]["livePublicSandboxStatus"] == "not_implemented"
    assert platform["sandbox"]["accessGatewayContract"] == "contracts/fate/developer/sandbox-access-gateway.json"
    assert platform["apiChangelog"]["machineContract"] == "contracts/fate/developer/api-changelog.json"
    assert token_contract["status"] == "contract_only"
    assert token_contract["liveServiceStatus"] == "not_implemented"
    assert token_contract["localGatewayContract"] == "contracts/fate/developer/sandbox-access-gateway.json"
    assert token_contract["tokenMaterialPolicy"] == "no_real_tokens_in_repo"
    assert changelog["currentApiVersion"] == "v1"
    assert "api-changelog.0067.developer-platform-contract" in {entry["id"] for entry in changelog["entries"]}
