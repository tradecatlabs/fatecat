from __future__ import annotations

from typing import Any

from fate_core.contracts.runtime import PureAnalysisRuntime


def _build_major_spirits(
    runtime: PureAnalysisRuntime,
    major_fortune: dict[str, Any],
) -> list[dict[str, Any]]:
    calculator = runtime.calculator
    ec = runtime.ec
    day_gan = ec.getDayGan()
    day_zhi = ec.getDayZhi()
    month_zhi = ec.getMonthZhi()
    year_zhi = ec.getYearZhi()

    items: list[dict[str, Any]] = []
    for pillar in major_fortune.get("pillars", []):
        if not isinstance(pillar, dict):
            continue
        gan_zhi = pillar.get("ganZhi") or pillar.get("fullName", "")
        if len(gan_zhi) < 2:
            continue
        gan, zhi = gan_zhi[0], gan_zhi[1]
        items.append(
            {
                "startYear": pillar.get("startYear"),
                "ganZhi": gan_zhi,
                "spirits": calculator._calc_spirits_for_ganzhi(
                    gan,
                    zhi,
                    day_gan,
                    day_zhi,
                    month_zhi,
                    year_zhi,
                ),
                "wuxingContribution": calculator._calc_wuxing_contrib(gan, zhi),
            }
        )
    return items


def _build_annual_spirits(
    runtime: PureAnalysisRuntime,
    annual_fortune: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    calculator = runtime.calculator
    ec = runtime.ec
    day_gan = ec.getDayGan()
    day_zhi = ec.getDayZhi()
    month_zhi = ec.getMonthZhi()
    year_zhi = ec.getYearZhi()

    items: list[dict[str, Any]] = []
    for annual in annual_fortune:
        if not isinstance(annual, dict):
            continue
        gan_zhi = annual.get("ganZhi") or annual.get("fullName", "")
        if len(gan_zhi) < 2:
            continue
        gan, zhi = gan_zhi[0], gan_zhi[1]
        items.append(
            {
                "year": annual.get("year"),
                "ganZhi": gan_zhi,
                "spirits": calculator._calc_spirits_for_ganzhi(
                    gan,
                    zhi,
                    day_gan,
                    day_zhi,
                    month_zhi,
                    year_zhi,
                ),
            }
        )
    return items


def _build_monthly_spirits(
    runtime: PureAnalysisRuntime,
    monthly_fortune: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    calculator = runtime.calculator
    ec = runtime.ec
    day_gan = ec.getDayGan()
    day_zhi = ec.getDayZhi()
    month_zhi = ec.getMonthZhi()
    year_zhi = ec.getYearZhi()

    items: list[dict[str, Any]] = []
    for monthly in monthly_fortune:
        if not isinstance(monthly, dict):
            continue
        gan_zhi = monthly.get("ganZhi", "")
        if len(gan_zhi) < 2:
            continue
        gan, zhi = gan_zhi[0], gan_zhi[1]
        items.append(
            {
                "year": monthly.get("year", ""),
                "month": monthly.get("month", monthly.get("monthCn", "")),
                "monthCn": monthly.get("monthCn", ""),
                "ganZhi": gan_zhi,
                "spirits": calculator._calc_spirits_for_ganzhi(
                    gan,
                    zhi,
                    day_gan,
                    day_zhi,
                    month_zhi,
                    year_zhi,
                ),
            }
        )
    return items


def build_fortune_section(runtime: PureAnalysisRuntime) -> dict[str, Any]:
    """装配纯命理运势字段。"""
    calculator = runtime.calculator
    day_gan = runtime.ec.getDayGan()

    major_fortune = calculator._add_fortune_shishen(calculator._calc_fortune(runtime.yun), day_gan)
    annual_fortune = calculator._add_annual_shishen(calculator._calc_annual(), day_gan)
    monthly_fortune = calculator._add_monthly_shishen(calculator._calc_monthly(runtime.yun), day_gan)

    return {
        "majorFortune": major_fortune,
        "majorFortuneSpirits": _build_major_spirits(runtime, major_fortune),
        "annualFortune": annual_fortune,
        "annualSpirits": _build_annual_spirits(runtime, annual_fortune),
        "monthlyFortune": monthly_fortune,
        "monthlySpirits": _build_monthly_spirits(runtime, monthly_fortune),
    }
