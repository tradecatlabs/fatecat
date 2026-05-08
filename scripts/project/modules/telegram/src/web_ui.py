"""原生 HTML Web 报告页。

该模块只负责 FastAPI 交付层的 HTML 呈现，不定义新的命理字段契约。
页面遵循零美化语义界面规范：服务端直出、原生表单、psql ASCII 表格、Markdown 原文可复制。
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import Any

from bazi_calculator import BaziCalculator
from fastapi.responses import HTMLResponse
from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from location import get as get_location
from prediction_systems import PREDICTION_SYSTEMS, report_system_allowed_text
from report_generator import REPORT_SYSTEM_LABELS, build_report_hide, generate_full_report, public_birth_place
from tabulate import tabulate
from utils.timezone import now_cn

logger = logging.getLogger(__name__)


@dataclass
class WebReportForm:
    birth_date: str = ""
    birth_time: str = ""
    birth_place: str = ""
    gender: str = ""
    name: str = ""
    report_system: str = "bazi"

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
    ) -> WebReportForm:
        return cls(
            birth_date=(birth_date or "").strip(),
            birth_time=(birth_time or "").strip(),
            birth_place=(birth_place or "").strip(),
            gender=(gender or "").strip(),
            name=(name or "").strip(),
            report_system=(report_system or "bazi").strip() or "bazi",
        )

    def has_input(self) -> bool:
        return any([self.birth_date, self.birth_time, self.birth_place, self.gender, self.name])


@dataclass
class WebReportResult:
    markdown: str
    resolved_longitude: float
    resolved_latitude: float
    normalized_time: str
    input_payload: dict[str, Any]
    report_system: str
    report_system_label: str


def render_web_report_page(
    *,
    birth_date: str | None = None,
    birth_time: str | None = None,
    birth_place: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    report_system: str | None = None,
) -> HTMLResponse:
    """渲染 Web 版标准 Markdown 报告页面。"""
    form = WebReportForm.from_query(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=birth_place,
        gender=gender,
        name=name,
        report_system=report_system,
    )

    errors: list[str] = []
    result: WebReportResult | None = None
    if form.has_input():
        try:
            result = _build_report(form)
        except ValueError as exc:
            errors.append(str(exc))
        except Exception:
            logger.exception("Web 报告生成失败")
            errors.append("生成报告失败")

    html = _render_document(form=form, result=result, errors=errors)
    return HTMLResponse(content=html)


def _build_report(form: WebReportForm) -> WebReportResult:
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
    display_birth_place = public_birth_place(form.birth_place)

    report_hide = build_report_hide(report_system)
    if report_system == "ziwei":
        calc_result = (
            CapabilityExecutor()
            .execute(
                CapabilityInput(
                    capability_id="ziwei",
                    payload={
                        "birthDateTime": birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "gender": gender,
                        "longitude": longitude,
                        "latitude": latitude,
                        "birthPlace": form.birth_place,
                        "name": form.name,
                        "useTrueSolarTime": True,
                    },
                )
            )
            .data
        )
    else:
        calculator = BaziCalculator(
            birth_dt,
            gender,
            longitude,
            latitude=latitude,
            name=form.name or None,
            birth_place=display_birth_place,
            use_true_solar_time=True,
        )
        calc_result = calculator.calculate(hide=report_hide)
    markdown = generate_full_report(calc_result, hide=report_hide, report_system=report_system)
    payload = {
        "birthDate": form.birth_date,
        "birthTime": normalized_time,
        "birthPlace": display_birth_place,
        "gender": gender,
        "name": form.name,
        "reportSystem": report_system,
        "reportSystemLabel": REPORT_SYSTEM_LABELS[report_system],
        "longitude": longitude,
        "latitude": latitude,
        "useTrueSolarTime": True,
    }
    return WebReportResult(
        markdown=markdown,
        resolved_longitude=longitude,
        resolved_latitude=latitude,
        normalized_time=normalized_time,
        input_payload=payload,
        report_system=report_system,
        report_system_label=REPORT_SYSTEM_LABELS[report_system],
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


def _render_document(*, form: WebReportForm, result: WebReportResult | None, errors: list[str]) -> str:
    generated_at = now_cn().isoformat()
    body_parts = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>FateCat Web Markdown 报告</title>",
        "</head>",
        "<body>",
        "<h1>FateCat Web Markdown 报告</h1>",
        "<p>该页面使用原生 HTML 表单生成标准命理排盘 Markdown 报告。核心结果由服务端直接写入页面。</p>",
        _render_meta(generated_at),
        _render_navigation(),
        _render_field_contract(),
        _render_form(form),
    ]

    if form.has_input():
        body_parts.append(_render_submitted_input(form, result))
    if errors:
        body_parts.append(_render_errors(errors))
    if result:
        body_parts.append(_render_report(result))

    body_parts.extend(
        [
            _render_copy_script(),
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(body_parts)


def _render_meta(generated_at: str) -> str:
    rows = [
        ("入口", "GET /web"),
        ("输出", "Markdown 文本"),
        ("报告模板", "report_generator.generate_full_report(report_system)"),
        ("地区解析", "location.get"),
        ("时间", generated_at),
        ("时区", "Asia/Hong_Kong"),
    ]
    items = "\n".join(f"<dt>{_h(k)}</dt><dd>{_h(v)}</dd>" for k, v in rows)
    return f"<h2>页面元信息</h2>\n<dl>\n{items}\n</dl>"


def _render_navigation() -> str:
    return "\n".join(
        [
            "<h2>相关入口</h2>",
            "<nav>",
            "<ul>",
            '<li><a href="/health">GET /health</a></li>',
            '<li><a href="/docs">FastAPI /docs</a></li>',
            '<li><a href="/web">GET /web 空表单</a></li>',
            "</ul>",
            "</nav>",
        ]
    )


def _render_field_contract() -> str:
    rows = [
        ["birthDate", "出生日期", "是", "YYYY-MM-DD", "HTML date；例 1990-01-01"],
        ["birthTime", "出生时间", "是", "HH:MM 或 HH:MM:SS", "HTML time；例 08:00"],
        ["birthPlace", "出生地区", "是", "中文地点或 lng,lat", "例 北京 / 116.4074,39.9042"],
        ["gender", "性别", "是", "male/female", "计算必需；不能默认猜测"],
        ["reportSystem", "输出体系", "否", report_system_allowed_text(), "默认 bazi；每次只输出一个已实现体系"],
        ["name", "姓名", "否", "文本", "为空时报告标题使用命主"],
    ]
    table = tabulate(rows, headers=["参数", "字段", "必填", "格式", "说明"], tablefmt="psql", missingval="")
    return f"<h2>字段契约</h2>\n<pre><code>{_h(table)}</code></pre>"


def _render_form(form: WebReportForm) -> str:
    return "\n".join(
        [
            '<h2 id="input-form">输入表单</h2>',
            '<form method="get" action="/web">',
            "<fieldset>",
            "<legend>必填字段</legend>",
            "<p>",
            '<label for="birthDate">出生日期（必填）</label><br>',
            f'<input id="birthDate" name="birthDate" type="date" value="{_attr(form.birth_date)}" required>',
            "</p>",
            "<p>",
            '<label for="birthTime">出生时间（必填）</label><br>',
            f'<input id="birthTime" name="birthTime" type="time" value="{_attr(_time_value(form.birth_time))}" required>',
            "</p>",
            "<p>",
            '<label for="birthPlace">出生地区（必填）</label><br>',
            (
                '<input id="birthPlace" name="birthPlace" type="text" '
                f'value="{_attr(public_birth_place(form.birth_place))}" '
                'placeholder="北京 或 116.4074,39.9042" required>'
            ),
            "</p>",
            "<p>",
            '<label for="gender">性别（必填）</label><br>',
            '<select id="gender" name="gender" required>',
            f'<option value=""{_selected(form.gender, "")}>请选择</option>',
            f'<option value="male"{_selected(form.gender, "male")}>男 male</option>',
            f'<option value="female"{_selected(form.gender, "female")}>女 female</option>',
            "</select>",
            "</p>",
            "</fieldset>",
            "<fieldset>",
            "<legend>输出体系</legend>",
            "<p>",
            '<label for="reportSystem">输出体系</label><br>',
            '<select id="reportSystem" name="reportSystem">',
            *_render_report_system_options(form.report_system),
            "</select>",
            "</p>",
            "</fieldset>",
            "<fieldset>",
            "<legend>非必填字段</legend>",
            "<p>",
            '<label for="name">姓名（非必填）</label><br>',
            f'<input id="name" name="name" type="text" value="{_attr(form.name)}" placeholder="可为空">',
            "</p>",
            "</fieldset>",
            '<p><button type="submit">生成 Markdown 报告</button></p>',
            "</form>",
        ]
    )


def _render_submitted_input(form: WebReportForm, result: WebReportResult | None) -> str:
    rows = [
        ["birthDate", form.birth_date, "query"],
        ["birthTime", form.birth_time, "query"],
        ["birthPlace", public_birth_place(form.birth_place), "query"],
        ["gender", form.gender, "query"],
        ["reportSystem", form.report_system or "bazi", "query"],
        ["name", form.name, "query"],
    ]
    if result:
        rows.extend(
            [
                ["selectedReportSystem", result.report_system_label, "server"],
                ["normalizedBirthTime", result.normalized_time, "server"],
                ["longitude", result.resolved_longitude, "location.get"],
                ["latitude", result.resolved_latitude, "location.get"],
            ]
        )
    table = tabulate(rows, headers=["字段", "值", "来源"], tablefmt="psql", missingval="")
    return f"<h2>当前输入</h2>\n<pre><code>{_h(table)}</code></pre>"


def _render_errors(errors: list[str]) -> str:
    items = "\n".join(f"<li>{_h(error)}</li>" for error in errors)
    return f"<h2>错误</h2>\n<ul>\n{items}\n</ul>"


def _render_report(result: WebReportResult) -> str:
    raw_json = json.dumps(result.input_payload, ensure_ascii=False, indent=2)
    return "\n".join(
        [
            "<h2>Markdown 输出</h2>",
            f"<p>当前输出体系：{_h(result.report_system_label)}</p>",
            '<p><button type="button" id="copy-report">复制 Markdown</button></p>',
            '<p id="copy-status">尚未复制</p>',
            '<pre><code id="report-markdown">' + _h(result.markdown) + "</code></pre>",
            "<details>",
            "<summary>机器可读输入</summary>",
            "<pre><code>" + _h(raw_json) + "</code></pre>",
            "</details>",
        ]
    )


def _render_copy_script() -> str:
    return "\n".join(
        [
            "<script>",
            "(() => {",
            '  const button = document.getElementById("copy-report");',
            '  const source = document.getElementById("report-markdown");',
            '  const status = document.getElementById("copy-status");',
            "  if (!button || !source || !status) { return; }",
            '  button.addEventListener("click", async () => {',
            "    try {",
            '      await navigator.clipboard.writeText(source.textContent || "");',
            '      status.textContent = "已复制 Markdown";',
            "    } catch (error) {",
            '      status.textContent = "复制失败；请手动选择 Markdown 输出区域复制。";',
            "    }",
            "  });",
            "})();",
            "</script>",
            "<noscript><p>当前浏览器未执行 JavaScript；请手动选择 Markdown 输出区域复制。</p></noscript>",
        ]
    )


def _selected(current: str, expected: str) -> str:
    return " selected" if current == expected else ""


def _render_report_system_options(current: str) -> list[str]:
    normalized = current if current in REPORT_SYSTEM_LABELS else "bazi"
    lines: list[str] = []
    current_group = ""
    for system in PREDICTION_SYSTEMS:
        if system.group != current_group:
            if current_group:
                lines.append("</optgroup>")
            current_group = system.group
            lines.append(f'<optgroup label="{_attr(current_group)}">')
        selected = _selected(normalized, system.id) if system.enabled else ""
        disabled = "" if system.enabled else " disabled"
        suffix = "" if system.enabled else "（待实现）"
        lines.append(
            f'<option value="{_attr(system.id)}"{selected}{disabled}>{_h(system.label)} {system.id}{suffix}</option>'
        )
    if current_group:
        lines.append("</optgroup>")
    return lines


def _time_value(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 5:
        return stripped[:5]
    return stripped


def _h(value: object) -> str:
    return escape("" if value is None else str(value), quote=False)


def _attr(value: object) -> str:
    return escape("" if value is None else str(value), quote=True)
