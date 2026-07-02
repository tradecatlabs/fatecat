#!/usr/bin/env python3
"""Postgres webhook outbox worker lease negative smoke.

该脚本连接操作员提供的 Postgres DSN，用两个独立 `PostgresReportJobStore`
实例模拟多副本 worker 并验证同一 outbox 记录的并发 claim 只能成功一次。
输出 JSON 只保留脱敏证据，不输出 DSN、用户名、密码、callback URL、secret 或报告正文。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from threading import Barrier
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-worker-lease-smoke.json"
DEFAULT_DSN_ENV_NAME = "FATE_REPORT_JOB_DATABASE_URL"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)
IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class PostgresWorkerLeaseSmokeError(RuntimeError):
    """Postgres worker lease smoke failed."""


class PostgresWorkerLeaseSmokeBlocked(RuntimeError):
    """Postgres worker lease smoke cannot run in this environment."""


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
        raise PostgresWorkerLeaseSmokeBlocked("missing optional dependency: psycopg") from exc

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
        raise PostgresWorkerLeaseSmokeError("Postgres smoke schema name is not a safe identifier")
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
        raise PostgresWorkerLeaseSmokeError("summary contains sensitive-looking inline value")
    for value in forbidden_values:
        if value and value in serialized:
            raise PostgresWorkerLeaseSmokeError("summary contains forbidden runtime value")


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise PostgresWorkerLeaseSmokeError(f"{name}: {details}")


def _make_job(runtime: RuntimeModules, *, job_id: str, now: Any) -> Any:
    return runtime.report_jobs._ReportJob(  # noqa: SLF001 - smoke validates persistence adapter boundary.
        job_id=job_id,
        kind="postgres_worker_lease_smoke",
        report_system="bazi",
        task=None,
        task_payload={"factory": "worker_lease_smoke", "version": 1},
        input_summary={"name": "测试用户", "birthPlace": "北京"},
        idempotency_key=f"{job_id}-idem",
        webhook_config=None,
        created_monotonic=time.monotonic(),
        expires_monotonic=time.monotonic() + 120,
        created_at=now.isoformat(),
        expires_at=(now + timedelta(seconds=120)).isoformat(),
        status="succeeded",
        result={"summary": "dummy-worker-lease-smoke-result"},
    )


def _make_outbox(runtime: RuntimeModules, *, outbox_id: str, job_id: str, now: Any) -> Any:
    return runtime.report_jobs.ReportJobWebhookOutboxRecord(
        outbox_id=outbox_id,
        job_id=job_id,
        event_type=runtime.report_jobs.REPORT_JOB_WEBHOOK_EVENT_TYPE,
        job_status="succeeded",
        status="failed",
        attempts=1,
        max_attempts=2,
        signature_mode="hmac-sha256",
        target_host_hash=_hash_value("dummy-callback-host"),
        created_at=now.isoformat(),
        updated_at=now.isoformat(),
        completed_at=None,
        last_error_type="SmokeTransportError",
        result_status_code=500,
    )


def _race_claim(store_a: Any, store_b: Any, record: Any, *, owner_a: str, owner_b: str) -> dict[str, Any]:
    barrier = Barrier(2)

    def claim(store: Any, owner: str) -> str | None:
        barrier.wait(timeout=5)
        claimed = store.claim_webhook_outbox_record(record, lease_owner=owner, lease_seconds=30)
        return owner if claimed is not None else None

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(claim, store_a, owner_a)
        second = executor.submit(claim, store_b, owner_b)
        winners = [winner for winner in (first.result(timeout=10), second.result(timeout=10)) if winner]
    return {"winnerCount": len(winners), "winners": winners}


def run_worker_lease_smoke(
    *,
    dsn_value: str,
    dsn_env_name: str = DEFAULT_DSN_ENV_NAME,
    schema_name: str | None = None,
    race_count: int = 5,
    drop_schema: bool = True,
) -> dict[str, Any]:
    if not str(dsn_value or "").strip():
        raise PostgresWorkerLeaseSmokeBlocked(f"missing {dsn_env_name}")

    runtime = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []
    run_id = secrets.token_hex(8)
    schema = _validate_schema_name(schema_name or f"fatecat_lease_{run_id}")
    now = runtime.report_jobs.now_cn()
    race_total = max(2, min(20, int(race_count)))
    connect = _connect_factory(runtime, dsn_value, schema)
    cleanup_error: str | None = None

    store_a = runtime.report_jobs.PostgresReportJobStore(
        dsn_value,
        connect_factory=connect,
        initialize_schema=True,
    )
    store_b = runtime.report_jobs.PostgresReportJobStore(
        dsn_value,
        connect_factory=connect,
        initialize_schema=False,
    )

    try:
        job_id = f"pg-worker-lease-job-{run_id}"
        store_a.save_job(_make_job(runtime, job_id=job_id, now=now))
        _check(
            checks,
            "schema_and_job_initialized",
            len([job for job in store_b.load_jobs() if job.job_id == job_id]) == 1,
            "visible across stores",
        )

        race_results: list[dict[str, Any]] = []
        for index in range(race_total):
            outbox_id = f"pg-worker-lease-outbox-{run_id}-{index}"
            record = _make_outbox(runtime, outbox_id=outbox_id, job_id=job_id, now=now)
            store_a.save_webhook_outbox_record(record)
            owner_a = f"worker-a-{run_id}-{index}"
            owner_b = f"worker-b-{run_id}-{index}"
            result = _race_claim(store_a, store_b, record, owner_a=owner_a, owner_b=owner_b)
            race_results.append({"winnerCount": result["winnerCount"]})
            _check(
                checks,
                f"duplicate_claim_negative_{index}",
                result["winnerCount"] == 1,
                f"winner_count={result['winnerCount']}",
            )
            winner = result["winners"][0]
            loser = owner_b if winner == owner_a else owner_a
            store_b.release_webhook_outbox_record(outbox_id, lease_owner=loser)
            _check(
                checks,
                f"loser_cannot_release_{index}",
                store_a.claim_webhook_outbox_record(record, lease_owner=loser, lease_seconds=30) is None,
                "loser release did not clear lease",
            )
            store_a.release_webhook_outbox_record(outbox_id, lease_owner=winner)

        expiry_outbox_id = f"pg-worker-lease-expiry-{run_id}"
        expiry_record = _make_outbox(runtime, outbox_id=expiry_outbox_id, job_id=job_id, now=now)
        store_a.save_webhook_outbox_record(expiry_record)
        expiry_owner_a = f"expiry-worker-a-{run_id}"
        expiry_owner_b = f"expiry-worker-b-{run_id}"
        _check(
            checks,
            "lease_initial_claim",
            store_a.claim_webhook_outbox_record(expiry_record, lease_owner=expiry_owner_a, lease_seconds=1) is not None,
            "claimed",
        )
        time.sleep(1.2)
        _check(
            checks,
            "lease_reclaim_after_expiry",
            store_b.claim_webhook_outbox_record(expiry_record, lease_owner=expiry_owner_b, lease_seconds=30)
            is not None,
            "reclaimed",
        )
        store_b.release_webhook_outbox_record(expiry_outbox_id, lease_owner=expiry_owner_b)
    finally:
        try:
            if drop_schema:
                _drop_schema(runtime, dsn_value, schema)
        except Exception as exc:  # noqa: BLE001 - cleanup failure must be reported without exposing DSN.
            cleanup_error = type(exc).__name__

    _check(checks, "cleanup", cleanup_error is None, "schema dropped" if cleanup_error is None else cleanup_error)
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_worker_lease_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "database": {
            "databaseUrlEnv": dsn_env_name,
            "target": _target_fingerprint(dsn_value),
            "schemaHash": _hash_value(schema),
        },
        "checks": checks,
        "leaseEvidence": {
            "independentStoreCount": 2,
            "duplicateClaimRaceCount": race_total,
            "duplicateClaimWinnerCount": 1,
            "loserReleaseBlocked": True,
            "leaseExpiryReclaim": True,
            "cleanup": cleanup_error is None,
        },
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "job execution worker lease is not implemented",
                "public webhook live delivery not verified",
                "external Vault/KMS and production secret lifecycle not verified",
                "exactly-once execution is not claimed",
            ],
        },
        "privacyBoundary": (
            "Worker lease smoke reads DSN only from the named environment variable and writes only hashes/check names; "
            "summary must not contain DSN, username, password, callback URL, secret, report body or user input."
        ),
        "nonClaims": [
            "does_not_prove_production_ready",
            "does_not_prove_job_execution_worker_lease",
            "does_not_prove_exactly_once",
            "does_not_prove_public_webhook_live",
            "does_not_prove_external_vault_or_kms",
        ],
    }
    _safe_summary(summary, forbidden_values=(dsn_value, run_id))
    return summary


def blocked_summary(*, reason: str, dsn_env_name: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_worker_lease_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "blocked",
        "database": {"databaseUrlEnv": dsn_env_name},
        "checks": [{"name": "environment_ready", "ok": False, "details": reason}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres worker lease smoke did not run",
                "job execution worker lease is not implemented",
                "public webhook live delivery not verified",
            ],
        },
        "privacyBoundary": "Blocked summary does not read or output DSN, username, password, callback URL, token, secret or report body.",
        "nonClaims": ["does_not_connect_to_postgres", "does_not_verify_worker_lease"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres webhook outbox worker lease negative smoke。")
    parser.add_argument(
        "--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="worker lease smoke summary JSON 输出路径。"
    )
    parser.add_argument(
        "--database-url-env",
        default=DEFAULT_DSN_ENV_NAME,
        help="保存 Postgres DSN 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument("--schema-name", default="", help="可选 smoke schema 名；默认生成一次性 schema。")
    parser.add_argument("--race-count", type=int, default=5, help="并发 duplicate claim 负例轮数，范围 2-20。")
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
        summary = run_worker_lease_smoke(
            dsn_value=dsn_value,
            dsn_env_name=args.database_url_env,
            schema_name=args.schema_name or None,
            race_count=args.race_count,
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
    except PostgresWorkerLeaseSmokeBlocked as exc:
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
        print(f"postgres worker lease smoke blocked: {exc}", file=sys.stderr)
        return 2
    except PostgresWorkerLeaseSmokeError as exc:
        print(f"postgres worker lease smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
