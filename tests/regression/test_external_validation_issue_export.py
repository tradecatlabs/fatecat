from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-issue-export.py"
RUNBOOK_SCRIPT_PATH = ROOT / "scripts" / "external-validation-category-runbooks.py"
OPERATOR_PACKET_SCRIPT_PATH = ROOT / "scripts" / "external-validation-operator-execution-packet.py"
CLOSURE_SUMMARY_SCRIPT_PATH = ROOT / "scripts" / "external-validation-closure-evidence-summary.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-issue-export.json"


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


def _work_item(*, category: str, owner: str) -> dict:
    return {
        "id": f"external-work.{category.replace('.', '-')}",
        "owner": owner,
        "assignee": f"unassigned:{owner}",
        "category": category,
        "priority": "P0",
        "status": "pending_external_evidence",
        "proofRef": "",
        "lastCheckedAt": "2026-07-04T00:00:00Z",
        "staleReason": "proof_ref_missing",
        "closeConditionResult": "not_evaluated_no_proof_ref",
        "credentialDependencies": ["redacted operator credential"],
        "requiredEvidence": ["redacted live proof JSON"],
        "verificationCommands": ["bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>"],
        "closureCondition": "真实外部证据通过后关闭。",
        "occurrences": [
            {
                "id": f"external.{category.replace('.', '-')}",
                "source": {
                    "path": "docs/release.md",
                    "line": 1,
                    "excerptSha256": "1" * 64,
                },
                "status": "external_connectivity_pending",
            }
        ],
    }


def _work_queue(categories: list[str]) -> dict:
    items = [_work_item(category=category, owner=f"owner-{index:02d}") for index, category in enumerate(categories, 1)]
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_work_queue",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "closurePlanJson": "fixture",
            "closurePlanSha256": "0" * 64,
            "closurePlanKind": "fatecat.external_validation_closure_plan",
            "closureItemCount": len(items),
        },
        "summary": {"totalOccurrences": len(items), "workItems": len(items)},
        "shipGate": {"status": "blocked"},
        "workItems": items,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _proof_ref_gate(work_items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_gate_summary",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "workQueueJson": "fixture",
            "workQueueSha256": "0" * 64,
            "workQueueKind": "fatecat.external_validation_closure_work_queue",
            "expectedCommit": "a" * 40,
        },
        "summary": {
            "workItems": len(work_items),
            "acceptedProofRefs": 0,
            "acceptedWorkItems": 0,
            "pendingWorkItems": len(work_items),
            "proofRefStatus": "external_connectivity_pending",
        },
        "proofRefStatus": "external_connectivity_pending",
        "proofRefGate": {"status": "external_connectivity_pending"},
        "shipGate": {"status": "blocked"},
        "acceptedProofRefs": [],
        "pendingWorkItems": [
            {
                "id": item["id"],
                "owner": item["owner"],
                "category": item["category"],
                "staleReason": "proof_ref_missing",
            }
            for item in work_items
        ],
        "negativeEvidenceRejected": [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _live_proof_gate(work_items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_live_proof_gate_summary",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "workQueueJson": "fixture",
            "workQueueSha256": "0" * 64,
            "proofRefGateJson": "fixture",
            "proofRefGateSha256": "0" * 64,
            "categoryRunbooksJson": "fixture",
            "categoryRunbooksSha256": "0" * 64,
            "expectedCommit": "a" * 40,
        },
        "summary": {
            "workItems": len(work_items),
            "acceptedLiveProofs": 0,
            "acceptedLiveWorkItems": 0,
            "pendingWorkItems": len(work_items),
            "liveProofStatus": "external_connectivity_pending",
        },
        "liveProofStatus": "external_connectivity_pending",
        "liveProofGate": {"status": "external_connectivity_pending"},
        "shipGate": {"status": "blocked"},
        "acceptedLiveProofs": [],
        "pendingWorkItems": [{"id": item["id"]} for item in work_items],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _closure_trend(work_items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_trend_dashboard",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "summary": {
            "workItems": len(work_items),
            "staleAlerts": len(work_items),
            "missingProofRefs": len(work_items),
            "categoryLivePendingWorkItems": len(work_items),
        },
        "staleAlerts": [
            {
                "id": f"stale-alert.{item['id']}",
                "workItemId": item["id"],
                "owner": item["owner"],
                "category": item["category"],
                "alertReasons": ["proof_ref_missing", "category_live_pending", "stale_owner_pending"],
                "ageHours": 1.0,
            }
            for item in work_items
        ],
        "alertStatus": "stale_alerts_pending",
        "alertGate": {"status": "blocked", "blockingItems": ["stale_owner_alerts_pending"]},
        "shipGate": {"status": "blocked", "blockingItems": ["external_validation_stale_alerts_pending"]},
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Alert is not live evidence closure."],
    }


def _fixture_files(tmp_path: Path) -> tuple[Path, Path, Path, Path, list[str]]:
    runbook_module = _load_module(RUNBOOK_SCRIPT_PATH, "fatecat_external_validation_category_runbooks_for_issue")
    operator_module = _load_module(OPERATOR_PACKET_SCRIPT_PATH, "fatecat_external_validation_operator_packet_for_issue")
    closure_module = _load_module(CLOSURE_SUMMARY_SCRIPT_PATH, "fatecat_external_validation_closure_summary_for_issue")
    categories = sorted(runbook_module.CATEGORY_PROFILES)
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    runbooks_json = tmp_path / "runbooks.json"
    operator_packet_json = tmp_path / "operator-packet.json"
    live_proof_gate_json = tmp_path / "live-proof-gate.json"
    closure_trend_json = tmp_path / "closure-trend.json"
    closure_summary_json = tmp_path / "closure-summary.json"

    work_queue = _work_queue(categories)
    work_items = work_queue["workItems"]
    _write_json(work_queue_json, work_queue)
    _write_json(proof_ref_gate_json, _proof_ref_gate(work_items))
    runbooks = runbook_module.build_summary(work_queue_json=work_queue_json)
    _write_json(runbooks_json, runbooks)
    operator_packet = operator_module.build_packet(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=runbooks_json,
        expected_commit="a" * 40,
    )
    _write_json(operator_packet_json, operator_packet)
    _write_json(live_proof_gate_json, _live_proof_gate(work_items))
    _write_json(closure_trend_json, _closure_trend(work_items))
    closure_summary = closure_module.build_summary(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=runbooks_json,
        operator_packet_json=operator_packet_json,
        live_proof_gate_json=live_proof_gate_json,
        closure_trend_dashboard_json=closure_trend_json,
    )
    _write_json(closure_summary_json, closure_summary)
    return work_queue_json, runbooks_json, operator_packet_json, closure_summary_json, categories


def test_external_validation_issue_export_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_issue_export_contract"
    assert contract["outputKind"] == "fatecat.external_validation_issue_export"
    assert "issueTemplates" in contract["requiredOutputFields"]
    assert "trackerImport" in contract["requiredOutputFields"]
    assert "Does not create issues in GitHub or any external tracker." in contract["nonClaims"]


def test_external_validation_issue_export_builds_all_pending_issue_templates(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_issue_export")
    work_queue_json, runbooks_json, operator_packet_json, closure_summary_json, categories = _fixture_files(tmp_path)

    export = module.build_export(
        work_queue_json=work_queue_json,
        category_runbooks_json=runbooks_json,
        operator_packet_json=operator_packet_json,
        closure_evidence_summary_json=closure_summary_json,
        expected_commit="a" * 40,
    )
    serialized = json.dumps(export, ensure_ascii=False, sort_keys=True)

    assert export["kind"] == "fatecat.external_validation_issue_export"
    assert export["status"] == "operator_action_required"
    assert export["issueGate"]["status"] == "blocked"
    assert export["summary"]["issueTemplates"] == len(categories)
    assert export["summary"]["externalPending"] == len(categories)
    assert export["trackerImport"]["createsIssues"] is False
    assert any(template["category"] == "runtime.postgres_live" for template in export["issueTemplates"])
    assert all("external-validation" in template["labels"] for template in export["issueTemplates"])
    assert all("bodyMarkdown" in template for template in export["issueTemplates"])
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()
    assert f"se{'cret'}=" not in serialized.lower()
    assert "database_url=" not in serialized.lower()
    assert "placeholder proof" not in serialized.lower()


def test_external_validation_issue_export_cli_writes_json_and_markdown(tmp_path):
    work_queue_json, runbooks_json, operator_packet_json, closure_summary_json, categories = _fixture_files(tmp_path)
    output_json = tmp_path / "issue-export.json"
    output_markdown = tmp_path / "ISSUE_EXPORT.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--work-queue-json",
            str(work_queue_json),
            "--category-runbooks-json",
            str(runbooks_json),
            "--operator-packet-json",
            str(operator_packet_json),
            "--closure-evidence-summary-json",
            str(closure_summary_json),
            "--expected-commit",
            "a" * 40,
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
    summary = json.loads(result.stdout)
    export = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_markdown.read_text(encoding="utf-8")
    assert summary["issueTemplates"] == len(categories)
    assert summary["issueGate"] == "blocked"
    assert export["summary"]["issueTemplates"] == len(categories)
    assert "External Validation Issue Export" in markdown
    assert "runtime.postgres_live" in markdown
    assert "https://" not in markdown


def test_external_validation_issue_export_rejects_sensitive_assignment(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_issue_export_sensitive")
    work_queue_json, runbooks_json, operator_packet_json, closure_summary_json, _categories = _fixture_files(tmp_path)
    operator_packet = json.loads(operator_packet_json.read_text(encoding="utf-8"))
    sensitive_assignment = f"to{'ken'}=REALVALUE bash scripts/external-validation-proof-ref-gate.sh"
    operator_packet["operatorSteps"][0]["operatorCommands"] = [sensitive_assignment]
    _write_json(operator_packet_json, operator_packet)

    with pytest.raises(module.ExternalValidationIssueExportError, match="sensitive-looking assignment"):
        module.build_export(
            work_queue_json=work_queue_json,
            category_runbooks_json=runbooks_json,
            operator_packet_json=operator_packet_json,
            closure_evidence_summary_json=closure_summary_json,
            expected_commit="a" * 40,
        )


def test_external_validation_issue_export_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external validation issue export" in local_ci
    assert "externalValidationIssueExport" in local_ci
    assert "external-validation-issue-export.py" in scripts_agents
    assert "external-validation-issue-export.json" in audit_agents
    assert "test_external_validation_issue_export.py" in tests_agents
    assert "external-validation-issue-export.sh" in roadmap
