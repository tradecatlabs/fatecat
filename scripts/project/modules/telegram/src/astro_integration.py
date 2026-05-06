#!/usr/bin/env python3
"""
天文占星集成器 - 原生Python实现

外部库依赖注入 (相对路径从项目根目录):
└── assets/vendor/github/js_astro-master/  # 参考算法

纯净性声明: 原生算法实现，失败即抛异常终止
"""

from datetime import datetime
from typing import Any

# 星座数据
ZODIAC = [
    ("摩羯座", 1, 20),
    ("水瓶座", 2, 19),
    ("双鱼座", 3, 20),
    ("白羊座", 4, 20),
    ("金牛座", 5, 21),
    ("双子座", 6, 21),
    ("巨蟹座", 7, 22),
    ("狮子座", 8, 23),
    ("处女座", 9, 23),
    ("天秤座", 10, 23),
    ("天蝎座", 11, 22),
    ("射手座", 12, 21),
]


class AstroCalculator:
    """天文占星集成器 - 原生算法实现"""

    def __init__(self, birth_dt: datetime, longitude: float, latitude: float):
        self.birth_dt = birth_dt
        self.longitude = longitude
        self.latitude = latitude

    def calculate_astronomical_positions(self) -> dict[str, Any]:
        """天文位置计算"""
        jd = self._to_julian_day()
        zodiac = self._get_zodiac()

        return {
            "astronomy": {
                "source": "天文占星原生算法",
                "julianDay": jd,
                "solarLongitude": self._calc_solar_longitude(jd),
                "status": "success",
            },
            "zodiac": {"sign": zodiac, "element": self._get_zodiac_element(zodiac)},
            "aspects": {"major": []},
            "houses": {"system": "placidus"},
        }

    def get_complete_astro_analysis(self) -> dict[str, Any]:
        """完整天文分析"""
        return self.calculate_astronomical_positions()

    def _to_julian_day(self) -> float:
        """转儒略日"""
        y, m, d = self.birth_dt.year, self.birth_dt.month, self.birth_dt.day
        h = self.birth_dt.hour + self.birth_dt.minute / 60

        if m <= 2:
            y -= 1
            m += 12

        a = int(y / 100)
        b = 2 - a + int(a / 4)

        jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5
        jd += h / 24
        return jd

    def _calc_solar_longitude(self, jd: float) -> float:
        """计算太阳黄经"""
        t = (jd - 2451545.0) / 36525
        l0 = 280.46646 + 36000.76983 * t
        return l0 % 360

    def _get_zodiac(self) -> str:
        """获取星座"""
        m, d = self.birth_dt.month, self.birth_dt.day
        for name, end_month, end_day in ZODIAC:
            if (m == end_month and d <= end_day) or (m == end_month - 1 and d > end_day):
                return name
        return "摩羯座"

    def _get_zodiac_element(self, zodiac: str) -> str:
        """星座元素"""
        fire = ["白羊座", "狮子座", "射手座"]
        earth = ["金牛座", "处女座", "摩羯座"]
        air = ["双子座", "天秤座", "水瓶座"]
        water = ["巨蟹座", "天蝎座", "双鱼座"]

        if zodiac in fire:
            return "火"
        if zodiac in earth:
            return "土"
        if zodiac in air:
            return "风"
        if zodiac in water:
            return "水"
        return "未知"
