"""预测体系注册表。

该模块只登记交付层可选择的体系，不负责实现具体算法。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionSystem:
    id: str
    label: str
    status: str
    group: str
    description: str

    @property
    def enabled(self) -> bool:
        return self.status == "enabled"


PREDICTION_SYSTEMS: tuple[PredictionSystem, ...] = (
    PredictionSystem("bazi", "综合八字", "enabled", "当前可用", "默认报告体系，八字主线与袁天罡称骨。"),
    PredictionSystem("ziwei", "紫微斗数", "enabled", "当前可用", "紫微斗数独立报告，不混入综合八字。"),
    PredictionSystem("huangli", "黄历/择日", "planned", "未来功能", "黄历、建除十二神、择日推荐的独立体系。"),
    PredictionSystem("liuyao", "六爻占卜", "planned", "未来功能", "事件型起卦体系，需独立问题与起卦时间。"),
    PredictionSystem("meihua", "梅花易数", "planned", "未来功能", "时间、数字或象意起卦体系。"),
    PredictionSystem("qimen", "奇门遁甲", "planned", "未来功能", "奇门排盘独立体系。"),
    PredictionSystem("liuren", "大六壬", "planned", "未来功能", "大六壬排盘独立体系。"),
    PredictionSystem("fengshui", "风水九星", "planned", "未来功能", "方位、山向、门向等风水体系。"),
    PredictionSystem("name_marriage", "姓名合婚", "planned", "未来功能", "姓名学与合婚独立体系。"),
    PredictionSystem("yijing", "易经系统", "planned", "未来功能", "易经卦辞与起卦体系。"),
)

REPORT_SYSTEM_LABELS: dict[str, str] = {system.id: system.label for system in PREDICTION_SYSTEMS if system.enabled}


def enabled_report_system_ids() -> tuple[str, ...]:
    return tuple(system.id for system in PREDICTION_SYSTEMS if system.enabled)


def report_system_allowed_text() -> str:
    return "、".join(enabled_report_system_ids())


def get_prediction_system(system_id: str) -> PredictionSystem | None:
    normalized = system_id.strip().lower().replace("-", "_")
    for system in PREDICTION_SYSTEMS:
        if system.id == normalized:
            return system
    return None


def prediction_systems_payload() -> list[dict[str, str | bool]]:
    return [
        {
            "id": system.id,
            "label": system.label,
            "status": system.status,
            "enabled": system.enabled,
            "group": system.group,
            "description": system.description,
        }
        for system in PREDICTION_SYSTEMS
    ]
