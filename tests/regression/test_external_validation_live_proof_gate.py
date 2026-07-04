from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-live-proof-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-live-proof-gate.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_live_proof_gate", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _work_item() -> dict:
    return {
        "id": "external-work.api",
        "owner": "release-ops",
        "assignee": "unassigned:release-ops",
        "category": "release.production_api_live",
        "priority": "P0",
        "status": "pending_external_evidence",
        "proofRef": "",
        "lastCheckedAt": "2026-07-04T00:00:00Z",
        "staleReason": "proof_ref_missing",
        "closeConditionResult": "not_evaluated_no_proof_ref",
        "credentialDependencies": ["production API token"],
        "requiredEvidence": ["redacted live API proof"],
        "verificationCommands": ["bash scripts/production-readiness.sh --api-url <redacted>"],
        "closureCondition": "真实 production API live smoke 通过后关闭。",
        "occurrences": [
            {
                "id": "external.api.1",
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
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_work_queue",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "closurePlanJson": "fixture",
            "closurePlanSha256": "0" * 64,
            "closurePlanKind": "fatecat.external_validation_closure_plan",
            "closureItemCount": 1,
        },
        "summary": {
            "totalOccurrences": 1,
            "workItems": 1,
        },
        "shipGate": {"status": "blocked"},
        "workItems": [_work_item()],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _proof_ref_gate(*, accepted: bool = True) -> dict:
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
            "workItems": 1,
            "acceptedProofRefs": 1 if accepted else 0,
            "acceptedWorkItems": 1 if accepted else 0,
            "pendingWorkItems": 0 if accepted else 1,
            "proofRefStatus": "schema_accepted_all_work_items" if accepted else "external_connectivity_pending",
        },
        "proofRefStatus": "schema_accepted_all_work_items" if accepted else "external_connectivity_pending",
        "proofRefGate": {"status": "schema_accepted_all_work_items" if accepted else "external_connectivity_pending"},
        "shipGate": {"status": "blocked"},
        "acceptedProofRefs": [
            {
                "id": "proof.api",
                "proofRef": "evidence://external-validation/release-api-live",
                "evidenceType": "production_api_live_smoke",
                "workItemId": "external-work.api",
                "owner": "release-ops",
                "category": "release.production_api_live",
                "issuer": "operator:release-ops",
                "capturedAt": "2026-07-04T00:00:00Z",
                "expiresAt": "2099-01-01T00:00:00Z",
                "artifactHash": f"sha256:{'b' * 64}",
                "verificationCommandSha256": "c" * 64,
                "occurrenceIds": ["external.api.1"],
            }
        ]
        if accepted
        else [],
        "pendingWorkItems": [] if accepted else [{"id": "external-work.api"}],
        "negativeEvidenceRejected": [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _runbooks() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_category_runbooks",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "summary": {"categories": 1, "runbooks": 1},
        "runbookStatus": "operator_runbooks_ready",
        "runbookGate": {"status": "passed"},
        "shipGate": {"status": "blocked"},
        "runbooks": [
            {
                "id": "external-runbook.release.production_api_live",
                "category": "release.production_api_live",
                "owners": ["release-ops"],
                "priority": "P0",
                "status": "operator_action_required",
                "evidenceType": "production_api_live_smoke",
                "requiredCredentials": ["production API token"],
                "operatorCommands": ["bash scripts/production-readiness.sh --api-url <redacted>"],
                "proofRefArtifactPattern": "evidence://external-validation/release.production_api_live/<run-id>",
                "redactionRule": "redact secrets",
                "expiryPolicy": "14 days",
                "failureRollback": "keep blocked",
                "closureCondition": "真实 production API live smoke 通过后关闭。",
                "verifierCommand": "bash scripts/external-validation-live-proof-gate.sh --work-queue-json <path>",
                "sourceWorkItemIds": ["external-work.api"],
                "occurrenceCount": 1,
                "nonClaims": ["Runbook readiness does not prove live evidence has passed."],
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _write_gate_inputs(tmp_path: Path, *, accepted_proof_ref: bool = True) -> tuple[Path, Path, Path]:
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    category_runbooks_json = tmp_path / "category-runbooks.json"
    _write_json(work_queue_json, _work_queue())
    _write_json(proof_ref_gate_json, _proof_ref_gate(accepted=accepted_proof_ref))
    _write_json(category_runbooks_json, _runbooks())
    return work_queue_json, proof_ref_gate_json, category_runbooks_json


def _live_evidence(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    commit: str = "a" * 40,
) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_live_evidence_bundle",
        "status": "external_live_evidence_supplied_by_operator",
        "generatedAt": "2026-07-04T00:00:00Z",
        "source": {
            "workQueueKind": "fatecat.external_validation_closure_work_queue",
            "workQueueSha256": _sha256(work_queue_json),
            "proofRefGateKind": "fatecat.external_validation_proof_ref_gate_summary",
            "proofRefGateSha256": _sha256(proof_ref_gate_json),
            "categoryRunbooksKind": "fatecat.external_validation_category_runbooks",
            "categoryRunbooksSha256": _sha256(category_runbooks_json),
            "commit": commit,
        },
        "liveProofs": [
            {
                "id": "live-proof.api",
                "proofRefId": "proof.api",
                "workItemId": "external-work.api",
                "owner": "release-ops",
                "category": "release.production_api_live",
                "runbookId": "external-runbook.release.production_api_live",
                "liveGateKind": "production_api_live_smoke",
                "liveGateStatus": "passed",
                "issuer": "operator:release-ops",
                "capturedAt": "2026-07-04T00:00:00Z",
                "expiresAt": "2099-01-01T00:00:00Z",
                "redactionBoundary": "redacted_no_secret_values",
                "verificationCommand": "bash scripts/production-readiness.sh --api-url <redacted>",
                "artifactHash": f"sha256:{'d' * 64}",
                "operatorAttestation": "real_external_execution_redacted",
                "sourceBinding": {
                    "commit": commit,
                    "workQueueSha256": _sha256(work_queue_json),
                    "proofRefGateSha256": _sha256(proof_ref_gate_json),
                    "categoryRunbooksSha256": _sha256(category_runbooks_json),
                    "occurrenceIds": ["external.api.1"],
                },
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not replace third-party audit."],
    }


def test_external_validation_live_proof_contract_lists_required_fields():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_live_proof_gate_contract"
    assert "fatecat.external_validation_live_evidence_bundle" in contract["inputKinds"]
    assert contract["inputSchema"] == "contracts/fate/audit/schemas/external-validation-live-evidence.schema.json"
    assert "operatorAttestation" in contract["requiredFieldsPerLiveProof"]
    assert contract["requiredOperatorAttestation"] == "real_external_execution_redacted"
    assert "Does not mean FateCat is 100% production infrastructure." in contract["nonClaims"]


def test_external_validation_live_proof_gate_outputs_pending_without_live_evidence(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_gate_inputs(tmp_path)

    summary = module.build_summary(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
        expected_commit="a" * 40,
    )

    assert summary["kind"] == "fatecat.external_validation_live_proof_gate_summary"
    assert summary["liveProofStatus"] == "external_connectivity_pending"
    assert summary["summary"]["pendingWorkItems"] == 1
    assert summary["shipGate"]["status"] == "blocked"
    assert "category_live_evidence_missing" in summary["shipGate"]["blockingItems"]


def test_external_validation_live_proof_gate_accepts_redacted_live_evidence(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_gate_inputs(tmp_path)
    evidence_json = tmp_path / "live-evidence.json"
    _write_json(
        evidence_json,
        _live_evidence(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=category_runbooks_json,
        ),
    )

    summary = module.build_summary(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
        live_evidence_json=evidence_json,
        expected_commit="a" * 40,
    )

    assert summary["liveProofStatus"] == "live_gate_accepted_all_work_items"
    assert summary["summary"]["acceptedLiveProofs"] == 1
    assert summary["summary"]["pendingWorkItems"] == 0
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["shipGate"]["blockingItems"] == [
        "third_party_audit_review_pending",
        "certification_external_claim_review_pending",
    ]
    accepted = summary["acceptedLiveProofs"][0]
    assert accepted["verificationCommandSha256"]
    assert "verificationCommand" not in accepted


def test_external_validation_live_proof_gate_rejects_live_without_schema_accepted_proof_ref(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_gate_inputs(
        tmp_path, accepted_proof_ref=False
    )
    evidence_json = tmp_path / "live-evidence.json"
    _write_json(
        evidence_json,
        _live_evidence(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=category_runbooks_json,
        ),
    )

    try:
        module.build_summary(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=category_runbooks_json,
            live_evidence_json=evidence_json,
            expected_commit="a" * 40,
        )
    except module.ExternalValidationLiveProofGateError as exc:
        assert "proofRefId was not schema-accepted" in str(exc)
    else:
        raise AssertionError("live proof without accepted proof-ref must be rejected")


def test_external_validation_live_proof_gate_rejects_raw_url_and_placeholder(tmp_path):
    module = _load_module()
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_gate_inputs(tmp_path)
    evidence = _live_evidence(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
    )
    evidence["liveProofs"][0]["verificationCommand"] = (
        "bash scripts/production-readiness.sh --api-url https://example.invalid"
    )
    evidence["liveProofs"][0]["liveGateKind"] = "placeholder"
    evidence_json = tmp_path / "live-evidence.json"
    _write_json(evidence_json, evidence)

    try:
        module.build_summary(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=category_runbooks_json,
            live_evidence_json=evidence_json,
            expected_commit="a" * 40,
        )
    except module.ExternalValidationLiveProofGateError as exc:
        assert "forbidden fragment" in str(exc)
    else:
        raise AssertionError("raw URLs and placeholder live proof must be rejected")


def test_external_validation_live_proof_gate_cli_writes_summary(tmp_path):
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_gate_inputs(tmp_path)
    output_json = tmp_path / "summary.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--work-queue-json",
            str(work_queue_json),
            "--proof-ref-gate-json",
            str(proof_ref_gate_json),
            "--category-runbooks-json",
            str(category_runbooks_json),
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
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["liveProofStatus"] == "external_connectivity_pending"


def test_external_validation_live_proof_gate_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    certification_contract = json.loads(
        (ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json").read_text(
            encoding="utf-8"
        )
    )

    assert "external-validation-live-proof-gate.sh" in local_ci
    assert "external-validation-live-proof-gate.py" in scripts_agents
    assert "external-validation-live-proof-gate.json" in audit_agents
    assert "test_external_validation_live_proof_gate.py" in tests_agents
    assert "external-validation-live-proof-gate.json" in certification_contract["requiredEvidenceFiles"]
