"""真太阳时计算边界。

主计算器只调用这里的函数；paipan-master Node 脚本路径和 JSON 解析留在本模块内部。
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta
from typing import Any

from fate_core.support.paths import FATE_TRUE_SOLAR_TIME_JS
from fate_core.support.timezone import ensure_cn


def calc_true_solar_time(dt: datetime, longitude: float) -> datetime:
    """简化真太阳时公式，仅保留给历史公开函数使用。"""
    return dt + timedelta(minutes=(longitude - 120) * 4)


def calculate_true_solar_time(dt: datetime, longitude: float, latitude: float | None = None) -> datetime:
    """调用 paipan-master 原生脚本计算真太阳时，失败即抛错。"""
    script = FATE_TRUE_SOLAR_TIME_JS
    if not script.exists():
        raise RuntimeError("真太阳时脚本缺失: true_solar_time.js")
    latitude_value = latitude if latitude is not None else 0
    try:
        output = (
            subprocess.check_output(
                [
                    "node",
                    str(script),
                    "--dt",
                    dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "--lon",
                    str(longitude),
                    "--lat",
                    str(latitude_value),
                ],
                timeout=8,
            )
            .decode("utf-8")
            .strip()
        )
        if not output:
            raise RuntimeError("真太阳时计算返回为空")
        return datetime.strptime(output, "%Y-%m-%d %H:%M:%S")
    except Exception as exc:
        raise RuntimeError(f"真太阳时计算失败: {exc}") from exc


def calculate_true_solar_time_detail(
    dt: datetime, longitude: float, latitude: float
) -> tuple[datetime, dict[str, Any], dict[str, Any]]:
    """调用 paipan-master 原生脚本计算真太阳时，并返回分解信息。"""
    script = FATE_TRUE_SOLAR_TIME_JS
    if not script.exists():
        raise RuntimeError("真太阳时脚本缺失: true_solar_time.js")
    try:
        output = (
            subprocess.check_output(
                [
                    "node",
                    str(script),
                    "--dt",
                    dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "--lon",
                    str(longitude),
                    "--lat",
                    str(latitude),
                    "--json",
                ],
                timeout=8,
            )
            .decode("utf-8")
            .strip()
        )
        if not output:
            raise RuntimeError("真太阳时计算返回为空")
        payload = json.loads(output)
        true_time_text = payload.get("trueSolarTime")
        if not true_time_text:
            raise RuntimeError("真太阳时 JSON 缺失 trueSolarTime")
        true_dt = datetime.strptime(true_time_text, "%Y-%m-%d %H:%M:%S")
        offsets = payload.get("offsets", {}) if isinstance(payload.get("offsets", {}), dict) else {}
        detail = {
            "originalTime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "trueSolarTime": true_time_text,
            "longitudeOffsetMinutes": offsets.get("longitudeOffsetMinutes"),
            "astronomicalOffsetMinutes": offsets.get("astronomicalOffsetMinutes"),
            "totalOffsetMinutes": offsets.get("totalOffsetMinutes"),
            "note": "真太阳时分解（天文算法口径，含经度修正与均时差）",
        }
        zi_time_analysis = (
            payload.get("ziTimeAnalysis", {}) if isinstance(payload.get("ziTimeAnalysis", {}), dict) else {}
        )
        return ensure_cn(true_dt), detail, zi_time_analysis
    except Exception as exc:
        raise RuntimeError(f"真太阳时计算失败: {exc}") from exc


__all__ = ["calc_true_solar_time", "calculate_true_solar_time", "calculate_true_solar_time_detail"]
