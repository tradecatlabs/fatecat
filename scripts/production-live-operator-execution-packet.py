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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "production-live-operator-execution-packet.json"
LIVE_PROOF_GATE_CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-live-proof-gate.json"
DELIVERY_BUNDLE_CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "production-live-delivery-evidence-bundle.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "production-live-operator-execution-packet.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OUTPUT_KIND = "fatecat.production_live_operator_execution_packet"
OUTPUT_STATUS = "operator_action_required"
PRIVACY_BOUNDARY = "redacted_no_secret_values"

LIVE_CATEGORIES = (
    "release.production_api_live",
    "release.hf_space_live",
    "release.telegram_bot_live",
    "runtime.public_webhook_live",
    "delivery.multi_surface_live",
)

CATEGORY_EXECUTION: dict[str, dict[str, Any]] = {
    "release.production_api_live": {
        "phase": "production_api_and_hf_live_release_gate",
        "requiredEnvVars": ("FATE_PRODUCTION_API_URL", "FATE_API_TOKEN", "FATE_CORS_ALLOW_ORIGINS"),
        "command": (
            "bash scripts/live-release-gate.sh --require-live --api-url ${FATE_PRODUCTION_API_URL} "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json"
        ),
        "outputArtifact": "${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json",
        "proofRefHandleTemplate": "evidence://external-validation/release-production-api-live/<run-id>",
        "evidenceType": "production_api_live_smoke",
    },
    "release.hf_space_live": {
        "phase": "production_api_and_hf_live_release_gate",
        "requiredEnvVars": ("FATE_HF_SPACE_URL",),
        "command": (
            "bash scripts/live-release-gate.sh --require-live --hf-space-url ${FATE_HF_SPACE_URL} "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json"
        ),
        "outputArtifact": "${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json",
        "proofRefHandleTemplate": "evidence://external-validation/release-hf-space-live/<run-id>",
        "evidenceType": "hf_space_live_smoke",
    },
    "release.telegram_bot_live": {
        "phase": "telegram_bot_live_release_gate",
        "requiredEnvVars": ("FATE_BOT_TOKEN",),
        "command": (
            "bash scripts/live-release-gate.sh --run-live-bot "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json"
        ),
        "outputArtifact": "${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json",
        "proofRefHandleTemplate": "evidence://external-validation/release-telegram-bot-live/<run-id>",
        "evidenceType": "telegram_bot_live_smoke",
    },
    "runtime.public_webhook_live": {
        "phase": "public_webhook_live_smoke",
        "requiredEnvVars": (
            "FATE_REPORT_JOB_DATABASE_URL",
            "FATE_WEBHOOK_LIVE_URL",
            "FATE_WEBHOOK_LIVE_SECRET",
            "FATE_WEBHOOK_ALLOWED_HOSTS",
        ),
        "command": (
            "bash scripts/postgres-public-webhook-live-smoke.sh "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/postgres-public-webhook-live-smoke.json"
        ),
        "outputArtifact": "${FATE_OPERATOR_OUTPUT_DIR}/postgres-public-webhook-live-smoke.json",
        "proofRefHandleTemplate": "evidence://external-validation/runtime-public-webhook-live/<run-id>",
        "evidenceType": "public_webhook_live",
    },
    "delivery.multi_surface_live": {
        "phase": "multi_surface_live_parity",
        "requiredEnvVars": ("FATE_OPERATOR_OUTPUT_DIR",),
        "command": (
            "bash scripts/multi-surface-semantic-diff.sh "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/multi-surface-semantic-diff.json"
        ),
        "outputArtifact": "${FATE_OPERATOR_OUTPUT_DIR}/multi-surface-semantic-diff.json",
        "proofRefHandleTemplate": "evidence://external-validation/delivery-multi-surface-live/<run-id>",
        "evidenceType": "multi_surface_live_parity",
    },
}

FINAL_GATE_COMMANDS = (
    {
        "id": "proof-ref-gate",
        "command": (
            "bash scripts/external-validation-proof-ref-gate.sh "
            "--work-queue-json <external-validation-closure-work-queue.json> "
            "--evidence-json ${FATE_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-bundle.json "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json"
        ),
        "produces": "${FATE_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json",
    },
    {
        "id": "production-live-delivery-evidence-bundle",
        "command": (
            "bash scripts/production-live-delivery-evidence-bundle.sh "
            "--work-queue-json <external-validation-closure-work-queue.json> "
            "--proof-ref-gate-json ${FATE_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json "
            "--category-runbooks-json <external-validation-category-runbooks.json> "
            "--live-release-gate-json ${FATE_OPERATOR_OUTPUT_DIR}/live-release-gate.json "
            "--public-webhook-json ${FATE_OPERATOR_OUTPUT_DIR}/postgres-public-webhook-live-smoke.json "
            "--multi-surface-json ${FATE_OPERATOR_OUTPUT_DIR}/multi-surface-semantic-diff.json "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/production-live-delivery-evidence-bundle.json"
        ),
        "produces": "${FATE_OPERATOR_OUTPUT_DIR}/production-live-delivery-evidence-bundle.json",
    },
    {
        "id": "external-validation-live-proof-gate",
        "command": (
            "bash scripts/external-validation-live-proof-gate.sh "
            "--work-queue-json <external-validation-closure-work-queue.json> "
            "--proof-ref-gate-json ${FATE_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json "
            "--category-runbooks-json <external-validation-category-runbooks.json> "
            "--live-evidence-json ${FATE_OPERATOR_OUTPUT_DIR}/production-live-delivery-evidence-bundle.json "
            "--output-json ${FATE_OPERATOR_OUTPUT_DIR}/external-validation-live-proof-gate.json"
        ),
        "produces": "${FATE_OPERATOR_OUTPUT_DIR}/external-validation-live-proof-gate.json",
    },
)

SENSITIVE_VALUE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


class ProductionLiveOperatorExecutionPacketError(RuntimeError):
    """生产 live operator execution packet 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ProductionLiveOperatorExecutionPacketError(f"JSON root must be object: {path}")
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


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload


def _assert_no_sensitive_assignment(payload: Any, *, area: str) -> None:
    rendered = _render(payload)
    if SENSITIVE_VALUE_RE.search(rendered):
        raise ProductionLiveOperatorExecutionPacketError(f"{area}: sensitive-looking assignment detected")


def _assert_output_safe(payload: dict[str, Any]) -> None:
    rendered = _render(payload)
    _assert_no_sensitive_assignment(rendered, area="output")
    if RAW_URL_RE.search(rendered):
        raise ProductionLiveOperatorExecutionPacketError("output: raw URL detected")
    for marker in ("placeholder proof", "fake proof", "dummy proof", "localhost proof"):
        if marker in rendered.lower():
            raise ProductionLiveOperatorExecutionPacketError(f"output: forbidden marker detected: {marker}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ProductionLiveOperatorExecutionPacketError(f"{area}.kind must be {expected}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.production_live_operator_execution_packet_contract":
        raise ProductionLiveOperatorExecutionPacketError("contract.kind mismatch")
    missing = sorted(set(LIVE_CATEGORIES) - set(contract.get("supportedCategories", [])))
    if missing:
        raise ProductionLiveOperatorExecutionPacketError(f"contract missing supported categories: {missing}")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("operatorSteps", "proofRefBundleTemplate", "finalGateCommands"):
        if field not in required:
            raise ProductionLiveOperatorExecutionPacketError(f"contract missing required output field: {field}")


def _work_items_by_id(work_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(work_queue, expected=WORK_QUEUE_KIND, area="workQueue")
    items = work_queue.get("workItems")
    if not isinstance(items, list):
        raise ProductionLiveOperatorExecutionPacketError("workQueue.workItems must be array")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise ProductionLiveOperatorExecutionPacketError("workQueue.workItems item must be object")
        for field in ("id", "owner", "category", "occurrences"):
            if item.get(field) in ("", None, []):
                raise ProductionLiveOperatorExecutionPacketError(f"work item missing {field}")
        result[str(item["id"])] = item
    return result


def _runbooks_by_category(category_runbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(category_runbooks, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = category_runbooks.get("runbooks")
    if not isinstance(runbooks, list):
        raise ProductionLiveOperatorExecutionPacketError("categoryRunbooks.runbooks must be array")
    result: dict[str, dict[str, Any]] = {}
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            raise ProductionLiveOperatorExecutionPacketError("categoryRunbooks.runbooks item must be object")
        if runbook.get("id") in ("", None) or runbook.get("category") in ("", None):
            raise ProductionLiveOperatorExecutionPacketError("runbook missing id/category")
        result[str(runbook["category"])] = runbook
    return result


def _validate_proof_ref_gate(proof_ref_gate: dict[str, Any]) -> None:
    _require_kind(proof_ref_gate, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    if "proofRefStatus" not in proof_ref_gate:
        raise ProductionLiveOperatorExecutionPacketError("proofRefGate.proofRefStatus missing")


def _occurrence_ids(work_item: dict[str, Any]) -> list[str]:
    occurrences = work_item.get("occurrences")
    if not isinstance(occurrences, list) or not occurrences:
        raise ProductionLiveOperatorExecutionPacketError(f"work item {work_item['id']}: occurrences required")
    result = [str(item["id"]) for item in occurrences if isinstance(item, dict) and item.get("id")]
    if not result:
        raise ProductionLiveOperatorExecutionPacketError(f"work item {work_item['id']}: occurrence ids required")
    return result


def _build_operator_step(order: int, *, work_item: dict[str, Any], runbook: dict[str, Any]) -> dict[str, Any]:
    category = str(work_item["category"])
    spec = CATEGORY_EXECUTION[category]
    step = {
        "order": order,
        "id": f"operator-step.{order:02d}.{_safe_id(category)}",
        "phase": spec["phase"],
        "workItemId": work_item["id"],
        "owner": work_item["owner"],
        "category": category,
        "runbookId": runbook["id"],
        "requiredEnvVars": list(spec["requiredEnvVars"]),
        "command": spec["command"],
        "outputArtifact": spec["outputArtifact"],
        "proofRefHandleTemplate": spec["proofRefHandleTemplate"],
        "redactionRule": runbook.get(
            "redactionRule",
            "Record only proof-ref handle, artifact hash, status/count summary and command hash.",
        ),
        "failureRollback": runbook.get("failureRollback", "keep live gate blocked"),
        "closureCondition": runbook.get("closureCondition", "live evidence accepted by gates"),
        "sourceBinding": {
            "occurrenceIds": _occurrence_ids(work_item),
        },
    }
    _assert_no_sensitive_assignment(step, area=f"operator step {category}")
    return step


def _build_proof_ref_template(*, steps: list[dict[str, Any]], work_queue_sha256: str, commit: str) -> dict[str, Any]:
    proof_refs = []
    for step in steps:
        spec = CATEGORY_EXECUTION[step["category"]]
        proof_refs.append(
            {
                "id": f"proof-ref-template.{_safe_id(step['workItemId'])}",
                "proofRef": spec["proofRefHandleTemplate"],
                "evidenceType": spec["evidenceType"],
                "workItemId": step["workItemId"],
                "owner": step["owner"],
                "category": step["category"],
                "issuer": "operator:<team-or-person>",
                "capturedAt": "<UTC timestamp>",
                "expiresAt": "<UTC timestamp + policy window>",
                "redactionBoundary": PRIVACY_BOUNDARY,
                "verificationCommand": step["command"],
                "artifactHash": "sha256:<64 lowercase hex artifact digest>",
                "sourceBinding": {
                    "commit": commit,
                    "workQueueSha256": work_queue_sha256,
                    "occurrenceIds": step["sourceBinding"]["occurrenceIds"],
                },
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_bundle",
        "status": "external_live_evidence_supplied_by_operator",
        "generatedAt": "<UTC timestamp>",
        "source": {
            "workQueueKind": WORK_QUEUE_KIND,
            "workQueueSha256": work_queue_sha256,
            "commit": commit,
        },
        "proofRefs": proof_refs,
        "privacyBoundary": PRIVACY_BOUNDARY,
        "nonClaims": [
            "Template only; replace placeholders with redacted operator evidence before running proof-ref gate.",
            "Does not contain secret values or raw endpoints.",
        ],
    }


def build_packet(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    expected_commit: str | None = None,
    operator_output_dir: str = "${FATE_OPERATOR_OUTPUT_DIR}",
) -> dict[str, Any]:
    for path in (work_queue_json, proof_ref_gate_json, category_runbooks_json):
        if not path.is_file():
            raise ProductionLiveOperatorExecutionPacketError(f"input json missing: {path}")
    if RAW_URL_RE.search(operator_output_dir):
        raise ProductionLiveOperatorExecutionPacketError("operator output dir must not be raw URL")
    _assert_no_sensitive_assignment(operator_output_dir, area="operator output dir")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)

    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ProductionLiveOperatorExecutionPacketError("--expected-commit must be 40 lowercase hex chars")

    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    category_runbooks = _load_json(category_runbooks_json)
    _assert_no_sensitive_assignment(work_queue, area="workQueue")
    _assert_no_sensitive_assignment(proof_ref_gate, area="proofRefGate")
    _assert_no_sensitive_assignment(category_runbooks, area="categoryRunbooks")
    _validate_proof_ref_gate(proof_ref_gate)

    work_items = _work_items_by_id(work_queue)
    runbooks = _runbooks_by_category(category_runbooks)

    work_queue_sha256 = _sha256_file(work_queue_json)
    proof_ref_gate_sha256 = _sha256_file(proof_ref_gate_json)
    category_runbooks_sha256 = _sha256_file(category_runbooks_json)
    live_proof_contract_sha256 = _sha256_file(LIVE_PROOF_GATE_CONTRACT_PATH)
    delivery_bundle_contract_sha256 = _sha256_file(DELIVERY_BUNDLE_CONTRACT_PATH)

    steps: list[dict[str, Any]] = []
    pending_reasons: list[dict[str, str]] = []
    for work_item in work_items.values():
        category = str(work_item["category"])
        if category not in LIVE_CATEGORIES:
            continue
        runbook = runbooks.get(category)
        if runbook is None:
            pending_reasons.append(
                {"workItemId": str(work_item["id"]), "category": category, "reason": "runbook_missing"}
            )
            continue
        steps.append(_build_operator_step(len(steps) + 1, work_item=work_item, runbook=runbook))

    required_env_vars = sorted({env for step in steps for env in step["requiredEnvVars"]})
    proof_ref_template = _build_proof_ref_template(
        steps=steps,
        work_queue_sha256=work_queue_sha256,
        commit=expected_commit,
    )
    packet = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": OUTPUT_STATUS,
        "generatedAt": _utc_now(),
        "source": {
            "workQueueKind": WORK_QUEUE_KIND,
            "workQueueSha256": work_queue_sha256,
            "proofRefGateKind": PROOF_REF_GATE_KIND,
            "proofRefGateSha256": proof_ref_gate_sha256,
            "proofRefStatus": proof_ref_gate.get("proofRefStatus", ""),
            "categoryRunbooksKind": CATEGORY_RUNBOOKS_KIND,
            "categoryRunbooksSha256": category_runbooks_sha256,
            "liveProofGateContractSha256": live_proof_contract_sha256,
            "productionLiveDeliveryEvidenceBundleContractSha256": delivery_bundle_contract_sha256,
            "commit": expected_commit,
        },
        "summary": {
            "supportedCategories": len(LIVE_CATEGORIES),
            "operatorSteps": len(steps),
            "requiredEnvVars": len(required_env_vars),
            "proofRefTemplates": len(proof_ref_template["proofRefs"]),
            "pendingReasons": len(pending_reasons),
            "finalGateCommands": len(FINAL_GATE_COMMANDS),
        },
        "packetGate": {
            "status": "blocked",
            "blockingItems": [
                "operator_external_credentials_required",
                "proof_ref_bundle_required",
                "production_live_summary_required",
                "external_validation_live_proof_gate_required",
            ],
            "reason": "operator packet is ready, but real external live execution and redacted evidence are still pending",
        },
        "operatorWorkspace": {
            "envVar": "FATE_OPERATOR_OUTPUT_DIR",
            "recommendedPath": operator_output_dir,
            "requiredFiles": [
                "live-release-gate.json",
                "postgres-public-webhook-live-smoke.json",
                "multi-surface-semantic-diff.json",
                "external-validation-proof-ref-bundle.json",
                "external-validation-proof-ref-gate.json",
                "production-live-delivery-evidence-bundle.json",
                "external-validation-live-proof-gate.json",
            ],
        },
        "operatorSteps": steps,
        "requiredEnvVars": required_env_vars,
        "proofRefBundleTemplate": proof_ref_template,
        "finalGateCommands": list(FINAL_GATE_COMMANDS),
        "pendingReasons": pending_reasons,
        "privacyBoundary": PRIVACY_BOUNDARY,
        "nonClaims": contract["nonClaims"],
    }
    _assert_output_safe(packet)
    return packet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build redacted production live operator execution packet.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--proof-ref-gate-json", type=Path, required=True)
    parser.add_argument("--category-runbooks-json", type=Path, required=True)
    parser.add_argument("--expected-commit")
    parser.add_argument("--operator-output-dir", default="${FATE_OPERATOR_OUTPUT_DIR}")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    packet = build_packet(
        work_queue_json=args.work_queue_json,
        proof_ref_gate_json=args.proof_ref_gate_json,
        category_runbooks_json=args.category_runbooks_json,
        expected_commit=args.expected_commit,
        operator_output_dir=args.operator_output_dir,
    )
    output_json = args.output_json
    if not output_json.is_absolute():
        output_json = ROOT / output_json
    _write_json(output_json, packet)
    print(
        json.dumps(
            {
                "status": packet["status"],
                "kind": packet["kind"],
                "operatorSteps": packet["summary"]["operatorSteps"],
                "packetGate": packet["packetGate"]["status"],
                "outputJson": str(output_json),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
