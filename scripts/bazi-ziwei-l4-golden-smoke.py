#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DATA_ROOT = REPO_ROOT / "domains" / "fate-analysis" / "data-products"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "golden" / "bazi-ziwei-l4.json"

BAZI_MATRIX = DATA_ROOT / "bazi" / "golden" / "coverage_matrix_cases.json"
BAZI_RULE_DEPTH = DATA_ROOT / "bazi" / "golden" / "rule_depth_cases.json"
BAZI_STATEMENTS = DATA_ROOT / "bazi" / "golden" / "statement_cases.json"
ZIWEI_CASES = DATA_ROOT / "ziwei" / "golden" / "cases.json"
ZIWEI_RULE_DEPTH = DATA_ROOT / "ziwei" / "golden" / "rule_depth_cases.json"
PROFILES = ("quick", "full")
QUICK_BAZI_MATRIX_TAGS = (
    "solar_term_boundary",
    "zi_time_boundary",
    "follow_pattern_guard",
    "special_pattern_guard",
    "season_summer",
)
QUICK_RULE_DEPTH_LIMIT = 2
QUICK_STATEMENT_LIMIT = 1
QUICK_ZIWEI_LIMIT = 1


class L4GoldenSmokeError(RuntimeError):
    """八字/紫微 L4 golden smoke 未满足预期。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from fastapi.testclient import TestClient  # noqa: PLC0415

    from fate_core.capabilities import CapabilityExecutor, CapabilityInput  # noqa: PLC0415
    from main import app  # noqa: PLC0415

    return CapabilityExecutor, CapabilityInput, TestClient, app


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise L4GoldenSmokeError(f"{name}: {details}")


def _pillar_names(result: dict[str, Any]) -> dict[str, str]:
    return {name: result["fourPillars"][name]["fullName"] for name in ["year", "month", "day", "hour"]}


def _limited_cases(cases: list[dict[str, Any]], profile: str, quick_limit: int) -> list[dict[str, Any]]:
    if profile == "full":
        return cases
    return cases[:quick_limit]


def _selected_bazi_matrix_cases(fixture: dict[str, Any], profile: str) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    tags = fixture["coverageRequirements"]["requiredTags"] if profile == "full" else QUICK_BAZI_MATRIX_TAGS
    for tag in sorted(tags):
        case = next((item for item in fixture["cases"] if tag in item["coverageTags"]), None)
        if case is None:
            raise L4GoldenSmokeError(f"missing bazi matrix tag: {tag}")
        selected[case["id"]] = case
    return list(selected.values())


def _rule_ids_from_applied(depth: dict[str, Any]) -> set[str]:
    return {str(item.get("ruleId")) for item in depth.get("appliedRules", []) if item.get("ruleId")}


def _topics_from_statements(depth: dict[str, Any]) -> set[str]:
    return {str(item.get("topic")) for item in depth.get("combinationStatements", []) if item.get("topic")}


def _run_capability(executor: Any, CapabilityInput: Any, capability_id: str, payload: dict[str, Any]) -> Any:
    return executor.execute(CapabilityInput(capability_id=capability_id, payload=payload))


def _check_bazi_matrix(
    *,
    executor: Any,
    CapabilityInput: Any,
    checks: list[dict[str, Any]],
    profile: str,
) -> dict[str, Any]:
    fixture = _load_json(BAZI_MATRIX)
    cases = fixture["cases"]
    required_tags = set(fixture["coverageRequirements"]["requiredTags"])
    observed_tags = {tag for case in cases for tag in case["coverageTags"]}
    _check(checks, "bazi_matrix:min_case_count", len(cases) >= 300, str(len(cases)))
    _check(
        checks, "bazi_matrix:required_tags", required_tags <= observed_tags, str(sorted(required_tags - observed_tags))
    )
    _check(
        checks,
        "bazi_matrix:privacy",
        all(case["input"]["birthPlace"] == "北京" for case in cases),
        "all fixture places are 北京",
    )

    selected = _selected_bazi_matrix_cases(fixture, profile)
    passed_ids: list[str] = []
    for case in selected:
        result = _run_capability(executor, CapabilityInput, "bazi", case["input"]).data
        expected = case["expected"]
        _check(checks, f"bazi_matrix:{case['id']}:pillars", _pillar_names(result) == expected["fourPillars"], "match")
        _check(
            checks,
            f"bazi_matrix:{case['id']}:day_stem",
            result["dayMaster"]["stem"] == expected["dayStem"],
            result["dayMaster"]["stem"],
        )
        _check(
            checks,
            f"bazi_matrix:{case['id']}:fortune_start",
            result["jiaoYun"]["startDate"] == expected["fortuneStart"]["startDate"],
            result["jiaoYun"]["startDate"],
        )
        _check(
            checks,
            f"bazi_matrix:{case['id']}:rule_depth",
            bool(result["baziRuleDepth"]["appliedRules"]),
            "appliedRules present",
        )
        passed_ids.append(case["id"])

    return {
        "fixture": BAZI_MATRIX.relative_to(REPO_ROOT).as_posix(),
        "caseCount": len(cases),
        "availableCaseCount": len(cases),
        "executedCaseCount": len(selected),
        "requiredTagCount": len(required_tags),
        "representativeCaseCount": len(selected),
        "passedRepresentativeIds": passed_ids,
    }


def _check_bazi_rule_depth(
    *,
    executor: Any,
    CapabilityInput: Any,
    checks: list[dict[str, Any]],
    profile: str,
) -> dict[str, Any]:
    fixture = _load_json(BAZI_RULE_DEPTH)
    selected = _limited_cases(fixture["cases"], profile, QUICK_RULE_DEPTH_LIMIT)
    passed_ids: list[str] = []
    for case in selected:
        result = _run_capability(executor, CapabilityInput, "bazi", case["input"]).data
        expected = case["expected"]
        depth = result["baziRuleDepth"]
        emitted = _rule_ids_from_applied(depth)
        topics = _topics_from_statements(depth)
        _check(checks, f"bazi_depth:{case['id']}:pillars", _pillar_names(result) == expected["fourPillars"], "match")
        _check(
            checks,
            f"bazi_depth:{case['id']}:strength",
            result["dayMaster"]["strength"] == expected["dayMasterStrength"],
            result["dayMaster"]["strength"],
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:geju",
            result["geju"]["main"] == expected["gejuMain"],
            result["geju"]["main"],
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:applied_count",
            len(depth["appliedRules"]) >= int(expected["appliedRuleCountMin"]),
            str(len(depth["appliedRules"])),
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:required_rules",
            set(expected["requiredRuleIds"]) <= emitted,
            str(sorted(set(expected["requiredRuleIds"]) - emitted)),
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:confidence",
            float(depth["weightProfile"]["weightedConfidence"]) >= float(expected["weightedConfidenceMin"]),
            str(depth["weightProfile"]["weightedConfidence"]),
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:combination_topics",
            set(expected["combinationTopics"]) <= topics,
            str(sorted(set(expected["combinationTopics"]) - topics)),
        )
        _check(
            checks,
            f"bazi_depth:{case['id']}:conflict_explanations",
            all(
                item.get("explanation") and item.get("counterEvidence") is not None
                for item in depth["conflictResolution"]["conflicts"]
            ),
            "conflicts include explanation and counterEvidence",
        )
        passed_ids.append(case["id"])

    return {
        "fixture": BAZI_RULE_DEPTH.relative_to(REPO_ROOT).as_posix(),
        "caseCount": len(fixture["cases"]),
        "availableCaseCount": len(fixture["cases"]),
        "executedCaseCount": len(selected),
        "passedIds": passed_ids,
    }


def _check_bazi_statement_cases(
    *,
    executor: Any,
    CapabilityInput: Any,
    checks: list[dict[str, Any]],
    profile: str,
) -> dict[str, Any]:
    fixture = _load_json(BAZI_STATEMENTS)
    selected = _limited_cases(fixture["cases"], profile, QUICK_STATEMENT_LIMIT)
    passed_ids: list[str] = []
    for case in selected:
        result = _run_capability(executor, CapabilityInput, "bazi", case["input"]).data
        expected = case["expected"]
        _check(
            checks, f"bazi_statement:{case['id']}:pillars", _pillar_names(result) == expected["fourPillars"], "match"
        )
        _check(
            checks,
            f"bazi_statement:{case['id']}:day_master",
            result["dayMaster"]["stem"] == expected["dayMaster"]["stem"],
            result["dayMaster"]["stem"],
        )
        _check(
            checks,
            f"bazi_statement:{case['id']}:geju",
            result["geju"]["main"] == expected["gejuMain"],
            result["geju"]["main"],
        )
        emitted = {
            rule_id for item in result["analysisEvidence"]["items"].values() for rule_id in item.get("ruleIds", [])
        }
        _check(
            checks,
            f"bazi_statement:{case['id']}:accuracy_rules",
            set(expected["accuracyRuleIds"]) <= emitted,
            str(sorted(set(expected["accuracyRuleIds"]) - emitted)),
        )
        passed_ids.append(case["id"])

    return {
        "fixture": BAZI_STATEMENTS.relative_to(REPO_ROOT).as_posix(),
        "caseCount": len(fixture["cases"]),
        "availableCaseCount": len(fixture["cases"]),
        "executedCaseCount": len(selected),
        "passedIds": passed_ids,
    }


def _check_ziwei_cases(
    *,
    executor: Any,
    CapabilityInput: Any,
    checks: list[dict[str, Any]],
    profile: str,
) -> dict[str, Any]:
    fixture = _load_json(ZIWEI_CASES)
    selected = _limited_cases(fixture["cases"], profile, QUICK_ZIWEI_LIMIT)
    passed_ids: list[str] = []
    for case in selected:
        result = _run_capability(executor, CapabilityInput, "ziwei", case["input"]).data
        expected = case["expected"]
        guards = result["ziweiGoldenGuards"]
        _check(
            checks,
            f"ziwei_case:{case['id']}:palace_count",
            guards["palaceCount"] == expected["palaceCount"],
            str(guards["palaceCount"]),
        )
        _check(checks, f"ziwei_case:{case['id']}:life_palace", guards["lifePalace"] == expected["lifePalace"], "match")
        _check(checks, f"ziwei_case:{case['id']}:body_palace", guards["bodyPalace"] == expected["bodyPalace"], "match")
        _check(
            checks,
            f"ziwei_case:{case['id']}:mutagen_count",
            guards["mutagenPlacementCount"] == expected["mutagenPlacementCount"],
            str(guards["mutagenPlacementCount"]),
        )
        _check(
            checks,
            f"ziwei_case:{case['id']}:fortune_link_count",
            guards["fortuneLinkCount"] == expected["fortuneLinkCount"],
            str(guards["fortuneLinkCount"]),
        )
        emitted = set(result["analysisEvidence"]["items"]["benchmarkHardening"]["ruleIds"])
        _check(
            checks,
            f"ziwei_case:{case['id']}:required_rules",
            set(expected["requiredRuleIds"]) <= emitted,
            str(sorted(set(expected["requiredRuleIds"]) - emitted)),
        )
        passed_ids.append(case["id"])

    return {
        "fixture": ZIWEI_CASES.relative_to(REPO_ROOT).as_posix(),
        "caseCount": len(fixture["cases"]),
        "availableCaseCount": len(fixture["cases"]),
        "executedCaseCount": len(selected),
        "passedIds": passed_ids,
    }


def _check_ziwei_rule_depth(
    *,
    executor: Any,
    CapabilityInput: Any,
    checks: list[dict[str, Any]],
    profile: str,
) -> dict[str, Any]:
    fixture = _load_json(ZIWEI_RULE_DEPTH)
    selected = _limited_cases(fixture["cases"], profile, QUICK_RULE_DEPTH_LIMIT)
    passed_ids: list[str] = []
    for case in selected:
        result = _run_capability(executor, CapabilityInput, "ziwei", case["input"]).data
        expected = case["expected"]
        depth = result["ziweiRuleDepth"]
        emitted = _rule_ids_from_applied(depth)
        topics = _topics_from_statements(depth)
        guards = result["ziweiGoldenGuards"]
        _check(checks, f"ziwei_depth:{case['id']}:life_palace", guards["lifePalace"] == expected["lifePalace"], "match")
        _check(checks, f"ziwei_depth:{case['id']}:body_palace", guards["bodyPalace"] == expected["bodyPalace"], "match")
        _check(
            checks,
            f"ziwei_depth:{case['id']}:applied_count",
            len(depth["appliedRules"]) >= int(expected["appliedRuleCountMin"]),
            str(len(depth["appliedRules"])),
        )
        _check(
            checks,
            f"ziwei_depth:{case['id']}:required_rules",
            set(expected["requiredRuleIds"]) <= emitted,
            str(sorted(set(expected["requiredRuleIds"]) - emitted)),
        )
        _check(
            checks,
            f"ziwei_depth:{case['id']}:confidence",
            float(depth["weightProfile"]["weightedConfidence"]) >= float(expected["weightedConfidenceMin"]),
            str(depth["weightProfile"]["weightedConfidence"]),
        )
        _check(
            checks,
            f"ziwei_depth:{case['id']}:combination_topics",
            set(expected["combinationTopics"]) <= topics,
            str(sorted(set(expected["combinationTopics"]) - topics)),
        )
        _check(
            checks,
            f"ziwei_depth:{case['id']}:conflict_explanations",
            all(
                item.get("explanation") and item.get("counterEvidence") is not None
                for item in depth["conflictResolution"]["conflicts"]
            ),
            "conflicts include explanation and counterEvidence",
        )
        passed_ids.append(case["id"])

    return {
        "fixture": ZIWEI_RULE_DEPTH.relative_to(REPO_ROOT).as_posix(),
        "caseCount": len(fixture["cases"]),
        "availableCaseCount": len(fixture["cases"]),
        "executedCaseCount": len(selected),
        "passedIds": passed_ids,
    }


def _check_markdown_profiles(*, TestClient: Any, app: Any, checks: list[dict[str, Any]]) -> dict[str, Any]:
    client = TestClient(app)
    payload = {
        "name": "测试样本",
        "gender": "male",
        "birthDate": "1990-01-01",
        "birthTime": "08:00:00",
        "birthPlace": {
            "name": "北京市",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "timezone": "Asia/Shanghai",
        },
        "options": {
            "useTrueSolarTime": True,
            "daylightSaving": "auto",
            "midnightMode": "early",
            "calendarType": "solar",
        },
    }
    summaries: dict[str, Any] = {}
    for report_system in ("bazi", "ziwei"):
        body = copy.deepcopy(payload)
        body["options"]["reportSystem"] = report_system
        response = client.post("/api/v1/report/markdown", json=body)
        _check(checks, f"markdown:{report_system}:status_code", response.status_code == 200, str(response.status_code))
        data = response.json()["data"]
        _check(
            checks,
            f"markdown:{report_system}:policy_gate",
            data["policyGate"]["status"] == "pass",
            data["policyGate"]["status"],
        )
        _check(
            checks,
            f"markdown:{report_system}:snapshot_gate",
            data["snapshotGate"]["status"] == "pass",
            data["snapshotGate"]["status"],
        )
        summaries[report_system] = {
            "policyGate": data["policyGate"]["status"],
            "snapshotGate": data["snapshotGate"]["status"],
            "headingCount": data["snapshotGate"]["headingCount"],
            "requiredHeadings": data["snapshotGate"]["requiredHeadings"],
        }
    return summaries


def run_smoke(profile: str = "quick") -> dict[str, Any]:
    if profile not in PROFILES:
        raise L4GoldenSmokeError(f"unsupported profile: {profile}")

    CapabilityExecutor, CapabilityInput, TestClient, app = _load_runtime()
    executor = CapabilityExecutor()
    checks: list[dict[str, Any]] = []
    started = time.perf_counter()

    bazi_matrix = _check_bazi_matrix(executor=executor, CapabilityInput=CapabilityInput, checks=checks, profile=profile)
    bazi_depth = _check_bazi_rule_depth(
        executor=executor, CapabilityInput=CapabilityInput, checks=checks, profile=profile
    )
    bazi_statements = _check_bazi_statement_cases(
        executor=executor, CapabilityInput=CapabilityInput, checks=checks, profile=profile
    )
    ziwei_cases = _check_ziwei_cases(executor=executor, CapabilityInput=CapabilityInput, checks=checks, profile=profile)
    ziwei_depth = _check_ziwei_rule_depth(
        executor=executor, CapabilityInput=CapabilityInput, checks=checks, profile=profile
    )
    markdown_profiles = _check_markdown_profiles(TestClient=TestClient, app=app, checks=checks)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "profile": profile,
        "smokeScope": "bazi_ziwei_l4_golden_evidence_baseline",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "summary": {
            "baziMatrix": bazi_matrix,
            "baziRuleDepth": bazi_depth,
            "baziStatements": bazi_statements,
            "ziweiCases": ziwei_cases,
            "ziweiRuleDepth": ziwei_depth,
            "markdownProfiles": markdown_profiles,
        },
        "checks": checks,
        "privacyBoundary": "L4 golden smoke 只读取项目内匿名 synthetic fixtures 和北京/测试样本，不读取真实用户、真实非北京地区、token、secret、DSN 或生产环境。",
        "limits": [
            "不锁定完整断语正文。",
            "不新增真实命例。",
            "不宣称八字/紫微专业能力 100%。",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行八字/紫微 L4 golden evidence smoke，并输出机器可读 JSON。")
    parser.add_argument(
        "--profile", choices=PROFILES, default="quick", help="quick 只跑代表样本；full 跑当前 golden fixture 全量样本。"
    )
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke(args.profile)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "profile": summary["profile"],
                    "checks": len(summary["checks"]),
                    "elapsedMs": summary["elapsedMs"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except L4GoldenSmokeError as exc:
        print(f"bazi/ziwei L4 golden smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
