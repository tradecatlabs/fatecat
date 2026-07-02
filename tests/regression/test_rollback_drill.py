from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_rollback_drill_generates_dry_run_evidence(tmp_path):
    output_json = tmp_path / "rollback-drill.json"
    result = subprocess.run(
        [
            "bash",
            str(ROOT / "scripts/rollback-drill.sh"),
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
    assert output_json.is_file()

    payload = _load_json(output_json)
    assert payload["kind"] == "fatecat.rollback_drill_evidence"
    assert payload["status"] == "passed"
    assert payload["mode"] == "dry-run"
    assert payload["productionRollbackExecuted"] is False
    assert payload["candidateCommands"]
    assert all(command["executesInDryRun"] is False for command in payload["candidateCommands"])
    assert payload["requiredDocuments"]
    assert all(document["exists"] is True for document in payload["requiredDocuments"])


def test_live_release_gate_accepts_rollback_drill_evidence(tmp_path):
    rollback_json = tmp_path / "rollback-drill.json"
    gate_json = tmp_path / "live-release-gate.json"
    subprocess.run(
        [
            "bash",
            str(ROOT / "scripts/rollback-drill.sh"),
            "--output-json",
            str(rollback_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--rollback-evidence-path",
            str(rollback_json),
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
    assert checks["evidence.rollback_drill"]["status"] == "pass"
    assert payload["shipGate"]["status"] == "blocked"


def test_live_release_gate_rejects_invalid_rollback_drill_evidence(tmp_path):
    rollback_json = tmp_path / "rollback-drill.json"
    gate_json = tmp_path / "live-release-gate.json"
    subprocess.run(
        [
            "bash",
            str(ROOT / "scripts/rollback-drill.sh"),
            "--output-json",
            str(rollback_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = _load_json(rollback_json)
    payload["productionRollbackExecuted"] = True
    rollback_json.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--rollback-evidence-path",
            str(rollback_json),
            "--output-json",
            str(gate_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    gate = _load_json(gate_json)
    checks = {item["id"]: item for item in gate["checks"]}
    assert checks["evidence.rollback_drill"]["status"] == "fail"
    assert "productionRollbackExecuted must be false" in checks["evidence.rollback_drill"]["detail"]
