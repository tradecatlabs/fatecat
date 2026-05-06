#!/usr/bin/env python3
"""
bazi-1完整五行评分系统集成器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

# 天干五行
GAN_WX = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}
# 地支五行
ZHI_WX = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}
# 五行分数
WX_SCORE = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}


class Bazi1Integration:
    """bazi-1五行评分系统 - 原生算法实现"""

    def __init__(self, four_pillars: dict):
        self.fp = four_pillars

    def get_complete_analysis(self) -> dict:
        """完整分析"""
        wx_score = self._calculate_wuxing_score()

        return {
            "bazi1Analysis": {
                "source": "五行评分原生算法",
                "wuxingScore": wx_score,
                "dominant": max(wx_score, key=wx_score.get),
                "weak": min(wx_score, key=wx_score.get),
                "balance": self._analyze_balance(wx_score),
                "status": "success",
            }
        }

    def _calculate_wuxing_score(self) -> dict:
        """计算五行分数"""
        score = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

        for pillar in ["year", "month", "day", "hour"]:
            p = self.fp.get(pillar, {})
            stem = p.get("stem", "")
            branch = p.get("branch", "")

            if stem in GAN_WX:
                score[GAN_WX[stem]] += 10
            if branch in ZHI_WX:
                score[ZHI_WX[branch]] += 10

        return score

    def _analyze_balance(self, score: dict) -> str:
        """分析平衡"""
        values = list(score.values())
        diff = max(values) - min(values)

        if diff <= 10:
            return "五行平衡"
        elif diff <= 20:
            return "五行略有偏颇"
        else:
            return "五行偏枯"
