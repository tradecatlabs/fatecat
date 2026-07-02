"""Web 报告页输入/输出模型。

这里只定义原生 HTML 表单与服务端报告结果的数据形状，不渲染 HTML。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class WebReportForm:
    birth_date: str = ""
    birth_time: str = ""
    birth_place: str = ""
    gender: str = ""
    name: str = ""
    report_system: str = "bazi"
    submitted: bool = False

    @classmethod
    def from_query(
        cls,
        *,
        birth_date: str | None = None,
        birth_time: str | None = None,
        birth_place: str | None = None,
        gender: str | None = None,
        name: str | None = None,
        report_system: str | None = None,
        submitted: str | None = None,
    ) -> WebReportForm:
        return cls(
            birth_date=(birth_date or "").strip(),
            birth_time=(birth_time or "").strip(),
            birth_place=(birth_place or "").strip(),
            gender=(gender or "").strip(),
            name=(name or "").strip(),
            report_system=(report_system or "bazi").strip() or "bazi",
            submitted=(submitted or "").strip() == "1",
        )

    def has_input(self) -> bool:
        return any([self.birth_date, self.birth_time, self.birth_place, self.gender, self.name])


@dataclass
class WebReportResult:
    markdown: str
    policy_gate: dict[str, Any]
    snapshot_gate: dict[str, Any]
    resolved_longitude: float
    resolved_latitude: float
    normalized_time: str
    input_payload: dict[str, Any]
    report_system: str
    report_system_label: str
    workbench: dict[str, Any]


@dataclass
class WebReportJobView:
    job_id: str
    status: str
    report_system: str
    created_at: str
    expires_at: str
    started_at: str | None = None
    finished_at: str | None = None
    queue_position: int | None = None
    error: str | None = None
    result: WebReportResult | None = None


__all__ = ["WebReportForm", "WebReportJobView", "WebReportResult"]
