from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fate_core.adapters import LegacyBaziInput
from fate_core.kernel.projector import project_by_profile
from fate_core.providers import (
    build_base_chart_section,
    build_classical_section,
    build_fortune_section,
    build_pure_analysis_runtime,
)
from fate_core.usecases.evaluators import (
    BRANCH_CLASH,
    ELEMENT_CONTROLS,
    GAN_ELEMENT,
    build_fortune_trigger_matrix,
    build_strength_score,
    build_ten_god_structure,
    ten_god_families,
    ten_god_values,
)
from fate_core.usecases.evaluators import (
    build_combine_transform_matrix as _build_combine_transform_matrix,
)
from fate_core.usecases.evaluators import (
    build_regular_pattern_candidates as _build_regular_pattern_candidates,
)
from fate_core.usecases.evaluators import (
    build_relation_order as _relation_order,
)
from fate_core.usecases.evaluators import (
    build_special_pattern_candidates as _build_special_pattern_candidates,
)
from fate_core.usecases.evaluators import (
    build_topic_profiles as _build_topic_profiles,
)
from fate_core.usecases.evaluators import (
    build_yongshen_decision as _build_yongshen_decision,
)
from fate_core.usecases.evaluators import (
    relation_families as _relation_families,
)
from fate_core.usecases.evaluators import (
    temperature_band as _temperature_band,
)
from fate_core.usecases.evidence_builder import (
    append_accuracy_evidence,
    append_bazi_benchmark_evidence,
    append_bazi_rule_depth_evidence,
    ensure_evidence_risk_boundaries,
)
from fate_core.usecases.rule_depth import (
    build_combination_statement,
    build_conflict_resolution,
    build_narrative_summary,
    build_rule_application,
    build_weight_profile,
    collect_source_rule_ids,
    registry_version,
    rules_for_system,
)

# Principle gate evidence:
# target end state: pure-analysis composes providers and evidence without owning transport.
# real constraints: CLI/API users pass ISO and wall-time strings today.
# inertia constraints: accepted input formats are contract migration, not parser proliferation.
# kill list: report rendering, Bot/Web coupling, and unregistered rule conclusions.
# proof point: API contracts, service contracts, and bazi rule-depth tests pass.
# falsifier: usecase imports delivery modules or emits unsupported deterministic claims.
# migration slice: normalize input here until public callers move to one canonical schema.
# existence: current consumer is pure analysis; owner is fate-core; verification is pytest.


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


DEFAULT_INPUT_TIMEZONE = "Asia/Shanghai"


def _parse_zoneinfo(value: str | None) -> ZoneInfo:
    zone_name = (value or DEFAULT_INPUT_TIMEZONE).strip() or DEFAULT_INPUT_TIMEZONE
    try:
        return ZoneInfo(zone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"无法识别时区: {zone_name}") from exc


def _strip_to_target_wall_time(parsed: datetime, target_timezone: str | None = None) -> datetime:
    if parsed.tzinfo is None:
        return parsed
    return parsed.astimezone(_parse_zoneinfo(target_timezone)).replace(tzinfo=None)


def parse_datetime(value: str, target_timezone: str | None = None) -> datetime:
    """解析出生时间，兼容 CLI/API 常见输入格式。"""
    normalized = value.strip()
    if not normalized:
        raise ValueError("birthDateTime 不能为空")
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
        return _strip_to_target_wall_time(parsed, target_timezone)
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
    input_timezone = _first_non_empty(
        raw_payload.get("timezone"),
        raw_payload.get("inputTimezone"),
        birth_place_object.get("timezone"),
        options.get("timezone"),
        DEFAULT_INPUT_TIMEZONE,
    )

    normalized = {
        "birthDateTime": birth_datetime,
        "gender": _first_non_empty(raw_payload.get("gender"), raw_payload.get("sex")),
        "longitude": longitude,
        "latitude": latitude,
        "name": raw_payload.get("name"),
        "birthPlace": birth_place_name or "",
        "useTrueSolarTime": _parse_bool(use_true_solar_time, default=True),
        "inputTimezone": str(input_timezone),
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
        birth_dt=parse_datetime(str(normalized["birthDateTime"]), target_timezone=str(normalized["inputTimezone"])),
        gender=str(normalized["gender"]),
        longitude=normalized["longitude"],
        latitude=normalized["latitude"],
        name=normalized["name"],
        birth_place=str(normalized["birthPlace"]),
        use_true_solar_time=normalized["useTrueSolarTime"],
    )


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
        trigger_types = []
        if gz and gz == day_gz:
            reasons.append("流年与日柱伏吟")
            trigger_types.append("fu_yin")
        if gz and active_major_gz and gz == active_major_gz:
            reasons.append("岁运并临")
            trigger_types.append("sui_yun_bing_lin")
        if len(gz) >= 2 and len(day_gz) >= 2 and gz[1] == day_gz[1]:
            reasons.append("流年地支与日支同气")
            trigger_types.append("annual_trigger")
        if len(gz) >= 2 and len(day_gz) >= 2 and BRANCH_CLASH.get(gz[1]) == day_gz[1]:
            annual_controls_day = ELEMENT_CONTROLS.get(GAN_ELEMENT.get(gz[0], "")) == GAN_ELEMENT.get(day_gz[0], "")
            day_controls_annual = ELEMENT_CONTROLS.get(GAN_ELEMENT.get(day_gz[0], "")) == GAN_ELEMENT.get(gz[0], "")
            if annual_controls_day or day_controls_annual:
                reasons.append("流年与日柱天克地冲/反吟")
                trigger_types.extend(["fan_yin", "tian_ke_di_chong"])
        if reasons:
            triggers.append(
                {
                    "year": item.get("year"),
                    "ganZhi": gz,
                    "activeMajorFortune": active_major_gz,
                    "triggerTypes": sorted(set(trigger_types)),
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
    ten_gods = ten_god_values(raw.get("tenGods", {}))
    ten_god_counts = {name: ten_gods.count(name) for name in sorted(set(ten_gods)) if name}
    geju = raw.get("geju", {}) if isinstance(raw.get("geju"), dict) else {}
    relation_order = _relation_order(raw)
    fortune_triggers = _fortune_triggers(raw)
    yongshen_strategies = _build_yongshen_strategies(raw)
    combine_matrix = _build_combine_transform_matrix(raw)
    regular_candidates = _build_regular_pattern_candidates(raw)
    special_candidates = _build_special_pattern_candidates(raw, combine_matrix)
    yongshen_decision = _build_yongshen_decision(raw, yongshen_strategies)
    fortune_trigger_matrix = build_fortune_trigger_matrix(raw, fortune_triggers)
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
        "strengthScore": build_strength_score(
            raw,
            {
                "siling": raw.get("siling", {}),
                "monthCommand": raw.get("accuracyGuards", {}).get("solarTermBoundary", {}).get("monthCommand")
                if isinstance(raw.get("accuracyGuards"), dict)
                else "",
            },
        ),
        "ganzhiPriority": relation_order,
        "combineTransformMatrix": combine_matrix,
        "fortuneTriggers": fortune_triggers,
        "patternRegistry": {
            "main": geju.get("main", ""),
            "patterns": geju.get("patterns", []),
            "status": "seed",
            "regularPatternCandidates": regular_candidates,
            "specialPatternCandidates": special_candidates,
            "boundary": "格局事实、特殊候选和成败条件分层呈现；从格、化气等高级格局必须逐条补 golden。",
            "ruleIds": ["bazi.pattern_by_month_command", "bazi.pattern_root_transparency"],
        },
        "yongShenStrategies": yongshen_strategies,
        "yongShenDecision": yongshen_decision,
        "fortuneTriggerMatrix": fortune_trigger_matrix,
        "tenGodStructure": build_ten_god_structure(raw),
        "topicProfiles": _build_topic_profiles(
            raw,
            ten_god_counts,
            fortune_triggers,
            yongshen_decision,
            fortune_trigger_matrix,
        ),
    }


def _rule_map(system: str) -> dict[str, dict[str, Any]]:
    return {str(rule.get("id", "")): rule for rule in rules_for_system(system)}


def _build_bazi_rule_depth(raw: dict[str, Any]) -> dict[str, Any]:
    """装配八字规则深度层：规则来自 registry，证据来自现有生产字段。"""
    rules = _rule_map("bazi")
    benchmark = raw.get("baziBenchmark", {}) if isinstance(raw.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    renyuan = benchmark.get("renYuanSiling", {}) if isinstance(benchmark.get("renYuanSiling"), dict) else {}
    pattern = benchmark.get("patternRegistry", {}) if isinstance(benchmark.get("patternRegistry"), dict) else {}
    yongshen = benchmark.get("yongShenStrategies", [])
    yongshen_decision = (
        benchmark.get("yongShenDecision", {}) if isinstance(benchmark.get("yongShenDecision"), dict) else {}
    )
    ten_god = benchmark.get("tenGodStructure", {}) if isinstance(benchmark.get("tenGodStructure"), dict) else {}
    relation = benchmark.get("ganzhiPriority", [])
    combine_matrix = (
        benchmark.get("combineTransformMatrix", {}) if isinstance(benchmark.get("combineTransformMatrix"), dict) else {}
    )
    special_candidates = (
        pattern.get("specialPatternCandidates", {}) if isinstance(pattern.get("specialPatternCandidates"), dict) else {}
    )
    regular_candidates = (
        pattern.get("regularPatternCandidates", {}) if isinstance(pattern.get("regularPatternCandidates"), dict) else {}
    )
    fortune = benchmark.get("fortuneTriggers", [])
    monthly = raw.get("monthlyFortune", [])
    spirits = raw.get("spiritsFull", {})
    bone = raw.get("boneWeight", {})

    applied = [
        build_rule_application(
            rules["bazi.depth.strength.month_root_transparency"],
            status="applied" if strength and renyuan else "partial",
            confidence=0.9 if strength and renyuan else 0.55,
            evidence={
                "strengthLabel": strength.get("label"),
                "strongScore": strength.get("strongScore"),
                "score": strength.get("score"),
                "basis": strength.get("basis", []),
                "sourceRuleId": strength.get("sourceRuleId", ""),
                "conflicts": strength.get("conflicts", []),
                "monthCommand": renyuan.get("monthCommand"),
                "currentSiling": renyuan.get("siling", {}).get("current")
                if isinstance(renyuan.get("siling"), dict)
                else "",
                "monthHiddenStems": renyuan.get("monthHiddenStems"),
            },
            notes=["强弱仍保留灰度标签，避免单一分数硬断。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.establishment"],
            status="applied" if pattern.get("main") or pattern.get("patterns") else "partial",
            confidence=0.82 if pattern.get("main") or pattern.get("patterns") else 0.5,
            evidence={
                "mainPattern": pattern.get("main"),
                "patterns": pattern.get("patterns", []),
                "regularPatternCandidates": regular_candidates,
                "relationPriorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
            },
            notes=["候选格局必须结合成败条件继续审查。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.regular_vs_special"],
            status="applied" if pattern.get("main") else "partial",
            confidence=0.8 if pattern.get("main") else 0.48,
            evidence={
                "mainPattern": pattern.get("main"),
                "patternStatus": pattern.get("status"),
                "regularPatternCandidates": regular_candidates,
                "advancedPatternBoundary": pattern.get("boundary"),
            },
            notes=["正格、变格、从格、化气先走候选和边界登记。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.follow_transform_guard"],
            status="applied" if special_candidates or combine_matrix else "guarded",
            confidence=0.76 if special_candidates or combine_matrix else 0.7,
            evidence={
                "mainPattern": pattern.get("main"),
                "specialPatternCandidates": special_candidates,
                "combineTransformMatrix": combine_matrix,
                "guard": "从格、化气、专旺具备条件矩阵后仍需 golden case，未达完整条件时不得强断。",
            },
            notes=["高级格局已有条件链字段；定格仍必须等待专门 golden 扩充后提升置信度。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.special_pattern_checklist"],
            status="applied" if special_candidates.get("candidates") else "guarded",
            confidence=0.72 if special_candidates.get("candidates") else 0.66,
            evidence={
                "mainPattern": pattern.get("main"),
                "candidates": special_candidates.get("candidates", []),
                "dominantFamily": special_candidates.get("dominantFamily", {}),
                "guard": "特殊格局开放候选成熟度和条件链，不在缺少完整证据时定格。",
            },
            notes=["特殊格局以候选矩阵输出，不输出市场化强断。"],
        ),
        build_rule_application(
            rules["bazi.depth.pattern.finance_official_seal_food_matrix"],
            status="applied" if ten_god.get("counts") and pattern.get("main") else "partial",
            confidence=0.71 if ten_god.get("counts") and pattern.get("main") else 0.45,
            evidence={
                "mainPattern": pattern.get("main"),
                "roleFamilies": ten_god_families(ten_god.get("counts", {})),
            },
            notes=["财官印食作为组合矩阵，不替代月令定格和成败条件。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.strategy_matrix"],
            status="applied" if isinstance(yongshen, list) and yongshen else "partial",
            confidence=0.84 if isinstance(yongshen, list) and len(yongshen) >= 4 else 0.6,
            evidence={
                "strategyCount": len(yongshen) if isinstance(yongshen, list) else 0,
                "strategies": [item.get("strategy") for item in yongshen if isinstance(item, dict)],
                "decision": yongshen_decision,
                "climateScores": raw.get("climateScores", {}),
                "fiveElementScore": strength.get("fiveElementScore", {}),
            },
            notes=["调候、扶抑、通关、病药按证据评分排序，但并列保留，不互相覆盖。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.tiaohou_priority"],
            status="applied" if raw.get("climateScores") else "partial",
            confidence=0.79 if raw.get("climateScores") else 0.52,
            evidence={
                "climateScores": raw.get("climateScores", {}),
                "tiaohouRaw": raw.get("yongShen", {}).get("tiaohouRaw")
                if isinstance(raw.get("yongShen"), dict)
                else "",
                "strategyNames": [item.get("strategy") for item in yongshen if isinstance(item, dict)]
                if isinstance(yongshen, list)
                else [],
            },
            notes=["寒暖燥湿优先作为调候证据，不直接覆盖扶抑策略。"],
        ),
        build_rule_application(
            rules["bazi.depth.yongshen.climate_detail_matrix"],
            status="applied" if raw.get("climateScores") else "partial",
            confidence=0.74 if raw.get("climateScores") else 0.46,
            evidence={
                "temperatureBand": _temperature_band(raw.get("climateScores", {})),
                "climateScores": raw.get("climateScores", {}),
                "strategyNames": [item.get("strategy") for item in yongshen if isinstance(item, dict)]
                if isinstance(yongshen, list)
                else [],
            },
            notes=["调候细分只影响解释权重，不直接输出生活处方。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.structure_profile"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.76 if ten_god.get("counts") else 0.5,
            evidence={
                "counts": ten_god.get("counts", {}),
                "basis": ten_god.get("basis", ""),
                "basisEvidence": ten_god.get("basisEvidence", []),
                "sourceRuleId": ten_god.get("sourceRuleId", ""),
            },
            notes=["十神组合以透干、藏干和位置为后续深化方向。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.overlap_profile"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.72 if ten_god.get("counts") else 0.48,
            evidence={
                "counts": ten_god.get("counts", {}),
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=3),
                "basis": ten_god.get("basis", ""),
                "basisEvidence": ten_god.get("basisEvidence", []),
            },
            notes=["十神重叠只给组合倾向，不把单项十神写成人生定论。"],
        ),
        build_rule_application(
            rules["bazi.depth.tengod.role_family_matrix"],
            status="applied" if ten_god.get("counts") else "partial",
            confidence=0.7 if ten_god.get("counts") else 0.45,
            evidence={
                "roleFamilies": ten_god_families(ten_god.get("counts", {})),
                "families": ten_god.get("families", {}),
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=5),
                "basisEvidence": ten_god.get("basisEvidence", []),
            },
            notes=["财官印食、比劫、食伤、官杀等族群只作结构摘要。"],
        ),
        build_rule_application(
            rules["bazi.depth.climate.seasonal_adjustment"],
            status="applied" if raw.get("climateScores") and renyuan else "partial",
            confidence=0.73 if raw.get("climateScores") and renyuan else 0.5,
            evidence={
                "monthCommand": renyuan.get("monthCommand"),
                "climateScores": raw.get("climateScores", {}),
                "currentSiling": renyuan.get("siling", {}).get("current")
                if isinstance(renyuan.get("siling"), dict)
                else "",
            },
            notes=["季节寒暖燥湿只作为调候依据，不替代格局判定。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.collision_priority"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.78 if isinstance(relation, list) and relation else 0.45,
            evidence={
                "priority": [
                    {
                        "key": item.get("key"),
                        "label": item.get("label"),
                        "count": item.get("count"),
                        "boundary": item.get("boundary"),
                    }
                    for item in relation
                    if isinstance(item, dict)
                ]
            },
            notes=["合化是否成化继续要求依据字段，当前不作强断。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.combine_transform_guard"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.7 if isinstance(relation, list) and relation else 0.46,
            evidence={
                "priorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
                "combineTransformMatrix": combine_matrix,
                "guard": "合、冲、刑、害、破先登记结构触发；合化成败另需月令、透干、通根和阻隔证据。",
            },
            notes=["合化判断有条件矩阵，不从关系名称直接跳到成化结论。"],
        ),
        build_rule_application(
            rules["bazi.depth.relation.punishment_harm_break_matrix"],
            status="applied" if isinstance(relation, list) and relation else "partial",
            confidence=0.67 if isinstance(relation, list) and relation else 0.43,
            evidence={
                "relationFamilies": _relation_families(relation),
                "priorityKeys": [item.get("key") for item in relation if isinstance(item, dict)],
            },
            notes=["刑冲害破只说明结构摩擦，不输出恐吓式事件。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.trigger_chain"],
            status="applied" if isinstance(fortune, list) else "partial",
            confidence=0.72 if isinstance(fortune, list) else 0.4,
            evidence={
                "triggerCount": len(fortune) if isinstance(fortune, list) else 0,
                "sampleTriggers": fortune[:5] if isinstance(fortune, list) else [],
                "triggerMatrix": benchmark.get("fortuneTriggerMatrix", {}),
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
            },
            notes=["动态层只说明触发链，不覆盖原局结构。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.decade_year_month_order"],
            status="applied" if raw.get("majorFortune") and raw.get("annualFortune") else "partial",
            confidence=0.69 if raw.get("majorFortune") and raw.get("annualFortune") else 0.44,
            evidence={
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
                "monthlyFortuneCount": len(monthly) if isinstance(monthly, list) else 0,
            },
            notes=["大运定阶段，流年定触发，流月只细化窗口。"],
        ),
        build_rule_application(
            rules["bazi.depth.fortune.month_trigger"],
            status="applied" if isinstance(monthly, list) and monthly else "partial",
            confidence=0.68 if isinstance(monthly, list) and monthly else 0.42,
            evidence={
                "monthlyFortuneCount": len(monthly) if isinstance(monthly, list) else 0,
                "sampleMonths": monthly[:3] if isinstance(monthly, list) else [],
            },
            notes=["流月只作短周期触发证据，必须受原局和大运流年约束。"],
        ),
        build_rule_application(
            rules["bazi.depth.auxiliary.boundary_guard"],
            status="applied" if spirits or bone else "partial",
            confidence=0.8 if spirits or bone else 0.5,
            evidence={
                "hasSpirits": bool(spirits),
                "hasBoneWeight": bool(bone),
                "weightBoundary": "神煞/称骨不参与核心强弱、喜忌和格局定性。",
            },
            notes=["辅助体系保留展示边界，防止污染综合八字核心判断。"],
        ),
        build_rule_application(
            rules["bazi.depth.statement.combination_boundary"],
            status="applied",
            confidence=0.74,
            evidence={
                "statementInputs": ["日主强弱", "格局", "用神策略", "十神组合", "岁运触发"],
                "guard": "组合断语必须同时给出规则 ID、证据字段和风险边界。",
            },
            notes=["组合断语输出为审计摘要，不新增不可追溯结论。"],
        ),
        build_rule_application(
            rules["bazi.depth.statement.narrative_markdown"],
            status="applied",
            confidence=0.72,
            evidence={
                "target": "baziRuleDepth.narrativeSummary",
                "format": "markdown",
            },
            notes=["自然语言报告只从组合断语生成，保留规则 ID。"],
        ),
    ]
    conflict_matrix = [
        {
            "type": "strategy_priority",
            "topic": "用神策略冲突",
            "rules": ["bazi.depth.yongshen.strategy_matrix", "bazi.depth.yongshen.tiaohou_priority"],
            "policy": "调候、扶抑、通关、病药并列，按证据完整度和风险边界解释。",
        },
        {
            "type": "pattern_candidate",
            "topic": "格局候选冲突",
            "rules": [
                "bazi.depth.pattern.establishment",
                "bazi.depth.pattern.regular_vs_special",
                "bazi.depth.pattern.follow_transform_guard",
                "bazi.depth.pattern.special_pattern_checklist",
                "bazi.depth.pattern.finance_official_seal_food_matrix",
            ],
            "policy": "普通格局、正格、特殊格局按成败条件分层，不把候选写成定格。",
        },
        {
            "type": "relation_boundary",
            "topic": "干支合化边界",
            "rules": [
                "bazi.depth.relation.collision_priority",
                "bazi.depth.relation.combine_transform_guard",
                "bazi.depth.relation.punishment_harm_break_matrix",
            ],
            "policy": "先登记合冲刑害破，再按月令、透干、通根和阻隔证据判断是否成化；缺证据时只保留合象。",
        },
        {
            "type": "time_hierarchy",
            "topic": "动态层级顺序",
            "rules": [
                "bazi.depth.fortune.trigger_chain",
                "bazi.depth.fortune.decade_year_month_order",
                "bazi.depth.fortune.month_trigger",
            ],
            "policy": "原局优先，大运定阶段，流年定触发，流月只细化窗口。",
        },
        {
            "type": "auxiliary_boundary",
            "topic": "辅助体系边界",
            "rules": ["bazi.depth.auxiliary.boundary_guard"],
            "policy": "神煞和称骨只可辅助，不参与核心喜忌和格局裁决。",
        },
    ]
    conflict_resolution = build_conflict_resolution(applied, conflict_matrix)
    combination_statements = _build_bazi_combination_statements(raw, applied)
    return {
        "schemaVersion": 1,
        "registryVersion": registry_version(),
        "system": "bazi",
        "boundary": "规则深度层只组织可追溯证据和冲突策略；默认报告仍保持综合八字结构边界。",
        "appliedRules": applied,
        "conflictMatrix": conflict_matrix,
        "conflictResolution": conflict_resolution,
        "weightProfile": build_weight_profile(applied),
        "combinationStatements": combination_statements,
        "narrativeSummary": build_narrative_summary(
            title="综合八字规则摘要",
            combination_statements=combination_statements,
            conflict_resolution=conflict_resolution,
        ),
        "sourceRuleIds": collect_source_rule_ids(applied),
    }


def _dominant_counts(counts: Any, *, limit: int) -> list[dict[str, Any]]:
    if not isinstance(counts, dict):
        return []
    items = sorted(
        ((str(name), int(value)) for name, value in counts.items() if isinstance(value, int | float)),
        key=lambda item: item[1],
        reverse=True,
    )
    return [{"name": name, "count": count} for name, count in items[:limit]]


def _build_bazi_combination_statements(raw: dict[str, Any], applied: list[dict[str, Any]]) -> list[dict[str, Any]]:
    benchmark = raw.get("baziBenchmark", {}) if isinstance(raw.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    pattern = benchmark.get("patternRegistry", {}) if isinstance(benchmark.get("patternRegistry"), dict) else {}
    ten_god = benchmark.get("tenGodStructure", {}) if isinstance(benchmark.get("tenGodStructure"), dict) else {}
    yongshen = benchmark.get("yongShenStrategies", [])
    yongshen_decision = (
        benchmark.get("yongShenDecision", {}) if isinstance(benchmark.get("yongShenDecision"), dict) else {}
    )
    relation = benchmark.get("ganzhiPriority", [])
    combine_matrix = (
        benchmark.get("combineTransformMatrix", {}) if isinstance(benchmark.get("combineTransformMatrix"), dict) else {}
    )
    special_candidates = (
        pattern.get("specialPatternCandidates", {}) if isinstance(pattern.get("specialPatternCandidates"), dict) else {}
    )
    applied_ids = {str(item.get("ruleId", "")) for item in applied}

    statements = [
        build_combination_statement(
            topic="强弱-格局-用神",
            statement="先以月令和日主强弱定结构背景，再用格局与用神策略解释取舍；不同策略并列保留，不压成单一喜忌。",
            rule_ids=[
                "bazi.depth.strength.month_root_transparency",
                "bazi.depth.pattern.establishment",
                "bazi.depth.yongshen.strategy_matrix",
            ],
            evidence={
                "strengthLabel": strength.get("label"),
                "mainPattern": pattern.get("main"),
                "strategyCount": len(yongshen) if isinstance(yongshen, list) else 0,
                "primaryYongShenStrategy": yongshen_decision.get("primaryStrategy"),
            },
            confidence=0.82,
            risk_boundary="该断语只说明解释顺序，不输出确定事件。",
        ),
        build_combination_statement(
            topic="十神组合",
            statement="十神数量和族群用于提示结构重心，必须回到透干、藏干和柱位；财官印食等族群只作观察入口。",
            rule_ids=[
                "bazi.depth.tengod.structure_profile",
                "bazi.depth.tengod.overlap_profile",
                "bazi.depth.tengod.role_family_matrix",
            ],
            evidence={
                "dominantTenGods": _dominant_counts(ten_god.get("counts", {}), limit=3),
                "roleFamilies": ten_god_families(ten_god.get("counts", {})),
            },
            confidence=0.72,
            risk_boundary="不得用单一十神标签替代完整八字判断。",
        ),
        build_combination_statement(
            topic="特殊格局边界",
            statement="从格、化气、专旺等特殊格局只开放检查清单；缺少完整成败条件时，仍以普通格局和候选缺口呈现。",
            rule_ids=[
                "bazi.depth.pattern.regular_vs_special",
                "bazi.depth.pattern.special_pattern_checklist",
                "bazi.depth.pattern.follow_transform_guard",
            ],
            evidence={
                "mainPattern": pattern.get("main"),
                "advancedPatternBoundary": pattern.get("boundary"),
                "candidates": special_candidates.get("candidates", []),
            },
            confidence=0.66,
            risk_boundary="特殊格局不得在证据不足时强行定格。",
        ),
        build_combination_statement(
            topic="调候细分",
            statement="寒暖燥湿先决定调候解释权重，再和扶抑、通关、病药并列；调候细分不替代完整用神判断。",
            rule_ids=[
                "bazi.depth.yongshen.tiaohou_priority",
                "bazi.depth.yongshen.climate_detail_matrix",
                "bazi.depth.climate.seasonal_adjustment",
            ],
            evidence={
                "temperatureBand": _temperature_band(raw.get("climateScores", {})),
                "climateScores": raw.get("climateScores", {}),
            },
            confidence=0.74,
            risk_boundary="调候解释不等于医疗、养生或现实处方。",
        ),
        build_combination_statement(
            topic="干支关系",
            statement="合冲刑害破先作为结构触发排序，合化成败另看月令、透干、通根与阻隔证据；刑害破只作结构摩擦提示。",
            rule_ids=[
                "bazi.depth.relation.collision_priority",
                "bazi.depth.relation.combine_transform_guard",
                "bazi.depth.relation.punishment_harm_break_matrix",
            ],
            evidence={
                "relationKeys": [item.get("key") for item in relation if isinstance(item, dict)],
                "relationFamilies": _relation_families(relation),
                "combineTransformStatus": combine_matrix.get("status"),
                "combineTransformCandidates": combine_matrix.get("candidates", []),
            },
            confidence=0.7,
            risk_boundary="缺少成化证据时只登记合象，不写成已成化。",
        ),
        build_combination_statement(
            topic="岁运层级",
            statement="原局是底盘，大运给阶段，流年给触发，流月只细化时间窗口；动态层不得覆盖原局结构。",
            rule_ids=[
                "bazi.depth.fortune.trigger_chain",
                "bazi.depth.fortune.decade_year_month_order",
                "bazi.depth.fortune.month_trigger",
            ],
            evidence={
                "majorFortuneAvailable": bool(raw.get("majorFortune")),
                "annualFortuneCount": len(raw.get("annualFortune", []))
                if isinstance(raw.get("annualFortune"), list)
                else 0,
                "monthlyFortuneCount": len(raw.get("monthlyFortune", []))
                if isinstance(raw.get("monthlyFortune"), list)
                else 0,
            },
            confidence=0.69,
            risk_boundary="岁运只作趋势触发说明，不承诺事件结果。",
        ),
    ]
    return [item for item in statements if set(item["ruleIds"]) <= applied_ids]


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
    raw["inputTrace"] = {
        "birthDateTime": payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "birthPlace": payload.birth_place,
        "longitude": payload.longitude,
        "latitude": payload.latitude,
        "useTrueSolarTime": payload.use_true_solar_time,
        "trueSolarTime": runtime.calculator.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
        "engine": "fate_core.usecases.calculate_pure_analysis",
    }
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
    append_accuracy_evidence(runtime, raw)
    raw["baziBenchmark"] = _build_bazi_benchmark(raw)
    append_bazi_benchmark_evidence(raw)
    raw["baziRuleDepth"] = _build_bazi_rule_depth(raw)
    append_bazi_rule_depth_evidence(raw)
    ensure_evidence_risk_boundaries(raw)
    projected = project_by_profile(raw, "pure_analysis")
    translated = runtime.calculator._translate_to_chinese(projected)
    safe_result = runtime.calculator._json_safe(translated)
    if not isinstance(safe_result, dict):
        raise RuntimeError("纯分析结果必须是 JSON 对象")
    return dict(safe_result)
