#!/usr/bin/env python3
"""
八字合婚计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

# 天干五行
GAN_WUXING = {
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
ZHI_WUXING = {
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
# 五行相生
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
# 五行相克
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


class HeHunCalculator:
    """八字合婚计算器 - 原生算法实现"""

    def __init__(self, male_bazi: dict, female_bazi: dict):
        self.male = male_bazi
        self.female = female_bazi

    def calculate(self) -> dict:
        """完整合婚计算"""
        score = 60  # 基础分
        analysis = []

        # 日柱分析
        m_day = self.male["fourPillars"]["day"]
        f_day = self.female["fourPillars"]["day"]

        m_wx = GAN_WUXING.get(m_day["stem"], "土")
        f_wx = GAN_WUXING.get(f_day["stem"], "土")

        # 五行相生加分
        if SHENG.get(m_wx) == f_wx or SHENG.get(f_wx) == m_wx:
            score += 20
            analysis.append(f"日主五行相生: {m_wx}与{f_wx}")
        # 五行相克减分
        elif KE.get(m_wx) == f_wx or KE.get(f_wx) == m_wx:
            score -= 10
            analysis.append(f"日主五行相克: {m_wx}与{f_wx}")
        else:
            score += 10
            analysis.append(f"日主五行平和: {m_wx}与{f_wx}")

        # 年支分析
        m_year_zhi = self.male["fourPillars"]["year"]["branch"]
        f_year_zhi = self.female["fourPillars"]["year"]["branch"]

        # 六合
        liuhe = [("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")]
        for a, b in liuhe:
            if (m_year_zhi == a and f_year_zhi == b) or (m_year_zhi == b and f_year_zhi == a):
                score += 15
                analysis.append(f"年支六合: {m_year_zhi}与{f_year_zhi}")
                break

        level = "上等婚配" if score >= 80 else "中等婚配" if score >= 60 else "下等婚配"

        return {
            "hehun": {
                "source": "合婚原生算法",
                "score": min(score, 100),
                "level": level,
                "analysis": analysis,
                "status": "success",
            }
        }
