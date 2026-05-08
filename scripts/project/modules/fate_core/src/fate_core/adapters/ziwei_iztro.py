from __future__ import annotations

import contextlib
import io
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.support.paths import TELEGRAM_SRC_DIR

from .legacy_bazi import BaziCalculator, now_cn

if str(TELEGRAM_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC_DIR))

from fortel_ziwei_integration import FortelZiweiCalculator  # noqa: E402


@dataclass(frozen=True)
class ZiweiIztroInput:
    """紫微 iztro 适配器输入。"""

    birth_dt: datetime
    gender: str
    longitude: float
    latitude: float
    name: str | None = None
    birth_place: str = ""
    use_true_solar_time: bool = True
    as_of: datetime | None = None


def _star_names(stars: object) -> list[str]:
    if not isinstance(stars, list):
        return []
    names: list[str] = []
    for star in stars:
        if isinstance(star, dict):
            name = str(star.get("name", "")).strip()
        else:
            name = str(star).strip()
        if name:
            names.append(name)
    return names


def _normalize_star_positions(palaces: object) -> list[dict[str, Any]]:
    """输出固定十二宫星曜索引，不因空宫或无主辅星而丢宫。"""
    if not isinstance(palaces, list):
        return []
    positions: list[dict[str, Any]] = []
    for palace in palaces:
        if not isinstance(palace, dict):
            continue
        positions.append(
            {
                "index": palace.get("index"),
                "palace": palace.get("name", ""),
                "heavenlyStem": palace.get("heavenlyStem", ""),
                "earthlyBranch": palace.get("earthlyBranch", ""),
                "isBodyPalace": bool(palace.get("isBodyPalace")),
                "isOriginalPalace": bool(palace.get("isOriginalPalace")),
                "majorStars": _star_names(palace.get("majorStars")),
                "minorStars": _star_names(palace.get("minorStars")),
                "adjectiveStars": _star_names(palace.get("adjectiveStars")),
            }
        )
    return positions


def calculate_ziwei_iztro(payload: ZiweiIztroInput) -> dict[str, Any]:
    """直接调用 iztro 紫微能力，只借用遗留八字计算器的真太阳时入口。

    这里不调用 `BaziCalculator.calculate()`，避免独立紫微 capability 被 sxwnl、
    民俗扩展或旧版 `ziwei.py` 基础算法牵连。
    """
    time_anchor = BaziCalculator(
        payload.birth_dt,
        payload.gender,
        payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=payload.birth_place,
        use_true_solar_time=payload.use_true_solar_time,
    )
    as_of = payload.as_of or now_cn().replace(tzinfo=None)
    with contextlib.redirect_stdout(io.StringIO()):
        ziwei_result = FortelZiweiCalculator(
            time_anchor.calc_dt,
            payload.gender,
            payload.longitude,
        ).calculate_professional_ziwei(as_of=as_of)

    chart = ziwei_result.get("professionalZiwei", {})
    palaces = chart.get("palaces", []) if isinstance(chart, dict) else []
    return {
        "inputTrace": {
            "originalTime": time_anchor.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "trueSolarTime": time_anchor.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
            "useTrueSolarTime": payload.use_true_solar_time,
            "longitude": payload.longitude,
            "latitude": payload.latitude,
            "timeZhi": time_anchor.zi_time_analysis.get("timeZhi", ""),
            "ziTimeAnalysis": time_anchor.zi_time_analysis,
            "trueSolarDetail": time_anchor.true_solar_detail,
            "iztroSolarDate": chart.get("solarDate") if isinstance(chart, dict) else "",
            "asOf": as_of.strftime("%Y-%m-%d %H:%M:%S"),
            "fixLeap": True,
        },
        "birthInfo": time_anchor._get_birth_info(),
        "ziweiChart": chart,
        "palaceAnalysis": palaces,
        "fiveElementsClass": chart.get("fiveElementsClass", "") if isinstance(chart, dict) else "",
        "starInfluence": chart.get("fiveElementsClass", "") if isinstance(chart, dict) else "",
        "starPositions": _normalize_star_positions(palaces),
        "ziweiHoroscope": ziwei_result.get("horoscope", {}),
    }
