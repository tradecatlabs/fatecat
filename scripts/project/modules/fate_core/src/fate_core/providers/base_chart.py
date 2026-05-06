from __future__ import annotations

from typing import Any

from fate_core.contracts.runtime import PureAnalysisRuntime


def _build_input(runtime: PureAnalysisRuntime) -> dict[str, Any]:
    payload = runtime.payload
    return {
        "name": payload.name or "命主",
        "gender": payload.gender,
        "birthDate": payload.birth_dt.strftime("%Y-%m-%d"),
        "birthTime": payload.birth_dt.strftime("%H:%M"),
        "birthPlace": payload.birth_place,
        "longitude": payload.longitude,
        "latitude": payload.latitude,
        "options": {
            "useTrueSolarTime": payload.use_true_solar_time,
            "calendarType": "solar",
        },
    }


def _build_meta(runtime: PureAnalysisRuntime) -> dict[str, str]:
    payload = runtime.payload
    return {
        "trueSolarTime": runtime.calculator.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
        "calculateTime": runtime.calc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "genderCn": "乾造(男)" if payload.gender == "male" else "坤造(女)",
    }


def build_base_chart_section(runtime: PureAnalysisRuntime) -> dict[str, Any]:
    """装配纯命理基础盘字段。"""
    calculator = runtime.calculator
    ec = runtime.ec
    four_pillars = runtime.four_pillars
    hidden_stems = runtime.hidden_stems

    spirits_full = calculator._calc_all_spirits(ec)
    wuxing_scores = calculator._calc_wuxing_scores(four_pillars)

    return {
        "input": _build_input(runtime),
        "meta": _build_meta(runtime),
        "fourPillars": four_pillars,
        "hiddenStems": hidden_stems,
        "tenGods": runtime.ten_gods,
        "twelveGrowth": runtime.twelve_growth,
        "fiveElements": runtime.five_elements,
        "wuxingState": calculator._calc_wuxing_state(runtime.five_elements, ec.getMonthZhi()),
        "specialPalaces": runtime.special_palaces,
        "voidInfo": runtime.void_info,
        "spirits": spirits_full,
        "spiritsFull": spirits_full,
        "spiritsExplain": calculator._calc_spirits_explain(spirits_full),
        "dayMaster": {
            **runtime.day_master_seed,
            "strength": wuxing_scores.get("weakStrong"),
            "selfSitting": calculator._calc_self_sitting(ec.getDayGan(), ec.getDayZhi()),
        },
        "ganzhiRelations": calculator._calc_ganzhi_relations(four_pillars),
        "ganzhiImagery": calculator._calc_ganzhi_imagery(four_pillars),
        "ganzhiExtra": calculator._calc_ganzhi_extra(four_pillars, hidden_stems),
        "branchRelations": calculator._calc_zhi_relations(four_pillars),
        "wuxingScores": wuxing_scores,
        "climateScores": calculator._calc_climate_scores(four_pillars),
    }
