#!/usr/bin/env python3
"""
输出格式化工具 - 支持JSON/JSONL多种格式

功能: 将66个字段按功能分类输出
"""

import json
from typing import Any

# 字段分类定义
FIELD_CATEGORIES = {
    "input": {"name": "用户传参", "desc": "出生时间性别经度", "fields": ["input"]},
    "core_bazi": {
        "name": "核心八字",
        "desc": "四柱干支基础数据",
        "fields": ["fourPillars", "hiddenStems", "tenGods", "twelveGrowth", "dayMaster"],
    },
    "wuxing": {"name": "五行分析", "desc": "五行统计与状态", "fields": ["fiveElements", "wuxingState"]},
    "spirits": {"name": "神煞系统", "desc": "吉神凶煞", "fields": ["spirits"]},
    "palaces": {"name": "宫位系统", "desc": "特殊宫位与空亡", "fields": ["specialPalaces", "voidInfo"]},
    "relations": {"name": "干支关系", "desc": "合冲刑害", "fields": ["ganzhiRelations"]},
    "fortune": {
        "name": "运势流年",
        "desc": "大运流年流月",
        "fields": ["majorFortune", "annualFortune", "monthlyFortune", "xiaoYun", "jiaoYun"],
    },
    "pattern": {"name": "格局用神", "desc": "格局判断与用神", "fields": ["geju", "yongShen"]},
    "birth_info": {"name": "出生信息", "desc": "公历农历生肖星座", "fields": ["birthInfo", "trueSolarTime"]},
    "jieqi": {"name": "节气司令", "desc": "节气与人元司令", "fields": ["jieqiDetail", "siling"]},
    "traditional": {"name": "传统命理", "desc": "称骨命卦黄历", "fields": ["boneWeight", "mingGua", "huangLi"]},
    "ziwei": {
        "name": "紫微斗数",
        "desc": "紫微排盘",
        "fields": ["ziweiChart", "starPositions", "palaceAnalysis", "starInfluence", "ziweiBasic"],
    },
    "divination_liuyao": {"name": "六爻占卜", "desc": "六爻起卦(当前时间)", "fields": ["liuyaoHexagram"]},
    "divination_meihua": {
        "name": "梅花易数",
        "desc": "梅花起卦(当前时间)",
        "fields": ["meihuaYishu", "numberDivination"],
    },
    "divination_qimen": {"name": "奇门遁甲", "desc": "奇门排盘(当前时间)", "fields": ["qimenDunjia", "mysticalGates"]},
    "divination_liuren": {"name": "大六壬", "desc": "六壬排盘", "fields": ["liurenDivination"]},
    "divination_yijing": {
        "name": "易经系统",
        "desc": "易经起卦(当前时间)",
        "fields": ["hexagrams", "yijingAnalysis", "divination"],
    },
    "zeri": {"name": "择日系统", "desc": "择日选吉(从当前日期)", "fields": ["dateSelection", "auspiciousDates"]},
    "fengshui": {
        "name": "风水罗盘",
        "desc": "方位九星八卦",
        "fields": ["fengshuiCompass", "directionAnalysis", "nineStars", "bagua"],
    },
    "astro": {
        "name": "天文占星",
        "desc": "行星星座",
        "fields": ["planetPositions", "zodiacSigns", "aspects", "houses"],
    },
    "calendar": {
        "name": "历法系统",
        "desc": "多历法节假日",
        "fields": ["sxwnlCalendar", "highPrecisionTime", "astronomicalData", "multiCalendar", "holidays", "festivals"],
    },
    "name_marriage": {
        "name": "姓名合婚",
        "desc": "需额外输入",
        "fields": ["marriageCompatibility", "baziMatching", "nameAnalysis", "fiveGrids", "strokeAnalysis"],
    },
    "modern": {"name": "现代化接口", "desc": "API兼容", "fields": ["modernBazi", "typeScriptModel", "apiInterface"]},
    "system": {"name": "系统优化", "desc": "性能缓存", "fields": ["performance", "caching", "optimization"]},
}

# 排除的分类（不输出）
EXCLUDED_CATEGORIES = {"name_marriage", "modern", "system"}


def to_jsonl(result: dict[str, Any]) -> str:
    """转换为JSONL格式 - 每个分类一行"""
    lines = []
    for cat_id, cat_info in FIELD_CATEGORIES.items():
        if cat_id in EXCLUDED_CATEGORIES:
            continue
        cat_data = {
            "category": cat_id,
            "name": cat_info["name"],
            "desc": cat_info["desc"],
            "data": {f: result[f] for f in cat_info["fields"] if f in result},
        }
        lines.append(json.dumps(cat_data, ensure_ascii=False, default=str))
    return "\n".join(lines)


def to_json(result: dict[str, Any]) -> str:
    """转换为分类JSON格式"""
    output = {}
    for cat_id, cat_info in FIELD_CATEGORIES.items():
        if cat_id in EXCLUDED_CATEGORIES:
            continue
        output[cat_id] = {
            "name": cat_info["name"],
            "desc": cat_info["desc"],
            "data": {f: result[f] for f in cat_info["fields"] if f in result},
        }
    return json.dumps(output, ensure_ascii=False, indent=2, default=str)


def get_category(result: dict[str, Any], category: str) -> dict:
    """获取单个分类数据"""
    if category not in FIELD_CATEGORIES:
        raise ValueError(f"未知分类: {category}")
    cat_info = FIELD_CATEGORIES[category]
    return {
        "category": category,
        "name": cat_info["name"],
        "data": {f: result[f] for f in cat_info["fields"] if f in result},
    }


def save_both(result: dict[str, Any], base_path: str) -> tuple:
    """同时保存JSON和JSONL两种格式"""
    json_path = f"{base_path}.json"
    jsonl_path = f"{base_path}.jsonl"

    # 保存JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    # 保存JSONL
    with open(jsonl_path, "w", encoding="utf-8") as f:
        f.write(to_jsonl(result))

    return json_path, jsonl_path


def list_categories() -> dict:
    """列出所有分类"""
    return {k: {"name": v["name"], "desc": v["desc"], "fields": v["fields"]} for k, v in FIELD_CATEGORIES.items()}
