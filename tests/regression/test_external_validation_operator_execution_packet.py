from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-operator-execution-packet.py"
RUNBOOK_SCRIPT_PATH = ROOT / "scripts" / "external-validation-category-runbooks.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-operator-execution-packet.json"


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


def _proof_ref_gate(work_item_count: int) -> dict:
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
            "workItems": work_item_count,
            "acceptedProofRefs": 0,
            "acceptedWorkItems": 0,
            "pendingWorkItems": work_item_count,
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


def _fixture_files(tmp_path: Path) -> tuple[Path, Path, Path, list[str]]:
    runbook_module = _load_module(RUNBOOK_SCRIPT_PATH, "fatecat_external_validation_category_runbooks_for_packet")
    categories = sorted(runbook_module.CATEGORY_PROFILES)
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    runbooks_json = tmp_path / "runbooks.json"
    _write_json(work_queue_json, _work_queue(categories))
    _write_json(proof_ref_gate_json, _proof_ref_gate(len(categories)))
    runbooks = runbook_module.build_summary(work_queue_json=work_queue_json)
    _write_json(runbooks_json, runbooks)
    return work_queue_json, proof_ref_gate_json, runbooks_json, categories


def test_external_validation_operator_packet_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_operator_execution_packet_contract"
    assert contract["outputKind"] == "fatecat.external_validation_operator_execution_packet"
    assert "domainGroups" in contract["requiredOutputFields"]
    assert "operatorSteps" in contract["requiredOutputFields"]
    assert "proofRefBundleTemplate" in contract["requiredOutputFields"]
    assert "Does not execute external live checks." in contract["nonClaims"]


def test_external_validation_operator_packet_builds_all_category_packet(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_operator_packet")
    work_queue_json, proof_ref_gate_json, runbooks_json, categories = _fixture_files(tmp_path)

    packet = module.build_packet(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=runbooks_json,
        expected_commit="a" * 40,
    )
    serialized = json.dumps(packet, ensure_ascii=False, sort_keys=True)

    assert packet["kind"] == "fatecat.external_validation_operator_execution_packet"
    assert packet["status"] == "operator_action_required"
    assert packet["packetGate"]["status"] == "blocked"
    assert packet["summary"]["categories"] == len(categories)
    assert packet["summary"]["operatorSteps"] == len(categories)
    assert packet["summary"]["proofRefTemplates"] == len(categories)
    assert packet["source"]["commit"] == "a" * 40
    assert {step["category"] for step in packet["operatorSteps"]} == set(categories)
    assert {"runtime", "security", "observability", "developer_platform"}.issubset(
        {group["domain"] for group in packet["domainGroups"]}
    )
    assert any(step["category"] == "runtime.postgres_live" for step in packet["operatorSteps"])
    assert any(command["id"] == "external-validation-proof-ref-gate" for command in packet["finalGateCommands"])
    assert "https://" not in serialized
    assert "token=" not in serialized.lower()
    assert "secret=" not in serialized.lower()
    assert "DATABASE_URL=" not in serialized
    assert "placeholder proof" not in serialized.lower()


def test_external_validation_operator_packet_cli_writes_output(tmp_path):
    work_queue_json, proof_ref_gate_json, runbooks_json, categories = _fixture_files(tmp_path)
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
    assert summary["operatorSteps"] == len(categories)
    assert summary["packetGate"] == "blocked"
    assert packet["operatorWorkspace"]["envVar"] == "FATE_EXTERNAL_OPERATOR_OUTPUT_DIR"


def test_external_validation_operator_packet_rejects_sensitive_assignment(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_external_validation_operator_packet_sensitive")
    work_queue_json, proof_ref_gate_json, runbooks_json, _categories = _fixture_files(tmp_path)
    runbooks = json.loads(runbooks_json.read_text(encoding="utf-8"))
    runbooks["runbooks"][0]["operatorCommands"] = ["token=REALVALUE bash scripts/external-validation-proof-ref-gate.sh"]
    _write_json(runbooks_json, runbooks)

    with pytest.raises(module.ExternalValidationOperatorExecutionPacketError, match="sensitive-looking assignment"):
        module.build_packet(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=runbooks_json,
            expected_commit="a" * 40,
        )


def test_external_validation_operator_packet_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external validation operator execution packet" in local_ci
    assert "externalValidationOperatorExecutionPacket" in local_ci
    assert "external-validation-operator-execution-packet.py" in scripts_agents
    assert "external-validation-operator-execution-packet.json" in audit_agents
    assert "test_external_validation_operator_execution_packet.py" in tests_agents
    assert "external-validation-operator-execution-packet.sh" in roadmap
