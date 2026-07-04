#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-proof-ref.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-proof-ref-gate.json"
)

PENDING_STATUS = "external_connectivity_pending"
LIVE_SUPPLIED_STATUS = "external_live_evidence_supplied_by_operator"
PROOF_REF_PREFIXES = ("evidence://", "artifact://", "ci-artifact://")
REDACTION_BOUNDARY = "redacted_no_secret_values"

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

FORBIDDEN_PROOF_FRAGMENTS = {
    "changeme",
    "debug",
    "dry-run",
    "dummy",
    "fake",
    "localhost",
    "local only",
    "placeholder",
    "sample",
}

ALLOWED_COMMAND_PREFIXES = ("bash scripts/", "python3 scripts/", "gh run view ")
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


class ProofRefGateError(RuntimeError):
    """外部验证 proof-ref gate 失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ProofRefGateError(f"JSON root must be object: {path}")
    return payload


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ProofRefGateError(f"{field}: timestamp required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProofRefGateError(f"{field}: must be ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ProofRefGateError(f"{field}: timezone required")
    return parsed.astimezone(UTC)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_json(payload: dict[str, Any]) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


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


def _assert_no_sensitive_fragments(payload: Any, *, area: str) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if re.search(r"https?://", rendered, re.I):
        bad.append("raw_url")
    if bad:
        raise ProofRefGateError(f"{area}: sensitive or raw fragment detected: {', '.join(bad)}")


def _require_fields(area: str, payload: dict[str, Any], fields: list[str]) -> None:
    missing = [field for field in fields if field not in payload or payload[field] in ("", None, [])]
    if missing:
        raise ProofRefGateError(f"{area}: missing fields {missing}")


def _replace_placeholders(value: Any, *, work_queue_sha256: str, expected_commit: str) -> Any:
    if isinstance(value, dict):
        return {
            key: _replace_placeholders(item, work_queue_sha256=work_queue_sha256, expected_commit=expected_commit)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [
            _replace_placeholders(item, work_queue_sha256=work_queue_sha256, expected_commit=expected_commit)
            for item in value
        ]
    if value == "__WORK_QUEUE_SHA256__":
        return work_queue_sha256
    if value == "__EXPECTED_COMMIT__":
        return expected_commit
    return value


def _validate_work_queue(work_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if work_queue.get("kind") != "fatecat.external_validation_closure_work_queue":
        raise ProofRefGateError("workQueue: kind must be fatecat.external_validation_closure_work_queue")
    work_items = work_queue.get("workItems")
    if not isinstance(work_items, list):
        raise ProofRefGateError("workQueue: workItems must be array")
    index: dict[str, dict[str, Any]] = {}
    for item in work_items:
        if not isinstance(item, dict):
            raise ProofRefGateError("workQueue: work item must be object")
        _require_fields("workQueue.item", item, ["id", "owner", "category", "status", "occurrences"])
        occurrences = item.get("occurrences")
        if not isinstance(occurrences, list) or not occurrences:
            raise ProofRefGateError(f"workQueue.item {item['id']}: occurrences required")
        index[str(item["id"])] = item
    return index


def _validate_bundle_root(
    bundle: dict[str, Any],
    *,
    work_queue_sha256: str,
    expected_commit: str,
) -> list[dict[str, Any]]:
    if bundle.get("kind") != "fatecat.external_validation_proof_ref_bundle":
        raise ProofRefGateError("evidence: kind must be fatecat.external_validation_proof_ref_bundle")
    status = bundle.get("status")
    if status == PENDING_STATUS:
        return []
    if status != LIVE_SUPPLIED_STATUS:
        raise ProofRefGateError(f"evidence: unsupported status {status!r}")
    source = bundle.get("source")
    if not isinstance(source, dict):
        raise ProofRefGateError("evidence.source: required")
    _require_fields("evidence.source", source, ["workQueueKind", "workQueueSha256", "commit"])
    if source["workQueueKind"] != "fatecat.external_validation_closure_work_queue":
        raise ProofRefGateError("evidence.source.workQueueKind: mismatch")
    if source["workQueueSha256"] != work_queue_sha256:
        raise ProofRefGateError("evidence.source.workQueueSha256: mismatch")
    if source["commit"] != expected_commit:
        raise ProofRefGateError("evidence.source.commit: mismatch")
    if bundle.get("privacyBoundary") != REDACTION_BOUNDARY:
        raise ProofRefGateError("evidence.privacyBoundary: redacted_no_secret_values required")
    proof_refs = bundle.get("proofRefs")
    if not isinstance(proof_refs, list):
        raise ProofRefGateError("evidence.proofRefs: array required")
    return proof_refs


def _validate_proof_ref_value(value: str, *, area: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProofRefGateError(f"{area}: proofRef required")
    if not value.startswith(PROOF_REF_PREFIXES):
        raise ProofRefGateError(f"{area}: proofRef must use redacted proof ref prefix")
    lowered = value.lower()
    bad = sorted(fragment for fragment in FORBIDDEN_PROOF_FRAGMENTS if fragment in lowered)
    if bad:
        raise ProofRefGateError(f"{area}: forbidden proof fragment: {', '.join(bad)}")
    _assert_no_sensitive_fragments(value, area=area)


def _validate_verification_command(value: str, *, area: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProofRefGateError(f"{area}: verificationCommand required")
    if not value.startswith(ALLOWED_COMMAND_PREFIXES):
        raise ProofRefGateError(f"{area}: verificationCommand must use approved command prefix")
    _assert_no_sensitive_fragments(value, area=area)


def _validate_artifact_hash(value: str, *, area: str) -> None:
    if not isinstance(value, str) or not SHA256_RE.match(value):
        raise ProofRefGateError(f"{area}: artifactHash must be sha256:<64 hex>")


def _validate_source_binding(
    proof: dict[str, Any],
    work_item: dict[str, Any],
    *,
    work_queue_sha256: str,
    expected_commit: str,
    area: str,
) -> None:
    source_binding = proof.get("sourceBinding")
    if not isinstance(source_binding, dict):
        raise ProofRefGateError(f"{area}.sourceBinding: required")
    _require_fields(f"{area}.sourceBinding", source_binding, ["commit", "workQueueSha256", "occurrenceIds"])
    if source_binding["commit"] != expected_commit:
        raise ProofRefGateError(f"{area}.sourceBinding.commit: mismatch")
    if source_binding["workQueueSha256"] != work_queue_sha256:
        raise ProofRefGateError(f"{area}.sourceBinding.workQueueSha256: mismatch")
    occurrence_ids = source_binding.get("occurrenceIds")
    if not isinstance(occurrence_ids, list) or not all(isinstance(item, str) and item for item in occurrence_ids):
        raise ProofRefGateError(f"{area}.sourceBinding.occurrenceIds: non-empty string array required")
    known_occurrences = {str(item.get("id")) for item in work_item["occurrences"]}
    unknown = sorted(set(occurrence_ids) - known_occurrences)
    if unknown:
        raise ProofRefGateError(f"{area}.sourceBinding.occurrenceIds: unknown {unknown}")


def validate_proof_ref(
    proof: dict[str, Any],
    *,
    work_items: dict[str, dict[str, Any]],
    work_queue_sha256: str,
    expected_commit: str,
    now: datetime,
) -> dict[str, Any]:
    if not isinstance(proof, dict):
        raise ProofRefGateError("proofRef: item must be object")
    required_fields = [
        "id",
        "proofRef",
        "evidenceType",
        "workItemId",
        "owner",
        "category",
        "issuer",
        "capturedAt",
        "expiresAt",
        "redactionBoundary",
        "verificationCommand",
        "artifactHash",
        "sourceBinding",
    ]
    _require_fields("proofRef", proof, required_fields)
    area = f"proofRef {proof['id']}"
    work_item_id = str(proof["workItemId"])
    work_item = work_items.get(work_item_id)
    if work_item is None:
        raise ProofRefGateError(f"{area}: unknown workItemId")
    if proof["owner"] != work_item["owner"]:
        raise ProofRefGateError(f"{area}: owner mismatch")
    if proof["category"] != work_item["category"]:
        raise ProofRefGateError(f"{area}: category mismatch")
    if proof["redactionBoundary"] != REDACTION_BOUNDARY:
        raise ProofRefGateError(f"{area}: redactionBoundary must be {REDACTION_BOUNDARY}")
    captured_at = _parse_timestamp(str(proof["capturedAt"]), f"{area}.capturedAt")
    expires_at = _parse_timestamp(str(proof["expiresAt"]), f"{area}.expiresAt")
    if expires_at <= captured_at:
        raise ProofRefGateError(f"{area}: expiresAt must be after capturedAt")
    if expires_at <= now:
        raise ProofRefGateError(f"{area}: proofRef is expired")
    _validate_proof_ref_value(str(proof["proofRef"]), area=area)
    _validate_verification_command(str(proof["verificationCommand"]), area=area)
    _validate_artifact_hash(str(proof["artifactHash"]), area=area)
    _validate_source_binding(
        proof,
        work_item,
        work_queue_sha256=work_queue_sha256,
        expected_commit=expected_commit,
        area=area,
    )
    _assert_no_sensitive_fragments(proof, area=area)
    return {
        "id": proof["id"],
        "proofRef": proof["proofRef"],
        "evidenceType": proof["evidenceType"],
        "workItemId": work_item_id,
        "owner": proof["owner"],
        "category": proof["category"],
        "issuer": proof["issuer"],
        "capturedAt": proof["capturedAt"],
        "expiresAt": proof["expiresAt"],
        "artifactHash": proof["artifactHash"],
        "verificationCommandSha256": _sha256_text(str(proof["verificationCommand"])),
        "occurrenceIds": list(proof["sourceBinding"]["occurrenceIds"]),
    }


def _validate_negative_cases(contract: dict[str, Any], *, expected_commit: str) -> list[str]:
    fixture_queue = copy.deepcopy(contract["negativeEvidenceWorkQueueFixture"])
    fixture_sha = _sha256_json(fixture_queue)
    work_items = _validate_work_queue(fixture_queue)
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        evidence = _replace_placeholders(
            copy.deepcopy(case["evidence"]),
            work_queue_sha256=fixture_sha,
            expected_commit=expected_commit,
        )
        try:
            proof_refs = _validate_bundle_root(
                evidence,
                work_queue_sha256=fixture_sha,
                expected_commit=expected_commit,
            )
            for proof in proof_refs:
                validate_proof_ref(
                    proof,
                    work_items=work_items,
                    work_queue_sha256=fixture_sha,
                    expected_commit=expected_commit,
                    now=datetime.now(UTC),
                )
        except ProofRefGateError as exc:
            if case["expectedErrorContains"] not in str(exc):
                raise ProofRefGateError(f"negative:{case['id']}: unexpected rejection: {exc}") from exc
            rejected.append(case["id"])
        else:
            raise ProofRefGateError(f"negative:{case['id']}: fake evidence was accepted")
    return rejected


def _validate_contract(contract: dict[str, Any], *, expected_commit: str) -> list[str]:
    if contract.get("kind") != "fatecat.external_validation_proof_ref_contract":
        raise ProofRefGateError("contract.kind mismatch")
    if "proofRef" not in contract.get("requiredFieldsPerProofRef", []):
        raise ProofRefGateError("contract.requiredFieldsPerProofRef missing proofRef")
    if set(PROOF_REF_PREFIXES) - set(contract.get("allowedProofRefPrefixes", [])):
        raise ProofRefGateError("contract.allowedProofRefPrefixes incomplete")
    if contract.get("requiredRedactionBoundary") != REDACTION_BOUNDARY:
        raise ProofRefGateError("contract.requiredRedactionBoundary mismatch")
    _assert_no_sensitive_fragments(contract, area="contract")
    return _validate_negative_cases(contract, expected_commit=expected_commit)


def build_summary(
    *,
    work_queue_json: Path,
    evidence_json: Path | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ProofRefGateError("--expected-commit must be 40 lowercase hex chars")
    if not work_queue_json.is_file():
        raise ProofRefGateError(f"work queue json missing: {work_queue_json}")
    work_queue = _load_json(work_queue_json)
    work_items = _validate_work_queue(work_queue)
    work_queue_sha256 = _sha256_file(work_queue_json)
    negative_cases = _validate_contract(contract, expected_commit=expected_commit)
    accepted: list[dict[str, Any]] = []
    evidence_status = PENDING_STATUS
    now = datetime.now(UTC)

    if evidence_json is not None:
        if not evidence_json.is_file():
            raise ProofRefGateError(f"evidence json missing: {evidence_json}")
        evidence = _load_json(evidence_json)
        _assert_no_sensitive_fragments(evidence, area="evidence")
        proof_refs = _validate_bundle_root(
            evidence,
            work_queue_sha256=work_queue_sha256,
            expected_commit=expected_commit,
        )
        evidence_status = str(evidence["status"])
        for proof in proof_refs:
            accepted.append(
                validate_proof_ref(
                    proof,
                    work_items=work_items,
                    work_queue_sha256=work_queue_sha256,
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
            "staleReason": "proof_ref_missing" if item["id"] not in accepted_work_ids else "proof_ref_schema_accepted",
        }
        for item in work_queue["workItems"]
        if item["id"] not in accepted_work_ids
    ]
    proof_ref_status = "external_connectivity_pending"
    if accepted and not pending_work_items:
        proof_ref_status = "schema_accepted_all_work_items"
    elif accepted:
        proof_ref_status = "schema_accepted_partial"

    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_gate_summary",
        "generatedAt": _utc_now(),
        "status": "passed",
        "source": {
            "workQueueJson": str(work_queue_json),
            "workQueueSha256": work_queue_sha256,
            "workQueueKind": work_queue.get("kind"),
            "evidenceJson": str(evidence_json) if evidence_json is not None else "",
            "expectedCommit": expected_commit,
        },
        "summary": {
            "workItems": len(work_items),
            "acceptedProofRefs": len(accepted),
            "acceptedWorkItems": len(accepted_work_ids),
            "pendingWorkItems": len(pending_work_items),
            "evidenceStatus": evidence_status,
            "proofRefStatus": proof_ref_status,
        },
        "proofRefStatus": proof_ref_status,
        "proofRefGate": {
            "status": proof_ref_status,
            "policy": "Proof-ref schema acceptance does not replace category-specific live gates or third-party audit.",
        },
        "shipGate": {
            "status": "blocked",
            "blockingItems": (
                ["proof_ref_missing"]
                if pending_work_items
                else ["category_live_gates_pending", "third_party_audit_review_pending"]
            ),
            "reason": (
                "proof refs are missing for some work items"
                if pending_work_items
                else "proof refs are structurally accepted but still require category live gates and audit review"
            ),
        },
        "acceptedProofRefs": accepted,
        "pendingWorkItems": pending_work_items,
        "negativeEvidenceRejected": negative_cases,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive_fragments(summary, area="summary")
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate external validation proof-ref evidence upload contract.")
    parser.add_argument(
        "--work-queue-json", type=Path, required=True, help="external-validation-closure-work-queue.json"
    )
    parser.add_argument("--evidence-json", type=Path, help="optional proof-ref evidence bundle")
    parser.add_argument("--expected-commit", help="expected current commit hash; defaults to git rev-parse HEAD")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output gate summary JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(
            work_queue_json=args.work_queue_json,
            evidence_json=args.evidence_json,
            expected_commit=args.expected_commit,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "proofRefStatus": summary["summary"]["proofRefStatus"],
                    "shipGate": summary["shipGate"]["status"],
                    "acceptedProofRefs": summary["summary"]["acceptedProofRefs"],
                    "pendingWorkItems": summary["summary"]["pendingWorkItems"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ProofRefGateError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"external validation proof-ref gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
