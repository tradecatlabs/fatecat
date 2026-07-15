from __future__ import annotations

from typing import Any

from fate_core.usecases.evaluators.relation import condition, relation_blockers
from fate_core.usecases.rule_depth import rules_for_system

REGULAR_PATTERN_TEN_GODS = {"正官", "七杀", "正印", "偏印", "食神", "伤官", "正财", "偏财"}


def pattern_matrix_contracts() -> dict[str, dict[str, Any]]:
    rule = next(
        (item for item in rules_for_system("bazi") if item.get("id") == "bazi.depth.pattern.regular_vs_special"), {}
    )
    matrix = rule.get("patternMatrix", []) if isinstance(rule, dict) else []
    return {str(item.get("name")): item for item in matrix if isinstance(item, dict)}


def _regular_pattern_status(score: int, blockers: list[str], transparent: bool) -> str:
    if score >= 85 and transparent and not blockers:
        return "established"
    if score >= 70:
        return "candidate"
    if score >= 40:
        return "uncertain"
    return "not_supported"


def build_regular_pattern_candidates(raw: dict[str, Any]) -> dict[str, Any]:
    """生成财官印食等常规格局候选；证据不足时只输出 uncertainty。"""
    ten_gods = raw.get("tenGods", {}) if isinstance(raw.get("tenGods"), dict) else {}
    hidden_stems = raw.get("hiddenStems", {}) if isinstance(raw.get("hiddenStems"), dict) else {}
    month_ten_gods = ten_gods.get("month", {}) if isinstance(ten_gods.get("month"), dict) else {}
    month_branch_ten_gods = month_ten_gods.get("branch", [])
    if not isinstance(month_branch_ten_gods, list):
        month_branch_ten_gods = [month_branch_ten_gods]
    month_hidden_stems = hidden_stems.get("month", [])
    if not isinstance(month_hidden_stems, list):
        month_hidden_stems = [month_hidden_stems]
    stem_ten_gods = {
        str(section.get("stem"))
        for section in ten_gods.values()
        if isinstance(section, dict) and section.get("stem") not in (None, "")
    }
    blockers = relation_blockers(raw, {"month"})
    candidates: list[dict[str, Any]] = []
    for index, ten_god in enumerate(month_branch_ten_gods):
        if ten_god not in REGULAR_PATTERN_TEN_GODS:
            continue
        hidden_stem = str(month_hidden_stems[index]) if index < len(month_hidden_stems) else ""
        transparent = ten_god in stem_ten_gods
        score = 45
        if hidden_stem:
            score += 20
        if transparent:
            score += 25
        if blockers:
            score -= 20
        status = _regular_pattern_status(score, blockers, transparent)
        uncertainty = []
        if not transparent:
            uncertainty.append("月令十神未透干，不能直接定格。")
        if blockers:
            uncertainty.append("月令相关合冲刑害破或克战存在，需进入破格审查。")
        if status == "uncertain" and not uncertainty:
            uncertainty.append("候选证据不足，保持 uncertainty。")
        candidates.append(
            {
                "name": f"{ten_god}格",
                "sourceTenGod": ten_god,
                "hiddenStem": hidden_stem,
                "score": max(0, min(100, score)),
                "status": status,
                "sourceRuleId": "bazi.pattern_by_month_command",
                "evidenceFields": [
                    f"tenGods.month.branch[{index}]",
                    f"hiddenStems.month[{index}]",
                    "tenGods.*.stem",
                    "branchRelations.canonical",
                ],
                "conditions": [
                    condition("month_branch_ten_god_present", True, ten_god),
                    condition("month_hidden_stem_present", bool(hidden_stem), hidden_stem),
                    condition("ten_god_transparent_in_heavenly_stems", transparent, sorted(stem_ten_gods)),
                    condition("no_month_relation_blocker", not blockers, blockers),
                ],
                "breaksWhen": [
                    "月令不清或节气边界未验证",
                    "透干、通根或藏干证据不足",
                    "月令被合冲刑害破改变取格依据但无证据链",
                    "特殊格局完整成立并有 golden 验证",
                ],
                "uncertainty": uncertainty,
                "riskBoundary": "常规格局只作为解释优先级；证据不足时必须输出 uncertainty，不得强断。",
            }
        )
    primary = max(candidates, key=lambda item: item["score"], default=None)
    return {
        "schemaVersion": 1,
        "primaryCandidate": primary if primary and primary["status"] == "established" else None,
        "candidates": candidates,
        "status": "has_candidates" if candidates else "no_regular_candidate",
        "uncertaintyPolicy": "未达到 established 的候选必须保留 uncertainty 与 breaksWhen，不写成定格。",
        "riskBoundary": "财官印食等正格候选必须回到月令、透干、藏干和破格条件，不输出确定人生断语。",
    }
