from __future__ import annotations

from typing import Any

from fate_core.usecases.evaluators.relation import build_relation_order


def five_element_spread(raw: dict[str, Any]) -> int:
    scores = (
        raw.get("wuxingScores", {}).get("fiveElementScore", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    )
    values = [int(value) for value in scores.values() if isinstance(value, int | float)]
    return max(values) - min(values) if values else 0


def temperature_band(climate_scores: Any) -> str:
    if not isinstance(climate_scores, dict):
        return "unknown"
    score = climate_scores.get("temperatureScore")
    if not isinstance(score, int | float):
        return "unknown"
    if score <= -7:
        return "cold_wet_bias"
    if score >= 7:
        return "hot_dry_bias"
    return "balanced_range"


def build_yongshen_decision(raw: dict[str, Any], strategies: list[dict[str, Any]]) -> dict[str, Any]:
    strategy_names = {str(item.get("strategy")): item for item in strategies if isinstance(item, dict)}
    relation_count = sum(
        item.get("count", 0) for item in build_relation_order(raw) if isinstance(item.get("count"), int)
    )
    spread = five_element_spread(raw)
    climate_band = temperature_band(raw.get("climateScores", {}))
    strength = raw.get("wuxingScores", {}) if isinstance(raw.get("wuxingScores"), dict) else {}
    yong_shen = raw.get("yongShen", {}) if isinstance(raw.get("yongShen"), dict) else {}
    strategy_contracts = {
        "调候": {
            "appliesWhen": ["月令、节气、寒暖燥湿、调候原始依据存在"],
            "doesNotApplyWhen": ["缺少季节气候依据", "把调候当作医疗/养生处方"],
            "conflictPolicy": "调候优先解释气候偏性，但不得覆盖扶抑、通关、病药。",
        },
        "扶抑": {
            "appliesWhen": ["日主强弱、月令、通根、透干、五行分数齐备"],
            "doesNotApplyWhen": ["只存在单一强弱标签", "五行分数或藏干缺失"],
            "conflictPolicy": "扶抑与调候冲突时并列呈现，不能单独覆盖用神。",
        },
        "通关": {
            "appliesWhen": ["干支冲合刑害破或五行克战关系显著", "存在可缓冲的中介五行"],
            "doesNotApplyWhen": ["关系链不可追溯", "只有单点五行偏枯而无冲突链"],
            "conflictPolicy": "通关只解释冲突缓冲，不替代调候或扶抑主策略。",
        },
        "病药": {
            "appliesWhen": ["五行偏枯、寒暖燥湿或格局病处可定位", "存在对应药处证据"],
            "doesNotApplyWhen": ["偏枯不明显", "病处无法回指证据字段", "输出生活处方"],
            "conflictPolicy": "病药作为解释优先级，不输出现实诊疗、金融或法律决策。",
        },
    }
    score_basis = {
        "调候": [
            {"factor": "base", "value": 35, "evidenceField": "yongShen.defaultBase"},
            {"factor": "调候表依据", "value": 25 if yong_shen.get("basis") else 0, "evidenceField": "yongShen.basis"},
            {
                "factor": "调候原始规则",
                "value": 20 if yong_shen.get("tiaohouRaw") else 0,
                "evidenceField": "yongShen.tiaohouRaw",
            },
        ],
        "扶抑": [
            {"factor": "base", "value": 35, "evidenceField": "yongShen.defaultBase"},
            {
                "factor": "强弱分数",
                "value": 25 if strength.get("strongScore") is not None else 0,
                "evidenceField": "wuxingScores.strongScore",
            },
            {
                "factor": "强弱细节",
                "value": 15 if strength.get("statusDetail") else 0,
                "evidenceField": "wuxingScores.statusDetail",
            },
        ],
        "通关": [
            {"factor": "base", "value": 25, "evidenceField": "yongShen.defaultBase"},
            {"factor": "干支关系数量", "value": relation_count * 8, "evidenceField": "baziBenchmark.ganzhiPriority"},
        ],
        "病药": [
            {"factor": "base", "value": 25, "evidenceField": "yongShen.defaultBase"},
            {"factor": "五行偏枯跨度", "value": spread * 3, "evidenceField": "wuxingScores.fiveElementScore"},
            {
                "factor": "寒暖燥湿偏性",
                "value": 15 if climate_band != "balanced_range" else 0,
                "evidenceField": "climateScores",
            },
        ],
    }
    scored = [
        {
            "strategy": "调候",
            "score": min(100, 35 + (25 if yong_shen.get("basis") else 0) + (20 if yong_shen.get("tiaohouRaw") else 0)),
            "basis": {
                "summary": "以月令、节气和寒暖燥湿解释调候优先级。",
                "sourceBasis": strategy_names.get("调候", {}).get("basis", ""),
                "climateBand": climate_band,
            },
            "scoreBasis": score_basis["调候"],
            "evidenceFields": ["yongShen.basis", "yongShen.tiaohouRaw", "climateScores"],
            "source": strategy_names.get("调候", {}).get("source", ""),
        },
        {
            "strategy": "扶抑",
            "score": min(
                100,
                35
                + (25 if strength.get("strongScore") is not None else 0)
                + (15 if strength.get("statusDetail") else 0),
            ),
            "basis": {
                "summary": "以日主强弱、月令、通根、透干和五行分数判断扶抑取向。",
                "sourceBasis": strategy_names.get("扶抑", {}).get("basis", ""),
                "strengthLabel": raw.get("dayMaster", {}).get("strength")
                if isinstance(raw.get("dayMaster"), dict)
                else "",
            },
            "scoreBasis": score_basis["扶抑"],
            "evidenceFields": ["dayMaster.strength", "wuxingScores.strongScore", "wuxingScores.statusDetail"],
            "source": strategy_names.get("扶抑", {}).get("source", ""),
        },
        {
            "strategy": "通关",
            "score": min(100, 25 + relation_count * 8),
            "basis": {
                "summary": "以干支冲合刑害破和五行克战链判断是否需要通关缓冲。",
                "relationCount": relation_count,
                "sourceBasis": strategy_names.get("通关", {}).get("basis", {}),
            },
            "scoreBasis": score_basis["通关"],
            "evidenceFields": [
                "ganzhiRelations.tianGan",
                "branchRelations.canonical",
                "baziBenchmark.ganzhiPriority",
            ],
            "source": strategy_names.get("通关", {}).get("source", ""),
        },
        {
            "strategy": "病药",
            "score": min(100, 25 + spread * 3 + (15 if climate_band != "balanced_range" else 0)),
            "basis": {
                "summary": "以五行偏枯、寒暖燥湿和格局病处定位病药解释。",
                "fiveElementSpread": spread,
                "climateBand": climate_band,
                "sourceBasis": strategy_names.get("病药", {}).get("basis", {}),
            },
            "scoreBasis": score_basis["病药"],
            "evidenceFields": ["wuxingScores.fiveElementScore", "climateScores", "geju"],
            "source": strategy_names.get("病药", {}).get("source", ""),
        },
    ]
    for item in scored:
        item.update(strategy_contracts[item["strategy"]])
    scored.sort(key=lambda item: item["score"], reverse=True)
    top_score = int(scored[0]["score"]) if scored else 0
    selection_threshold = max(45, top_score - 15)
    selected_candidates = [
        {
            "strategy": item["strategy"],
            "score": item["score"],
            "tier": "primary" if index == 0 else "parallel_review",
            "selectionReason": "score_within_parallel_threshold"
            if item["score"] >= selection_threshold
            else "retained_for_boundary",
            "evidenceFields": item["evidenceFields"],
        }
        for index, item in enumerate(scored)
        if item["score"] >= selection_threshold
    ]
    if len(selected_candidates) == 1 and len(scored) > 1:
        item = scored[1]
        selected_candidates.append(
            {
                "strategy": item["strategy"],
                "score": item["score"],
                "tier": "parallel_review",
                "selectionReason": "non_absolute_secondary_strategy_retained",
                "evidenceFields": item["evidenceFields"],
            }
        )

    conflicts = []
    if len(scored) > 1:
        second = scored[1]
        delta = top_score - int(second["score"])
        conflicts.append(
            {
                "type": "strategy_ranking_delta",
                "severity": "medium" if delta <= 15 else "low",
                "strategies": [scored[0]["strategy"], second["strategy"]],
                "delta": delta,
                "explanation": "最高分策略与次高分策略按证据完整度排序，但次级策略仍保留为并列解释边界。",
                "counterEvidence": second["doesNotApplyWhen"],
            }
        )
    score_by_strategy = {str(item["strategy"]): int(item["score"]) for item in scored}
    if "调候" in score_by_strategy and "扶抑" in score_by_strategy:
        conflicts.append(
            {
                "type": "climate_vs_strength",
                "severity": "medium" if abs(score_by_strategy["调候"] - score_by_strategy["扶抑"]) <= 15 else "low",
                "strategies": ["调候", "扶抑"],
                "delta": abs(score_by_strategy["调候"] - score_by_strategy["扶抑"]),
                "explanation": "调候解释季节气候，扶抑解释日主强弱；两者冲突时只排序，不互相覆盖。",
                "counterEvidence": list(strategy_contracts["调候"]["doesNotApplyWhen"])
                + list(strategy_contracts["扶抑"]["doesNotApplyWhen"]),
            }
        )
    if score_by_strategy.get("通关", 0) >= 45 or score_by_strategy.get("病药", 0) >= 45:
        conflicts.append(
            {
                "type": "relationship_or_imbalance_overlay",
                "severity": "medium",
                "strategies": ["通关", "病药"],
                "delta": abs(score_by_strategy.get("通关", 0) - score_by_strategy.get("病药", 0)),
                "explanation": "通关与病药只说明冲突缓冲和偏枯修正，不能替代调候、扶抑或格局判断。",
                "counterEvidence": list(strategy_contracts["通关"]["doesNotApplyWhen"])
                + list(strategy_contracts["病药"]["doesNotApplyWhen"]),
            }
        )

    ranking = [
        {
            "rank": index + 1,
            "strategy": item["strategy"],
            "score": item["score"],
            "basis": item["basis"],
            "evidenceFields": item["evidenceFields"],
            "rankingReason": "按 scoreBasis 证据完整度排序；相邻策略保留并列解释。",
        }
        for index, item in enumerate(scored)
    ]
    return {
        "schemaVersion": 1,
        "primaryStrategy": scored[0]["strategy"] if scored else "",
        "scoredStrategies": scored,
        "ranking": ranking,
        "selectedCandidates": selected_candidates,
        "conflicts": conflicts,
        "decisionTrace": [
            {
                "step": "score_strategies",
                "basis": "调候、扶抑、通关、病药分别按 scoreBasis 计算证据完整度。",
                "evidenceFields": ["scoredStrategies.scoreBasis"],
            },
            {
                "step": "rank_by_score",
                "basis": "按分数降序生成 ranking，分数只代表解释优先级。",
                "evidenceFields": ["yongShenDecision.ranking"],
            },
            {
                "step": "select_parallel_candidates",
                "basis": "选择最高分附近策略，并至少保留一个次级策略作为并列审查边界。",
                "evidenceFields": ["yongShenDecision.selectedCandidates"],
            },
            {
                "step": "attach_conflicts",
                "basis": "把调候和扶抑、通关和病药的冲突关系显式输出，禁止互相覆盖。",
                "evidenceFields": ["yongShenDecision.conflicts"],
            },
        ],
        "noAbsoluteConclusion": True,
        "conflictPolicy": "调候、扶抑、通关、病药按证据完整度排序，但报告必须保留并列策略和风险边界。",
        "riskBoundary": "用神评分只用于解释优先级，不承诺现实事件结果。",
    }
