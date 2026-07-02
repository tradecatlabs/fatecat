from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_release_artifacts_generate_and_verify(tmp_path):
    output_dir = tmp_path / "release-artifacts"
    summary_path = tmp_path / "summary.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/release-artifacts.py"),
            "--output-dir",
            str(output_dir),
            "--summary-json",
            str(summary_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    stdout_summary = json.loads(result.stdout)
    assert stdout_summary["status"] == "passed"
    assert stdout_summary["artifacts"] == 2
    assert summary_path.is_file()

    sbom = _load_json(output_dir / "sbom.cyclonedx.json")
    provenance = _load_json(output_dir / "provenance.slsa.json")
    manifest = _load_json(output_dir / "release-artifacts-manifest.json")

    assert sbom["bomFormat"] == "CycloneDX"
    assert sbom["specVersion"] == "1.5"
    assert any(component["name"] == "fastapi" for component in sbom["components"])
    assert provenance["_type"] == "https://in-toto.io/Statement/v1"
    assert provenance["predicateType"] == "https://slsa.dev/provenance/v1"
    assert provenance["subject"][0]["name"] == "sbom.cyclonedx.json"
    assert manifest["resourceType"] == "ReleaseArtifactManifest"
    assert {item["type"] for item in manifest["artifacts"]} == {"sbom", "provenance"}
    serialized = json.dumps(manifest, ensure_ascii=False).lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized

    verify_result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/release-artifacts.py"),
            "--verify-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert verify_result.returncode == 0, verify_result.stderr
    assert json.loads(verify_result.stdout)["status"] == "passed"


def test_live_release_gate_accepts_generated_sbom_and_provenance(tmp_path):
    output_dir = tmp_path / "release-artifacts"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/release-artifacts.py"), "--output-dir", str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    gate_json = tmp_path / "live-release-gate.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--sbom-path",
            str(output_dir / "sbom.cyclonedx.json"),
            "--provenance-path",
            str(output_dir / "provenance.slsa.json"),
            "--output-json",
            str(gate_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = _load_json(gate_json)
    checks = {item["id"]: item for item in payload["checks"]}
    assert checks["evidence.sbom_artifact"]["status"] == "pass"
    assert checks["evidence.provenance_artifact"]["status"] == "pass"
    assert payload["shipGate"]["status"] == "blocked"
