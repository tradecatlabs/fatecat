#!/usr/bin/env python3
"""测试统一品牌配置加载与拼装。"""

import pytest

from fate_core.support import (
    append_branding_text,
    build_branding_text,
    get_branding_payload,
    get_disclaimer_payload,
)


def test_get_branding_payload_contains_required_fields():
    branding = get_branding_payload()

    assert branding["name"] == "TradeCat Labs"
    assert branding["tradecatRepo"] == "https://github.com/tradecatlabs"
    assert branding["fatecatRepo"] == "https://github.com/tradecatlabs/fatecat"
    assert branding["dexScreenerUrl"] == "https://dexscreener.com/bsc/0x8a99b8d53eff6bc331af529af74ad267f3167777"
    assert branding["xUrl"] == "https://x.com/tradecatlabs"
    assert branding["githubUrl"] == "https://github.com/tradecatlabs"
    assert branding["huggingFaceUrl"] == "https://huggingface.co/tradecatlabs"
    assert branding["geminiGemUrl"] == ("https://gemini.google.com/gem/1d9XompAC8xk0xV6655X9IxZYQUNkDJoG?usp=sharing")
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
    assert "TradeCat Labs" in text
    assert "TradeCat Labs GitHub: https://github.com/tradecatlabs" in text
    assert "TradeCat Labs X: https://x.com/tradecatlabs" in text


def test_build_branding_text_puts_disclaimer_before_branding():
    text = build_branding_text(compact=False)

    assert text.startswith("⚠️ 免责声明")
    assert "TradeCat Labs｜FateCat 测算基础设施" in text


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
    assert text.index("## TradeCat Labs 实验室") < text.index("# 命理排盘报告：测试命主")

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


def test_bone_report_uses_concise_gendered_verse_output():
    from report_generator import generate_bone_section

    text = generate_bone_section(
        {
            "boneWeight": {
                "weightQian": 37,
                "weight": 3.7,
                "weightCn": "三两七钱",
                "summary": "财禄厚重白手成家之命",
                "text": "测试女命歌诀",
                "interpretation": {"audience": "女", "genderSpecific": True},
                "components": {
                    "year": {"ganZhi": "丙午", "weight": 1.3, "weightCn": "一两三钱"},
                    "month": {"month": 5, "monthCn": "五", "weight": 0.5, "weightCn": "五钱"},
                    "day": {"day": 17, "dayCn": "十七", "weight": 0.9, "weightCn": "九钱"},
                    "hour": {"zhi": "卯", "weight": 1.0, "weightCn": "一两"},
                },
                "calculation": {"tableVersion": "common-weight-table-v1"},
            }
        }
    )

    assert "女命歌诀：测试女命歌诀" in text
    assert "* 评语：财禄厚重白手成家之命" in text
    assert "* 称骨：三两七钱" in text
    assert "数值：3.7两" not in text
    assert "中文：" not in text
    assert "年柱 丙午：一两三钱" in text
    assert "月份 五月：五钱" in text
    assert "出生日 十七日：九钱" in text
    assert "时辰 卯时：一两" in text
    assert "男女共用" not in text
    assert "现代流传版本，非事实判断" not in text
    assert "版本边界" not in text
    assert "用途边界" not in text


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
        "## TradeCat Labs 实验室",
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
    assert "analysisEvidence" not in text
    assert "简表神煞" not in text
    assert "简表神煞释义" not in text
    assert text.count("**神煞释义**") == 1
    for name, description in result["spiritsFull"]["descriptions"].items():
        assert text.count(f"- {name}：{description}") == 1
    assert "男命歌诀：" in text
    assert "* 评语：" in text
    assert "男女共用" not in text
    assert "现代流传版本，非事实判断" not in text
    assert "版本边界" not in text
    assert "用途边界" not in text


def test_comprehensive_bazi_result_contains_hidden_analysis_evidence():
    from datetime import datetime

    from bazi_calculator import BaziCalculator
    from report_generator import build_report_hide

    result = BaziCalculator(
        datetime(1990, 1, 1, 8, 0, 0),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试样本",
        birth_place="北京",
        use_true_solar_time=True,
    ).calculate(hide=build_report_hide("bazi"))

    evidence = result["analysisEvidence"]
    assert evidence["schemaVersion"] == 1
    assert evidence["profile"] == "comprehensive_bazi"
    assert evidence["visibilityDefault"] == "hidden"
    assert evidence["items"]["dayMaster"]["weight"] == "core"
    assert "bazi.month_command_priority" in evidence["items"]["dayMaster"]["ruleIds"]
    assert evidence["items"]["wuxingPreference"]["weight"] == "core"
    assert evidence["items"]["pattern"]["weight"] == "core"
    assert evidence["items"]["ganzhiRelations"]["weight"] == "core"
    assert evidence["items"]["spirits"]["weight"] == "auxiliary"
    assert evidence["items"]["boneWeight"]["weight"] == "folk"


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
    assert "### 入盘依据" in ziwei_text
    assert "### 命宫与身宫" in ziwei_text
    assert "## 紫微结构解读（依据版）" in ziwei_text
    assert "### 主星组合" in ziwei_text
    assert "### 三方四正" in ziwei_text
    assert "### 四化落宫" in ziwei_text
    assert "### 大限/流年联动" in ziwei_text
    assert "## 紫微运限四化（大限/流年/流月/流日/流时）" in ziwei_text
    assert "## 紫微基础" not in ziwei_text
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
