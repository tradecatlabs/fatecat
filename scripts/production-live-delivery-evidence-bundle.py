#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "production-live-delivery-evidence-bundle.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "production-live-delivery-evidence-bundle.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OUTPUT_KIND = "fatecat.external_validation_live_evidence_bundle"
PENDING_STATUS = "external_connectivity_pending"
LIVE_SUPPLIED_STATUS = "external_live_evidence_supplied_by_operator"
REDACTION_BOUNDARY = "redacted_no_secret_values"
OPERATOR_ATTESTATION = "real_external_execution_redacted"

SENSITIVE_VALUE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


class ProductionLiveDeliveryEvidenceBundleError(RuntimeError):
    """生产交付 live evidence bundle 装配失败。"""


@dataclass(frozen=True)
class CategoryRule:
    category: str
    live_gate_kind: str
    verification_command: str
    evidence_arg_name: str
    live_release_check_id: str | None = None
    expected_kind: str | None = None


CATEGORY_RULES: dict[str, CategoryRule] = {
    "release.production_api_live": CategoryRule(
        category="release.production_api_live",
        live_gate_kind="production_api_live_smoke",
        verification_command="bash scripts/live-release-gate.sh --api-url <redacted> --output-json <live-release-gate-json>",
        evidence_arg_name="liveReleaseGate",
        live_release_check_id="evidence.production_api_live",
    ),
    "release.hf_space_live": CategoryRule(
        category="release.hf_space_live",
        live_gate_kind="hf_space_live_smoke",
        verification_command="bash scripts/live-release-gate.sh --hf-space-url <redacted> --output-json <live-release-gate-json>",
        evidence_arg_name="liveReleaseGate",
        live_release_check_id="evidence.hf_space_live",
    ),
    "release.telegram_bot_live": CategoryRule(
        category="release.telegram_bot_live",
        live_gate_kind="telegram_bot_live_smoke",
        verification_command="bash scripts/live-release-gate.sh --run-live-bot --output-json <live-release-gate-json>",
        evidence_arg_name="liveReleaseGate",
        live_release_check_id="evidence.telegram_bot_live",
    ),
    "runtime.public_webhook_live": CategoryRule(
        category="runtime.public_webhook_live",
        live_gate_kind="public_webhook_live",
        verification_command=("bash scripts/postgres-public-webhook-live-smoke.sh --output-json <public-webhook-json>"),
        evidence_arg_name="publicWebhook",
        expected_kind="fatecat.postgres_public_webhook_live_smoke",
    ),
    "delivery.multi_surface_live": CategoryRule(
        category="delivery.multi_surface_live",
        live_gate_kind="multi_surface_live_parity",
        verification_command=(
            "bash scripts/production-live-delivery-evidence-bundle.sh "
            "--live-release-gate-json <live-release-gate-json> --multi-surface-json <multi-surface-json>"
        ),
        evidence_arg_name="multiSurface",
        expected_kind="fatecat.multi_surface_semantic_diff",
    ),
}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ProductionLiveDeliveryEvidenceBundleError(f"JSON root must be object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", value.lower()).strip("-") or "item"


def _assert_no_inline_secret(payload: Any, *, area: str) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload
    if SENSITIVE_VALUE_RE.search(rendered):
        raise ProductionLiveDeliveryEvidenceBundleError(f"{area}: sensitive-looking inline value detected")


def _assert_no_output_leak(payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    _assert_no_inline_secret(rendered, area="output")
    if re.search(r"https?://", rendered, re.I):
        raise ProductionLiveDeliveryEvidenceBundleError("output: raw URL detected")
    for marker in ("placeholder", "fake", "dummy", "localhost", "dry-run"):
        if marker in rendered.lower():
            raise ProductionLiveDeliveryEvidenceBundleError(f"output: forbidden marker detected: {marker}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ProductionLiveDeliveryEvidenceBundleError(f"{area}.kind must be {expected}")


def _require_fields(area: str, payload: dict[str, Any], fields: tuple[str, ...]) -> None:
    missing = [field for field in fields if payload.get(field) in ("", None, [])]
    if missing:
        raise ProductionLiveDeliveryEvidenceBundleError(f"{area}: missing fields {missing}")


def _load_optional(path: Path | None, *, area: str) -> tuple[dict[str, Any] | None, str]:
    if path is None:
        return None, ""
    if not path.is_file():
        raise ProductionLiveDeliveryEvidenceBundleError(f"{area}: evidence json missing: {path}")
    payload = _load_json(path)
    _assert_no_inline_secret(payload, area=area)
    return payload, _sha256_file(path)


def _work_items_by_id(work_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(work_queue, expected=WORK_QUEUE_KIND, area="workQueue")
    items = work_queue.get("workItems")
    if not isinstance(items, list):
        raise ProductionLiveDeliveryEvidenceBundleError("workQueue.workItems must be array")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise ProductionLiveDeliveryEvidenceBundleError("workQueue.workItems item must be object")
        _require_fields("workQueue.workItem", item, ("id", "owner", "category", "occurrences"))
        result[str(item["id"])] = item
    return result


def _proof_refs_by_work_item(proof_ref_gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(proof_ref_gate, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    refs = proof_ref_gate.get("acceptedProofRefs")
    if not isinstance(refs, list):
        raise ProductionLiveDeliveryEvidenceBundleError("proofRefGate.acceptedProofRefs must be array")
    result: dict[str, dict[str, Any]] = {}
    for ref in refs:
        if not isinstance(ref, dict):
            raise ProductionLiveDeliveryEvidenceBundleError("proofRefGate.acceptedProofRefs item must be object")
        _require_fields("proofRef", ref, ("id", "workItemId", "owner", "category"))
        result[str(ref["workItemId"])] = ref
    return result


def _runbooks_by_category(category_runbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(category_runbooks, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = category_runbooks.get("runbooks")
    if not isinstance(runbooks, list):
        raise ProductionLiveDeliveryEvidenceBundleError("categoryRunbooks.runbooks must be array")
    result: dict[str, dict[str, Any]] = {}
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            raise ProductionLiveDeliveryEvidenceBundleError("categoryRunbooks.runbooks item must be object")
        _require_fields("runbook", runbook, ("id", "category"))
        result[str(runbook["category"])] = runbook
    return result


def _live_release_check_passed(payload: dict[str, Any] | None, check_id: str) -> bool:
    if payload is None or payload.get("status") != "passed":
        return False
    checks = payload.get("checks")
    if not isinstance(checks, list):
        return False
    for check in checks:
        if isinstance(check, dict) and check.get("id") == check_id:
            return check.get("status") == "pass"
    return False


def _public_webhook_passed(payload: dict[str, Any] | None) -> bool:
    if payload is None:
        return False
    if payload.get("kind") != "fatecat.postgres_public_webhook_live_smoke":
        return False
    live_evidence = payload.get("liveEvidence") if isinstance(payload.get("liveEvidence"), dict) else {}
    return payload.get("status") == "passed" and live_evidence.get("publicWebhookLiveDelivery") is True


def _multi_surface_passed(
    multi_surface: dict[str, Any] | None,
    live_release_gate: dict[str, Any] | None,
) -> bool:
    if multi_surface is None:
        return False
    if multi_surface.get("kind") != "fatecat.multi_surface_semantic_diff" or multi_surface.get("status") != "passed":
        return False
    required = ("evidence.production_api_live", "evidence.hf_space_live", "evidence.telegram_bot_live")
    return all(_live_release_check_passed(live_release_gate, check_id) for check_id in required)


def _category_passed(
    category: str,
    *,
    live_release_gate: dict[str, Any] | None,
    public_webhook: dict[str, Any] | None,
    multi_surface: dict[str, Any] | None,
) -> bool:
    rule = CATEGORY_RULES[category]
    if rule.live_release_check_id:
        return _live_release_check_passed(live_release_gate, rule.live_release_check_id)
    if category == "runtime.public_webhook_live":
        return _public_webhook_passed(public_webhook)
    if category == "delivery.multi_surface_live":
        return _multi_surface_passed(multi_surface, live_release_gate)
    return False


def _artifact_hash_for_category(
    category: str,
    *,
    live_release_gate_sha256: str,
    public_hook_digest: str,
    multi_surface_sha256: str,
) -> str:
    if category in {"release.production_api_live", "release.hf_space_live", "release.telegram_bot_live"}:
        return "sha256:" + live_release_gate_sha256
    if category == "runtime.public_webhook_live":
        return "sha256:" + public_hook_digest
    if category == "delivery.multi_surface_live":
        combined = f"{live_release_gate_sha256}:{multi_surface_sha256}"
        return "sha256:" + hashlib.sha256(combined.encode("utf-8")).hexdigest()
    raise ProductionLiveDeliveryEvidenceBundleError(f"unsupported category: {category}")


def _occurrence_ids(work_item: dict[str, Any], proof_ref: dict[str, Any]) -> list[str]:
    from_ref = proof_ref.get("occurrenceIds")
    if isinstance(from_ref, list) and all(isinstance(item, str) and item for item in from_ref):
        return list(from_ref)
    occurrences = work_item.get("occurrences")
    if not isinstance(occurrences, list) or not occurrences:
        raise ProductionLiveDeliveryEvidenceBundleError(f"work item {work_item['id']}: occurrences required")
    return [str(item["id"]) for item in occurrences if isinstance(item, dict) and item.get("id")]


def build_bundle(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    live_release_gate_json: Path | None = None,
    public_hook_json: Path | None = None,
    multi_surface_json: Path | None = None,
    expected_commit: str | None = None,
    issuer: str = "operator:delivery-ops",
    expires_in_days: int = 14,
) -> dict[str, Any]:
    for path in (work_queue_json, proof_ref_gate_json, category_runbooks_json):
        if not path.is_file():
            raise ProductionLiveDeliveryEvidenceBundleError(f"input json missing: {path}")

    contract = _load_json(CONTRACT_PATH)
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ProductionLiveDeliveryEvidenceBundleError("--expected-commit must be 40 lowercase hex chars")
    if expires_in_days < 1 or expires_in_days > 90:
        raise ProductionLiveDeliveryEvidenceBundleError("--expires-in-days must be between 1 and 90")

    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    category_runbooks = _load_json(category_runbooks_json)
    work_items = _work_items_by_id(work_queue)
    proof_refs = _proof_refs_by_work_item(proof_ref_gate)
    runbooks = _runbooks_by_category(category_runbooks)

    work_queue_sha256 = _sha256_file(work_queue_json)
    proof_ref_gate_sha256 = _sha256_file(proof_ref_gate_json)
    category_runbooks_sha256 = _sha256_file(category_runbooks_json)

    live_release_gate, live_release_gate_sha256 = _load_optional(live_release_gate_json, area="liveReleaseGate")
    public_hook_payload, public_hook_digest = _load_optional(public_hook_json, area="publicWebhook")
    multi_surface, multi_surface_sha256 = _load_optional(multi_surface_json, area="multiSurface")

    captured_at = _utc_now()
    expires_at = (
        (datetime.now(UTC) + timedelta(days=expires_in_days)).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    live_proofs: list[dict[str, Any]] = []
    pending: list[dict[str, str]] = []

    for work_item in work_items.values():
        category = str(work_item["category"])
        if category not in CATEGORY_RULES:
            continue
        proof_ref = proof_refs.get(str(work_item["id"]))
        if proof_ref is None:
            pending.append({"workItemId": str(work_item["id"]), "category": category, "reason": "proof_ref_missing"})
            continue
        runbook = runbooks.get(category)
        if runbook is None:
            pending.append({"workItemId": str(work_item["id"]), "category": category, "reason": "runbook_missing"})
            continue
        if not _category_passed(
            category,
            live_release_gate=live_release_gate,
            public_webhook=public_hook_payload,
            multi_surface=multi_surface,
        ):
            pending.append(
                {
                    "workItemId": str(work_item["id"]),
                    "category": category,
                    "reason": "delivery_live_evidence_missing_or_not_passed",
                }
            )
            continue
        rule = CATEGORY_RULES[category]
        occurrence_ids = _occurrence_ids(work_item, proof_ref)
        live_proofs.append(
            {
                "id": f"delivery-live-proof.{_safe_id(str(work_item['id']))}",
                "proofRefId": proof_ref["id"],
                "workItemId": work_item["id"],
                "owner": work_item["owner"],
                "category": category,
                "runbookId": runbook["id"],
                "liveGateKind": rule.live_gate_kind,
                "liveGateStatus": "passed",
                "issuer": issuer,
                "capturedAt": captured_at,
                "expiresAt": expires_at,
                "redactionBoundary": REDACTION_BOUNDARY,
                "verificationCommand": rule.verification_command,
                "artifactHash": _artifact_hash_for_category(
                    category,
                    live_release_gate_sha256=live_release_gate_sha256,
                    public_hook_digest=public_hook_digest,
                    multi_surface_sha256=multi_surface_sha256,
                ),
                "sourceBinding": {
                    "commit": expected_commit,
                    "workQueueSha256": work_queue_sha256,
                    "proofRefGateSha256": proof_ref_gate_sha256,
                    "categoryRunbooksSha256": category_runbooks_sha256,
                    "occurrenceIds": occurrence_ids,
                },
                "operatorAttestation": OPERATOR_ATTESTATION,
            }
        )

    status = LIVE_SUPPLIED_STATUS if live_proofs else PENDING_STATUS
    bundle = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": status,
        "generatedAt": captured_at,
        "source": {
            "workQueueKind": WORK_QUEUE_KIND,
            "workQueueSha256": work_queue_sha256,
            "proofRefGateKind": PROOF_REF_GATE_KIND,
            "proofRefGateSha256": proof_ref_gate_sha256,
            "categoryRunbooksKind": CATEGORY_RUNBOOKS_KIND,
            "categoryRunbooksSha256": category_runbooks_sha256,
            "commit": expected_commit,
        },
        "liveProofs": live_proofs,
        "privacyBoundary": REDACTION_BOUNDARY,
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_output_leak(bundle)
    return bundle


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble redacted production delivery live evidence bundle.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--proof-ref-gate-json", type=Path, required=True)
    parser.add_argument("--category-runbooks-json", type=Path, required=True)
    parser.add_argument("--live-release-gate-json", type=Path)
    parser.add_argument("--public-webhook-json", dest="public_hook_json", type=Path)
    parser.add_argument("--multi-surface-json", type=Path)
    parser.add_argument("--expected-commit")
    parser.add_argument("--issuer", default="operator:delivery-ops")
    parser.add_argument("--expires-in-days", type=int, default=14)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle = build_bundle(
        work_queue_json=args.work_queue_json,
        proof_ref_gate_json=args.proof_ref_gate_json,
        category_runbooks_json=args.category_runbooks_json,
        live_release_gate_json=args.live_release_gate_json,
        public_hook_json=args.public_hook_json,
        multi_surface_json=args.multi_surface_json,
        expected_commit=args.expected_commit,
        issuer=args.issuer,
        expires_in_days=args.expires_in_days,
    )
    output_json = args.output_json
    if not output_json.is_absolute():
        output_json = ROOT / output_json
    _write_json(output_json, bundle)
    print(
        json.dumps(
            {
                "status": bundle["status"],
                "kind": bundle["kind"],
                "liveProofs": len(bundle["liveProofs"]),
                "outputJson": str(output_json),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
