#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
CONTRACT_ROOT = REPO_ROOT / "contracts" / "fate"
DEFAULT_BASELINE = CONTRACT_ROOT / "evidence-coverage-baseline.json"
DEFAULT_CONTRACT = CONTRACT_ROOT / "evidence-coverage-trend-contract.json"
RULE_DEPTH_REGISTRY = CONTRACT_ROOT / "rule_depth_registry.json"
CLASSICS_RULE_INDEX = CONTRACT_ROOT / "classics_rule_index.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "quality" / "evidence-coverage-trend.json"
)

SAMPLE_PAYLOADS: dict[str, dict[str, Any]] = {
    "bazi": {
        "name": "测试样本",
        "gender": "male",
        "birthDateTime": "1990-01-01 08:00:00",
        "birthPlace": "北京",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "useTrueSolarTime": True,
    },
    "ziwei": {
        "name": "测试样本",
        "gender": "male",
        "birthDateTime": "1990-01-01 08:00:00",
        "birthPlace": "北京",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "useTrueSolarTime": True,
    },
}


class EvidenceCoverageTrendGateError(RuntimeError):
    """Evidence coverage trend gate 发现结构性错误。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)

    from fastapi.testclient import TestClient  # noqa: PLC0415

    from fate_core.capabilities import CapabilityExecutor, CapabilityInput  # noqa: PLC0415
    from main import app  # noqa: PLC0415

    return CapabilityExecutor, CapabilityInput, TestClient, app


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceCoverageTrendGateError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceCoverageTrendGateError(f"invalid JSON file: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceCoverageTrendGateError(f"JSON root must be object: {path}")
    return payload


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _classics_rule_ids() -> set[str]:
    payload = _load_json(CLASSICS_RULE_INDEX)
    return {str(item.get("id")) for item in payload.get("rules", []) if isinstance(item, dict) and item.get("id")}


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 1.0
    return round(numerator / denominator, 4)


def _rule_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_registry(classics_ids: set[str]) -> dict[str, Any]:
    registry = _load_json(RULE_DEPTH_REGISTRY)
    rules = registry.get("rules")
    if not isinstance(rules, list) or not rules:
        raise EvidenceCoverageTrendGateError("rule_depth_registry.json has no rules")

    broken_refs: list[dict[str, str]] = []
    rules_by_system: dict[str, int] = {}
    rules_by_layer: dict[str, int] = {}
    rule_ids: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_id = str(rule.get("id") or "")
        system = str(rule.get("system") or "unknown")
        layer = str(rule.get("layer") or "unknown")
        rule_ids.add(rule_id)
        rules_by_system[system] = rules_by_system.get(system, 0) + 1
        rules_by_layer[f"{system}.{layer}"] = rules_by_layer.get(f"{system}.{layer}", 0) + 1
        if rule_id not in classics_ids:
            broken_refs.append({"scope": "rule.id", "ruleId": rule_id, "missingRef": rule_id})
        for source_rule_id in _rule_ids(rule.get("sourceRuleIds")):
            if source_rule_id not in classics_ids:
                broken_refs.append({"scope": "rule.sourceRuleIds", "ruleId": rule_id, "missingRef": source_rule_id})

    return {
        "path": _rel(RULE_DEPTH_REGISTRY),
        "registryVersion": str(registry.get("registryVersion", "unknown")),
        "totalRules": len(rules),
        "rulesBySystem": rules_by_system,
        "rulesByLayer": rules_by_layer,
        "ruleIds": sorted(rule_ids),
        "brokenRuleRefs": broken_refs,
    }


def _evidence_item_complete(item: dict[str, Any]) -> bool:
    has_rule_ids = bool(_rule_ids(item.get("ruleIds")))
    has_source = _has_text(item.get("source")) or bool(item.get("sources"))
    has_basis = bool(item.get("basis"))
    has_risk = _has_text(item.get("riskBoundary")) or _has_text(item.get("risk"))
    return has_rule_ids and has_source and has_basis and has_risk


def _find_broken_rule_refs(
    *, scope: str, owner: str, rule_ids: list[str], classics_ids: set[str]
) -> list[dict[str, str]]:
    return [
        {"scope": scope, "owner": owner, "missingRef": rule_id} for rule_id in rule_ids if rule_id not in classics_ids
    ]


def _depth_key(capability_id: str) -> str:
    if capability_id == "bazi":
        return "baziRuleDepth"
    if capability_id == "ziwei":
        return "ziweiRuleDepth"
    raise EvidenceCoverageTrendGateError(f"unsupported capability: {capability_id}")


def _validate_applied_rules(
    *,
    capability_id: str,
    depth: dict[str, Any],
    registry_rule_ids: set[str],
    classics_ids: set[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    broken_refs: list[dict[str, str]] = []
    incomplete: list[dict[str, str]] = []
    for item in depth.get("appliedRules", []):
        if not isinstance(item, dict):
            continue
        rule_id = str(item.get("ruleId") or "")
        if rule_id not in registry_rule_ids:
            broken_refs.append(
                {"scope": f"{capability_id}.appliedRules.ruleId", "owner": rule_id, "missingRef": rule_id}
            )
        source_rule_ids = _rule_ids(item.get("sourceRuleIds"))
        broken_refs.extend(
            _find_broken_rule_refs(
                scope=f"{capability_id}.appliedRules.sourceRuleIds",
                owner=rule_id,
                rule_ids=source_rule_ids,
                classics_ids=classics_ids,
            )
        )
        required = ("ruleId", "evidenceFields", "conditions", "conflictPolicy", "riskBoundary", "sourceRuleIds")
        missing = [field for field in required if not item.get(field)]
        if missing:
            incomplete.append({"ruleId": rule_id, "missingFields": ",".join(missing)})
    return broken_refs, incomplete


def _validate_api_report_refs(
    *,
    client: Any,
    capability_id: str,
    payload: dict[str, Any],
    classics_ids: set[str],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    response = client.post(f"/capabilities/{capability_id}/calculate", json=payload)
    if response.status_code != 200:
        raise EvidenceCoverageTrendGateError(f"API calculate failed for {capability_id}: {response.status_code}")
    report = response.json().get("report")
    if not isinstance(report, dict):
        raise EvidenceCoverageTrendGateError(f"API report missing for {capability_id}")
    refs = report.get("evidenceRefs")
    if not isinstance(refs, list):
        raise EvidenceCoverageTrendGateError(f"API report evidenceRefs missing for {capability_id}")
    broken_refs: list[dict[str, str]] = []
    complete_count = 0
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        ref_id = str(ref.get("id") or "")
        if _has_text(ref.get("id")) and _has_text(ref.get("source")) and isinstance(ref.get("ruleIds"), list):
            complete_count += 1
        broken_refs.extend(
            _find_broken_rule_refs(
                scope=f"{capability_id}.report.evidenceRefs",
                owner=ref_id,
                rule_ids=_rule_ids(ref.get("ruleIds")),
                classics_ids=classics_ids,
            )
        )
    return {
        "count": len(refs),
        "completeCount": complete_count,
        "completeRatio": _ratio(complete_count, len(refs)),
    }, broken_refs


def _validate_capability(
    *,
    capability_id: str,
    executor: Any,
    CapabilityInput: Any,
    client: Any,
    registry_rule_ids: set[str],
    classics_ids: set[str],
) -> dict[str, Any]:
    payload = SAMPLE_PAYLOADS[capability_id]
    result = executor.execute(CapabilityInput(capability_id=capability_id, payload=payload))
    data = result.data
    evidence = result.evidence
    items = evidence.get("items")
    if not isinstance(items, dict):
        raise EvidenceCoverageTrendGateError(f"analysis evidence items missing for {capability_id}")

    broken_refs: list[dict[str, str]] = []
    incomplete_items: list[str] = []
    complete_count = 0
    for item_id, item in items.items():
        if not isinstance(item, dict):
            incomplete_items.append(str(item_id))
            continue
        rule_ids = _rule_ids(item.get("ruleIds"))
        broken_refs.extend(
            _find_broken_rule_refs(
                scope=f"{capability_id}.analysisEvidence.items",
                owner=str(item_id),
                rule_ids=rule_ids,
                classics_ids=classics_ids,
            )
        )
        if _evidence_item_complete(item):
            complete_count += 1
        else:
            incomplete_items.append(str(item_id))

    depth = data.get(_depth_key(capability_id))
    if not isinstance(depth, dict):
        raise EvidenceCoverageTrendGateError(f"rule depth missing for {capability_id}")
    applied_rules = depth.get("appliedRules", [])
    conflicts = depth.get("conflictResolution", {}).get("conflicts", [])
    statements = depth.get("combinationStatements", [])

    applied_broken_refs, incomplete_applied_rules = _validate_applied_rules(
        capability_id=capability_id,
        depth=depth,
        registry_rule_ids=registry_rule_ids,
        classics_ids=classics_ids,
    )
    broken_refs.extend(applied_broken_refs)

    conflict_count = len(conflicts) if isinstance(conflicts, list) else 0
    conflict_explanation_count = sum(
        1 for item in conflicts if isinstance(item, dict) and _has_text(item.get("explanation"))
    )
    conflict_counter_evidence_count = sum(
        1 for item in conflicts if isinstance(item, dict) and isinstance(item.get("counterEvidence"), list)
    )
    statement_count = len(statements) if isinstance(statements, list) else 0
    incomplete_statements = [
        str(index)
        for index, item in enumerate(statements if isinstance(statements, list) else [])
        if not isinstance(item, dict) or not item.get("ruleIds") or not item.get("riskBoundary")
    ]
    report_refs, report_broken_refs = _validate_api_report_refs(
        client=client,
        capability_id=capability_id,
        payload=payload,
        classics_ids=classics_ids,
    )
    broken_refs.extend(report_broken_refs)

    return {
        "status": "passed",
        "sample": {
            "name": payload["name"],
            "birthPlace": "北京测试样本",
        },
        "evidenceItems": {
            "count": len(items),
            "completeCount": complete_count,
            "completeRatio": _ratio(complete_count, len(items)),
            "evidenceItemIds": sorted(items.keys()),
            "incompleteItems": incomplete_items,
        },
        "ruleDepth": {
            "appliedRuleCount": len(applied_rules) if isinstance(applied_rules, list) else 0,
            "incompleteAppliedRules": incomplete_applied_rules,
            "conflictCount": conflict_count,
            "conflictExplanationRatio": _ratio(conflict_explanation_count, conflict_count),
            "conflictCounterEvidenceRatio": _ratio(conflict_counter_evidence_count, conflict_count),
            "combinationStatementCount": statement_count,
            "incompleteCombinationStatements": incomplete_statements,
        },
        "reportEvidenceRefs": report_refs,
        "brokenRuleRefs": broken_refs,
    }


def _append_finding(findings: list[dict[str, Any]], *, scope: str, metric: str, actual: Any, expected: Any) -> None:
    findings.append({"scope": scope, "metric": metric, "actual": actual, "expected": expected})


def _compare_with_baseline(
    *,
    baseline: dict[str, Any],
    registry: dict[str, Any],
    capabilities: dict[str, dict[str, Any]],
    broken_rule_refs: list[dict[str, str]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    registry_min = baseline["registryMinimums"]
    if int(registry["totalRules"]) < int(registry_min["totalRules"]):
        _append_finding(
            findings,
            scope="registry",
            metric="totalRules",
            actual=registry["totalRules"],
            expected=registry_min["totalRules"],
        )
    for system, expected in registry_min["rulesBySystem"].items():
        actual = int(registry["rulesBySystem"].get(system, 0))
        if actual < int(expected):
            _append_finding(
                findings, scope=f"registry.{system}", metric="rulesBySystem", actual=actual, expected=expected
            )

    for capability_id, minimums in baseline["capabilityMinimums"].items():
        actual = capabilities[capability_id]
        required_items = set(minimums.get("requiredEvidenceItems", []))
        missing_required = sorted(required_items - set(_evidence_item_ids(actual)))
        if missing_required:
            _append_finding(
                findings,
                scope=capability_id,
                metric="requiredEvidenceItems",
                actual=missing_required,
                expected=sorted(required_items),
            )
        checks = (
            ("minEvidenceItems", actual["evidenceItems"]["count"]),
            ("minReportEvidenceRefs", actual["reportEvidenceRefs"]["count"]),
            ("minAppliedRules", actual["ruleDepth"]["appliedRuleCount"]),
            ("minConflicts", actual["ruleDepth"]["conflictCount"]),
            ("minCombinationStatements", actual["ruleDepth"]["combinationStatementCount"]),
        )
        for key, value in checks:
            if int(value) < int(minimums[key]):
                _append_finding(findings, scope=capability_id, metric=key, actual=value, expected=minimums[key])
        ratio_checks = (
            ("minTraceCompletenessRatio", actual["evidenceItems"]["completeRatio"]),
            ("minReportEvidenceRefCompletenessRatio", actual["reportEvidenceRefs"]["completeRatio"]),
            ("minConflictExplanationRatio", actual["ruleDepth"]["conflictExplanationRatio"]),
            ("minConflictCounterEvidenceRatio", actual["ruleDepth"]["conflictCounterEvidenceRatio"]),
        )
        for key, value in ratio_checks:
            if float(value) < float(minimums[key]):
                _append_finding(findings, scope=capability_id, metric=key, actual=value, expected=minimums[key])
        if actual["ruleDepth"]["incompleteAppliedRules"]:
            _append_finding(
                findings,
                scope=capability_id,
                metric="incompleteAppliedRules",
                actual=actual["ruleDepth"]["incompleteAppliedRules"],
                expected=[],
            )
        if actual["ruleDepth"]["incompleteCombinationStatements"]:
            _append_finding(
                findings,
                scope=capability_id,
                metric="incompleteCombinationStatements",
                actual=actual["ruleDepth"]["incompleteCombinationStatements"],
                expected=[],
            )
    if len(broken_rule_refs) > int(baseline["maxBrokenRuleRefs"]):
        _append_finding(
            findings,
            scope="ruleRefs",
            metric="brokenRuleRefs",
            actual=len(broken_rule_refs),
            expected=baseline["maxBrokenRuleRefs"],
        )
    return findings


def _evidence_item_ids(capability_summary: dict[str, Any]) -> list[str]:
    # 只把字段名摘要输出，不复制 evidence item 内容。
    return list(capability_summary.get("evidenceItems", {}).get("evidenceItemIds", []))


def _assert_no_forbidden_fragments(summary: dict[str, Any], forbidden_fragments: list[str]) -> None:
    payload = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    hits = [fragment for fragment in forbidden_fragments if fragment and fragment in payload]
    if hits:
        joined = ", ".join(hits)
        raise EvidenceCoverageTrendGateError(f"summary contains forbidden fragments: {joined}")


def run_gate(*, baseline_path: Path = DEFAULT_BASELINE) -> dict[str, Any]:
    baseline = _load_json(baseline_path)
    contract = _load_json(DEFAULT_CONTRACT)
    classics_ids = _classics_rule_ids()
    registry = _validate_registry(classics_ids)
    registry_rule_ids = set(registry["ruleIds"])

    CapabilityExecutor, CapabilityInput, TestClient, app = _load_runtime()
    executor = CapabilityExecutor()
    client = TestClient(app)
    capabilities = {
        capability_id: _validate_capability(
            capability_id=capability_id,
            executor=executor,
            CapabilityInput=CapabilityInput,
            client=client,
            registry_rule_ids=registry_rule_ids,
            classics_ids=classics_ids,
        )
        for capability_id in ("bazi", "ziwei")
    }

    broken_rule_refs = list(registry["brokenRuleRefs"])
    for summary in capabilities.values():
        broken_rule_refs.extend(summary["brokenRuleRefs"])
    trend_findings = _compare_with_baseline(
        baseline=baseline,
        registry=registry,
        capabilities=capabilities,
        broken_rule_refs=broken_rule_refs,
    )
    status = "failed" if trend_findings else "passed"
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.evidence_coverage_trend_gate",
        "generatedAt": _utc_now(),
        "status": status,
        "baseline": {
            "path": _rel(baseline_path),
            "id": baseline.get("id"),
        },
        "contract": _rel(DEFAULT_CONTRACT),
        "registry": {key: value for key, value in registry.items() if key != "ruleIds"},
        "capabilities": capabilities,
        "trendFindings": trend_findings,
        "brokenRuleRefs": broken_rule_refs,
        "summary": {
            "capabilityCount": len(capabilities),
            "totalEvidenceItems": sum(item["evidenceItems"]["count"] for item in capabilities.values()),
            "totalReportEvidenceRefs": sum(item["reportEvidenceRefs"]["count"] for item in capabilities.values()),
            "totalAppliedRules": sum(item["ruleDepth"]["appliedRuleCount"] for item in capabilities.values()),
            "totalConflicts": sum(item["ruleDepth"]["conflictCount"] for item in capabilities.values()),
            "totalBrokenRuleRefs": len(broken_rule_refs),
        },
        "privacyBoundary": contract["privacyBoundary"],
        "productionBoundary": contract["productionBoundary"],
    }
    _assert_no_forbidden_fragments(summary, contract.get("forbiddenReportFragments", []))
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行八字/紫微 evidence coverage trend gate。")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE, help="evidence coverage baseline JSON.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary output JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(baseline_path=args.baseline)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "capabilities": summary["summary"]["capabilityCount"],
                    "evidenceItems": summary["summary"]["totalEvidenceItems"],
                    "reportEvidenceRefs": summary["summary"]["totalReportEvidenceRefs"],
                    "trendFindings": len(summary["trendFindings"]),
                    "brokenRuleRefs": len(summary["brokenRuleRefs"]),
                },
                ensure_ascii=False,
            )
        )
        return 0 if summary["status"] == "passed" else 1
    except (EvidenceCoverageTrendGateError, OSError, json.JSONDecodeError) as exc:
        print(f"evidence coverage trend gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
