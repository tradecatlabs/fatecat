"""Web Markdown 报告构建服务。

该模块连接 Web 表单、地区解析、capability 执行和 Markdown 生成。
HTML 呈现留在 `web_ui.py`，异步任务生命周期留在 `report_jobs.py`。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from calculation_service import calculate_delivery_result
from location import get as get_location
from prediction_systems import report_system_allowed_text
from report_generator import REPORT_SYSTEM_LABELS, generate_full_report, public_birth_place
from web_forms import WebReportForm, WebReportResult


@dataclass(frozen=True)
class ValidatedWebReportInput:
    birth_dt: datetime
    normalized_time: str
    gender: str
    report_system: str
    longitude: float
    latitude: float
    display_birth_place: str


def validate_web_report_form(form: WebReportForm) -> ValidatedWebReportInput:
    """校验 Web 表单并完成计算前的轻量解析。"""
    missing = []
    if not form.birth_date:
        missing.append("出生日期")
    if not form.birth_time:
        missing.append("出生时间")
    if not form.birth_place:
        missing.append("出生地区")
    if not form.gender:
        missing.append("性别")
    if missing:
        raise ValueError(f"缺少必填字段: {'、'.join(missing)}")

    birth_dt, normalized_time = _parse_birth_datetime(form.birth_date, form.birth_time)
    gender = _normalize_gender(form.gender)
    report_system = _normalize_report_system(form.report_system)
    try:
        longitude, latitude = get_location(form.birth_place)
    except ValueError as exc:
        if str(exc).startswith("地点无法识别"):
            raise ValueError("地点无法识别") from exc
        raise
    return ValidatedWebReportInput(
        birth_dt=birth_dt,
        normalized_time=normalized_time,
        gender=gender,
        report_system=report_system,
        longitude=longitude,
        latitude=latitude,
        display_birth_place=public_birth_place(form.birth_place),
    )


def build_web_report_result(form: WebReportForm) -> WebReportResult:
    """生成 Web 工作台使用的 Markdown 报告与结构化工作台数据。"""
    validated = validate_web_report_form(form)
    calculation = calculate_delivery_result(
        birth_dt=validated.birth_dt,
        gender=validated.gender,
        longitude=validated.longitude,
        latitude=validated.latitude,
        birth_place=validated.display_birth_place,
        name=form.name,
        report_system=validated.report_system,
        use_true_solar_time=True,
        bazi_engine="capability",
    )
    markdown = generate_full_report(
        calculation.data,
        hide=calculation.report_hide,
        report_system=calculation.report_system,
    )
    payload = {
        "birthDate": form.birth_date,
        "birthTime": validated.normalized_time,
        "birthPlace": calculation.display_birth_place,
        "gender": validated.gender,
        "name": form.name,
        "reportSystem": calculation.report_system,
        "reportSystemLabel": REPORT_SYSTEM_LABELS[calculation.report_system],
        "longitude": validated.longitude,
        "latitude": validated.latitude,
        "useTrueSolarTime": True,
    }
    return WebReportResult(
        markdown=markdown,
        resolved_longitude=validated.longitude,
        resolved_latitude=validated.latitude,
        normalized_time=validated.normalized_time,
        input_payload=payload,
        report_system=calculation.report_system,
        report_system_label=REPORT_SYSTEM_LABELS[calculation.report_system],
        workbench=_build_workbench_payload(calculation.data, calculation.report_system),
    )


def _parse_birth_datetime(birth_date: str, birth_time: str) -> tuple[datetime, str]:
    normalized_time = birth_time.strip()
    if len(normalized_time) == 5:
        normalized_time = f"{normalized_time}:00"
    try:
        birth_dt = datetime.strptime(f"{birth_date.strip()} {normalized_time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise ValueError("出生日期或出生时间格式无效；日期使用 YYYY-MM-DD，时间使用 HH:MM 或 HH:MM:SS。") from exc
    return birth_dt, normalized_time


def _normalize_gender(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"male", "m", "男"}:
        return "male"
    if normalized in {"female", "f", "女"}:
        return "female"
    raise ValueError("性别必须为 male/female，或中文 男/女。")


def _normalize_report_system(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in REPORT_SYSTEM_LABELS:
        return normalized
    raise ValueError(f"报告体系必须为: {report_system_allowed_text()}。未来体系需等独立功能实现后启用。")


def _build_workbench_payload(calc_result: dict[str, Any], report_system: str) -> dict[str, Any]:
    """构建 Web 工作台数据；只消费后端结构化结果，不定义命理规则。"""
    if report_system == "ziwei":
        return {
            "system": "ziwei",
            "palaces": calc_result.get("palaceAnalysis", []),
            "starTaxonomy": calc_result.get("ziweiStarTaxonomy", {}),
            "mutagenFlow": calc_result.get("ziweiMutagenFlow", {}),
            "palaceTopics": calc_result.get("ziweiPalaceTopics", []),
            "goldenGuards": calc_result.get("ziweiGoldenGuards", {}),
            "ruleDepth": calc_result.get("ziweiRuleDepth", {}),
        }
    return {
        "system": "bazi",
        "fourPillars": calc_result.get("fourPillars", {}),
        "tenGods": calc_result.get("tenGods", {}),
        "hiddenStems": calc_result.get("hiddenStems", {}),
        "wuxingScores": calc_result.get("wuxingScores", {}),
        "geju": calc_result.get("geju", {}),
        "yongShen": calc_result.get("yongShen", {}),
        "majorFortune": calc_result.get("majorFortune", {}),
        "annualFortune": calc_result.get("annualFortune", []),
        "baziBenchmark": calc_result.get("baziBenchmark", {}),
        "ruleDepth": calc_result.get("baziRuleDepth", {}),
    }


__all__ = ["ValidatedWebReportInput", "build_web_report_result", "validate_web_report_form"]
