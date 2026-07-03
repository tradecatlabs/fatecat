from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL_PLANE_DIR = ROOT / "contracts" / "fate" / "control-plane"
GATE_PATH = ROOT / "scripts" / "control-plane-gate.py"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_control_plane_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_control_plane_registry_defines_core_resource_envelopes():
    schema = _load_json(CONTROL_PLANE_DIR / "schemas" / "control-plane.schema.json")
    registry = _load_json(CONTROL_PLANE_DIR / "registry.json")
    resources = {item["id"]: item for item in registry["resources"]}

    assert schema["allowedResourceTypes"] == ["Capability", "Provider", "ReleaseGate", "EvaluationRun"]
    assert schema["requiredResourceFields"] == [
        "resourceType",
        "apiVersion",
        "id",
        "spec",
        "status",
        "links",
        "metadata",
    ]
    assert (
        "Provider reconciliation must point at provider lifecycle gate instead of reimplementing source/license/vendor checks."
        in schema["invariants"]
    )
    assert "bash scripts/control-plane-gate.sh" == registry["metadata"]["gateCommand"]
    assert {
        "control.capabilities",
        "control.providers",
        "control.release_gate",
        "control.evaluation_runs",
    } == set(resources)

    capabilities = resources["control.capabilities"]
    assert capabilities["resourceType"] == "Capability"
    assert capabilities["spec"]["desiredState"]["defaultCapabilityId"] == "bazi"
    assert capabilities["spec"]["desiredState"]["productionCapabilities"] == 4
    assert capabilities["spec"]["desiredState"]["plannedCapabilities"] == 5
    assert capabilities["status"]["reconciliation"]["status"] == "in_sync"

    providers = resources["control.providers"]
    assert providers["resourceType"] == "Provider"
    assert providers["spec"]["desiredState"]["productionProviderCount"] == 4
    assert providers["spec"]["gate"]["command"] == "bash scripts/provider-lifecycle-gate.sh"

    release_gate = resources["control.release_gate"]
    assert release_gate["resourceType"] == "ReleaseGate"
    assert release_gate["spec"]["admission"]["executable"] is False
    assert release_gate["status"]["reconciliation"]["status"] == "pending_external"

    evaluations = resources["control.evaluation_runs"]
    assert evaluations["resourceType"] == "EvaluationRun"
    assert "run.local_ci_quick" in evaluations["spec"]["desiredState"]["requiredRunIds"]


def test_control_plane_gate_reconciles_existing_registries(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "control-plane-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.control_plane_gate"
    assert stored["status"] == "passed"
    assert stored["resourceCount"] == 4
    assert stored["observed"]["capabilities"] == {"total": 9, "production": 4, "planned": 5}
    assert stored["observed"]["providers"] == {"productionProviders": 4}
    assert stored["observed"]["releaseGate"]["requiredEvidence"] == 10
    assert stored["observed"]["evaluationRuns"] == {"datasets": 5, "evaluationRuns": 5}
    assert "token" in stored["privacyBoundary"]


def test_control_plane_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "control-plane-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
