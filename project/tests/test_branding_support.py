#!/usr/bin/env python3
"""测试统一品牌配置加载与拼装。"""

import sys
from pathlib import Path

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
    assert "## 袁天罡称骨" in text

    removed_sections = [
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
