from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _proof_module():
    module_path = ROOT / "scripts/current-release-proof.py"
    spec = importlib.util.spec_from_file_location("current_release_proof", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_current_release_proof_local_contract_outputs_blocked(tmp_path):
    output_json = tmp_path / "current-release-proof.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/current-release-proof.py"),
            "--skip-remote",
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["status"] == "passed"
    assert summary["proofGate"] in {"blocked", "fail"}
    payload = _load_json(output_json)
    assert payload["kind"] == "fatecat.current_release_proof"
    assert payload["mode"] == "local-contract"
    checks = {item["id"]: item for item in payload["checks"]}
    assert checks["release.acceptance_current_commit"]["status"] == "pending"
    assert checks["release.container_workflow_current_commit"]["status"] == "pending"
    assert checks["release.container_registry_digest"]["status"] == "pending"
    assert checks["release.container_attestation"]["status"] == "pending"
    assert checks["release.release_artifacts_uploaded"]["status"] == "pending"
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized
    assert "password" + "=" not in serialized


def test_current_release_proof_required_mode_fails_without_remote(tmp_path):
    output_json = tmp_path / "current-release-proof-required.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/current-release-proof.py"),
            "--skip-remote",
            "--require-current-release",
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    summary = json.loads(result.stdout)
    assert summary["status"] == "failed"
    payload = _load_json(output_json)
    assert payload["proofGate"]["status"] in {"blocked", "fail"}
    assert "release.container_registry_digest" in payload["proofGate"]["pendingItems"]


def test_release_gate_contract_declares_current_release_proof():
    gate = _load_json(ROOT / "contracts/fate/delivery/release-gate.json")
    registry = _load_json(ROOT / "contracts/fate/delivery/registry.json")

    expected_local = "bash scripts/current-release-proof.sh --skip-remote --output-json <path>"
    expected_external = (
        "bash scripts/current-release-proof.sh --require-current-release "
        "--rollback-evidence-path <rollback.json> --output-json <path>"
    )

    assert expected_local in gate["localVerification"]
    assert expected_external in gate["externalVerification"]
    assert expected_local in registry["releaseGate"]["localVerification"]
    assert expected_external in registry["releaseGate"]["externalVerification"]


def test_current_release_proof_accepts_remote_attestation_steps():
    module = _proof_module()
    ok, detail = module.attestation_steps_from_jobs(
        [
            {
                "name": "delivery-image",
                "steps": [
                    {"name": "Attest main image", "conclusion": "success"},
                    {"name": "Verify main image attestation", "conclusion": "success"},
                ],
            }
        ]
    )

    assert ok is True
    assert "attestation steps succeeded" in detail


def test_current_release_proof_rejects_missing_remote_attestation_step():
    module = _proof_module()
    ok, detail = module.attestation_steps_from_jobs(
        [
            {
                "name": "delivery-image",
                "steps": [
                    {"name": "Attest main image", "conclusion": "success"},
                ],
            }
        ]
    )

    assert ok is False
    assert "Verify main image attestation=missing" in detail
