from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEVELOPER_PORTAL_GATE_PATH = ROOT / "scripts" / "developer-portal-gate.py"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_developer_portal_gate_locks_sdk_snapshot_and_no_live_overclaim(tmp_path):
    gate = _load_module("fatecat_developer_portal_gate_test", DEVELOPER_PORTAL_GATE_PATH)
    output_json = tmp_path / "developer-portal-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["kind"] == "fatecat.developer_portal_gate"
    assert stored["status"] == "passed"
    assert stored["summary"]["sdkPackageCandidates"] >= 4
    assert stored["summary"]["sandboxSnapshots"] >= 2
    assert stored["summary"]["publishedSdkPackages"] == 0
    assert stored["summary"]["liveSandboxTokenService"] is False
    assert stored["summary"]["externalPortalLive"] is False
    assert stored["portal"] == "contracts/fate/developer/developer-portal.json"
    assert stored["sdkReleaseBaseline"] == "contracts/fate/developer/sdk-release-baseline.json"
    assert stored["sandboxOutputSnapshot"] == "contracts/fate/developer/sandbox-output-snapshot.json"
    assert {item["status"] for item in stored["sdkSmokes"]} <= {"passed", "passed_shape_only"}
    assert {item["fixtureId"] for item in stored["sandboxSnapshots"]} == {
        "sandbox.almanac.travel.beijing.2026-05-08",
        "sandbox.meihua.number.beijing.test",
    }
    assert any("hosted developer portal" in item for item in stored["limitations"])
    assert any(item["name"] == "privacy:forbidden_fragments" and item["ok"] for item in stored["checks"])


def test_developer_portal_contracts_are_release_baseline_not_publication_claims():
    portal = json.loads((ROOT / "contracts/fate/developer/developer-portal.json").read_text(encoding="utf-8"))
    platform = json.loads((ROOT / "contracts/fate/developer/developer-platform.json").read_text(encoding="utf-8"))
    sdk = json.loads((ROOT / "contracts/fate/developer/sdk-release-baseline.json").read_text(encoding="utf-8"))
    snapshot = json.loads((ROOT / "contracts/fate/developer/sandbox-output-snapshot.json").read_text(encoding="utf-8"))
    changelog = json.loads((ROOT / "contracts/fate/developer/api-changelog.json").read_text(encoding="utf-8"))

    assert portal["status"] == "local_release_baseline"
    assert portal["externalPortalStatus"] == "not_implemented"
    assert platform["developerPortal"]["machineContract"] == "contracts/fate/developer/developer-portal.json"
    assert platform["sdkReleaseBaseline"]["machineContract"] == "contracts/fate/developer/sdk-release-baseline.json"
    assert platform["sandbox"]["fixedOutputSnapshotStatus"] == "local_fixed_snapshot"
    assert sdk["status"] == "local_release_candidate"
    assert sdk["packageRegistryStatus"] == "not_published"
    assert all(item["publishEvidence"] is None for item in sdk["packageCandidates"])
    assert snapshot["status"] == "local_fixed_snapshot"
    assert "full response bodies" in snapshot["privacyBoundary"]
    assert "api-changelog.0086.developer-portal-sdk-release-baseline" in {entry["id"] for entry in changelog["entries"]}
