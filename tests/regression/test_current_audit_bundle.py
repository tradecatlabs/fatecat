from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def _build_local_inputs(tmp_path: Path) -> dict[str, Path]:
    release_dir = tmp_path / "release-artifacts"
    rollback_json = tmp_path / "rollback-drill.json"
    handoff_dir = tmp_path / "audit-handoff"
    dry_run_dir = tmp_path / "audit-dry-run"
    proof_json = tmp_path / "current-release-proof.json"
    evidence_coverage_json = tmp_path / "evidence-coverage-trend-gate.json"
    runtime_proof_json = tmp_path / "runtime-proof-gate.json"
    evaluation_trend_dir = tmp_path / "evaluation-trend-gate-smoke"

    assert (
        _run([sys.executable, str(ROOT / "scripts/release-artifacts.py"), "--output-dir", str(release_dir)]).returncode
        == 0
    )
    assert (
        _run(
            [
                "bash",
                str(ROOT / "scripts/rollback-drill.sh"),
                "--output-json",
                str(rollback_json),
                "--release-artifacts-dir",
                str(release_dir),
            ]
        ).returncode
        == 0
    )
    assert (
        _run([sys.executable, str(ROOT / "scripts/audit-handoff.py"), "--output-dir", str(handoff_dir)]).returncode == 0
    )
    assert (
        _run(
            [
                sys.executable,
                str(ROOT / "scripts/audit-handoff-dry-run.py"),
                "--bundle-json",
                str(handoff_dir / "audit-handoff.json"),
                "--bundle-markdown",
                str(handoff_dir / "AUDIT_HANDOFF.md"),
                "--output-dir",
                str(dry_run_dir),
            ]
        ).returncode
        == 0
    )
    assert (
        _run(
            [
                sys.executable,
                str(ROOT / "scripts/current-release-proof.py"),
                "--skip-remote",
                "--rollback-evidence-path",
                str(rollback_json),
                "--output-json",
                str(proof_json),
            ]
        ).returncode
        == 0
    )
    assert (
        _run(
            [
                sys.executable,
                str(ROOT / "scripts/evidence-coverage-trend-gate.py"),
                "--output-json",
                str(evidence_coverage_json),
            ]
        ).returncode
        == 0
    )
    assert (
        _run(
            [
                "bash",
                str(ROOT / "scripts/evaluation-trend-gate-smoke.sh"),
                "--output-dir",
                str(evaluation_trend_dir),
            ]
        ).returncode
        == 0
    )
    assert (
        _run(
            [
                sys.executable,
                str(ROOT / "scripts/runtime-proof-gate.py"),
                "--output-json",
                str(runtime_proof_json),
            ]
        ).returncode
        == 0
    )
    return {
        "local_ci_output_dir": tmp_path,
        "release_dir": release_dir,
        "rollback_json": rollback_json,
        "handoff_json": handoff_dir / "audit-handoff.json",
        "handoff_markdown": handoff_dir / "AUDIT_HANDOFF.md",
        "dry_run_json": dry_run_dir / "audit-dry-run.json",
        "proof_json": proof_json,
    }


def test_current_audit_bundle_generates_local_blocked_bundle(tmp_path):
    inputs = _build_local_inputs(tmp_path)
    output_dir = tmp_path / "current-audit-bundle"

    result = _run(
        [
            sys.executable,
            str(ROOT / "scripts/current-audit-bundle.py"),
            "--output-dir",
            str(output_dir),
            "--audit-handoff-json",
            str(inputs["handoff_json"]),
            "--audit-handoff-markdown",
            str(inputs["handoff_markdown"]),
            "--audit-dry-run-json",
            str(inputs["dry_run_json"]),
            "--current-release-proof",
            str(inputs["proof_json"]),
            "--rollback-evidence-path",
            str(inputs["rollback_json"]),
            "--release-artifacts-dir",
            str(inputs["release_dir"]),
            "--local-ci-output-dir",
            str(inputs["local_ci_output_dir"]),
        ]
    )

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    bundle = _load_json(output_dir / "current-audit-bundle.json")
    markdown = (output_dir / "CURRENT_AUDIT_BUNDLE.md").read_text(encoding="utf-8")
    evidence_index = _load_json(output_dir / "evidence-index.json")
    risk_register = _load_json(output_dir / "risk-register.json")
    pending = _load_json(output_dir / "pending-external-validations.json")

    assert summary["status"] == "passed"
    assert summary["auditGate"] == "blocked"
    assert bundle["kind"] == "fatecat.current_audit_bundle"
    assert bundle["auditGate"]["status"] == "blocked"
    assert bundle["pendingExternalValidationCount"] == len(pending)
    assert {item["id"] for item in evidence_index} >= {
        "evidence.audit_handoff_json",
        "evidence.current_release_proof",
        "evidence.rollback_drill",
        "evidence.release_artifacts_manifest",
        "evidence.evidence_coverage_trend_gate",
        "evidence.evaluation_trend_gate",
        "evidence.runtime_proof_gate",
    }
    evidence_trend = next(item for item in evidence_index if item["id"] == "evidence.evidence_coverage_trend_gate")
    assert evidence_trend["status"] == "pass"
    assert "brokenRuleRefs=0" in evidence_trend["detail"]
    evaluation_trend = next(item for item in evidence_index if item["id"] == "evidence.evaluation_trend_gate")
    assert evaluation_trend["status"] == "pass"
    assert "latestStatus=passed" in evaluation_trend["detail"]
    runtime_proof = next(item for item in evidence_index if item["id"] == "evidence.runtime_proof_gate")
    assert runtime_proof["status"] == "pass"
    assert "runtimeProofStatus=external_connectivity_pending" in runtime_proof["detail"]
    assert any(item["id"] == "risk.external_validations_pending" for item in risk_register)
    assert "## Evidence Index" in markdown
    assert "## Final Conclusion" in markdown
    serialized = json.dumps(bundle, ensure_ascii=False).lower() + markdown.lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized
    assert "password" + "=" not in serialized


def test_current_audit_bundle_required_mode_rejects_local_contract_proof(tmp_path):
    inputs = _build_local_inputs(tmp_path)
    output_dir = tmp_path / "current-audit-bundle"

    result = _run(
        [
            sys.executable,
            str(ROOT / "scripts/current-audit-bundle.py"),
            "--require-current-release",
            "--output-dir",
            str(output_dir),
            "--audit-handoff-json",
            str(inputs["handoff_json"]),
            "--audit-handoff-markdown",
            str(inputs["handoff_markdown"]),
            "--audit-dry-run-json",
            str(inputs["dry_run_json"]),
            "--current-release-proof",
            str(inputs["proof_json"]),
            "--rollback-evidence-path",
            str(inputs["rollback_json"]),
            "--release-artifacts-dir",
            str(inputs["release_dir"]),
            "--local-ci-output-dir",
            str(inputs["local_ci_output_dir"]),
        ]
    )

    assert result.returncode == 1
    bundle = _load_json(output_dir / "current-audit-bundle.json")
    assert bundle["auditGate"]["status"] == "failed"
    assert "evidence.current_release_proof" in bundle["auditGate"]["blockingItems"]


def test_current_audit_bundle_required_mode_accepts_synthetic_current_proof(tmp_path):
    inputs = _build_local_inputs(tmp_path)
    output_dir = tmp_path / "current-audit-bundle"
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    local_ci = tmp_path / "summary.json"
    local_ci.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.local_ci_summary",
                "status": "passed",
                "profile": "quick",
                "commit": commit,
                "git": {"branch": branch, "dirtyCount": 0, "untrackedCount": 0},
                "artifacts": {},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    proof = tmp_path / "current-release-proof-passed.json"
    proof.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.current_release_proof",
                "status": "passed",
                "mode": "required-current-release",
                "git": {"branch": branch, "commit": commit, "originHead": commit, "dirtyCount": 0},
                "github": {"repo": "tradecatlabs/fatecat", "acceptanceRunId": 1, "containerRunId": 2},
                "container": {
                    "image": "ghcr.io/tradecatlabs/fatecat-delivery",
                    "tag": commit[:12],
                    "digest": "sha256:" + "1" * 64,
                },
                "proofGate": {"status": "passed", "blockingItems": [], "failedItems": [], "pendingItems": []},
                "checks": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = _run(
        [
            sys.executable,
            str(ROOT / "scripts/current-audit-bundle.py"),
            "--require-current-release",
            "--output-dir",
            str(output_dir),
            "--local-ci-summary",
            str(local_ci),
            "--audit-handoff-json",
            str(inputs["handoff_json"]),
            "--audit-handoff-markdown",
            str(inputs["handoff_markdown"]),
            "--audit-dry-run-json",
            str(inputs["dry_run_json"]),
            "--current-release-proof",
            str(proof),
            "--rollback-evidence-path",
            str(inputs["rollback_json"]),
            "--release-artifacts-dir",
            str(inputs["release_dir"]),
            "--local-ci-output-dir",
            str(inputs["local_ci_output_dir"]),
        ]
    )

    bundle = _load_json(output_dir / "current-audit-bundle.json")
    dirty_count = int(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).count("\n"))
    if dirty_count:
        assert result.returncode == 1
        assert bundle["auditGate"]["status"] == "failed"
        assert bundle["auditGate"]["blockingItems"] == ["git.clean"]
    else:
        assert result.returncode == 0, result.stderr
        assert bundle["auditGate"]["status"] == "passed"


def test_current_audit_bundle_contract_and_local_ci_are_wired():
    contract = _load_json(ROOT / "contracts/fate/audit/current-bundle.json")
    local_ci = (ROOT / "scripts/local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts/AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts/fate/audit/AGENTS.md").read_text(encoding="utf-8")

    assert contract["kind"] == "fatecat.current_audit_bundle_contract"
    assert "current-audit-bundle.json" in contract["requiredOutputs"]
    assert "current audit bundle" in local_ci
    assert "currentAuditBundle" in local_ci
    assert "--local-ci-output-dir" in local_ci
    assert any("local-ci gate artifacts" in item for item in contract["evidenceSources"])
    assert any("evaluation trend gate" in item for item in contract["evidenceSources"])
    assert "current-audit-bundle.sh" in scripts_agents
    assert "current-bundle.json" in audit_agents
