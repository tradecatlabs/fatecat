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


def assert_web_production_layout_html(text: str) -> None:
    assert "style=" not in text
    assert "<main>" not in text
    assert '<body>\n<form id="web-report-form" class="web-production-grid"' in text
    assert "<h1>FateCat Web Markdown 报告</h1>" not in text
    assert "--phi-major: 61.8034%;" in text
    assert "--phi-minor: 38.1966%;" in text
    assert "--phi-major-fr: 1.61803398875fr;" in text
    assert "--phi-minor-fr: 1fr;" in text
    assert "--web-production-panel-gap: 0;" in text
    assert "--web-production-panel-border: #3a3a3a;" in text
    assert "--web-production-panel-bg: #202020;" in text
    assert "--web-production-body-bg: #111;" in text
    assert "html { height: 100%; overflow: hidden; }" in text
    assert "height: calc(100vh - 2rem);" in text
    assert "minmax(0, min(var(--phi-minor), calc((100vh - 2rem) * 0.618034)))" in text
    assert "grid-template-rows: minmax(0, var(--phi-major-fr)) minmax(0, var(--phi-minor-fr));" in text
    assert "border: 1px solid var(--web-production-panel-border);" in text
    assert "background: var(--web-production-panel-bg);" in text
    assert "@media (max-width: 56rem)" in text
    for forbidden in [
        "box-shadow",
        "linear-gradient",
        "animation",
        "transition",
    ]:
        assert forbidden not in text
    allowed_classes = {
        "web-production-grid",
        "web-production-panel",
        "web-production-brand",
        "web-production-report",
        "web-production-report-header",
        "web-production-submit-button",
        "web-production-input",
        "web-production-control-grid",
        "web-production-control-wide",
    }
    for class_value in re.findall(r'class="([^"]+)"', text):
        assert set(class_value.split()).issubset(allowed_classes)


def test_web_page_renders_semantic_form():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    text = response.text
    assert "<title>FateCat Web Markdown 报告</title>" in text
    assert "<h1>FateCat Web Markdown 报告</h1>" not in text
    assert '<h2 id="project-brand">项目归属</h2>' in text
    assert "TradeCat Labs｜FateCat 命理 AI 实验室项目" in text
    assert "FateCat 是 TradeCat Labs 的实验室项目。" in text
    assert "https://dexscreener.com/bsc/0x8a99b8d53eff6bc331af529af74ad267f3167777" in text
    assert "https://x.com/tradecatlabs" in text
    assert "https://github.com/tradecatlabs" in text
    assert "https://huggingface.co/tradecatlabs" in text
    assert "免费 AI 分析入口（Gemini Gem）" in text
    assert "https://gemini.google.com/gem/1d9XompAC8xk0xV6655X9IxZYQUNkDJoG?usp=sharing" in text
    assert '<nav aria-label="页面导航">' in text
    assert '<a href="#project-brand">项目</a>' in text
    assert '<a href="#production-report">报告</a>' in text
    assert '<a href="#input-form">参数</a>' in text
    assert_web_production_layout_html(text)
    assert '<form id="web-report-form" class="web-production-grid" method="get" action="/web">' in text
    assert '<section class="web-production-panel web-production-brand" aria-labelledby="project-brand">' in text
    assert '<section class="web-production-panel web-production-report" aria-labelledby="production-report">' in text
    assert '<section class="web-production-panel web-production-input" aria-labelledby="input-form">' in text
    assert text.index('class="web-production-panel web-production-brand"') < text.index(
        'class="web-production-panel web-production-report"'
    )
    assert text.index('class="web-production-panel web-production-report"') < text.index(
        'class="web-production-panel web-production-input"'
    )
    assert '<h2 id="production-report">生成报告</h2>' in text
    assert '<div class="web-production-report-header">' in text
    assert (
        '<button class="web-production-submit-button" type="submit" form="web-report-form">生成 Markdown 报告</button>'
    ) in text
    assert "尚未生成报告。提交底部参数后，服务端会在这里写入 Markdown 输出。" in text
    assert 'id="production-report-state"' in text
    assert 'form.addEventListener("submit"' in text
    assert 'fetch("/api/v1/report/jobs/web"' in text
    assert "pollJob(jobId)" in text
    assert "正在生成 Markdown 报告..." in text
    assert "const setIdle = () =>" in text
    assert 'submitButton.textContent = "生成 Markdown 报告";' in text
    assert '<input type="hidden" name="submitted" value="1">' in text
    assert " required>" not in text
    assert '<details id="page-info">\n<summary>页面说明与元信息</summary>' in text
    assert "<details open>\n<summary>页面说明与元信息</summary>" not in text
    assert text.index(
        '<form id="web-report-form" class="web-production-grid" method="get" action="/web">'
    ) < text.index("<summary>页面说明与元信息</summary>")
    assert "页面元信息" in text
    assert "POST /api/v1/report/jobs/web；GET /api/v1/report/jobs/{job_id}" in text
    assert "免费公开入口默认不写数据库" in text
    assert "FateCat 不会自动发送报告到 Gemini" in text
    assert "相关入口" in text
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


def test_web_page_static_examples_do_not_show_non_beijing_regions():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    text = response.text
    assert "例 北京 / 116.4074,39.9042" in text
    blocked_terms = ("".join(["济", "南"]), "".join(["历", "下区"]))
    for term in blocked_terms:
        assert term not in text


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
    assert_web_production_layout_html(text)
    assert '<h2 id="errors">错误</h2>' in text
    assert "缺少必填字段" in text
    assert "出生日期" in text
    assert "出生时间" in text
    assert "出生地区" in text
    assert "性别" in text


def test_web_page_reports_unknown_birth_place():
    submitted_place = "不存在的地区"
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": submitted_place,
            "gender": "male",
        },
    )

    assert response.status_code == 200
    assert "地点无法识别" in response.text
    assert submitted_place in response.text


def test_web_page_generates_copyable_markdown_report():
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
        },
    )

    assert response.status_code == 200
    text = response.text
    assert_web_production_layout_html(text)
    assert '<a href="#workbench">工作台</a>' in text
    assert '<a href="#markdown-output">Markdown</a>' in text
    assert '<button type="button" id="copy-report">复制 Markdown</button>' in text
    assert '<h2 id="markdown-output">Markdown 输出</h2>' in text
    assert '<pre><code id="report-markdown">' in text
    assert '<section id="bazi-workbench">' in text
    assert "<details><summary>专题 profile / 风险边界</summary>" in text
    assert "财运 profile 只作结构趋势证据" in text
    assert "健康 profile 只作五行结构压力证据" in text
    assert "lifecycle" not in text
    for forbidden in ("医疗建议", "投资建议", "法律建议", "心理建议", "必然", "保证", "灾祸"):
        assert forbidden not in text
    assert text.index('<pre><code id="report-markdown">') < text.index('<section id="bazi-workbench">')
    assert text.index('<pre><code id="report-markdown">') < text.index("<summary>页面说明与元信息</summary>")
    assert "## TradeCat Labs 实验室" in text
    assert "# 命理排盘报告：测试样本" in text
    assert "当前输出体系：综合八字" in text
    assert "## 八字排盘详情" in text
    assert "## 紫微斗数" not in text
    assert "## 第三卷：民俗与建议（生活应用）" in text
    assert "## 袁天罡称骨" in text
    assert "机器可读输入" in text
    assert '"birthPlace": "北京"' in text
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
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "ziwei",
        },
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
    assert "## 八字排盘详情" not in text
    assert "## 袁天罡称骨" not in text
    assert '"reportSystem": "ziwei"' in text
    assert '<section id="ziwei-workbench">' in text
    assert text.index('<pre><code id="report-markdown">') < text.index('<section id="ziwei-workbench">')


def test_web_page_rejects_retired_report_systems():
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "jianchu",
        },
    )

    assert response.status_code == 200
    assert_web_production_layout_html(response.text)
    assert '<h2 id="errors">错误</h2>' in response.text
    assert "报告体系必须为: bazi、ziwei。未来体系需等独立功能实现后启用。" in response.text
    assert "# 建除十二神报告" not in response.text

    bone_response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "bone",
        },
    )
    assert bone_response.status_code == 200
    assert_web_production_layout_html(bone_response.text)
    assert "报告体系必须为: bazi、ziwei。未来体系需等独立功能实现后启用。" in bone_response.text
    assert "# 袁天罡称骨报告" not in bone_response.text


def test_web_page_rejects_out_of_range_direct_coordinates():
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "999,999",
            "gender": "male",
            "name": "测试样本",
        },
    )

    assert response.status_code == 200
    assert_web_production_layout_html(response.text)
    assert '<h2 id="errors">错误</h2>' in response.text
    assert "经度必须在 -180 到 180 之间" in response.text


def test_web_page_displays_submitted_birth_place_in_frontend():
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "上海",
            "gender": "male",
            "name": "测试样本",
        },
    )

    assert response.status_code == 200
    text = response.text
    assert "出生地区" in text
    assert "已填写（非北京地区已隐藏）" in text
    assert "上海" not in text
