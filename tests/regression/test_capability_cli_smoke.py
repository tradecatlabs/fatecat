from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "capability-cli-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_capability_cli_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_capability_cli_smoke_writes_safe_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "capability-cli-smoke.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.capability_cli_smoke"
    assert stored["status"] == "passed"
    assert stored["smokeScope"] == "local_cli_capability_command"
    assert stored["externalConnectivity"] == "not_required"
    assert {item["capabilityId"] for item in stored["capabilities"]} == {"almanac", "bazi", "meihua", "ziwei"}
    assert stored["plannedCapabilityRejection"]["capabilityId"] == "liuyao"
    assert stored["plannedCapabilityRejection"]["actualExitCode"] == 1
    assert "尚未生产化" in stored["plannedCapabilityRejection"]["errorContains"]
    assert all(item["stdoutSha256"] and item["stdoutBytes"] > 0 for item in stored["capabilities"])

    serialized = json.dumps(stored, ensure_ascii=False)
    assert "测试用户" not in serialized
    assert "birthDateTime" not in serialized
    assert "reportBody" not in serialized
    assert "FATE_BOT_TOKEN" not in serialized
    assert "DATABASE_URL" not in serialized


def test_delivery_registry_wires_cli_capability_command_contract():
    registry = json.loads((ROOT / "contracts" / "fate" / "delivery" / "registry.json").read_text(encoding="utf-8"))
    contract = json.loads(
        (ROOT / "contracts" / "fate" / "delivery" / "cli-capability-command.json").read_text(encoding="utf-8")
    )

    cli_surface = next(item for item in registry["surfaces"] if item["id"] == "surface.cli")

    assert cli_surface["status"] == "partial"
    assert "bash scripts/capability-cli.sh <capability_id>" in cli_surface["entrypoints"]
    assert "contracts/fate/delivery/cli-capability-command.json" in cli_surface["outputContracts"]
    assert "bash scripts/capability-cli-smoke.sh --output-json <path>" in cli_surface["localVerification"]
    assert cli_surface["metadata"]["capabilityCommandStatus"] == "available"
    assert contract["entrypoint"] == "bash scripts/capability-cli.sh <capability_id>"
    assert contract["supportedOutputs"] == ["json"]
    assert set(contract["supportedCapabilities"]) == {"almanac", "bazi", "meihua", "ziwei"}
    assert contract["plannedCapabilityPolicy"]["status"] == "must_reject"
    assert "multi-surface semantic diff" in " ".join(contract["nonClaims"])


def test_local_ci_and_agents_wire_capability_cli_smoke():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    delivery_agents = (ROOT / "contracts" / "fate" / "delivery" / "AGENTS.md").read_text(encoding="utf-8")

    assert "capability-cli-smoke.sh" in local_ci
    assert "FATE_LOCAL_CI_CAPABILITY_CLI_SMOKE" in local_ci
    assert "test_capability_cli_smoke.py" in local_ci
    assert "capability-cli.sh" in scripts_agents
    assert "capability-cli-smoke.py" in scripts_agents
    assert "test_capability_cli_smoke.py" in tests_agents
    assert "cli-capability-command.json" in delivery_agents
