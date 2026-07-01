#!/usr/bin/env python3
"""
梅花易数计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

from datetime import datetime

# 八卦数据
BAGUA = ["坤", "艮", "坎", "巽", "震", "离", "兑", "乾"]
BAGUA_WUXING = {"乾": "金", "兑": "金", "离": "火", "震": "木", "巽": "木", "坎": "水", "艮": "土", "坤": "土"}


class MeiHuaCalculator:
    """梅花易数计算器 - 原生算法实现"""

    def __init__(self, bazi_result: dict, current_time: datetime):
        self.bazi_result = bazi_result
        # 使用传入的当前时间起卦
        self.current_time = current_time

    def calculate(self) -> dict:
        """完整梅花易数计算 - 使用当前时间"""
        shang_gua, xia_gua, dong_yao = self._time_qi_gua()

        ben_gua = {"shang": BAGUA[shang_gua], "xia": BAGUA[xia_gua], "dongYao": dong_yao}
        hu_gua = self._get_hu_gua(shang_gua, xia_gua)
        bian_gua = self._get_bian_gua(shang_gua, xia_gua, dong_yao)

        return {
            "meihua": {
                "source": "梅花易数原生算法",
                "currentTime": self.current_time.strftime("%Y-%m-%d %H:%M"),
                "qiGuaMethod": "时间起卦法",
                "benGua": ben_gua,
                "huGua": hu_gua,
                "bianGua": bian_gua,
                "tiYong": self._analyze_ti_yong(dong_yao),
                "wuXingAnalysis": self._analyze_wu_xing(ben_gua),
                "status": "success",
            }
        }

    def _time_qi_gua(self):
        """时间起卦法 - 使用当前时间"""
        y = self.current_time.year
        m = self.current_time.month
        d = self.current_time.day
        h = self.current_time.hour

        shang = (y + m + d) % 8
        xia = (y + m + d + h) % 8
        dong = (y + m + d + h) % 6

        shang = shang if shang > 0 else 8
        xia = xia if xia > 0 else 8
        dong = dong if dong > 0 else 6

        return shang - 1, xia - 1, dong

    def _get_hu_gua(self, shang: int, xia: int) -> dict:
        return {"shang": BAGUA[(shang + xia) % 8], "xia": BAGUA[(shang * xia) % 8]}

    def _get_bian_gua(self, shang: int, xia: int, dong: int) -> dict:
        if dong <= 3:
            new_xia = (xia + dong) % 8
            return {"shang": BAGUA[shang], "xia": BAGUA[new_xia]}
        else:
            new_shang = (shang + dong) % 8
            return {"shang": BAGUA[new_shang], "xia": BAGUA[xia]}

    def _analyze_ti_yong(self, dong: int) -> dict:
        return {"ti": "下卦" if dong <= 3 else "上卦", "yong": "上卦" if dong <= 3 else "下卦"}

    def _analyze_wu_xing(self, ben_gua: dict) -> dict:
        shang_wx = BAGUA_WUXING.get(ben_gua["shang"], "土")
        xia_wx = BAGUA_WUXING.get(ben_gua["xia"], "土")
        return {"shangGuaWuxing": shang_wx, "xiaGuaWuxing": xia_wx}
