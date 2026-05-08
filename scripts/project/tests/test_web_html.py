from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
TELEGRAM_SRC = ROOT / "modules" / "telegram" / "src"
FATE_CORE_SRC = ROOT / "modules" / "fate_core" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

from main import app  # noqa: E402


def test_web_page_renders_semantic_form():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    text = response.text
    assert "<h1>FateCat Web Markdown 报告</h1>" in text
    assert '<form method="get" action="/web">' in text
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
    assert "<h2>错误</h2>" in text
    assert "缺少必填字段" in text
    assert "出生时间" in text
    assert "出生地区" in text
    assert "性别" in text


def test_web_page_reports_unknown_birth_place():
    hidden_place = "不存在的地区"
    response = TestClient(app).get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": hidden_place,
            "gender": "male",
        },
    )

    assert response.status_code == 200
    assert "地点无法识别" in response.text
    assert hidden_place not in response.text
    assert "已填写（非北京地区已隐藏）" in response.text


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
    assert '<button type="button" id="copy-report">复制 Markdown</button>' in text
    assert '<pre><code id="report-markdown">' in text
    assert "## 赞助支持" in text
    assert "# 命理排盘报告：测试样本" in text
    assert "当前输出体系：综合八字" in text
    assert "## 八字排盘详情" in text
    assert "## 紫微斗数" not in text
    assert "## 第三卷：民俗与建议（生活应用）" in text
    assert "## 袁天罡称骨" in text
    assert "机器可读输入" in text
    assert '"birthPlace": "北京"' in text
    assert '"reportSystem": "bazi"' in text


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
    assert "## 紫微运限四化（大限/流年/流月/流日/流时）" in text
    assert "## 紫微基础" not in text
    assert "## 八字排盘详情" not in text
    assert "## 袁天罡称骨" not in text
    assert '"reportSystem": "ziwei"' in text


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
    assert "<h2>错误</h2>" in response.text
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
    assert "报告体系必须为: bazi、ziwei。未来体系需等独立功能实现后启用。" in bone_response.text
    assert "# 袁天罡称骨报告" not in bone_response.text


def test_web_page_hides_non_beijing_birth_place_in_frontend():
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
    assert "上海" not in text
    assert "已填写（非北京地区已隐藏）" in text
