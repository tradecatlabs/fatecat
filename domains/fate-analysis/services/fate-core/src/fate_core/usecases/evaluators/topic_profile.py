from __future__ import annotations

from typing import Any

from fate_core.usecases.evaluators.relation import build_relation_order
from fate_core.usecases.evaluators.ten_god import ten_god_families
from fate_core.usecases.evaluators.yongshen import five_element_spread


def relation_families(relation: Any) -> dict[str, int]:
    if not isinstance(relation, list):
        return {}
    families = {"combine": 0, "clash": 0, "punishment_harm_break": 0, "storage": 0, "other": 0}
    for item in relation:
        if not isinstance(item, dict):
            continue
        text = f"{item.get('key', '')}{item.get('label', '')}"
        count = int(item.get("count", 1)) if isinstance(item.get("count", 1), int | float) else 1
        if "合" in text:
            families["combine"] += count
        elif "冲" in text:
            families["clash"] += count
        elif any(marker in text for marker in ["刑", "害", "破"]):
            families["punishment_harm_break"] += count
        elif "库" in text or "墓" in text:
            families["storage"] += count
        else:
            families["other"] += count
    return families


def build_topic_profiles(
    raw: dict[str, Any],
    ten_god_counts: dict[str, int],
    fortune_triggers: list[dict[str, Any]],
    yongshen_decision: dict[str, Any],
    fortune_trigger_matrix: dict[str, Any],
) -> list[dict[str, Any]]:
    families = ten_god_families(ten_god_counts)
    relation_order = build_relation_order(raw)
    relation_count = sum(item.get("count", 0) for item in relation_order if isinstance(item.get("count"), int))
    grouped_relations = relation_families(relation_order)
    spread = five_element_spread(raw)
    fortune_type_count = len({item for trigger in fortune_triggers for item in trigger.get("triggerTypes", [])})
    selected_yongshen = [
        item.get("strategy") for item in yongshen_decision.get("selectedCandidates", []) if isinstance(item, dict)
    ]
    trigger_type_counts = (
        fortune_trigger_matrix.get("triggerTypeCounts", {})
        if isinstance(fortune_trigger_matrix.get("triggerTypeCounts"), dict)
        else {}
    )
    active_dynamic_layers = [
        item.get("type")
        for item in fortune_trigger_matrix.get("matrix", [])
        if isinstance(item, dict) and item.get("status") in {"available", "triggered"}
    ]
    joint_score_inputs = {
        "tenGodFamilies": families,
        "mainPattern": raw.get("geju", {}).get("main", "") if isinstance(raw.get("geju"), dict) else "",
        "primaryYongShenStrategy": yongshen_decision.get("primaryStrategy", ""),
        "selectedYongShenStrategies": selected_yongshen,
        "fortuneTriggerTypes": sorted(trigger_type_counts),
        "activeDynamicLayers": active_dynamic_layers,
    }
    joint_score_basis = [
        {
            "factor": "用神候选",
            "value": min(12, len(selected_yongshen) * 4),
            "evidenceField": "baziBenchmark.yongShenDecision.selectedCandidates",
        },
        {
            "factor": "动态层级",
            "value": min(12, len(active_dynamic_layers) * 3),
            "evidenceField": "baziBenchmark.fortuneTriggerMatrix",
        },
    ]
    topic_specs: list[dict[str, Any]] = [
        {
            "topic": "事业",
            "basis": ["格局", "官杀", "印星", "大运流年"],
            "scoreBasis": [
                {"factor": "base", "value": 35, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "官杀", "value": families.get("官杀", 0) * 8, "evidenceField": "tenGods.官杀"},
                {"factor": "印星", "value": families.get("印", 0) * 5, "evidenceField": "tenGods.印"},
                {
                    "factor": "岁运触发",
                    "value": fortune_type_count * 3,
                    "evidenceField": "baziBenchmark.fortuneTriggers",
                },
            ],
            "evidenceFields": ["geju", "tenGods.官杀", "tenGods.印", "baziBenchmark.fortuneTriggers"],
            "riskBoundary": "事业 profile 只解释结构重心，不替代职业、雇佣或法律决策。",
        },
        {
            "topic": "财运",
            "basis": ["财星", "食伤", "用神", "岁运触发"],
            "scoreBasis": [
                {"factor": "base", "value": 35, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "财星", "value": families.get("财", 0) * 10, "evidenceField": "tenGods.财"},
                {"factor": "食伤", "value": families.get("食伤", 0) * 5, "evidenceField": "tenGods.食伤"},
                {
                    "factor": "岁运触发",
                    "value": fortune_type_count * 4,
                    "evidenceField": "baziBenchmark.fortuneTriggers",
                },
            ],
            "evidenceFields": ["tenGods.财", "tenGods.食伤", "yongShen", "baziBenchmark.fortuneTriggers"],
            "riskBoundary": "财运 profile 只作结构趋势证据，不替代投资、借贷或资产配置决策。",
        },
        {
            "topic": "婚姻",
            "basis": ["夫妻宫", "财官星", "合冲刑害", "岁运触发"],
            "scoreBasis": [
                {"factor": "base", "value": 30, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "财星", "value": families.get("财", 0) * 5, "evidenceField": "tenGods.财"},
                {"factor": "官杀", "value": families.get("官杀", 0) * 5, "evidenceField": "tenGods.官杀"},
                {"factor": "关系压力", "value": relation_count * 3, "evidenceField": "baziBenchmark.ganzhiPriority"},
            ],
            "evidenceFields": [
                "tenGods.财",
                "tenGods.官杀",
                "branchRelations.canonical",
                "baziBenchmark.fortuneTriggers",
            ],
            "riskBoundary": "婚姻 profile 只作关系结构证据，不替代亲密关系、心理或法律决策。",
        },
        {
            "topic": "健康",
            "basis": ["五行偏枯", "寒暖燥湿"],
            "scoreBasis": [
                {"factor": "base", "value": 25, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "五行偏枯", "value": spread * 3, "evidenceField": "wuxingScores.fiveElementScore"},
            ],
            "evidenceFields": ["wuxingScores.fiveElementScore", "climateScores"],
            "riskBoundary": "健康 profile 只作五行结构压力证据，不替代诊断、治疗或用药。",
        },
        {
            "topic": "学业",
            "basis": ["印星", "食伤", "文昌", "大运流年"],
            "scoreBasis": [
                {"factor": "base", "value": 35, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "印星", "value": families.get("印", 0) * 8, "evidenceField": "tenGods.印"},
                {"factor": "食伤", "value": families.get("食伤", 0) * 4, "evidenceField": "tenGods.食伤"},
                {
                    "factor": "岁运触发",
                    "value": fortune_type_count * 2,
                    "evidenceField": "baziBenchmark.fortuneTriggers",
                },
            ],
            "evidenceFields": ["tenGods.印", "tenGods.食伤", "geju", "baziBenchmark.fortuneTriggers"],
            "riskBoundary": "学业 profile 只作学习结构证据，不替代升学、培训或考试决策。",
        },
        {
            "topic": "迁移",
            "basis": ["驿马", "冲合", "岁运触发"],
            "scoreBasis": [
                {"factor": "base", "value": 30, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "冲合关系", "value": relation_count * 4, "evidenceField": "baziBenchmark.ganzhiPriority"},
                {
                    "factor": "岁运触发",
                    "value": len(fortune_triggers) * 3,
                    "evidenceField": "baziBenchmark.fortuneTriggers",
                },
            ],
            "evidenceFields": [
                "branchRelations.canonical",
                "ganzhiRelations.tianGan",
                "baziBenchmark.fortuneTriggers",
            ],
            "riskBoundary": "迁移 profile 只作变动结构证据，不替代搬迁、出行或签证决策。",
        },
        {
            "topic": "家庭",
            "basis": ["印星", "比劫", "合冲刑害", "家庭结构"],
            "scoreBasis": [
                {"factor": "base", "value": 30, "evidenceField": "topicProfiles.defaultBase"},
                {"factor": "印星", "value": families.get("印", 0) * 6, "evidenceField": "tenGods.印"},
                {"factor": "比劫", "value": families.get("比劫", 0) * 4, "evidenceField": "tenGods.比劫"},
                {
                    "factor": "合冲刑害",
                    "value": grouped_relations.get("combine", 0) * 2
                    + grouped_relations.get("clash", 0) * 3
                    + grouped_relations.get("punishment_harm_break", 0) * 3,
                    "evidenceField": "baziBenchmark.ganzhiPriority",
                },
            ],
            "evidenceFields": [
                "tenGods.印",
                "tenGods.比劫",
                "branchRelations.canonical",
                "baziBenchmark.ganzhiPriority",
            ],
            "riskBoundary": "家庭 profile 只作亲属结构证据，不替代家庭、法律或心理决策。",
        },
    ]
    profiles: list[dict[str, Any]] = []
    for spec in topic_specs:
        score = 0
        score_basis = [*spec["scoreBasis"], *joint_score_basis]
        for score_item in score_basis:
            value = score_item.get("value") if isinstance(score_item, dict) else None
            if isinstance(value, int | float):
                score += int(value)
        capped_score = max(0, min(100, int(score)))
        evidence_fields = [
            *spec["evidenceFields"],
            "baziBenchmark.yongShenDecision",
            "baziBenchmark.fortuneTriggerMatrix",
        ]
        profiles.append(
            {
                "topic": spec["topic"],
                "basis": spec["basis"],
                "score": capped_score,
                "scoreBasis": score_basis,
                "scoreTrace": {
                    "rawScore": score,
                    "cappedScore": capped_score,
                    "factors": score_basis,
                    "jointInputs": joint_score_inputs,
                },
                "jointScoreInputs": joint_score_inputs,
                "status": "evidence_seed",
                "lifecycle": "beta",
                "lifecycleGate": "进入 production 需要专题 golden、MingLi 分类回归和报告边界三者同时通过。",
                "productionGate": {
                    "status": "blocked",
                    "requiredEvidence": [
                        "topic golden",
                        "MingLi 分类回归",
                        "高风险输出 policy regression",
                        "Markdown/report 边界验收",
                    ],
                    "reason": "专题 profile 当前仅为结构联合评分，未具备 production 专题断法验收。",
                },
                "riskPolicy": {
                    "riskLevel": "high_topic_boundary",
                    "disclaimerRequired": True,
                    "forbiddenClaims": [
                        "deterministic_future",
                        "professional_replacement",
                        "guarantee",
                        "fear_claim",
                    ],
                },
                "evidenceFields": evidence_fields,
                "riskBoundary": spec["riskBoundary"],
            }
        )
    return profiles
