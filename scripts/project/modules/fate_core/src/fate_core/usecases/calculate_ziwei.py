from __future__ import annotations

from typing import Any

from fate_core.adapters import ZiweiIztroInput, calculate_ziwei_iztro
from fate_core.usecases.calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    normalize_gender,
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
        },
        "coverage": {
            "hasChart": bool(data.get("ziweiChart")),
            "hasHoroscope": bool(data.get("ziweiHoroscope")),
            "hasInterpretation": bool(data.get("ziweiInterpretation")),
            "hasBenchmarkHardening": bool(data.get("ziweiStarTaxonomy")) and bool(data.get("ziweiGoldenGuards")),
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
