#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-evidence-submission-readiness-audit.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-evidence-submission-readiness-audit.json"
)
DEFAULT_OUTPUT_MARKDOWN = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT.md"
)

OUTPUT_KIND = "fatecat.external_evidence_submission_readiness_audit"
PRIVACY_BOUNDARY = "redacted_no_secret_values"
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^(?:sha256:)?[a-f0-9]{64}$")
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
FORBIDDEN_FRAGMENTS = {
    "fake proof",
    "dummy proof",
    "localhost proof",
    "placeholder proof",
}


class ExternalEvidenceSubmissionReadinessAuditError(RuntimeError):
    """外部证据提交准备度审计失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalEvidenceSubmissionReadinessAuditError(f"JSON root must be object: {path}")
    return payload


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _current_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload


def _assert_safe(payload: Any, *, area: str) -> None:
    rendered = _render(payload)
    if RAW_URL_RE.search(rendered):
        raise ExternalEvidenceSubmissionReadinessAuditError(f"{area}: raw URL detected")
    if SENSITIVE_RE.search(rendered):
        raise ExternalEvidenceSubmissionReadinessAuditError(f"{area}: sensitive-looking assignment detected")
    lowered = rendered.lower()
    for fragment in FORBIDDEN_FRAGMENTS:
        if fragment in lowered:
            raise ExternalEvidenceSubmissionReadinessAuditError(f"{area}: forbidden fragment detected: {fragment}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalEvidenceSubmissionReadinessAuditError(f"{area}.kind must be {expected}")


def _blocking_items(gate: Any) -> list[str]:
    if not isinstance(gate, dict):
        return []
    raw = gate.get("blockingItems", [])
    if isinstance(raw, dict):
        return [str(key) for key, value in raw.items() if value]
    if isinstance(raw, list):
        return [str(item) for item in raw if str(item)]
    if isinstance(raw, str) and raw:
        return [raw]
    return []


def _gate_status(payload: dict[str, Any], gate_name: str, fallback: str = "") -> str:
    gate = payload.get(gate_name)
    if isinstance(gate, dict) and gate.get("status"):
        return str(gate["status"])
    if payload.get(gate_name):
        return str(payload[gate_name])
    return fallback


def _summary_int(payload: dict[str, Any], key: str) -> int:
    summary = payload.get("summary")
    if isinstance(summary, dict) and isinstance(summary.get(key), int):
        return int(summary[key])
    return 0


def _readiness_item(
    *,
    item_id: str,
    label: str,
    status: str,
    blocking_items: list[str],
    next_action: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": item_id,
        "label": label,
        "status": status,
        "blockingItems": sorted(set(blocking_items)),
        "nextAction": next_action,
        "evidence": evidence,
    }


def _validate_operator_packet(packet: dict[str, Any], *, expected_commit: str) -> tuple[dict[str, Any], list[str]]:
    _require_kind(packet, expected="fatecat.external_validation_operator_execution_packet", area="operatorPacket")
    source = packet.get("source")
    if not isinstance(source, dict) or source.get("commit") != expected_commit:
        raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.source.commit mismatch")
    steps = packet.get("operatorSteps")
    if not isinstance(steps, list) or not steps:
        raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.operatorSteps must be non-empty array")
    final_commands = packet.get("finalGateCommands")
    if not isinstance(final_commands, list) or not final_commands:
        raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.finalGateCommands must be non-empty array")

    missing_command_hashes: list[str] = []
    operator_commands = 0
    for step in steps:
        if not isinstance(step, dict):
            raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.operatorSteps item must be object")
        commands = step.get("operatorCommands")
        hashes = step.get("operatorCommandSha256s")
        if not isinstance(commands, list) or not commands:
            raise ExternalEvidenceSubmissionReadinessAuditError(f"operator step {step.get('id')}: commands missing")
        if not isinstance(hashes, list) or len(hashes) != len(commands):
            missing_command_hashes.append(str(step.get("id", "unknown")))
        operator_commands += len(commands)

    template = packet.get("proofRefBundleTemplate")
    if not isinstance(template, dict):
        raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.proofRefBundleTemplate required")
    proof_refs = template.get("proofRefs")
    if not isinstance(proof_refs, list) or not proof_refs:
        raise ExternalEvidenceSubmissionReadinessAuditError("operatorPacket.proofRefBundleTemplate.proofRefs required")

    missing_artifact_hash: list[str] = []
    placeholder_artifact_hashes = 0
    concrete_artifact_hashes = 0
    for proof_ref in proof_refs:
        if not isinstance(proof_ref, dict):
            raise ExternalEvidenceSubmissionReadinessAuditError("proofRefBundleTemplate.proofRefs item must be object")
        proof_ref_id = str(proof_ref.get("id", "unknown"))
        artifact_hash = str(proof_ref.get("artifactHash", ""))
        if not artifact_hash:
            missing_artifact_hash.append(proof_ref_id)
        elif artifact_hash == "sha256:<64 lowercase hex artifact digest>":
            placeholder_artifact_hashes += 1
        elif SHA256_RE.match(artifact_hash):
            concrete_artifact_hashes += 1
        else:
            raise ExternalEvidenceSubmissionReadinessAuditError(
                f"proofRefBundleTemplate {proof_ref_id}: invalid artifactHash"
            )

    audit = {
        "operatorSteps": len(steps),
        "operatorCommands": operator_commands,
        "finalGateCommands": len(final_commands),
        "proofRefTemplates": len(proof_refs),
        "placeholderArtifactHashes": placeholder_artifact_hashes,
        "concreteArtifactHashes": concrete_artifact_hashes,
        "missingArtifactHashFields": missing_artifact_hash,
        "missingCommandHashSteps": missing_command_hashes,
    }
    blockers = []
    if missing_artifact_hash:
        blockers.append("proof_ref_template_artifact_hash_field_missing")
    if missing_command_hashes:
        blockers.append("operator_command_hash_missing")
    return audit, blockers


def _proof_ref_item(proof_ref_gate: dict[str, Any]) -> dict[str, Any]:
    proof_ref_status = str(proof_ref_gate.get("proofRefStatus") or _gate_status(proof_ref_gate, "proofRefGate"))
    accepted = _summary_int(proof_ref_gate, "acceptedProofRefs")
    pending = _summary_int(proof_ref_gate, "pendingWorkItems")
    blocking = _blocking_items(proof_ref_gate.get("shipGate"))
    ready = proof_ref_status == "schema_accepted_all_work_items" and pending == 0 and accepted > 0
    if not ready and "proof_ref_bundle_required" not in blocking:
        blocking.append("proof_ref_bundle_required")
    return _readiness_item(
        item_id="proof_ref_bundle_schema",
        label="Proof-ref bundle schema submission",
        status="ready" if ready else "blocked",
        blocking_items=[] if ready else blocking,
        next_action="Submit redacted proof-ref bundle and rerun proof-ref gate."
        if not ready
        else "Rerun category live proof gate.",
        evidence={
            "proofRefStatus": proof_ref_status,
            "acceptedProofRefs": accepted,
            "pendingWorkItems": pending,
        },
    )


def _live_proof_item(live_proof_gate: dict[str, Any]) -> dict[str, Any]:
    live_status = str(live_proof_gate.get("liveProofStatus") or _gate_status(live_proof_gate, "liveProofGate"))
    accepted = _summary_int(live_proof_gate, "acceptedLiveProofs")
    pending = _summary_int(live_proof_gate, "pendingWorkItems")
    blocking = _blocking_items(live_proof_gate.get("shipGate"))
    ready = live_status == "live_gate_accepted_all_work_items" and pending == 0 and accepted > 0
    if not ready and "category_live_evidence_required" not in blocking:
        blocking.append("category_live_evidence_required")
    return _readiness_item(
        item_id="live_proof_bundle_schema",
        label="Category live proof bundle submission",
        status="ready" if ready else "blocked",
        blocking_items=[] if ready else blocking,
        next_action="Execute category runbooks and submit redacted live proof bundle."
        if not ready
        else "Proceed to audit rehearsal.",
        evidence={
            "liveProofStatus": live_status,
            "acceptedLiveProofs": accepted,
            "pendingWorkItems": pending,
        },
    )


def _operator_item(
    operator_packet: dict[str, Any], operator_audit: dict[str, Any], blockers: list[str]
) -> dict[str, Any]:
    packet_gate = operator_packet.get("packetGate")
    gate_blockers = _blocking_items(packet_gate)
    status = "ready_for_operator" if not blockers else "blocked"
    return _readiness_item(
        item_id="operator_execution_packet",
        label="Operator execution packet",
        status=status,
        blocking_items=blockers,
        next_action="Operator must execute runbooks and fill artifact hashes/proof refs."
        if not blockers
        else "Regenerate operator packet.",
        evidence={
            **operator_audit,
            "packetGateStatus": _gate_status(operator_packet, "packetGate"),
            "packetGateBlockingItems": gate_blockers,
        },
    )


def _human_review_item(human_review_gate: dict[str, Any]) -> dict[str, Any]:
    gate_status = _gate_status(human_review_gate, "humanReviewGate")
    benchmark_status = _gate_status(human_review_gate, "externalBenchmarkGate")
    no_leak_status = _gate_status(human_review_gate, "noLeakGate")
    ready = gate_status == "passed" and benchmark_status == "passed" and no_leak_status == "passed"
    blocking = []
    for gate_name in ("humanReviewGate", "externalBenchmarkGate", "noLeakGate"):
        blocking.extend(_blocking_items(human_review_gate.get(gate_name)))
    if not ready and not blocking:
        blocking.extend(
            [
                "professional_rubric_disposition_required",
                "external_benchmark_aggregate_required",
                "privacy_no_leak_signoff_required",
            ]
        )
    return _readiness_item(
        item_id="core_quality_human_review_bundle",
        label="Core quality human review bundle",
        status="ready" if ready else "blocked",
        blocking_items=[] if ready else blocking,
        next_action="Submit expert review, external benchmark aggregate and no-leak signoff bundle."
        if not ready
        else "Use accepted review gate in final certification.",
        evidence={
            "humanReviewGate": gate_status,
            "externalBenchmarkGate": benchmark_status,
            "noLeakGate": no_leak_status,
            "acceptedReviews": _summary_int(human_review_gate, "acceptedReviews"),
        },
    )


def _audit_rehearsal_item(rehearsal: dict[str, Any]) -> dict[str, Any]:
    status = _gate_status(rehearsal, "rehearsalGate")
    ready = status == "passed"
    blocking = _blocking_items(rehearsal.get("rehearsalGate"))
    if not ready and not blocking:
        blocking.append("third_party_audit_rehearsal_blocked")
    return _readiness_item(
        item_id="third_party_audit_rehearsal",
        label="Third-party audit rehearsal",
        status="ready" if ready else "blocked",
        blocking_items=[] if ready else blocking,
        next_action="Close external evidence and independent audit result before final rehearsal."
        if not ready
        else "Submit rehearsal package to independent auditor.",
        evidence={
            "rehearsalGate": status,
            "externalPending": _summary_int(rehearsal, "externalPending"),
            "blockingItems": len(blocking),
        },
    )


def _certification_item(certification: dict[str, Any]) -> dict[str, Any]:
    gate = certification.get("certificationGate")
    can_claim = bool(isinstance(gate, dict) and gate.get("canClaim100Percent") is True)
    status = str(certification.get("status", ""))
    ready = status == "passed" and can_claim
    blocking = [str(item.get("reason", item)) for item in certification.get("blockingItems", [])]
    if not ready and not blocking:
        blocking.append("measurement_infrastructure_certification_not_passed")
    return _readiness_item(
        item_id="measurement_infrastructure_certification",
        label="Measurement infrastructure certification",
        status="ready" if ready else "blocked",
        blocking_items=[] if ready else blocking,
        next_action="Rerun certification only after all evidence domains pass."
        if not ready
        else "100% claim may be reviewed.",
        evidence={
            "status": status,
            "canClaim100Percent": can_claim,
            "domains": len(certification.get("domains", [])) if isinstance(certification.get("domains"), list) else 0,
            "externalPending": len(certification.get("externalPending", []))
            if isinstance(certification.get("externalPending"), list)
            else 0,
            "blockingItems": len(certification.get("blockingItems", []))
            if isinstance(certification.get("blockingItems"), list)
            else 0,
        },
    )


def build_audit(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    live_proof_gate_json: Path,
    operator_packet_json: Path,
    core_quality_human_review_json: Path,
    third_party_audit_rehearsal_json: Path,
    certification_json: Path,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    if contract.get("kind") != "fatecat.external_evidence_submission_readiness_audit_contract":
        raise ExternalEvidenceSubmissionReadinessAuditError("contract.kind mismatch")
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalEvidenceSubmissionReadinessAuditError("--expected-commit must be 40 lowercase hex chars")

    input_paths = {
        "workQueue": work_queue_json,
        "proofRefGate": proof_ref_gate_json,
        "liveProofGate": live_proof_gate_json,
        "operatorPacket": operator_packet_json,
        "coreQualityHumanReviewGate": core_quality_human_review_json,
        "thirdPartyAuditRehearsal": third_party_audit_rehearsal_json,
        "certification": certification_json,
    }
    for path in input_paths.values():
        if not path.is_file():
            raise ExternalEvidenceSubmissionReadinessAuditError(f"input json missing: {path}")

    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    live_proof_gate = _load_json(live_proof_gate_json)
    operator_packet = _load_json(operator_packet_json)
    human_review_gate = _load_json(core_quality_human_review_json)
    audit_rehearsal = _load_json(third_party_audit_rehearsal_json)
    certification = _load_json(certification_json)

    for area, payload in (
        ("workQueue", work_queue),
        ("proofRefGate", proof_ref_gate),
        ("liveProofGate", live_proof_gate),
        ("operatorPacket", operator_packet),
        ("coreQualityHumanReviewGate", human_review_gate),
        ("thirdPartyAuditRehearsal", audit_rehearsal),
        ("certification", certification),
    ):
        _assert_safe(payload, area=area)

    _require_kind(work_queue, expected="fatecat.external_validation_closure_work_queue", area="workQueue")
    _require_kind(proof_ref_gate, expected="fatecat.external_validation_proof_ref_gate_summary", area="proofRefGate")
    _require_kind(live_proof_gate, expected="fatecat.external_validation_live_proof_gate_summary", area="liveProofGate")
    _require_kind(
        human_review_gate, expected="fatecat.core_quality_human_review_gate", area="coreQualityHumanReviewGate"
    )
    _require_kind(audit_rehearsal, expected="fatecat.third_party_audit_rehearsal", area="thirdPartyAuditRehearsal")
    _require_kind(certification, expected="fatecat.measurement_infrastructure_certification", area="certification")

    operator_audit, operator_blockers = _validate_operator_packet(operator_packet, expected_commit=expected_commit)
    readiness_matrix = [
        _operator_item(operator_packet, operator_audit, operator_blockers),
        _proof_ref_item(proof_ref_gate),
        _live_proof_item(live_proof_gate),
        _human_review_item(human_review_gate),
        _audit_rehearsal_item(audit_rehearsal),
        _certification_item(certification),
    ]
    blocked_items = [item for item in readiness_matrix if item["status"] == "blocked"]
    ready_items = [item for item in readiness_matrix if item["status"] != "blocked"]
    blocking_items = [
        {"id": item["id"], "blockingItems": item["blockingItems"], "nextAction": item["nextAction"]}
        for item in blocked_items
    ]
    submission_status = "ready_for_final_submission" if not blocked_items else "blocked"

    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": _utc_now(),
        "status": "passed",
        "submissionReadinessStatus": submission_status,
        "source": {
            "expectedCommit": expected_commit,
            "inputs": {
                key: {"path": str(path), "sha256": _sha256_file(path)} for key, path in sorted(input_paths.items())
            },
        },
        "summary": {
            "inputs": len(input_paths),
            "workItems": len(work_queue.get("workItems", [])) if isinstance(work_queue.get("workItems"), list) else 0,
            "readinessItems": len(readiness_matrix),
            "readyItems": len(ready_items),
            "blockedItems": len(blocked_items),
            "operatorSteps": operator_audit["operatorSteps"],
            "operatorCommands": operator_audit["operatorCommands"],
            "proofRefTemplates": operator_audit["proofRefTemplates"],
            "placeholderArtifactHashes": operator_audit["placeholderArtifactHashes"],
        },
        "submissionReadinessGate": {
            "status": "passed" if submission_status == "ready_for_final_submission" else "blocked",
            "blockingItems": [item["id"] for item in blocked_items],
            "policy": contract["submissionPolicy"],
        },
        "operatorCommandAudit": {
            "status": "passed" if not operator_blockers else "blocked",
            "details": operator_audit,
        },
        "readinessMatrix": readiness_matrix,
        "blockingItems": blocking_items,
        "privacyBoundary": PRIVACY_BOUNDARY,
        "nonClaims": contract["nonClaims"],
    }
    _assert_safe(summary, area="summary")
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# External Evidence Submission Readiness Audit",
        "",
        f"- status: `{summary['status']}`",
        f"- submissionReadinessStatus: `{summary['submissionReadinessStatus']}`",
        f"- gate: `{summary['submissionReadinessGate']['status']}`",
        f"- expectedCommit: `{summary['source']['expectedCommit']}`",
        "",
        "## Readiness Matrix",
        "",
        "| ID | Status | Blocking Items | Next Action |",
        "| --- | --- | --- | --- |",
    ]
    for item in summary["readinessMatrix"]:
        blockers = ", ".join(item["blockingItems"]) if item["blockingItems"] else "-"
        lines.append(f"| `{item['id']}` | `{item['status']}` | {blockers} | {item['nextAction']} |")
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
        ]
    )
    for item in summary["nonClaims"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit readiness for external evidence submission bundles.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--proof-ref-gate-json", type=Path, required=True)
    parser.add_argument("--live-proof-gate-json", type=Path, required=True)
    parser.add_argument("--operator-packet-json", type=Path, required=True)
    parser.add_argument("--core-quality-human-review-json", type=Path, required=True)
    parser.add_argument("--third-party-audit-rehearsal-json", type=Path, required=True)
    parser.add_argument("--certification-json", type=Path, required=True)
    parser.add_argument("--expected-commit")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_MARKDOWN)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_audit(
            work_queue_json=args.work_queue_json,
            proof_ref_gate_json=args.proof_ref_gate_json,
            live_proof_gate_json=args.live_proof_gate_json,
            operator_packet_json=args.operator_packet_json,
            core_quality_human_review_json=args.core_quality_human_review_json,
            third_party_audit_rehearsal_json=args.third_party_audit_rehearsal_json,
            certification_json=args.certification_json,
            expected_commit=args.expected_commit,
        )
        _write_json(args.output_json, summary)
        _write_text(args.output_markdown, render_markdown(summary))
        print(
            json.dumps(
                {
                    "kind": summary["kind"],
                    "status": summary["status"],
                    "submissionReadinessStatus": summary["submissionReadinessStatus"],
                    "submissionReadinessGate": summary["submissionReadinessGate"]["status"],
                    "blockedItems": summary["summary"]["blockedItems"],
                    "outputJson": str(args.output_json),
                    "outputMarkdown": str(args.output_markdown),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (
        ExternalEvidenceSubmissionReadinessAuditError,
        OSError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"external evidence submission readiness audit error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
