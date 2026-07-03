"""本地 retention cleanup baseline。

本模块只实现可审计的 SQLite 本地清理：用户记录按 `created_at` 保留天数清理，
report job 按 `expires_at` 清理终态任务及其事件/outbox/config 关联行。外部 SIEM、
生产数据库、调度器和真实删除证据仍由外部 live evidence 证明。
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

TERMINAL_REPORT_JOB_STATUSES = ("succeeded", "failed", "expired", "cancelled")


class RetentionCleanupError(RuntimeError):
    """Retention cleanup 执行失败。"""


@dataclass(frozen=True)
class RetentionCleanupConfig:
    """Retention cleanup 输入配置。"""

    record_db_path: Path
    report_job_db_path: Path
    record_retention_days: int
    audit_event_retention_days: int
    report_job_ttl_seconds: int
    delete_mode: str = "hard_delete"
    dry_run: bool = True
    now: datetime | None = None


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_utc(value: datetime) -> str:
    normalized = value if value.tzinfo else value.replace(tzinfo=UTC)
    return normalized.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_delete_mode(value: str) -> str:
    normalized = (value or "").strip().lower() or "hard_delete"
    allowed = {"hard_delete", "tombstone_then_purge"}
    if normalized not in allowed:
        raise RetentionCleanupError(f"unsupported retention delete mode: {normalized}")
    return normalized


def _connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (table,)).fetchone()
    return row is not None


def _count(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...] = ()) -> int:
    row = conn.execute(sql, params).fetchone()
    return int(row["count"] or 0)


def _placeholder_list(size: int) -> str:
    return ",".join("?" for _ in range(size))


def cleanup_records(config: RetentionCleanupConfig) -> dict[str, Any]:
    """按记录 created_at 清理本地 records 表，不输出记录 ID 或用户字段。"""

    now = config.now or utc_now()
    delete_mode = normalize_delete_mode(config.delete_mode)
    if config.record_retention_days <= 0:
        return {
            "target": "records",
            "status": "skipped",
            "reason": "record retention disabled; explicit delete baseline",
            "retentionDays": config.record_retention_days,
            "candidateCount": 0,
            "deletedCount": 0,
            "deleteMode": delete_mode,
        }
    if not config.record_db_path.is_file():
        return {
            "target": "records",
            "status": "skipped",
            "reason": "record db missing",
            "retentionDays": config.record_retention_days,
            "candidateCount": 0,
            "deletedCount": 0,
            "deleteMode": delete_mode,
        }

    cutoff = now - timedelta(days=config.record_retention_days)
    cutoff_sql = cutoff.strftime("%Y-%m-%d %H:%M:%S")
    with _connect(config.record_db_path) as conn:
        if not _table_exists(conn, "records"):
            return {
                "target": "records",
                "status": "skipped",
                "reason": "records table missing",
                "retentionDays": config.record_retention_days,
                "candidateCount": 0,
                "deletedCount": 0,
                "deleteMode": delete_mode,
                "cutoff": iso_utc(cutoff),
            }
        candidate_count = _count(
            conn,
            "SELECT COUNT(*) AS count FROM records WHERE datetime(created_at) < datetime(?)",
            (cutoff_sql,),
        )
        deleted_count = 0
        if not config.dry_run and candidate_count:
            cursor = conn.execute("DELETE FROM records WHERE datetime(created_at) < datetime(?)", (cutoff_sql,))
            deleted_count = int(cursor.rowcount or 0)
    return {
        "target": "records",
        "status": "passed",
        "retentionDays": config.record_retention_days,
        "candidateCount": candidate_count,
        "deletedCount": deleted_count,
        "deleteMode": delete_mode,
        "dryRun": config.dry_run,
        "cutoff": iso_utc(cutoff),
    }


def _candidate_report_job_ids(conn: sqlite3.Connection, now: datetime) -> list[str]:
    now_sql = now.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S")
    rows = conn.execute(
        f"""
        SELECT job_id
        FROM report_jobs
        WHERE status IN ({_placeholder_list(len(TERMINAL_REPORT_JOB_STATUSES))})
          AND datetime(expires_at) <= datetime(?)
        ORDER BY expires_at ASC, job_id ASC
        """,
        (*TERMINAL_REPORT_JOB_STATUSES, now_sql),
    ).fetchall()
    return [str(row["job_id"]) for row in rows]


def cleanup_report_jobs(config: RetentionCleanupConfig) -> dict[str, Any]:
    """清理 SQLite report job store 的过期终态任务及关联行。"""

    now = config.now or utc_now()
    delete_mode = normalize_delete_mode(config.delete_mode)
    if not config.report_job_db_path.is_file():
        return {
            "target": "reportJobs",
            "status": "skipped",
            "reason": "report job db missing",
            "ttlSeconds": config.report_job_ttl_seconds,
            "candidateCount": 0,
            "deletedJobs": 0,
            "deleteMode": delete_mode,
        }
    with _connect(config.report_job_db_path) as conn:
        if not _table_exists(conn, "report_jobs"):
            return {
                "target": "reportJobs",
                "status": "skipped",
                "reason": "report_jobs table missing",
                "ttlSeconds": config.report_job_ttl_seconds,
                "candidateCount": 0,
                "deletedJobs": 0,
                "deleteMode": delete_mode,
            }
        candidate_ids = _candidate_report_job_ids(conn, now)
        candidate_count = len(candidate_ids)
        related_counts = {"events": 0, "webhookOutbox": 0, "webhookDeliveryConfigs": 0}
        deleted_counts = {"jobs": 0, "events": 0, "webhookOutbox": 0, "webhookDeliveryConfigs": 0}
        if candidate_ids:
            placeholders = _placeholder_list(candidate_count)
            params = tuple(candidate_ids)
            if _table_exists(conn, "report_job_events"):
                related_counts["events"] = _count(
                    conn,
                    f"SELECT COUNT(*) AS count FROM report_job_events WHERE job_id IN ({placeholders})",
                    params,
                )
            if _table_exists(conn, "report_job_webhook_outbox"):
                related_counts["webhookOutbox"] = _count(
                    conn,
                    f"SELECT COUNT(*) AS count FROM report_job_webhook_outbox WHERE job_id IN ({placeholders})",
                    params,
                )
            if _table_exists(conn, "report_job_webhook_delivery_config"):
                related_counts["webhookDeliveryConfigs"] = _count(
                    conn,
                    f"SELECT COUNT(*) AS count FROM report_job_webhook_delivery_config WHERE job_id IN ({placeholders})",
                    params,
                )
            if not config.dry_run:
                if _table_exists(conn, "report_job_webhook_delivery_config"):
                    cursor = conn.execute(
                        f"DELETE FROM report_job_webhook_delivery_config WHERE job_id IN ({placeholders})",
                        params,
                    )
                    deleted_counts["webhookDeliveryConfigs"] = int(cursor.rowcount or 0)
                if _table_exists(conn, "report_job_webhook_outbox"):
                    cursor = conn.execute(
                        f"DELETE FROM report_job_webhook_outbox WHERE job_id IN ({placeholders})",
                        params,
                    )
                    deleted_counts["webhookOutbox"] = int(cursor.rowcount or 0)
                if _table_exists(conn, "report_job_events"):
                    cursor = conn.execute(
                        f"DELETE FROM report_job_events WHERE job_id IN ({placeholders})",
                        params,
                    )
                    deleted_counts["events"] = int(cursor.rowcount or 0)
                cursor = conn.execute(f"DELETE FROM report_jobs WHERE job_id IN ({placeholders})", params)
                deleted_counts["jobs"] = int(cursor.rowcount or 0)
    return {
        "target": "reportJobs",
        "status": "passed",
        "ttlSeconds": config.report_job_ttl_seconds,
        "candidateCount": candidate_count,
        "relatedCandidateRows": related_counts,
        "deletedRows": deleted_counts,
        "deleteMode": delete_mode,
        "dryRun": config.dry_run,
        "cutoff": iso_utc(now),
        "terminalStatuses": list(TERMINAL_REPORT_JOB_STATUSES),
    }


def cleanup_audit_events(config: RetentionCleanupConfig) -> dict[str, Any]:
    """声明本地 audit_event 当前是日志输出，不做本地物理清理伪证。"""

    return {
        "target": "auditEvents",
        "status": "external_connectivity_pending",
        "retentionDays": config.audit_event_retention_days,
        "mode": "structured_log_only",
        "deletedCount": 0,
        "reason": "audit_event 当前是结构化日志；外部 SIEM/不可变审计存储 retention 需要外部 evidence。",
    }


def run_retention_cleanup(config: RetentionCleanupConfig) -> dict[str, Any]:
    """执行本地 retention cleanup 并返回脱敏 summary。"""

    now = config.now or utc_now()
    normalized_config = RetentionCleanupConfig(
        record_db_path=config.record_db_path,
        report_job_db_path=config.report_job_db_path,
        record_retention_days=max(0, int(config.record_retention_days)),
        audit_event_retention_days=max(1, int(config.audit_event_retention_days)),
        report_job_ttl_seconds=max(60, int(config.report_job_ttl_seconds)),
        delete_mode=normalize_delete_mode(config.delete_mode),
        dry_run=bool(config.dry_run),
        now=now,
    )
    targets = [
        cleanup_records(normalized_config),
        cleanup_report_jobs(normalized_config),
        cleanup_audit_events(normalized_config),
    ]
    errors = [item for item in targets if item["status"] not in {"passed", "skipped", "external_connectivity_pending"}]
    status = "passed" if not errors else "failed"
    return {
        "schemaVersion": 1,
        "kind": "fatecat.retention_cleanup_summary",
        "status": status,
        "generatedAt": iso_utc(utc_now()),
        "dryRun": normalized_config.dry_run,
        "deleteMode": normalized_config.delete_mode,
        "targets": targets,
        "auditActions": ["retention.cleanup.dry_run" if normalized_config.dry_run else "retention.cleanup.completed"],
        "privacyBoundary": "summary 只保存目标类型、计数、模式和 cutoff，不保存 recordId、jobId、userId、姓名、出生地区、报告正文、token、secret、DSN 或 webhook URL。",
        "externalConnectivity": "外部 SIEM/不可变审计存储 retention 仍为外部连通验证待执行。",
    }


def assert_no_sensitive_payload(summary: dict[str, Any]) -> None:
    text = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    forbidden = (
        "recordId=",
        "jobId=",
        "userId=",
        "birthPlace=",
        "report_body",
        "old-user",
        "fresh-user",
        "old-terminal",
        "fresh-terminal",
        "old-running",
        "旧样本",
        "新样本",
        "token=",
        "secret=",
        "password=",
        "BEGIN RSA",
        "BEGIN OPENSSH",
    )
    hits = [marker for marker in forbidden if marker in text]
    if hits:
        raise RetentionCleanupError(f"retention cleanup summary contains forbidden marker(s): {', '.join(hits)}")
