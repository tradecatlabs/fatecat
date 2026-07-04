from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-proof-ref-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-proof-ref.json"
SCHEMA_PATH = ROOT / "contracts" / "fate" / "audit" / "schemas" / "external-validation-proof-ref.schema.json"

EXPECTED_COMMIT = "a" * 40


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_proof_ref_gate", SCRIPT_PATH)
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
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _work_queue_payload() -> dict:
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
        "shipGate": {
            "status": "blocked",
        },
        "workItems": [
            {
                "id": "external-work.release-api-live",
                "owner": "release-ops",
                "assignee": "unassigned:release-ops",
                "category": "release.production_api_live",
                "priority": "P0",
                "status": "pending_external_evidence",
                "proofRef": "",
                "lastCheckedAt": "2026-07-04T00:00:00Z",
                "staleReason": "proof_ref_missing",
                "closeConditionResult": "not_evaluated_no_proof_ref",
                "credentialDependencies": ["production API credential"],
                "requiredEvidence": ["redacted production API live smoke proof"],
                "verificationCommands": ["bash scripts/production-readiness.sh --api-url <redacted>"],
                "closureCondition": "真实 production API live smoke 通过后关闭。",
                "occurrences": [
                    {
                        "id": "external.release-api-live",
                        "source": {
                            "path": "docs/release.md",
                            "line": 1,
                            "excerptSha256": "1" * 64,
                        },
                        "status": "external_connectivity_pending",
                    }
                ],
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _write_work_queue(tmp_path: Path) -> tuple[Path, str]:
    path = tmp_path / "external-validation-closure-work-queue.json"
    _write_json(path, _work_queue_payload())
    return path, _sha256_file(path)


def _evidence_payload(*, work_queue_sha256: str) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_bundle",
        "status": "external_live_evidence_supplied_by_operator",
        "generatedAt": "2026-07-04T00:00:00Z",
        "source": {
            "workQueueKind": "fatecat.external_validation_closure_work_queue",
            "workQueueSha256": work_queue_sha256,
            "commit": EXPECTED_COMMIT,
        },
        "proofRefs": [
            {
                "id": "proof.release-api-live",
                "proofRef": "evidence://external-validation/release-api-live-0120",
                "evidenceType": "production_api_live_smoke",
                "workItemId": "external-work.release-api-live",
                "owner": "release-ops",
                "category": "release.production_api_live",
                "issuer": "operator:release-ops",
                "capturedAt": "2026-07-04T00:00:00Z",
                "expiresAt": "2099-01-01T00:00:00Z",
                "redactionBoundary": "redacted_no_secret_values",
                "verificationCommand": "bash scripts/production-readiness.sh --api-url <redacted>",
                "artifactHash": f"sha256:{'b' * 64}",
                "sourceBinding": {
                    "commit": EXPECTED_COMMIT,
                    "workQueueSha256": work_queue_sha256,
                    "occurrenceIds": ["external.release-api-live"],
                },
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def test_proof_ref_contract_lists_schema_and_non_claims():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_proof_ref_contract"
    assert contract["inputSchema"] == "contracts/fate/audit/schemas/external-validation-proof-ref.schema.json"
    assert contract["allowedProofRefPrefixes"] == ["evidence://", "artifact://", "ci-artifact://"]
    assert "proofRef" in contract["requiredFieldsPerProofRef"]
    assert "verificationCommand" in contract["requiredFieldsPerProofRef"]
    assert "Does not replace third-party audit." in contract["nonClaims"]
    assert schema["$defs"]["proofRef"]["properties"]["artifactHash"]["pattern"] == "^sha256:[a-f0-9]{64}$"


def test_proof_ref_gate_outputs_pending_without_evidence(tmp_path):
    module = _load_module()
    work_queue_json, _work_queue_sha256 = _write_work_queue(tmp_path)

    summary = module.build_summary(work_queue_json=work_queue_json, expected_commit=EXPECTED_COMMIT)

    assert summary["status"] == "passed"
    assert summary["proofRefStatus"] == "external_connectivity_pending"
    assert summary["proofRefGate"]["status"] == "external_connectivity_pending"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["shipGate"]["blockingItems"] == ["proof_ref_missing"]
    assert summary["summary"]["pendingWorkItems"] == 1
    assert summary["negativeEvidenceRejected"] == [
        "fake.placeholder_proof_ref",
        "fake.wrong_commit",
        "fake.category_mismatch",
    ]


def test_proof_ref_gate_accepts_redacted_operator_bundle_without_shipping(tmp_path):
    module = _load_module()
    work_queue_json, work_queue_sha256 = _write_work_queue(tmp_path)
    evidence_json = tmp_path / "proof-ref-bundle.json"
    _write_json(evidence_json, _evidence_payload(work_queue_sha256=work_queue_sha256))

    summary = module.build_summary(
        work_queue_json=work_queue_json,
        evidence_json=evidence_json,
        expected_commit=EXPECTED_COMMIT,
    )
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    assert summary["proofRefStatus"] == "schema_accepted_all_work_items"
    assert summary["summary"]["acceptedProofRefs"] == 1
    assert summary["summary"]["pendingWorkItems"] == 0
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["shipGate"]["blockingItems"] == ["category_live_gates_pending", "third_party_audit_review_pending"]
    assert "verificationCommand" not in summary["acceptedProofRefs"][0]
    assert "verificationCommandSha256" in summary["acceptedProofRefs"][0]
    assert "https://" not in rendered
    assert "token=" not in rendered
    assert "secret=" not in rendered


def test_proof_ref_gate_rejects_raw_url_evidence(tmp_path):
    module = _load_module()
    work_queue_json, work_queue_sha256 = _write_work_queue(tmp_path)
    payload = _evidence_payload(work_queue_sha256=work_queue_sha256)
    payload["proofRefs"][0]["proofRef"] = "https://example.invalid/proof"
    evidence_json = tmp_path / "proof-ref-bundle.json"
    _write_json(evidence_json, payload)

    with pytest.raises(module.ProofRefGateError, match="raw fragment"):
        module.build_summary(
            work_queue_json=work_queue_json,
            evidence_json=evidence_json,
            expected_commit=EXPECTED_COMMIT,
        )


def test_proof_ref_gate_cli_writes_pending_summary(tmp_path):
    module = _load_module()
    work_queue_json, _work_queue_sha256 = _write_work_queue(tmp_path)
    output_json = tmp_path / "out.json"

    exit_code = module.main(
        [
            "--work-queue-json",
            str(work_queue_json),
            "--expected-commit",
            EXPECTED_COMMIT,
            "--output-json",
            str(output_json),
        ]
    )

    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert stored["proofRefStatus"] == "external_connectivity_pending"
    assert stored["shipGate"]["status"] == "blocked"


def test_proof_ref_gate_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    certification_contract = (
        ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"
    ).read_text(encoding="utf-8")

    assert "external validation proof-ref gate" in local_ci
    assert "externalValidationProofRefGate" in local_ci
    assert "external-validation-proof-ref-gate.py" in scripts_agents
    assert "external-validation-proof-ref.json" in audit_agents
    assert "test_external_validation_proof_ref_gate.py" in tests_agents
    assert "external-validation-proof-ref-gate.json" in certification_contract
