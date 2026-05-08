from __future__ import annotations

from typing import Any

from fate_core.adapters import ZiweiIztroInput, calculate_ziwei_iztro
from fate_core.usecases.calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    normalize_gender,
)
from fate_core.usecases.rule_depth import (
    build_conflict_resolution,
    build_rule_application,
    collect_source_rule_ids,
    registry_version,
    rules_for_system,
)


def build_ziwei_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造紫微斗数输入。"""
    return build_pure_analysis_input_from_payload(raw_payload)


def _public_place(place: str) -> str:
    return place if "北京" in place else "已填写（非北京地区已隐藏）"


def _star_names(stars: object) -> list[str]:
    if not isinstance(stars, list):
        return []
    names: list[str] = []
    for star in stars:
        if not isinstance(star, dict):
            continue
        name = str(star.get("name", "")).strip()
        if name:
            names.append(name)
    return names


def _all_stars(palace: dict[str, Any]) -> list[dict[str, Any]]:
    stars: list[dict[str, Any]] = []
    for key in ("majorStars", "minorStars", "adjectiveStars"):
        values = palace.get(key)
        if isinstance(values, list):
            stars.extend([item for item in values if isinstance(item, dict)])
    return stars


def _star_category(star: dict[str, Any]) -> str:
    raw_type = str(star.get("type", "")).strip()
    name = str(star.get("name", "")).strip()
    if raw_type:
        return raw_type
    if name in {"擎羊", "陀罗", "火星", "铃星", "地空", "地劫"}:
        return "煞星"
    if name in {"左辅", "右弼", "文昌", "文曲", "天魁", "天钺", "禄存", "天马"}:
        return "辅星"
    return "杂曜"


def _opposite_index(index: int) -> int:
    return (index + 6) % 12


def _side_indices(index: int) -> list[int]:
    return [(index - 1) % 12, (index + 1) % 12]


def _palace_by_index(palaces: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    indexed: dict[int, dict[str, Any]] = {}
    for palace in palaces:
        raw_index = palace.get("index")
        if raw_index is None:
            continue
        try:
            indexed[int(raw_index)] = palace
        except Exception:
            continue
    return indexed


def _palace_marker(palace: dict[str, Any]) -> str:
    markers = []
    if palace.get("isOriginalPalace"):
        markers.append("命宫")
    if palace.get("isBodyPalace"):
        markers.append("身宫")
    return "、".join(markers)


def _summarize_surrounded_block(block: object) -> dict[str, Any]:
    if not isinstance(block, dict):
        return {}
    result: dict[str, Any] = {}
    for key, label in [("target", "本宫"), ("opposite", "对宫"), ("wealth", "财帛位"), ("career", "官禄位")]:
        palace = block.get(key)
        if not isinstance(palace, dict):
            continue
        result[key] = {
            "role": label,
            "palace": palace.get("name", ""),
            "earthlyBranch": palace.get("earthlyBranch", ""),
            "majorStars": _star_names(palace.get("majorStars")),
            "minorStars": _star_names(palace.get("minorStars")),
        }
    result["mutagenFlags"] = {
        "禄": bool(block.get("hasLu")),
        "权": bool(block.get("hasQuan")),
        "科": bool(block.get("hasKe")),
        "忌": bool(block.get("hasJi")),
    }
    return result


def _build_star_taxonomy(palaces: list[dict[str, Any]]) -> dict[str, Any]:
    categories: dict[str, list[dict[str, Any]]] = {}
    brightness: dict[str, list[dict[str, Any]]] = {}
    for palace in palaces:
        for star in _all_stars(palace):
            name = str(star.get("name", "")).strip()
            if not name:
                continue
            category = _star_category(star)
            item = {
                "name": name,
                "palace": palace.get("name", ""),
                "earthlyBranch": palace.get("earthlyBranch", ""),
                "scope": star.get("scope", ""),
                "brightness": star.get("brightness", ""),
                "mutagen": star.get("mutagen", ""),
            }
            categories.setdefault(category, []).append(item)
            if item["brightness"]:
                brightness.setdefault(str(item["brightness"]), []).append(item)
    return {
        "schemaVersion": 1,
        "categories": categories,
        "brightness": brightness,
        "categoryCounts": {key: len(value) for key, value in categories.items()},
        "brightnessCounts": {key: len(value) for key, value in brightness.items()},
        "ruleIds": ["ziwei.star_taxonomy", "ziwei.brightness_state"],
    }


def _build_palace_relations(palaces: list[dict[str, Any]]) -> dict[str, Any]:
    indexed = _palace_by_index(palaces)
    relations: list[dict[str, Any]] = []
    for palace in palaces:
        raw_index = palace.get("index")
        if raw_index is None:
            continue
        try:
            index = int(raw_index)
        except Exception:
            continue
        opposite = indexed.get(_opposite_index(index), {})
        sides = [indexed.get(item, {}) for item in _side_indices(index)]
        relations.append(
            {
                "palace": palace.get("name", ""),
                "index": index,
                "earthlyBranch": palace.get("earthlyBranch", ""),
                "opposite": {
                    "palace": opposite.get("name", ""),
                    "index": opposite.get("index"),
                    "earthlyBranch": opposite.get("earthlyBranch", ""),
                },
                "sandwichedBy": [
                    {
                        "palace": item.get("name", ""),
                        "index": item.get("index"),
                        "earthlyBranch": item.get("earthlyBranch", ""),
                    }
                    for item in sides
                    if item
                ],
                "markers": {
                    "life": bool(palace.get("isOriginalPalace")),
                    "body": bool(palace.get("isBodyPalace")),
                },
                "majorStars": _star_names(palace.get("majorStars")),
            }
        )
    return {
        "schemaVersion": 1,
        "relations": relations,
        "ruleIds": ["ziwei.palace_relations", "ziwei.opposite_palace", "ziwei.sandwiched_palaces"],
    }


def _build_mutagen_flow(data: dict[str, Any]) -> dict[str, Any]:
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    horoscope = data.get("ziweiHoroscope", {}) if isinstance(data.get("ziweiHoroscope"), dict) else {}
    placements = data.get("ziweiInterpretation", {}).get("mutagenPlacements", [])
    if not isinstance(placements, list):
        placements = []
    palace_by_name = {str(p.get("name", "")): p for p in palaces}
    flow = []
    for item in placements:
        if not isinstance(item, dict):
            continue
        palace = palace_by_name.get(str(item.get("palace", "")), {})
        try:
            index = int(palace.get("index"))
        except Exception:
            index = -1
        opposite = palace_by_name.get("")
        if index >= 0:
            opposite = _palace_by_index(palaces).get(_opposite_index(index), {})
        flow.append(
            {
                "mutagen": item.get("mutagen", ""),
                "star": item.get("star", ""),
                "fromScope": item.get("scope", ""),
                "enterPalace": item.get("palace", ""),
                "enterEarthlyBranch": palace.get("earthlyBranch", ""),
                "oppositePalace": opposite.get("name", "") if isinstance(opposite, dict) else "",
                "shineRelation": "落宫/对宫结构证据；飞入、冲照、会照只作结构提示。",
            }
        )
    horoscope_scopes = []
    for scope_key, scope_name in [
        ("decadal", "大限"),
        ("yearly", "流年"),
        ("monthly", "流月"),
        ("daily", "流日"),
        ("hourly", "流时"),
    ]:
        scope = horoscope.get(scope_key)
        if isinstance(scope, dict):
            horoscope_scopes.append(
                {
                    "scope": scope_name,
                    "ganZhi": f"{scope.get('heavenlyStem', '')}{scope.get('earthlyBranch', '')}",
                    "mutagen": scope.get("mutagen", []),
                    "palaceNames": scope.get("palaceNames", []),
                }
            )
    return {
        "schemaVersion": 1,
        "placements": flow,
        "horoscopeScopes": horoscope_scopes,
        "ruleIds": ["ziwei.mutagen_flow", "ziwei.mutagen_opposition"],
    }


def _build_star_encyclopedia_seed(palaces: list[dict[str, Any]]) -> dict[str, Any]:
    entries = []
    seen = set()
    for palace in palaces:
        for star in _all_stars(palace):
            name = str(star.get("name", "")).strip()
            if not name or name in seen:
                continue
            seen.add(name)
            entries.append(
                {
                    "star": name,
                    "category": _star_category(star),
                    "samplePalace": palace.get("name", ""),
                    "brightness": star.get("brightness", ""),
                    "mutagen": star.get("mutagen", ""),
                    "interpretationBoundary": "星曜百科种子只描述字段条件，不输出完整断语。",
                }
            )
    return {
        "schemaVersion": 1,
        "entries": entries,
        "ruleIds": ["ziwei.star_encyclopedia_seed"],
    }


def _build_palace_topics(data: dict[str, Any]) -> list[dict[str, Any]]:
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    relations = {
        item.get("palace"): item
        for item in data.get("ziweiPalaceRelations", {}).get("relations", [])
        if isinstance(item, dict)
    }
    topics = []
    for palace in palaces:
        name = palace.get("name", "")
        topics.append(
            {
                "palace": name,
                "earthlyBranch": palace.get("earthlyBranch", ""),
                "majorStars": _star_names(palace.get("majorStars")),
                "minorStars": _star_names(palace.get("minorStars")),
                "adjectiveStars": _star_names(palace.get("adjectiveStars")),
                "relation": relations.get(name, {}),
                "decadal": palace.get("decadal"),
                "statement": "十二宫专题只汇总宫位、星曜、四化与限运证据，不作确定性断语。",
                "ruleIds": ["ziwei.palace_topic"],
            }
        )
    return topics


def _build_pattern_matches(data: dict[str, Any]) -> list[dict[str, Any]]:
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    all_major = {star for palace in palaces for star in _star_names(palace.get("majorStars"))}
    candidates = [
        ("紫府同宫", {"紫微", "天府"}),
        ("机月同梁", {"天机", "太阴", "天梁"}),
        ("杀破狼", {"七杀", "破军", "贪狼"}),
        ("府相朝垣", {"天府", "天相"}),
        ("日月并明", {"太阳", "太阴"}),
    ]
    matches = []
    for name, required in candidates:
        present = sorted(required & all_major)
        matches.append(
            {
                "pattern": name,
                "matched": required.issubset(all_major),
                "presentStars": present,
                "missingStars": sorted(required - all_major),
                "ruleIds": ["ziwei.pattern_match_seed"],
            }
        )
    return matches


def _build_golden_guards(data: dict[str, Any]) -> dict[str, Any]:
    palaces = data.get("palaceAnalysis", [])
    interpretation = data.get("ziweiInterpretation", {}) if isinstance(data.get("ziweiInterpretation"), dict) else {}
    life = next((p for p in palaces if isinstance(p, dict) and p.get("isOriginalPalace")), {})
    body = next((p for p in palaces if isinstance(p, dict) and p.get("isBodyPalace")), {})
    return {
        "schemaVersion": 1,
        "palaceCount": len(palaces) if isinstance(palaces, list) else 0,
        "lifePalace": {
            "name": life.get("name", ""),
            "earthlyBranch": life.get("earthlyBranch", ""),
            "majorStars": _star_names(life.get("majorStars")),
        },
        "bodyPalace": {
            "name": body.get("name", ""),
            "earthlyBranch": body.get("earthlyBranch", ""),
            "majorStars": _star_names(body.get("majorStars")),
        },
        "mutagenPlacementCount": len(interpretation.get("mutagenPlacements", []))
        if isinstance(interpretation.get("mutagenPlacements"), list)
        else 0,
        "fortuneLinkCount": len(interpretation.get("fortuneLinks", []))
        if isinstance(interpretation.get("fortuneLinks"), list)
        else 0,
        "ruleIds": ["ziwei.golden_case_guard"],
    }


def _build_ziwei_rule_depth(data: dict[str, Any]) -> dict[str, Any]:
    """装配紫微规则深度层：只引用 iztro/FateCat 已有结构化字段。"""
    rules = {str(rule.get("id", "")): rule for rule in rules_for_system("ziwei")}
    taxonomy = data.get("ziweiStarTaxonomy", {}) if isinstance(data.get("ziweiStarTaxonomy"), dict) else {}
    relations = data.get("ziweiPalaceRelations", {}) if isinstance(data.get("ziweiPalaceRelations"), dict) else {}
    mutagen = data.get("ziweiMutagenFlow", {}) if isinstance(data.get("ziweiMutagenFlow"), dict) else {}
    patterns = data.get("ziweiPatternMatches", [])
    topics = data.get("ziweiPalaceTopics", [])
    encyclopedia = data.get("ziweiStarEncyclopedia", {}) if isinstance(data.get("ziweiStarEncyclopedia"), dict) else {}
    interpretation = data.get("ziweiInterpretation", {}) if isinstance(data.get("ziweiInterpretation"), dict) else {}
    surrounded = (
        interpretation.get("surroundedPalaces", {}) if isinstance(interpretation.get("surroundedPalaces"), dict) else {}
    )
    fortune_links = interpretation.get("fortuneLinks", [])
    pattern_by_name = (
        {item.get("pattern"): item for item in patterns if isinstance(item, dict)} if isinstance(patterns, list) else {}
    )

    applied = [
        build_rule_application(
            rules["ziwei.depth.star.brightness_weight"],
            status="applied" if taxonomy.get("brightnessCounts") else "partial",
            confidence=0.88 if taxonomy.get("brightnessCounts") else 0.55,
            evidence={
                "categoryCounts": taxonomy.get("categoryCounts", {}),
                "brightnessCounts": taxonomy.get("brightnessCounts", {}),
                "ruleIds": taxonomy.get("ruleIds", []),
            },
            notes=["亮度只修正解释权重，不单独断吉凶。"],
        ),
        build_rule_application(
            rules["ziwei.depth.palace.triad_focus"],
            status="applied" if surrounded or relations.get("relations") else "partial",
            confidence=0.86 if surrounded else 0.65,
            evidence={
                "surroundedPalaces": surrounded,
                "relationCount": len(relations.get("relations", []))
                if isinstance(relations.get("relations"), list)
                else 0,
            },
            notes=["原生三方四正优先，手工对宫和夹宫仅作补充。"],
        ),
        build_rule_application(
            rules["ziwei.depth.mutagen.scope_chain"],
            status="applied" if mutagen.get("placements") or mutagen.get("horoscopeScopes") else "partial",
            confidence=0.83 if mutagen.get("placements") else 0.6,
            evidence={
                "placementCount": len(mutagen.get("placements", []))
                if isinstance(mutagen.get("placements"), list)
                else 0,
                "horoscopeScopes": mutagen.get("horoscopeScopes", []),
            },
            notes=["本命四化和运限四化分层展示，避免混读。"],
        ),
        build_rule_application(
            rules["ziwei.depth.pattern.condition_matrix"],
            status="applied" if isinstance(patterns, list) and patterns else "partial",
            confidence=0.74 if isinstance(patterns, list) and patterns else 0.5,
            evidence={
                "matches": patterns,
                "matchedPatterns": [
                    item.get("pattern") for item in patterns if isinstance(item, dict) and item.get("matched")
                ]
                if isinstance(patterns, list)
                else [],
            },
            notes=["候选格局必须列出 presentStars 和 missingStars。"],
        ),
        build_rule_application(
            rules["ziwei.depth.pattern.sha_po_lang"],
            status="applied" if pattern_by_name.get("杀破狼", {}).get("matched") else "candidate",
            confidence=0.72 if pattern_by_name.get("杀破狼", {}).get("matched") else 0.42,
            evidence=pattern_by_name.get("杀破狼", {}),
            notes=["杀破狼只登记主星集合命中，完整格局仍需宫位和煞忌条件。"],
        ),
        build_rule_application(
            rules["ziwei.depth.pattern.ji_yue_tong_liang"],
            status="applied" if pattern_by_name.get("机月同梁", {}).get("matched") else "candidate",
            confidence=0.7 if pattern_by_name.get("机月同梁", {}).get("matched") else 0.42,
            evidence=pattern_by_name.get("机月同梁", {}),
            notes=["机月同梁只登记组合候选，后续继续补宫位和四化条件。"],
        ),
        build_rule_application(
            rules["ziwei.depth.star.encyclopedia_condition"],
            status="applied" if encyclopedia.get("entries") else "partial",
            confidence=0.69 if encyclopedia.get("entries") else 0.45,
            evidence={
                "entryCount": len(encyclopedia.get("entries", []))
                if isinstance(encyclopedia.get("entries"), list)
                else 0,
                "sampleEntries": encyclopedia.get("entries", [])[:5]
                if isinstance(encyclopedia.get("entries"), list)
                else [],
            },
            notes=["星曜百科只登记条件化解释，不直接生成完整断语。"],
        ),
        build_rule_application(
            rules["ziwei.depth.mutagen.opposition_guard"],
            status="applied" if mutagen.get("placements") else "partial",
            confidence=0.67 if mutagen.get("placements") else 0.42,
            evidence={
                "placements": mutagen.get("placements", []),
                "guard": "冲照会照先按落宫和对宫登记，完整飞星派另行配置。",
            },
            notes=["四化冲照会照不得覆盖原始四化事实。"],
        ),
        build_rule_application(
            rules["ziwei.depth.palace.topic_matrix"],
            status="applied" if isinstance(topics, list) and len(topics) == 12 else "partial",
            confidence=0.68 if isinstance(topics, list) and len(topics) == 12 else 0.45,
            evidence={
                "topicCount": len(topics) if isinstance(topics, list) else 0,
                "samplePalaces": [item.get("palace") for item in topics[:4] if isinstance(item, dict)]
                if isinstance(topics, list)
                else [],
            },
            notes=["专题解释必须回到宫位、星曜、四化和限运证据。"],
        ),
        build_rule_application(
            rules["ziwei.depth.palace.topic_risk_boundary"],
            status="applied" if isinstance(topics, list) and topics else "partial",
            confidence=0.68 if isinstance(topics, list) and topics else 0.45,
            evidence={
                "topicCount": len(topics) if isinstance(topics, list) else 0,
                "riskBoundary": "健康、财富、婚恋等主题不得替代专业建议。",
            },
            notes=["专题输出统一受风险边界约束。"],
        ),
        build_rule_application(
            rules["ziwei.depth.fortune.linkage_chain"],
            status="applied" if isinstance(fortune_links, list) and fortune_links else "partial",
            confidence=0.66 if isinstance(fortune_links, list) and len(fortune_links) >= 2 else 0.45,
            evidence={
                "fortuneLinkCount": len(fortune_links) if isinstance(fortune_links, list) else 0,
                "fortuneLinks": fortune_links,
            },
            notes=["本命为体、运限为用；运限不得覆盖本命盘面事实。"],
        ),
        build_rule_application(
            rules["ziwei.depth.fortune.decadal_yearly_bridge"],
            status="applied" if isinstance(fortune_links, list) and len(fortune_links) >= 2 else "partial",
            confidence=0.64 if isinstance(fortune_links, list) and len(fortune_links) >= 2 else 0.4,
            evidence={
                "fortuneLinks": fortune_links,
                "bridge": "大限定阶段，流年触发主题，流月/流日/流时只作细化。",
            },
            notes=["动态层级由粗到细，不反向覆盖本命。"],
        ),
    ]
    conflict_matrix = [
        {
            "topic": "四化作用域",
            "rules": [
                "ziwei.depth.mutagen.scope_chain",
                "ziwei.depth.mutagen.opposition_guard",
                "ziwei.depth.fortune.linkage_chain",
            ],
            "policy": "本命、大限、流年、流月、流日、流时分层显示，不混读。",
        },
        {
            "topic": "格局候选",
            "rules": [
                "ziwei.depth.pattern.condition_matrix",
                "ziwei.depth.pattern.sha_po_lang",
                "ziwei.depth.pattern.ji_yue_tong_liang",
            ],
            "policy": "不满足条件的格局保留 missingStars，不写成成立。",
        },
        {
            "topic": "专题风险边界",
            "rules": ["ziwei.depth.palace.topic_matrix", "ziwei.depth.palace.topic_risk_boundary"],
            "policy": "专题解释回到宫位、星曜、四化和限运证据，不替代专业建议。",
        },
    ]
    return {
        "schemaVersion": 1,
        "registryVersion": registry_version(),
        "system": "ziwei",
        "boundary": "紫微规则深度层只组织 iztro 原生命盘和项目解释层证据，不自研星曜排布底层算法。",
        "appliedRules": applied,
        "conflictMatrix": conflict_matrix,
        "conflictResolution": build_conflict_resolution(applied, conflict_matrix),
        "sourceRuleIds": collect_source_rule_ids(applied),
    }


def _build_ziwei_interpretation(data: dict[str, Any]) -> dict[str, Any]:
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    chart = data.get("ziweiChart", {}) if isinstance(data.get("ziweiChart"), dict) else {}
    horoscope = data.get("ziweiHoroscope", {}) if isinstance(data.get("ziweiHoroscope"), dict) else {}

    main_star_combinations = []
    life_body = []
    mutagen_placements = []
    for palace in palaces:
        major = _star_names(palace.get("majorStars"))
        minor = _star_names(palace.get("minorStars"))
        adjective = _star_names(palace.get("adjectiveStars"))
        if major:
            main_star_combinations.append(
                {
                    "palace": palace.get("name", ""),
                    "combination": "、".join(major),
                    "majorStars": major,
                    "minorStars": minor,
                    "adjectiveStars": adjective,
                    "basis": ["majorStars", "minorStars", "adjectiveStars"],
                }
            )
        marker = _palace_marker(palace)
        if marker:
            life_body.append(
                {
                    "marker": marker,
                    "palace": palace.get("name", ""),
                    "earthlyBranch": palace.get("earthlyBranch", ""),
                    "heavenlyStem": palace.get("heavenlyStem", ""),
                    "majorStars": major,
                    "decadal": palace.get("decadal"),
                    "basis": ["isOriginalPalace", "isBodyPalace", "majorStars", "decadal"],
                    "statement": f"{marker}落{palace.get('name', '')}，主星为{'、'.join(major) if major else '空宫'}；此处只作盘面结构说明。",
                }
            )
        for star in _all_stars(palace):
            mutagen = str(star.get("mutagen", "")).strip()
            if mutagen:
                mutagen_placements.append(
                    {
                        "mutagen": mutagen,
                        "star": star.get("name", ""),
                        "palace": palace.get("name", ""),
                        "scope": star.get("scope", ""),
                        "basis": ["star.mutagen", "palace.name"],
                    }
                )

    surrounded = chart.get("surroundedPalaces", {}) if isinstance(chart.get("surroundedPalaces"), dict) else {}
    surrounded_summary = {
        "life": _summarize_surrounded_block(surrounded.get("life")),
        "body": _summarize_surrounded_block(surrounded.get("body")),
    }

    fortune_links = []
    for scope_key, scope_name in [
        ("decadal", "大限"),
        ("yearly", "流年"),
        ("monthly", "流月"),
        ("daily", "流日"),
        ("hourly", "流时"),
    ]:
        scope = horoscope.get(scope_key)
        if not isinstance(scope, dict) or not scope:
            continue
        fortune_links.append(
            {
                "scope": scope_name,
                "ganZhi": f"{scope.get('heavenlyStem', '')}{scope.get('earthlyBranch', '')}",
                "mutagen": scope.get("mutagen", []),
                "palaceNames": scope.get("palaceNames", []),
                "basis": [f"ziweiHoroscope.{scope_key}.mutagen", f"ziweiHoroscope.{scope_key}.palaceNames"],
            }
        )

    return {
        "schemaVersion": 1,
        "interpretationBoundary": "结构化解释层，只解释盘面证据与作用域，不输出确定性断语。",
        "mainStarCombinations": main_star_combinations,
        "lifeBody": life_body,
        "surroundedPalaces": surrounded_summary,
        "mutagenPlacements": mutagen_placements,
        "fortuneLinks": fortune_links,
    }


def _select_ziwei_payload(raw: dict[str, Any], payload: PureAnalysisInput) -> dict[str, Any]:
    input_payload = {
        "name": payload.name or "命主",
        "gender": normalize_gender(payload.gender),
        "birthDateTime": payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "birthPlace": _public_place(payload.birth_place),
        "longitude": payload.longitude,
        "latitude": payload.latitude,
        "useTrueSolarTime": payload.use_true_solar_time,
    }

    data = {
        "capabilityId": "ziwei",
        "input": input_payload,
        "inputTrace": raw.get("inputTrace", {}),
        "birthInfo": raw.get("birthInfo", {}),
        "ziweiChart": raw.get("ziweiChart", {}),
        "palaceAnalysis": raw.get("palaceAnalysis", {}),
        "fiveElementsClass": raw.get("fiveElementsClass", ""),
        "starInfluence": raw.get("starInfluence", {}),
        "starPositions": raw.get("starPositions", []),
        "ziweiHoroscope": raw.get("ziweiHoroscope", {}),
        "meta": {
            "birthPlaceDisplay": _public_place(payload.birth_place),
            "source": "BaziCalculator true-solar pipeline + fortel/iztro",
            "legacyZiweiBasic": "disabled",
        },
    }
    data["ziweiInterpretation"] = _build_ziwei_interpretation(data)
    palaces = data.get("palaceAnalysis", [])
    palaces = [item for item in palaces if isinstance(item, dict)] if isinstance(palaces, list) else []
    data["ziweiStarTaxonomy"] = _build_star_taxonomy(palaces)
    data["ziweiPalaceRelations"] = _build_palace_relations(palaces)
    data["ziweiMutagenFlow"] = _build_mutagen_flow(data)
    data["ziweiStarEncyclopedia"] = _build_star_encyclopedia_seed(palaces)
    data["ziweiPatternMatches"] = _build_pattern_matches(data)
    data["ziweiPalaceTopics"] = _build_palace_topics(data)
    data["ziweiGoldenGuards"] = _build_golden_guards(data)
    data["ziweiRuleDepth"] = _build_ziwei_rule_depth(data)
    return data


def _build_evidence(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "capabilityId": "ziwei",
        "source": "iztro",
        "items": {
            "ziweiChart": {
                "source": "fortel_ziwei_integration -> iztro",
                "ruleIds": ["ziwei.iztro_chart", "ziwei.palace_metadata", "ziwei.decadal_ranges"],
                "basis": ["ziweiChart", "palaceAnalysis", "starPositions", "fiveElementsClass"],
                "risk": "folk_reference",
            },
            "horoscope": {
                "source": "iztro horoscope",
                "ruleIds": ["ziwei.horoscope_cycles", "ziwei.mutagen_scope"],
                "basis": ["ziweiHoroscope"],
                "risk": "folk_reference",
            },
            "timePipeline": {
                "source": "BaziCalculator true-solar pipeline",
                "ruleIds": ["bazi.true_solar_time_pipeline", "ziwei.time_index"],
                "basis": ["inputTrace.originalTime", "inputTrace.trueSolarTime", "inputTrace.timeZhi"],
                "risk": "calendar_boundary",
            },
            "interpretation": {
                "source": "iztro structured fields + FateCat interpretation boundary",
                "ruleIds": [
                    "ziwei.main_star_combination",
                    "ziwei.life_body_palaces",
                    "ziwei.surrounded_palaces",
                    "ziwei.mutagen_placement",
                    "ziwei.fortune_linkage",
                ],
                "basis": [
                    "ziweiInterpretation.mainStarCombinations",
                    "ziweiInterpretation.lifeBody",
                    "ziweiInterpretation.surroundedPalaces",
                    "ziweiInterpretation.mutagenPlacements",
                    "ziweiInterpretation.fortuneLinks",
                ],
                "risk": "folk_reference",
            },
            "benchmarkHardening": {
                "source": "iztro structured fields + FateCat benchmark hardening",
                "ruleIds": [
                    "ziwei.star_taxonomy",
                    "ziwei.brightness_state",
                    "ziwei.palace_relations",
                    "ziwei.mutagen_flow",
                    "ziwei.golden_case_guard",
                    "ziwei.star_encyclopedia_seed",
                    "ziwei.pattern_match_seed",
                    "ziwei.palace_topic",
                ],
                "basis": [
                    "ziweiStarTaxonomy",
                    "ziweiPalaceRelations",
                    "ziweiMutagenFlow",
                    "ziweiGoldenGuards",
                    "ziweiStarEncyclopedia",
                    "ziweiPatternMatches",
                    "ziweiPalaceTopics",
                ],
                "risk": "folk_reference",
            },
            "ruleDepth": {
                "source": "rule_depth_registry.json + iztro structured fields",
                "ruleIds": data.get("ziweiRuleDepth", {}).get("sourceRuleIds", [])
                if isinstance(data.get("ziweiRuleDepth"), dict)
                else [],
                "basis": [
                    "ziweiRuleDepth.appliedRules",
                    "ziweiRuleDepth.conflictMatrix",
                    "ziweiStarTaxonomy",
                    "ziweiPalaceRelations",
                    "ziweiMutagenFlow",
                    "ziweiPatternMatches",
                    "ziweiPalaceTopics",
                ],
                "risk": "folk_reference",
            },
        },
        "coverage": {
            "hasChart": bool(data.get("ziweiChart")),
            "hasHoroscope": bool(data.get("ziweiHoroscope")),
            "hasInterpretation": bool(data.get("ziweiInterpretation")),
            "hasBenchmarkHardening": bool(data.get("ziweiStarTaxonomy")) and bool(data.get("ziweiGoldenGuards")),
            "hasRuleDepth": bool(data.get("ziweiRuleDepth")),
            "palaceCount": len(data.get("palaceAnalysis", [])) if isinstance(data.get("palaceAnalysis"), list) else 0,
            "starPositionCount": len(data.get("starPositions", []))
            if isinstance(data.get("starPositions"), list)
            else 0,
            "hasInputTrace": bool(data.get("inputTrace")),
        },
    }


def calculate_ziwei(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算紫微斗数独立 capability。"""
    adapter_payload = ZiweiIztroInput(
        birth_dt=payload.birth_dt,
        gender=normalize_gender(payload.gender),
        longitude=payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=_public_place(payload.birth_place),
        use_true_solar_time=payload.use_true_solar_time,
    )
    raw = calculate_ziwei_iztro(adapter_payload)
    data = _select_ziwei_payload(raw, payload)
    data["analysisEvidence"] = _build_evidence(data)
    return data
