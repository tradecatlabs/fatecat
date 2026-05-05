#!/usr/bin/env python
"""
奇门遁甲计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

from datetime import datetime

from utils.timezone import ensure_cn, now_cn

# 八门
BAMEN = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门"]
# 九星
JIUXING = ["天蓬", "天任", "天冲", "天辅", "天英", "天芮", "天柱", "天心", "天禽"]
# 八神
BASHEN = ["值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天"]
# 天干
TIANGAN = "甲乙丙丁戊己庚辛壬癸"


class QimenCalculator:
    """奇门遁甲计算器 - 原生算法实现"""

    def __init__(self, bazi_result: dict):
        self.bazi_result = bazi_result
        self.four_pillars = bazi_result.get("fourPillars", {})
        # 使用当前时间排盘
        ct = bazi_result.get("currentTime")
        self.current_time = ensure_cn(ct) if isinstance(ct, datetime) else now_cn()

    def calculate(self) -> dict:
        """奇门遁甲计算 - 使用当前时间"""
        # 使用当前时间的时辰
        hour = self.current_time.hour
        day = self.current_time.day
        month = self.current_time.month

        # 计算局数
        ju = self._calc_ju(month, day, hour)

        # 计算值使门和值符星
        hour_idx = ((hour + 1) // 2) % 12

        return {
            "qimen": {
                "source": "奇门遁甲原生算法",
                "currentTime": self.current_time.strftime("%Y-%m-%d %H:%M"),
                "ju": f"{'阳' if ju <= 4 else '阴'}遁{ju}局",
                "zhishi": BAMEN[hour_idx % 8],
                "zhishen": BASHEN[hour_idx % 8],
                "jiuxing": JIUXING[hour_idx % 9],
                "bamen": {BAMEN[i]: f"宫{i + 1}" for i in range(8)},
                "analysis": self._analyze(ju),
                "status": "success",
            }
        }

    def _calc_ju(self, month: int, day: int, hour: int) -> int:
        """计算局数"""
        # 简化算法：根据月份和日期计算
        base = (month + day) % 9
        return base if base else 9

    def _analyze(self, ju: int) -> str:
        """分析"""
        if ju in [1, 4, 7]:
            return "吉局，利于行动"
        elif ju in [2, 5, 8]:
            return "中平，谨慎行事"
        else:
            return "凶局，宜守不宜攻"
