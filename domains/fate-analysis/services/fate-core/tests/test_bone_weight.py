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
    assert result["weightCn"] == "7两1钱"
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


def test_gender_changes_interpretation_audience_not_weight() -> None:
    male = calc_bone_weight("甲子", 1, 1, "子", gender="male")
    female = calc_bone_weight("甲子", 1, 1, "子", gender="female")

    assert male["weightQian"] == female["weightQian"]
    assert male["components"] == female["components"]
    assert male["interpretation"]["audience"] == "男"
    assert female["interpretation"]["audience"] == "女"
    assert male["interpretation"]["genderSpecific"] is False
    assert female["interpretation"]["genderSpecific"] is False


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


def test_seven_liang_two_qian_has_no_executable_gendered_interpretation() -> None:
    assert 72 not in BONE_TEXT_QIAN
    assert all(72 not in verses for verses in BONE_GENDERED_VERSE_QIAN.values())


def test_unknown_gender_is_rejected() -> None:
    with pytest.raises(ValueError, match="性别"):
        calc_bone_weight("甲子", 1, 1, "子", gender="unknown")


def test_leap_month_policy_is_explicit_and_preserves_source_month() -> None:
    first_half = calc_bone_weight("甲子", -3, 15, "子")
    second_half = calc_bone_weight("甲子", -3, 16, "子")

    assert first_half["components"]["month"] == {
        "month": 3,
        "sourceMonth": 3,
        "effectiveMonth": 3,
        "isLeapMonth": True,
        "leapMonthPolicy": "split_at_15",
        "weight": 1.8,
    }
    assert second_half["components"]["month"] == {
        "month": 4,
        "sourceMonth": 3,
        "effectiveMonth": 4,
        "isLeapMonth": True,
        "leapMonthPolicy": "split_at_15",
        "weight": 0.9,
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
    assert legacy["boneWeight"]["weightQian"] == pure["boneWeight"]["weightQian"]
    assert pure["analysisEvidence"]["items"]["boneWeight"]["conclusion"]["tableVersion"] == ("common-weight-table-v1")
