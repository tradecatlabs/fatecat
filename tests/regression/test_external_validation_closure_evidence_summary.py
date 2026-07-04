from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-closure-evidence-summary.py"
RUNBOOK_SCRIPT_PATH = ROOT / "scripts" / "external-validation-category-runbooks.py"
OPERATOR_PACKET_SCRIPT_PATH = ROOT / "scripts" / "external-validation-operator-execution-packet.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-evidence-summary.json"


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


def _fixture_files(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path, list[str]]:
    runbook_module = _load_module(RUNBOOK_SCRIPT_PATH, "fatecat_external_validation_category_runbooks_for_summary")
    operator_module = _load_module(
        OPERATOR_PACKET_SCRIPT_PATH, "fatecat_external_validation_operator_packet_for_summary"
    )
    categories = sorted(runbook_module.CATEGORY_PROFILES)
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    runbooks_json = tmp_path / "runbooks.json"
    operator_packet_json = tmp_path / "operator-packet.json"
    live_proof_gate_json = tmp_path / "live-proof-gate.json"
    closure_trend_json = tmp_path / "closure-trend.json"

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
    return (
        work_queue_json,
        proof_ref_gate_json,
        runbooks_json,
        operator_packet_json,
        live_proof_gate_json,
        closure_trend_json,
        categories,
    )


def test_external_validation_closure_evidence_summary_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_closure_evidence_summary_contract"
    assert "fatecat.external_validation_operator_execution_packet" in contract["requiredInputs"]
    assert "workItemSummaries" in contract["requiredOutputFields"]
    assert "externalPending" in contract["requiredOutputFields"]
    assert "Does not create proof refs or live proofs." in contract["nonClaims"]


def test_external_validation_closure_evidence_summary_builds_all_category_summary(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_closure_evidence_summary")
    (
        work_queue_json,
        proof_ref_gate_json,
        runbooks_json,
        operator_packet_json,
        live_proof_gate_json,
        closure_trend_json,
        categories,
    ) = _fixture_files(tmp_path)

    summary = module.build_summary(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=runbooks_json,
        operator_packet_json=operator_packet_json,
        live_proof_gate_json=live_proof_gate_json,
        closure_trend_dashboard_json=closure_trend_json,
    )
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    assert summary["kind"] == "fatecat.external_validation_closure_evidence_summary"
    assert summary["status"] == "passed"
    assert summary["closureGate"]["status"] == "blocked"
    assert summary["summary"]["workItems"] == len(categories)
    assert summary["summary"]["externalPending"] == len(categories)
    assert summary["summary"]["missingProofRefs"] == len(categories)
    assert summary["summary"]["livePending"] == len(categories)
    assert {item["category"] for item in summary["workItemSummaries"]} == set(categories)
    assert {"runtime", "security", "observability", "developer_platform"}.issubset(
        {item["domain"] for item in summary["domainSummaries"]}
    )
    assert all(item["operatorStepId"] for item in summary["workItemSummaries"])
    assert any(command_id == "external-validation-proof-ref-gate" for command_id in summary["finalGateCommandIds"])
    assert "https://" not in serialized
    assert "token=" not in serialized.lower()
    assert "secret=" not in serialized.lower()
    assert "DATABASE_URL=" not in serialized


def test_external_validation_closure_evidence_summary_cli_writes_output(tmp_path):
    (
        work_queue_json,
        proof_ref_gate_json,
        runbooks_json,
        operator_packet_json,
        live_proof_gate_json,
        closure_trend_json,
        categories,
    ) = _fixture_files(tmp_path)
    output_json = tmp_path / "closure-summary.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--work-queue-json",
            str(work_queue_json),
            "--proof-ref-gate-json",
            str(proof_ref_gate_json),
            "--category-runbooks-json",
            str(runbooks_json),
            "--operator-packet-json",
            str(operator_packet_json),
            "--live-proof-gate-json",
            str(live_proof_gate_json),
            "--closure-trend-dashboard-json",
            str(closure_trend_json),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    cli_summary = json.loads(result.stdout)
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert cli_summary["externalPending"] == len(categories)
    assert cli_summary["closureGate"] == "blocked"
    assert stored["summary"]["workItems"] == len(categories)


def test_external_validation_closure_evidence_summary_rejects_raw_url(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_closure_evidence_summary_raw_url")
    (
        work_queue_json,
        proof_ref_gate_json,
        runbooks_json,
        operator_packet_json,
        live_proof_gate_json,
        closure_trend_json,
        _categories,
    ) = _fixture_files(tmp_path)
    closure_trend = json.loads(closure_trend_json.read_text(encoding="utf-8"))
    closure_trend["staleAlerts"][0]["alertReasons"].append("https://example.invalid/proof")
    _write_json(closure_trend_json, closure_trend)

    with pytest.raises(module.ExternalValidationClosureEvidenceSummaryError, match="raw URL detected"):
        module.build_summary(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=runbooks_json,
            operator_packet_json=operator_packet_json,
            live_proof_gate_json=live_proof_gate_json,
            closure_trend_dashboard_json=closure_trend_json,
        )


def test_external_validation_closure_evidence_summary_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    certification_contract = (
        ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"
    ).read_text(encoding="utf-8")

    assert "external validation closure evidence summary" in local_ci
    assert "externalValidationClosureEvidenceSummary" in local_ci
    assert "external-validation-closure-evidence-summary.py" in scripts_agents
    assert "external-validation-closure-evidence-summary.json" in audit_agents
    assert "test_external_validation_closure_evidence_summary.py" in tests_agents
    assert "external-validation-closure-evidence-summary.json" in certification_contract
