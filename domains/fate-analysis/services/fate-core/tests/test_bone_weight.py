from __future__ import annotations

from datetime import datetime

import pytest

from fate_core.kernel.bazi_calculator import BaziCalculator
from fate_core.kernel.bone_weight import (
    BONE_DAY_QIAN,
    BONE_GENDERED_VERSE_QIAN,
    BONE_HOUR_QIAN,
    BONE_MONTH_QIAN,
    BONE_TEXT_QIAN,
    BONE_YEAR_QIAN,
    calc_bone_weight,
)
from fate_core.usecases.calculate_pure_analysis import PureAnalysisInput, calculate_pure_analysis


def test_maximum_weight_uses_exact_integer_qian() -> None:
    result = calc_bone_weight("己卯", 3, 18, "子", gender="male")

    assert result["weightQian"] == 71
    assert result["weight"] == 7.1
    assert result["weightCn"] == "七两一钱"
    assert result["text"] == BONE_GENDERED_VERSE_QIAN["male"][71]


def test_weight_table_reaches_every_value_from_21_to_71_but_not_72() -> None:
    totals = {
        year + month + day + hour
        for year in BONE_YEAR_QIAN.values()
        for month in BONE_MONTH_QIAN.values()
        for day in BONE_DAY_QIAN.values()
        for hour in BONE_HOUR_QIAN.values()
    }

    assert totals == set(range(21, 72))
    assert set(BONE_TEXT_QIAN) == totals
    assert 72 not in totals


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (("不存在", 1, 1, "子"), "年柱"),
        (([], 1, 1, "子"), "年柱"),
        (("甲子", 13, 1, "子"), "农历月份"),
        (("甲子", 1, 31, "子"), "农历日期"),
        (("甲子", 1, 1.0, "子"), "农历日期"),
        (("甲子", 1, 1, "不存在"), "时支"),
        (("甲子", 1, 1, []), "时支"),
    ],
)
def test_invalid_components_are_rejected(args: tuple[object, ...], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        calc_bone_weight(*args)


def test_gender_selects_distinct_interpretation_without_changing_weight() -> None:
    male = calc_bone_weight("甲子", 1, 1, "子", gender="male")
    female = calc_bone_weight("甲子", 1, 1, "子", gender="female")

    assert male["weightQian"] == female["weightQian"]
    assert male["components"] == female["components"]
    assert male["interpretation"]["audience"] == "男"
    assert female["interpretation"]["audience"] == "女"
    assert male["interpretation"]["genderSpecific"] is True
    assert female["interpretation"]["genderSpecific"] is True
    assert male["interpretation"]["coverage"] == "gendered-male-21-72"
    assert female["interpretation"]["coverage"] == "gendered-female-21-71"
    assert male["text"] != female["text"]


def test_gendered_verse_tables_preserve_distinct_gender_ranges() -> None:
    reachable = set(range(21, 72))

    assert set(BONE_GENDERED_VERSE_QIAN) == {"male", "female"}
    assert set(BONE_GENDERED_VERSE_QIAN["male"]) == reachable | {72}
    assert set(BONE_GENDERED_VERSE_QIAN["female"]) == reachable


def test_three_liang_seven_qian_uses_gendered_verse_and_chinese_components() -> None:
    male = calc_bone_weight("丙午", 5, 17, "卯", gender="male")
    female = calc_bone_weight("丙午", 5, 17, "卯", gender="female")

    assert male["weightQian"] == female["weightQian"] == 37
    assert male["weightCn"] == female["weightCn"] == "三两七钱"
    assert male["text"] == BONE_GENDERED_VERSE_QIAN["male"][37]
    assert female["text"] == BONE_GENDERED_VERSE_QIAN["female"][37]
    assert male["text"] != female["text"]
    assert male["components"]["year"]["weightCn"] == "一两三钱"
    assert male["components"]["month"]["weightCn"] == "五钱"
    assert male["components"]["day"]["weightCn"] == "九钱"
    assert male["components"]["hour"]["weightCn"] == "一两"


def test_seven_liang_one_qian_uses_distinct_gendered_verses() -> None:
    male = calc_bone_weight("己卯", 3, 18, "子", gender="male")
    female = calc_bone_weight("己卯", 3, 18, "子", gender="female")

    assert male["weightQian"] == female["weightQian"] == 71
    assert male["text"] == BONE_GENDERED_VERSE_QIAN["male"][71]
    assert female["text"] == BONE_GENDERED_VERSE_QIAN["female"][71]
    assert male["text"] != female["text"]
    assert male["interpretation"]["genderSpecific"] is True
    assert female["interpretation"]["genderSpecific"] is True
    assert male["interpretation"]["sourceRevision"] == "0f86a690499bfe828aa534fea17f241c85f038f1"


def test_seven_liang_two_qian_exists_only_in_male_verse_table_but_is_not_calculable() -> None:
    assert 72 not in BONE_TEXT_QIAN
    assert BONE_GENDERED_VERSE_QIAN["male"][72]
    assert 72 not in BONE_GENDERED_VERSE_QIAN["female"]


def test_unknown_gender_is_rejected() -> None:
    with pytest.raises(ValueError, match="性别"):
        calc_bone_weight("甲子", 1, 1, "子", gender="unknown")


def test_leap_month_policy_is_explicit_and_preserves_source_month() -> None:
    first_half = calc_bone_weight("甲子", -3, 15, "子")
    second_half = calc_bone_weight("甲子", -3, 16, "子")

    assert first_half["components"]["month"] == {
        "month": 3,
        "monthCn": "三",
        "sourceMonth": 3,
        "sourceMonthCn": "三",
        "effectiveMonth": 3,
        "effectiveMonthCn": "三",
        "isLeapMonth": True,
        "leapMonthPolicy": "split_at_15",
        "weightQian": 18,
        "weight": 1.8,
        "weightCn": "一两八钱",
    }
    assert second_half["components"]["month"] == {
        "month": 4,
        "monthCn": "四",
        "sourceMonth": 3,
        "sourceMonthCn": "三",
        "effectiveMonth": 4,
        "effectiveMonthCn": "四",
        "isLeapMonth": True,
        "leapMonthPolicy": "split_at_15",
        "weightQian": 9,
        "weight": 0.9,
        "weightCn": "九钱",
    }


def test_same_month_leap_policy_is_available_for_versioned_reproduction() -> None:
    result = calc_bone_weight("甲子", -3, 16, "子", leap_month_policy="same_month")

    assert result["components"]["month"]["effectiveMonth"] == 3
    assert result["components"]["month"]["leapMonthPolicy"] == "same_month"


def test_calculation_metadata_exposes_folk_and_attribution_boundaries() -> None:
    result = calc_bone_weight("甲子", 1, 1, "子")

    assert result["calculation"] == {
        "tableVersion": "common-weight-table-v1",
        "unit": "qian",
        "maxReachableQian": 71,
        "nonExecutableWeightsQian": [72],
        "historicalAttributionVerified": False,
        "scope": "folk-appendix-only",
    }


def test_legacy_and_pure_analysis_paths_preserve_gender_metadata() -> None:
    payload = {
        "birth_dt": datetime(1990, 1, 1, 8, 0),
        "gender": "female",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "name": "测试用户",
        "birth_place": "北京",
        "use_true_solar_time": True,
    }
    legacy = BaziCalculator(**payload).calculate(hide={"system": True})
    pure = calculate_pure_analysis(PureAnalysisInput(**payload))

    assert legacy["boneWeight"]["interpretation"]["audience"] == "女"
    assert pure["boneWeight"]["interpretation"]["audience"] == "女"
    assert legacy["boneWeight"]["interpretation"]["genderSpecific"] is True
    assert pure["boneWeight"]["interpretation"]["genderSpecific"] is True
    assert legacy["boneWeight"]["weightQian"] == pure["boneWeight"]["weightQian"]
    assert pure["analysisEvidence"]["items"]["boneWeight"]["conclusion"]["tableVersion"] == ("common-weight-table-v1")
