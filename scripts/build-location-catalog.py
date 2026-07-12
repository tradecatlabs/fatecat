#!/usr/bin/env python3
"""构建可审计的出生地点目录数据产品。

原始 GeoNames 与行政区快照只在构建阶段使用；运行时只消费经过哈希锁定、
字段归一化和确定性压缩的 NDJSON 数据产品。
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import shutil
import tempfile
import unicodedata
import urllib.request
import zipfile
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from opencc import OpenCC

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PRODUCT_DIR = REPO_ROOT / "domains" / "fate-analysis" / "data-products" / "locations"
SOURCE_LOCK_PATH = DATA_PRODUCT_DIR / "sources.lock.json"
OUTPUT_PATH = DATA_PRODUCT_DIR / "location_catalog.ndjson.gz"
MANIFEST_PATH = DATA_PRODUCT_DIR / "manifest.json"

MAINLAND_PROVINCE_PREFIXES = {
    "11",
    "12",
    "13",
    "14",
    "15",
    "21",
    "22",
    "23",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "50",
    "51",
    "52",
    "53",
    "54",
    "61",
    "62",
    "63",
    "64",
    "65",
}
ADMIN_SUFFIXES = (
    "特别行政区",
    "维吾尔自治区",
    "壮族自治区",
    "回族自治区",
    "自治区",
    "自治县",
    "自治州",
    "地区",
    "新区",
    "矿区",
    "林区",
    "省",
    "市",
    "区",
    "县",
    "旗",
    "盟",
    "州",
)
PSEUDO_AREA_NAMES = {"市辖区", "县", "省直辖县级行政区划", "自治区直辖县级行政区划"}
CJK_RE = re.compile(r"[\u3400-\u9fff]")
SEPARATOR_RE = re.compile(r"[\s'’·\-]+")
TRADITIONAL_TO_SIMPLIFIED = OpenCC("t2s")


@dataclass(frozen=True, slots=True)
class GeoName:
    geoname_id: str
    name: str
    ascii_name: str
    aliases: tuple[str, ...]
    latitude: float
    longitude: float
    feature_class: str
    feature_code: str
    country_code: str
    admin1_code: str
    admin2_code: str
    admin3_code: str
    population: int
    timezone: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_alias(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value or "").strip().casefold()
    return SEPARATOR_RE.sub("", normalized)


def _strip_admin_suffix(value: str) -> str:
    normalized = (value or "").strip()
    for suffix in ADMIN_SUFFIXES:
        if normalized.endswith(suffix) and len(normalized) > len(suffix):
            return normalized[: -len(suffix)]
    return normalized


def _unique_parts(*parts: str) -> list[str]:
    result: list[str] = []
    for part in parts:
        value = (part or "").strip()
        if value and (not result or result[-1] != value):
            result.append(value)
    return result


def _record_aliases(*values: str, extra: Iterable[str] = ()) -> list[str]:
    aliases: dict[str, str] = {}
    for raw in [*values, *extra]:
        value = (raw or "").strip()
        normalized = _normalize_alias(value)
        if normalized and len(value) <= 160:
            aliases.setdefault(normalized, value)
    return [aliases[key] for key in sorted(aliases)]


def _download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "FateCat location catalog builder/1"})
    with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)


def _materialize_sources(source_dir: Path, source_lock: dict[str, Any], *, download: bool) -> dict[str, Path]:
    source_dir.mkdir(parents=True, exist_ok=True)
    materialized: dict[str, Path] = {}
    for source in source_lock["sources"]:
        path = source_dir / source["fileName"]
        if not path.exists():
            if not download:
                raise FileNotFoundError(f"缺少原始来源文件: {path}")
            _download(source["url"], path)
        actual_hash = _sha256(path)
        if actual_hash != source["sha256"]:
            raise RuntimeError(f"来源文件 hash 不匹配: {source['id']} expected={source['sha256']} actual={actual_hash}")
        materialized[source["id"]] = path
    return materialized


def _read_geonames_zip(path: Path) -> Iterable[GeoName]:
    with zipfile.ZipFile(path) as archive:
        text_files = [
            name
            for name in archive.namelist()
            if name.endswith(".txt") and Path(name).name.casefold() not in {"readme.txt", "readme"}
        ]
        if len(text_files) != 1:
            raise RuntimeError(f"GeoNames ZIP 文本文件数量异常: {path}")
        with archive.open(text_files[0]) as raw, io.TextIOWrapper(raw, encoding="utf-8") as handle:
            for line in handle:
                columns = line.rstrip("\n").split("\t")
                if len(columns) < 19:
                    continue
                aliases = tuple(alias for alias in columns[3].split(",") if alias)
                yield GeoName(
                    geoname_id=columns[0],
                    name=columns[1],
                    ascii_name=columns[2],
                    aliases=aliases,
                    latitude=float(columns[4]),
                    longitude=float(columns[5]),
                    feature_class=columns[6],
                    feature_code=columns[7],
                    country_code=columns[8],
                    admin1_code=columns[10],
                    admin2_code=columns[11],
                    admin3_code=columns[12],
                    population=int(columns[14] or 0),
                    timezone=columns[17],
                )


def _geoname_aliases(item: GeoName) -> set[str]:
    return {
        normalized
        for normalized in (_normalize_alias(value) for value in (item.name, item.ascii_name, *item.aliases))
        if normalized
    }


def _choose_geoname(candidates: Iterable[GeoName], *, preferred_features: tuple[str, ...]) -> GeoName | None:
    values = list(candidates)
    if not values:
        return None
    priority = {feature: index for index, feature in enumerate(preferred_features)}
    values.sort(
        key=lambda item: (
            priority.get(item.feature_code, len(priority)),
            -item.population,
            item.geoname_id,
        )
    )
    return values[0]


def _load_china_geonames(path: Path) -> tuple[list[GeoName], dict[str, set[str]]]:
    retained_codes = {"ADM1", "ADM2", "ADM3", "PPLC", "PPLA", "PPLA2", "PPLA3"}
    retained = [item for item in _read_geonames_zip(path) if item.feature_code in retained_codes]
    aliases = {item.geoname_id: _geoname_aliases(item) for item in retained}
    return retained, aliases


def _select_chinese_alias(item: GeoName) -> str | None:
    values = {
        TRADITIONAL_TO_SIMPLIFIED.convert(alias.strip())
        for alias in item.aliases
        if CJK_RE.search(alias) and 1 <= len(alias.strip()) <= 24 and "/" not in alias
    }
    if not values:
        return None
    return min(values, key=lambda value: (len(value), value))


def _global_record(item: GeoName, source_version: str) -> dict[str, Any]:
    chinese_name = _select_chinese_alias(item)
    display_name = item.name
    if chinese_name and _normalize_alias(chinese_name) != _normalize_alias(item.name):
        display_name = f"{chinese_name} / {item.name}"
    qualifier = "-".join(part for part in (item.country_code, item.admin1_code, item.admin2_code) if part)
    if qualifier:
        display_name = f"{display_name}（{qualifier}）"
    searchable_aliases = [item.name, item.ascii_name]
    for alias in item.aliases:
        if CJK_RE.search(alias):
            searchable_aliases.extend((alias, TRADITIONAL_TO_SIMPLIFIED.convert(alias)))
    return {
        "locationId": f"geonames:{item.geoname_id}",
        "mode": "overseas",
        "name": chinese_name or item.name,
        "displayName": display_name,
        "countryCode": item.country_code,
        "admin1Code": item.admin1_code,
        "admin2Code": item.admin2_code,
        "admin3Code": item.admin3_code,
        "longitude": item.longitude,
        "latitude": item.latitude,
        "coordinateSystem": "WGS84",
        "timezone": item.timezone,
        "coordinatePrecision": "locality_centroid",
        "source": "geonames",
        "sourceVersion": source_version,
        "population": item.population,
        "aliases": _record_aliases(*searchable_aliases),
    }


def _load_current_divisions(
    path: Path,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], list[dict[str, str]]]:
    """读取固定快照中的现行省、市、区县层级，不保留乡镇和历史撤销代码。"""
    payload = json.loads(path.read_text(encoding="utf-8"))
    provinces: dict[str, dict[str, str]] = {}
    cities: dict[str, dict[str, str]] = {}
    areas: list[dict[str, str]] = []
    for province in payload:
        province_prefix = str(province["code"])
        if province_prefix not in MAINLAND_PROVINCE_PREFIXES:
            continue
        province_name = str(province["name"])
        provinces[province_prefix] = {"code": f"{province_prefix}0000", "name": province_name}
        for city in province.get("children", []):
            city_code = str(city["code"])
            city_name = str(city["name"])
            is_pseudo_city = city_name in PSEUDO_AREA_NAMES
            if not is_pseudo_city:
                cities[city_code] = {"code": f"{city_code}00", "name": city_name}
            for area in city.get("children", []):
                area_code = str(area["code"])
                area_name = str(area["name"])
                if (
                    len(area_code) != 6
                    or area_code == f"{city_code}00"
                    or area_name in PSEUDO_AREA_NAMES
                    or area_code[4:6].startswith("7")
                ):
                    continue
                areas.append(
                    {
                        "code": area_code,
                        "name": area_name,
                        "cityCode": city_code,
                        "cityName": "" if is_pseudo_city else city_name,
                    }
                )
    return provinces, cities, areas


def _domestic_records(
    division_path: Path,
    china_geonames_path: Path,
    *,
    division_version: str,
    geonames_version: str,
) -> list[dict[str, Any]]:
    provinces, cities, areas = _load_current_divisions(division_path)

    geonames, geoname_aliases = _load_china_geonames(china_geonames_path)
    admin1_by_alias: dict[str, list[GeoName]] = defaultdict(list)
    admin2_by_code: dict[str, list[GeoName]] = defaultdict(list)
    admin3_by_parent_alias: dict[tuple[str, str], list[GeoName]] = defaultdict(list)
    places_by_admin1: dict[str, list[GeoName]] = defaultdict(list)
    places_by_admin2: dict[str, list[GeoName]] = defaultdict(list)
    for item in geonames:
        aliases = geoname_aliases[item.geoname_id]
        if item.feature_code == "ADM1":
            for alias in aliases:
                admin1_by_alias[alias].append(item)
        if item.admin2_code:
            admin2_by_code[item.admin2_code].append(item)
            places_by_admin2[item.admin2_code].append(item)
        if item.admin1_code:
            places_by_admin1[item.admin1_code].append(item)
        if item.feature_code in {"ADM3", "PPLA3"} and item.admin2_code:
            for alias in aliases:
                admin3_by_parent_alias[(item.admin2_code, alias)].append(item)

    province_geo: dict[str, GeoName] = {}
    province_admin1: dict[str, str] = {}
    municipality_admin2: dict[str, str] = {}
    for prefix, province in provinces.items():
        alias = _normalize_alias(province["name"])
        candidates = admin1_by_alias.get(alias, []) or admin1_by_alias.get(
            _normalize_alias(_strip_admin_suffix(province["name"])), []
        )
        selected_admin = _choose_geoname(candidates, preferred_features=("ADM1",))
        if selected_admin:
            province_admin1[prefix] = selected_admin.admin1_code
            capital = _choose_geoname(
                places_by_admin1[selected_admin.admin1_code],
                preferred_features=("PPLC", "PPLA", "ADM1"),
            )
            province_geo[prefix] = capital or selected_admin
        if prefix in {"11", "12", "31", "50"}:
            admin2_candidates = [
                item for item in geonames if item.feature_code == "ADM2" and alias in geoname_aliases[item.geoname_id]
            ]
            selected_admin2 = _choose_geoname(admin2_candidates, preferred_features=("ADM2",))
            if selected_admin2:
                municipality_admin2[prefix] = selected_admin2.admin2_code
                province_geo[prefix] = selected_admin2

    city_geo: dict[str, GeoName] = {}
    for code, _city in cities.items():
        candidates = admin2_by_code.get(code, [])
        selected = _choose_geoname(candidates, preferred_features=("PPLA2", "PPLA", "ADM2", "PPLA3"))
        if selected:
            city_geo[code] = selected

    records: list[dict[str, Any]] = []
    source_version = f"administrative-divisions-of-china:{division_version}+geonames:{geonames_version}"

    def add_record(
        *,
        code: str,
        name: str,
        province_name: str,
        city_name: str,
        geo: GeoName,
        precision: str,
        aliases: Iterable[str],
    ) -> None:
        display_name = "".join(_unique_parts(province_name, city_name, name))
        records.append(
            {
                "locationId": f"cn:{code}",
                "mode": "domestic",
                "name": name,
                "displayName": display_name,
                "countryCode": "CN",
                "admin1Code": f"{code[:2]}0000",
                "admin2Code": f"{code[:4]}00" if not code.endswith("0000") else "",
                "admin3Code": code if not code.endswith("00") else "",
                "longitude": geo.longitude,
                "latitude": geo.latitude,
                "coordinateSystem": "WGS84",
                "timezone": "Asia/Shanghai",
                "coordinatePrecision": precision,
                "source": "administrative-divisions-of-china+geonames",
                "sourceVersion": source_version,
                "population": geo.population,
                "aliases": _record_aliases(display_name, name, _strip_admin_suffix(name), extra=aliases),
            }
        )

    for prefix, province in provinces.items():
        geo = province_geo.get(prefix)
        if not geo:
            continue
        add_record(
            code=province["code"],
            name=province["name"],
            province_name=province["name"],
            city_name="",
            geo=geo,
            precision="province_capital",
            aliases=(),
        )

    for code, city in cities.items():
        province = provinces.get(code[:2])
        geo = city_geo.get(code) or province_geo.get(code[:2])
        if not province or not geo:
            continue
        add_record(
            code=city["code"],
            name=city["name"],
            province_name=province["name"],
            city_name=city["name"],
            geo=geo,
            precision="city_centroid" if code in city_geo else "province_capital",
            aliases=(),
        )

    for area in areas:
        code = area["code"]
        province = provinces.get(code[:2])
        city = cities.get(area["cityCode"])
        city_name = area["cityName"] or (city["name"] if city else "")
        if not province:
            continue
        parent_keys = {code[:4]}
        municipality_key = municipality_admin2.get(code[:2])
        if municipality_key:
            parent_keys.add(municipality_key)
        normalized_area = _normalize_alias(area["name"])
        area_candidates: list[GeoName] = []
        for parent_key in parent_keys:
            area_candidates.extend(admin3_by_parent_alias.get((parent_key, normalized_area), []))
            area_candidates.extend(
                admin3_by_parent_alias.get((parent_key, _normalize_alias(_strip_admin_suffix(area["name"]))), [])
            )
        geo = _choose_geoname(area_candidates, preferred_features=("ADM3", "PPLA3"))
        precision = "district_centroid"
        if not geo:
            geo = city_geo.get(code[:4]) or province_geo.get(code[:2])
            precision = "parent_centroid"
        if not geo:
            continue
        add_record(
            code=code,
            name=area["name"],
            province_name=province["name"],
            city_name=city_name,
            geo=geo,
            precision=precision,
            aliases=(
                "".join(_unique_parts(province["name"], area["name"])),
                "".join(_unique_parts(city_name, area["name"])),
            ),
        )
    return records


def _write_catalog(records: Iterable[dict[str, Any]], output_path: Path) -> dict[str, Any]:
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        location_id = record["locationId"]
        if location_id in unique:
            raise RuntimeError(f"地点 ID 重复: {location_id}")
        if not record["timezone"]:
            raise RuntimeError(f"地点缺少 IANA 时区: {location_id}")
        unique[location_id] = record

    display_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in unique.values():
        display_groups[(record["mode"], record["displayName"])].append(record)
    for (_mode, original_display_name), values in display_groups.items():
        if len(values) <= 1:
            continue
        for record in values:
            stable_code = record["admin3Code"] or record["admin2Code"] or record["locationId"]
            record["displayName"] = f"{original_display_name}（{stable_code}）"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as text:
                for location_id in sorted(unique):
                    text.write(
                        json.dumps(unique[location_id], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    )
                    text.write("\n")

    mode_counts: dict[str, int] = defaultdict(int)
    precision_counts: dict[str, int] = defaultdict(int)
    timezone_ids: set[str] = set()
    alias_count = 0
    for record in unique.values():
        mode_counts[record["mode"]] += 1
        precision_counts[record["coordinatePrecision"]] += 1
        timezone_ids.add(record["timezone"])
        alias_count += len(record["aliases"])
    return {
        "recordCount": len(unique),
        "aliasCount": alias_count,
        "modeCounts": dict(sorted(mode_counts.items())),
        "coordinatePrecisionCounts": dict(sorted(precision_counts.items())),
        "timezoneCount": len(timezone_ids),
        "bytes": output_path.stat().st_size,
        "sha256": _sha256(output_path),
    }


def build(source_dir: Path, *, download: bool) -> dict[str, Any]:
    source_lock = json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))
    sources = _materialize_sources(source_dir, source_lock, download=download)
    source_versions = {source["id"]: source["version"] for source in source_lock["sources"]}

    domestic = _domestic_records(
        sources["administrative-divisions-of-china"],
        sources["geonames-cn"],
        division_version=source_versions["administrative-divisions-of-china"],
        geonames_version=source_versions["geonames-cn"],
    )
    global_records = [
        _global_record(item, source_versions["geonames-cities1000"])
        for item in _read_geonames_zip(sources["geonames-cities1000"])
        if item.country_code != "CN"
    ]
    output = _write_catalog([*domestic, *global_records], OUTPUT_PATH)
    manifest = {
        "schemaVersion": 1,
        "dataProduct": "fatecat-location-catalog",
        "coordinateSystem": "WGS84",
        "runtimeFormat": "gzip-compressed NDJSON; runtime builds an indexed SQLite cache",
        "builderDependencies": {"opencc-python-reimplemented": "0.1.7"},
        "output": {"path": str(OUTPUT_PATH.relative_to(REPO_ROOT)), **output},
        "sources": source_lock["sources"],
        "licenses": ["CC-BY-4.0", "WTFPL"],
        "attributionRequired": True,
        "qualityBoundary": (
            "国内行政区身份来自 Administrative-divisions-of-China 的固定现行快照；坐标来自 GeoNames。"
            "district_centroid 为区县级中心点，parent_centroid 为透明标记的上级中心点回退。"
        ),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 FateCat 出生地点目录")
    parser.add_argument("--source-dir", type=Path, help="原始来源文件目录；默认使用临时目录")
    parser.add_argument("--download", action="store_true", help="缺少来源文件时按锁定 URL 下载")
    args = parser.parse_args()

    if args.source_dir:
        manifest = build(args.source_dir.resolve(), download=args.download)
    else:
        with tempfile.TemporaryDirectory(prefix="fatecat-location-sources-") as temp_dir:
            manifest = build(Path(temp_dir), download=True)
    print(json.dumps(manifest["output"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
