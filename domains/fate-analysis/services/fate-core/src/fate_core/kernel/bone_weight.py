"""称骨民俗权重计算。

权重一律以整数“钱”为计算单位。称骨只作为综合八字报告的民俗附录，
不参与旺衰、格局、调候、喜忌或运势判断。
"""

from __future__ import annotations

from typing import Any, Literal

from fate_core.kernel.bone_weight_verses import BONE_GENDERED_VERSE_QIAN

LeapMonthPolicy = Literal["split_at_15", "same_month"]

DEFAULT_LEAP_MONTH_POLICY: LeapMonthPolicy = "split_at_15"
WEIGHT_TABLE_VERSION = "common-weight-table-v1"
INTERPRETATION_VERSION = "common-summary-v1"
GENDERED_INTERPRETATION_VERSION = "chxb-chenggu-gendered-full-v1"
GENDERED_INTERPRETATION_SOURCE = {
    "repository": "https://github.com/chxb/chenggu",
    "revision": "0f86a690499bfe828aa534fea17f241c85f038f1",
    "contentSha256": "38c01b3c93e337d4126b1ccc4bd777ec19bcdbddedac3612ddba23d7434b7da2",
    "rangeEvidenceUrl": "https://www.suanzhun.net/chengu/1750.html",
    "rangeEvidenceSha256": "7aa9941b36b1fb886abfc003e0c9102498e0d93c2cf14953c8d8c2917fd70cf4",
    "maleRangeQian": [21, 72],
    "femaleRangeQian": [21, 71],
    "license": "MIT",
    "historicalAuthority": False,
}

_CN_DIGITS = "零一二三四五六七八九"

BONE_YEAR_QIAN = {
    "甲子": 12,
    "乙丑": 9,
    "丙寅": 6,
    "丁卯": 7,
    "戊辰": 12,
    "己巳": 5,
    "庚午": 9,
    "辛未": 8,
    "壬申": 7,
    "癸酉": 8,
    "甲戌": 15,
    "乙亥": 9,
    "丙子": 16,
    "丁丑": 8,
    "戊寅": 8,
    "己卯": 19,
    "庚辰": 12,
    "辛巳": 6,
    "壬午": 8,
    "癸未": 7,
    "甲申": 5,
    "乙酉": 15,
    "丙戌": 6,
    "丁亥": 16,
    "戊子": 15,
    "己丑": 7,
    "庚寅": 9,
    "辛卯": 12,
    "壬辰": 10,
    "癸巳": 7,
    "甲午": 15,
    "乙未": 6,
    "丙申": 5,
    "丁酉": 14,
    "戊戌": 14,
    "己亥": 9,
    "庚子": 7,
    "辛丑": 7,
    "壬寅": 9,
    "癸卯": 12,
    "甲辰": 8,
    "乙巳": 7,
    "丙午": 13,
    "丁未": 5,
    "戊申": 14,
    "己酉": 5,
    "庚戌": 9,
    "辛亥": 17,
    "壬子": 5,
    "癸丑": 7,
    "甲寅": 12,
    "乙卯": 8,
    "丙辰": 8,
    "丁巳": 6,
    "戊午": 19,
    "己未": 6,
    "庚申": 8,
    "辛酉": 16,
    "壬戌": 10,
    "癸亥": 7,
}
BONE_MONTH_QIAN = {
    1: 6,
    2: 7,
    3: 18,
    4: 9,
    5: 5,
    6: 16,
    7: 9,
    8: 15,
    9: 18,
    10: 8,
    11: 9,
    12: 5,
}
BONE_DAY_QIAN = {
    1: 5,
    2: 10,
    3: 8,
    4: 15,
    5: 16,
    6: 15,
    7: 8,
    8: 16,
    9: 8,
    10: 16,
    11: 9,
    12: 17,
    13: 8,
    14: 17,
    15: 10,
    16: 8,
    17: 9,
    18: 18,
    19: 5,
    20: 15,
    21: 10,
    22: 9,
    23: 8,
    24: 9,
    25: 15,
    26: 18,
    27: 7,
    28: 8,
    29: 16,
    30: 6,
}
BONE_HOUR_QIAN = {
    "子": 16,
    "丑": 6,
    "寅": 7,
    "卯": 10,
    "辰": 9,
    "巳": 16,
    "午": 10,
    "未": 8,
    "申": 8,
    "酉": 9,
    "戌": 6,
    "亥": 6,
}
BONE_TEXT_QIAN = {
    21: "终身行乞孤苦之命",
    22: "一生劳碌之命",
    23: "终身困苦之命",
    24: "一生薄福之命",
    25: "六亲无靠自立更生之命",
    26: "平生衣禄苦中求之命",
    27: "一生衣禄不周之命",
    28: "一生行事似飘蓬之命",
    29: "初年运限未曾亨之命",
    30: "劳劳碌碌苦中求之命",
    31: "先苦后甘之命",
    32: "性巧过人衣食到贵之命",
    33: "早年作事事难成之命",
    34: "财谷有余主得内助之命",
    35: "生平福量不周全之命",
    36: "超群拔类衣禄厚重之命",
    37: "聪明富贵之命",
    38: "财帛丰厚宜称之命",
    39: "少年命运不通之命",
    40: "富贵近益生匪浅之命",
    41: "税户近贵门庭光彩之命",
    42: "兵权有职富贵才能之命",
    43: "财禄厚重白手成家之命",
    44: "初年无财中年有财之命",
    45: "福禄丰厚极富且贵之命",
    46: "富贵有余福寿双全之命",
    47: "高官禄厚学业饱满之命",
    48: "官员财禄厚重之命",
    49: "性巧精神仓库财禄之命",
    50: "文武才能钱谷丰盛之命",
    51: "官职财禄荣华富贵之命",
    52: "掌握兵权富贵长命",
    53: "僧道门中近贵之命",
    54: "大富大贵之命",
    55: "官职财禄丰厚之命",
    56: "官职长享荣华富贵之命",
    57: "官职财禄皆有之命",
    58: "官禄旺相才能性直富贵之命",
    59: "官品极品之命",
    60: "官职王侯之命",
    61: "名利双收之命",
    62: "权贵之命",
    63: "受职高官之命",
    64: "权贵显达之命",
    65: "细推此命福不轻之命",
    66: "大富大贵之命",
    67: "一世荣华富贵之命",
    68: "富贵双全之命",
    69: "受职于天之命",
    70: "荣华富贵之命",
    71: "此命生成大不同之命",
}


def _validate_inputs(year_gz: str, lunar_month: int, lunar_day: int, hour_zhi: str) -> None:
    if not isinstance(year_gz, str) or year_gz not in BONE_YEAR_QIAN:
        raise ValueError(f"未知年柱：{year_gz}")
    if isinstance(lunar_month, bool) or not isinstance(lunar_month, int):
        raise ValueError("农历月份必须是 1 至 12；负数表示闰月")
    if lunar_month == 0 or abs(lunar_month) not in BONE_MONTH_QIAN:
        raise ValueError(f"无效农历月份：{lunar_month}")
    if isinstance(lunar_day, bool) or not isinstance(lunar_day, int) or lunar_day not in BONE_DAY_QIAN:
        raise ValueError(f"无效农历日期：{lunar_day}")
    if not isinstance(hour_zhi, str) or hour_zhi not in BONE_HOUR_QIAN:
        raise ValueError(f"未知时支：{hour_zhi}")


def _resolve_lunar_month(
    lunar_month: int,
    lunar_day: int,
    policy: LeapMonthPolicy,
) -> tuple[int, bool]:
    if policy not in ("split_at_15", "same_month"):
        raise ValueError(f"不支持的闰月折算策略：{policy}")

    source_month = abs(lunar_month)
    is_leap_month = lunar_month < 0
    if not is_leap_month or policy == "same_month" or lunar_day <= 15:
        return source_month, is_leap_month
    return (source_month % 12) + 1, is_leap_month


def _normalize_gender(gender: str | None) -> tuple[str | None, str]:
    if gender is None:
        return None, "通用"
    if gender not in ("male", "female"):
        raise ValueError(f"不支持的性别值：{gender}")
    return gender, "男" if gender == "male" else "女"


def _format_integer_cn(value: int) -> str:
    if not 0 <= value < 100:
        raise ValueError(f"中文数字格式化只支持 0 至 99：{value}")
    if value < 10:
        return _CN_DIGITS[value]
    tens, ones = divmod(value, 10)
    prefix = "" if tens == 1 else _CN_DIGITS[tens]
    suffix = "" if ones == 0 else _CN_DIGITS[ones]
    return f"{prefix}十{suffix}"


def _format_qian_cn(weight_qian: int) -> str:
    liang, qian = divmod(weight_qian, 10)
    liang_text = f"{_format_integer_cn(liang)}两" if liang else ""
    qian_text = f"{_format_integer_cn(qian)}钱" if qian else ""
    return f"{liang_text}{qian_text}"


def calc_bone_weight(
    year_gz: str,
    lunar_month: int,
    lunar_day: int,
    hour_zhi: str,
    *,
    gender: str | None = None,
    leap_month_policy: LeapMonthPolicy = DEFAULT_LEAP_MONTH_POLICY,
) -> dict[str, Any]:
    """计算称骨权重和构成明细。

    年月日时按固定版本权重表求和，性别用于选择独立的男命或女命歌诀。
    ``lunar-python`` 使用负数月份表示闰月，本函数保留该语义并显式记录折算策略。
    """
    _validate_inputs(year_gz, lunar_month, lunar_day, hour_zhi)
    gender_code, audience = _normalize_gender(gender)
    effective_month, is_leap_month = _resolve_lunar_month(
        lunar_month,
        lunar_day,
        leap_month_policy,
    )

    year_qian = BONE_YEAR_QIAN[year_gz]
    month_qian = BONE_MONTH_QIAN[effective_month]
    day_qian = BONE_DAY_QIAN[lunar_day]
    hour_qian = BONE_HOUR_QIAN[hour_zhi]
    total_qian = year_qian + month_qian + day_qian + hour_qian
    gendered_verse = BONE_GENDERED_VERSE_QIAN.get(gender_code or "", {}).get(total_qian)
    interpretation_version = GENDERED_INTERPRETATION_VERSION if gendered_verse is not None else INTERPRETATION_VERSION

    return {
        "weightQian": total_qian,
        "weight": total_qian / 10,
        "weightCn": _format_qian_cn(total_qian),
        "summary": BONE_TEXT_QIAN[total_qian],
        "text": gendered_verse or BONE_TEXT_QIAN[total_qian],
        "components": {
            "year": {
                "ganZhi": year_gz,
                "weightQian": year_qian,
                "weight": year_qian / 10,
                "weightCn": _format_qian_cn(year_qian),
            },
            "month": {
                "month": effective_month,
                "monthCn": _format_integer_cn(effective_month),
                "sourceMonth": abs(lunar_month),
                "sourceMonthCn": _format_integer_cn(abs(lunar_month)),
                "effectiveMonth": effective_month,
                "effectiveMonthCn": _format_integer_cn(effective_month),
                "isLeapMonth": is_leap_month,
                "leapMonthPolicy": leap_month_policy,
                "weightQian": month_qian,
                "weight": month_qian / 10,
                "weightCn": _format_qian_cn(month_qian),
            },
            "day": {
                "day": lunar_day,
                "dayCn": _format_integer_cn(lunar_day),
                "weightQian": day_qian,
                "weight": day_qian / 10,
                "weightCn": _format_qian_cn(day_qian),
            },
            "hour": {
                "zhi": hour_zhi,
                "weightQian": hour_qian,
                "weight": hour_qian / 10,
                "weightCn": _format_qian_cn(hour_qian),
            },
        },
        "interpretation": {
            "audience": audience,
            "genderSpecific": gendered_verse is not None,
            "version": interpretation_version,
            "coverage": (
                f"gendered-{gender_code}-21-{'72' if gender_code == 'male' else '71'}"
                if gendered_verse is not None
                else "generic-summary"
            ),
            "source": GENDERED_INTERPRETATION_SOURCE if gendered_verse is not None else None,
            "sourceRevision": (GENDERED_INTERPRETATION_SOURCE["revision"] if gendered_verse is not None else ""),
        },
        "calculation": {
            "tableVersion": WEIGHT_TABLE_VERSION,
            "unit": "qian",
            "maxReachableQian": 71,
            "nonExecutableWeightsQian": [72],
            "historicalAttributionVerified": False,
            "scope": "folk-appendix-only",
        },
    }


__all__ = [
    "BONE_DAY_QIAN",
    "BONE_GENDERED_VERSE_QIAN",
    "BONE_HOUR_QIAN",
    "BONE_MONTH_QIAN",
    "BONE_TEXT_QIAN",
    "BONE_YEAR_QIAN",
    "DEFAULT_LEAP_MONTH_POLICY",
    "GENDERED_INTERPRETATION_SOURCE",
    "GENDERED_INTERPRETATION_VERSION",
    "INTERPRETATION_VERSION",
    "LeapMonthPolicy",
    "WEIGHT_TABLE_VERSION",
    "calc_bone_weight",
]
