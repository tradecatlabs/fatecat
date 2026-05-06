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


def normalize_gender(gender: str) -> str:
    """把人类输入统一成底层计算器使用的性别枚举。"""
    normalized = str(gender).strip().lower()
    if normalized in {"male", "m", "man", "boy", "男", "男性", "乾", "乾造"}:
        return "male"
    if normalized in {"female", "f", "woman", "girl", "女", "女性", "坤", "坤造"}:
        return "female"
    raise ValueError(f"无法识别性别: {gender}")


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
    projected = project_by_profile(raw, "pure_analysis")
    translated = runtime.calculator._translate_to_chinese(projected)
    safe_result = runtime.calculator._json_safe(translated)
    if not isinstance(safe_result, dict):
        raise RuntimeError("纯分析结果必须是 JSON 对象")
    return dict(safe_result)
