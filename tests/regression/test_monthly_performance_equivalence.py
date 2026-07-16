from __future__ import annotations

from typing import Any

from lunar_python.eightchar import LiuYue
from lunar_python.util.LunarUtil import LunarUtil

from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.kernel.bazi_calculator import BaziCalculator, _CachedAnnualGanZhi
from report_generator import generate_monthly_section


class _LiuYue:
    def __init__(self) -> None:
        self.gan_zhi_calls = 0

    @staticmethod
    def getIndex() -> int:
        return 0

    @staticmethod
    def getMonthInChinese() -> str:
        return "正"

    def getGanZhi(self) -> str:
        self.gan_zhi_calls += 1
        return "甲寅"


class _LiuNian:
    def __init__(self, monthly: _LiuYue) -> None:
        self.monthly = monthly
        self.gan_zhi_calls = 0

    @staticmethod
    def getYear() -> int:
        return 2026

    def getGanZhi(self) -> str:
        self.gan_zhi_calls += 1
        return "丙午"

    def getLiuYue(self) -> list[_LiuYue]:
        return [self.monthly]


class _DaYun:
    def __init__(self, annual: _LiuNian) -> None:
        self.annual = annual

    def getLiuNian(self) -> list[_LiuNian]:
        return [self.annual]


class _Yun:
    def __init__(self, major: _DaYun) -> None:
        self.major = major

    def getDaYun(self) -> list[_DaYun]:
        return [self.major]


class _CountingList(list[dict[str, Any]]):
    def __init__(self, values: list[dict[str, Any]]) -> None:
        super().__init__(values)
        self.iteration_count = 0

    def __iter__(self):
        self.iteration_count += 1
        return super().__iter__()


def test_monthly_ganzhi_is_computed_once_per_unique_month() -> None:
    monthly = _LiuYue()
    annual = _LiuNian(monthly)
    yun = _Yun(_DaYun(annual))

    result = BaziCalculator._calc_monthly(object(), yun)

    assert result == [
        {
            "year": 2026,
            "month": 1,
            "monthCn": "正",
            "ganZhi": "庚寅",
            "stem": "庚",
            "branch": "寅",
        }
    ]
    assert annual.gan_zhi_calls == 1
    assert monthly.gan_zhi_calls == 0


def test_cached_annual_adapter_matches_lunar_python_for_all_ganzhi_and_months() -> None:
    for annual_gan_zhi in LunarUtil.JIA_ZI:
        original_annual = _CachedAnnualGanZhi(annual_gan_zhi)
        cached_annual = _CachedAnnualGanZhi(annual_gan_zhi)
        expected = [LiuYue(original_annual, index).getGanZhi() for index in range(12)]
        actual = [LiuYue(cached_annual, index).getGanZhi() for index in range(12)]
        assert actual == expected


def test_monthly_report_indexes_fortune_once_and_preserves_first_match() -> None:
    monthly_fortune = _CountingList(
        [
            {"year": 2026, "month": 1, "ganZhi": "甲寅", "shiShen": "首项十神", "naYin": "首项纳音"},
            {"year": 2026, "month": 1, "ganZhi": "甲寅", "shiShen": "重复十神", "naYin": "重复纳音"},
            {"year": 2026, "month": 2, "ganZhi": "乙卯", "shiShen": "次项十神", "naYin": "次项纳音"},
        ]
    )
    result = {
        "monthlyFortune": monthly_fortune,
        "monthlySpirits": [
            {"year": 2026, "month": 1, "monthCn": "正", "ganZhi": "甲寅", "spirits": []},
            {"year": 2026, "month": 2, "monthCn": "二", "ganZhi": "乙卯", "spirits": []},
        ],
        "xiaoYun": [],
    }

    report = generate_monthly_section(result)

    assert monthly_fortune.iteration_count == 1
    assert "首项十神" in report
    assert "首项纳音" in report
    assert "重复十神" not in report
    assert "重复纳音" not in report
    assert "次项十神" in report
    assert "次项纳音" in report


def test_full_bazi_horizon_remains_98_years_and_1176_months() -> None:
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="bazi",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "male",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京市",
                "name": "测试样本",
                "useTrueSolarTime": True,
            },
        )
    )

    assert len(result.data["annualFortune"]) == 98
    assert len(result.data["monthlyFortune"]) == 1176
    assert len(result.data["monthlySpirits"]) == 1176
