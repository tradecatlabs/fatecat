"""报告生成任务队列。

该模块负责报告任务生命周期：排队、执行、状态查询、TTL 过期、指标和可选持久化。
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
from threading import Lock, Thread
from typing import Any, Literal

from utils.timezone import now_cn

logger = logging.getLogger(__name__)

ReportJobStatus = Literal["queued", "running", "succeeded", "failed", "expired", "cancelled"]


class ReportJobQueueFull(RuntimeError):
    """报告任务队列已满。"""


class ReportJobNotFound(KeyError):
    """报告任务不存在或已清理。"""


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


class ReportJobStore:
    """报告任务状态存储接口。"""

    backend_name = "memory"

    def load_jobs(self) -> list[_ReportJob]:
        return []

    def save_job(self, _job: _ReportJob) -> None:
        return


class InMemoryReportJobStore(ReportJobStore):
    """默认空持久化实现；真实状态仍由 manager 内存字典持有。"""

    backend_name = "memory"


class SQLiteReportJobStore(ReportJobStore):
    """SQLite 报告任务状态存储。

    该 backend 只持久化任务状态、结果和幂等索引；callable 不可序列化，因此重建 manager
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
                       idempotency_key
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
                    idempotency_key, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    now_cn().isoformat(),
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
        )


class ReportJobManager:
    """有界报告任务队列。

    ponytail: 默认内存实现适合单进程免费公开入口；SQLite backend 只提升本地状态
    可查询性。多副本生产、跨进程继续执行、retry 和 webhook 仍应升级到专用任务系统。
    """

    def __init__(
        self,
        *,
        max_workers: int,
        queue_size: int,
        ttl_seconds: int,
        store: ReportJobStore | None = None,
        webhook_dispatcher: ReportJobWebhookDispatcher | None = None,
    ) -> None:
        self.max_workers = max(1, max_workers)
        self.queue_size = max(1, queue_size)
        self.ttl_seconds = max(60, ttl_seconds)
        self.store = store or InMemoryReportJobStore()
        self.webhook_dispatcher = webhook_dispatcher
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
        now = time.monotonic()
        with self._lock:
            for job in self._jobs.values():
                if job.status in {"queued", "succeeded", "failed", "cancelled"} and now >= job.expires_monotonic:
                    job.status = "expired"
                    job.task = None
                    job.result = None
                    self._persist_locked(job)

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

        if task is None:
            return
        try:
            result = task()
        except Exception as exc:  # noqa: BLE001 - 任务边界必须捕获并转成 failed 状态。
            logger.exception("报告任务执行失败 job_id=%s", job_id)
            callback_snapshot: ReportJobSnapshot | None = None
            callback_config: Any | None = None
            with self._lock:
                job = self._jobs.get(job_id)
                if job and job.status != "cancelled":
                    job.status = "failed"
                    job.error = str(exc) or type(exc).__name__
                    job.finished_at = now_cn().isoformat()
                    job.task = None
                    self._persist_locked(job)
                    callback_snapshot = self._snapshot_locked(job)
                    callback_config = job.webhook_config
            self._dispatch_terminal_webhook(callback_snapshot, callback_config)
            return

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
            callback_snapshot = self._snapshot_locked(job)
            callback_config = job.webhook_config
        self._dispatch_terminal_webhook(callback_snapshot, callback_config)

    def _expire_job_if_needed_locked(self, job: _ReportJob) -> None:
        if job.status in {"queued", "succeeded", "failed", "cancelled"} and time.monotonic() >= job.expires_monotonic:
            job.status = "expired"
            job.task = None
            job.result = None
            self._persist_locked(job)

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
        )

    def _persist_locked(self, job: _ReportJob) -> None:
        self.store.save_job(job)

    def _dispatch_terminal_webhook(self, snapshot: ReportJobSnapshot | None, webhook_config: Any | None) -> None:
        if not snapshot or not webhook_config or not self.webhook_dispatcher:
            return
        if snapshot.status not in {"succeeded", "failed", "cancelled"}:
            return
        try:
            self.webhook_dispatcher(snapshot, webhook_config)
        except Exception:  # noqa: BLE001 - webhook 是附属出口，失败不能反向破坏任务终态。
            logger.exception("报告任务 webhook 投递失败 job_id=%s status=%s", snapshot.job_id, snapshot.status)

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
