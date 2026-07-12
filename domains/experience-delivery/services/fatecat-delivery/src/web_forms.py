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
    location_mode: str = "domestic"
    location_id: str = ""
    time_basis: str = "beijing_time"
    fold_choice: str = ""
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
        location_mode: str | None = None,
        location_id: str | None = None,
        time_basis: str | None = None,
        fold_choice: str | None = None,
        gender: str | None = None,
        name: str | None = None,
        report_system: str | None = None,
        submitted: str | None = None,
    ) -> WebReportForm:
        return cls(
            birth_date=(birth_date or "").strip(),
            birth_time=(birth_time or "").strip(),
            birth_place=(birth_place or "").strip(),
            location_mode=(location_mode or "domestic").strip() or "domestic",
            location_id=(location_id or "").strip(),
            time_basis=(time_basis or "beijing_time").strip() or "beijing_time",
            fold_choice=(fold_choice or "").strip(),
            gender=(gender or "").strip(),
            name=(name or "").strip(),
            report_system=(report_system or "bazi").strip() or "bazi",
            submitted=(submitted or "").strip() == "1",
        )

    def has_input(self) -> bool:
        return any(
            [
                self.birth_date,
                self.birth_time,
                self.birth_place,
                self.location_id,
                self.gender,
                self.name,
            ]
        )


@dataclass
class WebReportResult:
    markdown: str
    policy_gate: dict[str, Any]
    snapshot_gate: dict[str, Any]
    resolved_longitude: float
    resolved_latitude: float
    resolved_location_id: str
    resolved_location_name: str
    resolved_timezone: str
    coordinate_precision: str
    time_basis: str
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
