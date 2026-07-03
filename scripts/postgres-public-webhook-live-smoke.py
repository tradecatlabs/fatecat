#!/usr/bin/env python3
"""Postgres public webhook live smoke.

该脚本连接操作员提供的 Postgres DSN，并向操作员提供的公网 HTTPS
webhook endpoint 投递一条真实 report job 终态事件。输出 JSON 只保留
脱敏证据，不输出 DSN、webhook URL、webhook secret、报告正文或用户输入。
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
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "postgres-public-webhook-live-smoke.json"
)
DEFAULT_DSN_ENV_NAME = "FATE_REPORT_JOB_DATABASE_URL"
DEFAULT_CALLBACK_URL_ENV_NAME = "FATE_WEBHOOK_LIVE_URL"
DEFAULT_CALLBACK_SIGNATURE_ENV_NAME = "FATE_WEBHOOK_LIVE_SECRET"
DEFAULT_CALLBACK_ALLOWED_HOSTS_ENV_NAME = "FATE_WEBHOOK_LIVE_ALLOWED_HOSTS"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|https?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|"
    r"private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)
IDENTIFIER_PATTERN = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class PostgresPublicWebhookLiveSmokeError(RuntimeError):
    """Postgres public webhook live smoke failed."""


class PostgresPublicWebhookLiveSmokeBlocked(RuntimeError):
    """Postgres public webhook live smoke cannot run in this environment."""


@dataclass(frozen=True)
class RuntimeModules:
    report_jobs: Any
    webhook_callbacks: Any
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
        raise PostgresPublicWebhookLiveSmokeBlocked("missing optional dependency: psycopg") from exc

    import report_jobs  # noqa: PLC0415
    import webhook_callbacks  # noqa: PLC0415

    return RuntimeModules(
        report_jobs=report_jobs,
        webhook_callbacks=webhook_callbacks,
        psycopg=psycopg,
        sql=sql,
        dict_row=dict_row,
    )


def _hash_value(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()[:16]


def _database_fingerprint(database_url: str) -> dict[str, Any]:
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


def _webhook_fingerprint(webhook_url: str) -> dict[str, Any]:
    parsed = urlparse(webhook_url)
    host = parsed.hostname or "unknown"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    return {
        "scheme": parsed.scheme or "unknown",
        "hostHash": _hash_value(f"{host}:{port}"),
        "pathHash": _hash_value(path),
        "hasQuery": bool(parsed.query),
    }


def _validate_schema_name(schema_name: str) -> str:
    normalized = str(schema_name or "").strip().lower()
    if not IDENTIFIER_PATTERN.match(normalized):
        raise PostgresPublicWebhookLiveSmokeError("Postgres smoke schema name is not a safe identifier")
    return normalized


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


def _safe_summary(summary: dict[str, Any], *, forbidden_values: tuple[str, ...]) -> None:
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    if SENSITIVE_VALUE_PATTERN.search(serialized):
        raise PostgresPublicWebhookLiveSmokeError("summary contains sensitive-looking inline value")
    for value in forbidden_values:
        if value and value in serialized:
            raise PostgresPublicWebhookLiveSmokeError("summary contains forbidden runtime value")


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise PostgresPublicWebhookLiveSmokeError(f"{name}: {details}")


def _wait_for_webhook_terminal(manager: Any, job_id: str, *, timeout_seconds: float) -> Any:
    deadline = time.monotonic() + max(1.0, float(timeout_seconds))
    last_snapshot = None
    while time.monotonic() < deadline:
        last_snapshot = manager.get(job_id)
        if last_snapshot.status in {"failed", "cancelled", "expired"}:
            return last_snapshot
        if last_snapshot.status == "succeeded" and last_snapshot.callback_outbox:
            outbox = last_snapshot.callback_outbox[0]
            if outbox.status in {"succeeded", "failed"}:
                return last_snapshot
        time.sleep(0.05)
    raise PostgresPublicWebhookLiveSmokeError(
        f"webhook did not reach terminal outbox status: {getattr(last_snapshot, 'status', None)}"
    )


def run_public_webhook_live_smoke(
    *,
    database_url: str,
    webhook_url: str,
    callback_signature: str | None = None,
    allowed_hosts_raw: str | None = None,
    dsn_env_name: str = DEFAULT_DSN_ENV_NAME,
    callback_url_env_name: str = DEFAULT_CALLBACK_URL_ENV_NAME,
    callback_signature_env_name: str = DEFAULT_CALLBACK_SIGNATURE_ENV_NAME,
    schema_name: str | None = None,
    drop_schema: bool = True,
    timeout_seconds: int = 5,
    wait_seconds: float = 12.0,
) -> dict[str, Any]:
    if not str(database_url or "").strip():
        raise PostgresPublicWebhookLiveSmokeBlocked(f"missing {dsn_env_name}")
    if not str(webhook_url or "").strip():
        raise PostgresPublicWebhookLiveSmokeBlocked(f"missing {callback_url_env_name}")

    runtime = _load_runtime()
    started = time.perf_counter()
    checks: list[dict[str, Any]] = []
    run_id = secrets.token_hex(8)
    schema = _validate_schema_name(schema_name or f"fatecat_pub_webhook_{run_id}")
    connect = _connect_factory(runtime, database_url, schema)
    cleanup_error: str | None = None
    report_body = "# 命理排盘报告：测试用户"
    sample_name = "测试用户"
    sample_place = "北京"
    allowed_hosts = runtime.webhook_callbacks.parse_allowed_hosts(allowed_hosts_raw)
    webhook_config = runtime.webhook_callbacks.WebhookConfig(
        url=webhook_url,
        secret=callback_signature,
        allowed_hosts=allowed_hosts,
    )
    dispatcher = runtime.webhook_callbacks.HttpWebhookDispatcher(timeout_seconds=timeout_seconds)

    try:
        store = runtime.report_jobs.PostgresReportJobStore(
            database_url,
            connect_factory=connect,
            initialize_schema=True,
        )
        manager = runtime.report_jobs.ReportJobManager(
            max_workers=1,
            queue_size=4,
            ttl_seconds=120,
            store=store,
            webhook_dispatcher=dispatcher.deliver,
            callback_policy=runtime.report_jobs.ReportJobWebhookPolicy(max_attempts=1),
            job_execution_lease_seconds=5,
        )
        _check(checks, "schema_initialized", True, "disposable schema initialized")
        _check(checks, "webhook_config_validated", True, "public webhook URL accepted by WebhookConfig")

        created = manager.submit(
            kind="postgres_public_webhook_live_smoke",
            report_system="bazi",
            input_summary={"name": sample_name, "birthPlace": sample_place},
            webhook_config=webhook_config,
            task=lambda: {
                "reportSystem": "bazi",
                "markdown": report_body,
                "smoke": "postgres-public-webhook-live",
            },
        )
        snapshot = _wait_for_webhook_terminal(manager, created.job_id, timeout_seconds=wait_seconds)
        event_types = [event.event_type for event in snapshot.events]
        outbox = snapshot.callback_outbox[0] if snapshot.callback_outbox else None
        _check(checks, "job_succeeded", snapshot.status == "succeeded", snapshot.status)
        _check(checks, "outbox_created", outbox is not None, "outbox present")
        _check(checks, "webhook_outbox_succeeded", outbox is not None and outbox.status == "succeeded", "succeeded")
        _check(
            checks,
            "webhook_delivery_event_recorded",
            "webhook.delivery_succeeded" in event_types,
            ",".join(event_types),
        )
        _check(
            checks,
            "webhook_signature_mode",
            outbox is not None and outbox.signature_mode == webhook_config.signature_mode,
            webhook_config.signature_mode,
        )
    finally:
        try:
            if drop_schema:
                _drop_schema(runtime, database_url, schema)
        except Exception as exc:  # noqa: BLE001 - cleanup failure must be reported without DSN.
            cleanup_error = type(exc).__name__

    if cleanup_error:
        _check(checks, "cleanup", False, cleanup_error)
    else:
        _check(checks, "cleanup", True, "smoke schema dropped" if drop_schema else "schema retained by request")

    elapsed = round((time.perf_counter() - started) * 1000, 3)
    outbox_status = None if outbox is None else outbox.status
    outbox_attempts = None if outbox is None else outbox.attempts
    result_status_code = None if outbox is None else outbox.result_status_code
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_public_webhook_live_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "elapsedMs": elapsed,
        "database": {
            "databaseUrlEnv": dsn_env_name,
            "target": _database_fingerprint(database_url),
            "schemaHash": _hash_value(schema),
        },
        "webhook": {
            "urlEnv": callback_url_env_name,
            "secretEnv": callback_signature_env_name if callback_signature else None,
            "target": _webhook_fingerprint(webhook_url),
            "signatureMode": webhook_config.signature_mode,
            "allowedHostsConfigured": bool(allowed_hosts),
            "allowedHostsCount": len(allowed_hosts),
        },
        "checks": checks,
        "liveEvidence": {
            "jobStatus": snapshot.status,
            "outboxStatus": outbox_status,
            "outboxAttempts": outbox_attempts,
            "resultStatusCode": result_status_code,
            "deliveryEventRecorded": "webhook.delivery_succeeded" in event_types,
            "eventTypes": event_types,
            "publicWebhookLiveDelivery": True,
        },
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "public webhook live delivery smoke passed, but external Vault/KMS is not verified",
                "long-running multi-replica worker is not verified",
                "exactly-once execution is not claimed",
                "webhook receiver SLA is outside this repository",
            ],
        },
        "privacyBoundary": (
            "Live smoke reads DSN, webhook URL and optional secret only from named environment variables; "
            "summary stores only hashes, check names, event types and status codes."
        ),
        "nonClaims": [
            "does_not_prove_production_ready",
            "does_not_prove_multi_replica_ready",
            "does_not_prove_exactly_once",
            "does_not_prove_external_vault_or_kms",
            "does_not_prove_webhook_receiver_sla",
            "does_not_prove_heartbeat_polling_worker",
        ],
    }
    _safe_summary(
        summary,
        forbidden_values=(
            database_url,
            webhook_url,
            callback_signature or "",
            allowed_hosts_raw or "",
            report_body,
            sample_name,
            sample_place,
        ),
    )
    return summary


def blocked_summary(
    *,
    reason: str,
    dsn_env_name: str,
    callback_url_env_name: str,
    callback_signature_env_name: str,
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_public_webhook_live_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "blocked",
        "database": {"databaseUrlEnv": dsn_env_name},
        "webhook": {
            "urlEnv": callback_url_env_name,
            "secretEnv": callback_signature_env_name,
        },
        "checks": [{"name": "environment_ready", "ok": False, "details": reason}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres public webhook live smoke did not run",
                "public webhook live delivery not verified",
                "external Vault/KMS and production secret lifecycle not verified",
                "exactly-once execution is not claimed",
            ],
        },
        "privacyBoundary": (
            "Blocked summary names environment variables only; it does not output DSN, webhook URL, "
            "token, secret, report body or user input."
        ),
        "nonClaims": [
            "does_not_connect_to_postgres",
            "does_not_verify_public_webhook_live",
            "does_not_verify_external_vault_or_kms",
        ],
    }


def failed_summary(
    *,
    error_type: str,
    dsn_env_name: str,
    callback_url_env_name: str,
    callback_signature_env_name: str,
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_public_webhook_live_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "failed",
        "database": {"databaseUrlEnv": dsn_env_name},
        "webhook": {
            "urlEnv": callback_url_env_name,
            "secretEnv": callback_signature_env_name,
        },
        "checks": [{"name": "public_webhook_live_smoke", "ok": False, "details": error_type}],
        "shipGate": {
            "status": "blocked",
            "reasons": [
                "Postgres public webhook live smoke failed",
                "public webhook live delivery not verified",
            ],
        },
        "privacyBoundary": "Failed summary contains only exception type and env var names; runtime values are omitted.",
        "nonClaims": ["does_not_verify_public_webhook_live"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat Postgres public webhook live smoke。")
    parser.add_argument(
        "--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="live smoke summary JSON 输出路径。"
    )
    parser.add_argument(
        "--database-url-env",
        default=DEFAULT_DSN_ENV_NAME,
        help="保存 Postgres DSN 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument(
        "--webhook-url-env",
        default=DEFAULT_CALLBACK_URL_ENV_NAME,
        help="保存公网 webhook URL 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument(
        "--webhook-secret-env",
        default=DEFAULT_CALLBACK_SIGNATURE_ENV_NAME,
        help="保存 webhook HMAC secret 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument(
        "--webhook-allowed-hosts-env",
        default=DEFAULT_CALLBACK_ALLOWED_HOSTS_ENV_NAME,
        help="保存 webhook allowlist 的环境变量名；脚本不会输出该变量的值。",
    )
    parser.add_argument("--schema-name", default="", help="可选 smoke schema 名；默认生成一次性 schema。")
    parser.add_argument("--keep-schema", action="store_true", help="保留 smoke schema；默认 drop schema cascade。")
    parser.add_argument("--timeout-seconds", type=int, default=5, help="单次 webhook HTTP timeout。")
    parser.add_argument("--wait-seconds", type=float, default=12.0, help="等待 job/outbox 终态的秒数。")
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="缺少 DSN、webhook URL 或 psycopg 时写入 blocked summary 并返回 0；用于本地无外部环境巡检。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    database_url = os.getenv(args.database_url_env, "").strip()
    webhook_url = os.getenv(args.webhook_url_env, "").strip()
    callback_signature = os.getenv(args.webhook_secret_env, "").strip() or None
    allowed_hosts_raw = os.getenv(args.webhook_allowed_hosts_env, "").strip() or None
    try:
        summary = run_public_webhook_live_smoke(
            database_url=database_url,
            webhook_url=webhook_url,
            callback_signature=callback_signature,
            allowed_hosts_raw=allowed_hosts_raw,
            dsn_env_name=args.database_url_env,
            callback_url_env_name=args.webhook_url_env,
            callback_signature_env_name=args.webhook_secret_env,
            schema_name=args.schema_name or None,
            drop_schema=not args.keep_schema,
            timeout_seconds=args.timeout_seconds,
            wait_seconds=args.wait_seconds,
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
    except PostgresPublicWebhookLiveSmokeBlocked as exc:
        if args.allow_missing:
            summary = blocked_summary(
                reason=str(exc),
                dsn_env_name=args.database_url_env,
                callback_url_env_name=args.webhook_url_env,
                callback_signature_env_name=args.webhook_secret_env,
            )
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
        print(f"postgres public webhook live smoke blocked: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - CLI must write sanitized failed evidence for live operators.
        summary = failed_summary(
            error_type=type(exc).__name__,
            dsn_env_name=args.database_url_env,
            callback_url_env_name=args.webhook_url_env,
            callback_signature_env_name=args.webhook_secret_env,
        )
        write_summary(summary, args.output_json)
        print(f"postgres public webhook live smoke error: {type(exc).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
