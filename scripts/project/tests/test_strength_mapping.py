from __future__ import annotations

from datetime import datetime

from bazi_calculator import BaziCalculator


def _build_four_pillars(calc: BaziCalculator) -> dict:
    ec = calc.ec
    pillars = {
        pillar: calc._pillar(
            getattr(ec, f"get{pillar.title()}")(),
            getattr(ec, f"get{pillar.title()}Gan")(),
            getattr(ec, f"get{pillar.title()}Zhi")(),
        )
        for pillar in ["year", "month", "day"]
    }
    pillars["hour"] = calc._pillar(ec.getTime(), ec.getTimeGan(), ec.getTimeZhi())
    return pillars


def test_strength_label_thresholds() -> None:
    assert BaziCalculator._map_strength_label(weak=True, strong_score=20) == "身弱"
    assert BaziCalculator._map_strength_label(weak=True, strong_score=21) == "中和偏弱"
    assert BaziCalculator._map_strength_label(weak=True, strong_score=28) == "中和偏弱"
    assert BaziCalculator._map_strength_label(weak=True, strong_score=29) == "中和"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=25) == "中和偏弱"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=26) == "中和"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=33) == "中和"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=34) == "中和偏强"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=37) == "中和偏强"
    assert BaziCalculator._map_strength_label(weak=False, strong_score=38) == "身强"


def test_wuxing_scores_expose_five_level_strength() -> None:
    # 历史故障样本：旧实现会因为时柱帝旺，直接错误落成“身强”。
    calc = BaziCalculator(
        datetime(2013, 1, 1, 9, 19),
        "male",
        longitude=116.4074,
        latitude=39.9042,
        name="孙笑川",
        birth_place="北京",
    )
    wuxing_scores = calc._calc_wuxing_scores(_build_four_pillars(calc))

    assert wuxing_scores["weak"] is False
    assert wuxing_scores["strongScore"] == 25
    assert wuxing_scores["weakStrong"] == "中和偏弱"


def test_weak_bool_has_priority_over_score_side() -> None:
    # 分数可能跨过 29，但 weak=True 时不能直接落到偏强侧。
    assert BaziCalculator._map_strength_label(weak=True, strong_score=32) == "中和"
