from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.support.paths import TELEGRAM_SRC_DIR

if str(TELEGRAM_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC_DIR))

from bazi_calculator import ELEM_CN, STEM_ELEM, BaziCalculator, LunarUtil, calc_bone_weight, calc_ming_gua
from utils.timezone import now_cn

__all__ = [
    "BaziCalculator",
    "ELEM_CN",
    "LegacyBaziInput",
    "LunarUtil",
    "PURE_ANALYSIS_HIDE",
    "STEM_ELEM",
    "calc_bone_weight",
    "calc_ming_gua",
    "calculate_legacy_bazi",
    "calculate_pure_analysis_raw",
    "now_cn",
]

PURE_ANALYSIS_HIDE: dict[str, bool] = {
    "extensions": True,
    "divination": True,
    "number_divination": True,
    "yijing": True,
    "name_marriage": True,
    "system": True,
    "zeri": True,
    "fengshui": True,
    "astro": True,
    "calendar": True,
    "health": True,
}


@dataclass(frozen=True)
class LegacyBaziInput:
    """遗留八字计算器输入。"""

    birth_dt: datetime
    gender: str
    longitude: float
    latitude: float
    name: str | None = None
    birth_place: str = ""
    use_true_solar_time: bool = True


def calculate_legacy_bazi(payload: LegacyBaziInput, *, hide: dict[str, bool] | None = None) -> dict[str, Any]:
    """兼容调用遗留 `BaziCalculator`。"""
    calculator = BaziCalculator(
        payload.birth_dt,
        payload.gender,
        payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=payload.birth_place,
        use_true_solar_time=payload.use_true_solar_time,
    )
    result = calculator.calculate(hide=hide or {})
    if not isinstance(result, dict):
        raise RuntimeError("遗留八字计算器必须返回 JSON 对象")
    return dict(result)


def calculate_pure_analysis_raw(payload: LegacyBaziInput) -> dict[str, Any]:
    """生成纯命理分析所需的原始结果。"""
    return calculate_legacy_bazi(payload, hide=PURE_ANALYSIS_HIDE)
