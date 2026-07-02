from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_audit_handoff_dry_run_verifies_bundle_and_keeps_ship_gate_blocked(tmp_path):
    handoff_dir = tmp_path / "handoff"
    handoff = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/audit-handoff.py"),
            "--output-dir",
            str(handoff_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert handoff.returncode == 0, handoff.stderr

    dry_run_dir = tmp_path / "dry-run"
    dry_run = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/audit-handoff-dry-run.py"),
            "--bundle-json",
            str(handoff_dir / "audit-handoff.json"),
            "--bundle-markdown",
            str(handoff_dir / "AUDIT_HANDOFF.md"),
            "--output-dir",
            str(dry_run_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert dry_run.returncode == 0, dry_run.stderr
    summary = json.loads(dry_run.stdout)
    report = _load_json(dry_run_dir / "audit-dry-run.json")
    markdown = (dry_run_dir / "AUDIT_DRY_RUN.md").read_text(encoding="utf-8")

    assert summary["status"] == "passed"
    assert summary["shipGate"] == "blocked"
    assert report["kind"] == "fatecat.audit_handoff_dry_run"
    assert report["status"] == "passed"
    assert report["shipGate"]["status"] == "blocked"
    assert any("pendingExternalValidationCount=" in reason for reason in report["shipGate"]["reasons"])
    assert all(check["status"] == "passed" for check in report["checks"])
    assert "## Non Claims" in markdown
    serialized = json.dumps(report, ensure_ascii=False).lower() + markdown.lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized
    assert "password" + "=" not in serialized


def test_audit_dry_run_contract_and_local_ci_are_wired():
    contract = _load_json(ROOT / "contracts/fate/audit/dry-run.json")
    local_ci = (ROOT / "scripts/local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts/AGENTS.md").read_text(encoding="utf-8")

    assert contract["kind"] == "fatecat.audit_dry_run_contract"
    assert "shipGatePolicy" in contract
    assert (
        "bash scripts/audit-handoff-dry-run.sh --bundle-json <json> --bundle-markdown <md> --output-dir <dir>"
        == contract["verifier"]["command"]
    )
    assert "audit handoff dry-run" in local_ci
    assert "auditDryRun" in local_ci
    assert "audit-handoff-dry-run.sh" in scripts_agents
