"""原生 HTML Web 报告页。

该模块只负责 FastAPI 交付层的 HTML 呈现，不定义新的命理字段契约。
页面遵循零美化语义界面规范：服务端直出、原生表单、psql ASCII 表格、Markdown 原文可复制。
"""

from __future__ import annotations

import json
import logging
from html import escape
from typing import Any

from fastapi.responses import HTMLResponse

from branding import get_branding_payload
from prediction_systems import PREDICTION_SYSTEMS, report_system_allowed_text
from report_generator import public_birth_place
from utils.timezone import now_cn
from web_forms import WebReportForm, WebReportJobView, WebReportResult
from web_report_service import build_web_report_result

logger = logging.getLogger(__name__)


def render_web_report_page(
    *,
    birth_date: str | None = None,
    birth_time: str | None = None,
    birth_place: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    report_system: str | None = None,
    submitted: str | None = None,
    job: WebReportJobView | None = None,
) -> HTMLResponse:
    """渲染 Web 版标准 Markdown 报告页面。"""
    form = WebReportForm.from_query(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=birth_place,
        gender=gender,
        name=name,
        report_system=report_system,
        submitted=submitted,
    )

    errors: list[str] = []
    result: WebReportResult | None = job.result if job and job.result else None
    if job and job.status in {"failed", "expired"} and job.error:
        errors.append(job.error)
    if job is None and (form.submitted or form.has_input()):
        try:
            result = build_web_report_result(form)
        except ValueError as exc:
            errors.append(str(exc))
        except Exception:
            logger.exception("Web 报告生成失败")
            errors.append("生成报告失败")

    html = _render_document(form=form, result=result, errors=errors, job=job)
    return HTMLResponse(content=html)


def _render_document(
    *, form: WebReportForm, result: WebReportResult | None, errors: list[str], job: WebReportJobView | None
) -> str:
    generated_at = now_cn().isoformat()
    body_parts = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>faetcat</title>",
        "</head>",
        "<body>",
        "<h1>faetcat</h1>",
        _render_semantic_page(form=form, result=result, errors=errors, job=job, generated_at=generated_at),
    ]

    body_parts.extend(
        [
            _render_copy_script(),
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(body_parts)


def _render_semantic_page(
    *,
    form: WebReportForm,
    result: WebReportResult | None,
    errors: list[str],
    job: WebReportJobView | None,
    generated_at: str,
) -> str:
    return "\n".join(
        [
            _render_header_panel(
                generated_at=generated_at,
                has_result=result is not None,
                has_errors=bool(errors),
            ),
            _render_input_panel(form=form, result=result, errors=errors),
            _render_report_panel(result=result, errors=errors, job=job),
        ]
    )


def _render_report_panel(*, result: WebReportResult | None, errors: list[str], job: WebReportJobView | None) -> str:
    parts = ['<h2 id="production-report">生成报告</h2>']
    if job:
        parts.append(_render_job_status(job))
    if errors:
        parts.append('<p id="production-report-state">生成失败；请检查错误信息。</p>')
        parts.append(_render_errors(errors))
    if result:
        parts.append('<p id="production-report-state">报告已生成。</p>')
        parts.append(_render_report(result))
    if not errors and result is None:
        parts.append(
            '<p id="production-report-state">尚未生成报告。提交底部参数后，服务端会在这里写入 Markdown 输出。</p>'
        )
    return "\n".join(parts)


def _render_job_status(job: WebReportJobView) -> str:
    status_label = {
        "queued": "排队中",
        "running": "生成中",
        "succeeded": "已完成",
        "failed": "失败",
        "expired": "已过期",
    }.get(job.status, job.status)
    rows = [
        ["jobId", job.job_id],
        ["状态", status_label],
        ["输出体系", job.report_system],
        ["队列位置", job.queue_position if job.queue_position is not None else ""],
        ["创建时间", job.created_at],
        ["开始时间", job.started_at or ""],
        ["结束时间", job.finished_at or ""],
        ["过期时间", job.expires_at],
    ]
    if job.error:
        rows.append(["错误", job.error])
    return "\n".join(
        [
            (
                f'<p id="report-job-status" data-job-id="{_attr(job.job_id)}" '
                f'data-job-status="{_attr(job.status)}">任务状态：{_h(status_label)}</p>'
            ),
            _render_table(rows, ["字段", "值"], table_id="report-job-table"),
        ]
    )


def _render_header_panel(*, generated_at: str, has_result: bool, has_errors: bool) -> str:
    branding = get_branding_payload()
    links = [
        ("DEX Screener", branding["dexScreenerUrl"]),
        ("X", branding["xUrl"]),
        ("GitHub", branding["githubUrl"]),
        ("Hugging Face", branding["huggingFaceUrl"]),
        ("免费 AI 分析入口（Gemini Gem）", branding["geminiGemUrl"]),
        ("页面：项目与页面信息", "#project-brand"),
        ("页面：参数控件", "#input-form"),
        ("页面：生成报告", "#production-report"),
        ("服务：GET /health", "/health"),
        ("服务：FastAPI /docs", "/docs"),
        ("服务：GET /web 空表单", "/web"),
        ("服务：GET /api/v1/report/systems", "/api/v1/report/systems"),
    ]
    if has_errors:
        links.append(("页面：错误", "#errors"))
    if has_result:
        links.extend(
            [
                ("页面：Markdown 输出", "#markdown-output"),
                ("页面：工作台", "#workbench"),
            ]
        )
    rows = [
        ["CA", branding["ca"]],
        ["项目归属", branding["heroTitle"]],
        ["项目定位", branding["sponsorText"]],
        ["核心能力", branding["tagline"]],
        ["页面说明", "使用原生 HTML 表单生成标准命理排盘 Markdown 报告；公开入口优先走异步任务。"],
        ["入口", "GET /web"],
        ["异步任务", "POST /api/v1/report/jobs/web；GET /api/v1/report/jobs/{job_id}"],
        ["输出", "Markdown 文本"],
        ["报告模板", "report_generator.generate_full_report(report_system)"],
        ["存储策略", "免费公开入口默认不写数据库；任务只在进程内短暂保留，TTL 到期或 Space 重启后消失"],
        ["AI 分析", "FateCat 不会自动发送报告到 Gemini；用户复制 Markdown 后自行打开 Gemini Gem"],
        ["地区解析", "location.get"],
        ["服务入口", "GET /health"],
        ["服务入口", "FastAPI /docs"],
        ["服务入口", "GET /web 空表单"],
        ["服务入口", "GET /api/v1/report/systems"],
        ["生成时间", generated_at],
        ["时区", "Asia/Hong_Kong"],
        ["字段契约", "以下为 Web 报告输入参数"],
        ["birthDate", "出生日期｜必填：是｜格式：YYYY-MM-DD｜HTML date；例 1990-01-01"],
        ["birthTime", "出生时间｜必填：是｜格式：HH:MM 或 HH:MM:SS｜HTML time；例 08:00"],
        ["birthPlace", "出生地区｜必填：是｜格式：中文地点或 lng,lat｜例 北京 / 116.4074,39.9042"],
        ["gender", "性别｜必填：是｜格式：male/female｜计算必需；不能默认猜测"],
        [
            "reportSystem",
            f"输出体系｜必填：否｜格式：{report_system_allowed_text()}｜默认 bazi；每次只输出一个已实现体系",
        ],
        ["name", "姓名｜必填：否｜格式：文本｜为空时报告标题使用命主"],
    ]
    link_items = "\n".join(f'<li><a href="{_attr(url)}">{_h(label)}</a></li>' for label, url in links)
    return "\n".join(
        [
            '<h2 id="project-brand">项目与页面信息</h2>',
            _render_table(rows, ["字段", "内容"], table_id="project-metadata-table"),
            "<h3>全部链接</h3>",
            '<nav aria-label="项目、页面与服务链接">',
            f"<ul>\n{link_items}\n</ul>",
            "</nav>",
        ]
    )


def _render_input_panel(form: WebReportForm, result: WebReportResult | None, errors: list[str]) -> str:
    birth_place_value = form.birth_place if errors else public_birth_place(form.birth_place)
    parts = [
        '<h2 id="input-form">参数控件</h2>',
        '<form id="web-report-form" method="get" action="/web">',
        "<fieldset>",
        "<legend>排盘参数</legend>",
        '<input type="hidden" name="submitted" value="1">',
        "<p>",
        '<label for="birthDate">出生日期（必填）</label><br>',
        f'<input id="birthDate" name="birthDate" type="date" value="{_attr(form.birth_date)}">',
        "</p>",
        "<p>",
        '<label for="birthTime">出生时间（必填）</label><br>',
        f'<input id="birthTime" name="birthTime" type="time" value="{_attr(_time_value(form.birth_time))}">',
        "</p>",
        "<p>",
        '<label for="birthPlace">出生地区（必填）</label><br>',
        (
            '<input id="birthPlace" name="birthPlace" type="text" '
            f'value="{_attr(birth_place_value)}" '
            'placeholder="北京 或 116.4074,39.9042">'
        ),
        "</p>",
        "<p>",
        '<label for="gender">性别（必填）</label><br>',
        '<select id="gender" name="gender">',
        f'<option value=""{_selected(form.gender, "")}>请选择</option>',
        f'<option value="male"{_selected(form.gender, "male")}>男 male</option>',
        f'<option value="female"{_selected(form.gender, "female")}>女 female</option>',
        "</select>",
        "</p>",
        "<p>",
        '<label for="reportSystem">输出体系</label><br>',
        '<select id="reportSystem" name="reportSystem">',
        *_render_report_system_options(form.report_system),
        "</select>",
        "</p>",
        "<p>",
        '<label for="name">姓名（非必填）</label><br>',
        f'<input id="name" name="name" type="text" value="{_attr(form.name)}" placeholder="可为空">',
        "</p>",
        '<p><button type="submit">生成 Markdown 报告</button></p>',
        "</fieldset>",
        "</form>",
    ]
    if form.submitted or form.has_input():
        parts.append(_render_submitted_input(form, result))
    return "\n".join(parts)


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
    return "\n".join(
        [
            '<h2 id="submitted-input">当前输入</h2>',
            _render_table(rows, ["字段", "值", "来源"], table_id="submitted-input-table"),
        ]
    )


def _render_table(rows: list[list[object]], headers: list[str], *, table_id: str | None = None) -> str:
    """渲染浏览器原生语义表格，避免中英文字符宽度导致 ASCII 表格错位。"""
    table_attr = f' id="{_attr(table_id)}"' if table_id else ""
    head_cells = "\n".join(f'<th scope="col">{_h(header)}</th>' for header in headers)
    body_rows = []
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            text = "" if value is None else str(value)
            tag = 'th scope="row"' if index == 0 else "td"
            cells.append(f"<{tag}>{_h(text)}</{tag.split()[0]}>")
        body_rows.append("<tr>\n" + "\n".join(cells) + "\n</tr>")
    return "\n".join(
        [
            f"<table{table_attr}>",
            "<thead>",
            "<tr>",
            head_cells,
            "</tr>",
            "</thead>",
            "<tbody>",
            *body_rows,
            "</tbody>",
            "</table>",
        ]
    )


def _render_errors(errors: list[str]) -> str:
    items = "\n".join(f"<li>{_h(error)}</li>" for error in errors)
    return f'<h2 id="errors">错误</h2>\n<ul>\n{items}\n</ul>'


def _render_report(result: WebReportResult) -> str:
    raw_json = json.dumps(result.input_payload, ensure_ascii=False, indent=2)
    return "\n".join(
        [
            '<h2 id="markdown-output">Markdown 输出</h2>',
            f"<p>当前输出体系：{_h(result.report_system_label)}</p>",
            '<p><button type="button" id="copy-report">复制 Markdown</button></p>',
            '<p id="copy-status">尚未复制</p>',
            '<pre><code id="report-markdown">' + _h(result.markdown) + "</code></pre>",
            _render_workbench(result),
            "<details>",
            "<summary>机器可读输入</summary>",
            "<pre><code>" + _h(raw_json) + "</code></pre>",
            "</details>",
        ]
    )


def _render_workbench(result: WebReportResult) -> str:
    if result.report_system == "ziwei":
        return _render_ziwei_workbench(result.workbench)
    return _render_bazi_workbench(result.workbench)


def _render_bazi_workbench(workbench: dict[str, Any]) -> str:
    pillars = workbench.get("fourPillars", {}) if isinstance(workbench.get("fourPillars"), dict) else {}
    pillar_rows = []
    for key, label in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
        item = pillars.get(key, {}) if isinstance(pillars.get(key), dict) else {}
        pillar_rows.append([label, item.get("fullName", ""), item.get("stem", ""), item.get("branch", "")])
    benchmark = workbench.get("baziBenchmark", {}) if isinstance(workbench.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    renyuan = benchmark.get("renYuanSiling", {}) if isinstance(benchmark.get("renYuanSiling"), dict) else {}
    yongshen = workbench.get("yongShen", {}) if isinstance(workbench.get("yongShen"), dict) else {}
    geju = workbench.get("geju", {}) if isinstance(workbench.get("geju"), dict) else {}
    rule_depth = workbench.get("ruleDepth", {}) if isinstance(workbench.get("ruleDepth"), dict) else {}
    trigger_rows = []
    for item in benchmark.get("fortuneTriggers", [])[:12] if isinstance(benchmark.get("fortuneTriggers"), list) else []:
        if isinstance(item, dict):
            trigger_rows.append([item.get("year", ""), item.get("ganZhi", ""), "；".join(item.get("reasons", []))])
    if not trigger_rows:
        trigger_rows.append(["-", "-", "当前样本未命中已登记触发项"])
    profile_rows = []
    for item in benchmark.get("topicProfiles", []) if isinstance(benchmark.get("topicProfiles"), list) else []:
        if not isinstance(item, dict):
            continue
        profile_rows.append(
            [
                item.get("topic", ""),
                item.get("score", ""),
                item.get("lifecycle", ""),
                "、".join(str(part) for part in item.get("basis", []) if str(part).strip()),
                "、".join(str(field) for field in item.get("evidenceFields", []) if str(field).strip()),
                item.get("riskBoundary", ""),
            ]
        )
    if not profile_rows:
        profile_rows.append(["-", "-", "-", "-", "-", "当前样本未生成专题 profile"])
    rule_rows = _rule_depth_summary_rows(rule_depth)
    return "\n".join(
        [
            '<h2 id="workbench">八字工作台</h2>',
            "<p>该区域只展示后端结构化字段；复制 Markdown 内容不受工作台影响。</p>",
            "<details open><summary>四柱 / 十神 / 藏干</summary>",
            _render_table(pillar_rows, ["柱位", "干支", "天干", "地支"]),
            "</details>",
            "<details><summary>五行强弱与人元司令</summary>",
            "<pre><code>"
            + _h(
                json.dumps(
                    {
                        "strengthScore": strength,
                        "renYuanSiling": renyuan,
                        "wuxingScores": workbench.get("wuxingScores", {}),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            + "</code></pre>",
            "</details>",
            "<details><summary>格局与用神策略</summary>",
            "<pre><code>"
            + _h(
                json.dumps(
                    {
                        "geju": geju,
                        "yongShen": yongshen,
                        "yongShenStrategies": benchmark.get("yongShenStrategies", []),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            + "</code></pre>",
            "</details>",
            "<details><summary>大运流年触发</summary>",
            _render_table(trigger_rows, ["年份", "干支", "触发依据"]),
            "</details>",
            "<details><summary>专题 profile / 风险边界</summary>",
            _render_table(profile_rows, ["专题", "分数", "生命周期", "依据", "证据字段", "风险边界"]),
            "</details>",
            "<details><summary>规则深度 / 冲突策略</summary>",
            _render_table(rule_rows, ["规则", "主题", "状态", "置信度", "证据字段", "风险边界"]),
            "</details>",
        ]
    )


def _rule_depth_summary_rows(rule_depth: dict[str, Any]) -> list[list[object]]:
    """只展示可公开的规则摘要字段，不泄漏 evaluator 生命周期细节。"""
    rows: list[list[object]] = []
    applied = rule_depth.get("appliedRules", []) if isinstance(rule_depth.get("appliedRules"), list) else []
    for item in applied:
        if not isinstance(item, dict):
            continue
        rows.append(
            [
                item.get("ruleId", ""),
                item.get("topic", ""),
                item.get("status", ""),
                item.get("confidence", ""),
                "、".join(str(field) for field in item.get("evidenceFields", []) if str(field).strip()),
                item.get("riskBoundary", ""),
            ]
        )
    if not rows:
        rows.append(["-", "-", "-", "-", "-", "当前样本未生成规则深度摘要"])
    return rows


def _render_ziwei_workbench(workbench: dict[str, Any]) -> str:
    palaces = workbench.get("palaces", []) if isinstance(workbench.get("palaces"), list) else []
    palace_rows = []
    for palace in palaces:
        if not isinstance(palace, dict):
            continue
        palace_rows.append(
            [
                palace.get("name", ""),
                palace.get("earthlyBranch", ""),
                "、".join(_star_name_list(palace.get("majorStars"))),
                "命" if palace.get("isOriginalPalace") else "",
                "身" if palace.get("isBodyPalace") else "",
            ]
        )
    taxonomy = workbench.get("starTaxonomy", {}) if isinstance(workbench.get("starTaxonomy"), dict) else {}
    mutagen_flow = workbench.get("mutagenFlow", {}) if isinstance(workbench.get("mutagenFlow"), dict) else {}
    rule_depth = workbench.get("ruleDepth", {}) if isinstance(workbench.get("ruleDepth"), dict) else {}
    return "\n".join(
        [
            '<h2 id="workbench">紫微工作台</h2>',
            "<p>该区域只展示后端 iztro 结构化字段与解释索引；紫微仍为 standalone 输出。</p>",
            "<details open><summary>十二宫 / 星曜</summary>",
            _render_table(palace_rows, ["宫位", "地支", "主星", "命宫", "身宫"]),
            "</details>",
            "<details><summary>星曜分类 / 庙旺利陷</summary>",
            "<pre><code>" + _h(json.dumps(taxonomy, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
            "<details><summary>四化飞入 / 运限</summary>",
            "<pre><code>" + _h(json.dumps(mutagen_flow, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
            "<details><summary>规则深度 / 冲突策略</summary>",
            "<pre><code>" + _h(json.dumps(rule_depth, ensure_ascii=False, indent=2)) + "</code></pre>",
            "</details>",
        ]
    )


def _star_name_list(stars: object) -> list[str]:
    if not isinstance(stars, list):
        return []
    names = []
    for star in stars:
        if isinstance(star, dict) and star.get("name"):
            names.append(str(star.get("name")))
    return names


def _render_copy_script() -> str:
    return "\n".join(
        [
            "<script>",
            "(() => {",
            '  const form = document.getElementById("web-report-form");',
            '  const reportState = document.getElementById("production-report-state");',
            "  if (!form) { return; }",
            "  const setSubmitting = () => {",
            "    const buttons = document.querySelectorAll('#web-report-form button[type=\"submit\"]');",
            "    buttons.forEach((submitButton) => {",
            '      submitButton.setAttribute("aria-busy", "true");',
            '      submitButton.textContent = "生成中...";',
            "    });",
            '    if (reportState) { reportState.textContent = "正在生成 Markdown 报告..."; }',
            "  };",
            "  const setIdle = () => {",
            "    const buttons = document.querySelectorAll('#web-report-form button[type=\"submit\"]');",
            "    buttons.forEach((submitButton) => {",
            '      submitButton.removeAttribute("aria-busy");',
            '      submitButton.textContent = "生成 Markdown 报告";',
            "    });",
            "  };",
            "  const setStatus = (message) => { if (reportState) { reportState.textContent = message; } };",
            "  const pollJob = async (jobId) => {",
            "    try {",
            '      const response = await fetch(`/api/v1/report/jobs/${encodeURIComponent(jobId)}`, { headers: { accept: "application/json" } });',
            "      const body = await response.json();",
            '      if (!response.ok || !body.success) { throw new Error(body.error || "报告任务查询失败"); }',
            "      const data = body.data || {};",
            '      if (data.status === "succeeded") {',
            "        window.location.href = `/web?jobId=${encodeURIComponent(jobId)}`;",
            "        return;",
            "      }",
            '      if (data.status === "failed" || data.status === "expired") {',
            '        setStatus(data.error || "报告任务失败；请重新提交。");',
            "        setIdle();",
            "        return;",
            "      }",
            '      const position = data.queuePosition ? `，队列位置 ${data.queuePosition}` : "";',
            "      setStatus(`正在生成 Markdown 报告... 当前状态 ${data.status}${position}`);",
            "      window.setTimeout(() => pollJob(jobId), 1500);",
            "    } catch (error) {",
            '      setStatus(error instanceof Error ? error.message : "报告任务查询失败");',
            "      setIdle();",
            "    }",
            "  };",
            '  const currentJob = document.getElementById("report-job-status");',
            '  if (currentJob && ["queued", "running"].includes(currentJob.dataset.jobStatus || "")) {',
            '    pollJob(currentJob.dataset.jobId || "");',
            "  }",
            '  form.addEventListener("submit", async (event) => {',
            "    if (!window.fetch || !window.FormData) { setSubmitting(); return; }",
            "    event.preventDefault();",
            "    setSubmitting();",
            "    try {",
            "      const payload = Object.fromEntries(new FormData(form).entries());",
            '      const response = await fetch("/api/v1/report/jobs/web", {',
            '        method: "POST",',
            '        headers: { "content-type": "application/json", accept: "application/json" },',
            "        body: JSON.stringify(payload),",
            "      });",
            "      const body = await response.json();",
            '      if (!response.ok || !body.success) { throw new Error(body.error || "报告任务提交失败"); }',
            "      const jobId = body.data && body.data.jobId;",
            '      if (!jobId) { throw new Error("报告任务提交失败"); }',
            '      setStatus("报告任务已进入队列...");',
            "      pollJob(jobId);",
            "    } catch (error) {",
            '      setStatus(error instanceof Error ? error.message : "报告任务提交失败");',
            "      setIdle();",
            "    }",
            "  });",
            "})();",
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
    enabled_ids = {item.id for item in PREDICTION_SYSTEMS if item.enabled}
    normalized = current if current in enabled_ids else "bazi"
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
        suffix = (
            "" if system.enabled else "（结构化 capability 已可用）" if system.status == "production" else "（待实现）"
        )
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
