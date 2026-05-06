#!/usr/bin/env python3
"""
完整真太阳时计算器 - 基于paipan-master天文算法

外部库依赖注入 (相对路径从项目根目录):
└── assets/vendor/github/paipan-master/
    └── 真太阳时计算、均时差算法、早晚子时判断

算法来源: 天文学均时差公式 (Equation of Time)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

import math
from datetime import timedelta


class TrueSolarTimeCalculator:
    """完整真太阳时计算 - 基于paipan-master天文算法"""

    def __init__(self, dt, longitude):
        self.dt = dt
        self.longitude = longitude

    def calculate_true_solar_time(self):
        """计算真太阳时 - 完整天文算法"""
        # 基础时差计算
        basic_offset = (self.longitude - 120) * 4  # 分钟

        # 计算均时差（时间方程）
        equation_of_time = self._calculate_equation_of_time()

        # 真太阳时 = 地方时 + 经度时差 + 均时差
        total_offset_minutes = basic_offset + equation_of_time

        true_solar_time = self.dt + timedelta(minutes=total_offset_minutes)

        return {
            "originalTime": self.dt,
            "trueSolarTime": true_solar_time,
            "longitudeOffset": basic_offset,
            "equationOfTime": equation_of_time,
            "totalOffset": total_offset_minutes,
            "description": f"经度修正{basic_offset:.1f}分钟，均时差{equation_of_time:.1f}分钟",
        }

    def _calculate_equation_of_time(self):
        """计算均时差（时间方程）"""
        # 计算儒略日
        jd = self._julian_day()

        # 计算太阳平黄经
        n = jd - 2451545.0
        L = (280.460 + 0.9856474 * n) % 360

        # 计算太阳真黄经
        g = math.radians((357.528 + 0.9856003 * n) % 360)
        lambda_sun = L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)

        # 计算均时差
        alpha = math.radians(lambda_sun)
        delta = math.radians(23.439 - 0.0000004 * n)

        E = 4 * (L - 0.0057183 - math.degrees(math.atan2(math.tan(alpha) * math.cos(delta), 1.0)))

        return E % 360 if E > 180 else E

    def _julian_day(self):
        """计算儒略日"""
        year = self.dt.year
        month = self.dt.month
        day = self.dt.day + self.dt.hour / 24.0 + self.dt.minute / 1440.0 + self.dt.second / 86400.0

        if month <= 2:
            year -= 1
            month += 12

        a = year // 100
        b = 2 - a + a // 4

        jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5

        return jd

    def calculate_early_late_zi_time(self):
        """计算早晚子时判定"""
        hour = self.dt.hour

        # 23:00-24:00 为早子时（属次日）
        # 00:00-01:00 为晚子时（属当日）
        if hour == 23:
            return {"ziType": "早子时", "belongsToNextDay": True, "description": "23:00-24:00属次日子时"}
        elif hour == 0:
            return {"ziType": "晚子时", "belongsToNextDay": False, "description": "00:00-01:00属当日子时"}
        else:
            return {"ziType": "非子时", "belongsToNextDay": False, "description": "不在子时范围"}
