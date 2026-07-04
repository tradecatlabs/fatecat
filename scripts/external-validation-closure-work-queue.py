from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-work-queue.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-closure-work-queue.json"
)

FORBIDDEN_MARKERS = (
    "token=",
    "secret=",
    "password=",
    "passwd=",
    "api_key=",
    "api-key=",
    "private_key=",
    "private-key=",
    "DATABASE_URL=",
    "DB_DSN=",
    "BEGIN RSA",
    "BEGIN OPENSSH",
)

MANUAL_CATEGORY = "manual_triage"
POLICY_GUARDRAIL_CATEGORY = "governance.external_validation_policy_guardrail"


class ExternalValidationClosureWorkQueueError(RuntimeError):
    pass


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _stable_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _validate_list_of_strings(value: Any, *, field: str, item_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(entry, str) and entry for entry in value):
        raise ExternalValidationClosureWorkQueueError(
            f"closure item {item_id} field {field} must be non-empty string list"
        )
    return value


def _validate_closure_plan(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ExternalValidationClosureWorkQueueError("closure plan root must be an object")
    if payload.get("kind") != "fatecat.external_validation_closure_plan":
        raise ExternalValidationClosureWorkQueueError(
            "closure plan kind must be fatecat.external_validation_closure_plan"
        )
    items = payload.get("items")
    if not isinstance(items, list):
        raise ExternalValidationClosureWorkQueueError("closure plan items must be an array")
    validated: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ExternalValidationClosureWorkQueueError(f"closure item {index} must be object")
        item_id = item.get("id")
        category = item.get("category")
        owner = item.get("owner")
        status = item.get("status")
        source = item.get("source")
        closure_condition = item.get("closureCondition")
        if not isinstance(item_id, str) or not item_id:
            raise ExternalValidationClosureWorkQueueError(f"closure item {index} missing id")
        if not isinstance(category, str) or not category:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing category")
        if not isinstance(owner, str) or not owner:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing owner")
        if not isinstance(status, str) or not status:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing status")
        if not isinstance(source, dict):
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing source")
        if not isinstance(source.get("path"), str) or not source["path"]:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing source.path")
        if not isinstance(source.get("line"), int) or source["line"] <= 0:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing positive source.line")
        if not isinstance(source.get("excerptSha256"), str) or not source["excerptSha256"]:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing source.excerptSha256")
        if not isinstance(closure_condition, str) or not closure_condition:
            raise ExternalValidationClosureWorkQueueError(f"closure item {item_id} missing closureCondition")
        _validate_list_of_strings(item.get("credentialDependencies"), field="credentialDependencies", item_id=item_id)
        _validate_list_of_strings(item.get("requiredEvidence"), field="requiredEvidence", item_id=item_id)
        _validate_list_of_strings(item.get("verificationCommands"), field="verificationCommands", item_id=item_id)
        validated.append(item)
    return validated


def _work_item_status(category: str) -> str:
    if category == MANUAL_CATEGORY:
        return "manual_triage_required"
    if category == POLICY_GUARDRAIL_CATEGORY:
        return "policy_guardrail_review_required"
    return "pending_external_evidence"


def _priority(category: str) -> str:
    if category in {MANUAL_CATEGORY, POLICY_GUARDRAIL_CATEGORY}:
        return "P1"
    return "P0"


def _stale_reason(status: str) -> str:
    if status == "manual_triage_required":
        return "manual_classification_required"
    if status == "policy_guardrail_review_required":
        return "policy_guardrail_requires_review"
    return "proof_ref_missing"


def _close_condition_result(status: str) -> str:
    if status == "manual_triage_required":
        return "not_evaluated_manual_triage_required"
    if status == "policy_guardrail_review_required":
        return "not_evaluated_policy_guardrail_review_required"
    return "not_evaluated_no_proof_ref"


def _occurrence_ref(item: dict[str, Any]) -> dict[str, Any]:
    source = item["source"]
    return {
        "id": item["id"],
        "source": {
            "path": source["path"],
            "line": source["line"],
            "excerptSha256": source["excerptSha256"],
        },
        "status": item["status"],
    }


def _assert_no_forbidden(summary: dict[str, Any]) -> None:
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    forbidden = [marker for marker in FORBIDDEN_MARKERS if marker.lower() in rendered.lower()]
    if forbidden:
        raise ExternalValidationClosureWorkQueueError(
            "closure work queue contains forbidden sensitive marker: " + ", ".join(forbidden)
        )


def build_summary(*, closure_plan_json: Path) -> dict[str, Any]:
    if not closure_plan_json.is_file():
        raise ExternalValidationClosureWorkQueueError(f"closure plan json missing: {closure_plan_json}")
    contract = _load_json(CONTRACT_PATH)
    closure_plan = _load_json(closure_plan_json)
    closure_items = _validate_closure_plan(closure_plan)
    generated_at = _utc_now()

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in closure_items:
        grouped[(item["owner"], item["category"])].append(item)

    work_items: list[dict[str, Any]] = []
    by_owner: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for (owner, category), items in sorted(grouped.items()):
        status = _work_item_status(category)
        by_owner[owner] = by_owner.get(owner, 0) + len(items)
        by_status[status] = by_status.get(status, 0) + 1
        conditions = _stable_unique([str(item["closureCondition"]) for item in items])
        work_items.append(
            {
                "id": f"external-work.{_short_hash(f'{owner}:{category}')}",
                "owner": owner,
                "assignee": f"unassigned:{owner}",
                "category": category,
                "priority": _priority(category),
                "status": status,
                "proofRef": "",
                "lastCheckedAt": generated_at,
                "staleReason": _stale_reason(status),
                "closeConditionResult": _close_condition_result(status),
                "credentialDependencies": _stable_unique(
                    [entry for item in items for entry in item["credentialDependencies"]]
                ),
                "requiredEvidence": _stable_unique([entry for item in items for entry in item["requiredEvidence"]]),
                "verificationCommands": _stable_unique(
                    [entry for item in items for entry in item["verificationCommands"]]
                ),
                "closureCondition": (
                    conditions[0]
                    if len(conditions) == 1
                    else "All grouped occurrences must satisfy their closure conditions before status can change."
                ),
                "closureConditions": conditions,
                "occurrences": [_occurrence_ref(item) for item in sorted(items, key=lambda entry: entry["id"])],
            }
        )

    ship_status = "blocked" if work_items else "passed"
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_work_queue",
        "generatedAt": generated_at,
        "status": "passed",
        "source": {
            "closurePlanJson": str(closure_plan_json),
            "closurePlanSha256": _sha256_file(closure_plan_json),
            "closurePlanKind": closure_plan.get("kind"),
            "closureItemCount": len(closure_items),
        },
        "summary": {
            "totalOccurrences": len(closure_items),
            "workItems": len(work_items),
            "owners": len({owner for owner, _category in grouped}),
            "categories": len({category for _owner, category in grouped}),
            "manualTriageOccurrences": sum(1 for item in closure_items if item["category"] == MANUAL_CATEGORY),
            "policyGuardrailOccurrences": sum(
                1 for item in closure_items if item["category"] == POLICY_GUARDRAIL_CATEGORY
            ),
            "externalPendingOccurrences": sum(
                1 for item in closure_items if item["category"] not in {MANUAL_CATEGORY, POLICY_GUARDRAIL_CATEGORY}
            ),
            "staleItems": len(work_items),
            "byOwner": dict(sorted(by_owner.items())),
            "byStatus": dict(sorted(by_status.items())),
        },
        "shipGate": {
            "status": ship_status,
            "reason": (
                "external validation work queue has pending items"
                if work_items
                else "no external validation work items"
            ),
            "policy": contract["workQueuePolicy"]["shipGate"],
        },
        "workItems": work_items,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build external validation closure owner work queue.")
    parser.add_argument("--closure-plan-json", type=Path, required=True, help="external-validation-closure-gate.json")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output work queue JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(closure_plan_json=args.closure_plan_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "shipGate": summary["shipGate"]["status"],
                    "workItems": summary["summary"]["workItems"],
                    "totalOccurrences": summary["summary"]["totalOccurrences"],
                    "staleItems": summary["summary"]["staleItems"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ExternalValidationClosureWorkQueueError, OSError, json.JSONDecodeError) as exc:
        print(f"external validation closure work queue error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
