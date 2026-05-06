-- 八字排盘数据库 v2
-- SQLite 3

CREATE TABLE IF NOT EXISTS records (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       TEXT NOT NULL,
    biz_type      TEXT NOT NULL,
    -- 用户输入
    name          TEXT,
    gender        TEXT NOT NULL,
    calendar_type TEXT NOT NULL DEFAULT 'solar',
    birth_date    TEXT NOT NULL,
    birth_time    TEXT NOT NULL,
    birth_place   TEXT,
    longitude     REAL DEFAULT 116.4,
    latitude      REAL DEFAULT 39.9,
    -- 配置参数
    dst           INTEGER DEFAULT 0,
    true_solar    INTEGER DEFAULT 1,
    early_zi      INTEGER DEFAULT 0,
    -- 结果
    biz_data      TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_records_user ON records(user_id);
CREATE INDEX IF NOT EXISTS idx_records_user_biz ON records(user_id, biz_type);
CREATE INDEX IF NOT EXISTS idx_records_birth ON records(birth_date);
