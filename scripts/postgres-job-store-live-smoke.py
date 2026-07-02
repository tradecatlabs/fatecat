#!/usr/bin/env python3
"""Postgres ReportJobStore live smoke.

该脚本连接操作员提供的 Postgres DSN，使用独立 schema 执行真实 schema 初始化与
ReportJobStore 读写 smoke。输出 JSON 只保留脱敏证据，不输出 DSN、用户名、密码、
webhook URL、webhook secret 或报告正文。
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
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-job-store-live-smoke.json"
DEFAULT_DSN_ENV_NAME = "FATE_REPORT_JOB_DATABASE_URL"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)
IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class PostgresJobStoreLiveSmokeError(RuntimeError):
    """Postgres ReportJobStore live smoke failed."""


class PostgresJobStoreLiveSmokeBlocked(RuntimeError):
    """Postgres ReportJobStore live smoke cannot run in this environment."""


@dataclass(frozen=True)
class RuntimeModules:
    report_jobs: Any
    fernet_cls: Any
    config_codec_cls: Any
    stored_config_cls: Any
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
        raise PostgresJobStoreLiveSmokeBlocked("missing optional dependency: psycopg") from exc

    from cryptography.fernet import Fernet  # noqa: PLC0415

    import report_jobs  # noqa: PLC0415
    from webhook_config_store import FernetWebhookConfigCodec, StoredWebhookDeliveryConfig  # noqa: PLC0415

    return RuntimeModules(
        report_jobs=report_jobs,
        fernet_cls=Fernet,
        config_codec_cls=FernetWebhookConfigCodec,
        stored_config_cls=StoredWebhookDeliveryConfig,
        psycopg=psycopg,
        sql=sql,
        dict_row=dict_row,
    )


def _hash_value(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()[:16]


def _target_fingerprint(database_url: str) -> dict[str, Any]:
    parsed = urlparse(database_url)
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


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise PostgresJobStoreLiveSmokeError(f"{name}: {details}")


def _validate_schema_name(schema_name: str) -> str:
    normalized = str(schema_name or "").strip().lower()
    if not IDENTIFIER_PATTERN.match(normalized):
        raise PostgresJobStoreLiveSmokeError("Postgres smoke schema name is not a safe identifier")
    return normalized


def _safe_summary(summary: dict[str, Any], *, forbidden_values: tuple[str, ...]) -> None:
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    if SENSITIVE_VALUE_PATTERN.search(serialized):
        raise PostgresJobStoreLiveSmokeError("summary contains sensitive-looking inline value")
    for value in forbidden_values:
        if value and value in serialized:
            raise PostgresJobStoreLiveSmokeError("summary contains forbidden runtime secret value")


def _connect_factory(runtime: RuntimeModules, database_url: str, schema_name: str):
    def connect() -> Any:
        conn = runtime.psycopg.connect(database_url, row_factory=runtime.dict_row)
        conn.execute(runtime.sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(runtime.sql.Identifier(schema_name)))
        conn.execute(runtime.sql.SQL("SET search_path TO {}, public").format(runtime.sql.Identifier(schema_name)))
        return conn

    return connect


def _drop_schema(runtime: RuntimeModules, database_url: str, schema_name: str) -> None:
    with runtime.psycopg.connect(database_url) as conn:
        conn.execute(runtime.sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(runtime.sql.Identifier(schema_name)))


def _cleanup_rows(store: Any, job_id: str, outbox_id: str) -> None:
    # Fallback cleanup when schema drop is disabled. Values are generated smoke IDs only.
    with store._connect() as conn:  # noqa: SLF001 - smoke operates at backend boundary.
        conn.execute(
            "DELETE FROM report_job_webhook_delivery_config WHERE outbox_id = %(outbox_id)s", {"outbox_id": outbox_id}
        )
        conn.execute("DELETE FROM report_job_webhook_outbox WHERE outbox_id = %(outbox_id)s", {"outbox_id": outbox_id})
        conn.execute("DELETE FROM report_job_events WHERE job_id = %(job_id)s", {"job_id": job_id})
        conn.execute("DELETE FROM report_jobs WHERE job_id = %(job_id)s", {"job_id": job_id})


def run_live_smoke(
    *,
    database_url: str,
    dsn_env_name: str = DEFAULT_DSN_ENV_NAME,
    schema_name: str | None = None,
    drop_schema: bool = True,
) -> dict[str, Any]:
    if not str(database_url or "").strip():
        raise PostgresJobStoreLiveSmokeBlocked(f"missing {dsn_env_name}")

    runtime = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []
    run_id = secrets.token_hex(8)
    schema = _validate_schema_name(schema_name or f"fatecat_smoke_{run_id}")
    now = runtime.report_jobs.now_cn()
    job_id = f"pg-live-smoke-job-{run_id}"
    outbox_id = f"pg-live-smoke-outbox-{run_id}"
    event_id = f"pg-live-smoke-event-{run_id}"
    idempotency_key = f"pg-live-smoke-idem-{run_id}"
    lease_owner_a = f"pg-live-smoke-worker-a-{run_id}"
    lease_owner_b = f"pg-live-smoke-worker-b-{run_id}"
    webhook_url = "https://callback.example/postgres-live-smoke"
    webhook_secret = "dummy-webhook-shared-value"
    report_body = "# 命理排盘报告：测试样本"
    target_host_hash = _hash_value("callback.example")

    old_key = runtime.fernet_cls.generate_key().decode("ascii")
    new_key = runtime.fernet_cls.generate_key().decode("ascii")
    old_codec = runtime.config_codec_cls(keys={"old": old_key, "new": new_key}, active_key_id="old")
    new_codec = runtime.config_codec_cls(keys={"old": old_key, "new": new_key}, active_key_id="new")
    store = None
    cleanup_error: str | None = None
    try:
        store = runtime.report_jobs.PostgresReportJobStore(
            database_url,
            webhook_config_codec=old_codec,
            connect_factory=_connect_factory(runtime, database_url, schema),
            initialize_schema=True,
        )
        _check(checks, "schema_initialized", True, "schema created and DDL executed")

        job = runtime.report_jobs._ReportJob(  # noqa: SLF001 - smoke validates persistence adapter roundtrip.
            job_id=job_id,
            kind="postgres_live_smoke",
            report_system="bazi",
            task=None,
            task_payload={"factory": "smoke", "version": 1},
            input_summary={"name": "测试用户", "birthPlace": "北京"},
            idempotency_key=idempotency_key,
            webhook_config=None,
            created_monotonic=time.monotonic(),
            expires_monotonic=time.monotonic() + 120,
            created_at=now.isoformat(),
            expires_at=(now + timedelta(seconds=120)).isoformat(),
            status="queued",
            result={"reportSystem": "bazi", "markdown": report_body},
            max_attempts=2,
            attempt_timeout_seconds=3.0,
            retry_backoff_seconds=0.1,
        )
        store.save_job(job)
        loaded_jobs = [loaded for loaded in store.load_jobs() if loaded.job_id == job_id]
        _check(checks, "job_roundtrip", len(loaded_jobs) == 1, str(len(loaded_jobs)))
        loaded_job = loaded_jobs[0]
        _check(checks, "idempotency_roundtrip", loaded_job.idempotency_key == idempotency_key, "matched")
        _check(
            checks, "task_payload_roundtrip", loaded_job.task_payload == {"factory": "smoke", "version": 1}, "matched"
        )

        event = runtime.report_jobs.ReportJobEvent(
            event_id=event_id,
            job_id=job_id,
            event_type="job.queued",
            status="queued",
            created_at=now.isoformat(),
            message="postgres live smoke event",
            metadata={"smoke": True},
        )
        store.append_job_event(event)
        store.append_job_event(event)
        events = store.load_job_events(job_id)
        _check(checks, "event_idempotency", len(events) == 1 and events[0].event_id == event_id, str(len(events)))

        record = runtime.report_jobs.ReportJobWebhookOutboxRecord(
            outbox_id=outbox_id,
            job_id=job_id,
            event_type=runtime.report_jobs.REPORT_JOB_WEBHOOK_EVENT_TYPE,
            job_status="succeeded",
            status="failed",
            attempts=1,
            max_attempts=2,
            signature_mode="hmac-sha256",
            target_host_hash=target_host_hash,
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
            completed_at=None,
            last_error_type="SmokeTransportError",
            result_status_code=500,
        )
        store.save_webhook_outbox_record(record)
        loaded_outbox = store.load_webhook_outbox_records(job_id)
        _check(
            checks,
            "outbox_roundtrip",
            len(loaded_outbox) == 1 and loaded_outbox[0].outbox_id == outbox_id,
            str(len(loaded_outbox)),
        )
        _check(
            checks,
            "outbox_redeliverable_before_claim",
            len(store.load_redeliverable_webhook_outbox_records()) == 1,
            "visible",
        )
        claimed_by_a = store.claim_webhook_outbox_record(record, lease_owner=lease_owner_a, lease_seconds=30)
        _check(checks, "worker_a_claims", claimed_by_a is not None, "claimed")
        _check(
            checks, "leased_record_hidden_from_scan", not store.load_redeliverable_webhook_outbox_records(), "hidden"
        )
        _check(
            checks,
            "worker_b_cannot_double_claim",
            store.claim_webhook_outbox_record(record, lease_owner=lease_owner_b, lease_seconds=30) is None,
            "blocked",
        )
        store.release_webhook_outbox_record(outbox_id, lease_owner=lease_owner_a)
        claimed_by_b = store.claim_webhook_outbox_record(record, lease_owner=lease_owner_b, lease_seconds=30)
        _check(checks, "worker_b_claims_after_release", claimed_by_b is not None, "claimed")
        store.release_webhook_outbox_record(outbox_id, lease_owner=lease_owner_b)

        runtime_config = runtime.stored_config_cls(url=webhook_url, secret=webhook_secret)
        store.save_webhook_delivery_config(record, runtime_config)
        _check(checks, "encrypted_config_count", store.count_webhook_delivery_configs() == 1, "one encrypted config")
        loaded_config = store.load_webhook_delivery_config(record)
        _check(
            checks,
            "encrypted_config_roundtrip",
            loaded_config is not None and loaded_config.signature_mode == "hmac-sha256",
            "decrypted in memory",
        )
        store.webhook_config_codec = new_codec
        _check(checks, "rotation_count", store.rotate_webhook_delivery_configs() == 1, "rotated")
        store.delete_webhook_delivery_config(outbox_id)
        _check(checks, "encrypted_config_deleted", store.count_webhook_delivery_configs() == 0, "deleted")
    finally:
        if store is not None:
            try:
                if drop_schema:
                    _drop_schema(runtime, database_url, schema)
                else:
                    _cleanup_rows(store, job_id, outbox_id)
            except Exception as exc:  # noqa: BLE001 - cleanup failure must be reported but not expose DSN.
                cleanup_error = type(exc).__name__

    if cleanup_error:
        _check(checks, "cleanup", False, cleanup_error)
    else:
        _check(checks, "cleanup", True, "smoke schema dropped" if drop_schema else "smoke rows deleted")

    elapsed = round((time.perf_counter() - started) * 1000, 3)
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_job_store_live_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": elapsed,
        "database": {
            "databaseUrlEnv": dsn_env_name,
            "target": _target_fingerprint(database_url),
            "schemaHash": _hash_value(schema),
        },
        "checks": checks,
        "liveEvidence": {
            "schemaInitialized": True,
            "jobRoundtrip": True,
            "eventIdempotency": True,
            "outboxClaimRelease": True,
            "encryptedDeliveryConfig": True,
            "cleanup": cleanup_error is None,
        },
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "production multi-replica worker lease not verified",
                "public webhook live delivery not verified",
                "external Vault/KMS and production secret lifecycle not verified",
                "exactly-once execution is not claimed",
            ],
        },
        "privacyBoundary": (
            "Live smoke reads DSN only from the named environment variable and writes only hashes/check names; "
            "summary must not contain DSN, username, password, webhook URL, webhook secret, report body or user input."
        ),
        "nonClaims": [
            "does_not_prove_production_ready",
            "does_not_prove_multi_replica_worker_lease",
            "does_not_prove_exactly_once",
            "does_not_prove_public_webhook_live",
            "does_not_prove_external_vault_or_kms",
        ],
    }
    _safe_summary(
        summary,
        forbidden_values=(
            database_url,
            webhook_url,
            webhook_secret,
            report_body,
            lease_owner_a,
            lease_owner_b,
            old_key,
            new_key,
        ),
    )
    return summary


def blocked_summary(*, reason: str, dsn_env_name: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_job_store_live_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "blocked",
        "database": {"databaseUrlEnv": dsn_env_name},
        "checks": [{"name": "environment_ready", "ok": False, "details": reason}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres live smoke did not run",
                "production multi-replica worker lease not verified",
                "public webhook live delivery not verified",
            ],
        },
        "privacyBoundary": "Blocked summary does not read or output DSN, username, password, webhook URL, token, secret or report body.",
        "nonClaims": ["does_not_connect_to_postgres", "does_not_verify_external_live"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres ReportJobStore live smoke。")
    parser.add_argument(
        "--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="live smoke summary JSON 输出路径。"
    )
    parser.add_argument(
        "--database-url-env",
        default=DEFAULT_DSN_ENV_NAME,
        help="保存 Postgres DSN 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument("--schema-name", default="", help="可选 smoke schema 名；默认生成一次性 schema。")
    parser.add_argument(
        "--keep-schema", action="store_true", help="保留 schema，仅删除 smoke rows。默认 drop schema cascade。"
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="缺少 DSN 或 psycopg 时写入 blocked summary 并返回 0；用于本地无外部环境巡检。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    database_url = os.getenv(args.database_url_env, "").strip()
    try:
        summary = run_live_smoke(
            database_url=database_url,
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
    except PostgresJobStoreLiveSmokeBlocked as exc:
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
        print(f"postgres job store live smoke blocked: {exc}", file=sys.stderr)
        return 2
    except PostgresJobStoreLiveSmokeError as exc:
        print(f"postgres job store live smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
