from __future__ import annotations

from typing import Any

from fate_core.adapters import ELEM_CN, STEM_ELEM, BaziCalculator, LegacyBaziInput, LunarUtil, now_cn
from fate_core.contracts.runtime import PureAnalysisRuntime


def _alias_five_elements(five_elements: dict[str, Any]) -> dict[str, Any]:
    """补齐五行中英双键，兼容现有展示层。"""
    mapping = {
        "木": "wood",
        "火": "fire",
        "土": "earth",
        "金": "metal",
        "水": "water",
    }
    result = dict(five_elements)
    for cn_name, en_name in mapping.items():
        if cn_name in five_elements and en_name not in five_elements:
            result[en_name] = five_elements[cn_name]
        if en_name in five_elements and cn_name not in five_elements:
            result[cn_name] = five_elements[en_name]
    return result


def build_pure_analysis_runtime(payload: LegacyBaziInput) -> PureAnalysisRuntime:
    """构建纯命理分析共享运行时。"""
    calculator = BaziCalculator(
        payload.birth_dt,
        payload.gender,
        payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=payload.birth_place,
        use_true_solar_time=payload.use_true_solar_time,
    )
    if not calculator.ec:
        raise RuntimeError("lunar-python 初始化失败")

    ec = calculator.ec
    four_pillars = {
        pillar: calculator._pillar(
            getattr(ec, f"get{pillar.title()}")(),
            getattr(ec, f"get{pillar.title()}Gan")(),
            getattr(ec, f"get{pillar.title()}Zhi")(),
        )
        for pillar in ["year", "month", "day"]
    }
    four_pillars["hour"] = calculator._pillar(ec.getTime(), ec.getTimeGan(), ec.getTimeZhi())

    hidden_stems = {pillar: getattr(ec, f"get{pillar.title()}HideGan")() for pillar in ["year", "month", "day"]}
    hidden_stems["hour"] = ec.getTimeHideGan()

    ten_gods = {
        pillar: {
            "stem": getattr(ec, f"get{pillar.title()}ShiShenGan")(),
            "branch": getattr(ec, f"get{pillar.title()}ShiShenZhi")(),
        }
        for pillar in ["year", "month", "day"]
    }
    ten_gods["hour"] = {
        "stem": ec.getTimeShiShenGan(),
        "branch": ec.getTimeShiShenZhi(),
    }

    twelve_growth = {pillar: getattr(ec, f"get{pillar.title()}DiShi")() for pillar in ["year", "month", "day"]}
    twelve_growth["hour"] = ec.getTimeDiShi()

    five_elements = _alias_five_elements(calculator._calc_elements(four_pillars, hidden_stems))

    special_palaces = {
        "taiYuan": {"pillar": ec.getTaiYuan(), "nayin": ec.getTaiYuanNaYin()},
        "taiXi": {"pillar": ec.getTaiXi(), "nayin": ec.getTaiXiNaYin()},
        "mingGong": {"pillar": ec.getMingGong(), "nayin": ec.getMingGongNaYin()},
        "shenGong": {"pillar": ec.getShenGong(), "nayin": ec.getShenGongNaYin()},
    }

    void_info = {
        "year": {"xun": ec.getYearXun(), "kong": ec.getYearXunKong()},
        "month": {"xun": ec.getMonthXun(), "kong": ec.getMonthXunKong()},
        "day": {"xun": ec.getDayXun(), "kong": ec.getDayXunKong()},
        "hour": {"xun": ec.getTimeXun(), "kong": ec.getTimeXunKong()},
    }

    day_stem = ec.getDayGan()
    day_element = STEM_ELEM[day_stem]
    day_master_seed = {
        "stem": day_stem,
        "element": day_element,
        "elementCn": ELEM_CN[day_element],
        "yinYang": "阳" if LunarUtil.GAN.index(day_stem) % 2 == 0 else "阴",
    }

    return PureAnalysisRuntime(
        payload=payload,
        calculator=calculator,
        calc_now=now_cn(),
        ec=ec,
        lunar=calculator.lunar,
        yun=ec.getYun(1 if payload.gender == "male" else 0),
        four_pillars=four_pillars,
        hidden_stems=hidden_stems,
        ten_gods=ten_gods,
        twelve_growth=twelve_growth,
        five_elements=five_elements,
        special_palaces=special_palaces,
        void_info=void_info,
        day_master_seed=day_master_seed,
    )
