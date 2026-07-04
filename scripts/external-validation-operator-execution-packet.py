#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-operator-execution-packet.json"
PROOF_REF_CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-proof-ref.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-validation-operator-execution-packet.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OUTPUT_KIND = "fatecat.external_validation_operator_execution_packet"
OUTPUT_STATUS = "operator_action_required"
PRIVACY_BOUNDARY = "redacted_no_secret_values"

SENSITIVE_VALUE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")

FINAL_GATE_COMMANDS = (
    {
        "id": "external-validation-proof-ref-gate",
        "command": (
            "bash scripts/external-validation-proof-ref-gate.sh "
            "--work-queue-json <external-validation-closure-work-queue.json> "
            "--evidence-json ${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-bundle.json "
            "--output-json ${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json"
        ),
        "produces": "${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json",
    },
    {
        "id": "external-validation-closure-trend-dashboard",
        "command": (
            "bash scripts/external-validation-closure-trend-dashboard.sh "
            "--closure-plan-json <external-validation-closure-gate.json> "
            "--work-queue-json <external-validation-closure-work-queue.json> "
            "--proof-ref-gate-json ${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-proof-ref-gate.json "
            "--category-runbooks-json <external-validation-category-runbooks.json> "
            "--output-json ${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-closure-trend-dashboard.json"
        ),
        "produces": "${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/external-validation-closure-trend-dashboard.json",
    },
    {
        "id": "measurement-infrastructure-certification",
        "command": (
            "bash scripts/measurement-infrastructure-certification.sh "
            "--evidence-dir <local-ci-output-dir> "
            "--output-json ${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/measurement-infrastructure-certification.json"
        ),
        "produces": "${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}/measurement-infrastructure-certification.json",
    },
)


class ExternalValidationOperatorExecutionPacketError(RuntimeError):
    """外部验证 operator execution packet 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationOperatorExecutionPacketError(f"JSON root must be object: {path}")
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


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", value.lower()).strip("-") or "item"


def _domain_for_category(category: str) -> str:
    if "." not in category:
        return category
    return category.split(".", 1)[0]


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload


def _assert_no_sensitive_assignment(payload: Any, *, area: str) -> None:
    rendered = _render(payload)
    if SENSITIVE_VALUE_RE.search(rendered):
        raise ExternalValidationOperatorExecutionPacketError(f"{area}: sensitive-looking assignment detected")


def _assert_output_safe(payload: dict[str, Any]) -> None:
    rendered = _render(payload)
    _assert_no_sensitive_assignment(rendered, area="output")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationOperatorExecutionPacketError("output: raw URL detected")
    for marker in ("placeholder proof", "fake proof", "dummy proof", "localhost proof"):
        if marker in rendered.lower():
            raise ExternalValidationOperatorExecutionPacketError(f"output: forbidden marker detected: {marker}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalValidationOperatorExecutionPacketError(f"{area}.kind must be {expected}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_operator_execution_packet_contract":
        raise ExternalValidationOperatorExecutionPacketError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("operatorSteps", "proofRefBundleTemplate", "finalGateCommands", "domainGroups"):
        if field not in required:
            raise ExternalValidationOperatorExecutionPacketError(f"contract missing required output field: {field}")


def _work_items_by_id(work_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(work_queue, expected=WORK_QUEUE_KIND, area="workQueue")
    items = work_queue.get("workItems")
    if not isinstance(items, list):
        raise ExternalValidationOperatorExecutionPacketError("workQueue.workItems must be array")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise ExternalValidationOperatorExecutionPacketError("workQueue.workItems item must be object")
        for field in ("id", "owner", "category", "occurrences"):
            if item.get(field) in ("", None, []):
                raise ExternalValidationOperatorExecutionPacketError(f"work item missing {field}")
        result[str(item["id"])] = item
    return result


def _runbooks_by_category(category_runbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(category_runbooks, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = category_runbooks.get("runbooks")
    if not isinstance(runbooks, list):
        raise ExternalValidationOperatorExecutionPacketError("categoryRunbooks.runbooks must be array")
    result: dict[str, dict[str, Any]] = {}
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            raise ExternalValidationOperatorExecutionPacketError("categoryRunbooks.runbooks item must be object")
        for field in (
            "id",
            "category",
            "owners",
            "requiredCredentials",
            "operatorCommands",
            "proofRefArtifactPattern",
            "sourceWorkItemIds",
        ):
            if runbook.get(field) in ("", None, []):
                raise ExternalValidationOperatorExecutionPacketError(f"runbook missing {field}")
        result[str(runbook["category"])] = runbook
    return result


def _validate_proof_ref_gate(proof_ref_gate: dict[str, Any]) -> None:
    _require_kind(proof_ref_gate, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    if "proofRefStatus" not in proof_ref_gate:
        raise ExternalValidationOperatorExecutionPacketError("proofRefGate.proofRefStatus missing")


def _occurrence_ids(work_item: dict[str, Any]) -> list[str]:
    occurrences = work_item.get("occurrences")
    if not isinstance(occurrences, list) or not occurrences:
        raise ExternalValidationOperatorExecutionPacketError(f"work item {work_item['id']}: occurrences required")
    result = [str(item["id"]) for item in occurrences if isinstance(item, dict) and item.get("id")]
    if not result:
        raise ExternalValidationOperatorExecutionPacketError(f"work item {work_item['id']}: occurrence ids required")
    return result


def _source_binding_for_work_items(work_items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "workItems": [
            {
                "id": str(item["id"]),
                "owner": str(item["owner"]),
                "occurrenceIds": _occurrence_ids(item),
            }
            for item in work_items
        ],
        "workItemIds": [str(item["id"]) for item in work_items],
        "occurrenceIds": [occurrence_id for item in work_items for occurrence_id in _occurrence_ids(item)],
    }


def _build_operator_step(
    order: int,
    *,
    runbook: dict[str, Any],
    source_work_items: list[dict[str, Any]],
) -> dict[str, Any]:
    category = str(runbook["category"])
    commands = [str(command) for command in runbook.get("operatorCommands", [])]
    step = {
        "order": order,
        "id": f"operator-step.{order:02d}.{_safe_id(category)}",
        "domain": _domain_for_category(category),
        "category": category,
        "runbookId": runbook["id"],
        "owners": list(runbook["owners"]),
        "priority": runbook.get("priority", ""),
        "status": runbook.get("status", ""),
        "evidenceType": runbook.get("evidenceType", ""),
        "requiredCredentials": list(runbook["requiredCredentials"]),
        "operatorCommands": commands,
        "operatorCommandSha256s": [_sha256_text(command) for command in commands],
        "proofRefArtifactPattern": runbook["proofRefArtifactPattern"],
        "redactionRule": runbook.get("redactionRule", ""),
        "expiryPolicy": runbook.get("expiryPolicy", ""),
        "failureRollback": runbook.get("failureRollback", ""),
        "closureCondition": runbook.get("closureCondition", ""),
        "verifierCommand": runbook.get("verifierCommand", ""),
        "sourceBinding": _source_binding_for_work_items(source_work_items),
    }
    _assert_no_sensitive_assignment(step, area=f"operator step {category}")
    return step


def _build_domain_groups(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for step in steps:
        grouped[str(step["domain"])].append(step)
    result = []
    for domain in sorted(grouped):
        domain_steps = grouped[domain]
        result.append(
            {
                "domain": domain,
                "operatorSteps": len(domain_steps),
                "categories": [str(step["category"]) for step in domain_steps],
                "workItems": sum(len(step["sourceBinding"]["workItemIds"]) for step in domain_steps),
            }
        )
    return result


def _build_proof_ref_template(*, steps: list[dict[str, Any]], work_queue_sha256: str, commit: str) -> dict[str, Any]:
    proof_refs = []
    for step in steps:
        for work_item in step["sourceBinding"]["workItems"]:
            proof_refs.append(
                {
                    "id": f"proof-ref-template.{_safe_id(work_item['id'])}",
                    "proofRef": step["proofRefArtifactPattern"],
                    "evidenceType": step["evidenceType"],
                    "workItemId": work_item["id"],
                    "owner": work_item["owner"],
                    "category": step["category"],
                    "issuer": "operator:<team-or-person>",
                    "capturedAt": "<UTC timestamp>",
                    "expiresAt": "<UTC timestamp + policy window>",
                    "redactionBoundary": PRIVACY_BOUNDARY,
                    "verificationCommand": step["verifierCommand"]
                    or "bash scripts/external-validation-proof-ref-gate.sh",
                    "artifactHash": "sha256:<64 lowercase hex artifact digest>",
                    "sourceBinding": {
                        "commit": commit,
                        "workQueueSha256": work_queue_sha256,
                        "occurrenceIds": work_item["occurrenceIds"],
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
    operator_output_dir: str = "${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}",
) -> dict[str, Any]:
    for path in (work_queue_json, proof_ref_gate_json, category_runbooks_json):
        if not path.is_file():
            raise ExternalValidationOperatorExecutionPacketError(f"input json missing: {path}")
    if RAW_URL_RE.search(operator_output_dir):
        raise ExternalValidationOperatorExecutionPacketError("operator output dir must not be raw URL")
    _assert_no_sensitive_assignment(operator_output_dir, area="operator output dir")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)

    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationOperatorExecutionPacketError("--expected-commit must be 40 lowercase hex chars")

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
    proof_ref_contract_sha256 = _sha256_file(PROOF_REF_CONTRACT_PATH)

    steps: list[dict[str, Any]] = []
    pending_reasons: list[dict[str, str]] = []
    for category in sorted(runbooks):
        runbook = runbooks[category]
        source_work_items = []
        for item_id in runbook.get("sourceWorkItemIds", []):
            work_item = work_items.get(str(item_id))
            if work_item is None:
                pending_reasons.append(
                    {"workItemId": str(item_id), "category": category, "reason": "source_work_item_missing"}
                )
                continue
            source_work_items.append(work_item)
        if not source_work_items:
            continue
        steps.append(_build_operator_step(len(steps) + 1, runbook=runbook, source_work_items=source_work_items))

    required_credentials = sorted({credential for step in steps for credential in step["requiredCredentials"]})
    proof_ref_template = _build_proof_ref_template(
        steps=steps,
        work_queue_sha256=work_queue_sha256,
        commit=expected_commit,
    )
    domain_groups = _build_domain_groups(steps)
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
            "externalValidationProofRefContractSha256": proof_ref_contract_sha256,
            "commit": expected_commit,
        },
        "summary": {
            "domains": len(domain_groups),
            "categories": len(steps),
            "operatorSteps": len(steps),
            "operatorCommands": sum(len(step["operatorCommands"]) for step in steps),
            "requiredCredentials": len(required_credentials),
            "proofRefTemplates": len(proof_ref_template["proofRefs"]),
            "pendingReasons": len(pending_reasons),
            "finalGateCommands": len(FINAL_GATE_COMMANDS),
        },
        "packetGate": {
            "status": "blocked",
            "blockingItems": [
                "operator_external_credentials_required",
                "proof_ref_bundle_required",
                "category_live_execution_required",
                "external_audit_or_certification_required",
            ],
            "reason": "operator packet is ready, but real external execution and redacted proof refs are still pending",
        },
        "operatorWorkspace": {
            "envVar": "FATE_EXTERNAL_OPERATOR_OUTPUT_DIR",
            "recommendedPath": operator_output_dir,
            "requiredFiles": [
                "external-validation-proof-ref-bundle.json",
                "external-validation-proof-ref-gate.json",
                "external-validation-closure-trend-dashboard.json",
                "measurement-infrastructure-certification.json",
            ],
        },
        "domainGroups": domain_groups,
        "operatorSteps": steps,
        "requiredCredentials": required_credentials,
        "proofRefBundleTemplate": proof_ref_template,
        "finalGateCommands": list(FINAL_GATE_COMMANDS),
        "pendingReasons": pending_reasons,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_output_safe(packet)
    return packet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build redacted external validation operator execution packet.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--proof-ref-gate-json", type=Path, required=True)
    parser.add_argument("--category-runbooks-json", type=Path, required=True)
    parser.add_argument("--expected-commit")
    parser.add_argument("--operator-output-dir", default="${FATE_EXTERNAL_OPERATOR_OUTPUT_DIR}")
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
                "domains": packet["summary"]["domains"],
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
