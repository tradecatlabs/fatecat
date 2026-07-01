#!/usr/bin/env python3
"""塔罗抽牌：加权、无重复、可复现 JSON。"""

import argparse, hashlib, json, os, random, time
from datetime import datetime

MAJORS = (
    "愚者 魔术师 女祭司 女皇 皇帝 教皇 恋人 战车 力量 隐士 命运之轮 正义 "
    "倒吊人 死神 节制 恶魔 高塔 星星 月亮 太阳 审判 世界"
).split()
SUITS = {"权杖": "火", "圣杯": "水", "宝剑": "风", "星币": "土"}
RANKS = "Ace 二 三 四 五 六 七 八 九 十 侍从 骑士 皇后 国王".split()
MINORS = [f"{s}{r}" for s in SUITS for r in RANKS]
ELEMENTS = dict(zip(MAJORS, "风 风 水 土 火 土 风 水 火 土 火 风 水 水 火 土 火 风 水 火 火 土".split()))
ELEMENTS.update({c: SUITS[c[:2]] for c in MINORS})
CARDS = MAJORS + MINORS

SPREADS = {
    "single": ("单张牌", "当前指引,1,0"),
    "three": ("三牌阵", "过去,0,0|现在,1,0|未来,0,1"),
    "diamond": ("五牌阵", "核心,1,0|根源,0,0|阻力,0,0|潜力,0,0|建议,1,1"),
    "moon": ("月亮牌阵", "新月,1,0|上弦,0,0|满月,1,0|下弦,0,0"),
    "horseshoe": (
        "马蹄形",
        "远期过去,0,0|近期过去,0,0|当前,1,0|近期未来,0,0|外部影响,1,0|建议,0,1|结果,1,1",
    ),
    "celtic": (
        "凯尔特十字",
        "核心,1,0|交叉,0,0|意识目标,0,0|根基过去,0,0|近期过去,1,0|近期未来,0,0|"
        "自我,0,0|环境,0,0|希望与恐惧,0,0|结果,1,1",
    ),
}
TIME = {"morning": ("火", "风"), "afternoon": ("水", "土"), "night": ("major",)}


def make_seed(question=""):
    data = os.urandom(32) + str(time.time_ns()).encode() + question.encode()
    return int(hashlib.sha256(data).hexdigest()[:16], 16)


def get_time_factor(hour=None):
    h = datetime.now().hour if hour is None else hour
    return "morning" if 6 <= h < 12 else "afternoon" if h < 18 else "night"


def weight(card, key, boosted):
    major = card in MAJORS
    base = (60 / 28) if int(key) * major else 1.0
    hit = ("major" in boosted) * major + (ELEMENTS[card] in boosted)
    return base * (1.08 if hit else 1.0)


def draw_cards(spread_key, question="", seed=None, time_factor=None):
    spread_name, raw = SPREADS[spread_key]
    final_seed = make_seed(question) if seed is None else seed
    final_factor = get_time_factor() if time_factor is None else time_factor
    rng, pool, boosted, cards = random.Random(final_seed), list(CARDS), TIME[final_factor], []
    for item in raw.split("|"):
        name, key, upright = item.split(",")
        picked = rng.choices(pool, weights=[weight(c, key, boosted) for c in pool], k=1)[0]
        pool.remove(picked)
        card = {
            "position": name,
            "card": picked,
            "orientation": "正位" if rng.random() < (0.7 if int(upright) else 0.6) else "逆位",
            "is_major": picked in MAJORS,
        }
        cards.append(card)
    return {
        "seed": final_seed,
        "spread": spread_key,
        "spread_name": spread_name,
        "question": question,
        "time_factor": final_factor,
        "cards": cards,
    }


def main():
    parser = argparse.ArgumentParser(description="塔罗牌抽牌脚本")
    parser.add_argument("--spread", required=True, choices=SPREADS)
    parser.add_argument("--question", default="")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--time-factor", choices=TIME)
    parser.add_argument("--json-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    print(json.dumps(draw_cards(args.spread, args.question, args.seed, args.time_factor), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
