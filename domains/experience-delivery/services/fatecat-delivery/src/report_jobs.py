"""报告生成任务队列。

该模块负责报告任务生命周期：排队、执行、状态查询、TTL 过期、事件历史、指标和可选持久化。
默认仍使用单进程内存队列；自部署可以启用 SQLite backend 获得本地跨 manager 查询能力。
SQLite backend 不是分布式队列，不负责多副本抢任务或跨进程继续执行未完成 callable。
"""

from __future__ import annotations

import json
import logging
import secrets
import sqlite3
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from queue import Full, Queue
from threading import Event, Lock, Thread
from typing import Any, Literal
from urllib.parse import urlparse

from utils.timezone import now_cn
from webhook_config_store import EncryptedWebhookDeliveryConfig

logger = logging.getLogger(__name__)

ReportJobStatus = Literal["queued", "running", "succeeded", "failed", "expired", "cancelled"]
ReportJobWebhookOutboxStatus = Literal["pending", "succeeded", "failed"]
REPORT_JOB_WEBHOOK_EVENT_TYPE = "report_job.terminal"


class ReportJobQueueFull(RuntimeError):
    """报告任务队列已满。"""


class ReportJobNotFound(KeyError):
    """报告任务不存在或已清理。"""


class ReportJobNonRetryableError(RuntimeError):
    """报告任务不可重试错误。"""


class ReportJobTimeoutError(TimeoutError):
    """报告任务 attempt 超时。"""


@dataclass(frozen=True)
class ReportJobExecutionPolicy:
    max_attempts: int = 1
    attempt_timeout_seconds: float | None = None
    retry_backoff_seconds: float = 0.0
    non_retryable_exceptions: tuple[type[BaseException], ...] = (ReportJobNonRetryableError,)

    def normalized(self) -> ReportJobExecutionPolicy:
        timeout = self.attempt_timeout_seconds
        return ReportJobExecutionPolicy(
            max_attempts=max(1, int(self.max_attempts)),
            attempt_timeout_seconds=float(timeout) if timeout and timeout > 0 else None,
            retry_backoff_seconds=max(0.0, float(self.retry_backoff_seconds)),
            non_retryable_exceptions=self.non_retryable_exceptions or (ReportJobNonRetryableError,),
        )


@dataclass(frozen=True)
class ReportJobWebhookPolicy:
    max_attempts: int = 1
    retry_backoff_seconds: float = 0.0

    def normalized(self) -> ReportJobWebhookPolicy:
        return ReportJobWebhookPolicy(
            max_attempts=max(1, int(self.max_attempts)),
            retry_backoff_seconds=max(0.0, float(self.retry_backoff_seconds)),
        )


@dataclass(frozen=True)
class ReportJobEvent:
    event_id: str
    job_id: str
    event_type: str
    status: ReportJobStatus
    created_at: str
    message: str | None
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ReportJobWebhookOutboxRecord:
    outbox_id: str
    job_id: str
    event_type: str
    job_status: ReportJobStatus
    status: ReportJobWebhookOutboxStatus
    attempts: int
    max_attempts: int
    signature_mode: str
    target_host_hash: str | None
    created_at: str
    updated_at: str
    completed_at: str | None
    last_error_type: str | None
    result_status_code: int | None


@dataclass(frozen=True)
class ReportJobSnapshot:
    job_id: str
    kind: str
    status: ReportJobStatus
    report_system: str
    created_at: str
    expires_at: str
    started_at: str | None
    finished_at: str | None
    queue_position: int | None
    error: str | None
    result: Any | None
    input_summary: dict[str, Any]
    idempotency_key: str | None
    webhook_enabled: bool
    webhook_signature: str
    attempts: int
    max_attempts: int
    attempt_timeout_seconds: float | None
    retry_backoff_seconds: float
    events: tuple[ReportJobEvent, ...]
    callback_outbox: tuple[ReportJobWebhookOutboxRecord, ...]


ReportJobWebhookDispatcher = Callable[[ReportJobSnapshot, Any], Any]
ReportJobTaskFactory = Callable[[dict[str, Any]], Callable[[], Any]]


@dataclass
class _ReportJob:
    job_id: str
    kind: str
    report_system: str
    task: Callable[[], Any] | None
    input_summary: dict[str, Any]
    idempotency_key: str | None
    webhook_config: Any | None
    created_monotonic: float
    expires_monotonic: float
    created_at: str
    expires_at: str
    status: ReportJobStatus = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    error: str | None = None
    result: Any | None = None
    attempts: int = 0
    max_attempts: int = 1
    attempt_timeout_seconds: float | None = None
    retry_backoff_seconds: float = 0.0
    non_retryable_exceptions: tuple[type[BaseException], ...] = (ReportJobNonRetryableError,)
    task_payload: dict[str, Any] | None = None


class ReportJobStore:
    """报告任务状态存储接口。"""

    backend_name = "memory"

    def load_jobs(self) -> list[_ReportJob]:
        return []

    def save_job(self, _job: _ReportJob) -> None:
        return

    def claim_job_for_execution(
        self,
        job: _ReportJob,
        *,
        lease_owner: str,
        lease_seconds: float,
    ) -> _ReportJob | None:
        owner = str(lease_owner).strip()
        if not owner or job.status not in {"queued", "running"}:
            return None
        return job

    def release_job_execution_lease(self, _job_id: str, *, lease_owner: str) -> None:
        return

    def load_job_events(self, _job_id: str) -> list[ReportJobEvent]:
        return []

    def append_job_event(self, _event: ReportJobEvent) -> None:
        return

    def load_webhook_outbox_records(self, _job_id: str) -> list[ReportJobWebhookOutboxRecord]:
        return []

    def load_redeliverable_webhook_outbox_records(self) -> list[ReportJobWebhookOutboxRecord]:
        return []

    def save_webhook_outbox_record(self, _record: ReportJobWebhookOutboxRecord) -> None:
        return

    def claim_webhook_outbox_record(
        self,
        record: ReportJobWebhookOutboxRecord,
        *,
        lease_owner: str,
        lease_seconds: float,
    ) -> ReportJobWebhookOutboxRecord | None:
        return record

    def release_webhook_outbox_record(self, _outbox_id: str, *, lease_owner: str) -> None:
        return

    def has_webhook_delivery_config_store(self) -> bool:
        return False

    def save_webhook_delivery_config(
        self,
        _record: ReportJobWebhookOutboxRecord,
        _webhook_config: Any,
    ) -> None:
        return

    def load_webhook_delivery_config(self, _record: ReportJobWebhookOutboxRecord) -> Any | None:
        return None

    def delete_webhook_delivery_config(self, _outbox_id: str) -> None:
        return

    def rotate_webhook_delivery_configs(self) -> int:
        return 0

    def count_webhook_delivery_configs(self) -> int:
        return 0


class InMemoryReportJobStore(ReportJobStore):
    """默认单进程事件存储；任务主体状态仍由 manager 内存字典持有。"""

    backend_name = "memory"

    def __init__(self) -> None:
        self._events: dict[str, list[ReportJobEvent]] = {}
        self._lock = Lock()

    def load_job_events(self, job_id: str) -> list[ReportJobEvent]:
        with self._lock:
            return list(self._events.get(job_id, ()))

    def append_job_event(self, event: ReportJobEvent) -> None:
        with self._lock:
            self._events.setdefault(event.job_id, []).append(event)


POSTGRES_REPORT_JOB_SCHEMA_SQL: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS report_jobs (
        job_id TEXT PRIMARY KEY,
        kind TEXT NOT NULL,
        status TEXT NOT NULL,
        report_system TEXT NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        started_at TEXT,
        finished_at TEXT,
        error TEXT,
        result_json TEXT,
        input_summary_json TEXT NOT NULL,
        task_payload_json TEXT,
        idempotency_key TEXT,
        attempts INTEGER NOT NULL DEFAULT 0,
        max_attempts INTEGER NOT NULL DEFAULT 1,
        attempt_timeout_seconds DOUBLE PRECISION,
        retry_backoff_seconds DOUBLE PRECISION NOT NULL DEFAULT 0,
        lease_owner TEXT,
        lease_acquired_at TEXT,
        lease_expires_at TEXT,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_report_jobs_idempotency
    ON report_jobs(idempotency_key)
    WHERE idempotency_key IS NOT NULL
    """,
    "CREATE INDEX IF NOT EXISTS idx_report_jobs_status ON report_jobs(status)",
    "CREATE INDEX IF NOT EXISTS idx_report_jobs_expires_at ON report_jobs(expires_at)",
    """
    CREATE TABLE IF NOT EXISTS report_job_events (
        sequence BIGSERIAL PRIMARY KEY,
        event_id TEXT NOT NULL UNIQUE,
        job_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        message TEXT,
        metadata_json TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_report_job_events_job_sequence ON report_job_events(job_id, sequence)",
    """
    CREATE TABLE IF NOT EXISTS report_job_webhook_outbox (
        outbox_id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        job_status TEXT NOT NULL,
        status TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 0,
        max_attempts INTEGER NOT NULL DEFAULT 1,
        signature_mode TEXT NOT NULL,
        target_host_hash TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        completed_at TEXT,
        last_error_type TEXT,
        result_status_code INTEGER,
        lease_owner TEXT,
        lease_acquired_at TEXT,
        lease_expires_at TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_job ON report_job_webhook_outbox(job_id)",
    "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_status ON report_job_webhook_outbox(status)",
    """
    CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_lease
    ON report_job_webhook_outbox(status, lease_expires_at)
    """,
    """
    CREATE TABLE IF NOT EXISTS report_job_webhook_delivery_config (
        outbox_id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        cipher_suite TEXT NOT NULL,
        key_id TEXT NOT NULL,
        ciphertext TEXT NOT NULL,
        target_host_hash TEXT,
        signature_mode TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        rotated_at TEXT
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_report_job_webhook_delivery_config_job
    ON report_job_webhook_delivery_config(job_id)
    """,
)

POSTGRES_REPORT_JOB_LEASE_MIGRATION_SQL: tuple[str, ...] = (
    "ALTER TABLE report_jobs ADD COLUMN IF NOT EXISTS lease_owner TEXT",
    "ALTER TABLE report_jobs ADD COLUMN IF NOT EXISTS lease_acquired_at TEXT",
    "ALTER TABLE report_jobs ADD COLUMN IF NOT EXISTS lease_expires_at TEXT",
)

POSTGRES_REPORT_JOB_LEASE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_report_jobs_execution_lease
ON report_jobs(status, lease_expires_at)
"""

POSTGRES_JOB_EXECUTION_CLAIM_SQL = """
UPDATE report_jobs
SET lease_owner = %(lease_owner)s,
    lease_acquired_at = %(now)s,
    lease_expires_at = %(lease_expires_at)s,
    status = CASE WHEN status = 'queued' THEN 'running' ELSE status END,
    started_at = COALESCE(started_at, %(now)s),
    updated_at = %(now)s
WHERE job_id = %(job_id)s
  AND status IN ('queued', 'running')
  AND (
    lease_expires_at IS NULL
    OR lease_expires_at <= %(now)s
    OR lease_owner = %(lease_owner)s
  )
RETURNING job_id, kind, status, report_system, created_at, expires_at,
          started_at, finished_at, error, result_json, input_summary_json,
          idempotency_key, attempts, max_attempts, attempt_timeout_seconds,
          retry_backoff_seconds, task_payload_json
"""

POSTGRES_WEBHOOK_OUTBOX_CLAIM_SQL = """
UPDATE report_job_webhook_outbox
SET lease_owner = %(lease_owner)s,
    lease_acquired_at = %(now)s,
    lease_expires_at = %(lease_expires_at)s,
    updated_at = %(now)s
WHERE outbox_id = %(outbox_id)s
  AND event_type = %(event_type)s
  AND status IN ('pending', 'failed')
  AND (
    lease_expires_at IS NULL
    OR lease_expires_at <= %(now)s
    OR lease_owner = %(lease_owner)s
  )
RETURNING outbox_id, job_id, event_type, job_status, status, attempts,
          max_attempts, signature_mode, target_host_hash, created_at,
          updated_at, completed_at, last_error_type, result_status_code
"""

POSTGRES_REPORT_JOB_REQUIRED_TABLES = (
    "report_jobs",
    "report_job_events",
    "report_job_webhook_outbox",
    "report_job_webhook_delivery_config",
)

POSTGRES_REPORT_JOB_REQUIRED_INDEXES = (
    "idx_report_jobs_idempotency",
    "idx_report_jobs_status",
    "idx_report_jobs_expires_at",
    "idx_report_jobs_execution_lease",
    "idx_report_job_events_job_sequence",
    "idx_report_job_webhook_outbox_job",
    "idx_report_job_webhook_outbox_status",
    "idx_report_job_webhook_outbox_lease",
    "idx_report_job_webhook_delivery_config_job",
)


def postgres_report_job_schema_sql() -> tuple[str, ...]:
    """返回 Postgres ReportJobStore schema 语句；不包含 DSN 或外部连接信息。"""

    return POSTGRES_REPORT_JOB_SCHEMA_SQL


def _build_postgres_connect_factory(database_url: str) -> Callable[[], Any]:
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "FATE_REPORT_JOB_STORE=postgres 需要安装可选依赖 psycopg；"
            "请安装 fatecat[postgres] 或 psycopg[binary]，并通过 FATE_REPORT_JOB_DATABASE_URL 提供 DSN。"
        ) from exc

    def connect() -> Any:
        return psycopg.connect(database_url, row_factory=dict_row)

    return connect


class SQLiteReportJobStore(ReportJobStore):
    """SQLite 报告任务状态存储。

    该 backend 只持久化任务状态、结果、幂等索引和事件历史；callable 不可序列化，因此重建 manager
    时会把遗留的 queued/running 任务标记为 failed，避免假装任务仍可继续执行。
    """

    backend_name = "sqlite"

    def __init__(self, db_path: str | Path, *, webhook_config_codec: Any | None = None) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.webhook_config_codec = webhook_config_codec
        self._lock = Lock()
        self._init_schema()

    def load_jobs(self) -> list[_ReportJob]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT job_id, kind, status, report_system, created_at, expires_at,
                       started_at, finished_at, error, result_json, input_summary_json,
                       idempotency_key, attempts, max_attempts, attempt_timeout_seconds,
                       retry_backoff_seconds, task_payload_json
                FROM report_jobs
                ORDER BY created_at ASC
                """
            ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def save_job(self, job: _ReportJob) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_jobs (
                    job_id, kind, status, report_system, created_at, expires_at,
                    started_at, finished_at, error, result_json, input_summary_json,
                    task_payload_json, idempotency_key, attempts, max_attempts,
                    attempt_timeout_seconds, retry_backoff_seconds, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    kind=excluded.kind,
                    status=excluded.status,
                    report_system=excluded.report_system,
                    created_at=excluded.created_at,
                    expires_at=excluded.expires_at,
                    started_at=excluded.started_at,
                    finished_at=excluded.finished_at,
                    error=excluded.error,
                    result_json=excluded.result_json,
                    input_summary_json=excluded.input_summary_json,
                    task_payload_json=excluded.task_payload_json,
                    idempotency_key=excluded.idempotency_key,
                    attempts=excluded.attempts,
                    max_attempts=excluded.max_attempts,
                    attempt_timeout_seconds=excluded.attempt_timeout_seconds,
                    retry_backoff_seconds=excluded.retry_backoff_seconds,
                    updated_at=excluded.updated_at
                """,
                (
                    job.job_id,
                    job.kind,
                    job.status,
                    job.report_system,
                    job.created_at,
                    job.expires_at,
                    job.started_at,
                    job.finished_at,
                    job.error,
                    _json_dumps(job.result),
                    _json_dumps(job.input_summary),
                    _json_dumps(job.task_payload),
                    job.idempotency_key,
                    job.attempts,
                    job.max_attempts,
                    job.attempt_timeout_seconds,
                    job.retry_backoff_seconds,
                    now_cn().isoformat(),
                ),
            )

    def load_job_events(self, job_id: str) -> list[ReportJobEvent]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT event_id, job_id, event_type, status, created_at, message, metadata_json
                FROM report_job_events
                WHERE job_id = ?
                ORDER BY sequence ASC
                """,
                (job_id,),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def append_job_event(self, event: ReportJobEvent) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO report_job_events (
                    event_id, job_id, event_type, status, created_at, message, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.job_id,
                    event.event_type,
                    event.status,
                    event.created_at,
                    event.message,
                    _json_dumps(event.metadata),
                ),
            )

    def load_webhook_outbox_records(self, job_id: str) -> list[ReportJobWebhookOutboxRecord]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, job_id, event_type, job_status, status, attempts,
                       max_attempts, signature_mode, target_host_hash, created_at,
                       updated_at, completed_at, last_error_type, result_status_code
                FROM report_job_webhook_outbox
                WHERE job_id = ?
                ORDER BY created_at ASC, outbox_id ASC
                """,
                (job_id,),
            ).fetchall()
        return [self._row_to_webhook_outbox_record(row) for row in rows]

    def load_redeliverable_webhook_outbox_records(self) -> list[ReportJobWebhookOutboxRecord]:
        now = now_cn().isoformat()
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, job_id, event_type, job_status, status, attempts,
                       max_attempts, signature_mode, target_host_hash, created_at,
                       updated_at, completed_at, last_error_type, result_status_code
                FROM report_job_webhook_outbox
                WHERE event_type = ?
                  AND status IN ('pending', 'failed')
                  AND (lease_expires_at IS NULL OR lease_expires_at <= ?)
                ORDER BY updated_at ASC, created_at ASC, outbox_id ASC
                """,
                (REPORT_JOB_WEBHOOK_EVENT_TYPE, now),
            ).fetchall()
        return [self._row_to_webhook_outbox_record(row) for row in rows]

    def save_webhook_outbox_record(self, record: ReportJobWebhookOutboxRecord) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_job_webhook_outbox (
                    outbox_id, job_id, event_type, job_status, status, attempts,
                    max_attempts, signature_mode, target_host_hash, created_at,
                    updated_at, completed_at, last_error_type, result_status_code
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(outbox_id) DO UPDATE SET
                    job_id=excluded.job_id,
                    event_type=excluded.event_type,
                    job_status=excluded.job_status,
                    status=excluded.status,
                    attempts=excluded.attempts,
                    max_attempts=excluded.max_attempts,
                    signature_mode=excluded.signature_mode,
                    target_host_hash=excluded.target_host_hash,
                    created_at=excluded.created_at,
                    updated_at=excluded.updated_at,
                    completed_at=excluded.completed_at,
                    last_error_type=excluded.last_error_type,
                    result_status_code=excluded.result_status_code
                """,
                (
                    record.outbox_id,
                    record.job_id,
                    record.event_type,
                    record.job_status,
                    record.status,
                    record.attempts,
                    record.max_attempts,
                    record.signature_mode,
                    record.target_host_hash,
                    record.created_at,
                    record.updated_at,
                    record.completed_at,
                    record.last_error_type,
                    record.result_status_code,
                ),
            )

    def claim_webhook_outbox_record(
        self,
        record: ReportJobWebhookOutboxRecord,
        *,
        lease_owner: str,
        lease_seconds: float,
    ) -> ReportJobWebhookOutboxRecord | None:
        now = now_cn()
        now_text = now.isoformat()
        lease_ttl = max(1.0, float(lease_seconds))
        expires_at = (now + timedelta(seconds=lease_ttl)).isoformat()
        owner = str(lease_owner).strip()
        if not owner:
            return None
        with self._lock, self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE report_job_webhook_outbox
                SET lease_owner = ?,
                    lease_acquired_at = ?,
                    lease_expires_at = ?,
                    updated_at = ?
                WHERE outbox_id = ?
                  AND event_type = ?
                  AND status IN ('pending', 'failed')
                  AND (
                    lease_expires_at IS NULL
                    OR lease_expires_at <= ?
                    OR lease_owner = ?
                  )
                """,
                (
                    owner,
                    now_text,
                    expires_at,
                    now_text,
                    record.outbox_id,
                    record.event_type,
                    now_text,
                    owner,
                ),
            )
            if cursor.rowcount != 1:
                return None
            row = conn.execute(
                """
                SELECT outbox_id, job_id, event_type, job_status, status, attempts,
                       max_attempts, signature_mode, target_host_hash, created_at,
                       updated_at, completed_at, last_error_type, result_status_code
                FROM report_job_webhook_outbox
                WHERE outbox_id = ?
                """,
                (record.outbox_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_webhook_outbox_record(row)

    def release_webhook_outbox_record(self, outbox_id: str, *, lease_owner: str) -> None:
        owner = str(lease_owner).strip()
        if not owner:
            return
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE report_job_webhook_outbox
                SET lease_owner = NULL,
                    lease_acquired_at = NULL,
                    lease_expires_at = NULL
                WHERE outbox_id = ?
                  AND lease_owner = ?
                """,
                (outbox_id, owner),
            )

    def has_webhook_delivery_config_store(self) -> bool:
        return self.webhook_config_codec is not None

    def save_webhook_delivery_config(self, record: ReportJobWebhookOutboxRecord, webhook_config: Any) -> None:
        if not self.webhook_config_codec:
            return
        encrypted = self.webhook_config_codec.encrypt_config(webhook_config)
        now = now_cn().isoformat()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_job_webhook_delivery_config (
                    outbox_id, job_id, cipher_suite, key_id, ciphertext,
                    target_host_hash, signature_mode, created_at, updated_at, rotated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(outbox_id) DO UPDATE SET
                    job_id=excluded.job_id,
                    cipher_suite=excluded.cipher_suite,
                    key_id=excluded.key_id,
                    ciphertext=excluded.ciphertext,
                    target_host_hash=excluded.target_host_hash,
                    signature_mode=excluded.signature_mode,
                    updated_at=excluded.updated_at,
                    rotated_at=excluded.rotated_at
                """,
                (
                    record.outbox_id,
                    record.job_id,
                    encrypted.cipher_suite,
                    encrypted.key_id,
                    encrypted.ciphertext,
                    record.target_host_hash,
                    record.signature_mode,
                    now,
                    now,
                    None,
                ),
            )

    def load_webhook_delivery_config(self, record: ReportJobWebhookOutboxRecord) -> Any | None:
        if not self.webhook_config_codec:
            return None
        with self._lock, self._connect() as conn:
            row = conn.execute(
                """
                SELECT cipher_suite, key_id, ciphertext
                FROM report_job_webhook_delivery_config
                WHERE outbox_id = ?
                """,
                (record.outbox_id,),
            ).fetchone()
        if row is None:
            return None
        encrypted = EncryptedWebhookDeliveryConfig(
            cipher_suite=str(row["cipher_suite"]),
            key_id=str(row["key_id"]),
            ciphertext=str(row["ciphertext"]),
        )
        return self.webhook_config_codec.decrypt_config(encrypted)

    def delete_webhook_delivery_config(self, outbox_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "DELETE FROM report_job_webhook_delivery_config WHERE outbox_id = ?",
                (outbox_id,),
            )

    def rotate_webhook_delivery_configs(self) -> int:
        if not self.webhook_config_codec:
            return 0
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, cipher_suite, key_id, ciphertext
                FROM report_job_webhook_delivery_config
                ORDER BY updated_at ASC, outbox_id ASC
                """
            ).fetchall()
            rotated = 0
            now = now_cn().isoformat()
            for row in rows:
                old = EncryptedWebhookDeliveryConfig(
                    cipher_suite=str(row["cipher_suite"]),
                    key_id=str(row["key_id"]),
                    ciphertext=str(row["ciphertext"]),
                )
                if old.key_id == self.webhook_config_codec.active_key_id:
                    continue
                new = self.webhook_config_codec.rotate(old)
                conn.execute(
                    """
                    UPDATE report_job_webhook_delivery_config
                    SET cipher_suite = ?, key_id = ?, ciphertext = ?, updated_at = ?, rotated_at = ?
                    WHERE outbox_id = ?
                    """,
                    (new.cipher_suite, new.key_id, new.ciphertext, now, now, str(row["outbox_id"])),
                )
                rotated += 1
        return rotated

    def count_webhook_delivery_configs(self) -> int:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM report_job_webhook_delivery_config").fetchone()
        return int(row["count"] or 0)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS report_jobs (
                    job_id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    status TEXT NOT NULL,
                    report_system TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT,
                    error TEXT,
                    result_json TEXT,
                    input_summary_json TEXT NOT NULL,
                    idempotency_key TEXT,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_report_jobs_idempotency "
                "ON report_jobs(idempotency_key) WHERE idempotency_key IS NOT NULL"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_report_jobs_status ON report_jobs(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_report_jobs_expires_at ON report_jobs(expires_at)")
            self._ensure_column(conn, "report_jobs", "attempts", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(conn, "report_jobs", "max_attempts", "INTEGER NOT NULL DEFAULT 1")
            self._ensure_column(conn, "report_jobs", "attempt_timeout_seconds", "REAL")
            self._ensure_column(conn, "report_jobs", "retry_backoff_seconds", "REAL NOT NULL DEFAULT 0")
            self._ensure_column(conn, "report_jobs", "task_payload_json", "TEXT")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS report_job_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    job_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    message TEXT,
                    metadata_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_report_job_events_job_sequence ON report_job_events(job_id, sequence)"
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS report_job_webhook_outbox (
                    outbox_id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    job_status TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL DEFAULT 1,
                    signature_mode TEXT NOT NULL,
                    target_host_hash TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    completed_at TEXT,
                    last_error_type TEXT,
                    result_status_code INTEGER
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_job ON report_job_webhook_outbox(job_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_status ON report_job_webhook_outbox(status)"
            )
            self._ensure_column(conn, "report_job_webhook_outbox", "lease_owner", "TEXT")
            self._ensure_column(conn, "report_job_webhook_outbox", "lease_acquired_at", "TEXT")
            self._ensure_column(conn, "report_job_webhook_outbox", "lease_expires_at", "TEXT")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_outbox_lease "
                "ON report_job_webhook_outbox(status, lease_expires_at)"
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS report_job_webhook_delivery_config (
                    outbox_id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    cipher_suite TEXT NOT NULL,
                    key_id TEXT NOT NULL,
                    ciphertext TEXT NOT NULL,
                    target_host_hash TEXT,
                    signature_mode TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    rotated_at TEXT
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_report_job_webhook_delivery_config_job "
                "ON report_job_webhook_delivery_config(job_id)"
            )

    @staticmethod
    def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        columns = {str(row["name"]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in columns:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def _row_to_job(self, row: sqlite3.Row) -> _ReportJob:
        return _ReportJob(
            job_id=str(row["job_id"]),
            kind=str(row["kind"]),
            status=_coerce_status(str(row["status"])),
            report_system=str(row["report_system"]),
            task=None,
            task_payload=_coerce_task_payload(_json_loads(row["task_payload_json"])),
            input_summary=_json_loads(row["input_summary_json"]) or {},
            idempotency_key=row["idempotency_key"],
            webhook_config=None,
            created_monotonic=time.monotonic(),
            expires_monotonic=_expires_monotonic(str(row["expires_at"])),
            created_at=str(row["created_at"]),
            expires_at=str(row["expires_at"]),
            started_at=row["started_at"],
            finished_at=row["finished_at"],
            error=row["error"],
            result=_json_loads(row["result_json"]),
            attempts=int(row["attempts"] or 0),
            max_attempts=max(1, int(row["max_attempts"] or 1)),
            attempt_timeout_seconds=float(row["attempt_timeout_seconds"])
            if row["attempt_timeout_seconds"] is not None
            else None,
            retry_backoff_seconds=max(0.0, float(row["retry_backoff_seconds"] or 0)),
        )

    def _row_to_event(self, row: sqlite3.Row) -> ReportJobEvent:
        metadata = _json_loads(row["metadata_json"])
        return ReportJobEvent(
            event_id=str(row["event_id"]),
            job_id=str(row["job_id"]),
            event_type=str(row["event_type"]),
            status=_coerce_status(str(row["status"])),
            created_at=str(row["created_at"]),
            message=row["message"],
            metadata=metadata if isinstance(metadata, dict) else {},
        )

    def _row_to_webhook_outbox_record(self, row: sqlite3.Row) -> ReportJobWebhookOutboxRecord:
        return ReportJobWebhookOutboxRecord(
            outbox_id=str(row["outbox_id"]),
            job_id=str(row["job_id"]),
            event_type=str(row["event_type"]),
            job_status=_coerce_status(str(row["job_status"])),
            status=_coerce_webhook_outbox_status(str(row["status"])),
            attempts=max(0, int(row["attempts"] or 0)),
            max_attempts=max(1, int(row["max_attempts"] or 1)),
            signature_mode=str(row["signature_mode"]),
            target_host_hash=row["target_host_hash"],
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            completed_at=row["completed_at"],
            last_error_type=row["last_error_type"],
            result_status_code=int(row["result_status_code"]) if row["result_status_code"] is not None else None,
        )


class PostgresReportJobStore(ReportJobStore):
    """Postgres 报告任务状态存储。

    该 backend 是外部数据库 adapter baseline。它复用 `ReportJobStore` 接口和 Postgres
    事务语义承载 job state、event history、idempotency、webhook outbox 与 outbox lease；
    是否具备生产多副本能力仍必须由真实数据库 smoke 和运维证据证明。
    """

    backend_name = "postgres"

    def __init__(
        self,
        database_url: str,
        *,
        webhook_config_codec: Any | None = None,
        connect_factory: Callable[[], Any] | None = None,
        initialize_schema: bool = True,
    ) -> None:
        if not str(database_url or "").strip():
            raise ValueError("FATE_REPORT_JOB_STORE=postgres 需要 FATE_REPORT_JOB_DATABASE_URL")
        self.webhook_config_codec = webhook_config_codec
        self._connect_factory = connect_factory or _build_postgres_connect_factory(str(database_url))
        self._lock = Lock()
        if initialize_schema:
            self._init_schema()

    def load_jobs(self) -> list[_ReportJob]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT job_id, kind, status, report_system, created_at, expires_at,
                       started_at, finished_at, error, result_json, input_summary_json,
                       idempotency_key, attempts, max_attempts, attempt_timeout_seconds,
                       retry_backoff_seconds, task_payload_json
                FROM report_jobs
                ORDER BY created_at ASC
                """
            ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def save_job(self, job: _ReportJob) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_jobs (
                    job_id, kind, status, report_system, created_at, expires_at,
                    started_at, finished_at, error, result_json, input_summary_json,
                    task_payload_json, idempotency_key, attempts, max_attempts,
                    attempt_timeout_seconds, retry_backoff_seconds, updated_at
                )
                VALUES (
                    %(job_id)s, %(kind)s, %(status)s, %(report_system)s, %(created_at)s, %(expires_at)s,
                    %(started_at)s, %(finished_at)s, %(error)s, %(result_json)s, %(input_summary_json)s,
                    %(task_payload_json)s, %(idempotency_key)s, %(attempts)s, %(max_attempts)s,
                    %(attempt_timeout_seconds)s, %(retry_backoff_seconds)s, %(updated_at)s
                )
                ON CONFLICT(job_id) DO UPDATE SET
                    kind=EXCLUDED.kind,
                    status=EXCLUDED.status,
                    report_system=EXCLUDED.report_system,
                    created_at=EXCLUDED.created_at,
                    expires_at=EXCLUDED.expires_at,
                    started_at=EXCLUDED.started_at,
                    finished_at=EXCLUDED.finished_at,
                    error=EXCLUDED.error,
                    result_json=EXCLUDED.result_json,
                    input_summary_json=EXCLUDED.input_summary_json,
                    task_payload_json=EXCLUDED.task_payload_json,
                    idempotency_key=EXCLUDED.idempotency_key,
                    attempts=EXCLUDED.attempts,
                    max_attempts=EXCLUDED.max_attempts,
                    attempt_timeout_seconds=EXCLUDED.attempt_timeout_seconds,
                    retry_backoff_seconds=EXCLUDED.retry_backoff_seconds,
                    updated_at=EXCLUDED.updated_at
                """,
                {
                    "job_id": job.job_id,
                    "kind": job.kind,
                    "status": job.status,
                    "report_system": job.report_system,
                    "created_at": job.created_at,
                    "expires_at": job.expires_at,
                    "started_at": job.started_at,
                    "finished_at": job.finished_at,
                    "error": job.error,
                    "result_json": _json_dumps(job.result),
                    "input_summary_json": _json_dumps(job.input_summary),
                    "task_payload_json": _json_dumps(job.task_payload),
                    "idempotency_key": job.idempotency_key,
                    "attempts": job.attempts,
                    "max_attempts": job.max_attempts,
                    "attempt_timeout_seconds": job.attempt_timeout_seconds,
                    "retry_backoff_seconds": job.retry_backoff_seconds,
                    "updated_at": now_cn().isoformat(),
                },
            )

    def claim_job_for_execution(
        self,
        job: _ReportJob,
        *,
        lease_owner: str,
        lease_seconds: float,
    ) -> _ReportJob | None:
        owner = str(lease_owner).strip()
        if not owner:
            return None
        now = now_cn()
        lease_ttl = max(1.0, float(lease_seconds))
        with self._lock, self._connect() as conn:
            row = conn.execute(
                POSTGRES_JOB_EXECUTION_CLAIM_SQL,
                {
                    "lease_owner": owner,
                    "now": now.isoformat(),
                    "lease_expires_at": (now + timedelta(seconds=lease_ttl)).isoformat(),
                    "job_id": job.job_id,
                },
            ).fetchone()
        if row is None:
            return None
        return self._row_to_job(row)

    def release_job_execution_lease(self, job_id: str, *, lease_owner: str) -> None:
        owner = str(lease_owner).strip()
        if not owner:
            return
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE report_jobs
                SET lease_owner = NULL,
                    lease_acquired_at = NULL,
                    lease_expires_at = NULL,
                    updated_at = %(updated_at)s
                WHERE job_id = %(job_id)s
                  AND lease_owner = %(lease_owner)s
                """,
                {"job_id": job_id, "lease_owner": owner, "updated_at": now_cn().isoformat()},
            )

    def load_job_events(self, job_id: str) -> list[ReportJobEvent]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT event_id, job_id, event_type, status, created_at, message, metadata_json
                FROM report_job_events
                WHERE job_id = %(job_id)s
                ORDER BY sequence ASC
                """,
                {"job_id": job_id},
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def append_job_event(self, event: ReportJobEvent) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_job_events (
                    event_id, job_id, event_type, status, created_at, message, metadata_json
                )
                VALUES (
                    %(event_id)s, %(job_id)s, %(event_type)s, %(status)s,
                    %(created_at)s, %(message)s, %(metadata_json)s
                )
                ON CONFLICT(event_id) DO NOTHING
                """,
                {
                    "event_id": event.event_id,
                    "job_id": event.job_id,
                    "event_type": event.event_type,
                    "status": event.status,
                    "created_at": event.created_at,
                    "message": event.message,
                    "metadata_json": _json_dumps(event.metadata),
                },
            )

    def load_webhook_outbox_records(self, job_id: str) -> list[ReportJobWebhookOutboxRecord]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, job_id, event_type, job_status, status, attempts,
                       max_attempts, signature_mode, target_host_hash, created_at,
                       updated_at, completed_at, last_error_type, result_status_code
                FROM report_job_webhook_outbox
                WHERE job_id = %(job_id)s
                ORDER BY created_at ASC, outbox_id ASC
                """,
                {"job_id": job_id},
            ).fetchall()
        return [self._row_to_webhook_outbox_record(row) for row in rows]

    def load_redeliverable_webhook_outbox_records(self) -> list[ReportJobWebhookOutboxRecord]:
        now = now_cn().isoformat()
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, job_id, event_type, job_status, status, attempts,
                       max_attempts, signature_mode, target_host_hash, created_at,
                       updated_at, completed_at, last_error_type, result_status_code
                FROM report_job_webhook_outbox
                WHERE event_type = %(event_type)s
                  AND status IN ('pending', 'failed')
                  AND (lease_expires_at IS NULL OR lease_expires_at <= %(now)s)
                ORDER BY updated_at ASC, created_at ASC, outbox_id ASC
                """,
                {"event_type": REPORT_JOB_WEBHOOK_EVENT_TYPE, "now": now},
            ).fetchall()
        return [self._row_to_webhook_outbox_record(row) for row in rows]

    def save_webhook_outbox_record(self, record: ReportJobWebhookOutboxRecord) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_job_webhook_outbox (
                    outbox_id, job_id, event_type, job_status, status, attempts,
                    max_attempts, signature_mode, target_host_hash, created_at,
                    updated_at, completed_at, last_error_type, result_status_code
                )
                VALUES (
                    %(outbox_id)s, %(job_id)s, %(event_type)s, %(job_status)s, %(status)s, %(attempts)s,
                    %(max_attempts)s, %(signature_mode)s, %(target_host_hash)s, %(created_at)s,
                    %(updated_at)s, %(completed_at)s, %(last_error_type)s, %(result_status_code)s
                )
                ON CONFLICT(outbox_id) DO UPDATE SET
                    job_id=EXCLUDED.job_id,
                    event_type=EXCLUDED.event_type,
                    job_status=EXCLUDED.job_status,
                    status=EXCLUDED.status,
                    attempts=EXCLUDED.attempts,
                    max_attempts=EXCLUDED.max_attempts,
                    signature_mode=EXCLUDED.signature_mode,
                    target_host_hash=EXCLUDED.target_host_hash,
                    created_at=EXCLUDED.created_at,
                    updated_at=EXCLUDED.updated_at,
                    completed_at=EXCLUDED.completed_at,
                    last_error_type=EXCLUDED.last_error_type,
                    result_status_code=EXCLUDED.result_status_code
                """,
                {
                    "outbox_id": record.outbox_id,
                    "job_id": record.job_id,
                    "event_type": record.event_type,
                    "job_status": record.job_status,
                    "status": record.status,
                    "attempts": record.attempts,
                    "max_attempts": record.max_attempts,
                    "signature_mode": record.signature_mode,
                    "target_host_hash": record.target_host_hash,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at,
                    "completed_at": record.completed_at,
                    "last_error_type": record.last_error_type,
                    "result_status_code": record.result_status_code,
                },
            )

    def claim_webhook_outbox_record(
        self,
        record: ReportJobWebhookOutboxRecord,
        *,
        lease_owner: str,
        lease_seconds: float,
    ) -> ReportJobWebhookOutboxRecord | None:
        owner = str(lease_owner).strip()
        if not owner:
            return None
        now = now_cn()
        lease_ttl = max(1.0, float(lease_seconds))
        with self._lock, self._connect() as conn:
            row = conn.execute(
                POSTGRES_WEBHOOK_OUTBOX_CLAIM_SQL,
                {
                    "lease_owner": owner,
                    "now": now.isoformat(),
                    "lease_expires_at": (now + timedelta(seconds=lease_ttl)).isoformat(),
                    "outbox_id": record.outbox_id,
                    "event_type": record.event_type,
                },
            ).fetchone()
        if row is None:
            return None
        return self._row_to_webhook_outbox_record(row)

    def release_webhook_outbox_record(self, outbox_id: str, *, lease_owner: str) -> None:
        owner = str(lease_owner).strip()
        if not owner:
            return
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE report_job_webhook_outbox
                SET lease_owner = NULL,
                    lease_acquired_at = NULL,
                    lease_expires_at = NULL
                WHERE outbox_id = %(outbox_id)s
                  AND lease_owner = %(lease_owner)s
                """,
                {"outbox_id": outbox_id, "lease_owner": owner},
            )

    def has_webhook_delivery_config_store(self) -> bool:
        return self.webhook_config_codec is not None

    def save_webhook_delivery_config(self, record: ReportJobWebhookOutboxRecord, webhook_config: Any) -> None:
        if not self.webhook_config_codec:
            return
        encrypted = self.webhook_config_codec.encrypt_config(webhook_config)
        now = now_cn().isoformat()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO report_job_webhook_delivery_config (
                    outbox_id, job_id, cipher_suite, key_id, ciphertext,
                    target_host_hash, signature_mode, created_at, updated_at, rotated_at
                )
                VALUES (
                    %(outbox_id)s, %(job_id)s, %(cipher_suite)s, %(key_id)s, %(ciphertext)s,
                    %(target_host_hash)s, %(signature_mode)s, %(created_at)s, %(updated_at)s, %(rotated_at)s
                )
                ON CONFLICT(outbox_id) DO UPDATE SET
                    job_id=EXCLUDED.job_id,
                    cipher_suite=EXCLUDED.cipher_suite,
                    key_id=EXCLUDED.key_id,
                    ciphertext=EXCLUDED.ciphertext,
                    target_host_hash=EXCLUDED.target_host_hash,
                    signature_mode=EXCLUDED.signature_mode,
                    updated_at=EXCLUDED.updated_at,
                    rotated_at=EXCLUDED.rotated_at
                """,
                {
                    "outbox_id": record.outbox_id,
                    "job_id": record.job_id,
                    "cipher_suite": encrypted.cipher_suite,
                    "key_id": encrypted.key_id,
                    "ciphertext": encrypted.ciphertext,
                    "target_host_hash": record.target_host_hash,
                    "signature_mode": record.signature_mode,
                    "created_at": now,
                    "updated_at": now,
                    "rotated_at": None,
                },
            )

    def load_webhook_delivery_config(self, record: ReportJobWebhookOutboxRecord) -> Any | None:
        if not self.webhook_config_codec:
            return None
        with self._lock, self._connect() as conn:
            row = conn.execute(
                """
                SELECT cipher_suite, key_id, ciphertext
                FROM report_job_webhook_delivery_config
                WHERE outbox_id = %(outbox_id)s
                """,
                {"outbox_id": record.outbox_id},
            ).fetchone()
        if row is None:
            return None
        encrypted = EncryptedWebhookDeliveryConfig(
            cipher_suite=str(row["cipher_suite"]),
            key_id=str(row["key_id"]),
            ciphertext=str(row["ciphertext"]),
        )
        return self.webhook_config_codec.decrypt_config(encrypted)

    def delete_webhook_delivery_config(self, outbox_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "DELETE FROM report_job_webhook_delivery_config WHERE outbox_id = %(outbox_id)s",
                {"outbox_id": outbox_id},
            )

    def rotate_webhook_delivery_configs(self) -> int:
        if not self.webhook_config_codec:
            return 0
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT outbox_id, cipher_suite, key_id, ciphertext
                FROM report_job_webhook_delivery_config
                ORDER BY updated_at ASC, outbox_id ASC
                """
            ).fetchall()
            rotated = 0
            now = now_cn().isoformat()
            for row in rows:
                old = EncryptedWebhookDeliveryConfig(
                    cipher_suite=str(row["cipher_suite"]),
                    key_id=str(row["key_id"]),
                    ciphertext=str(row["ciphertext"]),
                )
                if old.key_id == self.webhook_config_codec.active_key_id:
                    continue
                new = self.webhook_config_codec.rotate(old)
                conn.execute(
                    """
                    UPDATE report_job_webhook_delivery_config
                    SET cipher_suite = %(cipher_suite)s,
                        key_id = %(key_id)s,
                        ciphertext = %(ciphertext)s,
                        updated_at = %(updated_at)s,
                        rotated_at = %(rotated_at)s
                    WHERE outbox_id = %(outbox_id)s
                    """,
                    {
                        "cipher_suite": new.cipher_suite,
                        "key_id": new.key_id,
                        "ciphertext": new.ciphertext,
                        "updated_at": now,
                        "rotated_at": now,
                        "outbox_id": str(row["outbox_id"]),
                    },
                )
                rotated += 1
        return rotated

    def count_webhook_delivery_configs(self) -> int:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM report_job_webhook_delivery_config").fetchone()
        return int(row["count"] or 0)

    def _connect(self) -> Any:
        return self._connect_factory()

    def _init_schema(self) -> None:
        with self._lock, self._connect() as conn:
            for statement in POSTGRES_REPORT_JOB_SCHEMA_SQL:
                conn.execute(statement)
            for statement in POSTGRES_REPORT_JOB_LEASE_MIGRATION_SQL:
                conn.execute(statement)
            conn.execute(POSTGRES_REPORT_JOB_LEASE_INDEX_SQL)

    def _row_to_job(self, row: Any) -> _ReportJob:
        return _ReportJob(
            job_id=str(row["job_id"]),
            kind=str(row["kind"]),
            status=_coerce_status(str(row["status"])),
            report_system=str(row["report_system"]),
            task=None,
            task_payload=_coerce_task_payload(_json_loads(row["task_payload_json"])),
            input_summary=_json_loads(row["input_summary_json"]) or {},
            idempotency_key=row["idempotency_key"],
            webhook_config=None,
            created_monotonic=time.monotonic(),
            expires_monotonic=_expires_monotonic(str(row["expires_at"])),
            created_at=str(row["created_at"]),
            expires_at=str(row["expires_at"]),
            started_at=row["started_at"],
            finished_at=row["finished_at"],
            error=row["error"],
            result=_json_loads(row["result_json"]),
            attempts=int(row["attempts"] or 0),
            max_attempts=max(1, int(row["max_attempts"] or 1)),
            attempt_timeout_seconds=float(row["attempt_timeout_seconds"])
            if row["attempt_timeout_seconds"] is not None
            else None,
            retry_backoff_seconds=max(0.0, float(row["retry_backoff_seconds"] or 0)),
        )

    def _row_to_event(self, row: Any) -> ReportJobEvent:
        metadata = _json_loads(row["metadata_json"])
        return ReportJobEvent(
            event_id=str(row["event_id"]),
            job_id=str(row["job_id"]),
            event_type=str(row["event_type"]),
            status=_coerce_status(str(row["status"])),
            created_at=str(row["created_at"]),
            message=row["message"],
            metadata=metadata if isinstance(metadata, dict) else {},
        )

    def _row_to_webhook_outbox_record(self, row: Any) -> ReportJobWebhookOutboxRecord:
        return ReportJobWebhookOutboxRecord(
            outbox_id=str(row["outbox_id"]),
            job_id=str(row["job_id"]),
            event_type=str(row["event_type"]),
            job_status=_coerce_status(str(row["job_status"])),
            status=_coerce_webhook_outbox_status(str(row["status"])),
            attempts=max(0, int(row["attempts"] or 0)),
            max_attempts=max(1, int(row["max_attempts"] or 1)),
            signature_mode=str(row["signature_mode"]),
            target_host_hash=row["target_host_hash"],
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            completed_at=row["completed_at"],
            last_error_type=row["last_error_type"],
            result_status_code=int(row["result_status_code"]) if row["result_status_code"] is not None else None,
        )


class ReportJobManager:
    """有界报告任务队列。

    ponytail: 默认内存实现适合单进程免费公开入口；SQLite backend 只提升本地状态
    可查询性。本地 retry/timeout 与 webhook retry/outbox trail 已由 policy 管理；多副本生产、
    跨进程继续执行、持久 callback outbox、生产硬 timeout 和 webhook 仍应升级到专用任务系统。
    """

    def __init__(
        self,
        *,
        max_workers: int,
        queue_size: int,
        ttl_seconds: int,
        store: ReportJobStore | None = None,
        webhook_dispatcher: ReportJobWebhookDispatcher | None = None,
        delivery_resolver: Any = None,
        execution_policy: ReportJobExecutionPolicy | None = None,
        callback_policy: ReportJobWebhookPolicy | None = None,
        task_factories: dict[str, ReportJobTaskFactory] | None = None,
        webhook_redelivery_lease_seconds: float = 30.0,
        job_execution_lease_seconds: float = 30.0,
    ) -> None:
        self.max_workers = max(1, max_workers)
        self.queue_size = max(1, queue_size)
        self.ttl_seconds = max(60, ttl_seconds)
        self.store = store or InMemoryReportJobStore()
        self.webhook_dispatcher = webhook_dispatcher
        self.delivery_resolver = delivery_resolver
        self.execution_policy = (execution_policy or ReportJobExecutionPolicy()).normalized()
        self.callback_policy = (callback_policy or ReportJobWebhookPolicy()).normalized()
        self.task_factories = dict(task_factories or {})
        self.webhook_redelivery_lease_seconds = max(1.0, float(webhook_redelivery_lease_seconds))
        self._webhook_redelivery_lease_owner = f"manager:{secrets.token_urlsafe(12)}"
        self.job_execution_lease_seconds = max(1.0, float(job_execution_lease_seconds))
        self._job_execution_lease_owner = f"manager-job:{secrets.token_urlsafe(12)}"
        self._queue: Queue[str] = Queue(maxsize=self.queue_size)
        self._jobs: dict[str, _ReportJob] = {}
        self._idempotency_index: dict[str, str] = {}
        self._lock = Lock()
        self._started = False
        self._recovered_requeued_count = 0
        self._load_persisted_jobs()
        self._schedule_webhook_outbox_redelivery()
        if self._recovered_requeued_count:
            self.start()

    @property
    def backend_name(self) -> str:
        return self.store.backend_name

    def start(self) -> None:
        with self._lock:
            if self._started:
                return
            self._started = True
            worker_count = self.max_workers
        for index in range(worker_count):
            thread = Thread(target=self._worker_loop, name=f"fatecat-report-worker-{index + 1}", daemon=True)
            thread.start()

    def submit(
        self,
        *,
        kind: str,
        report_system: str,
        task: Callable[[], Any],
        task_payload: dict[str, Any] | None = None,
        input_summary: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        webhook_config: Any | None = None,
        execution_policy: ReportJobExecutionPolicy | None = None,
    ) -> ReportJobSnapshot:
        self.start()
        self.cleanup_expired()
        normalized_idempotency_key = self._normalize_idempotency_key(idempotency_key)
        if normalized_idempotency_key:
            with self._lock:
                existing_job_id = self._idempotency_index.get(normalized_idempotency_key)
                existing_job = self._jobs.get(existing_job_id or "")
                if existing_job:
                    self._expire_job_if_needed_locked(existing_job)
                    return self._snapshot_locked(existing_job)

        job_id = secrets.token_urlsafe(18)
        created = now_cn()
        expires = created.timestamp() + self.ttl_seconds
        now_monotonic = time.monotonic()
        policy = (execution_policy or self.execution_policy).normalized()
        job = _ReportJob(
            job_id=job_id,
            kind=kind,
            report_system=report_system,
            task=task,
            task_payload=_coerce_task_payload(task_payload),
            input_summary=dict(input_summary or {}),
            idempotency_key=normalized_idempotency_key,
            webhook_config=webhook_config,
            created_monotonic=now_monotonic,
            expires_monotonic=now_monotonic + self.ttl_seconds,
            created_at=created.isoformat(),
            expires_at=now_cn().fromtimestamp(expires, tz=created.tzinfo).isoformat(),
            max_attempts=policy.max_attempts,
            attempt_timeout_seconds=policy.attempt_timeout_seconds,
            retry_backoff_seconds=policy.retry_backoff_seconds,
            non_retryable_exceptions=policy.non_retryable_exceptions,
        )
        with self._lock:
            if self._queue.full():
                raise ReportJobQueueFull("报告队列已满，请稍后再试")
            self._jobs[job_id] = job
            if normalized_idempotency_key:
                self._idempotency_index[normalized_idempotency_key] = job_id
            try:
                self._queue.put_nowait(job_id)
            except Full as exc:
                self._jobs.pop(job_id, None)
                if normalized_idempotency_key:
                    self._idempotency_index.pop(normalized_idempotency_key, None)
                raise ReportJobQueueFull("报告队列已满，请稍后再试") from exc
            self._persist_locked(job)
            self._append_event_locked(
                job,
                "job.queued",
                "报告任务已进入队列",
                {
                    "kind": kind,
                    "reportSystem": report_system,
                    "idempotencyKeyProvided": normalized_idempotency_key is not None,
                    "webhookEnabled": webhook_config is not None,
                    "maxAttempts": policy.max_attempts,
                    "attemptTimeoutSeconds": policy.attempt_timeout_seconds,
                    "retryBackoffSeconds": policy.retry_backoff_seconds,
                },
            )
            return self._snapshot_locked(job)

    def get(self, job_id: str) -> ReportJobSnapshot:
        self.cleanup_expired()
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                raise ReportJobNotFound(job_id)
            self._expire_job_if_needed_locked(job)
            return self._snapshot_locked(job)

    def cancel(self, job_id: str) -> ReportJobSnapshot:
        self.cleanup_expired()
        callback_snapshot: ReportJobSnapshot | None = None
        callback_config: Any | None = None
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                raise ReportJobNotFound(job_id)
            self._expire_job_if_needed_locked(job)
            if job.status not in {"queued", "running"}:
                return self._snapshot_locked(job)
            job.status = "cancelled"
            job.task = None
            job.result = None
            job.error = None
            job.finished_at = now_cn().isoformat()
            self._persist_locked(job)
            self._release_job_execution_lease_locked(job.job_id)
            self._append_event_locked(job, "job.cancelled", "报告任务已取消")
            callback_snapshot = self._snapshot_locked(job)
            callback_config = job.webhook_config
        self._dispatch_terminal_webhook(callback_snapshot, callback_config)
        return callback_snapshot

    def stats(self) -> dict[str, int]:
        self.cleanup_expired()
        with self._lock:
            counts = {"queued": 0, "running": 0, "succeeded": 0, "failed": 0, "expired": 0, "cancelled": 0}
            for job in self._jobs.values():
                counts[job.status] += 1
            counts["queue_size"] = counts["queued"]
            counts["queue_max"] = self.queue_size
            counts["worker_max"] = self.max_workers
            counts["ttl_seconds"] = self.ttl_seconds
            return counts

    def cleanup_expired(self) -> None:
        with self._lock:
            for job in self._jobs.values():
                self._expire_job_if_needed_locked(job)

    def _load_persisted_jobs(self) -> None:
        recovered = self.store.load_jobs()
        if not recovered:
            return
        for job in recovered:
            job.task = None
            if job.status in {"queued", "running"}:
                if self._try_requeue_recovered_job(job):
                    self._jobs[job.job_id] = job
                    if job.idempotency_key:
                        self._idempotency_index[job.idempotency_key] = job.job_id
                    continue
                self._mark_recovered_job_failed(job, reason="manager_rebuild")
            self._jobs[job.job_id] = job
            if job.idempotency_key:
                self._idempotency_index[job.idempotency_key] = job.job_id
        self.cleanup_expired()

    def _try_requeue_recovered_job(self, job: _ReportJob) -> bool:
        task = self._build_task_from_payload(job)
        if task is None:
            return False
        was_running = job.status == "running"
        job.task = task
        job.status = "queued"
        job.started_at = None
        job.error = None
        job.finished_at = None
        if was_running and job.attempts > 0:
            job.attempts -= 1
        try:
            self._queue.put_nowait(job.job_id)
        except Full:
            job.task = None
            self._mark_recovered_job_failed(job, reason="recovery_queue_full")
            return True
        self._recovered_requeued_count += 1
        self._append_event_locked(
            job,
            "job.recovered_requeued",
            "任务执行器重启后根据持久任务 payload 重新入队",
            {
                "reason": "manager_rebuild",
                "taskPayload": True,
                "taskFactory": job.kind,
            },
        )
        return True

    def _build_task_from_payload(self, job: _ReportJob) -> Callable[[], Any] | None:
        if not job.task_payload:
            return None
        factory = self.task_factories.get(job.kind)
        if not factory:
            return None
        return factory(dict(job.task_payload))

    def _mark_recovered_job_failed(self, job: _ReportJob, *, reason: str) -> None:
        job.status = "failed"
        job.error = job.error or "任务执行器已重启，未完成任务已终止"
        job.finished_at = job.finished_at or now_cn().isoformat()
        self.store.save_job(job)
        self._append_event_locked(
            job,
            "job.recovered_failed",
            "任务执行器重启后将未完成任务标记为失败",
            {"reason": reason},
        )

    def _schedule_webhook_outbox_redelivery(self) -> None:
        if not self.webhook_dispatcher:
            return
        if not self.delivery_resolver and not self.store.has_webhook_delivery_config_store():
            return
        records = tuple(self.store.load_redeliverable_webhook_outbox_records())
        if not records:
            return
        thread = Thread(
            target=self._redeliver_webhook_outbox_records,
            args=(records,),
            name="fatecat-webhook-outbox-redelivery",
            daemon=True,
        )
        thread.start()

    def _redeliver_webhook_outbox_records(self, records: tuple[ReportJobWebhookOutboxRecord, ...]) -> None:
        for record in records:
            self._redeliver_webhook_outbox_record(record)

    def _redeliver_webhook_outbox_record(self, record: ReportJobWebhookOutboxRecord) -> None:
        requested_record = record
        claimed_record = self.store.claim_webhook_outbox_record(
            requested_record,
            lease_owner=self._webhook_redelivery_lease_owner,
            lease_seconds=self.webhook_redelivery_lease_seconds,
        )
        if claimed_record is None:
            with self._lock:
                job = self._jobs.get(requested_record.job_id)
                if job:
                    self._append_event_locked(
                        job,
                        "webhook.redelivery_skipped",
                        "报告任务 webhook outbox 已被其他执行器 claim",
                        {
                            "outboxId": requested_record.outbox_id,
                            "outboxStatus": requested_record.status,
                            "reason": "lease_unavailable",
                        },
                    )
            return
        record = claimed_record
        try:
            with self._lock:
                job = self._jobs.get(record.job_id)
                if not job or job.status not in {"succeeded", "failed", "cancelled"}:
                    return
                snapshot = self._snapshot_locked(job)
            try:
                webhook_config = self.delivery_resolver(record, snapshot) if self.delivery_resolver else None
                if webhook_config is None:
                    webhook_config = self.store.load_webhook_delivery_config(record)
            except Exception as exc:  # noqa: BLE001 - resolver 是运行时外部边界，失败必须转成可审计事件。
                with self._lock:
                    job = self._jobs.get(record.job_id)
                    if job:
                        self._append_event_locked(
                            job,
                            "webhook.redelivery_failed",
                            "报告任务 webhook outbox 重投配置解析失败",
                            {
                                "outboxId": record.outbox_id,
                                "outboxStatus": record.status,
                                "reason": "config_resolution_failed",
                                "errorType": type(exc).__name__,
                            },
                        )
                return
            if webhook_config is None:
                with self._lock:
                    job = self._jobs.get(record.job_id)
                    if job:
                        self._append_event_locked(
                            job,
                            "webhook.redelivery_skipped",
                            "报告任务 webhook outbox 重投缺少运行时配置",
                            {
                                "outboxId": record.outbox_id,
                                "outboxStatus": record.status,
                                "reason": "config_unavailable",
                            },
                        )
                return

            with self._lock:
                job = self._jobs.get(record.job_id)
                if job:
                    self._append_event_locked(
                        job,
                        "webhook.redelivery_scheduled",
                        "报告任务 webhook outbox 已调度重投",
                        {
                            "outboxId": record.outbox_id,
                            "outboxStatus": record.status,
                            "previousAttempts": record.attempts,
                            "targetHostHash": record.target_host_hash,
                        },
                    )
            final_record = self._dispatch_terminal_webhook(
                snapshot,
                webhook_config,
                existing_outbox_record=record,
                redelivery=True,
            )
            if final_record is None:
                return
            with self._lock:
                job = self._jobs.get(record.job_id)
                if not job:
                    return
                if final_record.status == "succeeded":
                    self._append_event_locked(
                        job,
                        "webhook.redelivery_succeeded",
                        "报告任务 webhook outbox 重投成功",
                        {
                            "outboxId": final_record.outbox_id,
                            "attempts": final_record.attempts,
                            "statusCode": final_record.result_status_code,
                        },
                    )
                elif final_record.status == "failed":
                    self._append_event_locked(
                        job,
                        "webhook.redelivery_failed",
                        "报告任务 webhook outbox 重投失败",
                        {
                            "outboxId": final_record.outbox_id,
                            "attempts": final_record.attempts,
                            "errorType": final_record.last_error_type,
                        },
                    )
        finally:
            self.store.release_webhook_outbox_record(
                record.outbox_id,
                lease_owner=self._webhook_redelivery_lease_owner,
            )

    def _worker_loop(self) -> None:
        while True:
            job_id = self._queue.get()
            try:
                self._run_job(job_id)
            finally:
                self._queue.task_done()

    def _run_job(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job or job.status != "queued":
                return
            self._expire_job_if_needed_locked(job)
            if job.status != "queued":
                return
            task = job.task
            if task is None:
                return
            claimed_job = self.store.claim_job_for_execution(
                job,
                lease_owner=self._job_execution_lease_owner,
                lease_seconds=self.job_execution_lease_seconds,
            )
            if claimed_job is None:
                return
            job.status = "running"
            job.started_at = claimed_job.started_at or now_cn().isoformat()
            job.attempts = claimed_job.attempts
            job.max_attempts = claimed_job.max_attempts
            job.attempt_timeout_seconds = claimed_job.attempt_timeout_seconds
            job.retry_backoff_seconds = claimed_job.retry_backoff_seconds
            self._persist_locked(job)
            self._append_event_locked(job, "job.running", "报告任务开始执行")

        while True:
            with self._lock:
                job = self._jobs.get(job_id)
                if not job or job.status == "cancelled":
                    self._release_job_execution_lease_locked(job_id)
                    return
                if job.status != "running":
                    self._release_job_execution_lease_locked(job_id)
                    return
                job.attempts += 1
                attempt = job.attempts
                max_attempts = job.max_attempts
                timeout_seconds = job.attempt_timeout_seconds
                retry_backoff_seconds = job.retry_backoff_seconds
                self._persist_locked(job)

            outcome = _run_task_attempt(task, timeout_seconds)

            if outcome.timed_out:
                should_retry = attempt < max_attempts
                if self._handle_attempt_failure(
                    job_id,
                    ReportJobTimeoutError("报告任务执行超时"),
                    attempt=attempt,
                    timed_out=True,
                    should_retry=should_retry,
                    retryable=True,
                    timeout_seconds=timeout_seconds,
                ):
                    self._sleep_before_retry(retry_backoff_seconds)
                    continue
                return

            if outcome.error is not None:
                non_retryable = isinstance(outcome.error, job.non_retryable_exceptions)
                should_retry = not non_retryable and attempt < max_attempts
                if self._handle_attempt_failure(
                    job_id,
                    outcome.error,
                    attempt=attempt,
                    timed_out=False,
                    should_retry=should_retry,
                    retryable=not non_retryable,
                    timeout_seconds=timeout_seconds,
                ):
                    self._sleep_before_retry(retry_backoff_seconds)
                    continue
                return

            self._finish_job_success(job_id, outcome.result)
            return

    def _finish_job_success(self, job_id: str, result: Any) -> None:
        callback_snapshot = None
        callback_config = None
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            if job.status == "cancelled":
                job.task = None
                job.result = None
                self._persist_locked(job)
                self._release_job_execution_lease_locked(job_id)
                return
            job.status = "succeeded"
            job.result = result
            job.finished_at = now_cn().isoformat()
            job.task = None
            self._persist_locked(job)
            self._release_job_execution_lease_locked(job_id)
            self._append_event_locked(job, "job.succeeded", "报告任务执行成功", {"attempt": job.attempts})
            callback_snapshot = self._snapshot_locked(job)
            callback_config = job.webhook_config
        self._dispatch_terminal_webhook(callback_snapshot, callback_config)

    def _handle_attempt_failure(
        self,
        job_id: str,
        error: BaseException,
        *,
        attempt: int,
        timed_out: bool,
        should_retry: bool,
        retryable: bool,
        timeout_seconds: float | None,
    ) -> bool:
        error_type = type(error).__name__
        logger.warning(
            "报告任务 attempt 失败 job_id=%s attempt=%s error_type=%s timed_out=%s retryable=%s will_retry=%s",
            job_id,
            attempt,
            error_type,
            timed_out,
            retryable,
            should_retry,
        )
        callback_snapshot: ReportJobSnapshot | None = None
        callback_config: Any | None = None
        with self._lock:
            job = self._jobs.get(job_id)
            if not job or job.status == "cancelled":
                return False
            if job.status != "running":
                return False
            self._append_event_locked(
                job,
                "job.attempt_timed_out" if timed_out else "job.attempt_failed",
                "报告任务 attempt 超时" if timed_out else "报告任务 attempt 失败",
                {
                    "attempt": attempt,
                    "maxAttempts": job.max_attempts,
                    "errorType": error_type,
                    "retryable": retryable,
                    "willRetry": should_retry,
                    "timeoutSeconds": timeout_seconds,
                },
            )
            if should_retry:
                self._append_event_locked(
                    job,
                    "job.retry_scheduled",
                    "报告任务将按 retry policy 重试",
                    {
                        "attempt": attempt,
                        "nextAttempt": attempt + 1,
                        "maxAttempts": job.max_attempts,
                        "retryBackoffSeconds": job.retry_backoff_seconds,
                    },
                )
                self._persist_locked(job)
                return True

            job.status = "failed"
            job.error = str(error) or error_type
            job.finished_at = now_cn().isoformat()
            job.task = None
            self._persist_locked(job)
            self._release_job_execution_lease_locked(job_id)
            self._append_event_locked(
                job,
                "job.failed",
                "报告任务执行失败",
                {
                    "attempt": attempt,
                    "maxAttempts": job.max_attempts,
                    "errorType": error_type,
                    "retryable": retryable,
                    "timedOut": timed_out,
                },
            )
            callback_snapshot = self._snapshot_locked(job)
            callback_config = job.webhook_config
        self._dispatch_terminal_webhook(callback_snapshot, callback_config)
        return False

    def _sleep_before_retry(self, retry_backoff_seconds: float) -> None:
        if retry_backoff_seconds > 0:
            time.sleep(retry_backoff_seconds)

    def _expire_job_if_needed_locked(self, job: _ReportJob) -> None:
        if job.status in {"queued", "succeeded", "failed", "cancelled"} and time.monotonic() >= job.expires_monotonic:
            job.status = "expired"
            job.task = None
            job.result = None
            self._persist_locked(job)
            self._append_event_locked(job, "job.expired", "报告任务已过期")

    def _snapshot_locked(self, job: _ReportJob) -> ReportJobSnapshot:
        return ReportJobSnapshot(
            job_id=job.job_id,
            kind=job.kind,
            status=job.status,
            report_system=job.report_system,
            created_at=job.created_at,
            expires_at=job.expires_at,
            started_at=job.started_at,
            finished_at=job.finished_at,
            queue_position=self._queue_position_locked(job.job_id) if job.status == "queued" else None,
            error=job.error,
            result=job.result,
            input_summary=dict(job.input_summary),
            idempotency_key=job.idempotency_key,
            webhook_enabled=job.webhook_config is not None,
            webhook_signature=getattr(job.webhook_config, "signature_mode", "none")
            if job.webhook_config is not None
            else "none",
            attempts=job.attempts,
            max_attempts=job.max_attempts,
            attempt_timeout_seconds=job.attempt_timeout_seconds,
            retry_backoff_seconds=job.retry_backoff_seconds,
            events=tuple(self.store.load_job_events(job.job_id)),
            callback_outbox=tuple(self.store.load_webhook_outbox_records(job.job_id)),
        )

    def _persist_locked(self, job: _ReportJob) -> None:
        self.store.save_job(job)

    def _persist_webhook_outbox_locked(self, record: ReportJobWebhookOutboxRecord) -> None:
        self.store.save_webhook_outbox_record(record)

    def _release_job_execution_lease_locked(self, job_id: str) -> None:
        self.store.release_job_execution_lease(job_id, lease_owner=self._job_execution_lease_owner)

    def _append_event_locked(
        self,
        job: _ReportJob,
        event_type: str,
        message: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ReportJobEvent:
        event = ReportJobEvent(
            event_id=_new_event_id(job.job_id, event_type),
            job_id=job.job_id,
            event_type=event_type,
            status=job.status,
            created_at=now_cn().isoformat(),
            message=message,
            metadata=dict(metadata or {}),
        )
        self.store.append_job_event(event)
        return event

    def _dispatch_terminal_webhook(
        self,
        snapshot: ReportJobSnapshot | None,
        webhook_config: Any | None,
        *,
        existing_outbox_record: ReportJobWebhookOutboxRecord | None = None,
        redelivery: bool = False,
    ) -> ReportJobWebhookOutboxRecord | None:
        if not snapshot or not webhook_config or not self.webhook_dispatcher:
            return None
        if snapshot.status not in {"succeeded", "failed", "cancelled"}:
            return None
        max_attempts = self.callback_policy.max_attempts
        retry_backoff_seconds = self.callback_policy.retry_backoff_seconds
        now = now_cn().isoformat()
        if existing_outbox_record is None:
            outbox_record = ReportJobWebhookOutboxRecord(
                outbox_id=_webhook_outbox_id(snapshot),
                job_id=snapshot.job_id,
                event_type=REPORT_JOB_WEBHOOK_EVENT_TYPE,
                job_status=snapshot.status,
                status="pending",
                attempts=0,
                max_attempts=max_attempts,
                signature_mode=getattr(webhook_config, "signature_mode", "none"),
                target_host_hash=_target_host_hash(getattr(webhook_config, "url", None)),
                created_at=now,
                updated_at=now,
                completed_at=None,
                last_error_type=None,
                result_status_code=None,
            )
        else:
            outbox_record = replace(
                existing_outbox_record,
                status="pending",
                attempts=0,
                max_attempts=max_attempts,
                signature_mode=getattr(webhook_config, "signature_mode", existing_outbox_record.signature_mode),
                target_host_hash=existing_outbox_record.target_host_hash
                or _target_host_hash(getattr(webhook_config, "url", None)),
                updated_at=now,
                completed_at=None,
                last_error_type=None,
                result_status_code=None,
            )
        with self._lock:
            self._persist_webhook_outbox_locked(outbox_record)
        self._save_webhook_delivery_config(outbox_record, webhook_config)
        for attempt in range(1, max_attempts + 1):
            try:
                result = self.webhook_dispatcher(snapshot, webhook_config)
            except Exception as exc:  # noqa: BLE001 - webhook 是附属出口，失败不能反向破坏任务终态。
                error_type = type(exc).__name__
                will_retry = attempt < max_attempts
                updated_at = now_cn().isoformat()
                outbox_record = replace(
                    outbox_record,
                    status="pending" if will_retry else "failed",
                    attempts=attempt,
                    updated_at=updated_at,
                    completed_at=None if will_retry else updated_at,
                    last_error_type=error_type,
                    result_status_code=None,
                )
                logger.warning(
                    "报告任务 webhook 投递失败 job_id=%s status=%s attempt=%s error_type=%s will_retry=%s",
                    snapshot.job_id,
                    snapshot.status,
                    attempt,
                    error_type,
                    will_retry,
                )
                with self._lock:
                    self._persist_webhook_outbox_locked(outbox_record)
                    job = self._jobs.get(snapshot.job_id)
                    if job:
                        self._append_event_locked(
                            job,
                            "webhook.delivery_attempt_failed",
                            "报告任务 webhook 重投 attempt 失败"
                            if redelivery
                            else "报告任务 webhook 投递 attempt 失败",
                            {
                                "status": snapshot.status,
                                "attempt": attempt,
                                "maxAttempts": max_attempts,
                                "errorType": error_type,
                                "willRetry": will_retry,
                            },
                        )
                        if will_retry:
                            self._append_event_locked(
                                job,
                                "webhook.delivery_retry_scheduled",
                                "报告任务 webhook 重投将按 retry policy 重试"
                                if redelivery
                                else "报告任务 webhook 将按 retry policy 重试",
                                {
                                    "status": snapshot.status,
                                    "attempt": attempt,
                                    "nextAttempt": attempt + 1,
                                    "maxAttempts": max_attempts,
                                    "retryBackoffSeconds": retry_backoff_seconds,
                                },
                            )
                        else:
                            self._append_event_locked(
                                job,
                                "webhook.delivery_failed",
                                "报告任务 webhook 重投失败" if redelivery else "报告任务 webhook 投递失败",
                                {
                                    "status": snapshot.status,
                                    "attempt": attempt,
                                    "maxAttempts": max_attempts,
                                    "errorType": error_type,
                                },
                            )
                if will_retry:
                    self._sleep_before_retry(retry_backoff_seconds)
                    continue
                return outbox_record
            updated_at = now_cn().isoformat()
            outbox_record = replace(
                outbox_record,
                status="succeeded",
                attempts=attempt,
                updated_at=updated_at,
                completed_at=updated_at,
                last_error_type=None,
                result_status_code=getattr(result, "status_code", None),
            )
            with self._lock:
                self._persist_webhook_outbox_locked(outbox_record)
                job = self._jobs.get(snapshot.job_id)
                if job:
                    self._append_event_locked(
                        job,
                        "webhook.delivery_succeeded",
                        "报告任务 webhook 重投成功" if redelivery else "报告任务 webhook 投递成功",
                        {
                            "status": snapshot.status,
                            "attempt": attempt,
                            "maxAttempts": max_attempts,
                            "statusCode": getattr(result, "status_code", None),
                            "eventType": getattr(result, "event_type", None),
                        },
                    )
            self._delete_webhook_delivery_config(outbox_record.outbox_id)
            return outbox_record
        return outbox_record

    def _save_webhook_delivery_config(self, record: ReportJobWebhookOutboxRecord, webhook_config: Any) -> None:
        try:
            self.store.save_webhook_delivery_config(record, webhook_config)
        except Exception as exc:  # noqa: BLE001 - encrypted config 是附属持久化，失败不能破坏任务终态。
            logger.warning(
                "报告任务 webhook 配置加密持久化失败 job_id=%s outbox_id=%s error_type=%s",
                record.job_id,
                record.outbox_id,
                type(exc).__name__,
            )

    def _delete_webhook_delivery_config(self, outbox_id: str) -> None:
        try:
            self.store.delete_webhook_delivery_config(outbox_id)
        except Exception as exc:  # noqa: BLE001 - 清理失败不能反向破坏已完成投递。
            logger.warning(
                "报告任务 webhook 配置密文清理失败 outbox_id=%s error_type=%s",
                outbox_id,
                type(exc).__name__,
            )

    def _queue_position_locked(self, job_id: str) -> int | None:
        with self._queue.mutex:
            queued_ids = list(self._queue.queue)
        try:
            return queued_ids.index(job_id) + 1
        except ValueError:
            return None

    @staticmethod
    def _normalize_idempotency_key(value: str | None) -> str | None:
        normalized = str(value or "").strip()
        return normalized or None


def _coerce_status(value: str) -> ReportJobStatus:
    allowed: set[ReportJobStatus] = {"queued", "running", "succeeded", "failed", "expired", "cancelled"}
    if value in allowed:
        return value  # type: ignore[return-value]
    return "failed"


def _coerce_webhook_outbox_status(value: str) -> ReportJobWebhookOutboxStatus:
    allowed: set[ReportJobWebhookOutboxStatus] = {"pending", "succeeded", "failed"}
    if value in allowed:
        return value  # type: ignore[return-value]
    return "failed"


def _coerce_task_payload(value: Any) -> dict[str, Any] | None:
    if value is None or not isinstance(value, dict):
        return None
    payload = _to_json_payload(value)
    return payload if isinstance(payload, dict) else None


def _webhook_outbox_id(snapshot: ReportJobSnapshot) -> str:
    return f"whob_{snapshot.job_id}_{snapshot.status}"


def _target_host_hash(raw_url: str | None) -> str | None:
    hostname = urlparse(str(raw_url or "")).hostname
    if not hostname:
        return None
    return sha256(hostname.lower().encode("utf-8")).hexdigest()[:16]


def _expires_monotonic(expires_at: str) -> float:
    try:
        expires = datetime.fromisoformat(expires_at)
        now = datetime.now(expires.tzinfo) if expires.tzinfo else datetime.now()
        return time.monotonic() + max(0.0, (expires - now).total_seconds())
    except ValueError:
        return time.monotonic()


def _json_dumps(value: Any) -> str:
    return json.dumps(_to_json_payload(value), ensure_ascii=False, separators=(",", ":"))


def _json_loads(value: str | None) -> Any:
    if value is None:
        return None
    payload = json.loads(value)
    return _from_json_payload(payload)


def _to_json_payload(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if is_dataclass(value):
        return {"__fatecat_dataclass__": value.__class__.__name__, "data": _to_json_payload(asdict(value))}
    if isinstance(value, dict):
        return {str(key): _to_json_payload(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_json_payload(item) for item in value]
    return str(value)


def _from_json_payload(payload: Any) -> Any:
    if isinstance(payload, dict) and payload.get("__fatecat_dataclass__") == "WebReportResult":
        try:
            from web_forms import WebReportResult  # noqa: PLC0415

            data = payload.get("data")
            if isinstance(data, dict):
                return WebReportResult(**data)
        except (ImportError, TypeError, ValueError):
            return payload.get("data")
    return payload


@dataclass(frozen=True)
class _TaskAttemptOutcome:
    result: Any | None = None
    error: BaseException | None = None
    timed_out: bool = False


def _run_task_attempt(task: Callable[[], Any], timeout_seconds: float | None) -> _TaskAttemptOutcome:
    if not timeout_seconds:
        try:
            return _TaskAttemptOutcome(result=task())
        except Exception as exc:  # noqa: BLE001 - 任务异常需要转成 job 状态。
            return _TaskAttemptOutcome(error=exc)

    done = Event()
    holder: dict[str, Any] = {}

    def run() -> None:
        try:
            holder["result"] = task()
        except Exception as exc:  # noqa: BLE001 - 任务异常需要转成 job 状态。
            holder["error"] = exc
        finally:
            done.set()

    thread = Thread(target=run, name="fatecat-report-attempt", daemon=True)
    thread.start()
    if not done.wait(timeout_seconds):
        return _TaskAttemptOutcome(timed_out=True)
    error = holder.get("error")
    if isinstance(error, BaseException):
        return _TaskAttemptOutcome(error=error)
    return _TaskAttemptOutcome(result=holder.get("result"))


def _new_event_id(job_id: str, event_type: str) -> str:
    normalized_type = "".join(ch if ch.isalnum() else "_" for ch in event_type).strip("_") or "event"
    return f"evt_{job_id}_{normalized_type}_{secrets.token_urlsafe(6)}"


def _truncate_event_text(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(str(value).split())[:240]
