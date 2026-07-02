from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def _write_container_evidence(path: Path, *, image_id: str | None = None, smoke_status: str = "passed") -> None:
    payload = {
        "schemaVersion": 1,
        "kind": "fatecat.container_release_evidence",
        "status": "passed",
        "image": "fatecat-delivery:test",
        "imageId": image_id or "sha256:" + "1" * 64,
        "repoDigests": [],
        "registryDigestPresent": False,
        "pushExecuted": False,
        "buildStatus": "passed",
        "smokeStatus": smoke_status,
        "generatedAt": "2026-07-02T00:00:00+00:00",
        "startedAt": "2026-07-02T00:00:00+00:00",
        "git": {"branch": "main", "commit": _git_head()},
        "docker": {"created": "", "architecture": "amd64", "os": "linux", "inspectError": ""},
        "commands": {"build": "bash scripts/container-build.sh", "smoke": "bash scripts/container-smoke.sh"},
        "outputs": {"build": "", "smoke": ""},
        "limitations": ["local test fixture"],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_container_release_evidence_script_help():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/container-release-evidence.py"), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--output-json" in result.stdout
    assert "--skip-build" in result.stdout


def test_live_release_gate_accepts_container_evidence(tmp_path):
    evidence = tmp_path / "container-release-evidence.json"
    gate_json = tmp_path / "live-release-gate.json"
    _write_container_evidence(evidence)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--container-evidence-path",
            str(evidence),
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
    assert checks["evidence.container_digest"]["status"] == "pass"
    assert payload["shipGate"]["status"] == "blocked"


def test_live_release_gate_rejects_invalid_container_evidence(tmp_path):
    evidence = tmp_path / "container-release-evidence.json"
    gate_json = tmp_path / "live-release-gate.json"
    _write_container_evidence(evidence, image_id="sha256:not-a-digest", smoke_status="failed")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--container-evidence-path",
            str(evidence),
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
    assert checks["evidence.container_digest"]["status"] == "fail"
    assert "imageId must be sha256" in checks["evidence.container_digest"]["detail"]
    assert "smokeStatus must be passed" in checks["evidence.container_digest"]["detail"]
