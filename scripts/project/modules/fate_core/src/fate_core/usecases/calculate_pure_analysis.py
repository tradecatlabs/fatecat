from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.adapters import LegacyBaziInput
from fate_core.kernel import project_by_profile
from fate_core.providers import (
    build_base_chart_section,
    build_classical_section,
    build_fortune_section,
    build_pure_analysis_runtime,
)


@dataclass(frozen=True)
class PureAnalysisInput:
    """纯命理分析用例输入。"""

    birth_dt: datetime
    gender: str
    longitude: float
    latitude: float
    name: str | None = None
    birth_place: str = ""
    use_true_solar_time: bool = True


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", "否"}:
        return False
    raise ValueError(f"无法解析布尔值: {value}")


def parse_datetime(value: str) -> datetime:
    """解析出生时间，兼容 CLI/API 常见输入格式。"""
    normalized = value.strip()
    if not normalized:
        raise ValueError("birthDateTime 不能为空")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        pass
    for time_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(normalized, time_format)
        except ValueError:
            continue
    raise ValueError(f"无法解析出生时间: {value}")


def normalize_gender(gender: str) -> str:
    """把人类输入统一成底层计算器使用的性别枚举。"""
    normalized = str(gender).strip().lower()
    if normalized in {"male", "m", "man", "boy", "男", "男性", "乾", "乾造"}:
        return "male"
    if normalized in {"female", "f", "woman", "girl", "女", "女性", "坤", "坤造"}:
        return "female"
    raise ValueError(f"无法识别性别: {gender}")


def normalize_pure_analysis_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    """把 CLI/API/Capability 输入统一成纯分析用例字段。"""
    birth_place_value = raw_payload.get("birthPlace")
    birth_place_object: dict[str, Any] = birth_place_value if isinstance(birth_place_value, dict) else {}
    raw_options = raw_payload.get("options")
    options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}

    birth_datetime = _first_non_empty(
        raw_payload.get("birthDateTime"),
        raw_payload.get("birth_datetime"),
        raw_payload.get("birth_dt"),
        raw_payload.get("datetime"),
    )
    if not birth_datetime and raw_payload.get("birthDate") and raw_payload.get("birthTime"):
        birth_datetime = f"{raw_payload['birthDate']} {raw_payload['birthTime']}"

    longitude = _first_non_empty(
        raw_payload.get("longitude"),
        raw_payload.get("lng"),
        birth_place_object.get("longitude"),
        birth_place_object.get("lng"),
    )
    latitude = _first_non_empty(
        raw_payload.get("latitude"),
        raw_payload.get("lat"),
        birth_place_object.get("latitude"),
        birth_place_object.get("lat"),
    )
    birth_place_name = _first_non_empty(
        raw_payload.get("birth_place"),
        raw_payload.get("birthPlaceName"),
        birth_place_value if isinstance(birth_place_value, str) else None,
        birth_place_object.get("name"),
    )
    use_true_solar_time = _first_non_empty(
        raw_payload.get("useTrueSolarTime"),
        raw_payload.get("use_true_solar_time"),
        options.get("useTrueSolarTime"),
    )

    normalized = {
        "birthDateTime": birth_datetime,
        "gender": _first_non_empty(raw_payload.get("gender"), raw_payload.get("sex")),
        "longitude": longitude,
        "latitude": latitude,
        "name": raw_payload.get("name"),
        "birthPlace": birth_place_name or "",
        "useTrueSolarTime": _parse_bool(use_true_solar_time, default=True),
    }
    missing = [
        field for field in ("birthDateTime", "gender", "longitude", "latitude") if normalized[field] in (None, "")
    ]
    if missing:
        raise ValueError(f"缺少必填字段: {', '.join(missing)}")
    normalized["longitude"] = float(normalized["longitude"])
    normalized["latitude"] = float(normalized["latitude"])
    normalized["gender"] = normalize_gender(str(normalized["gender"]))
    return normalized


def build_pure_analysis_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造纯分析输入。"""
    normalized = normalize_pure_analysis_payload(raw_payload)
    return PureAnalysisInput(
        birth_dt=parse_datetime(str(normalized["birthDateTime"])),
        gender=str(normalized["gender"]),
        longitude=normalized["longitude"],
        latitude=normalized["latitude"],
        name=normalized["name"],
        birth_place=str(normalized["birthPlace"]),
        use_true_solar_time=normalized["useTrueSolarTime"],
    )


def _evidence_item(
    *,
    conclusion: dict[str, Any],
    basis: list[str],
    sources: list[str],
    rule_ids: list[str],
    weight: str = "core",
) -> dict[str, Any]:
    return {
        "conclusion": conclusion,
        "basis": basis,
        "sources": sources,
        "ruleIds": rule_ids,
        "weight": weight,
        "visibility": "audit",
    }


def _build_accuracy_guards(runtime: Any, raw: dict[str, Any]) -> dict[str, Any]:
    """装配综合八字准确性二期的关键边界证据。"""
    calculator = runtime.calculator
    ec = runtime.ec
    true_solar_detail = raw.get("completeTrueSolarTime", {})
    jieqi_detail = raw.get("jieqiDetail", {})
    jiao_yun = raw.get("jiaoYun", {})
    geju = raw.get("geju", {})
    yong_shen = raw.get("yongShen", {})

    return {
        "schemaVersion": 1,
        "timePipeline": {
            "inputLocalTime": runtime.payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "useTrueSolarTime": runtime.payload.use_true_solar_time,
            "trueSolarTime": calculator.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
            "longitude": runtime.payload.longitude,
            "latitude": runtime.payload.latitude,
            "longitudeOffsetMinutes": true_solar_detail.get("longitudeOffsetMinutes"),
            "astronomicalOffsetMinutes": true_solar_detail.get("astronomicalOffsetMinutes"),
            "totalOffsetMinutes": true_solar_detail.get("totalOffsetMinutes"),
            "ziTimeAnalysis": raw.get("ziTimeAnalysis", {}),
        },
        "solarTermBoundary": {
            "yearPillar": ec.getYear(),
            "monthPillar": ec.getMonth(),
            "monthCommand": ec.getMonthZhi(),
            "previousTerm": jieqi_detail.get("prevJieQi", {}),
            "nextTerm": jieqi_detail.get("nextJieQi", {}),
            "description": jieqi_detail.get("description", ""),
        },
        "fortuneStartBoundary": {
            "gender": runtime.payload.gender,
            "startDate": jiao_yun.get("startDate"),
            "description": jiao_yun.get("description", ""),
            "anchorTerm": jiao_yun.get("jiaoJieQi", ""),
        },
        "patternUseGodTrace": {
            "mainPattern": geju.get("main", "") if isinstance(geju, dict) else "",
            "patterns": geju.get("patterns", []) if isinstance(geju, dict) else [],
            "monthPillar": ec.getMonth(),
            "monthHiddenStems": runtime.hidden_stems.get("month", []),
            "yongShenBasis": yong_shen.get("basis", "") if isinstance(yong_shen, dict) else "",
            "yongShenBasisSource": yong_shen.get("basisSource", "") if isinstance(yong_shen, dict) else "",
            "tiaohouRaw": yong_shen.get("tiaohouRaw", "") if isinstance(yong_shen, dict) else "",
        },
    }


def _append_accuracy_evidence(runtime: Any, raw: dict[str, Any]) -> None:
    evidence = raw.get("analysisEvidence")
    if not isinstance(evidence, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return

    guards = raw.get("accuracyGuards", {})
    time_pipeline = guards.get("timePipeline", {}) if isinstance(guards, dict) else {}
    solar_term = guards.get("solarTermBoundary", {}) if isinstance(guards, dict) else {}
    fortune_start = guards.get("fortuneStartBoundary", {}) if isinstance(guards, dict) else {}
    pattern_trace = guards.get("patternUseGodTrace", {}) if isinstance(guards, dict) else {}

    zi_time_analysis = time_pipeline.get("ziTimeAnalysis", {})
    items["timePipeline"] = _evidence_item(
        conclusion={
            "trueSolarTime": time_pipeline.get("trueSolarTime"),
            "totalOffsetMinutes": time_pipeline.get("totalOffsetMinutes"),
            "ziTimeShift": zi_time_analysis.get("zwzShift") if isinstance(zi_time_analysis, dict) else None,
        },
        basis=[
            f"输入时间={time_pipeline.get('inputLocalTime', '')}",
            f"经度={runtime.payload.longitude}",
            f"纬度={runtime.payload.latitude}",
            f"真太阳时={time_pipeline.get('trueSolarTime', '')}",
        ],
        sources=["paipan-master 真太阳时算法", "lunar-python"],
        rule_ids=["bazi.true_solar_time_pipeline", "bazi.zi_time_boundary"],
    )
    items["solarTermBoundary"] = _evidence_item(
        conclusion={
            "yearPillar": solar_term.get("yearPillar"),
            "monthPillar": solar_term.get("monthPillar"),
            "monthCommand": solar_term.get("monthCommand"),
        },
        basis=[
            f"上一节气={solar_term.get('previousTerm', {})}",
            f"下一节气={solar_term.get('nextTerm', {})}",
            f"说明={solar_term.get('description', '')}",
        ],
        sources=["lunar-python", "1900-2030 交节时间 golden fixture"],
        rule_ids=["bazi.solar_term_month_boundary", "bazi.lichun_year_boundary"],
    )
    items["fortuneStartBoundary"] = _evidence_item(
        conclusion={
            "startDate": fortune_start.get("startDate"),
            "anchorTerm": fortune_start.get("anchorTerm"),
        },
        basis=[f"性别={runtime.payload.gender}", f"起运说明={fortune_start.get('description', '')}"],
        sources=["lunar-python EightChar.getYun", "项目起运边界回归"],
        rule_ids=["bazi.fortune_start_boundary"],
        weight="fortune",
    )
    items["patternUseGodTrace"] = _evidence_item(
        conclusion={
            "mainPattern": pattern_trace.get("mainPattern"),
            "yongShenBasisSource": pattern_trace.get("yongShenBasisSource"),
        },
        basis=[
            f"月柱={pattern_trace.get('monthPillar', '')}",
            f"月支藏干={pattern_trace.get('monthHiddenStems', [])}",
            f"调候原始={pattern_trace.get('tiaohouRaw', '')}",
        ],
        sources=["bazi-1", "项目格局/调候规则索引"],
        rule_ids=["bazi.pattern_use_god_trace"],
    )


def _ten_god_values(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            values.extend(_ten_god_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(_ten_god_values(item))
    elif value not in (None, ""):
        values.append(str(value))
    return values


def _relation_order(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """把干支关系按审计优先级整理成稳定结构。"""
    relations = raw.get("ganzhiRelations", {}) if isinstance(raw.get("ganzhiRelations"), dict) else {}
    branch_rel = raw.get("branchRelations", {}) if isinstance(raw.get("branchRelations"), dict) else {}
    extra = raw.get("ganzhiExtra", {}) if isinstance(raw.get("ganzhiExtra"), dict) else {}
    groups = [
        ("hehua", "合化", relations.get("tianGan", []), "先记录天干五合；是否成化需要后续条件字段确认。"),
        ("sanHui", "三会", branch_rel.get("sanHuiDetail") or branch_rel.get("sanHui", []), "三会优先于三合展示。"),
        ("sanHe", "三合", branch_rel.get("sanHeDetail") or branch_rel.get("sanHe", []), "完整三合优先于半合。"),
        ("liuHe", "六合", branch_rel.get("liuHeDetail") or branch_rel.get("liuHe", []), "六合作为结构辅助关系。"),
        (
            "conflict",
            "冲刑害破",
            branch_rel.get("conflictsDetail") or branch_rel.get("conflicts", []),
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


def _fortune_triggers(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """抽取岁运触发点：只做结构提示，不输出确定性断语。"""
    pillars = raw.get("fourPillars", {}) if isinstance(raw.get("fourPillars"), dict) else {}
    day_pillar = pillars.get("day", {}) if isinstance(pillars.get("day"), dict) else {}
    day_gz = day_pillar.get("fullName", "")
    major = raw.get("majorFortune", {}) if isinstance(raw.get("majorFortune"), dict) else {}
    major_pillars = major.get("pillars", []) if isinstance(major.get("pillars"), list) else []
    annual = raw.get("annualFortune", []) if isinstance(raw.get("annualFortune"), list) else []
    triggers: list[dict[str, Any]] = []
    active_major = next((item for item in major_pillars if isinstance(item, dict) and item.get("isCurrent")), None)
    active_major_gz = (active_major or {}).get("ganZhi") or (active_major or {}).get("fullName", "")
    for item in annual[:24]:
        if not isinstance(item, dict):
            continue
        gz = item.get("ganZhi") or item.get("fullName", "")
        reasons = []
        if gz and gz == day_gz:
            reasons.append("流年与日柱伏吟")
        if gz and active_major_gz and gz == active_major_gz:
            reasons.append("岁运并临")
        if len(gz) >= 2 and len(day_gz) >= 2 and gz[1] == day_gz[1]:
            reasons.append("流年地支与日支同气")
        if reasons:
            triggers.append(
                {
                    "year": item.get("year"),
                    "ganZhi": gz,
                    "activeMajorFortune": active_major_gz,
                    "reasons": reasons,
                    "riskBoundary": "只作趋势触发证据，不作确定未来断语。",
                }
            )
    return triggers


def _build_yongshen_strategies(raw: dict[str, Any]) -> list[dict[str, Any]]:
    yong_shen = raw.get("yongShen", {}) if isinstance(raw.get("yongShen"), dict) else {}
    day_master = raw.get("dayMaster", {}) if isinstance(raw.get("dayMaster"), dict) else {}
    strength = str(day_master.get("strength", ""))
    tiao_hou = yong_shen.get("tiaoHou", {}) if isinstance(yong_shen.get("tiaoHou"), dict) else {}
    strategies = [
        {
            "strategy": "调候",
            "conclusion": tiao_hou,
            "basis": yong_shen.get("basis", ""),
            "source": yong_shen.get("basisSource", ""),
            "ruleIds": ["bazi.regulating_climate"],
        },
        {
            "strategy": "扶抑",
            "conclusion": "偏弱先看印比扶助；偏强先看泄耗制化；中和以格局和调候优先。",
            "basis": f"日主强弱={strength}",
            "source": "项目扶抑策略边界",
            "ruleIds": ["bazi.day_master_strength", "bazi.balance_five_elements"],
        },
        {
            "strategy": "通关",
            "conclusion": "仅在合冲克战明显时作为冲突调解策略登记。",
            "basis": raw.get("ganzhiRelations", {}),
            "source": "项目干支关系规则",
            "ruleIds": ["bazi.stem_branch_relations"],
        },
        {
            "strategy": "病药",
            "conclusion": "以五行偏枯、寒暖燥湿和格局成败共同判断，当前只登记依据不作强断。",
            "basis": raw.get("climateScores", {}),
            "source": "项目调候与五行平衡规则",
            "ruleIds": ["bazi.regulating_climate", "bazi.balance_five_elements"],
        },
    ]
    return strategies


def _build_bazi_benchmark(raw: dict[str, Any]) -> dict[str, Any]:
    ten_gods = _ten_god_values(raw.get("tenGods", {}))
    ten_god_counts = {name: ten_gods.count(name) for name in sorted(set(ten_gods)) if name}
    geju = raw.get("geju", {}) if isinstance(raw.get("geju"), dict) else {}
    return {
        "schemaVersion": 1,
        "boundary": "标杆加固结构层；默认 Markdown 可选择摘要展示，核心事实仍以原始字段为准。",
        "timeBoundaryGolden": {
            "trueSolarTime": raw.get("trueSolarTime"),
            "ziTimeAnalysis": raw.get("ziTimeAnalysis", {}),
            "solarTermBoundary": raw.get("accuracyGuards", {}).get("solarTermBoundary", {})
            if isinstance(raw.get("accuracyGuards"), dict)
            else {},
            "ruleIds": ["bazi.true_solar_time_pipeline", "bazi.zi_time_boundary", "bazi.solar_term_month_boundary"],
        },
        "renYuanSiling": {
            "siling": raw.get("siling", {}),
            "monthCommand": raw.get("accuracyGuards", {}).get("solarTermBoundary", {}).get("monthCommand")
            if isinstance(raw.get("accuracyGuards"), dict)
            else "",
            "wuxingState": raw.get("wuxingState", {}),
            "monthHiddenStems": raw.get("hiddenStems", {}).get("month", {})
            if isinstance(raw.get("hiddenStems"), dict)
            else {},
            "ruleIds": ["bazi.month_command_priority", "bazi.renyuan_siling_weight"],
        },
        "strengthScore": {
            "label": raw.get("dayMaster", {}).get("strength", {}) if isinstance(raw.get("dayMaster"), dict) else "",
            "weak": raw.get("wuxingScores", {}).get("weak") if isinstance(raw.get("wuxingScores"), dict) else None,
            "strongScore": raw.get("wuxingScores", {}).get("strongScore")
            if isinstance(raw.get("wuxingScores"), dict)
            else None,
            "statusDetail": raw.get("wuxingScores", {}).get("statusDetail", [])
            if isinstance(raw.get("wuxingScores"), dict)
            else [],
            "fiveElementScore": raw.get("wuxingScores", {}).get("fiveElementScore", {})
            if isinstance(raw.get("wuxingScores"), dict)
            else {},
            "ruleIds": ["bazi.day_master_strength", "bazi.strength_score_golden"],
        },
        "ganzhiPriority": _relation_order(raw),
        "fortuneTriggers": _fortune_triggers(raw),
        "patternRegistry": {
            "main": geju.get("main", ""),
            "patterns": geju.get("patterns", []),
            "status": "seed",
            "boundary": "第一批只锁当前格局事实和可追溯依据；从格、化气等高级格局后续逐条补 golden。",
            "ruleIds": ["bazi.pattern_by_month_command", "bazi.pattern_root_transparency"],
        },
        "yongShenStrategies": _build_yongshen_strategies(raw),
        "tenGodStructure": {
            "counts": ten_god_counts,
            "basis": "从 tenGods 字段递归统计，仅作结构摘要。",
            "ruleIds": ["bazi.ten_god_structure"],
        },
        "topicProfiles": [
            {"topic": "事业", "basis": ["格局", "官杀", "大运流年"], "visibility": "standalone_future"},
            {"topic": "财运", "basis": ["财星", "用神", "岁运触发"], "visibility": "standalone_future"},
            {"topic": "婚姻", "basis": ["夫妻宫", "财官星", "岁运触发"], "visibility": "standalone_future"},
            {
                "topic": "健康",
                "basis": ["五行偏枯", "寒暖燥湿"],
                "visibility": "standalone_future",
                "risk": "需要增强免责声明",
            },
            {"topic": "学业", "basis": ["印星", "食伤", "大运流年"], "visibility": "standalone_future"},
            {"topic": "迁移", "basis": ["驿马", "冲合", "岁运触发"], "visibility": "standalone_future"},
        ],
    }


def _append_bazi_benchmark_evidence(raw: dict[str, Any]) -> None:
    evidence = raw.get("analysisEvidence")
    benchmark = raw.get("baziBenchmark")
    if not isinstance(evidence, dict) or not isinstance(benchmark, dict):
        return
    items = evidence.setdefault("items", {})
    if not isinstance(items, dict):
        return
    items["baziBenchmark"] = _evidence_item(
        conclusion={
            "hasTimeBoundary": bool(benchmark.get("timeBoundaryGolden")),
            "hasRenyuan": bool(benchmark.get("renYuanSiling")),
            "hasStrengthScore": bool(benchmark.get("strengthScore")),
            "fortuneTriggerCount": len(benchmark.get("fortuneTriggers", []))
            if isinstance(benchmark.get("fortuneTriggers"), list)
            else 0,
        },
        basis=[
            "baziBenchmark.timeBoundaryGolden",
            "baziBenchmark.renYuanSiling",
            "baziBenchmark.strengthScore",
            "baziBenchmark.ganzhiPriority",
            "baziBenchmark.fortuneTriggers",
            "baziBenchmark.yongShenStrategies",
        ],
        sources=["lunar-python", "bazi-1", "项目标杆加固规则"],
        rule_ids=[
            "bazi.renyuan_siling_weight",
            "bazi.strength_score_golden",
            "bazi.ganzhi_priority",
            "bazi.fortune_trigger_boundary",
            "bazi.yongshen_strategy",
            "bazi.ten_god_structure",
            "bazi.topic_profile_boundary",
        ],
    )


def calculate_pure_analysis(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算纯命理分析字段集合。"""
    runtime = build_pure_analysis_runtime(
        LegacyBaziInput(
            birth_dt=payload.birth_dt,
            gender=normalize_gender(payload.gender),
            longitude=payload.longitude,
            latitude=payload.latitude,
            name=payload.name,
            birth_place=payload.birth_place,
            use_true_solar_time=payload.use_true_solar_time,
        )
    )
    raw = {}
    raw.update(build_base_chart_section(runtime))
    raw.update(build_fortune_section(runtime))
    raw.update(build_classical_section(runtime))
    raw["analysisEvidence"] = runtime.calculator._calc_analysis_evidence(
        four_pillars=runtime.four_pillars,
        hidden_stems=runtime.hidden_stems,
        day_master=raw.get("dayMaster", {}),
        wuxing_scores=raw.get("wuxingScores", {}),
        geju=raw.get("geju", {}),
        yongshen=raw.get("yongShen", {}),
        ganzhi_relations=raw.get("ganzhiRelations", {}),
        branch_relations=raw.get("branchRelations", {}),
        spirits=raw.get("spiritsFull", {}),
        bone_weight=raw.get("boneWeight", {}),
    )
    raw["accuracyGuards"] = _build_accuracy_guards(runtime, raw)
    _append_accuracy_evidence(runtime, raw)
    raw["baziBenchmark"] = _build_bazi_benchmark(raw)
    _append_bazi_benchmark_evidence(raw)
    projected = project_by_profile(raw, "pure_analysis")
    translated = runtime.calculator._translate_to_chinese(projected)
    safe_result = runtime.calculator._json_safe(translated)
    if not isinstance(safe_result, dict):
        raise RuntimeError("纯分析结果必须是 JSON 对象")
    return dict(safe_result)
