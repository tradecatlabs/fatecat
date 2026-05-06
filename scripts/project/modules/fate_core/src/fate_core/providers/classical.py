from __future__ import annotations

from typing import Any

from fate_core.adapters import calc_bone_weight, calc_ming_gua
from fate_core.contracts.runtime import PureAnalysisRuntime


def build_classical_section(runtime: PureAnalysisRuntime) -> dict[str, Any]:
    """装配纯命理传统分析字段。"""
    calculator = runtime.calculator
    ec = runtime.ec
    four_pillars = runtime.four_pillars

    bone_weight = calc_bone_weight(
        ec.getYear(),
        abs(runtime.lunar.getMonth()),
        runtime.lunar.getDay(),
        ec.getTimeZhi(),
    )
    ming_gua = calc_ming_gua(calculator.calc_dt.year, runtime.payload.gender)
    jieqi_detail = calculator._calc_jieqi_detail()
    days_from_jieqi = jieqi_detail.get("prevJieQi", {}).get("daysAfter", 0)
    yong_shen = calculator._calc_yongshen(ec.getDayGan(), ec.getMonthZhi(), four_pillars)

    return {
        "boneWeight": bone_weight,
        "mingGua": ming_gua,
        "birthInfo": calculator._get_birth_info(),
        "jieqiDetail": jieqi_detail,
        "siling": calculator._calc_siling(ec.getMonthZhi(), days_from_jieqi),
        "geju": calculator._calc_geju(ec, four_pillars),
        "xiaoYun": calculator._calc_xiao_yun(runtime.yun, ec, yong_shen),
        "jiaoYun": calculator._calc_jiao_yun(runtime.yun),
        "trueSolarTime": calculator.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
        "yongShen": yong_shen,
        "siziSummary": calculator._calc_sizi_summary(four_pillars),
        "huangLi": calculator._calc_huangli(),
        "completeTrueSolarTime": calculator.true_solar_detail,
        "ziTimeAnalysis": calculator.zi_time_analysis,
    }
