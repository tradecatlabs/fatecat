from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-closure-trend-dashboard.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-trend-dashboard.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_closure_trend_dashboard", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _closure_item(*, item_id: str, owner: str, category: str, status: str = "external_connectivity_pending") -> dict:
    return {
        "id": item_id,
        "source": {
            "id": item_id,
            "path": "docs/release.md",
            "line": 1,
            "excerptSha256": "1" * 64,
        },
        "category": category,
        "owner": owner,
        "status": status,
        "credentialDependencies": ["redacted credential"],
        "requiredEvidence": ["redacted live proof JSON"],
        "verificationCommands": ["bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>"],
        "closureCondition": "真实外部证据通过后关闭。",
    }


def _closure_plan(items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_plan",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {"pendingExternalJson": "fixture", "itemCount": len(items)},
        "summary": {"total": len(items)},
        "shipGate": {"status": "blocked"},
        "items": items,
        "privacyBoundary": "fixture privacy",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _work_item(
    *,
    item_id: str,
    owner: str,
    category: str,
    priority: str = "P0",
    status: str = "pending_external_evidence",
    stale_reason: str = "proof_ref_missing",
) -> dict:
    return {
        "id": item_id,
        "owner": owner,
        "assignee": f"unassigned:{owner}",
        "category": category,
        "priority": priority,
        "status": status,
        "proofRef": "",
        "lastCheckedAt": "2026-07-04T00:00:00Z",
        "staleReason": stale_reason,
        "closeConditionResult": "not_evaluated_no_proof_ref",
        "credentialDependencies": ["redacted credential"],
        "requiredEvidence": ["redacted live proof JSON"],
        "verificationCommands": ["bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>"],
        "closureCondition": "真实外部证据通过后关闭。",
        "occurrences": [
            {
                "id": f"occurrence.{item_id}",
                "source": {
                    "path": "docs/release.md",
                    "line": 1,
                    "excerptSha256": "1" * 64,
                },
                "status": "external_connectivity_pending",
            }
        ],
    }


def _work_queue(items: list[dict], *, total_occurrences: int | None = None) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_work_queue",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "closurePlanJson": "fixture",
            "closurePlanSha256": "0" * 64,
            "closurePlanKind": "fatecat.external_validation_closure_plan",
            "closureItemCount": total_occurrences or len(items),
        },
        "summary": {
            "totalOccurrences": total_occurrences or len(items),
            "workItems": len(items),
        },
        "shipGate": {
            "status": "blocked",
        },
        "workItems": items,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _proof_ref_gate(*, accepted_ids: list[str], work_items: list[dict]) -> dict:
    pending_items = [item for item in work_items if item["id"] not in set(accepted_ids)]
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
            "acceptedProofRefs": len(accepted_ids),
            "acceptedWorkItems": len(accepted_ids),
            "pendingWorkItems": len(pending_items),
            "proofRefStatus": "schema_accepted_all_work_items"
            if not pending_items
            else "external_connectivity_pending",
        },
        "proofRefStatus": "schema_accepted_all_work_items" if not pending_items else "external_connectivity_pending",
        "proofRefGate": {
            "status": "schema_accepted_all_work_items" if not pending_items else "external_connectivity_pending"
        },
        "shipGate": {"status": "blocked"},
        "acceptedProofRefs": [
            {
                "id": f"proof.{item_id}",
                "proofRef": f"evidence://external-validation/{item_id}",
                "evidenceType": "redacted_live_evidence",
                "workItemId": item_id,
                "owner": "release-ops",
                "category": "release.production_api_live",
                "issuer": "operator:release-ops",
                "capturedAt": "2026-07-04T00:00:00Z",
                "expiresAt": "2099-01-01T00:00:00Z",
                "artifactHash": f"sha256:{'b' * 64}",
                "verificationCommandSha256": "c" * 64,
                "occurrenceIds": [f"occurrence.{item_id}"],
            }
            for item_id in accepted_ids
        ],
        "pendingWorkItems": [
            {
                "id": item["id"],
                "owner": item["owner"],
                "category": item["category"],
                "staleReason": "proof_ref_missing",
            }
            for item in pending_items
        ],
        "negativeEvidenceRejected": [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _runbooks(categories: list[str]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_category_runbooks",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "summary": {"categories": len(categories), "runbooks": len(categories)},
        "runbookStatus": "operator_runbooks_ready",
        "runbookGate": {"status": "passed"},
        "shipGate": {"status": "blocked"},
        "runbooks": [
            {
                "id": f"external-runbook.{category}",
                "category": category,
                "owners": ["release-ops"],
                "priority": "P0",
                "status": "operator_action_required",
                "evidenceType": "redacted_live_evidence",
                "requiredCredentials": ["redacted credential"],
                "operatorCommands": ["bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>"],
                "proofRefArtifactPattern": f"evidence://external-validation/{category}/<run-id>",
                "redactionRule": "redact secrets",
                "expiryPolicy": "14 days",
                "failureRollback": "keep blocked",
                "closureCondition": "真实外部证据通过后关闭。",
                "verifierCommand": "bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>",
                "sourceWorkItemIds": [],
                "occurrenceCount": 1,
                "nonClaims": ["Runbook readiness does not prove live evidence has passed."],
            }
            for category in categories
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _write_inputs(tmp_path: Path, *, accepted_ids: list[str] | None = None) -> dict[str, Path]:
    accepted_ids = accepted_ids or []
    closure_items = [
        _closure_item(item_id="api-1", owner="release-ops", category="release.production_api_live"),
        _closure_item(
            item_id="manual-1",
            owner="engineering-audit",
            category="manual_triage",
            status="manual_triage_required",
        ),
        _closure_item(
            item_id="policy-1",
            owner="governance",
            category="governance.external_validation_policy_guardrail",
        ),
    ]
    work_items = [
        _work_item(item_id="external-work.api", owner="release-ops", category="release.production_api_live"),
        _work_item(
            item_id="external-work.manual",
            owner="engineering-audit",
            category="manual_triage",
            priority="P1",
            status="manual_triage_required",
            stale_reason="manual_classification_required",
        ),
        _work_item(
            item_id="external-work.policy",
            owner="governance",
            category="governance.external_validation_policy_guardrail",
            priority="P1",
            status="policy_guardrail_review_required",
            stale_reason="policy_guardrail_requires_review",
        ),
    ]
    paths = {
        "closure": tmp_path / "closure.json",
        "work_queue": tmp_path / "work-queue.json",
        "proof": tmp_path / "proof.json",
        "runbooks": tmp_path / "runbooks.json",
    }
    _write_json(paths["closure"], _closure_plan(closure_items))
    _write_json(paths["work_queue"], _work_queue(work_items, total_occurrences=len(closure_items)))
    _write_json(paths["proof"], _proof_ref_gate(accepted_ids=accepted_ids, work_items=work_items))
    _write_json(paths["runbooks"], _runbooks([item["category"] for item in work_items]))
    return paths


def test_external_validation_closure_trend_dashboard_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_closure_trend_dashboard_contract"
    assert "fatecat.external_validation_closure_work_queue" in contract["inputKinds"]
    assert "ownerDashboard" in contract["requiredOutputFields"]
    assert "staleAlerts" in contract["requiredOutputFields"]
    assert contract["alertPolicy"]["deliveryMode"] == "local_dry_run_only"
    assert "Does not send real alerts or create external issues." in contract["nonClaims"]


def test_external_validation_closure_trend_dashboard_builds_owner_category_alerts(tmp_path):
    module = _load_module()
    paths = _write_inputs(tmp_path)

    summary = module.build_summary(
        closure_plan_json=paths["closure"],
        work_queue_json=paths["work_queue"],
        proof_ref_gate_json=paths["proof"],
        category_runbooks_json=paths["runbooks"],
        now_iso="2026-07-05T00:00:00Z",
    )
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    assert summary["kind"] == "fatecat.external_validation_closure_trend_dashboard"
    assert summary["status"] == "passed"
    assert summary["alertStatus"] == "stale_alerts_pending"
    assert summary["alertGate"]["status"] == "blocked"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["summary"]["workItems"] == 3
    assert summary["summary"]["staleAlerts"] == 3
    assert summary["summary"]["missingProofRefs"] == 3
    assert summary["summary"]["manualTriageWorkItems"] == 1
    assert summary["summary"]["policyGuardrailWorkItems"] == 1
    assert summary["summary"]["categoryLivePendingWorkItems"] == 3
    assert summary["summary"]["maxAgeHours"] == 24.0
    assert summary["statusDashboard"]["pending_external_evidence"] == 1
    assert any(item["owner"] == "release-ops" for item in summary["ownerDashboard"])
    assert any(item["category"] == "release.production_api_live" for item in summary["categoryDashboard"])
    assert "proof_ref_missing" in summary["staleAlerts"][0]["alertReasons"]
    assert "https://" not in rendered
    assert "token=" not in rendered
    assert "secret=" not in rendered


def test_external_validation_closure_trend_dashboard_keeps_category_live_pending_after_proof_ref_acceptance(tmp_path):
    module = _load_module()
    paths = _write_inputs(tmp_path, accepted_ids=["external-work.api", "external-work.manual", "external-work.policy"])

    summary = module.build_summary(
        closure_plan_json=paths["closure"],
        work_queue_json=paths["work_queue"],
        proof_ref_gate_json=paths["proof"],
        category_runbooks_json=paths["runbooks"],
        now_iso="2026-07-05T00:00:00Z",
    )

    assert summary["summary"]["acceptedProofRefs"] == 3
    assert summary["summary"]["missingProofRefs"] == 0
    assert summary["summary"]["categoryLivePendingWorkItems"] == 3
    assert summary["shipGate"]["status"] == "blocked"
    assert "category_live_execution_pending" in summary["shipGate"]["blockingItems"]
    api_alert = next(item for item in summary["staleAlerts"] if item["workItemId"] == "external-work.api")
    assert api_alert["proofRefStatus"] == "schema_accepted"
    assert api_alert["alertReasons"] == ["category_live_pending", "stale_owner_pending"]


def test_external_validation_closure_trend_dashboard_rejects_missing_category_runbook(tmp_path):
    module = _load_module()
    paths = _write_inputs(tmp_path)
    runbooks = json.loads(paths["runbooks"].read_text(encoding="utf-8"))
    runbooks["runbooks"] = [item for item in runbooks["runbooks"] if item["category"] != "manual_triage"]
    _write_json(paths["runbooks"], runbooks)

    with pytest.raises(module.ExternalValidationClosureTrendDashboardError, match="category runbook missing"):
        module.build_summary(
            closure_plan_json=paths["closure"],
            work_queue_json=paths["work_queue"],
            proof_ref_gate_json=paths["proof"],
            category_runbooks_json=paths["runbooks"],
            now_iso="2026-07-05T00:00:00Z",
        )


def test_external_validation_closure_trend_dashboard_cli_writes_summary(tmp_path):
    paths = _write_inputs(tmp_path)
    output_json = tmp_path / "dashboard.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--closure-plan-json",
            str(paths["closure"]),
            "--work-queue-json",
            str(paths["work_queue"]),
            "--proof-ref-gate-json",
            str(paths["proof"]),
            "--category-runbooks-json",
            str(paths["runbooks"]),
            "--now",
            "2026-07-05T00:00:00Z",
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    assert summary["alertStatus"] == "stale_alerts_pending"
    assert summary["alertGate"]["deliveryStatus"] == "not_sent"
    assert summary["trend"]["previousDashboardProvided"] is False


def test_external_validation_closure_trend_dashboard_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    certification_contract = (
        ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"
    ).read_text(encoding="utf-8")

    assert "external validation closure trend dashboard" in local_ci
    assert "externalValidationClosureTrendDashboard" in local_ci
    assert "external-validation-closure-trend-dashboard.py" in scripts_agents
    assert "external-validation-closure-trend-dashboard.json" in audit_agents
    assert "test_external_validation_closure_trend_dashboard.py" in tests_agents
    assert "external-validation-closure-trend-dashboard.json" in certification_contract
