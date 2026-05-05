"""数据库操作模块"""

import json
import sqlite3

from _paths import BAZI_DB_PATH, BAZI_SCHEMA_PATH

DB_PATH = BAZI_DB_PATH
SCHEMA_PATH = BAZI_SCHEMA_PATH
_initialized = False


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表结构"""
    conn = get_conn()
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def ensure_db():
    """确保数据库已初始化（自动检测，启动时调用）"""
    global _initialized
    if _initialized:
        return

    # 确保目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 检查表是否存在
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='records'")
    exists = cur.fetchone() is not None
    conn.close()

    if not exists:
        print("[DB] 初始化数据库表...")
        init_db()
        print("[DB] 数据库初始化完成")

    _initialized = True


def save_record(
    user_id: str,
    biz_type: str,
    gender: str,
    birth_date: str,
    birth_time: str,
    biz_data: dict,
    name: str = None,
    calendar_type: str = "solar",
    birth_place: str = None,
    longitude: float = 116.4,
    latitude: float = 39.9,
    dst: int = 0,
    true_solar: int = 1,
    early_zi: int = 0,
) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO records (user_id, biz_type, name, gender, calendar_type,
            birth_date, birth_time, birth_place, longitude, latitude,
            dst, true_solar, early_zi, biz_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            user_id,
            biz_type,
            name,
            gender,
            calendar_type,
            birth_date,
            birth_time,
            birth_place,
            longitude,
            latitude,
            dst,
            true_solar,
            early_zi,
            json.dumps(biz_data, ensure_ascii=False, default=str),
        ),
    )
    rid = cur.lastrowid
    conn.commit()
    conn.close()
    return rid


def get_record(record_id: int) -> dict | None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    row = cur.fetchone()
    conn.close()
    return _row_to_dict(row) if row else None


def get_user_records(user_id: str, biz_type: str = None, limit: int = 10) -> list[dict]:
    conn = get_conn()
    cur = conn.cursor()
    if biz_type:
        cur.execute(
            "SELECT * FROM records WHERE user_id = ? AND biz_type = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, biz_type, limit),
        )
    else:
        cur.execute("SELECT * FROM records WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def delete_record(record_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE id = ?", (record_id,))
    ok = cur.rowcount > 0
    conn.commit()
    conn.close()
    return ok


def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "userId": row["user_id"],
        "bizType": row["biz_type"],
        "input": {
            "name": row["name"],
            "gender": row["gender"],
            "calendarType": row["calendar_type"],
            "birthDate": row["birth_date"],
            "birthTime": row["birth_time"],
            "birthPlace": row["birth_place"],
            "longitude": row["longitude"],
            "latitude": row["latitude"],
            "dst": row["dst"],
            "trueSolar": row["true_solar"],
            "earlyZi": row["early_zi"],
        },
        "bizData": json.loads(row["biz_data"]),
        "createdAt": row["created_at"],
    }


if __name__ == "__main__":
    init_db()
    print("数据库初始化完成")
