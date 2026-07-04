#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-evidence-summary.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-validation-closure-evidence-summary.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OPERATOR_PACKET_KIND = "fatecat.external_validation_operator_execution_packet"
LIVE_PROOF_GATE_KIND = "fatecat.external_validation_live_proof_gate_summary"
CLOSURE_TREND_KIND = "fatecat.external_validation_closure_trend_dashboard"
OUTPUT_KIND = "fatecat.external_validation_closure_evidence_summary"
PRIVACY_BOUNDARY = "redacted_no_secret_values"

SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
FORBIDDEN_TEXT = ("placeholder proof", "fake proof", "dummy proof", "localhost proof")


class ExternalValidationClosureEvidenceSummaryError(RuntimeError):
    """外部验证 closure evidence summary 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationClosureEvidenceSummaryError(f"JSON root must be object: {path}")
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


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload


def _assert_no_sensitive(payload: Any, *, area: str) -> None:
    rendered = _render(payload)
    if SENSITIVE_RE.search(rendered):
        raise ExternalValidationClosureEvidenceSummaryError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationClosureEvidenceSummaryError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise ExternalValidationClosureEvidenceSummaryError(f"{area}: forbidden marker detected: {marker}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalValidationClosureEvidenceSummaryError(f"{area}.kind must be {expected}")


def _stable_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _domain_for_category(category: str) -> str:
    return category.split(".", 1)[0] if "." in category else category


def _counter_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_closure_evidence_summary_contract":
        raise ExternalValidationClosureEvidenceSummaryError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("domainSummaries", "categorySummaries", "ownerSummaries", "workItemSummaries", "externalPending"):
        if field not in required:
            raise ExternalValidationClosureEvidenceSummaryError(f"contract missing required output field: {field}")


def _work_items(work_queue: dict[str, Any]) -> list[dict[str, Any]]:
    _require_kind(work_queue, expected=WORK_QUEUE_KIND, area="workQueue")
    items = work_queue.get("workItems")
    if not isinstance(items, list):
        raise ExternalValidationClosureEvidenceSummaryError("workQueue.workItems must be array")
    result = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ExternalValidationClosureEvidenceSummaryError(f"workQueue.workItems[{index}] must be object")
        for field in ("id", "owner", "category", "priority", "status", "occurrences"):
            if item.get(field) in ("", None, []):
                raise ExternalValidationClosureEvidenceSummaryError(f"work item {index} missing {field}")
        result.append(item)
    return result


def _accepted_proof_refs(proof_ref_gate: dict[str, Any]) -> set[str]:
    _require_kind(proof_ref_gate, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    accepted = proof_ref_gate.get("acceptedProofRefs")
    if not isinstance(accepted, list):
        raise ExternalValidationClosureEvidenceSummaryError("proofRefGate.acceptedProofRefs must be array")
    return {str(item["workItemId"]) for item in accepted if isinstance(item, dict) and item.get("workItemId")}


def _accepted_live_proofs(live_proof_gate: dict[str, Any], *, expected_work_items: int) -> set[str]:
    _require_kind(live_proof_gate, expected=LIVE_PROOF_GATE_KIND, area="liveProofGate")
    accepted = live_proof_gate.get("acceptedLiveProofs")
    if not isinstance(accepted, list):
        raise ExternalValidationClosureEvidenceSummaryError("liveProofGate.acceptedLiveProofs must be array")
    summary_work_items = int(live_proof_gate.get("summary", {}).get("workItems", expected_work_items))
    if summary_work_items != expected_work_items:
        raise ExternalValidationClosureEvidenceSummaryError("liveProofGate.summary.workItems mismatch work queue")
    return {str(item["workItemId"]) for item in accepted if isinstance(item, dict) and item.get("workItemId")}


def _runbooks_by_category(category_runbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(category_runbooks, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = category_runbooks.get("runbooks")
    if not isinstance(runbooks, list):
        raise ExternalValidationClosureEvidenceSummaryError("categoryRunbooks.runbooks must be array")
    result: dict[str, dict[str, Any]] = {}
    for runbook in runbooks:
        if not isinstance(runbook, dict) or not runbook.get("category"):
            raise ExternalValidationClosureEvidenceSummaryError("categoryRunbooks.runbooks item missing category")
        result[str(runbook["category"])] = runbook
    return result


def _operator_steps_by_category(operator_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(operator_packet, expected=OPERATOR_PACKET_KIND, area="operatorPacket")
    steps = operator_packet.get("operatorSteps")
    if not isinstance(steps, list):
        raise ExternalValidationClosureEvidenceSummaryError("operatorPacket.operatorSteps must be array")
    result: dict[str, dict[str, Any]] = {}
    for step in steps:
        if not isinstance(step, dict) or not step.get("category") or not step.get("id"):
            raise ExternalValidationClosureEvidenceSummaryError("operatorPacket.operatorSteps item missing id/category")
        result[str(step["category"])] = step
    return result


def _alerts_by_work_item(closure_trend: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(closure_trend, expected=CLOSURE_TREND_KIND, area="closureTrendDashboard")
    alerts = closure_trend.get("staleAlerts")
    if not isinstance(alerts, list):
        raise ExternalValidationClosureEvidenceSummaryError("closureTrendDashboard.staleAlerts must be array")
    return {str(alert["workItemId"]): alert for alert in alerts if isinstance(alert, dict) and alert.get("workItemId")}


def _blocking_items(
    *,
    item_id: str,
    category: str,
    accepted_proof_ids: set[str],
    accepted_live_ids: set[str],
    alert: dict[str, Any] | None,
) -> list[str]:
    reasons: list[str] = []
    if item_id not in accepted_proof_ids:
        reasons.append("proof_ref_missing")
    if item_id not in accepted_live_ids:
        reasons.append("category_live_evidence_missing")
    if alert is not None:
        reasons.extend(str(reason) for reason in alert.get("alertReasons", []) if reason)
    if category == "manual_triage":
        reasons.append("manual_triage_pending")
    if category == "governance.external_validation_policy_guardrail":
        reasons.append("policy_guardrail_review_pending")
    return _stable_unique(reasons)


def _build_work_item_summary(
    *,
    item: dict[str, Any],
    runbook: dict[str, Any],
    operator_step: dict[str, Any],
    accepted_proof_ids: set[str],
    accepted_live_ids: set[str],
    alert: dict[str, Any] | None,
) -> dict[str, Any]:
    item_id = str(item["id"])
    category = str(item["category"])
    required_credentials = _stable_unique(
        [str(value) for value in runbook.get("requiredCredentials", [])]
        + [str(value) for value in operator_step.get("requiredCredentials", [])]
    )
    blocking = _blocking_items(
        item_id=item_id,
        category=category,
        accepted_proof_ids=accepted_proof_ids,
        accepted_live_ids=accepted_live_ids,
        alert=alert,
    )
    return {
        "id": item_id,
        "domain": _domain_for_category(category),
        "category": category,
        "owner": str(item["owner"]),
        "assignee": str(item.get("assignee", "")),
        "priority": str(item["priority"]),
        "status": str(item["status"]),
        "occurrences": len(item.get("occurrences") or []),
        "requiredCredentials": required_credentials,
        "requiredCredentialCount": len(required_credentials),
        "evidenceType": str(runbook.get("evidenceType", "")),
        "runbookId": str(runbook.get("id", "")),
        "operatorStepId": str(operator_step.get("id", "")),
        "operatorCommandCount": len(operator_step.get("operatorCommands", []) or []),
        "proofRefStatus": "accepted" if item_id in accepted_proof_ids else "missing",
        "liveProofStatus": "accepted" if item_id in accepted_live_ids else "missing",
        "alertStatus": "stale_alert" if alert is not None else "clear",
        "alertReasons": [str(reason) for reason in (alert or {}).get("alertReasons", [])],
        "blockingItems": blocking,
        "closureStatus": "closed_with_live_evidence" if not blocking else "external_connectivity_pending",
    }


def _rollup(
    work_item_summaries: list[dict[str, Any]],
    *,
    group_field: str,
    output_field: str,
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in work_item_summaries:
        grouped[str(item[group_field])].append(item)
    result = []
    for key in sorted(grouped):
        items = grouped[key]
        credential_names = _stable_unique(
            [credential for item in items for credential in item.get("requiredCredentials", [])]
        )
        blocking = Counter(reason for item in items for reason in item["blockingItems"])
        result.append(
            {
                output_field: key,
                "workItems": len(items),
                "occurrences": sum(int(item["occurrences"]) for item in items),
                "acceptedProofRefs": sum(1 for item in items if item["proofRefStatus"] == "accepted"),
                "acceptedLiveProofs": sum(1 for item in items if item["liveProofStatus"] == "accepted"),
                "missingProofRefs": sum(1 for item in items if item["proofRefStatus"] != "accepted"),
                "livePending": sum(1 for item in items if item["liveProofStatus"] != "accepted"),
                "staleAlerts": sum(1 for item in items if item["alertStatus"] == "stale_alert"),
                "requiredCredentials": credential_names,
                "requiredCredentialCount": len(credential_names),
                "blockingItems": _counter_dict(blocking),
            }
        )
    return result


def build_summary(
    *,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    operator_packet_json: Path,
    live_proof_gate_json: Path,
    closure_trend_dashboard_json: Path,
) -> dict[str, Any]:
    paths = (
        work_queue_json,
        proof_ref_gate_json,
        category_runbooks_json,
        operator_packet_json,
        live_proof_gate_json,
        closure_trend_dashboard_json,
    )
    for path in paths:
        if not path.is_file():
            raise ExternalValidationClosureEvidenceSummaryError(f"input json missing: {path}")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    category_runbooks = _load_json(category_runbooks_json)
    operator_packet = _load_json(operator_packet_json)
    live_proof_gate = _load_json(live_proof_gate_json)
    closure_trend = _load_json(closure_trend_dashboard_json)

    work_items = _work_items(work_queue)
    accepted_proof_ids = _accepted_proof_refs(proof_ref_gate)
    accepted_live_ids = _accepted_live_proofs(live_proof_gate, expected_work_items=len(work_items))
    runbooks = _runbooks_by_category(category_runbooks)
    operator_steps = _operator_steps_by_category(operator_packet)
    alerts = _alerts_by_work_item(closure_trend)

    work_item_categories = {str(item["category"]) for item in work_items}
    missing_runbooks = sorted(work_item_categories - set(runbooks))
    missing_operator_steps = sorted(work_item_categories - set(operator_steps))
    if missing_runbooks:
        raise ExternalValidationClosureEvidenceSummaryError(f"category runbook missing: {missing_runbooks}")
    if missing_operator_steps:
        raise ExternalValidationClosureEvidenceSummaryError(f"operator step missing: {missing_operator_steps}")

    work_item_summaries = [
        _build_work_item_summary(
            item=item,
            runbook=runbooks[str(item["category"])],
            operator_step=operator_steps[str(item["category"])],
            accepted_proof_ids=accepted_proof_ids,
            accepted_live_ids=accepted_live_ids,
            alert=alerts.get(str(item["id"])),
        )
        for item in sorted(work_items, key=lambda entry: str(entry["id"]))
    ]

    external_pending = [
        {
            "workItemId": item["id"],
            "domain": item["domain"],
            "category": item["category"],
            "owner": item["owner"],
            "blockingItems": item["blockingItems"],
            "nextAction": "execute_category_runbook_and_submit_redacted_proof_ref",
        }
        for item in work_item_summaries
        if item["blockingItems"]
    ]
    blocking_counter = Counter(reason for item in work_item_summaries for reason in item["blockingItems"])
    status = "blocked" if external_pending else "passed"
    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": "passed",
        "generatedAt": _utc_now(),
        "source": {
            "workQueueKind": WORK_QUEUE_KIND,
            "workQueueSha256": _sha256_file(work_queue_json),
            "proofRefGateKind": PROOF_REF_GATE_KIND,
            "proofRefGateSha256": _sha256_file(proof_ref_gate_json),
            "categoryRunbooksKind": CATEGORY_RUNBOOKS_KIND,
            "categoryRunbooksSha256": _sha256_file(category_runbooks_json),
            "operatorPacketKind": OPERATOR_PACKET_KIND,
            "operatorPacketSha256": _sha256_file(operator_packet_json),
            "liveProofGateKind": LIVE_PROOF_GATE_KIND,
            "liveProofGateSha256": _sha256_file(live_proof_gate_json),
            "closureTrendDashboardKind": CLOSURE_TREND_KIND,
            "closureTrendDashboardSha256": _sha256_file(closure_trend_dashboard_json),
        },
        "summary": {
            "domains": len({item["domain"] for item in work_item_summaries}),
            "categories": len({item["category"] for item in work_item_summaries}),
            "workItems": len(work_item_summaries),
            "occurrences": sum(int(item["occurrences"]) for item in work_item_summaries),
            "operatorSteps": len(operator_steps),
            "acceptedProofRefs": sum(1 for item in work_item_summaries if item["proofRefStatus"] == "accepted"),
            "acceptedLiveProofs": sum(1 for item in work_item_summaries if item["liveProofStatus"] == "accepted"),
            "missingProofRefs": sum(1 for item in work_item_summaries if item["proofRefStatus"] != "accepted"),
            "livePending": sum(1 for item in work_item_summaries if item["liveProofStatus"] != "accepted"),
            "staleAlerts": sum(1 for item in work_item_summaries if item["alertStatus"] == "stale_alert"),
            "externalPending": len(external_pending),
        },
        "closureGate": {
            "status": status,
            "blockingItems": _counter_dict(blocking_counter),
            "policy": contract["closurePolicy"],
        },
        "domainSummaries": _rollup(work_item_summaries, group_field="domain", output_field="domain"),
        "categorySummaries": _rollup(work_item_summaries, group_field="category", output_field="category"),
        "ownerSummaries": _rollup(work_item_summaries, group_field="owner", output_field="owner"),
        "workItemSummaries": work_item_summaries,
        "externalPending": external_pending,
        "finalGateCommandIds": [
            str(command.get("id", ""))
            for command in operator_packet.get("finalGateCommands", [])
            if isinstance(command, dict) and command.get("id")
        ],
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(summary, area="summary")
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build external validation closure evidence summary.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--proof-ref-gate-json", type=Path, required=True)
    parser.add_argument("--category-runbooks-json", type=Path, required=True)
    parser.add_argument("--operator-packet-json", type=Path, required=True)
    parser.add_argument("--live-proof-gate-json", type=Path, required=True)
    parser.add_argument("--closure-trend-dashboard-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(
            work_queue_json=args.work_queue_json,
            proof_ref_gate_json=args.proof_ref_gate_json,
            category_runbooks_json=args.category_runbooks_json,
            operator_packet_json=args.operator_packet_json,
            live_proof_gate_json=args.live_proof_gate_json,
            closure_trend_dashboard_json=args.closure_trend_dashboard_json,
        )
        _write_json(args.output_json, summary)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "closureGate": summary["closureGate"]["status"],
                    "domains": summary["summary"]["domains"],
                    "workItems": summary["summary"]["workItems"],
                    "externalPending": summary["summary"]["externalPending"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (ExternalValidationClosureEvidenceSummaryError, OSError, json.JSONDecodeError) as exc:
        print(f"external validation closure evidence summary error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
