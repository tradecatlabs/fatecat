from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-tracker-issue-evidence-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-issue-evidence.json"


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


def _tracker_import_package() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_tracker_import_package",
        "status": "operator_action_required",
        "generatedAt": "2026-07-04T00:00:00Z",
        "source": {
            "issueExportKind": "fatecat.external_validation_issue_export",
            "issueExportSha256": "1" * 64,
            "issueExportCommit": "a" * 40,
            "commit": "a" * 40,
        },
        "summary": {"issueTemplates": 2, "issueFiles": 2, "commands": 2, "externalPending": 2},
        "packageGate": {"status": "blocked", "blockingItems": ["tracker_issue_creation_required"]},
        "trackerImport": {
            "tracker": "github_issues",
            "format": "github_cli_command_text_and_markdown_body_files",
            "createsIssues": False,
            "executesCommands": False,
            "commandFile": "gh-issue-create-commands.txt",
        },
        "files": [
            {
                "id": "external-validation-issue.external-work.category-1",
                "workItemId": "external-work.category-1",
                "category": "runtime.category_1",
                "owner": "owner-1",
                "path": "issues/external-validation-issue.external-work.category-1.md",
                "sha256": "b" * 64,
            },
            {
                "id": "external-validation-issue.external-work.category-2",
                "workItemId": "external-work.category-2",
                "category": "runtime.category_2",
                "owner": "owner-2",
                "path": "issues/external-validation-issue.external-work.category-2.md",
                "sha256": "c" * 64,
            },
        ],
        "commands": [
            {
                "id": "tracker-import-command.external-validation-issue.external-work.category-1",
                "issueTemplateId": "external-validation-issue.external-work.category-1",
                "workItemId": "external-work.category-1",
                "bodyFile": "issues/external-validation-issue.external-work.category-1.md",
                "command": "gh issue create --title '[External Validation] runtime/category-1' --body-file issue-1.md",
                "sha256": "d" * 64,
                "execution": "manual_review_required",
            },
            {
                "id": "tracker-import-command.external-validation-issue.external-work.category-2",
                "issueTemplateId": "external-validation-issue.external-work.category-2",
                "workItemId": "external-work.category-2",
                "bodyFile": "issues/external-validation-issue.external-work.category-2.md",
                "command": "gh issue create --title '[External Validation] runtime/category-2' --body-file issue-2.md",
                "sha256": "e" * 64,
                "execution": "manual_review_required",
            },
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not create issues in GitHub or any external tracker."],
    }


def _issue_evidence(package_sha256: str, *, issues: list[dict] | None = None) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_tracker_issue_evidence_bundle",
        "source": {
            "trackerImportPackageKind": "fatecat.external_validation_tracker_import_package",
            "trackerImportPackageSha256": package_sha256,
            "commit": "a" * 40,
        },
        "issues": issues
        if issues is not None
        else [
            _accepted_issue(
                work_item_id="external-work.category-1",
                issue_template_id="external-validation-issue.external-work.category-1",
                issue_ref="github:tradecatlabs/fatecat#101",
                body_sha256="b" * 64,
                artifact_sha256="1" * 64,
            ),
            _accepted_issue(
                work_item_id="external-work.category-2",
                issue_template_id="external-validation-issue.external-work.category-2",
                issue_ref="github:tradecatlabs/fatecat#102",
                body_sha256="c" * 64,
                artifact_sha256="2" * 64,
            ),
        ],
    }


def _accepted_issue(
    *,
    work_item_id: str,
    issue_template_id: str,
    issue_ref: str,
    body_sha256: str,
    artifact_sha256: str,
) -> dict:
    return {
        "workItemId": work_item_id,
        "issueTemplateId": issue_template_id,
        "trackerIssueRef": issue_ref,
        "titleSha256": "f" * 64,
        "bodySha256": body_sha256,
        "artifactSha256": artifact_sha256,
        "labels": ["external-validation", "measurement-infrastructure", "operator-action-required"],
        "createdAt": "2026-07-04T00:00:00Z",
        "createdByRole": "operator",
        "redactionStatus": "redacted_no_secret_values",
    }


def test_tracker_issue_evidence_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_tracker_issue_evidence_contract"
    assert contract["outputKind"] == "fatecat.external_validation_tracker_issue_evidence_gate"
    assert "issueCreation" in contract["requiredOutputFields"]
    assert "issueEvidenceGate" in contract["requiredOutputFields"]
    assert "shipGate" in contract["requiredOutputFields"]
    assert contract["evidenceBundlePolicy"]["createsIssues"] is False
    assert contract["evidenceBundlePolicy"]["executesCommands"] is False


def test_tracker_issue_evidence_gate_defaults_to_pending_without_external_evidence(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_gate")
    package_json = tmp_path / "tracker-import-package.json"
    _write_json(package_json, _tracker_import_package())

    gate = module.build_gate(tracker_import_package_json=package_json, expected_commit="a" * 40)

    assert gate["kind"] == "fatecat.external_validation_tracker_issue_evidence_gate"
    assert gate["status"] == "external_connectivity_pending"
    assert gate["summary"]["workItems"] == 2
    assert gate["summary"]["acceptedIssues"] == 0
    assert gate["summary"]["pendingIssues"] == 2
    assert gate["issueCreation"]["createsIssues"] is False
    assert gate["issueEvidenceGate"]["status"] == "blocked"
    assert gate["shipGate"]["status"] == "blocked"


def test_tracker_issue_evidence_gate_accepts_full_redacted_issue_binding(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_gate_accepted")
    package_json = tmp_path / "tracker-import-package.json"
    evidence_json = tmp_path / "issue-evidence.json"
    _write_json(package_json, _tracker_import_package())
    _write_json(evidence_json, _issue_evidence(_sha256_file(package_json)))

    gate = module.build_gate(
        tracker_import_package_json=package_json,
        issue_evidence_json=evidence_json,
        expected_commit="a" * 40,
    )
    serialized = json.dumps(gate, ensure_ascii=False, sort_keys=True)

    assert gate["status"] == "accepted"
    assert gate["summary"]["acceptedIssues"] == 2
    assert gate["summary"]["pendingIssues"] == 0
    assert gate["summary"]["rejectedIssues"] == 0
    assert gate["issueEvidenceGate"]["status"] == "passed"
    assert gate["shipGate"]["status"] == "blocked"
    assert "github:tradecatlabs/fatecat#101" in serialized
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()


def test_tracker_issue_evidence_gate_rejects_raw_url_sensitive_and_placeholder(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_gate_negative")
    package_json = tmp_path / "tracker-import-package.json"
    _write_json(package_json, _tracker_import_package())
    package_sha256 = _sha256_file(package_json)

    evidence = _issue_evidence(package_sha256)
    evidence["issues"][0]["trackerIssueRef"] = "https://github.com/tradecatlabs/fatecat/issues/101"
    evidence_json = tmp_path / "issue-evidence-url.json"
    _write_json(evidence_json, evidence)
    try:
        module.build_gate(
            tracker_import_package_json=package_json,
            issue_evidence_json=evidence_json,
            expected_commit="a" * 40,
        )
    except Exception as exc:  # noqa: BLE001
        assert "raw URL" in str(exc)
    else:
        raise AssertionError("raw URL should be rejected")

    evidence = _issue_evidence(package_sha256)
    evidence["issues"][0]["artifactSha256"] = f"to{'ken'}=redacted"
    evidence_json = tmp_path / "issue-evidence-secret.json"
    _write_json(evidence_json, evidence)
    try:
        module.build_gate(
            tracker_import_package_json=package_json,
            issue_evidence_json=evidence_json,
            expected_commit="a" * 40,
        )
    except Exception as exc:  # noqa: BLE001
        assert "sensitive-looking assignment" in str(exc)
    else:
        raise AssertionError("sensitive assignment should be rejected")

    evidence = _issue_evidence(package_sha256)
    evidence["issues"][0]["createdByRole"] = "placeholder proof"
    evidence_json = tmp_path / "issue-evidence-placeholder.json"
    _write_json(evidence_json, evidence)
    try:
        module.build_gate(
            tracker_import_package_json=package_json,
            issue_evidence_json=evidence_json,
            expected_commit="a" * 40,
        )
    except Exception as exc:  # noqa: BLE001
        assert "forbidden marker" in str(exc)
    else:
        raise AssertionError("placeholder marker should be rejected")


def test_tracker_issue_evidence_gate_blocks_mismatch_unknown_and_duplicate(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_gate_rejected")
    package_json = tmp_path / "tracker-import-package.json"
    evidence_json = tmp_path / "issue-evidence.json"
    _write_json(package_json, _tracker_import_package())
    package_sha256 = _sha256_file(package_json)
    issues = [
        _accepted_issue(
            work_item_id="external-work.category-1",
            issue_template_id="external-validation-issue.external-work.category-1",
            issue_ref="github:tradecatlabs/fatecat#101",
            body_sha256="0" * 64,
            artifact_sha256="1" * 64,
        ),
        _accepted_issue(
            work_item_id="external-work.category-9",
            issue_template_id="external-validation-issue.external-work.category-9",
            issue_ref="github:tradecatlabs/fatecat#109",
            body_sha256="9" * 64,
            artifact_sha256="9" * 64,
        ),
        _accepted_issue(
            work_item_id="external-work.category-2",
            issue_template_id="external-validation-issue.external-work.category-2",
            issue_ref="github:tradecatlabs/fatecat#102",
            body_sha256="c" * 64,
            artifact_sha256="2" * 64,
        ),
        _accepted_issue(
            work_item_id="external-work.category-2",
            issue_template_id="external-validation-issue.external-work.category-2",
            issue_ref="github:tradecatlabs/fatecat#103",
            body_sha256="c" * 64,
            artifact_sha256="3" * 64,
        ),
    ]
    _write_json(evidence_json, _issue_evidence(package_sha256, issues=issues))

    gate = module.build_gate(
        tracker_import_package_json=package_json,
        issue_evidence_json=evidence_json,
        expected_commit="a" * 40,
    )

    assert gate["summary"]["acceptedIssues"] == 1
    assert gate["summary"]["rejectedIssues"] == 3
    assert gate["summary"]["pendingIssues"] == 1
    assert gate["issueEvidenceGate"]["status"] == "blocked"
    assert {issue["reason"] for issue in gate["rejectedIssues"]} == {
        "body_sha256_mismatch",
        "unknown_work_item",
        "duplicate_work_item",
    }


def test_tracker_issue_evidence_gate_cli_outputs_summary(tmp_path):
    package_json = tmp_path / "tracker-import-package.json"
    output_json = tmp_path / "tracker-issue-evidence-gate.json"
    _write_json(package_json, _tracker_import_package())

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--tracker-import-package-json",
            str(package_json),
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

    assert cli_summary["kind"] == "fatecat.external_validation_tracker_issue_evidence_gate"
    assert cli_summary["issueEvidenceGate"] == "blocked"
    assert cli_summary["shipGate"] == "blocked"
    assert cli_summary["acceptedIssues"] == 0
    assert cli_summary["pendingIssues"] == 2
    assert output_json.is_file()


def test_tracker_issue_evidence_gate_wiring_mentions_local_ci_docs_and_agents():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external validation tracker issue evidence gate" in local_ci
    assert "externalValidationTrackerIssueEvidenceGate" in local_ci
    assert "external-validation-tracker-issue-evidence-gate.py" in scripts_agents
    assert "external-validation-tracker-issue-evidence.json" in audit_agents
    assert "test_external_validation_tracker_issue_evidence_gate.py" in tests_agents
    assert "Post-0132 External Validation Tracker Issue Evidence Gate" in roadmap
