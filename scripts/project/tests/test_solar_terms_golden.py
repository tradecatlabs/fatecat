from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR_LUNAR = ROOT / "assets" / "vendor" / "github" / "lunar-python-master"
FIXTURE = ROOT / "assets" / "data" / "calendar" / "solar_terms" / "golden" / "solar_terms_1900_2030.json"

if str(VENDOR_LUNAR) not in sys.path:
    sys.path.insert(0, str(VENDOR_LUNAR))

from lunar_python import Solar  # noqa: E402

JIE_TERMS = {"立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "小寒"}
FIXTURE_BOUNDARY_LOCK_YEARS = {1936, 1969, 2000, 2024, 2030}
FIXTURE_BOUNDARY_LOCK_SECONDS = 120
TERM_ALIASES = {
    "冬至": ["冬至", "DONG_ZHI"],
    "小寒": ["小寒", "XIAO_HAN"],
    "大寒": ["大寒", "DA_HAN"],
    "立春": ["立春", "LI_CHUN"],
    "雨水": ["雨水", "YU_SHUI"],
    "惊蛰": ["惊蛰", "JING_ZHE"],
    "大雪": ["大雪", "DA_XUE"],
}


def _load_fixture() -> dict:
    with FIXTURE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _fixture_dt(row: dict) -> datetime:
    return datetime.fromisoformat(row["iso"])


def _solar_dt(solar) -> datetime:
    return datetime(
        solar.getYear(),
        solar.getMonth(),
        solar.getDay(),
        solar.getHour(),
        solar.getMinute(),
        solar.getSecond(),
    )


def _actual_term_dt(row: dict) -> datetime:
    expected = _fixture_dt(row)
    lunar = Solar.fromYmdHms(expected.year, expected.month, expected.day, 12, 0, 0).getLunar()
    table = lunar.getJieQiTable()
    names = TERM_ALIASES.get(row["term"], [row["term"]])
    candidates = [_solar_dt(table[name]) for name in names if name in table]
    assert candidates, f"missing lunar-python term candidates for {row['term']}"
    return min(candidates, key=lambda candidate: abs((candidate - expected.replace(microsecond=0)).total_seconds()))


def _eight_char_at(dt: datetime):
    return Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar().getEightChar()


def test_solar_terms_fixture_schema_and_coverage():
    payload = _load_fixture()

    assert payload["schemaVersion"] == 1
    assert payload["timezone"] == "Asia/Shanghai"
    assert payload["source"]["sha256"] == "76585429b1af2d4b9b66bf06c6eaf7ce8696a76b47fd18b1f27497df8d4759e4"
    assert payload["coverage"] == {"startYear": 1900, "endYear": 2030, "termsPerYear": 24, "rowCount": 3144}
    assert payload["rows"][0]["term"] == "小寒"
    assert payload["rows"][-1]["term"] == "冬至"


def test_lunar_python_solar_terms_match_golden_fixture_with_declared_tolerance():
    payload = _load_fixture()
    tolerance = int(payload["toleranceSeconds"])

    for row in payload["rows"]:
        expected = _fixture_dt(row)
        actual = _actual_term_dt(row)
        delta = abs((actual - expected.replace(microsecond=0)).total_seconds())
        assert delta <= tolerance, f"{row['term']} {expected.isoformat()} delta={delta}s"


def test_month_pillar_changes_across_jie_boundaries():
    payload = _load_fixture()
    checked = 0

    for row in payload["rows"]:
        if row["term"] not in JIE_TERMS or int(row["year"]) not in FIXTURE_BOUNDARY_LOCK_YEARS:
            continue
        boundary = _fixture_dt(row).replace(microsecond=0)
        before = _eight_char_at(boundary - timedelta(seconds=1)).getMonth()
        after = _eight_char_at(boundary + timedelta(seconds=FIXTURE_BOUNDARY_LOCK_SECONDS)).getMonth()
        assert before != after, f"{row['term']} {boundary.isoformat()} should change month pillar"
        checked += 1
    assert checked == len(JIE_TERMS) * len(FIXTURE_BOUNDARY_LOCK_YEARS)


def test_lichun_changes_bazi_year_boundary():
    payload = _load_fixture()
    checked = 0

    for row in payload["rows"]:
        if row["term"] != "立春" or int(row["year"]) not in FIXTURE_BOUNDARY_LOCK_YEARS:
            continue
        boundary = _fixture_dt(row).replace(microsecond=0)
        before = _eight_char_at(boundary - timedelta(seconds=1)).getYear()
        after = _eight_char_at(boundary + timedelta(seconds=FIXTURE_BOUNDARY_LOCK_SECONDS)).getYear()
        assert before != after, f"立春 {boundary.isoformat()} should change bazi year pillar"
        checked += 1
    assert checked == len(FIXTURE_BOUNDARY_LOCK_YEARS)


def test_true_solar_time_feeds_lunar_python_across_lichun_fixture_boundary():
    from bazi_calculator import BaziCalculator
    from report_generator import build_report_hide

    boundary = datetime(2024, 2, 4, 16, 26, 53)
    samples = [
        ("2024-02-04T16:54:00", "before", "癸卯", "乙丑"),
        ("2024-02-04T16:56:00", "after", "甲辰", "丙寅"),
    ]

    for iso_value, side, expected_year, expected_month in samples:
        calc = BaziCalculator(
            datetime.fromisoformat(iso_value),
            "male",
            116.4074,
            latitude=39.9042,
            name="测试样本",
            birth_place="北京",
            use_true_solar_time=True,
        )
        result = calc.calculate(hide=build_report_hide("bazi"))
        true_solar_time = calc.true_solar_time.replace(tzinfo=None)

        if side == "before":
            assert true_solar_time < boundary
        else:
            assert true_solar_time > boundary
        assert result["fourPillars"]["year"]["fullName"] == expected_year
        assert result["fourPillars"]["month"]["fullName"] == expected_month


def test_yun_start_time_regression_samples():
    samples = [
        ("1990-01-01T08:00:00", "male", "1998-04-11 08:00:00"),
        ("1990-01-01T08:00:00", "female", "1991-07-11 08:00:00"),
        ("2024-02-04T16:30:00", "male", "2034-01-04 16:30:00"),
        ("2024-02-04T16:30:00", "female", "2024-02-04 16:30:00"),
    ]

    for iso_value, gender, expected in samples:
        dt = datetime.fromisoformat(iso_value)
        ec = _eight_char_at(dt)
        yun = ec.getYun(1 if gender == "male" else 0)
        assert yun.getStartSolar().toYmdHms() == expected
