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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-trend-dashboard.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-validation-closure-trend-dashboard.json"
)

CLOSURE_PLAN_KIND = "fatecat.external_validation_closure_plan"
WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
PROOF_REF_GATE_KIND = "fatecat.external_validation_proof_ref_gate_summary"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OUTPUT_KIND = "fatecat.external_validation_closure_trend_dashboard"

MANUAL_CATEGORY = "manual_triage"
POLICY_GUARDRAIL_CATEGORY = "governance.external_validation_policy_guardrail"

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
    "dummy proof",
    "fake proof",
    "localhost proof",
    "placeholder proof",
}


class ExternalValidationClosureTrendDashboardError(RuntimeError):
    """外部验证 closure trend dashboard gate 失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: str, *, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ExternalValidationClosureTrendDashboardError(f"{field}: timestamp required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ExternalValidationClosureTrendDashboardError(f"{field}: must be ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ExternalValidationClosureTrendDashboardError(f"{field}: timezone required")
    return parsed.astimezone(UTC)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationClosureTrendDashboardError(f"JSON root must be object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_forbidden(payload: Any, *, area: str) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if re.search(r"https?://", rendered, re.I):
        bad.append("raw_url")
    bad.extend(sorted(fragment for fragment in FORBIDDEN_TEXT if fragment in rendered))
    if bad:
        raise ExternalValidationClosureTrendDashboardError(f"{area}: forbidden fragment detected: {', '.join(bad)}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalValidationClosureTrendDashboardError(f"{area}.kind must be {expected}")


def _validate_closure_plan(payload: dict[str, Any]) -> list[dict[str, Any]]:
    _require_kind(payload, expected=CLOSURE_PLAN_KIND, area="closurePlan")
    items = payload.get("items")
    if not isinstance(items, list):
        raise ExternalValidationClosureTrendDashboardError("closurePlan.items must be array")
    return [item for item in items if isinstance(item, dict)]


def _validate_work_queue(payload: dict[str, Any]) -> list[dict[str, Any]]:
    _require_kind(payload, expected=WORK_QUEUE_KIND, area="workQueue")
    work_items = payload.get("workItems")
    if not isinstance(work_items, list):
        raise ExternalValidationClosureTrendDashboardError("workQueue.workItems must be array")
    validated: list[dict[str, Any]] = []
    for index, item in enumerate(work_items):
        if not isinstance(item, dict):
            raise ExternalValidationClosureTrendDashboardError(f"workQueue.workItems[{index}] must be object")
        for field in ("id", "owner", "category", "priority", "status", "lastCheckedAt", "occurrences"):
            if field not in item or item[field] in ("", None, []):
                raise ExternalValidationClosureTrendDashboardError(f"work item {index} missing {field}")
        if not isinstance(item["occurrences"], list):
            raise ExternalValidationClosureTrendDashboardError(f"work item {item['id']} occurrences must be array")
        validated.append(item)
    return validated


def _validate_proof_ref_gate(payload: dict[str, Any]) -> tuple[set[str], set[str]]:
    _require_kind(payload, expected=PROOF_REF_GATE_KIND, area="proofRefGate")
    accepted = payload.get("acceptedProofRefs")
    pending = payload.get("pendingWorkItems")
    if not isinstance(accepted, list) or not isinstance(pending, list):
        raise ExternalValidationClosureTrendDashboardError(
            "proofRefGate acceptedProofRefs/pendingWorkItems must be arrays"
        )
    accepted_ids = {str(item["workItemId"]) for item in accepted if isinstance(item, dict) and item.get("workItemId")}
    pending_ids = {str(item["id"]) for item in pending if isinstance(item, dict) and item.get("id")}
    return accepted_ids, pending_ids


def _validate_category_runbooks(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(payload, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = payload.get("runbooks")
    if not isinstance(runbooks, list):
        raise ExternalValidationClosureTrendDashboardError("categoryRunbooks.runbooks must be array")
    by_category: dict[str, dict[str, Any]] = {}
    for index, runbook in enumerate(runbooks):
        if not isinstance(runbook, dict) or not runbook.get("category"):
            raise ExternalValidationClosureTrendDashboardError(f"categoryRunbooks.runbooks[{index}] missing category")
        by_category[str(runbook["category"])] = runbook
    return by_category


def _age_hours(*, now: datetime, last_checked_at: str) -> float:
    checked_at = _parse_timestamp(last_checked_at, field="lastCheckedAt")
    seconds = max((now - checked_at).total_seconds(), 0.0)
    return round(seconds / 3600.0, 3)


def _alert_reasons(
    item: dict[str, Any],
    *,
    accepted_work_ids: set[str],
    runbook_by_category: dict[str, dict[str, Any]],
) -> list[str]:
    category = str(item["category"])
    reasons: list[str] = []
    if category == MANUAL_CATEGORY or item.get("status") == "manual_triage_required":
        reasons.append("manual_triage")
    if category == POLICY_GUARDRAIL_CATEGORY or item.get("status") == "policy_guardrail_review_required":
        reasons.append("policy_guardrail")
    if str(item["id"]) not in accepted_work_ids:
        reasons.append("proof_ref_missing")
    if category in runbook_by_category:
        reasons.append("category_live_pending")
    if item.get("staleReason"):
        reasons.append("stale_owner_pending")
    return _stable_unique(reasons)


def _alert_level(priority: str, reasons: list[str]) -> str:
    if priority == "P0" and ("proof_ref_missing" in reasons or "category_live_pending" in reasons):
        return "P0"
    if "manual_triage" in reasons or "policy_guardrail" in reasons:
        return "P1"
    if reasons:
        return "P2"
    return "clear"


def _count_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def _previous_summary(previous_dashboard_json: Path | None) -> dict[str, int] | None:
    if previous_dashboard_json is None:
        return None
    if not previous_dashboard_json.is_file():
        raise ExternalValidationClosureTrendDashboardError(
            f"previous dashboard json missing: {previous_dashboard_json}"
        )
    previous = _load_json(previous_dashboard_json)
    _require_kind(previous, expected=OUTPUT_KIND, area="previousDashboard")
    summary = previous.get("summary")
    if not isinstance(summary, dict):
        raise ExternalValidationClosureTrendDashboardError("previousDashboard.summary must be object")
    fields = (
        "workItems",
        "staleAlerts",
        "missingProofRefs",
        "manualTriageWorkItems",
        "policyGuardrailWorkItems",
        "categoryLivePendingWorkItems",
    )
    return {field: int(summary.get(field, 0)) for field in fields}


def _build_dashboard_lists(
    *,
    work_items: list[dict[str, Any]],
    alerts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    alerts_by_item = {alert["workItemId"]: alert for alert in alerts}
    owner_counts: dict[str, Counter[str]] = defaultdict(Counter)
    owner_categories: dict[str, Counter[str]] = defaultdict(Counter)
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    status_counts: Counter[str] = Counter()
    owner_max_age: dict[str, float] = defaultdict(float)
    category_max_age: dict[str, float] = defaultdict(float)

    for item in work_items:
        owner = str(item["owner"])
        category = str(item["category"])
        status = str(item["status"])
        alert = alerts_by_item.get(str(item["id"]))
        alert_reasons = alert["alertReasons"] if alert is not None else []
        age_hours = float(alert["ageHours"]) if alert is not None else 0.0
        status_counts[status] += 1
        owner_counts[owner]["workItems"] += 1
        owner_counts[owner]["occurrences"] += len(item.get("occurrences") or [])
        owner_categories[owner][category] += 1
        category_counts[category]["workItems"] += 1
        category_counts[category]["occurrences"] += len(item.get("occurrences") or [])
        owner_max_age[owner] = max(owner_max_age[owner], age_hours)
        category_max_age[category] = max(category_max_age[category], age_hours)
        for reason in alert_reasons:
            owner_counts[owner][reason] += 1
            category_counts[category][reason] += 1

    owner_dashboard = [
        {
            "owner": owner,
            "workItems": counts["workItems"],
            "occurrences": counts["occurrences"],
            "staleAlerts": sum(
                counts[reason]
                for reason in ("proof_ref_missing", "category_live_pending", "manual_triage", "policy_guardrail")
            ),
            "maxAgeHours": round(owner_max_age[owner], 3),
            "categoryBreakdown": _count_dict(owner_categories[owner]),
            "reasonBreakdown": _count_dict(
                Counter({key: value for key, value in counts.items() if key not in {"workItems", "occurrences"}})
            ),
        }
        for owner, counts in sorted(owner_counts.items())
    ]
    category_dashboard = [
        {
            "category": category,
            "workItems": counts["workItems"],
            "occurrences": counts["occurrences"],
            "maxAgeHours": round(category_max_age[category], 3),
            "reasonBreakdown": _count_dict(
                Counter({key: value for key, value in counts.items() if key not in {"workItems", "occurrences"}})
            ),
        }
        for category, counts in sorted(category_counts.items())
    ]
    return owner_dashboard, category_dashboard, _count_dict(status_counts)


def build_summary(
    *,
    closure_plan_json: Path,
    work_queue_json: Path,
    proof_ref_gate_json: Path,
    category_runbooks_json: Path,
    previous_dashboard_json: Path | None = None,
    now_iso: str | None = None,
) -> dict[str, Any]:
    for path in (closure_plan_json, work_queue_json, proof_ref_gate_json, category_runbooks_json):
        if not path.is_file():
            raise ExternalValidationClosureTrendDashboardError(f"input json missing: {path}")
    contract = _load_json(CONTRACT_PATH)
    closure_plan = _load_json(closure_plan_json)
    work_queue = _load_json(work_queue_json)
    proof_ref_gate = _load_json(proof_ref_gate_json)
    category_runbooks = _load_json(category_runbooks_json)
    closure_items = _validate_closure_plan(closure_plan)
    work_items = _validate_work_queue(work_queue)
    accepted_work_ids, pending_work_ids = _validate_proof_ref_gate(proof_ref_gate)
    runbook_by_category = _validate_category_runbooks(category_runbooks)
    categories = {str(item["category"]) for item in work_items}
    missing_runbooks = sorted(categories - set(runbook_by_category))
    if missing_runbooks:
        raise ExternalValidationClosureTrendDashboardError(f"category runbook missing: {missing_runbooks}")
    if int(work_queue.get("summary", {}).get("totalOccurrences", len(closure_items))) != len(closure_items):
        raise ExternalValidationClosureTrendDashboardError("workQueue.summary.totalOccurrences mismatch closure plan")
    if int(proof_ref_gate.get("summary", {}).get("workItems", len(work_items))) != len(work_items):
        raise ExternalValidationClosureTrendDashboardError("proofRefGate.summary.workItems mismatch work queue")
    now = _parse_timestamp(now_iso, field="--now") if now_iso else datetime.now(UTC)
    generated_at = now.isoformat(timespec="seconds").replace("+00:00", "Z")

    alerts: list[dict[str, Any]] = []
    for item in sorted(work_items, key=lambda entry: str(entry["id"])):
        item_id = str(item["id"])
        reasons = _alert_reasons(item, accepted_work_ids=accepted_work_ids, runbook_by_category=runbook_by_category)
        if not reasons:
            continue
        priority = str(item.get("priority", "P0"))
        age_hours = _age_hours(now=now, last_checked_at=str(item["lastCheckedAt"]))
        alerts.append(
            {
                "id": f"stale-alert.{item_id}",
                "workItemId": item_id,
                "owner": str(item["owner"]),
                "assignee": str(item.get("assignee", "")),
                "category": str(item["category"]),
                "priority": priority,
                "alertLevel": _alert_level(priority, reasons),
                "status": str(item["status"]),
                "staleReason": str(item.get("staleReason", "")),
                "alertReasons": reasons,
                "ageHours": age_hours,
                "lastCheckedAt": str(item["lastCheckedAt"]),
                "occurrenceCount": len(item.get("occurrences") or []),
                "proofRefStatus": "schema_accepted" if item_id in accepted_work_ids else "missing",
                "proofRefPending": item_id in pending_work_ids,
                "categoryRunbookStatus": "ready",
                "nonClosureBoundary": "Alert is a local owner reminder; it is not live evidence closure.",
            }
        )

    owner_dashboard, category_dashboard, status_dashboard = _build_dashboard_lists(work_items=work_items, alerts=alerts)
    previous = _previous_summary(previous_dashboard_json)
    current_trend_fields = {
        "workItems": len(work_items),
        "staleAlerts": len(alerts),
        "missingProofRefs": sum(1 for item in work_items if str(item["id"]) not in accepted_work_ids),
        "manualTriageWorkItems": sum(1 for item in work_items if item["category"] == MANUAL_CATEGORY),
        "policyGuardrailWorkItems": sum(1 for item in work_items if item["category"] == POLICY_GUARDRAIL_CATEGORY),
        "categoryLivePendingWorkItems": len(work_items),
    }
    deltas = (
        {field: current_trend_fields[field] - previous[field] for field in current_trend_fields}
        if previous is not None
        else {}
    )
    ship_blocking_items = []
    if alerts:
        ship_blocking_items.append("external_validation_stale_alerts_pending")
    if current_trend_fields["missingProofRefs"]:
        ship_blocking_items.append("proof_ref_evidence_pending")
    if current_trend_fields["categoryLivePendingWorkItems"]:
        ship_blocking_items.append("category_live_execution_pending")
    if current_trend_fields["manualTriageWorkItems"]:
        ship_blocking_items.append("manual_triage_pending")
    if current_trend_fields["policyGuardrailWorkItems"]:
        ship_blocking_items.append("policy_guardrail_review_pending")

    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": generated_at,
        "status": "passed",
        "source": {
            "closurePlanJson": str(closure_plan_json),
            "closurePlanSha256": _sha256_file(closure_plan_json),
            "workQueueJson": str(work_queue_json),
            "workQueueSha256": _sha256_file(work_queue_json),
            "proofRefGateJson": str(proof_ref_gate_json),
            "proofRefGateSha256": _sha256_file(proof_ref_gate_json),
            "categoryRunbooksJson": str(category_runbooks_json),
            "categoryRunbooksSha256": _sha256_file(category_runbooks_json),
            "previousDashboardJson": str(previous_dashboard_json) if previous_dashboard_json else "",
        },
        "summary": {
            "totalOccurrences": len(closure_items),
            "workItems": len(work_items),
            "owners": len({str(item["owner"]) for item in work_items}),
            "categories": len(categories),
            "acceptedProofRefs": len(accepted_work_ids),
            "pendingWorkItems": len(pending_work_ids),
            "missingProofRefs": current_trend_fields["missingProofRefs"],
            "manualTriageWorkItems": current_trend_fields["manualTriageWorkItems"],
            "policyGuardrailWorkItems": current_trend_fields["policyGuardrailWorkItems"],
            "categoryLivePendingWorkItems": current_trend_fields["categoryLivePendingWorkItems"],
            "staleOwnerCount": len({alert["owner"] for alert in alerts}),
            "staleAlerts": len(alerts),
            "maxAgeHours": max((float(alert["ageHours"]) for alert in alerts), default=0.0),
        },
        "trend": {
            "previousDashboardProvided": previous is not None,
            "current": current_trend_fields,
            "delta": deltas,
        },
        "ownerDashboard": owner_dashboard,
        "categoryDashboard": category_dashboard,
        "statusDashboard": status_dashboard,
        "staleAlerts": alerts,
        "alertStatus": "stale_alerts_pending" if alerts else "clear",
        "alertGate": {
            "status": "blocked" if alerts else "passed",
            "deliveryMode": contract["alertPolicy"]["deliveryMode"],
            "deliveryStatus": "not_sent",
            "staleAlerts": len(alerts),
            "staleOwners": len({alert["owner"] for alert in alerts}),
            "policy": contract["alertPolicy"]["ackPolicy"],
            "blockingItems": ["stale_owner_alerts_pending"] if alerts else [],
        },
        "shipGate": {
            "status": "blocked" if ship_blocking_items else "passed",
            "blockingItems": ship_blocking_items,
            "policy": contract["alertPolicy"]["shipGate"],
        },
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary, area="summary")
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build external validation closure trend dashboard.")
    parser.add_argument("--closure-plan-json", type=Path, required=True, help="external-validation-closure-gate.json")
    parser.add_argument(
        "--work-queue-json", type=Path, required=True, help="external-validation-closure-work-queue.json"
    )
    parser.add_argument(
        "--proof-ref-gate-json", type=Path, required=True, help="external-validation-proof-ref-gate.json"
    )
    parser.add_argument(
        "--category-runbooks-json", type=Path, required=True, help="external-validation-category-runbooks.json"
    )
    parser.add_argument("--previous-dashboard-json", type=Path, help="optional previous dashboard JSON for delta")
    parser.add_argument("--now", help="override generatedAt/age clock for deterministic tests")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output dashboard JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(
            closure_plan_json=args.closure_plan_json,
            work_queue_json=args.work_queue_json,
            proof_ref_gate_json=args.proof_ref_gate_json,
            category_runbooks_json=args.category_runbooks_json,
            previous_dashboard_json=args.previous_dashboard_json,
            now_iso=args.now,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "alertStatus": summary["alertStatus"],
                    "shipGate": summary["shipGate"]["status"],
                    "staleAlerts": summary["summary"]["staleAlerts"],
                    "staleOwners": summary["summary"]["staleOwnerCount"],
                    "missingProofRefs": summary["summary"]["missingProofRefs"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ExternalValidationClosureTrendDashboardError, OSError, json.JSONDecodeError) as exc:
        print(f"external validation closure trend dashboard error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
