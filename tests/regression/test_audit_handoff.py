from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PENDING_PHRASE = "外部连通验证待执行"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _git_pending_count() -> int:
    result = subprocess.run(
        ["git", "grep", "-n", "-I", PENDING_PHRASE],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode in {0, 1}, result.stderr
    count = len([line for line in result.stdout.splitlines() if line.strip()])
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert untracked.returncode == 0, untracked.stderr
    for path_text in untracked.stdout.splitlines():
        if not path_text or path_text.startswith(("infra/runtime/", ".venv/", "tools/reference-repos/")):
            continue
        path = ROOT / path_text
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            count += sum(1 for line in path.read_text(encoding="utf-8").splitlines() if PENDING_PHRASE in line)
        except UnicodeDecodeError:
            continue
    return count


def test_audit_handoff_generator_writes_markdown_and_json_with_all_pending_external_validations(tmp_path):
    output_dir = tmp_path / "audit-handoff"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/audit-handoff.py"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    payload = _load_json(output_dir / "audit-handoff.json")
    markdown = (output_dir / "AUDIT_HANDOFF.md").read_text(encoding="utf-8")

    assert summary["status"] == "passed"
    assert payload["kind"] == "fatecat.audit_handoff_bundle"
    assert payload["status"] == "passed"
    assert payload["pendingExternalValidationCount"] == _git_pending_count()
    assert len(payload["pendingExternalValidations"]) == payload["pendingExternalValidationCount"]
    assert payload["pendingExternalValidationCount"] > 0
    assert all(item["path"] and item["line"] and item["excerpt"] for item in payload["pendingExternalValidations"])
    assert "## Pending External Validations" in markdown
    assert "## Final Conclusion" in markdown
    serialized = json.dumps(payload, ensure_ascii=False).lower() + markdown.lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized
    assert "password" + "=" not in serialized


def test_audit_handoff_contract_and_local_ci_are_wired():
    contract = _load_json(ROOT / "contracts/fate/audit/handoff.json")
    local_ci = (ROOT / "scripts/local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts/AGENTS.md").read_text(encoding="utf-8")

    assert contract["kind"] == "fatecat.audit_handoff_contract"
    assert contract["pendingExternalValidationPolicy"]["requiredPhrase"] == PENDING_PHRASE
    assert "bash scripts/audit-handoff.sh --output-dir <dir>" == contract["generator"]["command"]
    assert "audit handoff" in local_ci
    assert "auditHandoff" in local_ci
    assert "audit-handoff.sh" in scripts_agents
