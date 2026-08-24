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
from tabulate import tabulate

from branding import get_branding_payload
from prediction_systems import PREDICTION_SYSTEMS
from public_discovery import DISCOVERY_UPDATED_ON, public_base_url, schema_org_json
from utils.timezone import now_cn
from web_forms import WebReportForm, WebReportJobView, WebReportResult
from web_report_service import build_web_report_result

logger = logging.getLogger(__name__)


def render_web_report_page(
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
    job: WebReportJobView | None = None,
) -> HTMLResponse:
    """渲染 Web 版标准 Markdown 报告页面。"""
    form = WebReportForm.from_query(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=birth_place,
        location_mode=location_mode,
        location_id=location_id,
        time_basis=time_basis,
        fold_choice=fold_choice,
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

    html = _render_document(
        form=form,
        result=result,
        errors=errors,
        job=job,
    )
    return HTMLResponse(content=html)


def _render_document(
    *,
    form: WebReportForm,
    result: WebReportResult | None,
    errors: list[str],
    job: WebReportJobView | None,
) -> str:
    generated_at = now_cn().isoformat()
    canonical_url = f"{public_base_url()}/web"
    body_parts = [
        "<!doctype html>",
        '<html lang="zh-CN" data-workbench-profile="tradecatlabs.native-workbench.v0.1.compatibility">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="description" content="FateCat 是 TradeCat Labs 面向 Agent 与应用开发者的测算基础设施，提供综合八字、紫微斗数、统一能力协议、证据化解释和多端交付接口。">',
        '<meta name="author" content="TradeCat Labs">',
        f'<meta name="date" content="{DISCOVERY_UPDATED_ON}">',
        '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">',
        f'<link rel="canonical" href="{_attr(canonical_url)}">',
        '<link rel="alternate" type="text/plain" href="/llms.txt" title="FateCat llms.txt">',
        '<link rel="sitemap" type="application/xml" href="/sitemap.xml" title="FateCat sitemap">',
        '<link rel="alternate" type="application/json" href="/api/v1/capabilities" title="FateCat capabilities">',
        '<script type="application/ld+json">' + schema_org_json() + "</script>",
        _render_workbench_style(),
        "<title>FateCat</title>",
        "</head>",
        "<body>",
        _render_semantic_page(
            form=form,
            result=result,
            errors=errors,
            job=job,
            generated_at=generated_at,
        ),
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
            '<div id="workspace" data-sidebar="expanded" aria-label="FateCat 工作台">',
            '<div id="top-layer" data-layer="top" data-workbench-layer="top" aria-label="工作台交互层">',
            '<button id="sidebar-toggle" type="button" data-glyph="⬅️" aria-controls="control-plane" aria-expanded="true" aria-label="收起控制面" title="收起控制面"><canvas data-glyph-canvas aria-hidden="true"></canvas></button>',
            "</div>",
            '<aside id="control-plane" data-layer="middle" data-workbench-layer="middle" aria-label="项目说明与参数控制面">',
            "<h1>FateCat</h1>",
            _render_header_panel(
                generated_at=generated_at,
                has_result=result is not None,
                has_errors=bool(errors),
            ),
            '<fieldset id="control-content" aria-labelledby="input-form">',
            "<legend>参数控制面</legend>",
            _render_input_panel(
                form=form,
                result=result,
                errors=errors,
            ),
            "</fieldset>",
            "</aside>",
            '<main id="data-plane" data-layer="bottom" data-workbench-layer="bottom" aria-labelledby="production-report">',
            _render_report_panel(result=result, errors=errors, job=job),
            "</main>",
            "</div>",
        ]
    )


def _render_report_panel(*, result: WebReportResult | None, errors: list[str], job: WebReportJobView | None) -> str:
    parts = ['<h1 id="production-report">生成报告</h1>']
    if job:
        parts.append(_render_job_status(job))
    if errors:
        parts.append(
            '<p id="production-report-state" data-layer="bottom" data-workbench-layer="bottom">生成失败；请检查错误信息。</p>'
        )
        parts.append(_render_errors(errors))
    if result:
        parts.append(
            '<p id="production-report-state" data-layer="bottom" data-workbench-layer="bottom">报告已生成。</p>'
        )
        parts.append(_render_report(result))
    if not errors and result is None:
        parts.append(
            '<p id="production-report-state" data-layer="bottom" data-workbench-layer="bottom">尚未生成报告。提交底部参数后，服务端会在这里写入 Markdown 输出。</p>'
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
    table = tabulate(rows, headers=["字段", "值"], tablefmt="psql", missingval="")
    return "\n".join(
        [
            (
                f'<p id="report-job-status" data-job-id="{_attr(job.job_id)}" '
                f'data-job-status="{_attr(job.status)}">任务状态：{_h(status_label)}</p>'
            ),
            "<pre><code>" + _h(table) + "</code></pre>",
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
        ("项目说明与常见问题", "/about"),
        ("综合八字能力说明", "/guides/bazi"),
        ("紫微斗数能力说明", "/guides/ziwei"),
        ("AI / Agent 文档（llms.txt）", "/llms.txt"),
        ("页面：项目与页面信息", "#project-brand"),
        ("页面：参数控件", "#input-form"),
        ("页面：生成报告", "#production-report"),
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
        ["项目归属", "交易猫实验室｜FateCat 测算基础设施"],
        ["项目定位", branding["sponsorText"]],
        ["核心能力", branding["tagline"]],
        ["页面说明", "使用原生 HTML 表单生成标准命理排盘 Markdown 报告；公开入口优先走异步任务。"],
        ["可用体系", "综合八字 bazi；紫微斗数 ziwei"],
        ["输出", "Markdown 文本"],
        ["存储策略", "免费公开入口默认不写数据库；任务只在进程内短暂保留，TTL 到期或 Space 重启后消失"],
        ["AI 分析", "FateCat 不会自动发送报告到 Gemini；用户复制 Markdown 后自行打开 Gemini Gem"],
        ["AI / Agent 文档", "GET /llms.txt"],
        ["生成时间", generated_at],
        ["时区", "Asia/Hong_Kong"],
    ]
    table = tabulate(rows, headers=["字段", "内容"], tablefmt="psql", missingval="")
    link_items = "\n".join(f'<li><a href="{_attr(url)}">{_h(label)}</a></li>' for label, url in links)
    return "\n".join(
        [
            '<h2 id="project-brand">项目与页面信息</h2>',
            "<pre><code>" + _h(table) + "</code></pre>",
            "<h3>全部链接</h3>",
            '<nav aria-label="项目、页面与服务链接">',
            f'<ul data-layer="top" data-workbench-layer="top">\n{link_items}\n</ul>',
            "</nav>",
        ]
    )


def _render_input_panel(
    form: WebReportForm,
    result: WebReportResult | None,
    errors: list[str],
) -> str:
    parts = [
        '<h2 id="input-form">参数控件</h2>',
        '<form id="web-report-form" method="get" action="/web">',
        "<fieldset>",
        "<legend>排盘参数</legend>",
        "<p>",
        '<label for="birthDate">出生日期（必填）</label><br>',
        f'<input id="birthDate" name="birthDate" type="date" value="{_attr(form.birth_date)}" data-layer="middle" data-workbench-layer="middle">',
        "</p>",
        "<p>",
        '<label for="birthTime">出生时间（必填）</label><br>',
        f'<input id="birthTime" name="birthTime" type="time" value="{_attr(_time_value(form.birth_time))}">',
        "</p>",
        _render_birth_place_search(form),
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
        '<p><button id="generate-report" type="submit" name="submitted" value="1">生成 Markdown 报告</button></p>',
        "</fieldset>",
        "</form>",
    ]
    if form.submitted or form.has_input():
        parts.append(_render_submitted_input(form, result))
    return "\n".join(parts)


def _render_birth_place_search(form: WebReportForm) -> str:
    return "\n".join(
        [
            "<p>",
            '<label for="birthPlace">出生地区（必填）</label><br>',
            (
                '<input id="birthPlace" name="birthPlace" type="text" list="birth-place-options" '
                'autocomplete="off" maxlength="160" '
                f'value="{_attr(form.birth_place)}" placeholder="输入省、市或区/县名称">'
            ),
            f'<input id="locationId" name="locationId" type="hidden" value="{_attr(form.location_id)}">',
            '<datalist id="birth-place-options"></datalist>',
            "</p>",
        ]
    )


def _render_submitted_input(form: WebReportForm, result: WebReportResult | None) -> str:
    rows = [
        ["birthDate", form.birth_date, "query"],
        ["birthTime", form.birth_time, "query"],
        ["birthPlace", form.birth_place, "query"],
        ["locationId", form.location_id, "query"],
        ["gender", form.gender, "query"],
        ["reportSystem", form.report_system or "bazi", "query"],
        ["name", form.name, "query"],
    ]
    if result:
        rows.extend(
            [
                ["selectedReportSystem", result.report_system_label, "server"],
                ["normalizedBirthTime", result.normalized_time, "server"],
                ["resolvedLocationId", result.resolved_location_id, "location.resolve"],
                ["resolvedLocationName", result.resolved_location_name, "location.resolve"],
                ["resolvedTimezone", result.resolved_timezone, "IANA"],
                ["coordinatePrecision", result.coordinate_precision, "catalog"],
                ["longitude", result.resolved_longitude, "location.resolve"],
                ["latitude", result.resolved_latitude, "location.resolve"],
            ]
        )
    table = tabulate(rows, headers=["字段", "值", "来源"], tablefmt="psql", missingval="")
    return f'<h2 id="submitted-input">当前输入</h2>\n<pre><code>{_h(table)}</code></pre>'


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
            "<pre><code>"
            + _h(tabulate(pillar_rows, headers=["柱位", "干支", "天干", "地支"], tablefmt="psql"))
            + "</code></pre>",
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
            "<pre><code>"
            + _h(tabulate(trigger_rows, headers=["年份", "干支", "触发依据"], tablefmt="psql"))
            + "</code></pre>",
            "</details>",
            "<details><summary>专题 profile / 风险边界</summary>",
            "<pre><code>"
            + _h(
                tabulate(
                    profile_rows,
                    headers=["专题", "分数", "生命周期", "依据", "证据字段", "风险边界"],
                    tablefmt="psql",
                )
            )
            + "</code></pre>",
            "</details>",
            "<details><summary>规则深度 / 冲突策略</summary>",
            "<pre><code>"
            + _h(
                tabulate(
                    rule_rows,
                    headers=["规则", "主题", "状态", "置信度", "证据字段", "风险边界"],
                    tablefmt="psql",
                )
            )
            + "</code></pre>",
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
            "<pre><code>"
            + _h(tabulate(palace_rows, headers=["宫位", "地支", "主星", "命宫", "身宫"], tablefmt="psql"))
            + "</code></pre>",
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


def _render_workbench_style() -> str:
    return "\n".join(
        [
            "<style>",
            "html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }",
            "#workspace { position: relative; isolation: isolate; width: 100%; height: 100vh; overflow: hidden; --workbench-edge-gap: 4px; }",
            "#top-layer { position: absolute; inset: 0; z-index: 3; pointer-events: none; font-size: 32px; }",
            "#sidebar-toggle { position: absolute; inset-block-start: 0; inset-inline-start: 0; pointer-events: auto; appearance: none; border: 0; background: transparent; padding: 0; margin-block-start: var(--workbench-edge-gap); margin-inline-start: var(--workbench-edge-gap); margin-block-end: 0; margin-inline-end: 0; font: inherit; cursor: pointer; }",
            "#sidebar-toggle[data-ink-measured] { inline-size: var(--toggle-ink-inline-size); block-size: var(--toggle-ink-block-size); }",
            "#sidebar-toggle > [data-glyph-canvas] { display: block; inline-size: 0; block-size: 0; pointer-events: none; }",
            "#sidebar-toggle[data-ink-measured] > [data-glyph-canvas] { inline-size: 100%; block-size: 100%; }",
            "#control-plane { position: absolute; inset-block: 0; inset-inline-start: 0; z-index: 2; width: clamp(320px, 28vw, 440px); min-width: 0; max-height: 100vh; padding-block-start: var(--content-top, 0px); padding-inline: var(--workbench-edge-gap); padding-block-end: 2rem; overflow-x: hidden; overflow-y: scroll; background: Canvas; box-sizing: border-box; }",
            "#control-plane h1 { margin-block-start: 0; }",
            "#control-plane pre { max-width: 100%; overflow: auto; box-sizing: border-box; }",
            "#control-plane fieldset { min-width: 0; max-width: 100%; width: 100%; margin-inline: 0; box-sizing: border-box; }",
            "#control-plane input, #control-plane select, #control-plane button { max-width: 100%; box-sizing: border-box; }",
            "#data-plane { position: relative; width: 100%; height: 100vh; min-height: 0; z-index: 1; overflow: auto; padding-block-start: var(--content-top, 0px); padding-inline: var(--workbench-edge-gap); box-sizing: border-box; }",
            "#data-plane > :first-child { margin-block-start: 0; }",
            "#data-plane pre { max-width: 100%; overflow: auto; }",
            '#workspace[data-sidebar="collapsed"] #control-plane { display: none; }',
            "@media (max-width: 959px) { #control-plane { width: 100%; } }",
            "</style>",
        ]
    )


def _render_copy_script() -> str:
    return "\n".join(
        [
            "<script>",
            "(() => {",
            '  const workspace = document.getElementById("workspace");',
            '  const control = document.getElementById("control-plane");',
            '  const toggle = document.getElementById("sidebar-toggle");',
            '  const glyphCanvas = toggle && toggle.querySelector("[data-glyph-canvas]");',
            "  if (!workspace || !control || !toggle || !glyphCanvas) { return; }",
            "  const readContentGap = () => {",
            '    const gap = Number.parseFloat(getComputedStyle(workspace).getPropertyValue("--workbench-edge-gap"));',
            '    if (!Number.isFinite(gap) || gap < 0) { throw new Error("native workbench edge gap is invalid"); }',
            "    return gap;",
            "  };",
            "  const cropGlyphToInk = () => {",
            "    const style = getComputedStyle(toggle);",
            "    const glyph = toggle.dataset.glyph;",
            "    const fontSize = Number.parseFloat(style.fontSize);",
            "    const scale = Math.max(1, window.devicePixelRatio || 1);",
            "    const font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;",
            "    const probe = document.createElement('canvas');",
            "    const context = probe.getContext('2d', { willReadFrequently: true });",
            "    if (!context || !glyph || !Number.isFinite(fontSize) || fontSize <= 0) { throw new Error('native workbench toggle glyph measurement failed'); }",
            "    context.font = font;",
            "    const metrics = context.measureText(glyph);",
            "    const ascent = Number.isFinite(metrics.actualBoundingBoxAscent) ? metrics.actualBoundingBoxAscent : fontSize;",
            "    const descent = Math.max(0, Number.isFinite(metrics.actualBoundingBoxDescent) ? metrics.actualBoundingBoxDescent : fontSize * 0.25);",
            "    const left = Number.isFinite(metrics.actualBoundingBoxLeft) ? metrics.actualBoundingBoxLeft : 0;",
            "    const right = Number.isFinite(metrics.actualBoundingBoxRight) ? metrics.actualBoundingBoxRight : metrics.width;",
            "    const logicalWidth = Math.max(metrics.width, left + right);",
            "    if (!Number.isFinite(logicalWidth) || logicalWidth <= 0 || ascent <= 0) { throw new Error('native workbench toggle glyph metrics are invalid'); }",
            "    probe.width = Math.max(1, Math.ceil(logicalWidth * scale) + 1);",
            "    probe.height = Math.max(1, Math.ceil((ascent + descent) * scale) + 1);",
            "    context.setTransform(scale, 0, 0, scale, 0, 0);",
            "    context.font = font;",
            "    context.textAlign = 'start';",
            "    context.textBaseline = 'alphabetic';",
            "    context.fillStyle = '#000';",
            "    context.fillText(glyph, left, ascent);",
            "    const image = context.getImageData(0, 0, probe.width, probe.height);",
            "    let minX = probe.width; let minY = probe.height; let maxX = -1; let maxY = -1;",
            "    for (let y = 0; y < probe.height; y += 1) {",
            "      for (let x = 0; x < probe.width; x += 1) {",
            "        if (image.data[(y * probe.width + x) * 4 + 3] === 0) continue;",
            "        minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);",
            "      }",
            "    }",
            "    if (maxX < minX || maxY < minY) { throw new Error('native workbench toggle glyph has no visible ink'); }",
            "    const pixelWidth = maxX - minX + 1;",
            "    const pixelHeight = maxY - minY + 1;",
            "    const cropped = context.getImageData(minX, minY, pixelWidth, pixelHeight);",
            "    const output = glyphCanvas.getContext('2d');",
            "    if (!output) { throw new Error('native workbench glyph canvas is unavailable'); }",
            "    glyphCanvas.width = pixelWidth;",
            "    glyphCanvas.height = pixelHeight;",
            "    glyphCanvas.style.inlineSize = `${pixelWidth / scale}px`;",
            "    glyphCanvas.style.blockSize = `${pixelHeight / scale}px`;",
            "    output.putImageData(cropped, 0, 0);",
            "    return { width: pixelWidth / scale, height: pixelHeight / scale };",
            "  };",
            "  const syncLayout = () => {",
            '    toggle.removeAttribute("data-ink-measured");',
            '    toggle.style.removeProperty("--toggle-ink-inline-size");',
            '    toggle.style.removeProperty("--toggle-ink-block-size");',
            '    workspace.style.removeProperty("--content-top");',
            "    const ink = cropGlyphToInk();",
            '    toggle.style.setProperty("--toggle-ink-inline-size", `${ink.width}px`);',
            '    toggle.style.setProperty("--toggle-ink-block-size", `${ink.height}px`);',
            '    toggle.dataset.inkMeasured = "true";',
            "    const toggleBox = toggle.getBoundingClientRect();",
            "    const controlBox = control.getBoundingClientRect();",
            "    const contentTop = toggleBox.bottom - controlBox.top + readContentGap();",
            '    workspace.style.setProperty("--content-top", `${contentTop}px`);',
            "  };",
            '  let collapsed = window.innerWidth < 960 || workspace.dataset.sidebar === "collapsed";',
            "  const renderShell = () => {",
            '    workspace.dataset.sidebar = collapsed ? "collapsed" : "expanded";',
            '    control.setAttribute("aria-hidden", String(collapsed));',
            "    control.inert = collapsed;",
            '    toggle.setAttribute("aria-expanded", String(!collapsed));',
            '    toggle.setAttribute("aria-label", collapsed ? "展开控制面" : "收起控制面");',
            '    toggle.setAttribute("title", collapsed ? "展开控制面" : "收起控制面");',
            '    toggle.dataset.glyph = collapsed ? "➡️" : "⬅️";',
            "    syncLayout();",
            "  };",
            "  renderShell();",
            '  toggle.addEventListener("click", () => { collapsed = !collapsed; renderShell(); });',
            '  window.addEventListener("resize", syncLayout);',
            "})();",
            "(() => {",
            '  const form = document.getElementById("web-report-form");',
            '  const reportState = document.getElementById("production-report-state");',
            "  if (!form) { return; }",
            '  const locationInput = document.getElementById("birthPlace");',
            '  const locationIdInput = document.getElementById("locationId");',
            '  const locationOptions = document.getElementById("birth-place-options");',
            "  let locationTimer = 0;",
            "  let locationRequest = null;",
            "  let locationCandidates = new Map();",
            "  const bindLocationCandidate = () => {",
            "    if (!locationInput || !locationIdInput) { return false; }",
            "    const candidate = locationCandidates.get(locationInput.value.trim());",
            "    locationIdInput.value = candidate ? candidate.locationId : '';",
            "    if (candidate) { locationInput.setCustomValidity(''); }",
            "    return Boolean(candidate);",
            "  };",
            "  const renderLocationCandidates = (items) => {",
            "    if (!locationOptions) { return; }",
            "    locationCandidates = new Map();",
            "    locationOptions.replaceChildren();",
            "    items.forEach((item) => {",
            "      const label = String(item.displayName || item.name || '');",
            "      if (!label || !item.locationId) { return; }",
            "      locationCandidates.set(label, item);",
            "      const option = document.createElement('option');",
            "      option.value = label;",
            "      locationOptions.appendChild(option);",
            "    });",
            "  };",
            "  const searchLocations = async (query) => {",
            "    if (locationRequest) { locationRequest.abort(); }",
            "    locationRequest = new AbortController();",
            "    try {",
            '      const response = await fetch(`/api/v1/locations?q=${encodeURIComponent(query)}&mode=domestic&limit=8`, { signal: locationRequest.signal, headers: { accept: "application/json" } });',
            "      const body = await response.json();",
            '      if (!response.ok || !body.success) { throw new Error(body.error || "地区查找失败"); }',
            "      const items = body.data && Array.isArray(body.data.locations) ? body.data.locations : [];",
            "      renderLocationCandidates(items);",
            "      bindLocationCandidate();",
            "    } catch (error) {",
            "      if (error && error.name === 'AbortError') { return; }",
            "    }",
            "  };",
            "  if (locationInput && locationIdInput && locationOptions) {",
            "    locationInput.addEventListener('input', () => {",
            "      locationIdInput.value = '';",
            "      locationInput.setCustomValidity('');",
            "      window.clearTimeout(locationTimer);",
            "      const query = locationInput.value.trim();",
            "      if (bindLocationCandidate()) { return; }",
            "      if (locationRequest) { locationRequest.abort(); }",
            "      renderLocationCandidates([]);",
            "      if (!query) {",
            "        return;",
            "      }",
            "      locationTimer = window.setTimeout(() => searchLocations(query), 100);",
            "    });",
            "    locationInput.addEventListener('change', bindLocationCandidate);",
            "  }",
            "  const setSubmitting = () => {",
            '    const submitButton = document.getElementById("generate-report");',
            "    if (submitButton) {",
            '      submitButton.setAttribute("aria-busy", "true");',
            '      submitButton.textContent = "生成中...";',
            "    }",
            '    if (reportState) { reportState.textContent = "正在生成 Markdown 报告..."; }',
            "  };",
            "  const setIdle = () => {",
            '    const submitButton = document.getElementById("generate-report");',
            "    if (submitButton) {",
            '      submitButton.removeAttribute("aria-busy");',
            '      submitButton.textContent = "生成 Markdown 报告";',
            "    }",
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
            "    if (locationInput && locationIdInput && !locationIdInput.value) {",
            "      locationInput.setCustomValidity(locationInput.value.trim() ? '请从候选列表选择完整地区' : '请输入出生地区');",
            "      locationInput.focus();",
            "      locationInput.reportValidity();",
            "      return;",
            "    }",
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
