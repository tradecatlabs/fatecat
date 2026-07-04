from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-tracker-import-package.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-import-package.json"


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


def _issue_template(index: int) -> dict:
    issue_id = f"external-validation-issue.external-work.category-{index}"
    return {
        "id": issue_id,
        "title": f"[External Validation] runtime/runtime.category_{index} - owner-{index}",
        "labels": [
            "external-validation",
            "measurement-infrastructure",
            "operator-action-required",
            "domain.runtime",
            f"category.runtime.category_{index}",
            f"owner.owner-{index}",
        ],
        "assigneeHint": f"unassigned:owner-{index}",
        "workItemId": f"external-work.category-{index}",
        "domain": "runtime",
        "category": f"runtime.category_{index}",
        "owner": f"owner-{index}",
        "priority": "P0",
        "status": "operator_action_required",
        "occurrenceIds": [f"external.category-{index}"],
        "requiredCredentials": ["FATE_REDACTED_OPERATOR_CREDENTIAL"],
        "requiredEvidence": ["redacted live proof JSON"],
        "runbookId": f"external-validation-runbook.runtime.category_{index}",
        "operatorStepId": f"operator-step.runtime.category_{index}",
        "operatorCommandCount": 1,
        "operatorCommands": ["bash scripts/example-live-smoke.sh --output-json <redacted-summary.json>"],
        "operatorCommandSha256s": ["1" * 64],
        "proofRefPattern": "proofref:fatecat:external-validation:runtime.category",
        "artifactHashInstruction": "sha256:<64 lowercase hex artifact digest>",
        "verificationCommand": "bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>",
        "blockingItems": ["proof_ref_missing", "category_live_pending"],
        "closureCondition": "真实外部证据通过后关闭。",
        "sourceBinding": {
            "workItemId": f"external-work.category-{index}",
            "occurrenceIds": [f"external.category-{index}"],
            "runbookId": f"external-validation-runbook.runtime.category_{index}",
            "operatorStepId": f"operator-step.runtime.category_{index}",
        },
        "bodyMarkdown": (
            "## External Validation Work Item\n\n"
            f"- Work item: `external-work.category-{index}`\n"
            f"- Category: `runtime.category_{index}`\n\n"
            "## Required Credentials\n\n"
            "- `FATE_REDACTED_OPERATOR_CREDENTIAL`\n\n"
            "## Non-Claims\n\n"
            "- This issue does not prove live validation has passed.\n"
        ),
    }


def _issue_export() -> dict:
    templates = [_issue_template(1), _issue_template(2)]
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_issue_export",
        "status": "operator_action_required",
        "generatedAt": "2026-07-04T00:00:00Z",
        "source": {
            "workQueueKind": "fatecat.external_validation_closure_work_queue",
            "workQueueSha256": "1" * 64,
            "categoryRunbooksKind": "fatecat.external_validation_category_runbooks",
            "categoryRunbooksSha256": "2" * 64,
            "operatorPacketKind": "fatecat.external_validation_operator_execution_packet",
            "operatorPacketSha256": "3" * 64,
            "closureEvidenceSummaryKind": "fatecat.external_validation_closure_evidence_summary",
            "closureEvidenceSummarySha256": "4" * 64,
            "commit": "a" * 40,
        },
        "summary": {
            "domains": 1,
            "categories": 2,
            "workItems": 2,
            "externalPending": 2,
            "issueTemplates": 2,
            "requiredCredentials": 1,
            "operatorCommands": 2,
        },
        "issueGate": {"status": "blocked", "blockingItems": ["tracker_issue_creation_required"]},
        "trackerImport": {
            "format": "github_issue_markdown_copy_paste",
            "createsIssues": False,
            "bodyFilePattern": "external-validation-issues/{issueTemplateId}.md",
            "requiredLabels": ["external-validation", "measurement-infrastructure", "operator-action-required"],
        },
        "issueTemplates": templates,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not create issues in GitHub or any external tracker."],
    }


def test_tracker_import_package_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_tracker_import_package_contract"
    assert contract["outputKind"] == "fatecat.external_validation_tracker_import_package"
    assert "files" in contract["requiredOutputFields"]
    assert "commands" in contract["requiredOutputFields"]
    assert contract["trackerPolicy"]["createsIssues"] is False
    assert contract["trackerPolicy"]["executesCommands"] is False


def test_tracker_import_package_writes_manifest_issue_files_and_commands(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_import_package")
    issue_export_json = tmp_path / "issue-export.json"
    package_dir = tmp_path / "tracker-package"
    output_json = tmp_path / "tracker-package.json"
    output_markdown = tmp_path / "TRACKER_PACKAGE.md"
    _write_json(issue_export_json, _issue_export())

    package = module.build_package(
        issue_export_json=issue_export_json,
        package_dir=package_dir,
        expected_commit="a" * 40,
    )
    module.write_package(
        package=package,
        package_dir=package_dir,
        output_json=output_json,
        output_markdown=output_markdown,
    )
    serialized = json.dumps(package, ensure_ascii=False, sort_keys=True)

    assert package["kind"] == "fatecat.external_validation_tracker_import_package"
    assert package["status"] == "operator_action_required"
    assert package["packageGate"]["status"] == "blocked"
    assert package["trackerImport"]["createsIssues"] is False
    assert package["trackerImport"]["executesCommands"] is False
    assert package["summary"]["issueFiles"] == 2
    assert package["summary"]["commands"] == 2
    assert (package_dir / "README.md").is_file()
    assert (package_dir / "import-manifest.json").is_file()
    assert (package_dir / "gh-issue-create-commands.txt").is_file()
    assert all((package_dir / item["path"]).is_file() for item in package["files"])
    assert "gh issue create" in (package_dir / "gh-issue-create-commands.txt").read_text(encoding="utf-8")
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()
    assert f"se{'cret'}=" not in serialized.lower()


def test_tracker_import_package_rejects_raw_url_and_sensitive_assignment(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_tracker_import_package_negative")
    payload = _issue_export()
    payload["issueTemplates"][0]["bodyMarkdown"] += "\n" + "https://example.invalid/proof"
    issue_export_json = tmp_path / "bad-issue-export-url.json"
    _write_json(issue_export_json, payload)

    try:
        module.build_package(
            issue_export_json=issue_export_json, package_dir=tmp_path / "package", expected_commit="a" * 40
        )
    except Exception as exc:  # noqa: BLE001
        assert "raw URL" in str(exc)
    else:
        raise AssertionError("raw URL should be rejected")

    payload = _issue_export()
    payload["issueTemplates"][0]["bodyMarkdown"] += "\n" + f"to{'ken'}=redacted"
    issue_export_json = tmp_path / "bad-issue-export-secret.json"
    _write_json(issue_export_json, payload)

    try:
        module.build_package(
            issue_export_json=issue_export_json, package_dir=tmp_path / "package", expected_commit="a" * 40
        )
    except Exception as exc:  # noqa: BLE001
        assert "sensitive-looking assignment" in str(exc)
    else:
        raise AssertionError("sensitive assignment should be rejected")


def test_tracker_import_package_cli_outputs_paths(tmp_path):
    issue_export_json = tmp_path / "issue-export.json"
    package_dir = tmp_path / "package"
    output_json = tmp_path / "package.json"
    output_markdown = tmp_path / "PACKAGE.md"
    _write_json(issue_export_json, _issue_export())

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--issue-export-json",
            str(issue_export_json),
            "--package-dir",
            str(package_dir),
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

    assert cli_summary["kind"] == "fatecat.external_validation_tracker_import_package"
    assert cli_summary["packageGate"] == "blocked"
    assert cli_summary["issueFiles"] == 2
    assert output_json.is_file()
    assert output_markdown.is_file()
    assert (package_dir / "issues").is_dir()


def test_tracker_import_package_wiring_mentions_local_ci_docs_and_agents():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external validation tracker import package" in local_ci
    assert "externalValidationTrackerImportPackage" in local_ci
    assert "external-validation-tracker-import-package.py" in scripts_agents
    assert "external-validation-tracker-import-package.json" in audit_agents
    assert "test_external_validation_tracker_import_package.py" in tests_agents
    assert "Post-0131 External Validation Tracker Import Package" in roadmap
