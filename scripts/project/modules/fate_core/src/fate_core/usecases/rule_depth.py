from __future__ import annotations

import json
from functools import cache
from typing import Any

from fate_core.support.paths import FATE_ASSETS_DIR


@cache
def load_rule_depth_registry() -> dict[str, Any]:
    """加载八字/紫微规则深度 registry。"""
    path = FATE_ASSETS_DIR / "rule_depth_registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    if not isinstance(registry, dict):
        raise ValueError("rule_depth_registry.json 必须是 JSON 对象")
    rules = registry.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("rule_depth_registry.json 缺少 rules")
    return registry


def rules_for_system(system: str) -> list[dict[str, Any]]:
    """按体系选择规则，保持 priority 降序稳定输出。"""
    registry = load_rule_depth_registry()
    selected = [rule for rule in registry["rules"] if isinstance(rule, dict) and rule.get("system") == system]
    return sorted(selected, key=lambda item: int(item.get("priority", 0)), reverse=True)


def registry_version() -> str:
    """返回规则深度 registry 版本。"""
    return str(load_rule_depth_registry().get("registryVersion", "unknown"))


def build_rule_application(
    rule: dict[str, Any],
    *,
    status: str,
    evidence: dict[str, Any],
    confidence: float | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """把 registry 规则和命盘证据组合成可审计应用记录。"""
    weight = float(rule.get("weight", 0.0))
    score = weight if confidence is None else round(max(0.0, min(1.0, confidence)), 2)
    return {
        "ruleId": rule.get("id", ""),
        "topic": rule.get("topic", ""),
        "layer": rule.get("layer", ""),
        "status": status,
        "weight": weight,
        "confidence": score,
        "evidenceFields": rule.get("evidenceFields", []),
        "conditions": rule.get("conditions", []),
        "evidence": evidence,
        "conflictPolicy": rule.get("conflictPolicy", ""),
        "riskBoundary": rule.get("riskBoundary", ""),
        "sourceRuleIds": rule.get("sourceRuleIds", []),
        "notes": notes or [],
    }


def collect_source_rule_ids(applied_rules: list[dict[str, Any]]) -> list[str]:
    """从应用记录中收集 classics_rule_index 可追溯规则 ID。"""
    ids: list[str] = []
    seen = set()
    for item in applied_rules:
        for rule_id in item.get("sourceRuleIds", []):
            if isinstance(rule_id, str) and rule_id and rule_id not in seen:
                ids.append(rule_id)
                seen.add(rule_id)
    return ids


def build_conflict_resolution(
    applied_rules: list[dict[str, Any]],
    conflict_matrix: list[dict[str, Any]],
) -> dict[str, Any]:
    """按层级、权重和置信度生成统一冲突裁决摘要。"""
    layer_rank = {"core": 4, "dynamic": 3, "topic": 2, "boundary": 1}
    ranked = sorted(
        applied_rules,
        key=lambda item: (
            layer_rank.get(str(item.get("layer", "")), 0),
            float(item.get("confidence", 0.0)),
            float(item.get("weight", 0.0)),
        ),
        reverse=True,
    )
    primary = [item.get("ruleId", "") for item in ranked[:3] if item.get("ruleId")]
    auxiliary = [item.get("ruleId", "") for item in ranked[3:] if item.get("ruleId")]
    indexed = {item.get("ruleId"): item for item in applied_rules}
    conflicts = []
    for conflict in conflict_matrix:
        rule_ids = [rule_id for rule_id in conflict.get("rules", []) if rule_id in indexed]
        if not rule_ids:
            continue
        conflicts.append(
            {
                "topic": conflict.get("topic", ""),
                "rules": rule_ids,
                "policy": conflict.get("policy", ""),
                "primaryRule": next((rule_id for rule_id in primary if rule_id in rule_ids), rule_ids[0]),
                "status": "resolved_by_policy",
            }
        )
    return {
        "schemaVersion": 1,
        "method": "layer_rank_then_confidence_then_weight",
        "primaryRuleIds": primary,
        "auxiliaryRuleIds": auxiliary,
        "conflicts": conflicts,
        "riskBoundary": "冲突裁决只决定解释优先级，不输出确定未来或替代专业建议。",
    }
