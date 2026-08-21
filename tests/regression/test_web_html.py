from __future__ import annotations

import re
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

from main import app  # noqa: E402


def assert_psql_row(text: str, *cells: str) -> None:
    pattern = r"\|\s*" + r"\s*\|\s*".join(re.escape(cell) for cell in cells) + r"\s*\|"
    assert re.search(pattern, text)


def assert_zero_beauty_semantic_html(text: str) -> None:
    """保留零美化内容规则，同时验证登记的三层结构例外。"""
    assert "<style>" in text
    assert "style=" not in text
    assert 'rel="stylesheet"' not in text
    assert "class=" not in text
    assert '<div id="workspace" data-sidebar="expanded"' in text
    assert (
        '<div id="top-layer" data-layer="top" data-workbench-layer="top" aria-label="工作台交互层">\n'
        '<button id="sidebar-toggle" type="button" aria-controls="control-plane" aria-expanded="true"' in text
    )
    assert (
        '<aside id="control-plane" data-layer="middle" data-workbench-layer="middle" aria-label="项目说明与参数控制面">\n'
        "<h1>faetcat</h1>" in text
    )
    assert '<fieldset id="control-content" aria-labelledby="input-form">' in text
    assert (
        '<main id="data-plane" data-layer="bottom" data-workbench-layer="bottom" aria-labelledby="production-report">'
        in text
    )
    assert '<div id="report-content">' in text
    assert "padding-inline-start: calc(clamp(320px, 28vw, 440px) + 1rem)" in text
    assert '#workspace[data-sidebar="expanded"] #report-content' not in text
    assert "z-index: 3" in text
    assert "z-index: 2" in text
    assert "z-index: 1" in text
    assert "width: clamp(320px, 28vw, 440px)" in text
    assert '<form id="web-report-form" method="get" action="/web">' in text
    for forbidden in [
        "box-shadow",
        "border-radius",
        "font-family",
        "grid-template",
        "linear-gradient",
        "animation",
        "transition",
    ]:
        assert forbidden not in text


def domestic_form_params(**overrides: str) -> dict[str, str]:
    params = {
        "birthDate": "1990-01-01",
        "birthTime": "08:00",
        "birthPlace": "北京市朝阳区",
        "locationId": "cn:110105",
        "gender": "male",
        "name": "测试样本",
    }
    params.update(overrides)
    return params


def test_web_page_renders_semantic_form():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    text = response.text
    assert "<title>faetcat</title>" in text
    assert "<h1>faetcat</h1>" in text
    assert '<link rel="alternate" type="text/plain" href="/llms.txt" title="FateCat llms.txt">' in text
    assert '<html lang="zh-CN" data-workbench-profile="tradecatlabs.native-workbench.v0.1.compatibility">' in text
    assert '<ul data-layer="top" data-workbench-layer="top">' in text
    assert re.search(r'<input id="birthDate"[^>]*data-layer="middle"[^>]*data-workbench-layer="middle">', text)
    assert 'id="production-report-state" data-layer="bottom" data-workbench-layer="bottom"' in text
    assert '<link rel="canonical" href="https://tradecatlabs-fatecat.hf.space/web">' in text
    assert '<meta name="description"' in text
    assert '<meta name="author" content="TradeCat Labs">' in text
    assert '<script type="application/ld+json">' in text
    assert '<h2 id="project-brand">项目与页面信息</h2>' in text
    assert '<div id="workspace" data-sidebar="expanded"' in text
    assert '<div id="top-layer" data-layer="top" data-workbench-layer="top"' in text
    assert '<aside id="control-plane" data-layer="middle" data-workbench-layer="middle"' in text
    assert '<main id="data-plane" data-layer="bottom" data-workbench-layer="bottom"' in text
    assert '<button id="sidebar-toggle" type="button"' in text
    assert_psql_row(text, "项目归属", "交易猫实验室｜FateCat 测算基础设施")
    assert_psql_row(text, "项目定位", "FateCat 是面向 Agent 与应用开发者的测算基础设施。")
    assert_psql_row(text, "核心能力", "提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。")
    assert_psql_row(text, "CA", "0x8a99b8d53eff6bc331af529af74ad267f3167777")
    assert text.index("| CA") < text.index("| 项目归属")
    assert_psql_row(text, "页面说明", "使用原生 HTML 表单生成标准命理排盘 Markdown 报告；公开入口优先走异步任务。")
    assert "<h3>全部链接</h3>" in text
    assert "TradeCat Labs｜FateCat 测算基础设施" not in text
    assert "FateCat 是面向 Agent 与应用开发者的测算基础设施。" in text
    assert "https://dexscreener.com/bsc/0x8a99b8d53eff6bc331af529af74ad267f3167777" in text
    assert "https://x.com/tradecatlabs" in text
    assert "https://github.com/tradecatlabs" in text
    assert "https://huggingface.co/tradecatlabs" in text
    assert "免费 AI 分析入口（Gemini Gem）" in text
    assert "https://gemini.google.com/gem/1d9XompAC8xk0xV6655X9IxZYQUNkDJoG?usp=sharing" in text
    assert '<a href="/llms.txt">AI / Agent 文档（llms.txt）</a>' in text
    assert '<nav aria-label="项目、页面与服务链接">' in text
    assert '<a href="#project-brand">页面：项目与页面信息</a>' in text
    assert '<a href="#production-report">页面：生成报告</a>' in text
    assert '<a href="#input-form">页面：参数控件</a>' in text
    assert 'href="#field-contract"' not in text
    assert_zero_beauty_semantic_html(text)
    assert '<form id="web-report-form" method="get" action="/web">' in text
    assert text.index('<h2 id="project-brand">') < text.index('<h2 id="input-form">')
    assert text.index('<h2 id="input-form">') < text.index('<h2 id="production-report">')
    assert '<h2 id="production-report">生成报告</h2>' in text
    assert "<fieldset>\n<legend>排盘参数</legend>" in text
    assert (
        '<p><button id="generate-report" type="submit" name="submitted" value="1">生成 Markdown 报告</button></p>'
    ) in text
    assert "尚未生成报告。提交底部参数后，服务端会在这里写入 Markdown 输出。" in text
    assert 'id="production-report-state"' in text
    assert 'form.addEventListener("submit"' in text
    assert 'fetch("/api/v1/report/jobs/web"' in text
    assert "pollJob(jobId)" in text
    assert "正在生成 Markdown 报告..." in text
    assert "const setIdle = () =>" in text
    assert 'submitButton.textContent = "生成 Markdown 报告";' in text
    assert '<input type="hidden" name="submitted" value="1">' not in text
    assert " required>" not in text
    assert '<details id="page-info">' not in text
    assert "<summary>页面说明与元信息</summary>" not in text
    assert_psql_row(text, "可用体系", "综合八字 bazi；紫微斗数 ziwei")
    assert_psql_row(text, "输出", "Markdown 文本")
    assert_psql_row(text, "时区", "Asia/Hong_Kong")
    assert "免费公开入口默认不写数据库" in text
    assert "FateCat 不会自动发送报告到 Gemini" in text
    assert_psql_row(text, "AI / Agent 文档", "GET /llms.txt")
    for moved_field in ("报告模板", "地区解析", "服务入口", "字段契约", "birthDate", "birthTime", "birthPlace"):
        assert not re.search(rf"\|\s*{re.escape(moved_field)}\s*\|", text)
    assert "字段契约 ·" not in text
    assert '<h2 id="field-contract">字段契约</h2>' not in text
    assert "参数控件" in text
    assert "出生日期（必填）" in text
    assert "出生时间（必填）" in text
    assert "出生地区（必填）" in text
    assert "性别（必填）" in text
    assert "输出体系" in text
    assert '<select id="reportSystem" name="reportSystem">' in text
    assert "综合八字 bazi" in text
    assert "紫微斗数 ziwei" in text
    assert "黄历/择日 huangli（待实现）" in text
    assert "六爻占卜 liuyao（待实现）" in text
    assert "梅花易数 meihua（结构化 capability 已可用）" in text
    assert "奇门遁甲 qimen（待实现）" in text
    assert "袁天罡称骨 bone" not in text
    assert "姓名（非必填）" in text
    assert "<pre><code>+" in text


def test_llms_txt_exposes_machine_contract_and_is_shipped_to_hf():
    response = TestClient(app).get("/llms.txt")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    text = response.text
    assert text.startswith("# FateCat\n")
    assert "TradeCat Labs（交易猫实验室）" in text
    assert "POST /api/v1/report/jobs/web" in text
    assert "GET /api/v1/report/jobs/{job_id}" in text
    assert "GET /api/v1/locations?q={query}&mode=domestic&limit=8" in text
    assert "`birthDate`" in text
    assert "`locationId`" in text
    assert "Public API warm round trip" in text
    assert "344 ms median" in text
    assert "Web input debounce: 100 ms" in text
    assert "Browser input-to-candidate rendering" in text
    assert "459 ms median" in text
    assert "First browser query after a Space rebuild: 4.51 s" in text
    assert "not a latency SLA" in text
    assert "## Canonical Identity" in text
    assert "## Availability Matrix" in text
    assert "## High-Intent Questions and Answers" in text
    assert "## Citation Guidance" in text

    deploy_script = (ROOT / "scripts" / "hf-space-deploy.sh").read_text(encoding="utf-8")
    assert re.search(r"\n\s+llms\.txt\s+\\", deploy_script)


def test_web_page_uses_one_native_fuzzy_location_input():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    text = response.text
    assert (
        '<input id="birthPlace" name="birthPlace" type="text" list="birth-place-options" '
        'autocomplete="off" maxlength="160"' in text
    )
    assert '<input id="locationId" name="locationId" type="hidden" value="">' in text
    assert '<datalist id="birth-place-options"></datalist>' in text
    assert 'id="birth-place-status"' not in text
    assert 'aria-describedby="birth-place-status"' not in text
    assert "setLocationStatus" not in text
    assert "正在查找地区" not in text
    assert "找到 ${items.length} 个候选" not in text
    assert "未找到地区" not in text
    assert "已选择：" not in text
    assert "searchLocations" in text
    assert "/api/v1/locations?q=" in text
    assert "mode=domestic&limit=8" in text
    assert "window.setTimeout(() => searchLocations(query), 100)" in text
    assert "if (!query)" in text
    assert "query.length < 2" not in text
    assert "输入至少两个字" not in text
    assert "locationIdInput.value = '';" in text
    assert "locationInput.setCustomValidity('');" in text
    assert "locationInput.reportValidity();" in text
    assert "请从候选列表选择完整地区" in text
    for removed in [
        'id="birthProvince"',
        'id="birthCity"',
        'id="locationMode"',
        'id="timeBasis"',
        'id="foldChoice"',
        'id="domestic-location-hierarchy"',
        'name="locationMode"',
        'name="timeBasis"',
        "地区模式（必填）",
        "出生时间口径（必填）",
        "WGS84 经纬度",
    ]:
        assert removed not in text
    assert "<style>" in text
    assert "class=" not in text


def test_web_page_no_javascript_fallback_accepts_full_location_name():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(locationId="", birthPlace="陕西省西安市长安区"),
    )

    assert response.status_code == 200
    assert '<h2 id="errors">错误</h2>' not in response.text
    assert '"locationId": "cn:610116"' in response.text
    assert '"birthPlace": "陕西省西安市长安区"' in response.text


def test_web_page_reports_missing_required_fields():
    response = TestClient(app).get("/web", params={"birthDate": "1990-01-01"})

    assert response.status_code == 200
    text = response.text
    assert '<h2 id="errors">错误</h2>' in text
    assert "缺少必填字段" in text
    assert "出生时间" in text
    assert "出生地区" in text
    assert "性别" in text


def test_web_page_empty_submit_reports_server_side_errors():
    response = TestClient(app).get("/web", params={"submitted": "1"})

    assert response.status_code == 200
    text = response.text
    assert_zero_beauty_semantic_html(text)
    assert '<h2 id="errors">错误</h2>' in text
    assert "缺少必填字段" in text
    assert "出生日期" in text
    assert "出生时间" in text
    assert "出生地区" in text
    assert "性别" in text


def test_web_page_reports_ambiguous_unselected_location():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(locationId="", birthPlace="长安区"),
    )

    assert response.status_code == 200
    assert "地点存在多个匹配" in response.text
    assert "河北省石家庄市长安区" in response.text
    assert "陕西省西安市长安区" in response.text


def test_web_page_rejects_mismatched_location_name_and_id():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(birthPlace="上海市黄浦区", locationId="cn:110105"),
    )

    assert response.status_code == 200
    assert "出生地区名称与所选候选不一致" in response.text


def test_web_page_uses_qualified_location_candidate_for_report_coordinates():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(
            birthPlace="陕西省西安市长安区",
            locationId="cn:610116",
        ),
    )

    assert response.status_code == 200
    assert '<h2 id="errors">错误</h2>' not in response.text
    assert '"birthPlace": "陕西省西安市长安区"' in response.text
    assert '"locationId": "cn:610116"' in response.text
    assert '"longitude": 108.93366' in response.text
    assert '"latitude": 34.03702' in response.text


def test_web_page_generates_copyable_markdown_report():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(),
    )

    assert response.status_code == 200
    text = response.text
    assert_zero_beauty_semantic_html(text)
    assert '<a href="#workbench">页面：工作台</a>' in text
    assert '<a href="#markdown-output">页面：Markdown 输出</a>' in text
    assert '<button type="button" id="copy-report">复制 Markdown</button>' in text
    assert '<h2 id="markdown-output">Markdown 输出</h2>' in text
    assert '<pre><code id="report-markdown">' in text
    assert '<h2 id="workbench">八字工作台</h2>' in text
    assert "<details><summary>专题 profile / 风险边界</summary>" in text
    assert "财运 profile 只作结构趋势证据" in text
    assert "健康 profile 只作五行结构压力证据" in text
    assert "lifecycle" not in text
    for forbidden in ("医疗建议", "投资建议", "法律建议", "心理建议", "必然", "保证", "灾祸"):
        assert forbidden not in text
    assert text.index('<pre><code id="report-markdown">') < text.index('<h2 id="workbench">八字工作台</h2>')
    assert text.index('<h2 id="project-brand">项目与页面信息</h2>') < text.index('<pre><code id="report-markdown">')
    assert "**TradeCat Labs 实验室**" in text
    assert "# 命理排盘报告：测试样本" in text
    assert "当前输出体系：综合八字" in text
    assert "### 八字排盘详情" in text
    assert "## 紫微斗数" not in text
    assert "## 第三卷：民俗与建议（生活应用）" in text
    assert "### 袁天罡称骨" in text
    assert "机器可读输入" in text
    assert '"birthPlace": "北京市朝阳区"' in text
    assert '"locationId": "cn:110105"' in text
    assert '"reportSystem": "bazi"' in text


def test_web_page_workbench_does_not_recalculate_domain_rules():
    source = (TELEGRAM_SRC / "web_ui.py").read_text(encoding="utf-8")

    assert "from web_report_service import build_web_report_result" in source
    for forbidden in [
        "from fate_core.capabilities import",
        "from fate_core.usecases import",
        "from fate_core.usecases.evaluators",
        "CapabilityExecutor(",
        "calculate_pure_analysis",
        "rules_for_system(",
        "build_fortune_trigger_matrix",
        "bazi.depth.",
    ]:
        assert forbidden not in source


def test_web_page_can_select_ziwei_report_without_bazi_blocks():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(reportSystem="ziwei"),
    )

    assert response.status_code == 200
    text = response.text
    assert "当前输出体系：紫微斗数" in text
    assert "# 紫微斗数报告：测试样本" in text
    assert "## 紫微斗数" in text
    assert "### 入盘依据" in text
    assert "### 命宫与身宫" in text
    assert "## 紫微结构解读（依据版）" in text
    assert "### 主星组合" in text
    assert "### 三方四正" in text
    assert "### 四化落宫" in text
    assert "### 大限/流年联动" in text
    assert "## 紫微运限四化（大限/流年/流月/流日/流时）" in text
    assert "## 紫微基础" not in text
    assert "八字排盘详情" not in text
    assert "袁天罡称骨" not in text
    assert '"reportSystem": "ziwei"' in text
    assert '<h2 id="workbench">紫微工作台</h2>' in text
    assert text.index('<pre><code id="report-markdown">') < text.index('<h2 id="workbench">紫微工作台</h2>')


def test_web_page_rejects_retired_report_systems():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(reportSystem="jianchu"),
    )

    assert response.status_code == 200
    assert_zero_beauty_semantic_html(response.text)
    assert '<h2 id="errors">错误</h2>' in response.text
    assert "报告体系必须为: bazi、ziwei。未来体系需等独立功能实现后启用。" in response.text
    assert "# 建除十二神报告" not in response.text

    bone_response = TestClient(app).get(
        "/web",
        params=domestic_form_params(reportSystem="bone"),
    )
    assert bone_response.status_code == 200
    assert_zero_beauty_semantic_html(bone_response.text)
    assert "报告体系必须为: bazi、ziwei。未来体系需等独立功能实现后启用。" in bone_response.text
    assert "# 袁天罡称骨报告" not in bone_response.text


def test_web_page_displays_submitted_birth_place_in_frontend():
    response = TestClient(app).get(
        "/web",
        params=domestic_form_params(
            birthPlace="上海市黄浦区",
            locationId="cn:310101",
        ),
    )

    assert response.status_code == 200
    text = response.text
    assert "出生地区" in text
    assert "上海" in text
    assert "已填写（非北京地区已隐藏）" not in text
