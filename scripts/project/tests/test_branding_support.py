#!/usr/bin/env python3
"""测试统一品牌配置加载与拼装。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modules" / "fate_core" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modules" / "telegram" / "src"))

from fate_core.support import (
    append_branding_text,
    build_branding_text,
    get_branding_payload,
    get_disclaimer_payload,
)


def test_get_branding_payload_contains_required_fields():
    branding = get_branding_payload()

    assert branding["name"] == "交易猫 TradeCat"
    assert branding["tradecatRepo"] == "https://github.com/tukuaiai/tradecat"
    assert branding["fatecatRepo"] == "https://github.com/tukuaiai/fatecat"
    assert branding["ca"] == "0x8a99b8d53eff6bc331af529af74ad267f3167777"


def test_get_disclaimer_payload_matches_required_text():
    disclaimer = get_disclaimer_payload()

    assert "本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。" in disclaimer
    assert "命理学非精密科学，命运掌握在自己手中。" in disclaimer
    assert "本开源项目及开发者概不负责。" in disclaimer


def test_append_branding_text_appends_sponsor_block():
    text = append_branding_text("测试正文", compact=True)

    assert text.startswith("⚠️ 免责声明")
    assert "测试正文" in text
    assert "交易猫 TradeCat" in text
    assert "TradeCat Repo: https://github.com/tukuaiai/tradecat" in text


def test_build_branding_text_puts_disclaimer_before_branding():
    text = build_branding_text(compact=False)

    assert text.startswith("⚠️ 免责声明")
    assert "交易猫 TradeCat｜专业命理排盘与 AI 命理分析基础设施" in text


def test_full_report_puts_sponsor_before_report_and_drops_extension_blocks():
    from report_generator import DEFAULT_HIDE, generate_full_report

    text = generate_full_report(
        {
            "input": {"name": "测试命主"},
            "boneWeight": {"weight": "3.8", "text": "测试评语"},
        },
        hide=dict.fromkeys(DEFAULT_HIDE, False),
    )

    assert text.startswith("⚠️ 免责声明")
    assert text.index("## 赞助支持") < text.index("# 命理排盘报告：测试命主")

    removed_sections = [
        "### 建除十二神",
        "## 紫微斗数",
        "## 紫微基础",
        "## 紫微运限四化（大限/流年/流月/流日/流时）",
        "## 健康预警（五行脏腑/养生提示）",
        "## 出生日黄历",
        "## 第五卷：学术参数（隐藏/技术区）",
        "## 六爻占卜",
        "## 梅花易数",
        "## 数字起卦",
        "## 奇门遁甲",
        "## 大六壬",
        "## 风水九星",
        "## 天文占星",
        "## 高级历法",
        "## 择日推荐",
        "## 易经系统",
        "## 姓名合婚模块",
        "## 系统优化与现代化八字",
    ]
    for section in removed_sections:
        assert section not in text
    assert "## 袁天罡称骨" in text


def test_full_report_default_heading_contract_matches_standard_blocks():
    from datetime import datetime

    from bazi_calculator import BaziCalculator
    from report_generator import build_report_hide, generate_full_report

    hide = build_report_hide("bazi")
    result = BaziCalculator(
        datetime(1990, 1, 1, 8, 0, 0),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试样本",
        birth_place="北京",
        use_true_solar_time=True,
    ).calculate(hide=hide)
    text = generate_full_report(result, hide=hide)
    headings = [line for line in text.splitlines() if line.startswith("#")]

    assert text.startswith("⚠️ 免责声明")
    assert not text.splitlines()[0].startswith("#")
    assert headings == [
        "## 赞助支持",
        "# 命理排盘报告：测试样本",
        "## 第一卷：先天命格（静态分析）",
        "## 基本资料（含真太阳时、节气）",
        "### 基本资料",
        "## 八字排盘详情",
        "### 五行分数",
        "### 天干分数",
        "### 温湿度与拱神",
        "### 干支合克与入库",
        "#### 干支相合（依据）",
        "#### 天干相克（依据）",
        "#### 地支入库（依据）",
        "### 地支关系",
        "## 神煞断语",
        "### 简表神煞（字段展开）",
        "## 日主概览",
        "## 五行喜忌（调候与平衡）",
        "### 五行比例",
        "### 五行分数",
        "### 天干分数",
        "## 五行停匀与寒湿燥热（调候依据）",
        "## 干支取象（原文）",
        "## 命造格局（格局用神）",
        "## 节气司令",
        "## 干支关系",
        "## 第二卷：后天运路（动态趋势）",
        "## 运势分析",
        "### 大运分析",
        "### 流年",
        "### 流月运势",
        "### 小运",
        "## 第三卷：民俗与建议（生活应用）",
        "## 袁天罡称骨",
    ]
    for section in ["### 建除十二神", "## 紫微斗数", "## 紫微基础"]:
        assert section not in headings


def test_full_report_other_systems_are_independent_outputs():
    from datetime import datetime

    from bazi_calculator import BaziCalculator
    from report_generator import build_report_hide, generate_full_report

    result = BaziCalculator(
        datetime(1990, 1, 1, 8, 0, 0),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试样本",
        birth_place="北京",
        use_true_solar_time=True,
    ).calculate(hide=build_report_hide("ziwei"))

    ziwei_text = generate_full_report(result, hide=build_report_hide("ziwei"), report_system="ziwei")
    assert "# 紫微斗数报告：测试样本" in ziwei_text
    assert "## 紫微斗数" in ziwei_text
    assert "## 紫微运限四化（大限/流年/流月/流日/流时）" in ziwei_text
    assert "## 八字排盘详情" not in ziwei_text
    assert "## 袁天罡称骨" not in ziwei_text

    with pytest.raises(ValueError, match="未知报告体系"):
        generate_full_report(result, report_system="bone")


def test_name_marriage_candidate_fields_do_not_emit_placeholders():
    from datetime import datetime

    from bazi_calculator import BaziCalculator
    from report_generator import DEFAULT_HIDE

    hide = dict(DEFAULT_HIDE)
    hide["name_marriage"] = False
    result = BaziCalculator(
        datetime(1990, 1, 1, 8, 0, 0),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试命主",
        birth_place="北京市",
        use_true_solar_time=True,
    ).calculate(hide=hide)

    for field in ["marriageCompatibility", "baziMatching", "nameAnalysis", "fiveGrids", "strokeAnalysis"]:
        assert result[field] == {}
