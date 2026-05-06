#!/usr/bin/env python
"""
紫微斗数计算器 (基础版) - 原生Python实现

外部库依赖注入: 无 (原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

from datetime import datetime
from typing import Any

DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
PALACES = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", "迁移", "交友", "官禄", "田宅", "福德", "父母"]


class ZiweiCalculator:
    """紫微斗数计算器 - 原生算法实现"""

    def __init__(self, bazi_result: dict, birth_dt: datetime, gender: str):
        self.bazi_result = bazi_result
        self.birth_dt = birth_dt
        self.gender = gender

    def calculate(self) -> dict[str, Any]:
        """紫微斗数计算"""
        ming_gong = self._calculate_ming_gong()

        return {
            "ziwei": {
                "source": "紫微斗数原生算法",
                "mingGong": ming_gong,
                "twelvePalaces": self._calculate_twelve_palaces(ming_gong["index"]),
                "status": "success",
            }
        }

    def _calculate_ming_gong(self) -> dict:
        """计算命宫"""
        hour = self.birth_dt.hour
        month = self.birth_dt.month

        # 时辰索引 (0-11)
        hour_idx = ((hour + 1) // 2) % 12

        # 命宫地支计算: 寅月起子时在寅，顺数到生时
        ming_idx = (14 - month + hour_idx) % 12

        return {"gong": "命宫", "dizhi": DIZHI[ming_idx], "index": ming_idx}

    def _calculate_twelve_palaces(self, ming_idx: int) -> list:
        """计算十二宫"""
        palaces = []
        for i, name in enumerate(PALACES):
            idx = (ming_idx + i) % 12
            palaces.append({"name": name, "dizhi": DIZHI[idx], "index": idx})
        return palaces
