from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))

import location  # noqa: E402


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("999,999", "经度必须在 -180 到 180 之间"),
        ("181,0", "经度必须在 -180 到 180 之间"),
        ("-181,0", "经度必须在 -180 到 180 之间"),
        ("0,91", "纬度必须在 -90 到 90 之间"),
        ("0,-91", "纬度必须在 -90 到 90 之间"),
    ],
)
def test_direct_coordinate_input_rejects_out_of_range_values(raw: str, message: str):
    with pytest.raises(ValueError, match=message):
        location.get(raw)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("180,90", (180.0, 90.0)),
        ("-180,-90", (-180.0, -90.0)),
        ("0,0", (0.0, 0.0)),
    ],
)
def test_direct_coordinate_input_accepts_legal_boundaries(raw: str, expected: tuple[float, float]):
    assert location.get(raw) == expected


def test_full_administrative_path_resolves_one_location():
    resolved = location.resolve("陕西省西安市长安区", mode="domestic")

    assert resolved.location_id == "cn:610116"
    assert resolved.coordinate_system == "WGS84"
    assert resolved.coordinate_precision == "district_centroid"
    assert resolved.timezone == "Asia/Shanghai"
    assert resolved.longitude == pytest.approx(108.93366)
    assert resolved.latitude == pytest.approx(34.03702)


def test_unique_short_city_name_remains_supported():
    resolved = location.resolve("杭州", mode="domestic")

    assert resolved.location_id == "cn:330100"
    assert resolved.coordinate_precision == "city_centroid"
    assert resolved.longitude == pytest.approx(120.16142)
    assert resolved.latitude == pytest.approx(30.29365)


def test_ambiguous_county_name_requires_full_administrative_path():
    with pytest.raises(ValueError, match="地点存在多个匹配") as exc_info:
        location.get("长安区")

    message = str(exc_info.value)
    assert "河北省石家庄市长安区" in message
    assert "陕西省西安市长安区" in message


def test_retired_administrative_code_is_not_exposed_as_duplicate_candidate():
    candidates = location.search_records("福建省三明市三元区", mode="domestic")

    assert [(item.location_id, item.display_name) for item in candidates] == [
        ("cn:350404", "福建省三明市三元区"),
    ]
    with pytest.raises(ValueError, match="地点 ID 不存在"):
        location.resolve("cn:350403")


@pytest.mark.parametrize(
    ("query", "expected_location_id"),
    [
        ("西安长安", "cn:610116"),
        ("陕西西安", "cn:610100"),
        ("北京朝阳", "cn:110105"),
    ],
)
def test_domestic_fuzzy_search_ignores_administrative_suffixes(query, expected_location_id):
    candidates = location.search_records(query, mode="domestic", limit=8)

    assert candidates
    assert candidates[0].location_id == expected_location_id


def test_location_options_are_qualified_deduplicated_and_conflict_free():
    options = location.option_values()

    assert len(options) > 3000
    assert len(options) == len(set(options))
    assert options == tuple(sorted(options))
    assert "北京市朝阳区" in options
    assert "陕西省西安市长安区" in options
    assert "江苏省南京市鼓楼区" in options
    assert "福建省三明市三元区" in options


def test_get_coords_does_not_hide_ambiguity_by_selecting_first_match():
    assert location.get_coords("长安区") is None


def test_location_rejects_input_over_server_limit():
    with pytest.raises(ValueError, match="地点输入过长，最多 160 个字符"):
        location.get("北" * 161)


def test_global_location_search_returns_stable_id_and_iana_timezone():
    resolved = location.resolve("纽约", mode="overseas")

    assert resolved.location_id == "geonames:5128581"
    assert resolved.country_code == "US"
    assert resolved.coordinate_system == "WGS84"
    assert resolved.timezone == "America/New_York"


def test_direct_coordinates_resolve_timezone_without_network():
    resolved = location.resolve("116.4074,39.9042", mode="coordinates")

    assert resolved.location_id == "coordinates:116.4074,39.9042"
    assert resolved.timezone == "Asia/Shanghai"
    assert resolved.source == "user"


def test_nonexistent_dst_wall_time_is_rejected():
    new_york = location.resolve("geonames:5128581")

    with pytest.raises(ValueError, match="夏令时跳跃缺口"):
        location.normalize_birth_time(
            datetime(2024, 3, 10, 2, 30),
            new_york,
            time_basis="local_civil",
        )


def test_ambiguous_dst_wall_time_requires_and_honors_fold_choice():
    new_york = location.resolve("geonames:5128581")
    wall_time = datetime(2024, 11, 3, 1, 30)

    with pytest.raises(ValueError, match="重复出现"):
        location.normalize_birth_time(wall_time, new_york, time_basis="local_civil")

    earlier = location.normalize_birth_time(
        wall_time,
        new_york,
        time_basis="local_civil",
        fold_choice="earlier",
    )
    later = location.normalize_birth_time(
        wall_time,
        new_york,
        time_basis="local_civil",
        fold_choice="later",
    )
    assert earlier.engine_beijing_time.isoformat() == "2024-11-03T13:30:00"
    assert later.engine_beijing_time.isoformat() == "2024-11-03T14:30:00"
    assert earlier.utc_offset_seconds == -14400
    assert later.utc_offset_seconds == -18000
