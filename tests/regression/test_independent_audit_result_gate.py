from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "independent-audit-result-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "independent-audit-result.json"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _audit_result_bundle(*, decision: str = "accepted_with_findings", commit: str = "a" * 40) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.independent_audit_result_bundle",
        "source": {"commit": commit},
        "auditor": {
            "auditorRole": "independent_auditor",
            "organizationRef": "audit-artifact:org-hash-001",
            "identityProofRef": "evidence:auditor-identity-hash-001",
            "signedAt": "2026-07-04T00:00:00Z",
            "signedResultArtifactSha256": "b" * 64,
        },
        "result": {
            "decision": decision,
            "scopeHash": "c" * 64,
            "reportArtifactSha256": "d" * 64,
            "criticalFindings": 0,
            "highFindings": 0,
            "mediumFindings": 1 if decision == "accepted_with_findings" else 0,
            "lowFindings": 2 if decision == "accepted_with_findings" else 0,
            "redactionStatus": "redacted_no_secret_values",
        },
        "reviewedArtifacts": [
            {
                "id": "third-party-audit-rehearsal",
                "kind": "fatecat.third_party_audit_rehearsal",
                "sha256": "e" * 64,
            },
            {
                "id": "current-audit-bundle",
                "kind": "fatecat.current_audit_bundle",
                "sha256": "f" * 64,
            },
        ],
        "privacyBoundary": "redacted_no_secret_values",
    }


def test_independent_audit_result_contract_lists_boundaries() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.independent_audit_result_contract"
    assert contract["outputKind"] == "fatecat.independent_audit_result_gate"
    assert "independentAuditResult" in contract["requiredOutputFields"]
    assert "auditResultGate" in contract["requiredOutputFields"]
    assert contract["auditResultGatePolicy"]["productionBoundary"]
    assert "Does not create, simulate or replace an independent auditor result." in contract["nonClaims"]
    assert "https://" in contract["forbiddenFragments"]


def test_independent_audit_result_gate_defaults_to_external_pending() -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_independent_audit_result_gate_pending")

    gate = module.build_gate(expected_commit="a" * 40)

    assert gate["kind"] == "fatecat.independent_audit_result_gate"
    assert gate["status"] == "external_audit_result_pending"
    assert gate["summary"]["pendingResults"] == 1
    assert gate["summary"]["acceptedResults"] == 0
    assert gate["auditResultGate"]["status"] == "blocked"
    assert gate["shipGate"]["status"] == "blocked"
    assert "independent_audit_result_required" in gate["auditResultGate"]["blockingItems"]


def test_independent_audit_result_gate_accepts_redacted_signed_result(tmp_path: Path) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_independent_audit_result_gate_accepted")
    bundle_json = tmp_path / "independent-audit-result.json"
    _write_json(bundle_json, _audit_result_bundle())

    gate = module.build_gate(independent_audit_result_json=bundle_json, expected_commit="a" * 40)
    serialized = json.dumps(gate, ensure_ascii=False, sort_keys=True)

    assert gate["status"] == "accepted"
    assert gate["summary"]["acceptedResults"] == 1
    assert gate["summary"]["pendingResults"] == 0
    assert gate["summary"]["rejectedResults"] == 0
    assert gate["summary"]["reviewedArtifacts"] == 2
    assert gate["source"]["independentAuditResultBundleSha256"] == _sha256_file(bundle_json)
    assert gate["auditResultGate"]["status"] == "passed"
    assert gate["shipGate"]["status"] == "blocked"
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()


def test_independent_audit_result_gate_accepts_rejected_decision_as_blocking_result(tmp_path: Path) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_independent_audit_result_gate_rejected")
    bundle_json = tmp_path / "independent-audit-result.json"
    _write_json(bundle_json, _audit_result_bundle(decision="rejected"))

    gate = module.build_gate(independent_audit_result_json=bundle_json, expected_commit="a" * 40)

    assert gate["status"] == "rejected"
    assert gate["summary"]["rejectedResults"] == 1
    assert gate["auditResultGate"]["status"] == "blocked"
    assert "independent_auditor_rejected_release" in gate["auditResultGate"]["blockingItems"]


def test_independent_audit_result_gate_rejects_raw_url_sensitive_placeholder_and_commit_mismatch(
    tmp_path: Path,
) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_independent_audit_result_gate_negative")

    bundle = _audit_result_bundle()
    bundle["auditor"]["identityProofRef"] = "https://example.invalid/auditor"
    bundle_json = tmp_path / "audit-result-url.json"
    _write_json(bundle_json, bundle)
    result = module.main(
        [
            "--independent-audit-result-json",
            str(bundle_json),
            "--output-json",
            str(tmp_path / "url-out.json"),
            "--expected-commit",
            "a" * 40,
        ]
    )
    assert result == 1

    bundle = _audit_result_bundle()
    bundle["auditor"]["identityProofRef"] = f"to{'ken'}=redacted"
    bundle_json = tmp_path / "audit-result-secret.json"
    _write_json(bundle_json, bundle)
    result = module.main(
        [
            "--independent-audit-result-json",
            str(bundle_json),
            "--output-json",
            str(tmp_path / "secret-out.json"),
            "--expected-commit",
            "a" * 40,
        ]
    )
    assert result == 1

    bundle = _audit_result_bundle()
    bundle["auditor"]["organizationRef"] = "placeholder proof"
    bundle_json = tmp_path / "audit-result-placeholder.json"
    _write_json(bundle_json, bundle)
    result = module.main(
        [
            "--independent-audit-result-json",
            str(bundle_json),
            "--output-json",
            str(tmp_path / "placeholder-out.json"),
            "--expected-commit",
            "a" * 40,
        ]
    )
    assert result == 1

    bundle = _audit_result_bundle(commit="b" * 40)
    bundle_json = tmp_path / "audit-result-commit-mismatch.json"
    _write_json(bundle_json, bundle)
    result = module.main(
        [
            "--independent-audit-result-json",
            str(bundle_json),
            "--output-json",
            str(tmp_path / "commit-out.json"),
            "--expected-commit",
            "a" * 40,
        ]
    )
    assert result == 1


def test_independent_audit_result_gate_cli_outputs_summary(tmp_path: Path) -> None:
    bundle_json = tmp_path / "independent-audit-result.json"
    output_json = tmp_path / "independent-audit-result-gate.json"
    _write_json(bundle_json, _audit_result_bundle(decision="accepted_no_findings"))

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--independent-audit-result-json",
            str(bundle_json),
            "--output-json",
            str(output_json),
            "--expected-commit",
            "a" * 40,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    cli_summary = json.loads(result.stdout)

    assert cli_summary["kind"] == "fatecat.independent_audit_result_gate"
    assert cli_summary["status"] == "accepted"
    assert cli_summary["auditResultGate"] == "passed"
    assert cli_summary["shipGate"] == "blocked"
    assert cli_summary["acceptedResults"] == 1
    assert output_json.is_file()


def test_independent_audit_result_gate_wiring_mentions_local_ci_docs_and_agents() -> None:
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "independent audit result gate" in local_ci
    assert "FATE_LOCAL_CI_INDEPENDENT_AUDIT_RESULT_GATE" in local_ci
    assert "independent-audit-result-gate.py" in scripts_agents
    assert "independent-audit-result.json" in audit_agents
    assert "test_independent_audit_result_gate.py" in tests_agents
    assert "Post-0140 Independent Audit Result Intake" in roadmap
