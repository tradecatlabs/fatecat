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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-live-proof-gate.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-live-proof-gate.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
LIVE_EVIDENCE_KIND = "fatecat.external_validation_live_evidence_bundle"
OUTPUT_KIND = "fatecat.external_validation_live_proof_gate_summary"

PENDING_STATUS = "external_connectivity_pending"
LIVE_SUPPLIED_STATUS = "external_live_evidence_supplied_by_operator"
REDACTION_BOUNDARY = "redacted_no_secret_values"
OPERATOR_ATTESTATION = "real_external_execution_redacted"
ALLOWED_COMMAND_PREFIXES = ("bash scripts/", "python3 scripts/", "gh run view ")

SENSITIVE_FRAGMENTS = {
    "BEGIN OPENSSH",
    "BEGIN RSA",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "callback_url=",
    "password=",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}

FORBIDDEN_TEXT = {
    "changeme",
    "debug",
    "dry-run",
    "dummy",
    "fake",
    "local only",
    "localhost",
    "placeholder",
    "sample",
}

SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


class ExternalValidationLiveProofGateError(RuntimeError):
    """外部验证 live proof gate 失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationLiveProofGateError(f"JSON root must be object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_forbidden(payload: Any, *, area: str) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if re.search(r"https?://", rendered, re.I):
        bad.append("raw_url")
    bad.extend(sorted(fragment for fragment in FORBIDDEN_TEXT if fragment in rendered))
    if bad:
        raise ExternalValidationLiveProofGateError(f"{area}: forbidden fragment detected: {', '.join(bad)}")


def _parse_timestamp(value: str, *, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ExternalValidationLiveProofGateError(f"{field}: timestamp required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ExternalValidationLiveProofGateError(f"{field}: must be ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ExternalValidationLiveProofGateError(f"{field}: timezone required")
    return parsed.astimezone(UTC)


def _require_fields(area: str, payload: dict[str, Any], fields: list[str]) -> None:
    missing = [field for field in fields if payload.get(field) in ("", None, [])]
    if missing:
        raise ExternalValidationLiveProofGateError(f"{area}: missing fields {missing}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalValidationLiveProofGateError(f"{area}.kind must be {expected}")


def _validate_work_queue(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(payload, expected=WORK_QUEUE_KIND, area="workQueue")
    work_items = payload.get("workItems")
    if not isinstance(work_items, list):
        raise ExternalValidationLiveProofGateError("workQueue.workItems must be array")
    index: dict[str, dict[str, Any]] = {}
    for idx, item in enumerate(work_items):
        if not isinstance(item, dict):
            raise ExternalValidationLiveProofGateError(f"workQueue.workItems[{idx}] must be object")
        _require_fields("workQueue.workItem", item, ["id", "owner", "category", "occurrences"])
        occurrences = item.get("occurrences")
        if not isinstance(occurrences, list) or not occurrences:
            raise ExternalValidationLiveProofGateError(f"work item {item['id']}: occurrences required")
        index[str(item["id"])] = item
    return index


def _validate_proof_ref_gate(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(payload, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    accepted = payload.get("acceptedProofRefs")
    if not isinstance(accepted, list):
        raise ExternalValidationLiveProofGateError("proofRefGate.acceptedProofRefs must be array")
    proof_refs: dict[str, dict[str, Any]] = {}
    for idx, proof_ref in enumerate(accepted):
        if not isinstance(proof_ref, dict):
            raise ExternalValidationLiveProofGateError(f"proofRefGate.acceptedProofRefs[{idx}] must be object")
        _require_fields("proofRefGate.acceptedProofRef", proof_ref, ["id", "workItemId", "owner", "category"])
        proof_refs[str(proof_ref["id"])] = proof_ref
    return proof_refs


def _validate_category_runbooks(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(payload, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = payload.get("runbooks")
    if not isinstance(runbooks, list):
        raise ExternalValidationLiveProofGateError("categoryRunbooks.runbooks must be array")
    by_category: dict[str, dict[str, Any]] = {}
    for idx, runbook in enumerate(runbooks):
        if not isinstance(runbook, dict):
            raise ExternalValidationLiveProofGateError(f"categoryRunbooks.runbooks[{idx}] must be object")
        _require_fields("categoryRunbooks.runbook", runbook, ["id", "category", "closureCondition"])
        by_category[str(runbook["category"])] = runbook
    return by_category


def _validate_command(value: str, *, area: str) -> None:
    if not value.startswith(ALLOWED_COMMAND_PREFIXES):
        raise ExternalValidationLiveProofGateError(f"{area}: verificationCommand must use approved prefix")
    _assert_no_forbidden(value, area=area)


def _validate_source_binding(
    binding: dict[str, Any],
    work_item: dict[str, Any],
    *,
    work_queue_sha256: str,
    proof_ref_gate_sha256: str,
    category_runbooks_sha256: str,
    expected_commit: str,
    area: str,
) -> list[str]:
    _require_fields(
        f"{area}.sourceBinding",
        binding,
        ["commit", "workQueueSha256", "proofRefGateSha256", "categoryRunbooksSha256", "occurrenceIds"],
    )
    if binding["commit"] != expected_commit:
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.commit: mismatch")
    if binding["workQueueSha256"] != work_queue_sha256:
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.workQueueSha256: mismatch")
    if binding["proofRefGateSha256"] != proof_ref_gate_sha256:
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.proofRefGateSha256: mismatch")
    if binding["categoryRunbooksSha256"] != category_runbooks_sha256:
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.categoryRunbooksSha256: mismatch")
    occurrence_ids = binding.get("occurrenceIds")
    if not isinstance(occurrence_ids, list) or not all(isinstance(item, str) and item for item in occurrence_ids):
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.occurrenceIds: string array required")
    known = {str(item.get("id")) for item in work_item["occurrences"]}
    unknown = sorted(set(occurrence_ids) - known)
    if unknown:
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding.occurrenceIds: unknown {unknown}")
    return occurrence_ids


def _validate_bundle_root(
    payload: dict[str, Any],
    *,
    work_queue_sha256: str,
    proof_ref_gate_sha256: str,
    category_runbooks_sha256: str,
    expected_commit: str,
) -> list[dict[str, Any]]:
    _require_kind(payload, expected=LIVE_EVIDENCE_KIND, area="liveEvidence")
    status = payload.get("status")
    if status == PENDING_STATUS:
        return []
    if status != LIVE_SUPPLIED_STATUS:
        raise ExternalValidationLiveProofGateError(f"liveEvidence.status unsupported: {status!r}")
    source = payload.get("source")
    if not isinstance(source, dict):
        raise ExternalValidationLiveProofGateError("liveEvidence.source required")
    _require_fields(
        "liveEvidence.source",
        source,
        [
            "workQueueKind",
            "workQueueSha256",
            "proofRefGateKind",
            "proofRefGateSha256",
            "categoryRunbooksKind",
            "categoryRunbooksSha256",
            "commit",
        ],
    )
    expected_source = {
        "workQueueKind": WORK_QUEUE_KIND,
        "workQueueSha256": work_queue_sha256,
        "proofRefGateKind": PROOF_REF_GATE_KIND,
        "proofRefGateSha256": proof_ref_gate_sha256,
        "categoryRunbooksKind": CATEGORY_RUNBOOKS_KIND,
        "categoryRunbooksSha256": category_runbooks_sha256,
        "commit": expected_commit,
    }
    for key, expected_value in expected_source.items():
        if source[key] != expected_value:
            raise ExternalValidationLiveProofGateError(f"liveEvidence.source.{key}: mismatch")
    if payload.get("privacyBoundary") != REDACTION_BOUNDARY:
        raise ExternalValidationLiveProofGateError(f"liveEvidence.privacyBoundary must be {REDACTION_BOUNDARY}")
    live_proofs = payload.get("liveProofs")
    if not isinstance(live_proofs, list):
        raise ExternalValidationLiveProofGateError("liveEvidence.liveProofs must be array")
    return live_proofs


def _validate_live_proof(
    proof: dict[str, Any],
    *,
    work_items: dict[str, dict[str, Any]],
    accepted_proof_refs: dict[str, dict[str, Any]],
    runbooks_by_category: dict[str, dict[str, Any]],
    work_queue_sha256: str,
    proof_ref_gate_sha256: str,
    category_runbooks_sha256: str,
    expected_commit: str,
    now: datetime,
) -> dict[str, Any]:
    required_fields = [
        "id",
        "proofRefId",
        "workItemId",
        "owner",
        "category",
        "runbookId",
        "liveGateKind",
        "liveGateStatus",
        "issuer",
        "capturedAt",
        "expiresAt",
        "redactionBoundary",
        "verificationCommand",
        "artifactHash",
        "sourceBinding",
        "operatorAttestation",
    ]
    _require_fields("liveProof", proof, required_fields)
    area = f"liveProof {proof['id']}"
    work_item_id = str(proof["workItemId"])
    work_item = work_items.get(work_item_id)
    if work_item is None:
        raise ExternalValidationLiveProofGateError(f"{area}: unknown workItemId")
    proof_ref = accepted_proof_refs.get(str(proof["proofRefId"]))
    if proof_ref is None:
        raise ExternalValidationLiveProofGateError(f"{area}: proofRefId was not schema-accepted")
    if str(proof_ref["workItemId"]) != work_item_id:
        raise ExternalValidationLiveProofGateError(f"{area}: proofRefId workItemId mismatch")
    for field in ("owner", "category"):
        if proof[field] != work_item[field] or proof[field] != proof_ref[field]:
            raise ExternalValidationLiveProofGateError(f"{area}: {field} mismatch")
    runbook = runbooks_by_category.get(str(proof["category"]))
    if runbook is None:
        raise ExternalValidationLiveProofGateError(f"{area}: category runbook missing")
    if proof["runbookId"] != runbook["id"]:
        raise ExternalValidationLiveProofGateError(f"{area}: runbookId mismatch")
    if proof["liveGateStatus"] != "passed":
        raise ExternalValidationLiveProofGateError(f"{area}: liveGateStatus must be passed")
    if proof["redactionBoundary"] != REDACTION_BOUNDARY:
        raise ExternalValidationLiveProofGateError(f"{area}: redactionBoundary must be {REDACTION_BOUNDARY}")
    if proof["operatorAttestation"] != OPERATOR_ATTESTATION:
        raise ExternalValidationLiveProofGateError(f"{area}: operatorAttestation must be {OPERATOR_ATTESTATION}")
    captured_at = _parse_timestamp(str(proof["capturedAt"]), field=f"{area}.capturedAt")
    expires_at = _parse_timestamp(str(proof["expiresAt"]), field=f"{area}.expiresAt")
    if expires_at <= captured_at:
        raise ExternalValidationLiveProofGateError(f"{area}: expiresAt must be after capturedAt")
    if expires_at <= now:
        raise ExternalValidationLiveProofGateError(f"{area}: live proof is expired")
    if not isinstance(proof["artifactHash"], str) or not SHA256_RE.match(proof["artifactHash"]):
        raise ExternalValidationLiveProofGateError(f"{area}: artifactHash must be sha256:<64 hex>")
    _validate_command(str(proof["verificationCommand"]), area=area)
    binding = proof.get("sourceBinding")
    if not isinstance(binding, dict):
        raise ExternalValidationLiveProofGateError(f"{area}.sourceBinding: required")
    occurrence_ids = _validate_source_binding(
        binding,
        work_item,
        work_queue_sha256=work_queue_sha256,
        proof_ref_gate_sha256=proof_ref_gate_sha256,
        category_runbooks_sha256=category_runbooks_sha256,
        expected_commit=expected_commit,
        area=area,
    )
    _assert_no_forbidden(proof, area=area)
    return {
        "id": proof["id"],
        "proofRefId": proof["proofRefId"],
        "workItemId": work_item_id,
        "owner": proof["owner"],
        "category": proof["category"],
        "runbookId": proof["runbookId"],
        "liveGateKind": proof["liveGateKind"],
        "issuer": proof["issuer"],
        "capturedAt": proof["capturedAt"],
        "expiresAt": proof["expiresAt"],
        "artifactHash": proof["artifactHash"],
        "verificationCommandSha256": _sha256_text(str(proof["verificationCommand"])),
        "occurrenceIds": occurrence_ids,
    }


def build_summary(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    live_evidence_json: Path | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    for path in (work_queue_json, proof_ref_gate_json, category_runbooks_json):
        if not path.is_file():
            raise ExternalValidationLiveProofGateError(f"input json missing: {path}")
    contract = _load_json(CONTRACT_PATH)
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationLiveProofGateError("--expected-commit must be 40 lowercase hex chars")

    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    category_runbooks = _load_json(category_runbooks_json)
    work_items = _validate_work_queue(work_queue)
    accepted_proof_refs = _validate_proof_ref_gate(proof_ref_gate)
    runbooks_by_category = _validate_category_runbooks(category_runbooks)
    work_queue_sha256 = _sha256_file(work_queue_json)
    proof_ref_gate_sha256 = _sha256_file(proof_ref_gate_json)
    category_runbooks_sha256 = _sha256_file(category_runbooks_json)

    evidence_status = PENDING_STATUS
    accepted: list[dict[str, Any]] = []
    if live_evidence_json is not None:
        if not live_evidence_json.is_file():
            raise ExternalValidationLiveProofGateError(f"live evidence json missing: {live_evidence_json}")
        live_evidence = _load_json(live_evidence_json)
        _assert_no_forbidden(live_evidence, area="liveEvidence")
        live_proofs = _validate_bundle_root(
            live_evidence,
            work_queue_sha256=work_queue_sha256,
            proof_ref_gate_sha256=proof_ref_gate_sha256,
            category_runbooks_sha256=category_runbooks_sha256,
            expected_commit=expected_commit,
        )
        evidence_status = str(live_evidence["status"])
        now = datetime.now(UTC)
        for proof in live_proofs:
            if not isinstance(proof, dict):
                raise ExternalValidationLiveProofGateError("liveEvidence.liveProofs item must be object")
            accepted.append(
                _validate_live_proof(
                    proof,
                    work_items=work_items,
                    accepted_proof_refs=accepted_proof_refs,
                    runbooks_by_category=runbooks_by_category,
                    work_queue_sha256=work_queue_sha256,
                    proof_ref_gate_sha256=proof_ref_gate_sha256,
                    category_runbooks_sha256=category_runbooks_sha256,
                    expected_commit=expected_commit,
                    now=now,
                )
            )

    accepted_work_ids = {item["workItemId"] for item in accepted}
    pending_work_items = [
        {
            "id": item["id"],
            "owner": item["owner"],
            "category": item["category"],
            "reason": (
                "proof_ref_schema_not_accepted"
                if item["id"] not in {ref["workItemId"] for ref in accepted_proof_refs.values()}
                else "category_live_evidence_missing"
            ),
        }
        for item in work_items.values()
        if item["id"] not in accepted_work_ids
    ]
    if accepted and not pending_work_items:
        live_proof_status = "live_gate_accepted_all_work_items"
    elif accepted:
        live_proof_status = "live_gate_accepted_partial"
    else:
        live_proof_status = PENDING_STATUS

    ship_blocking_items = (
        ["category_live_evidence_missing"]
        if pending_work_items
        else ["third_party_audit_review_pending", "certification_external_claim_review_pending"]
    )
    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": _utc_now(),
        "status": "passed",
        "source": {
            "workQueueJson": str(work_queue_json),
            "workQueueSha256": work_queue_sha256,
            "proofRefGateJson": str(proof_ref_gate_json),
            "proofRefGateSha256": proof_ref_gate_sha256,
            "categoryRunbooksJson": str(category_runbooks_json),
            "categoryRunbooksSha256": category_runbooks_sha256,
            "liveEvidenceJson": str(live_evidence_json) if live_evidence_json else "",
            "expectedCommit": expected_commit,
        },
        "summary": {
            "workItems": len(work_items),
            "proofRefAcceptedWorkItems": len({ref["workItemId"] for ref in accepted_proof_refs.values()}),
            "acceptedLiveProofs": len(accepted),
            "acceptedLiveWorkItems": len(accepted_work_ids),
            "pendingWorkItems": len(pending_work_items),
            "evidenceStatus": evidence_status,
            "liveProofStatus": live_proof_status,
        },
        "liveProofStatus": live_proof_status,
        "liveProofGate": {
            "status": live_proof_status,
            "policy": contract["closurePolicy"]["nonClosure"],
        },
        "shipGate": {
            "status": "blocked",
            "blockingItems": ship_blocking_items,
            "policy": contract["closurePolicy"]["shipGate"],
        },
        "acceptedLiveProofs": accepted,
        "pendingWorkItems": pending_work_items,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary, area="summary")
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate external validation live proof evidence bundle.")
    parser.add_argument(
        "--work-queue-json", type=Path, required=True, help="external-validation-closure-work-queue.json"
    )
    parser.add_argument(
        "--proof-ref-gate-json", type=Path, required=True, help="external-validation-proof-ref-gate.json"
    )
    parser.add_argument(
        "--category-runbooks-json", type=Path, required=True, help="external-validation-category-runbooks.json"
    )
    parser.add_argument("--live-evidence-json", type=Path, help="optional external validation live evidence bundle")
    parser.add_argument("--expected-commit", help="expected current commit hash; defaults to git rev-parse HEAD")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output gate summary JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(
            work_queue_json=args.work_queue_json,
            proof_ref_gate_json=args.proof_ref_gate_json,
            category_runbooks_json=args.category_runbooks_json,
            live_evidence_json=args.live_evidence_json,
            expected_commit=args.expected_commit,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "liveProofStatus": summary["liveProofStatus"],
                    "shipGate": summary["shipGate"]["status"],
                    "acceptedLiveProofs": summary["summary"]["acceptedLiveProofs"],
                    "pendingWorkItems": summary["summary"]["pendingWorkItems"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (
        ExternalValidationLiveProofGateError,
        OSError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"external validation live proof gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
