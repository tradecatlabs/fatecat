from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "third-party-audit-rehearsal.py"
CONTRACT = ROOT / "contracts" / "fate" / "audit" / "third-party-audit-rehearsal.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("third_party_audit_rehearsal", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _fixtures(tmp_path: Path) -> dict[str, Path]:
    current_audit_bundle = {
        "kind": "fatecat.current_audit_bundle",
        "status": "passed",
        "git": {"commit": "abc123", "clean": True},
        "auditGate": {"status": "blocked", "blockingItems": ["evidence.current_release_proof"]},
        "pendingExternalValidationCount": 416,
    }
    audit_dry_run = {
        "kind": "fatecat.audit_handoff_dry_run",
        "status": "passed",
        "shipGate": {"status": "blocked", "reasons": ["pendingExternalValidationCount=416"]},
    }
    current_release_proof = {
        "kind": "fatecat.current_release_proof",
        "status": "passed",
        "mode": "local-contract",
        "git": {"commit": "abc123"},
        "proofGate": {"status": "blocked", "blockingItems": ["remote_ci_pending"]},
    }
    certification = {
        "kind": "fatecat.measurement_infrastructure_certification",
        "status": "blocked",
        "certificationGate": {"canClaim100Percent": False},
        "domains": [{"id": "audit", "status": "blocked"}],
        "externalPending": [{"domain": "audit", "reason": "proofRefStatus=external_connectivity_pending"}],
        "blockingItems": [{"domain": "audit", "reason": "blocked_gate"}],
    }
    closure_summary = {
        "kind": "fatecat.external_validation_closure_evidence_summary",
        "status": "passed",
        "summary": {"domains": 2, "workItems": 2, "externalPending": 2},
        "closureGate": {"status": "blocked", "blockingItems": {"proof_ref_missing": 2}},
        "externalPending": [
            {
                "workItemId": "external-validation.runtime.postgres_live",
                "domain": "runtime",
                "category": "runtime.postgres_live",
                "owner": "runtime",
                "blockingItems": ["proof_ref_missing", "category_live_evidence_missing"],
                "nextAction": "execute_category_runbook_and_submit_redacted_proof_ref",
            },
            {
                "workItemId": "external-validation.audit.third_party_review",
                "domain": "audit",
                "category": "audit.third_party_review",
                "owner": "audit",
                "blockingItems": ["proof_ref_missing", "category_live_evidence_missing"],
                "nextAction": "execute_category_runbook_and_submit_redacted_proof_ref",
            },
        ],
    }
    tracker_import_package = {
        "kind": "fatecat.external_validation_tracker_import_package",
        "status": "operator_action_required",
        "summary": {"issueTemplates": 2, "issueFiles": 2, "commands": 2, "externalPending": 2},
        "packageGate": {
            "status": "blocked",
            "blockingItems": ["tracker_issue_creation_required", "proof_ref_bundle_required"],
        },
    }
    tracker_issue_template = {
        "kind": "fatecat.external_validation_tracker_issue_evidence_bundle_template",
        "status": "operator_action_required",
        "summary": {"workItems": 2, "readyToSubmitToGate": False},
        "templateGate": {
            "status": "operator_action_required",
            "blockingItems": ["tracker_issue_ref_fill_required", "artifact_sha256_fill_required"],
        },
    }
    tracker_issue_gate = {
        "kind": "fatecat.external_validation_tracker_issue_evidence_gate",
        "status": "external_connectivity_pending",
        "summary": {"acceptedIssues": 0, "pendingIssues": 2, "rejectedIssues": 0},
        "issueEvidenceGate": {
            "status": "blocked",
            "blockingItems": ["tracker_issue_creation_evidence_required"],
        },
        "shipGate": {"status": "blocked", "blockingItems": ["external_validation_live_proof_gate_required"]},
    }
    return {
        "current_audit_bundle": _write(tmp_path / "current-audit-bundle.json", current_audit_bundle),
        "audit_dry_run": _write(tmp_path / "audit-dry-run.json", audit_dry_run),
        "current_release_proof": _write(tmp_path / "current-release-proof.json", current_release_proof),
        "certification": _write(tmp_path / "measurement-infrastructure-certification.json", certification),
        "closure_summary": _write(tmp_path / "external-validation-closure-evidence-summary.json", closure_summary),
        "tracker_import_package": _write(
            tmp_path / "external-validation-tracker-import-package.json", tracker_import_package
        ),
        "tracker_issue_template": _write(
            tmp_path / "external-validation-tracker-issue-evidence-template.json", tracker_issue_template
        ),
        "tracker_issue_gate": _write(
            tmp_path / "external-validation-tracker-issue-evidence-gate.json", tracker_issue_gate
        ),
    }


def test_contract_declares_rehearsal_boundaries() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.third_party_audit_rehearsal_contract"
    assert "current-audit-bundle.json" in contract["requiredInputs"]
    assert "measurement-infrastructure-certification.json" in contract["requiredInputs"]
    assert "external-validation-closure-evidence-summary.json" in contract["requiredInputs"]
    assert "external-validation-tracker-import-package.json" in contract["requiredInputs"]
    assert "external-validation-tracker-issue-evidence-template.json" in contract["requiredInputs"]
    assert "external-validation-tracker-issue-evidence-gate.json" in contract["requiredInputs"]
    assert contract["requiredKinds"]["trackerImportPackage"] == "fatecat.external_validation_tracker_import_package"
    assert (
        contract["requiredKinds"]["trackerIssueEvidenceTemplate"]
        == "fatecat.external_validation_tracker_issue_evidence_bundle_template"
    )
    assert (
        contract["requiredKinds"]["trackerIssueEvidenceGate"]
        == "fatecat.external_validation_tracker_issue_evidence_gate"
    )
    assert "Does not replace third-party audit." in contract["nonClaims"]
    assert "rehearsalGate" in contract["requiredOutputFields"]
    assert "https://" in contract["forbiddenFragments"]


def test_build_report_keeps_rehearsal_blocked_with_external_pending(tmp_path: Path) -> None:
    module = _load_module()
    fixtures = _fixtures(tmp_path)
    output_json = tmp_path / "third-party-audit-rehearsal.json"
    output_markdown = tmp_path / "THIRD_PARTY_AUDIT_REHEARSAL.md"

    report, markdown = module.build_report(
        current_audit_bundle_json=fixtures["current_audit_bundle"],
        audit_dry_run_json=fixtures["audit_dry_run"],
        current_release_proof_json=fixtures["current_release_proof"],
        certification_json=fixtures["certification"],
        closure_evidence_summary_json=fixtures["closure_summary"],
        tracker_import_package_json=fixtures["tracker_import_package"],
        tracker_issue_evidence_template_json=fixtures["tracker_issue_template"],
        tracker_issue_evidence_gate_json=fixtures["tracker_issue_gate"],
        output_json=output_json,
        output_markdown=output_markdown,
    )

    assert report["kind"] == "fatecat.third_party_audit_rehearsal"
    assert report["status"] == "passed"
    assert report["rehearsalGate"]["status"] == "blocked"
    assert report["summary"]["evidenceInputs"] == 8
    assert report["summary"]["externalPending"] == 2
    assert any(item["id"] == "third_party.independent_result" for item in report["auditorChecklist"])
    evidence_ids = {item["id"] for item in report["evidenceIndex"]}
    assert "external_validation_tracker_import_package" in evidence_ids
    assert "external_validation_tracker_issue_evidence_template" in evidence_ids
    assert "external_validation_tracker_issue_evidence_gate" in evidence_ids
    checklist_ids = {item["id"] for item in report["auditorChecklist"]}
    assert "tracker.import_package_gate" in checklist_ids
    assert "tracker.issue_evidence_template_gate" in checklist_ids
    assert "tracker.issue_evidence_gate" in checklist_ids
    assert "Third-Party Audit Rehearsal" in markdown
    assert "external_validation_tracker_issue_evidence_gate" in markdown
    assert "third-party audit passed" not in json.dumps(report, ensure_ascii=False).lower()
    assert "https://" not in json.dumps(report, ensure_ascii=False)


def test_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    fixtures = _fixtures(tmp_path)
    output_json = tmp_path / "out" / "third-party-audit-rehearsal.json"
    output_markdown = tmp_path / "out" / "THIRD_PARTY_AUDIT_REHEARSAL.md"

    result = subprocess.run(
        [
            "python3",
            str(SCRIPT),
            "--current-audit-bundle-json",
            str(fixtures["current_audit_bundle"]),
            "--audit-dry-run-json",
            str(fixtures["audit_dry_run"]),
            "--current-release-proof-json",
            str(fixtures["current_release_proof"]),
            "--certification-json",
            str(fixtures["certification"]),
            "--closure-evidence-summary-json",
            str(fixtures["closure_summary"]),
            "--tracker-import-package-json",
            str(fixtures["tracker_import_package"]),
            "--tracker-issue-evidence-template-json",
            str(fixtures["tracker_issue_template"]),
            "--tracker-issue-evidence-gate-json",
            str(fixtures["tracker_issue_gate"]),
            "--output-json",
            str(output_json),
            "--output-markdown",
            str(output_markdown),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["rehearsalGate"]["status"] == "blocked"
    assert output_markdown.is_file()
    assert "rehearsalGate" in result.stdout


def test_rejects_raw_url_in_output(tmp_path: Path) -> None:
    module = _load_module()
    fixtures = _fixtures(tmp_path)
    closure_summary = json.loads(fixtures["closure_summary"].read_text(encoding="utf-8"))
    closure_summary["externalPending"][0]["category"] = "https://example.invalid/leak"
    fixtures["closure_summary"].write_text(json.dumps(closure_summary), encoding="utf-8")

    try:
        module.build_report(
            current_audit_bundle_json=fixtures["current_audit_bundle"],
            audit_dry_run_json=fixtures["audit_dry_run"],
            current_release_proof_json=fixtures["current_release_proof"],
            certification_json=fixtures["certification"],
            closure_evidence_summary_json=fixtures["closure_summary"],
            tracker_import_package_json=fixtures["tracker_import_package"],
            tracker_issue_evidence_template_json=fixtures["tracker_issue_template"],
            tracker_issue_evidence_gate_json=fixtures["tracker_issue_gate"],
            output_json=tmp_path / "out.json",
            output_markdown=tmp_path / "out.md",
        )
    except module.ThirdPartyAuditRehearsalError as exc:
        assert "raw URL" in str(exc)
    else:
        raise AssertionError("expected raw URL rejection")


def test_local_ci_and_agents_wiring() -> None:
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")

    assert "third-party audit rehearsal" in local_ci
    assert "third-party-audit-rehearsal.json" in local_ci
    assert "test_third_party_audit_rehearsal.py" in local_ci
    assert "third-party-audit-rehearsal.py" in scripts_agents
    assert "third-party-audit-rehearsal.json" in audit_agents
    assert "test_third_party_audit_rehearsal.py" in tests_agents
