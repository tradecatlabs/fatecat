#!/usr/bin/env python3
"""Postgres worker heartbeat/polling smoke.

该脚本连接操作员提供的 Postgres DSN，验证 ReportJobManager 在 external
backend 下具备三项 worker runtime baseline：空闲 worker 可轮询持久 queued
任务，长任务执行期间可 heartbeat 续约 execution lease，expired running job
可被 polling worker 恢复执行。输出 JSON 只保留脱敏证据，不输出 DSN、用户
名、密码、callback URL、secret、报告正文或用户输入。
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
from threading import Event, Lock
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-worker-heartbeat-polling-smoke.json"
)
DEFAULT_DSN_ENV_NAME = "FATE_REPORT_JOB_DATABASE_URL"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)
IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class PostgresWorkerHeartbeatPollingSmokeError(RuntimeError):
    """Postgres worker heartbeat/polling smoke failed."""


class PostgresWorkerHeartbeatPollingSmokeBlocked(RuntimeError):
    """Postgres worker heartbeat/polling smoke cannot run in this environment."""


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
        raise PostgresWorkerHeartbeatPollingSmokeBlocked("missing optional dependency: psycopg") from exc

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
        raise PostgresWorkerHeartbeatPollingSmokeError("Postgres smoke schema name is not a safe identifier")
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
        raise PostgresWorkerHeartbeatPollingSmokeError("summary contains sensitive-looking inline value")
    for value in forbidden_values:
        if value and value in serialized:
            raise PostgresWorkerHeartbeatPollingSmokeError("summary contains forbidden runtime value")


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise PostgresWorkerHeartbeatPollingSmokeError(f"{name}: {details}")


def _make_job(runtime: RuntimeModules, *, job_id: str, now: Any, scenario: str, status: str = "queued") -> Any:
    return runtime.report_jobs._ReportJob(  # noqa: SLF001 - smoke validates persistence adapter boundary.
        job_id=job_id,
        kind="worker_heartbeat_polling_smoke",
        report_system="bazi",
        task=None,
        task_payload={"taskType": "worker_heartbeat_polling_smoke", "scenario": scenario, "version": 1},
        input_summary={"name": "测试用户", "birthPlace": "北京"},
        idempotency_key=f"{job_id}-idem",
        webhook_config=None,
        created_monotonic=time.monotonic(),
        expires_monotonic=time.monotonic() + 120,
        created_at=now.isoformat(),
        expires_at=(now + timedelta(seconds=120)).isoformat(),
        status=status,
        started_at=now.isoformat() if status == "running" else None,
        attempts=1 if status == "running" else 0,
        max_attempts=1,
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
    raise PostgresWorkerHeartbeatPollingSmokeError(
        f"job did not reach terminal status: {getattr(last_job, 'status', None)}"
    )


def _load_lease_owner(runtime: RuntimeModules, dsn_value: str, schema_name: str, job_id: str) -> str | None:
    with runtime.psycopg.connect(dsn_value, row_factory=runtime.dict_row) as conn:
        conn.execute(runtime.sql.SQL("SET search_path TO {}, public").format(runtime.sql.Identifier(schema_name)))
        row = conn.execute("SELECT lease_owner FROM report_jobs WHERE job_id = %s", (job_id,)).fetchone()
    return None if row is None else row["lease_owner"]


def run_worker_heartbeat_polling_smoke(
    *,
    dsn_value: str,
    dsn_env_name: str = DEFAULT_DSN_ENV_NAME,
    schema_name: str | None = None,
    drop_schema: bool = True,
) -> dict[str, Any]:
    if not str(dsn_value or "").strip():
        raise PostgresWorkerHeartbeatPollingSmokeBlocked(f"missing {dsn_env_name}")

    runtime = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []
    run_id = secrets.token_hex(8)
    schema = _validate_schema_name(schema_name or f"fatecat_worker_hp_{run_id}")
    now = runtime.report_jobs.now_cn()
    connect = _connect_factory(runtime, dsn_value, schema)
    cleanup_error: str | None = None
    execution_lock = Lock()
    execution_log: list[str] = []
    heartbeat_started = Event()

    seed_store = runtime.report_jobs.PostgresReportJobStore(dsn_value, connect_factory=connect, initialize_schema=True)
    observer_store = runtime.report_jobs.PostgresReportJobStore(
        dsn_value,
        connect_factory=connect,
        initialize_schema=False,
    )

    def build_task(payload: dict[str, Any]):
        scenario = str(payload.get("scenario") or "unknown")

        def run_task() -> dict[str, Any]:
            with execution_lock:
                execution_log.append(scenario)
            if scenario == "heartbeat":
                heartbeat_started.set()
                time.sleep(1.45)
            else:
                time.sleep(0.1)
            return {"reportSystem": "bazi", "scenario": scenario, "smoke": "worker-heartbeat-polling"}

        return run_task

    try:
        manager = runtime.report_jobs.ReportJobManager(
            max_workers=1,
            queue_size=8,
            ttl_seconds=120,
            store=runtime.report_jobs.PostgresReportJobStore(
                dsn_value,
                connect_factory=connect,
                initialize_schema=False,
            ),
            task_factories={"worker_heartbeat_polling_smoke": build_task},
            job_execution_lease_seconds=1,
            job_execution_heartbeat_interval_seconds=0.2,
            job_store_poll_interval_seconds=0.1,
        )
        manager.start()
        _check(checks, "manager_started", manager.backend_name == "postgres", "postgres manager started")

        polling_job_id = f"pg-worker-polling-{run_id}"
        seed_store.save_job(_make_job(runtime, job_id=polling_job_id, now=now, scenario="polling"))
        polling_terminal = _wait_for_persisted_terminal(observer_store, polling_job_id)
        polling_events = tuple(event.event_type for event in observer_store.load_job_events(polling_job_id))
        _check(
            checks,
            "polling_job_succeeded",
            polling_terminal.status == "succeeded",
            f"status={polling_terminal.status}",
        )
        _check(checks, "polling_event_recorded", "job.polled_requeued" in polling_events, ",".join(polling_events))

        heartbeat_snapshot = manager.submit(
            kind="worker_heartbeat_polling_smoke",
            report_system="bazi",
            task=build_task({"scenario": "heartbeat"}),
            task_payload={"taskType": "worker_heartbeat_polling_smoke", "scenario": "heartbeat", "version": 1},
            input_summary={"name": "测试用户", "birthPlace": "北京"},
        )
        _check(checks, "heartbeat_job_started", heartbeat_started.wait(timeout=3), "heartbeat task started")
        time.sleep(1.2)
        heartbeat_job = next(job for job in observer_store.load_jobs() if job.job_id == heartbeat_snapshot.job_id)
        stolen = observer_store.claim_job_for_execution(heartbeat_job, lease_owner="heartbeat-stealer", lease_seconds=5)
        _check(checks, "heartbeat_prevented_duplicate_claim", stolen is None, "lease was renewed before expiry")
        heartbeat_terminal = _wait_for_persisted_terminal(observer_store, heartbeat_snapshot.job_id)
        heartbeat_lease_owner = _load_lease_owner(runtime, dsn_value, schema, heartbeat_snapshot.job_id)
        _check(
            checks,
            "heartbeat_job_succeeded",
            heartbeat_terminal.status == "succeeded",
            f"status={heartbeat_terminal.status}",
        )
        _check(checks, "heartbeat_lease_cleared", heartbeat_lease_owner is None, "terminal job lease cleared")

        stuck_job_id = f"pg-worker-stuck-{run_id}"
        stuck_job = _make_job(runtime, job_id=stuck_job_id, now=now, scenario="stuck", status="running")
        seed_store.save_job(stuck_job)
        _check(
            checks,
            "stuck_job_dead_worker_claimed",
            seed_store.claim_job_for_execution(stuck_job, lease_owner="dead-worker", lease_seconds=1) is not None,
            "dead worker lease claimed",
        )
        time.sleep(1.2)
        stuck_terminal = _wait_for_persisted_terminal(observer_store, stuck_job_id)
        stuck_events = tuple(event.event_type for event in observer_store.load_job_events(stuck_job_id))
        stuck_lease_owner = _load_lease_owner(runtime, dsn_value, schema, stuck_job_id)
        _check(checks, "stuck_job_recovered", stuck_terminal.status == "succeeded", f"status={stuck_terminal.status}")
        _check(checks, "stuck_job_polled", "job.polled_requeued" in stuck_events, ",".join(stuck_events))
        _check(checks, "stuck_lease_cleared", stuck_lease_owner is None, "terminal job lease cleared")
    finally:
        try:
            if drop_schema:
                _drop_schema(runtime, dsn_value, schema)
        except Exception as exc:  # noqa: BLE001 - cleanup failure must be reported without exposing DSN.
            cleanup_error = type(exc).__name__

    _check(checks, "cleanup", cleanup_error is None, "schema dropped" if cleanup_error is None else cleanup_error)
    scenario_counts = {scenario: execution_log.count(scenario) for scenario in sorted(set(execution_log))}
    _check(
        checks,
        "execution_log_complete",
        scenario_counts == {"heartbeat": 1, "polling": 1, "stuck": 1},
        str(scenario_counts),
    )
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_worker_heartbeat_polling_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "database": {
            "databaseUrlEnv": dsn_env_name,
            "target": _target_fingerprint(dsn_value),
            "schemaHash": _hash_value(schema),
        },
        "checks": checks,
        "executionCounts": scenario_counts,
        "pollingQueuedJobExecuted": True,
        "heartbeatPreventedDuplicateClaim": True,
        "stuckJobRecovered": True,
        "leaseClearedAfterTerminal": True,
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "long-running multi-replica production runtime not verified",
                "public webhook live passed evidence not verified",
                "external Vault/KMS and production secret lifecycle not verified",
                "exactly-once execution is not claimed",
            ],
        },
        "privacyBoundary": (
            "Worker heartbeat/polling smoke reads DSN only from the named environment variable and writes only "
            "hashes/check names; summary must not contain DSN, username, password, callback URL, secret, report body "
            "or user input."
        ),
        "nonClaims": [
            "does_not_prove_production_ready",
            "does_not_prove_exactly_once",
            "does_not_prove_public_webhook_live",
            "does_not_prove_external_vault_or_kms",
            "does_not_prove_long_running_multi_replica_runtime",
        ],
    }
    _safe_summary(summary, forbidden_values=(dsn_value, run_id))
    return summary


def blocked_summary(*, reason: str, dsn_env_name: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_worker_heartbeat_polling_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "blocked",
        "database": {"databaseUrlEnv": dsn_env_name},
        "checks": [{"name": "environment_ready", "ok": False, "details": reason}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres worker heartbeat/polling smoke did not run",
                "long-running multi-replica production runtime not verified",
                "public webhook live passed evidence not verified",
            ],
        },
        "privacyBoundary": "Blocked summary does not read or output DSN, username, password, callback URL, token, secret or report body.",
        "nonClaims": [
            "does_not_connect_to_postgres",
            "does_not_verify_worker_heartbeat_polling",
            "does_not_prove_exactly_once",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres worker heartbeat/polling smoke。")
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help="worker heartbeat/polling smoke summary JSON 输出路径。",
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
        summary = run_worker_heartbeat_polling_smoke(
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
                    "shipGate": summary["shipGate"]["status"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except PostgresWorkerHeartbeatPollingSmokeBlocked as exc:
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
        print(f"postgres worker heartbeat/polling smoke blocked: {exc}", file=sys.stderr)
        return 2
    except PostgresWorkerHeartbeatPollingSmokeError as exc:
        print(f"postgres worker heartbeat/polling smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
