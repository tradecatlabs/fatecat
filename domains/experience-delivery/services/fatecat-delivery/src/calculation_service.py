"""交付层统一计算入口。

本模块只收敛 Web/API/Bot 的重复编排：输入已由各入口校验，领域计算仍归 fate-core。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from report_generator import build_report_hide, normalize_report_system, public_birth_place


@dataclass(frozen=True)
class DeliveryCalculationResult:
    """交付层共享的计算结果载体。"""

    data: dict[str, Any]
    report_system: str
    report_hide: dict[str, Any]
    birth_dt: datetime
    display_birth_place: str


def calculate_delivery_result(
    *,
    birth_dt: datetime,
    gender: str,
    longitude: float,
    latitude: float,
    birth_place: str,
    name: str | None,
    report_system: str = "bazi",
    use_true_solar_time: bool = True,
) -> DeliveryCalculationResult:
    """按报告体系执行 canonical 计算，不在交付层定义命理规则。"""
    normalized_system = normalize_report_system(report_system)
    report_hide = build_report_hide(normalized_system)
    display_birth_place = public_birth_place(birth_place)

    capability_id = "ziwei" if normalized_system == "ziwei" else "bazi"
    data = (
        CapabilityExecutor()
        .execute(
            CapabilityInput(
                capability_id=capability_id,
                payload={
                    "birthDateTime": birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "gender": gender,
                    "longitude": longitude,
                    "latitude": latitude,
                    "birthPlace": display_birth_place,
                    "name": name,
                    "useTrueSolarTime": use_true_solar_time,
                },
            )
        )
        .data
    )
    return DeliveryCalculationResult(
        data=data,
        report_system=normalized_system,
        report_hide=report_hide,
        birth_dt=birth_dt,
        display_birth_place=display_birth_place,
    )
