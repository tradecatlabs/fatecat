from __future__ import annotations

from typing import Any


def condition(name: str, met: bool, evidence: Any) -> dict[str, Any]:
    return {"name": name, "met": bool(met), "evidence": evidence}


def build_relation_order(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """把干支关系按审计优先级整理成稳定结构。"""
    relations = raw.get("ganzhiRelations", {}) if isinstance(raw.get("ganzhiRelations"), dict) else {}
    branch_rel = raw.get("branchRelations", {}) if isinstance(raw.get("branchRelations"), dict) else {}
    extra = raw.get("ganzhiExtra", {}) if isinstance(raw.get("ganzhiExtra"), dict) else {}
    canonical = branch_rel.get("canonical", []) if isinstance(branch_rel.get("canonical"), list) else []

    def branch_items(*relations: str) -> list[dict[str, Any]]:
        return [item for item in canonical if isinstance(item, dict) and item.get("relation") in relations]

    groups = [
        ("hehua", "合化", relations.get("tianGan", []), "先记录天干五合；是否成化需要后续条件字段确认。"),
        ("sanHui", "三会", branch_items("三会", "会"), "三会优先于三合展示。"),
        ("sanHe", "三合", branch_items("三合", "合"), "完整三合优先于半合。"),
        ("liuHe", "六合", branch_items("六合"), "六合作为结构辅助关系。"),
        (
            "conflict",
            "冲刑害破",
            branch_items("冲", "刑", "害", "破", "暗合"),
            "动态触发时优先进入运势证据。",
        ),
        ("ku", "入库", extra.get("kuDetail", {}), "库气与入库只作为结构证据，不单独决定喜忌。"),
    ]
    ordered = []
    for priority, (key, label, value, boundary) in enumerate(groups, start=1):
        count = len(value) if isinstance(value, (list, dict)) else (1 if value else 0)
        ordered.append(
            {
                "key": key,
                "label": label,
                "priority": priority,
                "count": count,
                "items": value,
                "boundary": boundary,
            }
        )
    return ordered


def relation_blockers(raw: dict[str, Any], positions: set[str]) -> list[str]:
    blockers: list[str] = []
    branch_rel = raw.get("branchRelations", {}) if isinstance(raw.get("branchRelations"), dict) else {}
    canonical = branch_rel.get("canonical", []) if isinstance(branch_rel.get("canonical"), list) else []
    for item in canonical:
        if not isinstance(item, dict):
            continue
        if item.get("relation") not in {"冲", "刑", "害", "破"}:
            continue
        relation_positions = {str(position) for position in item.get("positions", [])}
        if relation_positions & positions:
            blockers.append(str(item.get("text", "")))
    extra = raw.get("ganzhiExtra", {}) if isinstance(raw.get("ganzhiExtra"), dict) else {}
    for item in extra.get("keDetail", []) if isinstance(extra.get("keDetail"), list) else []:
        if isinstance(item, dict) and {item.get("from"), item.get("to")} & positions:
            blockers.append(str(item.get("text", "")))
    return [item for item in blockers if item][:8]
