"""出生地点目录的只读运行时索引。

canonical 数据产品保持为可审计的压缩 NDJSON；本模块只在运行态生成 SQLite
查询索引。SQLite 文件可随时删除重建，不属于仓库资产或用户数据。
"""

from __future__ import annotations

import fcntl
import gzip
import hashlib
import json
import os
import sqlite3
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from _paths import LOCATION_CATALOG_MANIFEST, LOCATION_CATALOG_PATH, LOCATION_INDEX_DIR, LOCATION_INDEX_PATH


def normalize_alias(value: str) -> str:
    """生成跨 Web/API 一致的地点检索键。"""
    normalized = unicodedata.normalize("NFKC", value or "").strip().casefold()
    return "".join(character for character in normalized if not character.isspace() and character not in "'’·-")


def normalize_fuzzy_alias(value: str) -> str:
    """移除行政层级后缀，支持“陕西西安”“西安长安”等连续关键词。"""
    normalized = normalize_alias(value)
    for suffix in ("特别行政区", "自治区", "自治州", "自治县", "地区", "省", "市", "区", "县", "盟", "旗"):
        normalized = normalized.replace(suffix, "")
    return normalized


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class CatalogLocation:
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
    population: int

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
            "population": self.population,
        }


_LOCATION_COLUMNS = """
l.location_id AS location_id, l.mode AS mode, l.name AS name, l.display_name AS display_name,
l.country_code AS country_code, l.admin1_code AS admin1_code, l.admin2_code AS admin2_code,
l.admin3_code AS admin3_code, l.longitude AS longitude, l.latitude AS latitude,
l.coordinate_system AS coordinate_system, l.timezone AS timezone,
l.coordinate_precision AS coordinate_precision, l.source AS source,
l.source_version AS source_version, l.population AS population
"""


def _row_to_location(row: sqlite3.Row) -> CatalogLocation:
    return CatalogLocation(
        location_id=row["location_id"],
        mode=row["mode"],
        name=row["name"],
        display_name=row["display_name"],
        country_code=row["country_code"],
        admin1_code=row["admin1_code"],
        admin2_code=row["admin2_code"],
        admin3_code=row["admin3_code"],
        longitude=float(row["longitude"]),
        latitude=float(row["latitude"]),
        coordinate_system=row["coordinate_system"],
        timezone=row["timezone"],
        coordinate_precision=row["coordinate_precision"],
        source=row["source"],
        source_version=row["source_version"],
        population=int(row["population"]),
    )


class LocationCatalog:
    """压缩地点数据产品上的线程安全只读查询门面。"""

    def __init__(self) -> None:
        manifest = json.loads(LOCATION_CATALOG_MANIFEST.read_text(encoding="utf-8"))
        output = manifest["output"]
        self._expected_hash = str(output["sha256"])
        self._expected_count = int(output["recordCount"])
        if _sha256(LOCATION_CATALOG_PATH) != self._expected_hash:
            raise RuntimeError("地点目录数据产品 hash 与 manifest 不一致")

    def ensure_index(self) -> Path:
        LOCATION_INDEX_DIR.mkdir(parents=True, exist_ok=True)
        lock_path = LOCATION_INDEX_DIR / ".location-catalog.lock"
        with lock_path.open("a+b") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            if not self._index_is_current():
                self._build_index()
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
        return LOCATION_INDEX_PATH

    def _index_is_current(self) -> bool:
        if not LOCATION_INDEX_PATH.exists():
            return False
        try:
            with sqlite3.connect(LOCATION_INDEX_PATH) as connection:
                metadata = dict(connection.execute("SELECT key, value FROM metadata").fetchall())
                count = int(connection.execute("SELECT COUNT(*) FROM locations").fetchone()[0])
            return (
                metadata.get("catalog_sha256") == self._expected_hash
                and metadata.get("schema_version") == "2"
                and count == self._expected_count
            )
        except (OSError, sqlite3.Error, TypeError, ValueError):
            return False

    def _build_index(self) -> None:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix="location-catalog-",
            suffix=".sqlite3",
            dir=LOCATION_INDEX_DIR,
        )
        os.close(descriptor)
        temporary_path = Path(temporary_name)
        try:
            with sqlite3.connect(temporary_path) as connection:
                connection.executescript(
                    """
                    PRAGMA journal_mode=OFF;
                    PRAGMA synchronous=OFF;
                    PRAGMA temp_store=MEMORY;
                    CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    CREATE TABLE locations (
                        location_id TEXT PRIMARY KEY,
                        mode TEXT NOT NULL,
                        name TEXT NOT NULL,
                        display_name TEXT NOT NULL,
                        country_code TEXT NOT NULL,
                        admin1_code TEXT NOT NULL,
                        admin2_code TEXT NOT NULL,
                        admin3_code TEXT NOT NULL,
                        longitude REAL NOT NULL,
                        latitude REAL NOT NULL,
                        coordinate_system TEXT NOT NULL,
                        timezone TEXT NOT NULL,
                        coordinate_precision TEXT NOT NULL,
                        source TEXT NOT NULL,
                        source_version TEXT NOT NULL,
                        population INTEGER NOT NULL
                    );
                    CREATE TABLE aliases (
                        location_id TEXT NOT NULL,
                        alias TEXT NOT NULL,
                        normalized_alias TEXT NOT NULL,
                        fuzzy_alias TEXT NOT NULL,
                        PRIMARY KEY (location_id, normalized_alias),
                        FOREIGN KEY (location_id) REFERENCES locations(location_id)
                    );
                    """
                )
                location_rows: list[tuple[object, ...]] = []
                alias_rows: list[tuple[str, str, str, str]] = []
                with gzip.open(LOCATION_CATALOG_PATH, "rt", encoding="utf-8") as handle:
                    for line in handle:
                        record = json.loads(line)
                        location_id = str(record["locationId"])
                        location_rows.append(
                            (
                                location_id,
                                record["mode"],
                                record["name"],
                                record["displayName"],
                                record["countryCode"],
                                record["admin1Code"],
                                record["admin2Code"],
                                record["admin3Code"],
                                record["longitude"],
                                record["latitude"],
                                record["coordinateSystem"],
                                record["timezone"],
                                record["coordinatePrecision"],
                                record["source"],
                                record["sourceVersion"],
                                record["population"],
                            )
                        )
                        alias_rows.extend(
                            (location_id, alias, normalize_alias(alias), normalize_fuzzy_alias(alias))
                            for alias in record.get("aliases", [])
                        )
                        if len(location_rows) >= 5000:
                            self._flush_rows(connection, location_rows, alias_rows)
                self._flush_rows(connection, location_rows, alias_rows)
                connection.executescript(
                    """
                    CREATE INDEX aliases_normalized_idx ON aliases(normalized_alias, location_id);
                    CREATE INDEX aliases_fuzzy_idx ON aliases(fuzzy_alias, location_id);
                    CREATE INDEX locations_mode_admin_idx ON locations(mode, admin1_code, admin2_code, admin3_code);
                    CREATE INDEX locations_country_idx ON locations(country_code, population DESC);
                    """
                )
                connection.executemany(
                    "INSERT INTO metadata(key, value) VALUES (?, ?)",
                    (
                        ("catalog_sha256", self._expected_hash),
                        ("record_count", str(self._expected_count)),
                        ("schema_version", "2"),
                    ),
                )
                connection.commit()
            os.replace(temporary_path, LOCATION_INDEX_PATH)
        finally:
            temporary_path.unlink(missing_ok=True)

    @staticmethod
    def _flush_rows(
        connection: sqlite3.Connection,
        location_rows: list[tuple[object, ...]],
        alias_rows: list[tuple[str, str, str, str]],
    ) -> None:
        if location_rows:
            connection.executemany(
                "INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                location_rows,
            )
            connection.executemany("INSERT OR IGNORE INTO aliases VALUES (?, ?, ?, ?)", alias_rows)
            location_rows.clear()
            alias_rows.clear()

    def _connect(self) -> sqlite3.Connection:
        path = self.ensure_index()
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        return connection

    def get(self, location_id: str) -> CatalogLocation | None:
        with self._connect() as connection:
            row = connection.execute(
                f"SELECT {_LOCATION_COLUMNS} FROM locations l WHERE l.location_id = ?",
                (location_id,),
            ).fetchone()
        return _row_to_location(row) if row else None

    def exact(self, query: str, *, mode: str | None = None, limit: int = 50) -> list[CatalogLocation]:
        normalized = normalize_alias(query)
        if not normalized:
            return []
        mode_clause = "AND l.mode = ?" if mode else ""
        params: list[object] = [normalized]
        if mode:
            params.append(mode)
        params.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT {_LOCATION_COLUMNS}
                FROM aliases a
                JOIN locations l ON l.location_id = a.location_id
                WHERE a.normalized_alias = ? {mode_clause}
                ORDER BY CASE l.mode WHEN 'domestic' THEN 0 ELSE 1 END,
                         l.population DESC, l.display_name, l.location_id
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [_row_to_location(row) for row in rows]

    def search(self, query: str, *, mode: str | None = None, limit: int = 20) -> list[CatalogLocation]:
        normalized = normalize_alias(query)
        if not normalized:
            return []
        mode_clause = "AND l.mode = ?" if mode else ""
        fuzzy = normalize_fuzzy_alias(query)
        domestic_fuzzy = mode == "domestic" and bool(fuzzy)
        fuzzy_clause = "OR instr(a.fuzzy_alias, ?) > 0" if domestic_fuzzy else ""
        params: list[object] = [
            normalized,
            normalized,
            f"{normalized}\U0010ffff",
            normalized,
            f"{normalized}\U0010ffff",
        ]
        if domestic_fuzzy:
            params.append(fuzzy)
        if mode:
            params.append(mode)
        params.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT {_LOCATION_COLUMNS},
                       MIN(CASE
                               WHEN a.normalized_alias = ? THEN 0
                               WHEN a.normalized_alias >= ? AND a.normalized_alias < ? THEN 1
                               ELSE 2
                           END) AS match_rank
                FROM aliases a
                JOIN locations l ON l.location_id = a.location_id
                WHERE ((a.normalized_alias >= ? AND a.normalized_alias < ?) {fuzzy_clause}) {mode_clause}
                GROUP BY l.location_id
                ORDER BY match_rank,
                         CASE l.mode WHEN 'domestic' THEN 0 ELSE 1 END,
                         l.population DESC, l.display_name, l.location_id
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [_row_to_location(row) for row in rows]

    def domestic_option_values(self) -> tuple[str, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT display_name FROM locations WHERE mode = 'domestic' ORDER BY display_name"
            ).fetchall()
        return tuple(str(row[0]) for row in rows)

    def status(self) -> dict[str, object]:
        path = self.ensure_index()
        with self._connect() as connection:
            counts = dict(connection.execute("SELECT mode, COUNT(*) FROM locations GROUP BY mode").fetchall())
            timezone_count = int(connection.execute("SELECT COUNT(DISTINCT timezone) FROM locations").fetchone()[0])
        return {
            "catalogSha256": self._expected_hash,
            "recordCount": self._expected_count,
            "modeCounts": counts,
            "timezoneCount": timezone_count,
            "runtimeIndexBytes": path.stat().st_size,
        }


_CATALOG: LocationCatalog | None = None


def get_catalog() -> LocationCatalog:
    global _CATALOG
    if _CATALOG is None:
        _CATALOG = LocationCatalog()
    return _CATALOG


__all__ = [
    "CatalogLocation",
    "LocationCatalog",
    "get_catalog",
    "normalize_alias",
    "normalize_fuzzy_alias",
]
