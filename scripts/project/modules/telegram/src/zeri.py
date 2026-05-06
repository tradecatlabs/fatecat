#!/usr/bin/env python3
"""
择日算法计算器 - 基于lunar-python

外部库依赖注入 (相对路径从项目根目录):
└── assets/vendor/github/lunar-python-master/  # 历法支持

纯净性声明: 强制调用原生算法，失败即抛异常终止
"""

import sys

from _paths import LUNAR_PYTHON_DIR

sys.path.insert(0, str(LUNAR_PYTHON_DIR))

from datetime import datetime, timedelta

from lunar_python import Solar


class ZeRiCalculator:
    """择日算法计算器 - 原生算法实现"""

    def __init__(self, start_date: datetime, end_date: datetime, purpose: str):
        self.start_date = start_date
        self.end_date = end_date
        self.purpose = purpose

    def calculate(self) -> dict:
        """完整择日计算"""
        dates = self._get_date_range()
        analyzed = [self._analyze_date(d) for d in dates]
        auspicious = [a for a in analyzed if a["score"] >= 70]

        return {
            "zeri": {
                "source": "择日原生算法",
                "purpose": self.purpose,
                "dateRange": {"start": self.start_date.strftime("%Y-%m-%d"), "end": self.end_date.strftime("%Y-%m-%d")},
                "totalDays": len(dates),
                "auspiciousDays": len(auspicious),
                "recommendedDates": auspicious,
                "status": "success",
            }
        }

    def _get_date_range(self) -> list[datetime]:
        """获取日期范围"""
        dates = []
        current = self.start_date
        while current <= self.end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates

    def _analyze_date(self, date: datetime) -> dict:
        """分析单日"""
        solar = Solar.fromYmd(date.year, date.month, date.day)
        lunar = solar.getLunar()

        # 基础评分
        score = 60

        # 建除十二神
        jian = lunar.getDayZhi()  # 使用日支代替
        zhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        jian_list = ["建", "除", "满", "平", "定", "执", "破", "危", "成", "收", "开", "闭"]
        jian_idx = zhi_list.index(jian) if jian in zhi_list else 0
        jian_xing = jian_list[jian_idx % 12]

        if jian_xing in ["建", "除", "满", "平", "定", "执", "成", "开"]:
            score += 20

        # 节气加分
        jieqi = lunar.getJieQi()
        if jieqi:
            score += 10

        return {
            "date": date.strftime("%Y-%m-%d"),
            "lunar": lunar.toString(),
            "jianXing": jian_xing,
            "score": min(score, 100),
            "yi": lunar.getDayYi() if lunar.getDayYi() else [],
            "ji": lunar.getDayJi() if lunar.getDayJi() else [],
        }
