"""出生地点、IANA 时区与出生钟表口径解析。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from typing import Literal
from zoneinfo import ZoneInfo

from location_catalog import CatalogLocation, get_catalog

LocationMode = Literal["domestic", "overseas", "coordinates"]
TimeBasis = Literal["local_civil", "beijing_time", "utc"]
FoldChoice = Literal["earlier", "later"]

_COORDINATE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$")
_MAX_LOCATION_LENGTH = 160


@dataclass(frozen=True, slots=True)
class ResolvedLocation:
    location_id: str
    mode: str
    name: str
    display_name: str
    country_code: str
    admin1_code: str
    admin2_code: str
    admin3_code: str
    longitude: float
    latitude: float
    coordinate_system: str
    timezone: str
    coordinate_precision: str
    source: str
    source_version: str

    @classmethod
    def from_catalog(cls, item: CatalogLocation) -> ResolvedLocation:
        return cls(
            location_id=item.location_id,
            mode=item.mode,
            name=item.name,
            display_name=item.display_name,
            country_code=item.country_code,
            admin1_code=item.admin1_code,
            admin2_code=item.admin2_code,
            admin3_code=item.admin3_code,
            longitude=item.longitude,
            latitude=item.latitude,
            coordinate_system=item.coordinate_system,
            timezone=item.timezone,
            coordinate_precision=item.coordinate_precision,
            source=item.source,
            source_version=item.source_version,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "locationId": self.location_id,
            "mode": self.mode,
            "name": self.name,
            "displayName": self.display_name,
            "countryCode": self.country_code,
            "admin1Code": self.admin1_code,
            "admin2Code": self.admin2_code,
            "admin3Code": self.admin3_code,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "coordinateSystem": self.coordinate_system,
            "timezone": self.timezone,
            "coordinatePrecision": self.coordinate_precision,
            "source": self.source,
            "sourceVersion": self.source_version,
        }


@dataclass(frozen=True, slots=True)
class NormalizedBirthTime:
    original_wall_time: datetime
    engine_beijing_time: datetime
    input_timezone: str
    time_basis: str
    utc_offset_seconds: int
    fold: int

    def as_dict(self) -> dict[str, object]:
        return {
            "originalWallTime": self.original_wall_time.isoformat(sep=" "),
            "engineBeijingTime": self.engine_beijing_time.isoformat(sep=" "),
            "inputTimezone": self.input_timezone,
            "timeBasis": self.time_basis,
            "utcOffsetSeconds": self.utc_offset_seconds,
            "fold": self.fold,
        }


def _validate_coordinates(longitude: float, latitude: float) -> tuple[float, float]:
    if not -180 <= longitude <= 180:
        raise ValueError("经度必须在 -180 到 180 之间")
    if not -90 <= latitude <= 90:
        raise ValueError("纬度必须在 -90 到 90 之间")
    return longitude, latitude


@lru_cache(maxsize=1)
def _timezone_finder():
    from timezonefinder import TimezoneFinder

    return TimezoneFinder()


def resolve_coordinates(longitude: float, latitude: float) -> ResolvedLocation:
    longitude, latitude = _validate_coordinates(longitude, latitude)
    timezone = _timezone_finder().timezone_at(lng=longitude, lat=latitude)
    if not timezone:
        raise ValueError("该经纬度无法映射到陆地 IANA 时区，请选择城市或明确提供时区")
    normalized_longitude = round(longitude, 6)
    normalized_latitude = round(latitude, 6)
    display_name = f"{normalized_longitude},{normalized_latitude}"
    return ResolvedLocation(
        location_id=f"coordinates:{display_name}",
        mode="coordinates",
        name=display_name,
        display_name=display_name,
        country_code="",
        admin1_code="",
        admin2_code="",
        admin3_code="",
        longitude=normalized_longitude,
        latitude=normalized_latitude,
        coordinate_system="WGS84",
        timezone=timezone,
        coordinate_precision="user_coordinates",
        source="user",
        source_version="input-v1",
    )


def resolve(value: str, *, mode: str | None = None) -> ResolvedLocation:
    normalized = (value or "").strip()
    if not normalized:
        raise ValueError("地点为空")
    if len(normalized) > _MAX_LOCATION_LENGTH:
        raise ValueError(f"地点输入过长，最多 {_MAX_LOCATION_LENGTH} 个字符")

    coordinate_match = _COORDINATE_RE.fullmatch(normalized)
    if coordinate_match:
        if mode and mode != "coordinates":
            raise ValueError("经纬度输入必须选择 coordinates 地区模式")
        return resolve_coordinates(float(coordinate_match.group(1)), float(coordinate_match.group(2)))

    if mode == "coordinates":
        raise ValueError("coordinates 地区模式必须使用 lng,lat 格式")

    catalog = get_catalog()
    if normalized.startswith(("cn:", "geonames:")):
        item = catalog.get(normalized)
        if not item:
            raise ValueError(f"地点 ID 不存在: {normalized}")
        if mode and item.mode != mode:
            raise ValueError(f"地点 ID 与选择模式不一致: {normalized}")
        return ResolvedLocation.from_catalog(item)

    exact = catalog.exact(normalized, mode=mode)
    if len(exact) == 1:
        return ResolvedLocation.from_catalog(exact[0])
    if len(exact) > 1:
        labels = "、".join(item.display_name for item in exact[:8])
        suffix = "等" if len(exact) > 8 else ""
        raise ValueError(f"地点存在多个匹配，请选择稳定地点 ID: {labels}{suffix}")

    suggestions = catalog.search(normalized, mode=mode, limit=8)
    if suggestions:
        labels = "、".join(item.display_name for item in suggestions)
        raise ValueError(f"地点输入不完整，请选择候选地点: {labels}")
    raise ValueError(f"地点无法识别: {normalized}")


def search_records(query: str, *, mode: str | None = None, limit: int = 20) -> list[ResolvedLocation]:
    if not 1 <= limit <= 100:
        raise ValueError("地点搜索 limit 必须在 1 到 100 之间")
    return [ResolvedLocation.from_catalog(item) for item in get_catalog().search(query, mode=mode, limit=limit)]


def search(query: str) -> list[tuple[str, float, float]]:
    return [(item.display_name, item.longitude, item.latitude) for item in search_records(query, limit=50)]


@lru_cache(maxsize=1)
def option_values() -> tuple[str, ...]:
    return get_catalog().domestic_option_values()


def get(value: str) -> tuple[float, float]:
    item = resolve(value)
    return item.longitude, item.latitude


def get_coords(value: str) -> tuple[float, float] | None:
    try:
        return get(value)
    except ValueError:
        return None


def _valid_local_time(naive: datetime, timezone: ZoneInfo, fold: int) -> datetime | None:
    aware = naive.replace(tzinfo=timezone, fold=fold)
    round_trip = aware.astimezone(UTC).astimezone(timezone)
    if round_trip.replace(tzinfo=None) != naive:
        return None
    return aware


def normalize_birth_time(
    wall_time: datetime,
    location: ResolvedLocation,
    *,
    time_basis: TimeBasis,
    fold_choice: FoldChoice | None = None,
) -> NormalizedBirthTime:
    """把用户钟表时间转换为现有真太阳时引擎使用的北京时间墙上时间。"""
    if wall_time.tzinfo is not None:
        raise ValueError("出生时间规范化只接受不带时区的墙上时间")
    timezone_name = {
        "local_civil": location.timezone,
        "beijing_time": "Asia/Shanghai",
        "utc": "UTC",
    }.get(time_basis)
    if not timezone_name:
        raise ValueError("时间口径必须为 local_civil、beijing_time 或 utc")

    timezone = ZoneInfo(timezone_name)
    earlier = _valid_local_time(wall_time, timezone, 0)
    later = _valid_local_time(wall_time, timezone, 1)
    if earlier is None and later is None:
        raise ValueError(f"出生时间位于 {timezone_name} 的夏令时跳跃缺口，属于不存在的当地时间")

    ambiguous = (
        earlier is not None
        and later is not None
        and earlier.utcoffset() is not None
        and later.utcoffset() is not None
        and earlier.utcoffset() != later.utcoffset()
    )
    if ambiguous and fold_choice not in {"earlier", "later"}:
        raise ValueError("出生时间在夏令时回拨时重复出现，请明确选择 earlier 或 later")
    fold = 1 if ambiguous and fold_choice == "later" else 0
    aware = later if fold else earlier
    if aware is None:
        aware = later
        fold = 1
    if aware is None or aware.utcoffset() is None:
        raise ValueError("出生时间无法应用 IANA 时区规则")

    beijing_wall_time = aware.astimezone(ZoneInfo("Asia/Shanghai")).replace(tzinfo=None)
    return NormalizedBirthTime(
        original_wall_time=wall_time,
        engine_beijing_time=beijing_wall_time,
        input_timezone=timezone_name,
        time_basis=time_basis,
        utc_offset_seconds=int(aware.utcoffset().total_seconds()),
        fold=fold,
    )


def catalog_status() -> dict[str, object]:
    return get_catalog().status()


__all__ = [
    "FoldChoice",
    "LocationMode",
    "NormalizedBirthTime",
    "ResolvedLocation",
    "TimeBasis",
    "catalog_status",
    "get",
    "get_coords",
    "normalize_birth_time",
    "option_values",
    "resolve",
    "resolve_coordinates",
    "search",
    "search_records",
]
