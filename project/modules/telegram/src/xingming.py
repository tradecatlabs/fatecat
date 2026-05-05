#!/usr/bin/env python3
"""
姓名学计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生算法)
纯净性声明: 原生算法实现，失败即抛异常终止
"""

import random

# 常用字笔画 (康熙字典)
STROKES = {
    "张": 11,
    "王": 4,
    "李": 7,
    "赵": 14,
    "刘": 15,
    "陈": 16,
    "杨": 13,
    "黄": 12,
    "周": 8,
    "吴": 7,
    "郑": 19,
    "孙": 10,
    "马": 10,
    "朱": 6,
    "胡": 11,
    "林": 8,
    "三": 3,
    "一": 1,
    "二": 2,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "明": 8,
    "华": 14,
    "国": 11,
    "建": 9,
    "文": 4,
    "伟": 11,
    "强": 11,
    "军": 9,
}

# 五格吉凶
WUGE_JIXI = {
    1: "吉",
    3: "吉",
    5: "吉",
    6: "吉",
    7: "吉",
    8: "吉",
    11: "吉",
    13: "吉",
    15: "吉",
    16: "吉",
    17: "吉",
    18: "吉",
    21: "吉",
    23: "吉",
    24: "吉",
    2: "凶",
    4: "凶",
    9: "凶",
    10: "凶",
    12: "凶",
    14: "凶",
    19: "凶",
    20: "凶",
}


class XingMingCalculator:
    """姓名学计算器 - 原生算法实现"""

    def __init__(self, name: str, bazi_result: dict):
        self.name = name
        self.bazi_result = bazi_result

    def calculate(self) -> dict:
        """完整姓名学计算"""
        strokes = self._get_strokes()
        wuge = self._calculate_wuge(strokes)
        sancai = self._calculate_sancai(wuge)

        return {
            "xingming": {
                "source": "姓名学原生算法",
                "name": self.name,
                "strokes": strokes,
                "wuGe": wuge,
                "sanCai": sancai,
                "score": self._calculate_score(wuge),
                "status": "success",
            }
        }

    def _get_strokes(self) -> list:
        """获取笔画"""
        return [STROKES.get(c, len(c.encode("gbk")) // 2 + 5) for c in self.name]

    def _calculate_wuge(self, strokes: list) -> dict:
        """计算五格"""
        if len(strokes) < 2:
            strokes = strokes + [1]

        xing = strokes[0]
        ming = sum(strokes[1:]) if len(strokes) > 1 else 1

        tiange = xing + 1
        renge = xing + (strokes[1] if len(strokes) > 1 else 1)
        dige = ming + 1 if len(strokes) == 2 else sum(strokes[1:])
        waige = tiange + dige - renge
        zongge = sum(strokes)

        return {
            "天格": {"num": tiange, "jixi": WUGE_JIXI.get(tiange % 25, "中")},
            "人格": {"num": renge, "jixi": WUGE_JIXI.get(renge % 25, "中")},
            "地格": {"num": dige, "jixi": WUGE_JIXI.get(dige % 25, "中")},
            "外格": {"num": waige, "jixi": WUGE_JIXI.get(waige % 25, "中")},
            "总格": {"num": zongge, "jixi": WUGE_JIXI.get(zongge % 25, "中")},
        }

    def _calculate_sancai(self, wuge: dict) -> dict:
        """计算三才"""
        tian = (wuge["天格"]["num"] - 1) % 10
        ren = (wuge["人格"]["num"] - 1) % 10
        di = (wuge["地格"]["num"] - 1) % 10

        wx = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
        return {"tianCai": wx[tian], "renCai": wx[ren], "diCai": wx[di], "config": f"{wx[tian]}{wx[ren]}{wx[di]}"}

    def _calculate_score(self, wuge: dict) -> int:
        """计算总分"""
        score = 60
        for v in wuge.values():
            if v["jixi"] == "吉":
                score += 8
            elif v["jixi"] == "凶":
                score -= 5
        return min(max(score, 0), 100)


# ==================== 对外辅助函数（测试/演示用） ====================
def _char_element(strokes: int) -> str:
    """用简单规则推断五行：画数 mod 5"""
    m = strokes % 5
    return ["水", "木", "火", "土", "金"][m]


def calc_wuge(xing: str, ming: str) -> dict:
    """
    计算五格剖象法（简化版）
    返回：分数、级别、姓/名五行、五格详情
    """
    name = xing + ming
    calc = XingMingCalculator(name, {})
    strokes = calc._get_strokes()
    wuge = calc._calculate_wuge(strokes)

    # 评分与级别
    score = calc._calculate_score(wuge)
    level = "优" if score >= 85 else "良" if score >= 70 else "中" if score >= 60 else "待提升"

    xing_elements = [_char_element(calc._get_strokes()[0])]
    ming_elements = [_char_element(s) for s in calc._get_strokes()[1:]]

    # 转换五格字段名
    mapped = {}
    for k, v in wuge.items():
        mapped[k] = {
            "shu": v["num"],
            "jixiong": v["jixi"],
        }

    return {
        "name": name,
        "score": score,
        "level": level,
        "xingElements": xing_elements,
        "mingElements": ming_elements,
        "wuge": mapped,
    }


def suggest_names(xing: str, target_score: int = 80, target_elements=None, limit: int = 10):
    """
    简单姓名推荐：随机生成两字名，筛选得分>=target_score 且包含期望五行
    仅供演示/测试，无外部依赖。
    """
    if target_elements is None:
        target_elements = []
    chars_pool = list(STROKES.keys())
    suggestions = []
    attempts = 0
    while len(suggestions) < limit and attempts < 200:
        attempts += 1
        ming = "".join(random.sample(chars_pool, 2))
        res = calc_wuge(xing, ming)
        if res["score"] < target_score:
            continue
        if target_elements:
            merged = set(res["xingElements"] + res["mingElements"])
            if not set(target_elements).issubset(merged):
                continue
        suggestions.append(
            {
                "name": xing + ming,
                "score": res["score"],
                "chars": list(ming),
            }
        )
    return suggestions


def analyze_name_elements(name: str) -> dict:
    """
    分析姓名的五行分布（基于笔画模5规则）
    返回：每字笔画/五行，主导五行，计数。
    """
    chars_info = []
    count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for c in name:
        strokes = STROKES.get(c, len(c.encode("gbk")) // 2 + 5)
        elem = _char_element(strokes)
        count[elem] += 1
        chars_info.append(
            {
                "char": c,
                "strokes": strokes,
                "element": elem,
            }
        )
    dominant = max(count.items(), key=lambda x: x[1])[0] if chars_info else ""
    return {
        "name": name,
        "dominantElement": dominant,
        "chars": chars_info,
        "elementCount": count,
    }
