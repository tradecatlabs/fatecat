from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "external-evidence-submission-readiness-audit.py"
CONTRACT = ROOT / "contracts" / "fate" / "audit" / "external-evidence-submission-readiness-audit.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("external_evidence_submission_readiness_audit", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _work_queue() -> dict[str, Any]:
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
        "summary": {"totalOccurrences": 1, "workItems": 1},
        "shipGate": {"status": "blocked"},
        "workItems": [
            {
                "id": "external-work.release-production-api-live",
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
                "requiredEvidence": ["redacted live proof JSON"],
                "verificationCommands": ["bash scripts/production-readiness.sh --api-url <redacted>"],
                "closureCondition": "真实 live 证据通过后关闭。",
                "occurrences": [
                    {
                        "id": "external.release.production_api_live",
                        "source": {"path": "docs/release.md", "line": 1, "excerptSha256": "1" * 64},
                        "status": "external_connectivity_pending",
                    }
                ],
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _proof_ref_gate(*, accepted: bool) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_gate_summary",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "proofRefStatus": "schema_accepted_all_work_items" if accepted else "external_connectivity_pending",
        "summary": {
            "workItems": 1,
            "acceptedProofRefs": 1 if accepted else 0,
            "acceptedWorkItems": 1 if accepted else 0,
            "pendingWorkItems": 0 if accepted else 1,
        },
        "proofRefGate": {"status": "schema_accepted_all_work_items" if accepted else "external_connectivity_pending"},
        "shipGate": {
            "status": "blocked" if not accepted else "passed",
            "blockingItems": ["proof_ref_missing"] if not accepted else [],
        },
        "acceptedProofRefs": [
            {"id": "proof.release-api-live", "workItemId": "external-work.release-production-api-live"}
        ]
        if accepted
        else [],
        "pendingWorkItems": [{"id": "external-work.release-production-api-live"}] if not accepted else [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _live_proof_gate(*, accepted: bool) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_live_proof_gate_summary",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "liveProofStatus": "live_gate_accepted_all_work_items" if accepted else "external_connectivity_pending",
        "summary": {
            "workItems": 1,
            "acceptedLiveProofs": 1 if accepted else 0,
            "acceptedLiveWorkItems": 1 if accepted else 0,
            "pendingWorkItems": 0 if accepted else 1,
        },
        "liveProofGate": {
            "status": "live_gate_accepted_all_work_items" if accepted else "external_connectivity_pending"
        },
        "shipGate": {
            "status": "blocked" if not accepted else "passed",
            "blockingItems": ["category_live_evidence_missing"] if not accepted else [],
        },
        "acceptedLiveProofs": [{"id": "live.release-api-live"}] if accepted else [],
        "pendingWorkItems": [{"id": "external-work.release-production-api-live"}] if not accepted else [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _operator_packet() -> dict[str, Any]:
    command = "bash scripts/production-readiness.sh --api-url <redacted>"
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_operator_execution_packet",
        "status": "operator_action_required",
        "generatedAt": "2026-07-04T00:00:00Z",
        "source": {"commit": "a" * 40},
        "summary": {"operatorSteps": 1, "operatorCommands": 1, "proofRefTemplates": 1, "finalGateCommands": 1},
        "packetGate": {
            "status": "blocked",
            "blockingItems": ["operator_external_credentials_required", "proof_ref_bundle_required"],
        },
        "operatorSteps": [
            {
                "id": "operator-step.01.release-production-api-live",
                "domain": "release",
                "category": "release.production_api_live",
                "owners": ["release-ops"],
                "operatorCommands": [command],
                "operatorCommandSha256s": [_sha256_text(command)],
                "proofRefArtifactPattern": "evidence://external-validation/release-api-live",
                "sourceBinding": {
                    "workItemIds": ["external-work.release-production-api-live"],
                    "occurrenceIds": ["external.release.production_api_live"],
                },
            }
        ],
        "proofRefBundleTemplate": {
            "kind": "fatecat.external_validation_proof_ref_bundle",
            "status": "external_live_evidence_supplied_by_operator",
            "source": {"commit": "a" * 40},
            "proofRefs": [
                {
                    "id": "proof-ref-template.external-work.release-production-api-live",
                    "proofRef": "evidence://external-validation/release-api-live",
                    "artifactHash": "sha256:<64 lowercase hex artifact digest>",
                    "verificationCommand": command,
                }
            ],
        },
        "finalGateCommands": [
            {
                "id": "external-validation-proof-ref-gate",
                "command": "bash scripts/external-validation-proof-ref-gate.sh",
            }
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not execute external live checks."],
    }


def _human_review_gate(*, accepted: bool) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.core_quality_human_review_gate",
        "status": "passed",
        "humanReviewGate": {
            "status": "passed" if accepted else "blocked",
            "blockingItems": [] if accepted else ["professional_rubric_disposition_required"],
        },
        "externalBenchmarkGate": {
            "status": "passed" if accepted else "blocked",
            "blockingItems": [] if accepted else ["external_benchmark_aggregate_required"],
        },
        "noLeakGate": {
            "status": "passed" if accepted else "blocked",
            "blockingItems": [] if accepted else ["privacy_no_leak_signoff_required"],
        },
        "summary": {"acceptedReviews": 1 if accepted else 0, "pendingReviews": 0 if accepted else 1},
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not mean bazi/ziwei professional quality is 100% proven."],
    }


def _audit_rehearsal(*, accepted: bool) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.third_party_audit_rehearsal",
        "status": "passed",
        "rehearsalGate": {
            "status": "passed" if accepted else "blocked",
            "blockingItems": [] if accepted else ["external_validation_live_proof_gate_required"],
        },
        "summary": {"externalPending": 0 if accepted else 1},
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not replace third-party audit."],
    }


def _certification(*, accepted: bool) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.measurement_infrastructure_certification",
        "status": "passed" if accepted else "blocked",
        "certificationGate": {"canClaim100Percent": accepted},
        "domains": [{"id": "audit", "status": "passed" if accepted else "blocked"}],
        "externalPending": [] if accepted else [{"domain": "audit", "reason": "external proof pending"}],
        "blockingItems": [] if accepted else [{"domain": "audit", "reason": "blocked_gate"}],
        "privacyBoundary": "redacted_no_secret_values",
    }


def _fixtures(tmp_path: Path, *, accepted: bool = False) -> dict[str, Path]:
    return {
        "work_queue": _write(tmp_path / "work-queue.json", _work_queue()),
        "proof_ref_gate": _write(tmp_path / "proof-ref-gate.json", _proof_ref_gate(accepted=accepted)),
        "live_proof_gate": _write(tmp_path / "live-proof-gate.json", _live_proof_gate(accepted=accepted)),
        "operator_packet": _write(tmp_path / "operator-packet.json", _operator_packet()),
        "human_review_gate": _write(tmp_path / "human-review-gate.json", _human_review_gate(accepted=accepted)),
        "audit_rehearsal": _write(tmp_path / "third-party-audit-rehearsal.json", _audit_rehearsal(accepted=accepted)),
        "certification": _write(
            tmp_path / "measurement-infrastructure-certification.json", _certification(accepted=accepted)
        ),
    }


def test_contract_declares_submission_readiness_boundaries() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_evidence_submission_readiness_audit_contract"
    assert "fatecat.external_validation_proof_ref_gate_summary" in contract["requiredInputs"]
    assert "fatecat.core_quality_human_review_gate" in contract["requiredInputs"]
    assert "submissionReadinessGate" in contract["requiredOutputFields"]
    assert "operatorCommandAudit" in contract["requiredOutputFields"]
    assert "Does not execute external live checks." in contract["nonClaims"]
    assert "https://" in contract["forbiddenFragments"]


def test_readiness_audit_reports_current_external_blockers(tmp_path: Path) -> None:
    module = _load_module()
    fixtures = _fixtures(tmp_path, accepted=False)

    audit = module.build_audit(
        work_queue_json=fixtures["work_queue"],
        proof_ref_gate_json=fixtures["proof_ref_gate"],
        live_proof_gate_json=fixtures["live_proof_gate"],
        operator_packet_json=fixtures["operator_packet"],
        core_quality_human_review_json=fixtures["human_review_gate"],
        third_party_audit_rehearsal_json=fixtures["audit_rehearsal"],
        certification_json=fixtures["certification"],
        expected_commit="a" * 40,
    )
    serialized = json.dumps(audit, ensure_ascii=False, sort_keys=True)

    assert audit["kind"] == "fatecat.external_evidence_submission_readiness_audit"
    assert audit["status"] == "passed"
    assert audit["submissionReadinessGate"]["status"] == "blocked"
    assert audit["summary"]["blockedItems"] == 5
    assert audit["operatorCommandAudit"]["status"] == "passed"
    matrix = {item["id"]: item for item in audit["readinessMatrix"]}
    assert matrix["operator_execution_packet"]["status"] == "ready_for_operator"
    assert matrix["proof_ref_bundle_schema"]["status"] == "blocked"
    assert matrix["core_quality_human_review_bundle"]["status"] == "blocked"
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()


def test_readiness_audit_allows_synthetic_all_green_without_overriding_policy(tmp_path: Path) -> None:
    module = _load_module()
    fixtures = _fixtures(tmp_path, accepted=True)

    audit = module.build_audit(
        work_queue_json=fixtures["work_queue"],
        proof_ref_gate_json=fixtures["proof_ref_gate"],
        live_proof_gate_json=fixtures["live_proof_gate"],
        operator_packet_json=fixtures["operator_packet"],
        core_quality_human_review_json=fixtures["human_review_gate"],
        third_party_audit_rehearsal_json=fixtures["audit_rehearsal"],
        certification_json=fixtures["certification"],
        expected_commit="a" * 40,
    )

    assert audit["submissionReadinessStatus"] == "ready_for_final_submission"
    assert audit["submissionReadinessGate"]["status"] == "passed"
    assert audit["summary"]["blockedItems"] == 0
    assert audit["summary"]["readyItems"] == 6
    assert any("Does not execute external live checks." == item for item in audit["nonClaims"])


def test_readiness_audit_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    fixtures = _fixtures(tmp_path, accepted=False)
    output_json = tmp_path / "out" / "readiness.json"
    output_markdown = tmp_path / "out" / "READINESS.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--work-queue-json",
            str(fixtures["work_queue"]),
            "--proof-ref-gate-json",
            str(fixtures["proof_ref_gate"]),
            "--live-proof-gate-json",
            str(fixtures["live_proof_gate"]),
            "--operator-packet-json",
            str(fixtures["operator_packet"]),
            "--core-quality-human-review-json",
            str(fixtures["human_review_gate"]),
            "--third-party-audit-rehearsal-json",
            str(fixtures["audit_rehearsal"]),
            "--certification-json",
            str(fixtures["certification"]),
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
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["submissionReadinessGate"]["status"] == "blocked"
    assert "External Evidence Submission Readiness Audit" in output_markdown.read_text(encoding="utf-8")
    assert "submissionReadinessGate" in result.stdout


def test_readiness_audit_rejects_raw_url_and_sensitive_values(tmp_path: Path) -> None:
    module = _load_module()
    fixtures = _fixtures(tmp_path, accepted=False)
    work_queue = json.loads(fixtures["work_queue"].read_text(encoding="utf-8"))
    work_queue["workItems"][0]["category"] = "https://example.invalid/leak"
    _write(fixtures["work_queue"], work_queue)

    try:
        module.build_audit(
            work_queue_json=fixtures["work_queue"],
            proof_ref_gate_json=fixtures["proof_ref_gate"],
            live_proof_gate_json=fixtures["live_proof_gate"],
            operator_packet_json=fixtures["operator_packet"],
            core_quality_human_review_json=fixtures["human_review_gate"],
            third_party_audit_rehearsal_json=fixtures["audit_rehearsal"],
            certification_json=fixtures["certification"],
            expected_commit="a" * 40,
        )
    except module.ExternalEvidenceSubmissionReadinessAuditError as exc:
        assert "raw URL" in str(exc)
    else:
        raise AssertionError("raw URL was accepted")


def test_readiness_audit_wiring_mentions_local_ci_docs_and_tests() -> None:
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "external evidence submission readiness audit" in local_ci
    assert "FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT" in local_ci
    assert "external-evidence-submission-readiness-audit.py" in scripts_agents
    assert "external-evidence-submission-readiness-audit.json" in audit_agents
    assert "test_external_evidence_submission_readiness_audit.py" in tests_agents
    assert "External evidence submission readiness audit" in roadmap
