from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "production-live-operator-execution-packet.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "production-live-operator-execution-packet.json"

CATEGORIES = (
    ("release.production_api_live", "release-ops"),
    ("release.hf_space_live", "release-ops"),
    ("release.telegram_bot_live", "bot-ops"),
    ("runtime.public_webhook_live", "runtime-ops"),
    ("delivery.multi_surface_live", "delivery-ops"),
)


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_production_live_operator_packet", SCRIPT_PATH)
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
        "verificationCommands": ["bash scripts/live-release-gate.sh --output-json <path>"],
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


def _work_queue() -> dict:
    items = [_work_item(category=category, owner=owner) for category, owner in CATEGORIES]
    items.append(_work_item(category="security.identity_oidc", owner="security-ops"))
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


def _proof_ref_gate() -> dict:
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
            "workItems": 6,
            "acceptedProofRefs": 0,
            "acceptedWorkItems": 0,
            "pendingWorkItems": 6,
            "proofRefStatus": "external_connectivity_pending",
        },
        "proofRefStatus": "external_connectivity_pending",
        "proofRefGate": {"status": "external_connectivity_pending"},
        "shipGate": {"status": "blocked"},
        "acceptedProofRefs": [],
        "pendingWorkItems": [],
        "negativeEvidenceRejected": [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _runbooks() -> dict:
    runbooks = []
    for category, owner in CATEGORIES:
        runbooks.append(
            {
                "id": f"external-runbook.{category}",
                "category": category,
                "owners": [owner],
                "priority": "P0",
                "status": "operator_action_required",
                "evidenceType": category.replace(".", "_"),
                "requiredCredentials": ["redacted credential"],
                "operatorCommands": ["bash scripts/live-release-gate.sh --output-json <path>"],
                "proofRefArtifactPattern": f"evidence://external-validation/{category}/<run-id>",
                "redactionRule": "redact secrets",
                "expiryPolicy": "14 days",
                "failureRollback": "keep blocked",
                "closureCondition": "真实外部证据通过后关闭。",
                "verifierCommand": "bash scripts/external-validation-live-proof-gate.sh --work-queue-json <path>",
                "sourceWorkItemIds": [f"external-work.{category.replace('.', '-')}"],
                "occurrenceCount": 1,
                "nonClaims": ["Runbook readiness does not prove live evidence has passed."],
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_category_runbooks",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "summary": {"categories": len(CATEGORIES), "runbooks": len(CATEGORIES)},
        "runbookStatus": "operator_runbooks_ready",
        "runbookGate": {"status": "passed"},
        "shipGate": {"status": "blocked"},
        "runbooks": runbooks,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _fixture_files(tmp_path: Path) -> tuple[Path, Path, Path]:
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    runbooks_json = tmp_path / "runbooks.json"
    _write_json(work_queue_json, _work_queue())
    _write_json(proof_ref_gate_json, _proof_ref_gate())
    _write_json(runbooks_json, _runbooks())
    return work_queue_json, proof_ref_gate_json, runbooks_json


def test_production_live_operator_packet_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.production_live_operator_execution_packet_contract"
    assert "operatorSteps" in contract["requiredOutputFields"]
    assert "proofRefBundleTemplate" in contract["requiredOutputFields"]
    assert "finalGateCommands" in contract["requiredOutputFields"]
    assert set(contract["supportedCategories"]) == {category for category, _ in CATEGORIES}
    assert "Does not execute production live checks." in contract["nonClaims"]


def test_production_live_operator_packet_builds_redacted_execution_packet(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, runbooks_json = _fixture_files(tmp_path)

    packet = module.build_packet(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=runbooks_json,
        expected_commit="a" * 40,
    )
    serialized = json.dumps(packet, ensure_ascii=False, sort_keys=True)

    assert packet["kind"] == "fatecat.production_live_operator_execution_packet"
    assert packet["status"] == "operator_action_required"
    assert packet["packetGate"]["status"] == "blocked"
    assert packet["summary"]["operatorSteps"] == len(CATEGORIES)
    assert packet["summary"]["proofRefTemplates"] == len(CATEGORIES)
    assert "FATE_BOT_TOKEN" in packet["requiredEnvVars"]
    assert "FATE_REPORT_JOB_DATABASE_URL" in packet["requiredEnvVars"]
    assert any(step["category"] == "runtime.public_webhook_live" for step in packet["operatorSteps"])
    assert any(command["id"] == "external-validation-live-proof-gate" for command in packet["finalGateCommands"])
    assert packet["source"]["commit"] == "a" * 40
    assert "https://" not in serialized
    assert "token=" not in serialized.lower()
    assert "secret=" not in serialized.lower()
    assert "DATABASE_URL=" not in serialized
    assert "placeholder proof" not in serialized.lower()


def test_production_live_operator_packet_cli_writes_output(tmp_path):
    work_queue_json, proof_ref_gate_json, runbooks_json = _fixture_files(tmp_path)
    output_json = tmp_path / "operator-packet.json"

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
            "--expected-commit",
            "a" * 40,
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)
    packet = json.loads(output_json.read_text(encoding="utf-8"))
    assert summary["operatorSteps"] == len(CATEGORIES)
    assert summary["packetGate"] == "blocked"
    assert packet["operatorWorkspace"]["envVar"] == "FATE_OPERATOR_OUTPUT_DIR"


def test_production_live_operator_packet_rejects_sensitive_assignment(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, runbooks_json = _fixture_files(tmp_path)
    work_queue = json.loads(work_queue_json.read_text(encoding="utf-8"))
    work_queue["workItems"][0]["verificationCommands"] = ["token=REALVALUE bash scripts/live-release-gate.sh"]
    _write_json(work_queue_json, work_queue)

    with pytest.raises(module.ProductionLiveOperatorExecutionPacketError, match="sensitive-looking assignment"):
        module.build_packet(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=runbooks_json,
            expected_commit="a" * 40,
        )


def test_production_live_operator_packet_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "production live operator execution packet" in local_ci
    assert "productionLiveOperatorExecutionPacket" in local_ci
    assert "production-live-operator-execution-packet.py" in scripts_agents
    assert "production-live-operator-execution-packet.json" in audit_agents
    assert "test_production_live_operator_execution_packet.py" in tests_agents
    assert "production-live-operator-execution-packet.sh" in roadmap
