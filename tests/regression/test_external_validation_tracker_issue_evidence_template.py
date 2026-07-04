from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-tracker-issue-evidence-template.py"
GATE_SCRIPT_PATH = ROOT / "scripts" / "external-validation-tracker-issue-evidence-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-issue-evidence-template.json"


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


def _fill_bundle_skeleton(template: dict) -> dict:
    bundle = json.loads(json.dumps(template["bundleSkeleton"]))
    for index, issue in enumerate(bundle["issues"], start=1):
        issue["trackerIssueRef"] = f"github:tradecatlabs/fatecat#{100 + index}"
        issue["titleSha256"] = f"{index}" * 64
        issue["artifactSha256"] = f"{index + 2}" * 64
        issue["createdAt"] = "2026-07-04T00:00:00Z"
        issue["createdByRole"] = "operator"
    return bundle


def test_tracker_issue_evidence_template_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_tracker_issue_evidence_template_contract"
    assert contract["outputKind"] == "fatecat.external_validation_tracker_issue_evidence_bundle_template"
    assert contract["targetEvidenceKind"] == "fatecat.external_validation_tracker_issue_evidence_bundle"
    assert "bundleSkeleton" in contract["requiredOutputFields"]
    assert "issueEvidenceItems" in contract["requiredOutputFields"]
    assert contract["templatePolicy"]["createsIssues"] is False
    assert contract["templatePolicy"]["executesCommands"] is False


def test_tracker_issue_evidence_template_builds_fillable_bundle_skeleton(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_template")
    package_json = tmp_path / "tracker-import-package.json"
    output_json = tmp_path / "template.json"
    output_markdown = tmp_path / "TEMPLATE.md"
    _write_json(package_json, _tracker_import_package())

    template = module.build_template(tracker_import_package_json=package_json, expected_commit="a" * 40)
    module.write_template(template=template, output_json=output_json, output_markdown=output_markdown)
    serialized = json.dumps(template, ensure_ascii=False, sort_keys=True)

    assert template["kind"] == "fatecat.external_validation_tracker_issue_evidence_bundle_template"
    assert template["status"] == "operator_action_required"
    assert template["summary"]["workItems"] == 2
    assert template["summary"]["readyToSubmitToGate"] is False
    assert template["templateGate"]["status"] == "operator_action_required"
    assert template["bundleSkeleton"]["kind"] == "fatecat.external_validation_tracker_issue_evidence_bundle"
    assert template["bundleSkeleton"]["issues"][0]["bodySha256"] == "b" * 64
    assert template["bundleSkeleton"]["issues"][0]["trackerIssueRef"] == ""
    assert output_json.is_file()
    assert output_markdown.is_file()
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()


def test_tracker_issue_evidence_template_skeleton_can_be_filled_and_accepted_by_gate(tmp_path):
    template_module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_template_filled")
    gate_module = _load_module(
        GATE_SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_gate_from_template"
    )
    package_json = tmp_path / "tracker-import-package.json"
    evidence_json = tmp_path / "issue-evidence.json"
    _write_json(package_json, _tracker_import_package())

    template = template_module.build_template(tracker_import_package_json=package_json, expected_commit="a" * 40)
    evidence_bundle = _fill_bundle_skeleton(template)
    _write_json(evidence_json, evidence_bundle)

    assert evidence_bundle["source"]["trackerImportPackageSha256"] == _sha256_file(package_json)
    gate = gate_module.build_gate(
        tracker_import_package_json=package_json,
        issue_evidence_json=evidence_json,
        expected_commit="a" * 40,
    )

    assert gate["status"] == "accepted"
    assert gate["summary"]["acceptedIssues"] == 2
    assert gate["summary"]["pendingIssues"] == 0
    assert gate["issueEvidenceGate"]["status"] == "passed"
    assert gate["shipGate"]["status"] == "blocked"


def test_tracker_issue_evidence_template_rejects_raw_url_and_sensitive_assignment(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_issue_evidence_template_negative")
    payload = _tracker_import_package()
    payload["files"][0]["owner"] = "https://example.invalid/owner"
    package_json = tmp_path / "tracker-import-package-url.json"
    _write_json(package_json, payload)

    try:
        module.build_template(tracker_import_package_json=package_json, expected_commit="a" * 40)
    except Exception as exc:  # noqa: BLE001
        assert "raw URL" in str(exc)
    else:
        raise AssertionError("raw URL should be rejected")

    payload = _tracker_import_package()
    payload["files"][0]["owner"] = f"to{'ken'}=redacted"
    package_json = tmp_path / "tracker-import-package-secret.json"
    _write_json(package_json, payload)

    try:
        module.build_template(tracker_import_package_json=package_json, expected_commit="a" * 40)
    except Exception as exc:  # noqa: BLE001
        assert "sensitive-looking assignment" in str(exc)
    else:
        raise AssertionError("sensitive assignment should be rejected")


def test_tracker_issue_evidence_template_cli_outputs_json_and_markdown(tmp_path):
    package_json = tmp_path / "tracker-import-package.json"
    output_json = tmp_path / "template.json"
    output_markdown = tmp_path / "TEMPLATE.md"
    _write_json(package_json, _tracker_import_package())

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--tracker-import-package-json",
            str(package_json),
            "--output-json",
            str(output_json),
            "--output-markdown",
            str(output_markdown),
            "--expected-commit",
            "a" * 40,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    cli_summary = json.loads(result.stdout)

    assert cli_summary["kind"] == "fatecat.external_validation_tracker_issue_evidence_bundle_template"
    assert cli_summary["templateGate"] == "operator_action_required"
    assert cli_summary["workItems"] == 2
    assert cli_summary["readyToSubmitToGate"] is False
    assert output_json.is_file()
    assert output_markdown.is_file()


def test_tracker_issue_evidence_template_wiring_mentions_local_ci_docs_and_agents():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external validation tracker issue evidence template" in local_ci
    assert "externalValidationTrackerIssueEvidenceTemplate" in local_ci
    assert "external-validation-tracker-issue-evidence-template.py" in scripts_agents
    assert "external-validation-tracker-issue-evidence-template.json" in audit_agents
    assert "test_external_validation_tracker_issue_evidence_template.py" in tests_agents
    assert "Post-0133 External Validation Tracker Issue Evidence Template" in roadmap
