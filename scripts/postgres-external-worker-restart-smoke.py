#!/usr/bin/env python3
"""Postgres external backend worker restart smoke.

该脚本连接操作员提供的 Postgres DSN，用 stale running job + expired
execution lease 模拟 worker crash，再启动两个 `ReportJobManager` 实例
模拟 restart 后的竞争恢复。smoke 只输出脱敏 JSON，不输出 DSN、用户名、
密码、callback URL、secret、报告正文或用户输入。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-external-worker-restart-smoke.json"
)
DEFAULT_DSN_ENV_NAME = "FATE_REPORT_JOB_DATABASE_URL"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)
IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class PostgresExternalWorkerRestartSmokeError(RuntimeError):
    """Postgres external worker restart smoke failed."""


class PostgresExternalWorkerRestartSmokeBlocked(RuntimeError):
    """Postgres external worker restart smoke cannot run in this environment."""


@dataclass(frozen=True)
class RuntimeModules:
    report_jobs: Any
    psycopg: Any
    sql: Any
    dict_row: Any


def _load_runtime() -> RuntimeModules:
    if str(DELIVERY_SRC) not in sys.path:
        sys.path.insert(0, str(DELIVERY_SRC))
    try:
        import psycopg  # noqa: PLC0415
        from psycopg import sql  # noqa: PLC0415
        from psycopg.rows import dict_row  # noqa: PLC0415
    except ModuleNotFoundError as exc:
        raise PostgresExternalWorkerRestartSmokeBlocked("missing optional dependency: psycopg") from exc

    import report_jobs  # noqa: PLC0415

    return RuntimeModules(report_jobs=report_jobs, psycopg=psycopg, sql=sql, dict_row=dict_row)


def _hash_value(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()[:16]


def _target_fingerprint(dsn_value: str) -> dict[str, Any]:
    parsed = urlparse(dsn_value)
    host = parsed.hostname or "unknown"
    port = parsed.port or 5432
    db_name = (parsed.path or "/").lstrip("/") or "default"
    return {
        "scheme": parsed.scheme or "unknown",
        "hostHash": _hash_value(f"{host}:{port}"),
        "databaseHash": _hash_value(db_name),
        "hasUsername": bool(parsed.username),
        "hasPassword": bool(parsed.password),
    }


def _validate_schema_name(schema_name: str) -> str:
    normalized = str(schema_name or "").strip().lower()
    if not IDENTIFIER_PATTERN.match(normalized):
        raise PostgresExternalWorkerRestartSmokeError("Postgres smoke schema name is not a safe identifier")
    return normalized


def _connect_factory(runtime: RuntimeModules, dsn_value: str, schema_name: str):
    def connect() -> Any:
        conn = runtime.psycopg.connect(dsn_value, row_factory=runtime.dict_row)
        conn.execute(runtime.sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(runtime.sql.Identifier(schema_name)))
        conn.execute(runtime.sql.SQL("SET search_path TO {}, public").format(runtime.sql.Identifier(schema_name)))
        return conn

    return connect


def _drop_schema(runtime: RuntimeModules, dsn_value: str, schema_name: str) -> None:
    with runtime.psycopg.connect(dsn_value) as conn:
        conn.execute(runtime.sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(runtime.sql.Identifier(schema_name)))


def _safe_summary(summary: dict[str, Any], *, forbidden_values: tuple[str, ...]) -> None:
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    if SENSITIVE_VALUE_PATTERN.search(serialized):
        raise PostgresExternalWorkerRestartSmokeError("summary contains sensitive-looking inline value")
    for value in forbidden_values:
        if value and value in serialized:
            raise PostgresExternalWorkerRestartSmokeError("summary contains forbidden runtime value")


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise PostgresExternalWorkerRestartSmokeError(f"{name}: {details}")


def _make_stale_running_job(runtime: RuntimeModules, *, job_id: str, now: Any) -> Any:
    return runtime.report_jobs._ReportJob(  # noqa: SLF001 - smoke validates persistence adapter boundary.
        job_id=job_id,
        kind="external_worker_restart_smoke",
        report_system="bazi",
        task=None,
        task_payload={"taskType": "external_worker_restart_smoke", "version": 1},
        input_summary={"name": "测试用户", "birthPlace": "北京"},
        idempotency_key=f"{job_id}-idem",
        webhook_config=None,
        created_monotonic=time.monotonic(),
        expires_monotonic=time.monotonic() + 120,
        created_at=now.isoformat(),
        expires_at=(now + timedelta(seconds=120)).isoformat(),
        status="running",
        started_at=now.isoformat(),
        attempts=1,
        max_attempts=1,
    )


def _append_seed_events(runtime: RuntimeModules, store: Any, job: Any, now: Any) -> None:
    for event_type, status in (("job.queued", "queued"), ("job.running", "running")):
        store.append_job_event(
            runtime.report_jobs.ReportJobEvent(
                event_id=f"{job.job_id}:{event_type}",
                job_id=job.job_id,
                event_type=event_type,
                status=status,
                created_at=now.isoformat(),
                message=f"seeded {event_type}",
                metadata={"seededBy": "postgres_external_worker_restart_smoke"},
            )
        )


def _wait_for_persisted_terminal(store: Any, job_id: str, *, timeout_seconds: float = 8.0) -> Any:
    deadline = time.monotonic() + timeout_seconds
    last_job = None
    while time.monotonic() < deadline:
        jobs = {job.job_id: job for job in store.load_jobs()}
        last_job = jobs.get(job_id)
        if last_job and last_job.status in {"succeeded", "failed", "cancelled", "expired"}:
            return last_job
        time.sleep(0.05)
    raise PostgresExternalWorkerRestartSmokeError(
        f"job did not reach terminal status: {getattr(last_job, 'status', None)}"
    )


def _load_lease_owner(runtime: RuntimeModules, dsn_value: str, schema_name: str, job_id: str) -> str | None:
    with runtime.psycopg.connect(dsn_value, row_factory=runtime.dict_row) as conn:
        conn.execute(runtime.sql.SQL("SET search_path TO {}, public").format(runtime.sql.Identifier(schema_name)))
        row = conn.execute("SELECT lease_owner FROM report_jobs WHERE job_id = %s", (job_id,)).fetchone()
    return None if row is None else row["lease_owner"]


def run_external_worker_restart_smoke(
    *,
    dsn_value: str,
    dsn_env_name: str = DEFAULT_DSN_ENV_NAME,
    schema_name: str | None = None,
    drop_schema: bool = True,
) -> dict[str, Any]:
    if not str(dsn_value or "").strip():
        raise PostgresExternalWorkerRestartSmokeBlocked(f"missing {dsn_env_name}")

    runtime = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []
    run_id = secrets.token_hex(8)
    schema = _validate_schema_name(schema_name or f"fatecat_ext_worker_{run_id}")
    now = runtime.report_jobs.now_cn()
    connect = _connect_factory(runtime, dsn_value, schema)
    cleanup_error: str | None = None
    execution_lock = Lock()
    execution_labels: list[str] = []

    seed_store = runtime.report_jobs.PostgresReportJobStore(dsn_value, connect_factory=connect, initialize_schema=True)
    observer_store = runtime.report_jobs.PostgresReportJobStore(
        dsn_value,
        connect_factory=connect,
        initialize_schema=False,
    )

    def factory(label: str):
        def build_task(_payload: dict[str, Any]):
            def run_task() -> dict[str, Any]:
                with execution_lock:
                    execution_labels.append(label)
                time.sleep(0.2)
                return {"reportSystem": "bazi", "executorLabel": label, "smoke": "external-worker-restart"}

            return run_task

        return build_task

    try:
        job_id = f"pg-external-worker-restart-{run_id}"
        stale_job = _make_stale_running_job(runtime, job_id=job_id, now=now)
        seed_store.save_job(stale_job)
        _append_seed_events(runtime, seed_store, stale_job, now)
        _check(
            checks,
            "stale_running_job_seeded",
            any(job.job_id == job_id and job.status == "running" for job in observer_store.load_jobs()),
            "seeded running job visible",
        )

        dead_owner = "dead-worker"
        _check(
            checks,
            "dead_worker_claimed_initial_lease",
            seed_store.claim_job_for_execution(stale_job, lease_owner=dead_owner, lease_seconds=1) is not None,
            "stale job lease claimed by simulated crashed worker",
        )
        time.sleep(1.2)

        manager_a = runtime.report_jobs.ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=runtime.report_jobs.PostgresReportJobStore(
                dsn_value,
                connect_factory=connect,
                initialize_schema=False,
            ),
            task_factories={"external_worker_restart_smoke": factory("manager-a")},
            job_execution_lease_seconds=5,
        )
        manager_b = runtime.report_jobs.ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=runtime.report_jobs.PostgresReportJobStore(
                dsn_value,
                connect_factory=connect,
                initialize_schema=False,
            ),
            task_factories={"external_worker_restart_smoke": factory("manager-b")},
            job_execution_lease_seconds=5,
        )
        _check(
            checks,
            "two_managers_started",
            manager_a.backend_name == "postgres" and manager_b.backend_name == "postgres",
            "two postgres managers created",
        )

        terminal_job = _wait_for_persisted_terminal(observer_store, job_id)
        events = tuple(event.event_type for event in observer_store.load_job_events(job_id))
        lease_owner_after_terminal = _load_lease_owner(runtime, dsn_value, schema, job_id)
        execution_count = len(execution_labels)
        persisted_result = terminal_job.result if isinstance(terminal_job.result, dict) else {}

        _check(
            checks, "persisted_status_succeeded", terminal_job.status == "succeeded", f"status={terminal_job.status}"
        )
        _check(checks, "execution_count_one", execution_count == 1, f"execution_count={execution_count}")
        _check(
            checks,
            "persisted_executor_matches_execution_log",
            persisted_result.get("executorLabel") in execution_labels,
            "persisted executor is the worker that executed",
        )
        _check(checks, "recovered_requeued_event", "job.recovered_requeued" in events, ",".join(events))
        _check(checks, "job_running_event", "job.running" in events, ",".join(events))
        _check(checks, "job_succeeded_event", "job.succeeded" in events, ",".join(events))
        _check(
            checks,
            "lease_cleared_after_terminal",
            lease_owner_after_terminal is None,
            "terminal job has no active lease owner",
        )
    finally:
        try:
            if drop_schema:
                _drop_schema(runtime, dsn_value, schema)
        except Exception as exc:  # noqa: BLE001 - cleanup failure must be reported without exposing DSN.
            cleanup_error = type(exc).__name__

    _check(checks, "cleanup", cleanup_error is None, "schema dropped" if cleanup_error is None else cleanup_error)
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_external_worker_restart_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "database": {
            "databaseUrlEnv": dsn_env_name,
            "target": _target_fingerprint(dsn_value),
            "schemaHash": _hash_value(schema),
        },
        "checks": checks,
        "executionCount": execution_count,
        "executionLabels": sorted(execution_labels),
        "persistedStatus": terminal_job.status,
        "recoveredFromExpiredLease": True,
        "duplicateExecutionBlocked": execution_count == 1,
        "leaseClearedAfterTerminal": lease_owner_after_terminal is None,
        "eventTypes": events,
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "public webhook live delivery not verified",
                "external Vault/KMS and production secret lifecycle not verified",
                "exactly-once execution is not claimed",
                "heartbeat/renew and DB polling worker are not implemented",
            ],
        },
        "privacyBoundary": (
            "External worker restart smoke reads DSN only from the named environment variable and writes only hashes/check names; "
            "summary must not contain DSN, username, password, callback URL, secret, report body or user input."
        ),
        "nonClaims": [
            "does_not_prove_production_ready",
            "does_not_prove_exactly_once",
            "does_not_prove_public_webhook_live",
            "does_not_prove_external_vault_or_kms",
            "does_not_prove_heartbeat_or_polling_worker",
        ],
    }
    _safe_summary(summary, forbidden_values=(dsn_value, run_id))
    return summary


def blocked_summary(*, reason: str, dsn_env_name: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_external_worker_restart_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "blocked",
        "database": {"databaseUrlEnv": dsn_env_name},
        "checks": [{"name": "environment_ready", "ok": False, "details": reason}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres external worker restart smoke did not run",
                "public webhook live delivery not verified",
                "external Vault/KMS and production secret lifecycle not verified",
            ],
        },
        "privacyBoundary": "Blocked summary does not read or output DSN, username, password, callback URL, token, secret or report body.",
        "nonClaims": ["does_not_connect_to_postgres", "does_not_verify_external_worker_restart"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres external worker restart smoke。")
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help="external worker restart smoke summary JSON 输出路径。",
    )
    parser.add_argument(
        "--database-url-env",
        default=DEFAULT_DSN_ENV_NAME,
        help="保存 Postgres DSN 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument("--schema-name", default="", help="可选 smoke schema 名；默认生成一次性 schema。")
    parser.add_argument("--keep-schema", action="store_true", help="保留 schema。默认 drop schema cascade。")
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="缺少 DSN 或 psycopg 时写入 blocked summary 并返回 0；用于本地无外部环境巡检。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    dsn_value = os.getenv(args.database_url_env, "").strip()
    try:
        summary = run_external_worker_restart_smoke(
            dsn_value=dsn_value,
            dsn_env_name=args.database_url_env,
            schema_name=args.schema_name or None,
            drop_schema=not args.keep_schema,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "kind": summary["kind"],
                    "checks": len(summary["checks"]),
                    "executionCount": summary["executionCount"],
                    "shipGate": summary["shipGate"]["status"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except PostgresExternalWorkerRestartSmokeBlocked as exc:
        if args.allow_missing:
            summary = blocked_summary(reason=str(exc), dsn_env_name=args.database_url_env)
            write_summary(summary, args.output_json)
            print(
                json.dumps(
                    {
                        "status": summary["status"],
                        "kind": summary["kind"],
                        "reason": str(exc),
                        "outputJson": str(args.output_json),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0
        print(f"postgres external worker restart smoke blocked: {exc}", file=sys.stderr)
        return 2
    except PostgresExternalWorkerRestartSmokeError as exc:
        print(f"postgres external worker restart smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
