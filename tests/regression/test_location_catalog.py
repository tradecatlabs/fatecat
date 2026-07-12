from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "domains" / "fate-analysis" / "data-products" / "locations"
CATALOG_PATH = DATA_DIR / "location_catalog.ndjson.gz"
MANIFEST_PATH = DATA_DIR / "manifest.json"
SOURCE_LOCK_PATH = DATA_DIR / "sources.lock.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_location_catalog_matches_manifest_and_source_lock():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source_lock = json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))

    assert manifest["coordinateSystem"] == "WGS84"
    assert manifest["output"]["sha256"] == _sha256(CATALOG_PATH)
    assert manifest["output"]["bytes"] == CATALOG_PATH.stat().st_size
    assert manifest["sources"] == source_lock["sources"]
    assert manifest["licenses"] == ["CC-BY-4.0", "WTFPL"]
    assert manifest["attributionRequired"] is True


def test_location_catalog_has_unique_valid_records_and_current_admin_codes():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    ids: set[str] = set()
    timezones: set[str] = set()
    modes: dict[str, int] = {}
    precision: dict[str, int] = {}
    alias_count = 0

    with gzip.open(CATALOG_PATH, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = json.loads(line)
            location_id = record["locationId"]
            assert location_id not in ids, f"duplicate locationId at line {line_number}: {location_id}"
            ids.add(location_id)
            assert record["coordinateSystem"] == "WGS84"
            assert -180 <= record["longitude"] <= 180
            assert -90 <= record["latitude"] <= 90
            assert record["timezone"]
            assert record["coordinatePrecision"]
            assert record["source"]
            assert record["sourceVersion"]
            assert record["aliases"]
            assert len(record["aliases"]) == len(set(record["aliases"]))
            alias_count += len(record["aliases"])
            timezones.add(record["timezone"])
            modes[record["mode"]] = modes.get(record["mode"], 0) + 1
            key = record["coordinatePrecision"]
            precision[key] = precision.get(key, 0) + 1

    for timezone in timezones:
        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError as exc:
            raise AssertionError(f"unknown IANA timezone: {timezone}") from exc

    assert len(ids) == manifest["output"]["recordCount"]
    assert alias_count == manifest["output"]["aliasCount"]
    assert modes == manifest["output"]["modeCounts"]
    assert precision == manifest["output"]["coordinatePrecisionCounts"]
    assert len(timezones) == manifest["output"]["timezoneCount"]
    assert "cn:110000" in ids
    assert "cn:110101" in ids
    assert "cn:110228" not in ids
    assert "cn:110229" not in ids
    assert "cn:350403" not in ids
    assert "cn:350404" in ids
    assert "geonames:5128581" in ids


def test_location_catalog_builder_and_runtime_index_have_separate_ownership():
    builder = (ROOT / "scripts" / "build-location-catalog.py").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "sources.lock.json" in builder
    assert "sha256" in builder
    assert "location_catalog.ndjson.gz" in builder
    assert "infra/runtime/local-state/database/locations/" in gitignore
    assert not (DATA_DIR.parent / "china_coordinates.csv").exists()
