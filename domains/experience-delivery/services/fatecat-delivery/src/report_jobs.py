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
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from pathlib import Path
from queue import Full, Queue
from threading import Event, Lock, Thread
from typing import Any, Literal

from utils.timezone import now_cn

logger = logging.getLogger(__name__)

ReportJobStatus = Literal["queued", "running", "succeeded", "failed", "expired", "cancelled"]


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
class ReportJobEvent:
    event_id: str
    job_id: str
    event_type: str
    status: ReportJobStatus
    created_at: str
    message: str | None
    metadata: dict[str, Any]


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


ReportJobWebhookDispatcher = Callable[[ReportJobSnapshot, Any], Any]


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


class ReportJobStore:
    """报告任务状态存储接口。"""

    backend_name = "memory"

    def load_jobs(self) -> list[_ReportJob]:
        return []

    def save_job(self, _job: _ReportJob) -> None:
        return

    def load_job_events(self, _job_id: str) -> list[ReportJobEvent]:
        return []

    def append_job_event(self, _event: ReportJobEvent) -> None:
        return


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


class SQLiteReportJobStore(ReportJobStore):
    """SQLite 报告任务状态存储。

    该 backend 只持久化任务状态、结果、幂等索引和事件历史；callable 不可序列化，因此重建 manager
    时会把遗留的 queued/running 任务标记为 failed，避免假装任务仍可继续执行。
    """

    backend_name = "sqlite"

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._init_schema()

    def load_jobs(self) -> list[_ReportJob]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT job_id, kind, status, report_system, created_at, expires_at,
                       started_at, finished_at, error, result_json, input_summary_json,
                       idempotency_key, attempts, max_attempts, attempt_timeout_seconds,
                       retry_backoff_seconds
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
                    idempotency_key, attempts, max_attempts, attempt_timeout_seconds,
                    retry_backoff_seconds, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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


class ReportJobManager:
    """有界报告任务队列。

    ponytail: 默认内存实现适合单进程免费公开入口；SQLite backend 只提升本地状态
    可查询性。本地 retry/timeout 已由 execution policy 管理；多副本生产、跨进程继续执行、
    callback retry/outbox、生产硬 timeout 和 webhook 仍应升级到专用任务系统。
    """

    def __init__(
        self,
        *,
        max_workers: int,
        queue_size: int,
        ttl_seconds: int,
        store: ReportJobStore | None = None,
        webhook_dispatcher: ReportJobWebhookDispatcher | None = None,
        execution_policy: ReportJobExecutionPolicy | None = None,
    ) -> None:
        self.max_workers = max(1, max_workers)
        self.queue_size = max(1, queue_size)
        self.ttl_seconds = max(60, ttl_seconds)
        self.store = store or InMemoryReportJobStore()
        self.webhook_dispatcher = webhook_dispatcher
        self.execution_policy = (execution_policy or ReportJobExecutionPolicy()).normalized()
        self._queue: Queue[str] = Queue(maxsize=self.queue_size)
        self._jobs: dict[str, _ReportJob] = {}
        self._idempotency_index: dict[str, str] = {}
        self._lock = Lock()
        self._started = False
        self._load_persisted_jobs()

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
                job.status = "failed"
                job.error = job.error or "任务执行器已重启，未完成任务已终止"
                job.finished_at = job.finished_at or now_cn().isoformat()
                self.store.save_job(job)
                self._append_event_locked(
                    job,
                    "job.recovered_failed",
                    "任务执行器重启后将未完成任务标记为失败",
                    {"reason": "manager_rebuild"},
                )
            self._jobs[job.job_id] = job
            if job.idempotency_key:
                self._idempotency_index[job.idempotency_key] = job.job_id
        self.cleanup_expired()

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
            job.status = "running"
            job.started_at = now_cn().isoformat()
            self._persist_locked(job)
            self._append_event_locked(job, "job.running", "报告任务开始执行")

        if task is None:
            return

        while True:
            with self._lock:
                job = self._jobs.get(job_id)
                if not job or job.status == "cancelled":
                    return
                if job.status != "running":
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
                return
            job.status = "succeeded"
            job.result = result
            job.finished_at = now_cn().isoformat()
            job.task = None
            self._persist_locked(job)
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
        )

    def _persist_locked(self, job: _ReportJob) -> None:
        self.store.save_job(job)

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

    def _dispatch_terminal_webhook(self, snapshot: ReportJobSnapshot | None, webhook_config: Any | None) -> None:
        if not snapshot or not webhook_config or not self.webhook_dispatcher:
            return
        if snapshot.status not in {"succeeded", "failed", "cancelled"}:
            return
        try:
            result = self.webhook_dispatcher(snapshot, webhook_config)
        except Exception:  # noqa: BLE001 - webhook 是附属出口，失败不能反向破坏任务终态。
            logger.exception("报告任务 webhook 投递失败 job_id=%s status=%s", snapshot.job_id, snapshot.status)
            with self._lock:
                job = self._jobs.get(snapshot.job_id)
                if job:
                    self._append_event_locked(
                        job,
                        "webhook.delivery_failed",
                        "报告任务 webhook 投递失败",
                        {"status": snapshot.status},
                    )
            return
        with self._lock:
            job = self._jobs.get(snapshot.job_id)
            if job:
                self._append_event_locked(
                    job,
                    "webhook.delivery_succeeded",
                    "报告任务 webhook 投递成功",
                    {
                        "status": snapshot.status,
                        "statusCode": getattr(result, "status_code", None),
                        "eventType": getattr(result, "event_type", None),
                    },
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
