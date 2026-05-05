#!/usr/bin/env python3
"""
六爻占卜计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

import random
from datetime import datetime

from utils.timezone import ensure_cn, now_cn

# 八卦
BAGUA = ["坤", "艮", "坎", "巽", "震", "离", "兑", "乾"]
# 六十四卦名
GUA64 = {
    (7, 7): "乾为天",
    (0, 0): "坤为地",
    (4, 2): "水雷屯",
    (2, 4): "山水蒙",
    (2, 7): "水天需",
    (7, 2): "天水讼",
    (0, 2): "地水师",
    (2, 0): "水地比",
}


class LiuYaoCalculator:
    """六爻占卜计算器 - 原生算法实现"""

    def __init__(self, question: str, bazi_result: dict):
        self.question = question
        self.bazi_result = bazi_result
        # 使用当前时间起卦
        ct = bazi_result.get("currentTime")
        self.current_time = ensure_cn(ct) if isinstance(ct, datetime) else now_cn()

    def calculate(self) -> dict:
        """完整六爻计算 - 使用当前时间"""
        yao_list = self._qi_gua()
        ben_gua = self._get_gua_name(yao_list)
        bian_gua = self._get_bian_gua(yao_list)

        return {
            "liuyao": {
                "source": "六爻原生算法",
                "currentTime": self.current_time.strftime("%Y-%m-%d %H:%M"),
                "question": self.question,
                "yaoList": yao_list,
                "benGua": ben_gua,
                "bianGua": bian_gua,
                "dongYao": self._get_dong_yao(yao_list),
                "analysis": self._analyze(yao_list),
                "status": "success",
            }
        }

    def _qi_gua(self) -> list[int]:
        """起卦 - 使用当前时间作为种子"""
        seed = int(self.current_time.timestamp() * 1000)
        random.seed(seed)
        return [random.choice([6, 7, 8, 9]) for _ in range(6)]

    def _get_gua_name(self, yao: list[int]) -> str:
        xia = sum([(1 if y in [7, 9] else 0) << i for i, y in enumerate(yao[:3])])
        shang = sum([(1 if y in [7, 9] else 0) << i for i, y in enumerate(yao[3:])])
        return GUA64.get((shang, xia), f"{BAGUA[shang % 8]}{BAGUA[xia % 8]}")

    def _get_bian_gua(self, yao: list[int]) -> str:
        bian_yao = [7 if y == 6 else 8 if y == 9 else y for y in yao]
        return self._get_gua_name(bian_yao)

    def _get_dong_yao(self, yao: list[int]) -> list[int]:
        return [i + 1 for i, y in enumerate(yao) if y in [6, 9]]

    def _analyze(self, yao: list[int]) -> str:
        dong = self._get_dong_yao(yao)
        if not dong:
            return "静卦，以本卦断"
        if len(dong) == 1:
            return "一爻动，以动爻断"
        return f"{len(dong)}爻动，综合分析"
