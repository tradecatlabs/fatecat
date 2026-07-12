import asyncio
import hashlib
import json
import logging
import os
import secrets
import sys
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import BoundedSemaphore, Lock
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

from _paths import ASSETS_DIR, FATE_CORE_SRC_DIR, RUNTIME_DATABASE_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from service_config import cors_allow_origins, env_flag, env_int
from utils.timezone import now_cn
from webhook_config_store import FernetWebhookConfigCodec, WebhookConfigStoreError

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

try:
    load_dotenv(get_env_file(), override=False)
except FileNotFoundError:
    pass

SERVICE_HOST = os.getenv("FATE_SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = int(os.getenv("FATE_SERVICE_PORT", "8001"))
API_TOKEN = os.getenv("FATE_API_TOKEN", "").strip()
MAX_REQUEST_BYTES = env_int("FATE_MAX_REQUEST_BYTES", 1_048_576, minimum=1024)
REQUEST_TIMEOUT_SECONDS = env_int("FATE_REQUEST_TIMEOUT_SECONDS", 30, minimum=1)
RATE_LIMIT_PER_MINUTE = env_int("FATE_RATE_LIMIT_PER_MINUTE", 120, minimum=0)
MAX_INFLIGHT_CALCULATIONS = env_int("FATE_MAX_INFLIGHT_CALCULATIONS", 2, minimum=1)
REPORT_JOB_QUEUE_SIZE = env_int("FATE_REPORT_JOB_QUEUE_SIZE", 20, minimum=1)
REPORT_JOB_WORKERS = env_int("FATE_REPORT_JOB_WORKERS", 1, minimum=1)
REPORT_JOB_TTL_SECONDS = env_int("FATE_REPORT_JOB_TTL_SECONDS", 1800, minimum=60)
REPORT_JOB_MAX_ATTEMPTS = env_int("FATE_REPORT_JOB_MAX_ATTEMPTS", 1, minimum=1)
REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS = env_int("FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS", 0, minimum=0)
REPORT_JOB_RETRY_BACKOFF_SECONDS = env_int("FATE_REPORT_JOB_RETRY_BACKOFF_SECONDS", 0, minimum=0)
REPORT_JOB_STORE = os.getenv("FATE_REPORT_JOB_STORE", "memory").strip().lower() or "memory"
REPORT_JOB_DATABASE_URL = os.getenv("FATE_REPORT_JOB_DATABASE_URL", "").strip()
REPORT_JOB_DB_PATH = os.getenv(
    "FATE_REPORT_JOB_DB_PATH",
    str(RUNTIME_DATABASE_DIR / "report_jobs.sqlite"),
).strip()
REPORT_JOB_WEBHOOKS_ENABLED = env_flag("FATE_REPORT_JOB_WEBHOOKS_ENABLED")
WEBHOOK_TIMEOUT_SECONDS = env_int("FATE_WEBHOOK_TIMEOUT_SECONDS", 5, minimum=1)
WEBHOOK_MAX_ATTEMPTS = env_int("FATE_WEBHOOK_MAX_ATTEMPTS", 1, minimum=1)
WEBHOOK_RETRY_BACKOFF_SECONDS = env_int("FATE_WEBHOOK_RETRY_BACKOFF_SECONDS", 0, minimum=0)
WEBHOOK_REDELIVERY_LEASE_SECONDS = env_int("FATE_WEBHOOK_REDELIVERY_LEASE_SECONDS", 30, minimum=1)
WEBHOOK_ALLOWED_HOSTS = os.getenv("FATE_WEBHOOK_ALLOWED_HOSTS", "").strip()
WEBHOOK_ALLOW_HTTP = env_flag("FATE_WEBHOOK_ALLOW_HTTP")
WEBHOOK_CONFIG_FERNET_KEYS = os.getenv("FATE_WEBHOOK_CONFIG_FERNET_KEYS", "").strip()
WEBHOOK_CONFIG_ACTIVE_KEY_ID = os.getenv("FATE_WEBHOOK_CONFIG_ACTIVE_KEY_ID", "").strip() or None
AUDIT_LOG_ENABLED = os.getenv("FATE_AUDIT_LOG_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
AUDIT_EVENT_RETENTION_DAYS = env_int("FATE_AUDIT_EVENT_RETENTION_DAYS", 30, minimum=1)
RECORD_RETENTION_DAYS = env_int("FATE_RECORD_RETENTION_DAYS", 0, minimum=0)
TRUST_PROXY_HEADERS = env_flag("FATE_TRUST_PROXY_HEADERS")
ENABLE_HSTS = env_flag("FATE_ENABLE_HSTS")

import db_v2 as db  # noqa: E402
from calculation_service import calculate_delivery_result  # noqa: E402
from fate_core.capabilities import (  # noqa: E402
    CapabilityExecutor,
    CapabilityInput,
    build_markdown_report_policy_gate,
    build_markdown_snapshot_gate,
    build_report_policy_gate,
    get_capability,
    get_provider,
    get_provider_for_capability,
    list_capabilities,
    list_providers,
)
from fate_core.observability import (  # noqa: E402
    current_trace_id,
    current_traceparent,
    reset_trace_context,
    set_trace_context,
    trace_context_from_traceparent,
    trace_span,
)
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis  # noqa: E402
from liuyao_factors import generate_factor  # noqa: E402
from location import (  # noqa: E402
    NormalizedBirthTime,
    ResolvedLocation,
    catalog_status,
    normalize_birth_time,
    resolve_coordinates,
    search_records,
)
from location import (  # noqa: E402
    resolve as resolve_location,
)
from models import (  # noqa: E402
    BaziData,
    BaziRequest,
    BaziResponse,
    BrandingInfo,
    LiuyaoFactorData,
    LiuyaoFactorRequest,
    LiuyaoFactorResponse,
    Meta,
    TimeInfo,
)
from prediction_systems import enabled_report_system_ids, prediction_systems_payload  # noqa: E402
from rate_limiter import get_queue_status  # noqa: E402
from report_generator import (  # noqa: E402
    generate_full_report,
    normalize_report_system,
    public_birth_place,
)
from report_jobs import (  # noqa: E402
    PostgresReportJobStore,
    ReportJobEvent,
    ReportJobExecutionPolicy,
    ReportJobManager,
    ReportJobNotFound,
    ReportJobQueueFull,
    ReportJobSnapshot,
    ReportJobWebhookOutboxRecord,
    ReportJobWebhookPolicy,
    SQLiteReportJobStore,
)
from telegram_webhook import (  # noqa: E402
    TELEGRAM_DELIVERY_PATH,
    TelegramWebhookConfig,
    TelegramWebhookDisabled,
    TelegramWebhookInvalidUpdate,
    TelegramWebhookQueueFull,
    TelegramWebhookRuntime,
    TelegramWebhookUnauthorized,
)
from web_forms import WebReportForm, WebReportJobView, WebReportResult  # noqa: E402
from web_report_service import build_web_report_result, validate_web_report_form  # noqa: E402
from web_ui import render_web_report_page  # noqa: E402
from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig, parse_allowed_hosts  # noqa: E402

logger = logging.getLogger(__name__)
telegram_webhook_runtime = TelegramWebhookRuntime(TelegramWebhookConfig.from_env())
_request_id_context: ContextVar[str | None] = ContextVar("fatecat_request_id", default=None)
_metrics_lock = Lock()
_request_counts: dict[tuple[str, str, int], int] = defaultdict(int)
_request_latency_seconds: dict[tuple[str, str, int], float] = defaultdict(float)
_request_latency_buckets: dict[tuple[str, str, int, str], int] = defaultdict(int)
_request_error_counts: dict[tuple[str, str, int, str], int] = defaultdict(int)
_inflight_requests = 0
_calculation_slots = BoundedSemaphore(MAX_INFLIGHT_CALCULATIONS)
_calculation_slots_lock = Lock()
_calculation_slots_in_use = 0
_rate_limit_lock = Lock()
_rate_limit_windows: dict[str, deque[float]] = defaultdict(deque)
_RATE_LIMIT_EXEMPT_PATHS = {"/health", "/live", "/ready", "/metrics", TELEGRAM_DELIVERY_PATH}
_REQUEST_LATENCY_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
_BODY_LIMIT_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _build_webhook_config_codec() -> FernetWebhookConfigCodec | None:
    try:
        return FernetWebhookConfigCodec.from_raw(
            WEBHOOK_CONFIG_FERNET_KEYS,
            active_key_id=WEBHOOK_CONFIG_ACTIVE_KEY_ID,
        )
    except WebhookConfigStoreError as exc:
        raise RuntimeError("FATE_WEBHOOK_CONFIG_FERNET_KEYS 配置无效") from exc


def _build_report_job_manager() -> ReportJobManager:
    store = None
    if REPORT_JOB_STORE == "sqlite":
        db_path = Path(REPORT_JOB_DB_PATH)
        if not db_path.is_absolute():
            db_path = RUNTIME_DATABASE_DIR / db_path
        store = SQLiteReportJobStore(db_path, webhook_config_codec=_build_webhook_config_codec())
    elif REPORT_JOB_STORE == "postgres":
        store = PostgresReportJobStore(
            REPORT_JOB_DATABASE_URL,
            webhook_config_codec=_build_webhook_config_codec(),
        )
    elif REPORT_JOB_STORE != "memory":
        raise RuntimeError("FATE_REPORT_JOB_STORE 只支持 memory、sqlite 或 postgres")
    return ReportJobManager(
        max_workers=REPORT_JOB_WORKERS,
        queue_size=REPORT_JOB_QUEUE_SIZE,
        ttl_seconds=REPORT_JOB_TTL_SECONDS,
        store=store,
        webhook_dispatcher=HttpWebhookDispatcher(timeout_seconds=WEBHOOK_TIMEOUT_SECONDS).deliver,
        execution_policy=ReportJobExecutionPolicy(
            max_attempts=REPORT_JOB_MAX_ATTEMPTS,
            attempt_timeout_seconds=REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS or None,
            retry_backoff_seconds=REPORT_JOB_RETRY_BACKOFF_SECONDS,
        ),
        callback_policy=ReportJobWebhookPolicy(
            max_attempts=WEBHOOK_MAX_ATTEMPTS,
            retry_backoff_seconds=WEBHOOK_RETRY_BACKOFF_SECONDS,
        ),
        **{"webhook_redelivery_lease_seconds": WEBHOOK_REDELIVERY_LEASE_SECONDS},
        task_factories=_report_job_task_factories(),
    )


def _records_enabled() -> bool:
    return os.getenv("FATE_RECORDS_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}


if _records_enabled():
    db.ensure_db()


RECORD_SCOPE_READ = "record.read"
RECORD_SCOPE_LIST = "record.list"
RECORD_SCOPE_WRITE = "record.write"
RECORD_SCOPE_DELETE = "record.delete"
RECORD_SCOPES = frozenset(
    {
        RECORD_SCOPE_READ,
        RECORD_SCOPE_LIST,
        RECORD_SCOPE_WRITE,
        RECORD_SCOPE_DELETE,
    }
)
ADMIN_RECORD_SCOPES = RECORD_SCOPES
DEFAULT_USER_RECORD_SCOPES = RECORD_SCOPES
SANDBOX_TOKEN_CONTRACT_PATH = ASSETS_DIR / "developer" / "sandbox-token-contract.json"
SANDBOX_SCOPE_PREFIX = "capability:calculate:"


@dataclass(frozen=True)
class ApiPrincipal:
    role: str
    user_id: str | None = None
    scopes: frozenset[str] = field(default_factory=frozenset)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes


class RequestBodyLimitMiddleware:
    """在 Starlette BaseHTTPMiddleware 外层限制请求体大小。"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("method") not in _BODY_LIMIT_METHODS:
            await self.app(scope, receive, send)
            return

        request_id = self._request_id(scope)
        content_length = self._header(scope, b"content-length")
        if content_length:
            try:
                if int(content_length.decode("latin-1")) > MAX_REQUEST_BYTES:
                    await self._send_json_error(scope, receive, send, request_id, 413, "请求体过大")
                    return
            except ValueError:
                await self._send_json_error(scope, receive, send, request_id, 400, "Content-Length 无效")
                return

        received = 0
        chunks: list[bytes] = []
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                await self.app(scope, self._disconnect_receive, send)
                return
            if message["type"] != "http.request":
                continue
            chunk = message.get("body", b"")
            received += len(chunk)
            if received > MAX_REQUEST_BYTES:
                await self._send_json_error(scope, receive, send, request_id, 413, "请求体过大")
                return
            if chunk:
                chunks.append(chunk)
            if not message.get("more_body", False):
                break

        body = b"".join(chunks)
        consumed = False
        disconnect_wait = asyncio.Event()

        async def replay_receive():
            nonlocal consumed
            if consumed:
                await disconnect_wait.wait()
                return {"type": "http.disconnect"}
            consumed = True
            return {"type": "http.request", "body": body, "more_body": False}

        await self.app(scope, replay_receive, send)

    @staticmethod
    async def _disconnect_receive():
        return {"type": "http.disconnect"}

    @staticmethod
    def _header(scope, name: bytes) -> bytes | None:
        for header_name, value in scope.get("headers", []):
            if header_name.lower() == name:
                return value
        return None

    @classmethod
    def _request_id(cls, scope) -> str:
        raw = cls._header(scope, b"x-request-id")
        if raw:
            return raw.decode("latin-1", errors="ignore")
        return uuid.uuid4().hex

    @staticmethod
    async def _send_json_error(scope, receive, send, request_id: str, status_code: int, error: str) -> None:
        response = _apply_public_response_headers(_json_error(status_code, error), request_id)
        await response(scope, receive, send)


def _extract_auth_token(x_api_key: str | None, authorization: str | None) -> str:
    if x_api_key:
        return x_api_key.strip()
    if authorization:
        scheme, _, value = authorization.strip().partition(" ")
        if scheme.lower() == "bearer" and value:
            return value.strip()
    return ""


def _admin_tokens() -> list[str]:
    tokens = [API_TOKEN, os.getenv("FATE_API_ADMIN_TOKEN", "").strip()]
    return [token for token in dict.fromkeys(tokens) if token]


def _parse_record_scope_list(raw: str) -> frozenset[str]:
    requested = {item.strip() for item in raw.split("|") if item.strip()}
    return frozenset(scope for scope in requested if scope in RECORD_SCOPES)


def _user_token_principals() -> list[tuple[str, ApiPrincipal]]:
    raw = os.getenv("FATE_API_USER_TOKENS", "").strip()
    if not raw:
        return []

    principals: list[tuple[str, ApiPrincipal]] = []
    for item in raw.split(","):
        parts = item.strip().split(":", 2)
        if len(parts) < 2:
            continue
        user_id = parts[0].strip()
        token = parts[1].strip()
        scopes = _parse_record_scope_list(parts[2]) if len(parts) == 3 else DEFAULT_USER_RECORD_SCOPES
        if user_id and token:
            principals.append((token, ApiPrincipal(role="user", user_id=user_id, scopes=scopes)))
    return principals


def _sandbox_allowed_scopes() -> frozenset[str]:
    try:
        contract = json.loads(SANDBOX_TOKEN_CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return frozenset()
    scopes = {
        item.get("scope")
        for item in contract.get("scopes", [])
        if isinstance(item, dict) and isinstance(item.get("scope"), str)
    }
    return frozenset(scopes)


def _parse_sandbox_scope_list(raw: str) -> frozenset[str]:
    allowed_scopes = _sandbox_allowed_scopes()
    requested = {item.strip() for item in raw.split("|") if item.strip()}
    return frozenset(scope for scope in requested if scope in allowed_scopes)


def _sandbox_token_principals() -> list[tuple[str, ApiPrincipal]]:
    raw = os.getenv("FATE_SANDBOX_TOKENS", "").strip()
    if not raw:
        return []

    principals: list[tuple[str, ApiPrincipal]] = []
    for item in raw.split(","):
        parts = item.strip().split(":", 2)
        if len(parts) != 3:
            continue
        subject = parts[0].strip()
        token = parts[1].strip()
        scopes = _parse_sandbox_scope_list(parts[2])
        if subject and token and scopes:
            principals.append((token, ApiPrincipal(role="sandbox", user_id=subject, scopes=scopes)))
    return principals


def _require_record_access(x_api_key: str | None, authorization: str | None) -> ApiPrincipal:
    if not _records_enabled():
        raise HTTPException(status_code=403, detail="记录接口未启用")
    admin_tokens = _admin_tokens()
    user_principals = _user_token_principals()
    if not admin_tokens and not user_principals:
        raise HTTPException(status_code=403, detail="记录接口未启用")
    supplied = _extract_auth_token(x_api_key, authorization)
    if not supplied:
        raise HTTPException(status_code=403, detail="未授权")
    for token in admin_tokens:
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="admin", scopes=ADMIN_RECORD_SCOPES)
    for token, principal in user_principals:
        if secrets.compare_digest(supplied, token):
            return principal
    raise HTTPException(status_code=403, detail="未授权")


def _sandbox_scope_for_capability(capability_id: str) -> str:
    return f"{SANDBOX_SCOPE_PREFIX}{capability_id}"


def _require_sandbox_capability_access(
    capability_id: str,
    x_sandbox_token: str | None,
    authorization: str | None,
) -> ApiPrincipal:
    required_scope = _sandbox_scope_for_capability(capability_id)
    if required_scope not in _sandbox_allowed_scopes():
        raise HTTPException(status_code=403, detail="sandbox capability 未开放")

    principals = _sandbox_token_principals()
    if not principals:
        raise HTTPException(status_code=403, detail="sandbox token gateway 未启用")

    supplied = _extract_auth_token(x_sandbox_token, authorization)
    if not supplied:
        raise HTTPException(status_code=403, detail="sandbox token 缺失")

    for token, principal in principals:
        if secrets.compare_digest(supplied, token):
            _require_scope(principal, required_scope)
            return principal
    raise HTTPException(status_code=403, detail="sandbox token 无效")


def _require_scope(principal: ApiPrincipal, scope: str) -> None:
    if principal.has_scope(scope):
        return
    raise HTTPException(status_code=403, detail="权限不足")


def _require_owner_or_admin(principal: ApiPrincipal, user_id: str) -> None:
    if principal.is_admin:
        return
    if principal.user_id == user_id:
        return
    raise HTTPException(status_code=403, detail="无权访问该记录")


@asynccontextmanager
async def _app_lifespan(_app: FastAPI):
    await telegram_webhook_runtime.start_managed()
    try:
        yield
    finally:
        await telegram_webhook_runtime.stop()


app = FastAPI(title="八字排盘服务", version="1.0.0", lifespan=_app_lifespan)
app.add_middleware(CORSMiddleware, allow_origins=cors_allow_origins(), allow_methods=["*"], allow_headers=["*"])


def _client_key(request: Request) -> str:
    if TRUST_PROXY_HEADERS:
        forwarded_for = request.headers.get("x-forwarded-for", "")
        if forwarded_for:
            return forwarded_for.split(",", 1)[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _route_label(request: Request) -> str:
    route = request.scope.get("route")
    path = getattr(route, "path", None)
    if isinstance(path, str):
        return path
    return request.url.path


def _json_error(status_code: int, error: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=attach_branding({"success": False, "error": error, "statusCode": status_code}),
    )


def _check_rate_limit(request: Request) -> tuple[bool, int]:
    if RATE_LIMIT_PER_MINUTE <= 0 or request.url.path in _RATE_LIMIT_EXEMPT_PATHS:
        return True, 0

    now = time.monotonic()
    key = _client_key(request)
    with _rate_limit_lock:
        window = _rate_limit_windows[key]
        cutoff = now - 60
        while window and window[0] <= cutoff:
            window.popleft()
        if len(window) >= RATE_LIMIT_PER_MINUTE:
            retry_after = max(1, int(60 - (now - window[0])))
            return False, retry_after
        window.append(now)
    return True, 0


def _record_request_metric(
    method: str,
    route: str,
    status_code: int,
    elapsed_seconds: float,
    *,
    error_class: str | None = None,
) -> None:
    key = (method, route, status_code)
    with _metrics_lock:
        _request_counts[key] += 1
        _request_latency_seconds[key] += elapsed_seconds
        for bucket in _REQUEST_LATENCY_BUCKETS:
            if elapsed_seconds <= bucket:
                _request_latency_buckets[(method, route, status_code, _format_bucket(bucket))] += 1
        _request_latency_buckets[(method, route, status_code, "+Inf")] += 1
        if error_class:
            _request_error_counts[(method, route, status_code, error_class)] += 1


def _classify_error(status_code: int) -> str | None:
    if status_code < 400:
        return None
    if status_code == 400:
        return "bad_request"
    if status_code in {401, 403}:
        return "auth"
    if status_code == 404:
        return "not_found"
    if status_code == 413:
        return "body_too_large"
    if status_code == 422:
        return "validation"
    if status_code == 429:
        return "rate_limited"
    if status_code == 504:
        return "timeout"
    if status_code >= 500:
        return "server_error"
    return "client_error"


def _format_bucket(bucket: float) -> str:
    return f"{bucket:g}"


def _escape_metric_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _current_request_id() -> str:
    return _request_id_context.get() or "-"


def _request_id_from_request(request: Request) -> str:
    value = getattr(request.state, "request_id", None)
    if isinstance(value, str) and value:
        return value
    return _current_request_id()


def _log_structured(level: str, payload: dict[str, Any]) -> None:
    message = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    getattr(logger, level)(message)


def _audit_hash(value: Any) -> str:
    return hashlib.sha256(str(value).encode("utf-8", errors="ignore")).hexdigest()[:16]


def _audit_principal_payload(principal: ApiPrincipal | None) -> dict[str, Any]:
    if principal is None:
        return {"actorRole": "anonymous"}
    payload: dict[str, Any] = {"actorRole": principal.role, "scopeCount": len(principal.scopes)}
    if principal.user_id:
        payload["actorUserHash"] = _audit_hash(principal.user_id)
    return payload


def _log_audit_event(
    action: str,
    *,
    principal: ApiPrincipal | None = None,
    target_type: str,
    target_id: Any | None = None,
    outcome: str = "success",
    metadata: dict[str, Any] | None = None,
) -> None:
    if not AUDIT_LOG_ENABLED:
        return
    payload: dict[str, Any] = {
        "event": "audit_event",
        "requestId": _current_request_id(),
        "action": action,
        "targetType": target_type,
        "outcome": outcome,
        "auditRetentionDays": AUDIT_EVENT_RETENTION_DAYS,
    }
    payload.update(_audit_principal_payload(principal))
    if target_id is not None:
        payload["targetIdHash"] = _audit_hash(target_id)
    if metadata:
        payload["metadata"] = metadata
    _log_structured("info", payload)


def _log_business_exception(message: str, *, error_type: str | None = None) -> None:
    payload = {
        "event": "business_error",
        "requestId": _current_request_id(),
        "message": message,
    }
    if error_type:
        payload["errorType"] = error_type
    logger.exception(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


@contextmanager
def _calculation_slot():
    """限制同步命理计算并发，避免超时请求继续堆积计算线程。"""
    global _calculation_slots_in_use
    if not _calculation_slots.acquire(blocking=False):
        raise HTTPException(status_code=503, detail="服务繁忙，请稍后再试")
    with _calculation_slots_lock:
        _calculation_slots_in_use += 1
    try:
        yield
    finally:
        with _calculation_slots_lock:
            _calculation_slots_in_use = max(0, _calculation_slots_in_use - 1)
        _calculation_slots.release()


def _run_with_calculation_slot(fn):
    with _calculation_slot():
        return fn()


def _web_form_from_payload(payload: dict[str, Any]) -> WebReportForm:
    return WebReportForm.from_query(
        birth_date=str(payload.get("birthDate") or ""),
        birth_time=str(payload.get("birthTime") or ""),
        birth_place=str(payload.get("birthPlace") or ""),
        location_mode=str(payload.get("locationMode") or "domestic"),
        location_id=str(payload.get("locationId") or ""),
        time_basis=str(payload.get("timeBasis") or ""),
        fold_choice=str(payload.get("foldChoice") or ""),
        gender=str(payload.get("gender") or ""),
        name=str(payload.get("name") or ""),
        report_system=str(payload.get("reportSystem") or "bazi"),
        submitted="1",
    )


def _web_job_view(snapshot: ReportJobSnapshot) -> WebReportJobView:
    result = snapshot.result if isinstance(snapshot.result, WebReportResult) else None
    return WebReportJobView(
        job_id=snapshot.job_id,
        status=snapshot.status,
        report_system=snapshot.report_system,
        created_at=snapshot.created_at,
        expires_at=snapshot.expires_at,
        started_at=snapshot.started_at,
        finished_at=snapshot.finished_at,
        queue_position=snapshot.queue_position,
        error=snapshot.error,
        result=result,
    )


def _report_job_payload(snapshot: ReportJobSnapshot, *, include_result: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "resourceType": "CalculationJob",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "jobId": snapshot.job_id,
        "id": snapshot.job_id,
        "kind": snapshot.kind,
        "status": snapshot.status,
        "reportSystem": snapshot.report_system,
        "idempotencyKey": snapshot.idempotency_key,
        "queuePosition": snapshot.queue_position,
        "attempts": snapshot.attempts,
        "maxAttempts": snapshot.max_attempts,
        "attemptTimeoutSeconds": snapshot.attempt_timeout_seconds,
        "retryBackoffSeconds": snapshot.retry_backoff_seconds,
        "createdAt": snapshot.created_at,
        "startedAt": snapshot.started_at,
        "finishedAt": snapshot.finished_at,
        "expiresAt": snapshot.expires_at,
        "error": snapshot.error,
        "statusUrl": f"/api/v1/report/jobs/{snapshot.job_id}",
        "cancelUrl": f"/api/v1/report/jobs/{snapshot.job_id}/cancel",
        "webhook": {
            "enabled": snapshot.webhook_enabled,
            "signature": snapshot.webhook_signature,
        },
        "webhookOutbox": [_report_job_webhook_outbox_payload(record) for record in snapshot.callback_outbox],
        "events": [_report_job_event_payload(event) for event in snapshot.events],
        "links": {
            "self": f"/api/v1/report/jobs/{snapshot.job_id}",
            "cancel": f"/api/v1/report/jobs/{snapshot.job_id}/cancel",
            "reports": "/reports",
            "errors": "/errors",
        },
        "input": snapshot.input_summary,
    }
    if include_result and snapshot.status == "succeeded":
        payload["result"] = _serialize_report_job_result(snapshot.result)
    return payload


def _report_job_event_payload(event: ReportJobEvent) -> dict[str, Any]:
    return {
        "resourceType": "CalculationJobEvent",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "eventId": event.event_id,
        "id": event.event_id,
        "jobId": event.job_id,
        "eventType": event.event_type,
        "status": event.status,
        "createdAt": event.created_at,
        "message": event.message,
        "metadata": event.metadata,
    }


def _report_job_webhook_outbox_payload(record: ReportJobWebhookOutboxRecord) -> dict[str, Any]:
    return {
        "resourceType": "CalculationJobWebhookOutbox",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "outboxId": record.outbox_id,
        "id": record.outbox_id,
        "jobId": record.job_id,
        "eventType": record.event_type,
        "jobStatus": record.job_status,
        "status": record.status,
        "attempts": record.attempts,
        "maxAttempts": record.max_attempts,
        "signature": record.signature_mode,
        "targetHostHash": record.target_host_hash,
        "createdAt": record.created_at,
        "updatedAt": record.updated_at,
        "completedAt": record.completed_at,
        "lastErrorType": record.last_error_type,
        "resultStatusCode": record.result_status_code,
        "privacyBoundary": "excludes webhook url, webhook secret, request body, report markdown and user input",
    }


def _serialize_report_job_result(result: Any) -> dict[str, Any] | None:
    if isinstance(result, WebReportResult):
        return {
            "reportSystem": result.report_system,
            "reportSystemLabel": result.report_system_label,
            "markdown": result.markdown,
            "policyGate": result.policy_gate,
            "snapshotGate": result.snapshot_gate,
            "input": result.input_payload,
        }
    if isinstance(result, dict):
        return result
    return None


def _capability_item_payload(item: Any, markdown_enabled_ids: set[str]) -> dict[str, Any]:
    markdown_report_enabled = item.capability_id in markdown_enabled_ids
    return {
        "capabilityId": item.capability_id,
        "name": item.name,
        "tradition": item.tradition,
        "status": item.status,
        "defaultVisibility": item.default_visibility,
        "maturity": {
            "level": item.maturity_level,
            "status": item.maturity_status,
            "summary": item.maturity_summary,
        },
        "engine": {
            "provider": item.provider,
            "engineVersion": item.engine_version,
            "deterministic": item.deterministic,
        },
        "reportProfile": item.report_profile,
        "markdownDefault": item.markdown_default,
        "capabilityApiEnabled": item.status == "production",
        "markdownReportEnabled": markdown_report_enabled,
        "surfaces": {
            "capabilityApi": item.status == "production",
            "markdownReport": markdown_report_enabled,
            "webForm": markdown_report_enabled,
        },
        "evidencePolicy": item.evidence_policy,
        "testGate": item.test_gate,
        "riskLevel": item.risk_level,
        "provider": _capability_provider_payload(item),
    }


def _capability_provider_payload(item: Any) -> dict[str, Any]:
    if item.status != "production":
        return {
            "providerId": item.provider,
            "engineVersion": item.engine_version,
            "health": {
                "status": "blocked",
                "checks": {
                    "reason": "planned capability",
                    "executable": False,
                },
            },
        }
    provider = get_provider_for_capability(item)
    return {
        **provider.metadata().as_dict(),
        "health": provider.health().as_dict(),
    }


def _capability_schema_refs() -> dict[str, str]:
    return {
        "capability": "contracts/fate/capabilities/schemas/capability.schema.json",
        "provider": "contracts/fate/capabilities/schemas/provider.schema.json",
        "report": "contracts/fate/capabilities/schemas/report.schema.json",
        "resource": "contracts/fate/capabilities/schemas/resource.schema.json",
        "input": "contracts/fate/capabilities/schemas/input.schema.json",
        "output": "contracts/fate/capabilities/schemas/output.schema.json",
        "evidence": "contracts/fate/capabilities/schemas/evidence.schema.json",
        "error": "contracts/fate/capabilities/schemas/error.schema.json",
    }


def _capability_resource_payload(item: Any) -> dict[str, Any]:
    markdown_enabled_ids = set(enabled_report_system_ids())
    payload = _capability_item_payload(item, markdown_enabled_ids)
    executable = item.status == "production"
    payload.update(
        {
            "resourceType": "Capability",
            "apiVersion": "fatecat.tradecatlabs/v1",
            "id": item.capability_id,
            "description": item.description,
            "input": {
                "required": list(item.input_required),
                "optional": list(item.input_optional),
            },
            "report": {
                "profile": item.report_profile,
                "markdownDefault": item.markdown_default,
                "markdownEnabled": item.capability_id in markdown_enabled_ids,
            },
            "risk": {
                "riskLevel": item.risk_level,
                "disclaimerRequired": item.disclaimer_required,
                "forbiddenClaims": list(item.forbidden_claims),
            },
            "schemas": _capability_schema_refs(),
            "links": {
                "self": f"/capabilities/{item.capability_id}",
                "collection": "/capabilities",
                "calculate": f"/capabilities/{item.capability_id}/calculate",
                "provider": f"/providers/{item.provider}",
                "errors": "/errors",
            },
            "admission": {
                "executable": executable,
                "reason": "production capability" if executable else "能力尚未生产化，当前只允许发现和审计",
            },
        }
    )
    return payload


def _capabilities_payload() -> dict[str, Any]:
    markdown_enabled_ids = set(enabled_report_system_ids())
    return {"capabilities": [_capability_item_payload(item, markdown_enabled_ids) for item in list_capabilities()]}


def _provider_resource_payload(provider: Any) -> dict[str, Any]:
    metadata = provider.metadata().as_dict()
    provider_id = metadata["providerId"]
    return {
        "resourceType": "Provider",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "id": provider_id,
        **metadata,
        "health": provider.health().as_dict(),
        "links": {
            "self": f"/providers/{provider_id}",
            "collection": "/providers",
            "capabilities": "/capabilities",
            "errors": "/errors",
        },
        "metadata": {
            "interfaceVersion": metadata["interfaceVersion"],
            "adapterType": metadata["adapterType"],
            "healthScope": "in-process",
            "externalConnectivity": "外部连通验证待执行",
        },
    }


def _providers_payload() -> dict[str, Any]:
    return {"providers": [_provider_resource_payload(provider) for provider in list_providers()]}


def _report_sections_from_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for key in data:
        if key == "analysisEvidence":
            continue
        sections.append(
            {
                "id": str(key),
                "type": "jsonField",
                "source": f"data.{key}",
            }
        )
    return sections


def _evidence_refs_from_evidence(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    default_source = str(evidence.get("source", "") or "analysisEvidence")
    root_rule_ids = evidence.get("ruleIds")
    if isinstance(root_rule_ids, list) and root_rule_ids:
        refs.append(
            {
                "id": "root",
                "source": default_source,
                "ruleIds": [str(item) for item in root_rule_ids],
            }
        )

    items = evidence.get("items")
    if isinstance(items, dict):
        for item_id, item in items.items():
            if not isinstance(item, dict):
                continue
            rule_ids = item.get("ruleIds")
            normalized_rule_ids = [str(rule_id) for rule_id in rule_ids] if isinstance(rule_ids, list) else []
            refs.append(
                {
                    "id": str(item_id),
                    "source": str(item.get("source", default_source) or default_source),
                    "ruleIds": normalized_rule_ids,
                    "risk": item.get("risk"),
                    "confidence": item.get("confidence"),
                }
            )
    return refs


def _capability_report_payload(result: Any) -> dict[str, Any]:
    capability = get_capability(result.capability_id)
    provider_id = str(result.metadata.get("engine", {}).get("provider", capability.provider))
    report_id = f"{result.capability_id}:{result.report_profile}:json"
    report = {
        "resourceType": "Report",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "id": report_id,
        "capabilityId": result.capability_id,
        "profile": result.report_profile,
        "formats": ["json"],
        "defaultFormat": "json",
        "markdownDefault": capability.markdown_default,
        "sections": _report_sections_from_data(result.data),
        "evidenceRefs": _evidence_refs_from_evidence(result.evidence),
        "risk": result.risk,
        "links": {
            "capability": f"/capabilities/{result.capability_id}",
            "provider": f"/providers/{provider_id}",
            "schemas": _capability_schema_refs(),
            "errors": "/errors",
        },
        "metadata": {
            "source": "capability-executor",
            "dataRule": "data 保存结构化结果，不直接拼 Markdown。",
            "evidenceRefsRule": "evidenceRefs 是 best-effort 引用索引，原始 evidence 仍完整返回。",
            "snapshotGate": "后续切片实现完整 report snapshot gate。",
        },
    }
    report["policyGate"] = build_report_policy_gate(
        content={
            "sections": report["sections"],
            "metadata": report["metadata"],
        },
        forbidden_claims=result.risk.get("forbiddenClaims", []),
        checked_fields=["report.sections", "report.metadata"],
        excluded_fields=[
            "report.risk.forbiddenClaims",
            "risk.forbiddenClaims",
            "report.policyGate",
        ],
        scope="capability-report-envelope",
        content_coverage="Capability API 的 Report envelope 摘要字段；完整 Markdown snapshot gate 后续单独实现。",
        policy_source="result.risk.forbiddenClaims",
    )
    return report


def _markdown_report_gates(*, report_system: str, markdown: str) -> dict[str, Any]:
    capability = get_capability(report_system)
    return {
        "policyGate": build_markdown_report_policy_gate(
            markdown=markdown,
            forbidden_claims=capability.forbidden_claims,
            report_system=report_system,
        ),
        "snapshotGate": build_markdown_snapshot_gate(markdown=markdown, report_system=report_system),
    }


def _error_catalog_payload() -> dict[str, Any]:
    path = ASSETS_DIR / "capabilities" / "errors.json"
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _evaluation_registry_payload() -> dict[str, Any]:
    path = ASSETS_DIR / "evaluations" / "registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    return {
        "schemaVersion": registry["schemaVersion"],
        "resources": registry["resources"],
        "schemas": registry["schemas"],
        "metadata": registry["metadata"],
    }


def _evaluation_resource_payload(evaluation_id: str) -> dict[str, Any]:
    for item in _evaluation_registry_payload()["resources"]:
        if item["id"] == evaluation_id:
            return item
    raise ValueError(f"未找到评测资源: {evaluation_id}")


def _observability_registry_payload() -> dict[str, Any]:
    path = ASSETS_DIR / "observability" / "registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    return {
        "schemaVersion": registry["schemaVersion"],
        "signals": registry["signals"],
        "schemas": registry["schemas"],
        "metadata": registry["metadata"],
    }


def _observability_signal_payload(signal_id: str) -> dict[str, Any]:
    for item in _observability_registry_payload()["signals"]:
        if item["id"] == signal_id:
            return item
    raise ValueError(f"未找到观测信号: {signal_id}")


def _security_registry_payload() -> dict[str, Any]:
    path = ASSETS_DIR / "security" / "registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    return {
        "schemaVersion": registry["schemaVersion"],
        "controls": registry["controls"],
        "schemas": registry["schemas"],
        "metadata": registry["metadata"],
    }


def _security_control_payload(control_id: str) -> dict[str, Any]:
    for item in _security_registry_payload()["controls"]:
        if item["id"] == control_id:
            return item
    raise ValueError(f"未找到安全控制: {control_id}")


def _delivery_surface_registry_payload() -> dict[str, Any]:
    path = ASSETS_DIR / "delivery" / "registry.json"
    with path.open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    return {
        "schemaVersion": registry["schemaVersion"],
        "surfaces": registry["surfaces"],
        "schemas": registry["schemas"],
        "releaseGate": registry["releaseGate"],
        "metadata": registry["metadata"],
    }


def _delivery_surface_payload(surface_id: str) -> dict[str, Any]:
    for item in _delivery_surface_registry_payload()["surfaces"]:
        if item["id"] == surface_id:
            return item
    raise ValueError(f"未找到交付面: {surface_id}")


def _webhook_config_from_headers(webhook_url: str | None, webhook_secret: str | None) -> WebhookConfig | None:
    if not webhook_url:
        if webhook_secret:
            raise HTTPException(status_code=422, detail="X-FateCat-Webhook-Secret 需要同时提供 webhook URL")
        return None
    if not REPORT_JOB_WEBHOOKS_ENABLED:
        raise HTTPException(status_code=403, detail="报告任务 webhook callback 未启用")
    try:
        return WebhookConfig(
            url=webhook_url,
            secret=webhook_secret,
            allowed_hosts=parse_allowed_hosts(WEBHOOK_ALLOWED_HOSTS),
            allow_http=WEBHOOK_ALLOW_HTTP,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _submit_report_job(
    *,
    kind: str,
    report_system: str,
    task,
    input_summary: dict[str, Any],
    task_payload: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
    webhook_config: WebhookConfig | None = None,
) -> ReportJobSnapshot:
    try:
        with trace_span(
            "report_job.submit",
            attributes={
                "kind": kind,
                "reportSystem": report_system,
                "webhookEnabled": webhook_config is not None,
            },
        ):
            snapshot = report_job_manager.submit(
                kind=kind,
                report_system=report_system,
                task=task,
                task_payload=task_payload,
                input_summary=input_summary,
                idempotency_key=idempotency_key,
                webhook_config=webhook_config,
            )
        _log_audit_event(
            "report_job.submit",
            target_type="CalculationJob",
            target_id=snapshot.job_id,
            metadata={
                "kind": kind,
                "reportSystem": report_system,
                "idempotencyKeyProvided": bool(idempotency_key),
                "webhookProvided": webhook_config is not None,
                "webhookSignature": webhook_config.signature_mode if webhook_config else "none",
                "status": snapshot.status,
                "ttlSeconds": REPORT_JOB_TTL_SECONDS,
            },
        )
        return snapshot
    except ReportJobQueueFull as exc:
        _log_audit_event(
            "report_job.submit",
            target_type="CalculationJob",
            outcome="rejected",
            metadata={
                "kind": kind,
                "reportSystem": report_system,
                "webhookProvided": webhook_config is not None,
                "reason": "queue_full",
            },
        )
        raise HTTPException(status_code=429, detail=str(exc)) from exc


def _apply_public_response_headers(response: Response, request_id: str) -> Response:
    response.headers["X-Request-ID"] = request_id
    traceparent = current_traceparent()
    if traceparent:
        response.headers["Traceparent"] = traceparent
        response.headers["X-Trace-ID"] = current_trace_id()
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; frame-ancestors 'none'",
    )
    if ENABLE_HSTS:
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    return response


def _finalize_early_response(
    request: Request,
    response: Response,
    request_id: str,
    status_code: int,
    started: float,
    error_class: str,
) -> Response:
    elapsed = time.perf_counter() - started
    route = _route_label(request)
    _record_request_metric(request.method, route, status_code, elapsed, error_class=error_class)
    _log_request(request, request_id, route, status_code, elapsed, error_class=error_class)
    return _apply_public_response_headers(response, request_id)


def _log_request(
    request: Request,
    request_id: str,
    route: str,
    status_code: int,
    elapsed_seconds: float,
    *,
    error_class: str | None,
) -> None:
    payload = {
        "event": "http_request",
        "requestId": request_id,
        "traceId": current_trace_id(),
        "method": request.method,
        "route": route,
        "status": status_code,
        "elapsedMs": round(elapsed_seconds * 1000, 3),
        "client": _client_key(request),
    }
    if error_class:
        payload["errorClass"] = error_class
    message = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if status_code >= 500:
        logger.error(message)
    elif status_code >= 400:
        logger.warning(message)
    else:
        logger.info(message)


@app.middleware("http")
async def production_guardrails(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.request_id = request_id
    request_id_token = _request_id_context.set(request_id)
    trace_context = trace_context_from_traceparent(request.headers.get("traceparent"))
    request.state.trace_id = trace_context.trace_id
    trace_token = set_trace_context(trace_context)
    started = time.perf_counter()
    try:
        with trace_span(
            "http.request",
            span_kind="server",
            attributes={"http.method": request.method, "http.route": _route_label(request)},
        ):
            allowed, retry_after = _check_rate_limit(request)
            if not allowed:
                response = _json_error(429, "请求过于频繁")
                response.headers["Retry-After"] = str(retry_after)
                return _finalize_early_response(request, response, request_id, 429, started, "rate_limited")

            global _inflight_requests
            with _metrics_lock:
                _inflight_requests += 1

            status_code = 500
            error_class: str | None = None
            try:
                response = await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_SECONDS)
                status_code = response.status_code
                error_class = _classify_error(status_code)
            except TimeoutError:
                response = _json_error(504, "请求处理超时")
                status_code = 504
                error_class = "timeout"
            finally:
                elapsed = time.perf_counter() - started
                route = _route_label(request)
                _record_request_metric(request.method, route, status_code, elapsed, error_class=error_class)
                _log_request(request, request_id, route, status_code, elapsed, error_class=error_class)
                with _metrics_lock:
                    _inflight_requests -= 1

            return _apply_public_response_headers(response, request_id)
    finally:
        reset_trace_context(trace_token)
        _request_id_context.reset(request_id_token)


app.add_middleware(RequestBodyLimitMiddleware)


def _branding_model() -> BrandingInfo:
    return BrandingInfo(**get_branding_payload())


def _disclaimer_model() -> str:
    return get_disclaimer_payload()


@app.exception_handler(HTTPException)
async def branded_http_exception_handler(_request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc.detail),
                "statusCode": exc.status_code,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def branded_validation_exception_handler(request: Request, exc: RequestValidationError):
    _log_structured(
        "info",
        {
            "event": "validation_error",
            "requestId": _request_id_from_request(request),
            "errorCount": len(exc.errors()),
        },
    )
    return JSONResponse(
        status_code=422,
        content=attach_branding(
            {
                "success": False,
                "error": "请求参数无效",
                "statusCode": 422,
            }
        ),
    )


@app.exception_handler(Exception)
async def branded_exception_handler(request: Request, exc: Exception):
    _log_structured(
        "error",
        {
            "event": "unhandled_exception",
            "requestId": _request_id_from_request(request),
            "errorType": type(exc).__name__,
        },
    )
    return JSONResponse(
        status_code=500,
        content=attach_branding(
            {
                "success": False,
                "error": "服务器内部错误",
                "statusCode": 500,
            }
        ),
    )


@app.post(TELEGRAM_DELIVERY_PATH, include_in_schema=True)
async def receive_telegram_webhook(
    request: Request,
    secret_token: str | None = Header(default=None, alias="X-Telegram-Bot-Api-Secret-Token"),
):
    """接收 Telegram Update；只负责鉴权和入队，不同步执行测算。"""
    if not telegram_webhook_runtime.enabled:
        raise HTTPException(status_code=404, detail="Telegram Webhook 未启用")
    try:
        payload = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Telegram Update 必须是 JSON") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Telegram Update 必须是 JSON 对象")
    try:
        status = await telegram_webhook_runtime.enqueue(payload, secret_token)
    except TelegramWebhookDisabled as exc:
        raise HTTPException(status_code=404, detail="Telegram Webhook 未启用") from exc
    except TelegramWebhookUnauthorized as exc:
        raise HTTPException(status_code=403, detail="Telegram Webhook 未授权") from exc
    except TelegramWebhookInvalidUpdate as exc:
        raise HTTPException(status_code=400, detail="Telegram Update 格式无效") from exc
    except TelegramWebhookQueueFull:
        return JSONResponse(status_code=503, headers={"Retry-After": "1"}, content={"status": "queue_full"})
    return JSONResponse(status_code=200 if status == "duplicate" else 202, content={"status": status})


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


@app.get("/live")
def live():
    return attach_branding({"status": "live"})


@app.get("/ready")
def ready():
    telegram_status = telegram_webhook_runtime.status()
    checks = {
        "database": "disabled" if not _records_enabled() else "ok",
        "capabilities": "ok",
        "locationCatalog": "checking",
        "telegramWebhook": "ok"
        if telegram_status["ready"]
        else ("disabled" if not telegram_status["enabled"] else "not_ready"),
    }
    try:
        if _records_enabled():
            db.ensure_db()
        list_capabilities()
        location_status = catalog_status()
        checks["locationCatalog"] = f"ok:{location_status['recordCount']}"
    except Exception as exc:
        _log_business_exception("readiness 检查失败", error_type=type(exc).__name__)
        return JSONResponse(
            status_code=503,
            content=attach_branding({"status": "not_ready", "checks": checks, "error": str(exc)}),
        )
    degraded_surfaces = []
    if telegram_status["enabled"] and not telegram_status["ready"]:
        degraded_surfaces.append("telegramWebhook")
    return attach_branding(
        {
            "status": "ready",
            "checks": checks,
            "degraded": bool(degraded_surfaces),
            "degradedSurfaces": degraded_surfaces,
        }
    )


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    lines = [
        "# HELP fatecat_requests_total Total HTTP requests.",
        "# TYPE fatecat_requests_total counter",
    ]
    with _metrics_lock:
        counts = dict(_request_counts)
        latencies = dict(_request_latency_seconds)
        latency_buckets = dict(_request_latency_buckets)
        error_counts = dict(_request_error_counts)
        inflight = _inflight_requests
    with _calculation_slots_lock:
        calculation_slots_in_use = _calculation_slots_in_use
    bot_queue_status = get_queue_status()
    report_job_status = report_job_manager.stats()
    telegram_webhook_status = telegram_webhook_runtime.status()

    for (method, route, status_code), count in sorted(counts.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_requests_total{{{labels}}} {count}")

    lines.extend(
        [
            "# HELP fatecat_request_latency_seconds HTTP request latency histogram.",
            "# TYPE fatecat_request_latency_seconds histogram",
        ]
    )
    for (method, route, status_code, bucket), count in sorted(latency_buckets.items()):
        labels = (
            f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",'
            f'status="{status_code}",le="{bucket}"'
        )
        lines.append(f"fatecat_request_latency_seconds_bucket{{{labels}}} {count}")
    for (method, route, status_code), count in sorted(counts.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_request_latency_seconds_count{{{labels}}} {count}")
    for (method, route, status_code), total in sorted(latencies.items()):
        labels = f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",status="{status_code}"'
        lines.append(f"fatecat_request_latency_seconds_sum{{{labels}}} {total:.6f}")

    lines.extend(
        [
            "# HELP fatecat_request_errors_total Total HTTP error responses by class.",
            "# TYPE fatecat_request_errors_total counter",
        ]
    )
    for (method, route, status_code, error_class), count in sorted(error_counts.items()):
        labels = (
            f'method="{_escape_metric_label(method)}",route="{_escape_metric_label(route)}",'
            f'status="{status_code}",error_class="{_escape_metric_label(error_class)}"'
        )
        lines.append(f"fatecat_request_errors_total{{{labels}}} {count}")

    lines.extend(
        [
            "# HELP fatecat_inflight_requests Current in-flight HTTP requests.",
            "# TYPE fatecat_inflight_requests gauge",
            f"fatecat_inflight_requests {inflight}",
            "# HELP fatecat_calculation_slots_in_use Current synchronous calculation slots in use.",
            "# TYPE fatecat_calculation_slots_in_use gauge",
            f"fatecat_calculation_slots_in_use {calculation_slots_in_use}",
            "# HELP fatecat_calculation_slots_max Configured synchronous calculation slot ceiling.",
            "# TYPE fatecat_calculation_slots_max gauge",
            f"fatecat_calculation_slots_max {MAX_INFLIGHT_CALCULATIONS}",
            "# HELP fatecat_report_job_store_backend_info Configured report job store backend.",
            "# TYPE fatecat_report_job_store_backend_info gauge",
            f'fatecat_report_job_store_backend_info{{backend="{_escape_metric_label(report_job_manager.backend_name)}"}} 1',
            "# HELP fatecat_report_job_queue_size Current Web/API report jobs waiting in report job queue.",
            "# TYPE fatecat_report_job_queue_size gauge",
            f"fatecat_report_job_queue_size {report_job_status['queue_size']}",
            "# HELP fatecat_report_job_queue_max Configured Web/API report job queue capacity.",
            "# TYPE fatecat_report_job_queue_max gauge",
            f"fatecat_report_job_queue_max {report_job_status['queue_max']}",
            "# HELP fatecat_report_job_workers Configured in-process report job workers.",
            "# TYPE fatecat_report_job_workers gauge",
            f"fatecat_report_job_workers {report_job_status['worker_max']}",
            "# HELP fatecat_report_jobs Current report jobs by status.",
            "# TYPE fatecat_report_jobs gauge",
            f'fatecat_report_jobs{{status="queued"}} {report_job_status["queued"]}',
            f'fatecat_report_jobs{{status="running"}} {report_job_status["running"]}',
            f'fatecat_report_jobs{{status="succeeded"}} {report_job_status["succeeded"]}',
            f'fatecat_report_jobs{{status="failed"}} {report_job_status["failed"]}',
            f'fatecat_report_jobs{{status="expired"}} {report_job_status["expired"]}',
            f'fatecat_report_jobs{{status="cancelled"}} {report_job_status["cancelled"]}',
        ]
    )
    lines.extend(
        [
            "# HELP fatecat_bot_queue_size Current Telegram Bot calculation queue size.",
            "# TYPE fatecat_bot_queue_size gauge",
            f"fatecat_bot_queue_size {bot_queue_status['queue_size']}",
            "# HELP fatecat_bot_queue_scope_info Telegram Bot queue backend and scope info.",
            "# TYPE fatecat_bot_queue_scope_info gauge",
            "fatecat_bot_queue_scope_info{"
            f'backend="{_escape_metric_label(str(bot_queue_status["backend"]))}",'
            f'scope="{_escape_metric_label(str(bot_queue_status["scope"]))}"'
            "} 1",
            "# HELP fatecat_bot_queue_max_size Configured Telegram Bot queue capacity.",
            "# TYPE fatecat_bot_queue_max_size gauge",
            f"fatecat_bot_queue_max_size {bot_queue_status['queue_max']}",
            "# HELP fatecat_bot_concurrent_requests Current Telegram Bot concurrent calculations.",
            "# TYPE fatecat_bot_concurrent_requests gauge",
            f"fatecat_bot_concurrent_requests {bot_queue_status['concurrent']}",
            "# HELP fatecat_bot_max_concurrent_requests Configured Telegram Bot concurrency ceiling.",
            "# TYPE fatecat_bot_max_concurrent_requests gauge",
            f"fatecat_bot_max_concurrent_requests {bot_queue_status['max_concurrent']}",
            "# HELP fatecat_bot_user_cooldown_seconds Configured per-user Bot cooldown seconds.",
            "# TYPE fatecat_bot_user_cooldown_seconds gauge",
            f"fatecat_bot_user_cooldown_seconds {bot_queue_status['user_cooldown_seconds']}",
            "# HELP fatecat_bot_user_daily_limit Configured per-user Bot daily request limit.",
            "# TYPE fatecat_bot_user_daily_limit gauge",
            f"fatecat_bot_user_daily_limit {bot_queue_status['user_daily_limit']}",
            "# HELP fatecat_telegram_webhook_enabled Whether Telegram webhook delivery is enabled.",
            "# TYPE fatecat_telegram_webhook_enabled gauge",
            f"fatecat_telegram_webhook_enabled {int(bool(telegram_webhook_status['enabled']))}",
            "# HELP fatecat_telegram_webhook_ready Whether Telegram webhook delivery is ready.",
            "# TYPE fatecat_telegram_webhook_ready gauge",
            f"fatecat_telegram_webhook_ready {int(bool(telegram_webhook_status['ready']))}",
            "# HELP fatecat_telegram_webhook_queue_depth Current Telegram webhook update queue depth.",
            "# TYPE fatecat_telegram_webhook_queue_depth gauge",
            f"fatecat_telegram_webhook_queue_depth {telegram_webhook_status['queueDepth']}",
            "# HELP fatecat_telegram_webhook_queue_capacity Configured Telegram webhook update queue capacity.",
            "# TYPE fatecat_telegram_webhook_queue_capacity gauge",
            f"fatecat_telegram_webhook_queue_capacity {telegram_webhook_status['queueCapacity']}",
            "# HELP fatecat_telegram_webhook_updates_total Telegram webhook updates by result.",
            "# TYPE fatecat_telegram_webhook_updates_total counter",
            f'fatecat_telegram_webhook_updates_total{{result="accepted"}} {telegram_webhook_status["acceptedTotal"]}',
            f'fatecat_telegram_webhook_updates_total{{result="duplicate"}} {telegram_webhook_status["duplicateTotal"]}',
            f'fatecat_telegram_webhook_updates_total{{result="queue_full"}} {telegram_webhook_status["queueFullTotal"]}',
            f'fatecat_telegram_webhook_updates_total{{result="unauthorized"}} {telegram_webhook_status["unauthorizedTotal"]}',
            f'fatecat_telegram_webhook_updates_total{{result="invalid"}} {telegram_webhook_status["invalidTotal"]}',
            "# HELP fatecat_telegram_webhook_start_failures_total Telegram webhook startup failures.",
            "# TYPE fatecat_telegram_webhook_start_failures_total counter",
            f"fatecat_telegram_webhook_start_failures_total {telegram_webhook_status['startFailureTotal']}",
        ]
    )
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")


@app.get("/web", response_class=HTMLResponse)
def web_report(
    birthDate: str | None = None,
    birthTime: str | None = None,
    birthPlace: str | None = None,
    locationMode: str | None = None,
    locationId: str | None = None,
    timeBasis: str | None = None,
    foldChoice: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    reportSystem: str | None = None,
    submitted: str | None = None,
    jobId: str | None = None,
):
    """原生 HTML Web 版标准 Markdown 报告。"""
    job = None
    if jobId:
        try:
            job = _web_job_view(report_job_manager.get(jobId))
        except ReportJobNotFound:
            job = WebReportJobView(
                job_id=jobId,
                status="expired",
                report_system=reportSystem or "bazi",
                created_at="",
                expires_at="",
                error="报告任务不存在或已过期；请重新提交。",
            )
    return render_web_report_page(
        birth_date=birthDate,
        birth_time=birthTime,
        birth_place=birthPlace,
        location_mode=locationMode,
        location_id=locationId,
        time_basis=timeBasis,
        fold_choice=foldChoice,
        gender=gender,
        name=name,
        report_system=reportSystem,
        submitted=submitted,
        job=job,
    )


@app.get("/api/v1/locations")
def search_locations(
    q: str = Query(..., min_length=1, max_length=160),
    mode: str | None = Query(default=None, pattern="^(domestic|overseas)$"),
    limit: int = Query(default=20, ge=1, le=100),
):
    """搜索稳定出生地点 ID；返回 WGS84 坐标、IANA 时区与来源精度。"""
    results = [item.as_dict() for item in search_records(q, mode=mode, limit=limit)]
    return attach_branding(
        {
            "success": True,
            "data": {"query": q, "mode": mode, "count": len(results), "locations": results},
            "meta": {"catalog": catalog_status()},
        }
    )


@app.get("/api/v1/locations/{location_id:path}")
def get_location(location_id: str):
    """按稳定地点 ID 获取出生地点事实。"""
    try:
        item = resolve_location(location_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return attach_branding({"success": True, "data": item.as_dict(), "meta": {"catalog": catalog_status()}})


@app.post("/api/v1/report/jobs/web")
def create_web_report_job(
    payload: dict[str, Any],
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    webhook_url: str | None = Header(default=None, alias="X-FateCat-Webhook-Url"),
    webhook_secret: str | None = Header(default=None, alias="X-FateCat-Webhook-Secret"),
):
    """提交 Web 表单报告任务；公开工作台默认使用该异步入口。"""
    form = _web_form_from_payload(payload)
    try:
        validated = validate_web_report_form(form)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    webhook_config = _webhook_config_from_headers(webhook_url, webhook_secret)
    snapshot = _submit_report_job(
        kind="web",
        report_system=validated.report_system,
        input_summary={
            "birthDate": form.birth_date,
            "birthTime": validated.normalized_time,
            "birthPlace": validated.display_birth_place,
            "gender": validated.gender,
            "name": form.name,
        },
        task=lambda: _run_with_calculation_slot(lambda: build_web_report_result(form)),
        task_payload=_web_report_task_payload(form),
        idempotency_key=idempotency_key,
        webhook_config=webhook_config,
    )
    return JSONResponse(
        status_code=202,
        content=attach_branding(
            {
                "success": True,
                "data": _report_job_payload(snapshot, include_result=False),
                "meta": {"acceptedAt": now_cn().isoformat()},
            }
        ),
    )


@app.get("/api/v1/report/systems")
def list_report_systems():
    """列出当前可用和未来规划的独立输出体系。"""
    return attach_branding({"success": True, "data": {"systems": prediction_systems_payload()}})


@app.get("/api/v1/capabilities")
def list_prediction_capabilities():
    """列出统一测算 capability 注册表。"""
    return attach_branding({"success": True, "data": _capabilities_payload()})


@app.get("/capabilities")
def list_measurement_capabilities():
    """基础设施口径 capability 注册表别名。"""
    return list_prediction_capabilities()


@app.get("/api/v1/capabilities/{capability_id}")
def get_prediction_capability(capability_id: str):
    """读取单个 capability 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _capability_resource_payload(get_capability(capability_id))})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/capabilities/{capability_id}")
def get_measurement_capability(capability_id: str):
    """基础设施口径 capability 资源详情别名。"""
    return get_prediction_capability(capability_id)


@app.get("/api/v1/providers")
def list_prediction_providers():
    """列出 production provider 资源注册表。"""
    return attach_branding({"success": True, "data": _providers_payload()})


@app.get("/providers")
def list_measurement_providers():
    """基础设施口径 provider 注册表别名。"""
    return list_prediction_providers()


@app.get("/api/v1/providers/{provider_id}")
def get_prediction_provider(provider_id: str):
    """读取单个 provider 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _provider_resource_payload(get_provider(provider_id))})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/providers/{provider_id}")
def get_measurement_provider(provider_id: str):
    """基础设施口径 provider 资源详情别名。"""
    return get_prediction_provider(provider_id)


def _capability_execution_payload(capability_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    result = _run_with_calculation_slot(
        lambda: CapabilityExecutor().execute(CapabilityInput(capability_id=capability_id, payload=payload))
    )
    return {
        "success": True,
        "capabilityId": result.capability_id,
        "status": result.status,
        "reportProfile": result.report_profile,
        "data": result.data,
        "evidence": result.evidence,
        "risk": result.risk,
        "metadata": result.metadata,
        "report": _capability_report_payload(result),
    }


@app.post("/api/v1/capabilities/{capability_id}")
def execute_prediction_capability(capability_id: str, payload: dict[str, Any]):
    """执行已生产化的独立 capability。"""
    try:
        data = _capability_execution_payload(capability_id, payload)
        return attach_branding(
            {
                **data,
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/capabilities/{capability_id}/calculate")
def calculate_measurement_capability(capability_id: str, payload: dict[str, Any]):
    """基础设施口径 capability 执行别名。"""
    return execute_prediction_capability(capability_id, payload)


@app.post("/api/v1/sandbox/capabilities/{capability_id}/calculate")
def calculate_sandbox_capability(
    capability_id: str,
    payload: dict[str, Any],
    x_fatecat_sandbox_token: str | None = Header(default=None, alias="X-FateCat-Sandbox-Token"),
    authorization: str | None = Header(default=None),
):
    """本地 sandbox gateway：验证 sandbox token scope 后执行白名单 capability。"""
    principal = _require_sandbox_capability_access(capability_id, x_fatecat_sandbox_token, authorization)
    required_scope = _sandbox_scope_for_capability(capability_id)
    try:
        data = _capability_execution_payload(capability_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    _log_audit_event(
        "sandbox.capability.calculate",
        principal=principal,
        target_type="Capability",
        target_id=capability_id,
        metadata={
            "scope": required_scope,
            "sandbox": True,
            "reportProfile": data.get("reportProfile"),
            "liveServiceStatus": "local_gateway_only",
        },
    )
    return attach_branding(
        {
            **data,
            "sandbox": {
                "authorized": True,
                "scope": required_scope,
                "subjectHash": _audit_hash(principal.user_id or "sandbox"),
                "liveServiceStatus": "local_gateway_only",
            },
            "meta": {"calculatedAt": now_cn().isoformat()},
        }
    )


@app.post("/sandbox/capabilities/{capability_id}/calculate")
def calculate_measurement_sandbox_capability(
    capability_id: str,
    payload: dict[str, Any],
    x_fatecat_sandbox_token: str | None = Header(default=None, alias="X-FateCat-Sandbox-Token"),
    authorization: str | None = Header(default=None),
):
    """基础设施口径 sandbox gateway 别名。"""
    return calculate_sandbox_capability(capability_id, payload, x_fatecat_sandbox_token, authorization)


@app.get("/api/v1/errors")
def list_error_catalog():
    """列出测算基础设施标准错误码。"""
    return attach_branding({"success": True, "data": _error_catalog_payload()})


@app.get("/errors")
def list_measurement_errors():
    """基础设施口径标准错误码别名。"""
    return list_error_catalog()


@app.get("/api/v1/evaluations")
def list_prediction_evaluations():
    """列出 Dataset 与 EvaluationRun 评测资源注册表。"""
    return attach_branding({"success": True, "data": _evaluation_registry_payload()})


@app.get("/evaluations")
def list_measurement_evaluations():
    """基础设施口径评测资源注册表别名。"""
    return list_prediction_evaluations()


@app.get("/api/v1/evaluations/{evaluation_id}")
def get_prediction_evaluation(evaluation_id: str):
    """读取单个 Dataset 或 EvaluationRun 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _evaluation_resource_payload(evaluation_id)})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/evaluations/{evaluation_id}")
def get_measurement_evaluation(evaluation_id: str):
    """基础设施口径评测资源详情别名。"""
    return get_prediction_evaluation(evaluation_id)


@app.get("/api/v1/observability")
def list_prediction_observability():
    """列出 health、ready、metrics、logs 与 planned trace/SLO 观测资源。"""
    return attach_branding({"success": True, "data": _observability_registry_payload()})


@app.get("/observability")
def list_measurement_observability():
    """基础设施口径观测资源注册表别名。"""
    return list_prediction_observability()


@app.get("/api/v1/observability/{signal_id}")
def get_prediction_observability_signal(signal_id: str):
    """读取单个 ObservabilitySignal 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _observability_signal_payload(signal_id)})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/observability/{signal_id}")
def get_measurement_observability_signal(signal_id: str):
    """基础设施口径观测资源详情别名。"""
    return get_prediction_observability_signal(signal_id)


@app.get("/api/v1/security")
def list_prediction_security_controls():
    """列出安全、隐私与发布门禁 SecurityControl 资源注册表。"""
    return attach_branding({"success": True, "data": _security_registry_payload()})


@app.get("/security")
def list_measurement_security_controls():
    """基础设施口径安全控制资源注册表别名。"""
    return list_prediction_security_controls()


@app.get("/api/v1/security/{control_id}")
def get_prediction_security_control(control_id: str):
    """读取单个 SecurityControl 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _security_control_payload(control_id)})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/security/{control_id}")
def get_measurement_security_control(control_id: str):
    """基础设施口径安全控制资源详情别名。"""
    return get_prediction_security_control(control_id)


@app.get("/api/v1/surfaces")
def list_prediction_delivery_surfaces():
    """列出 Web、API、Bot、CLI、Skill 和托管 Web 交付面资源注册表。"""
    return attach_branding({"success": True, "data": _delivery_surface_registry_payload()})


@app.get("/surfaces")
def list_measurement_delivery_surfaces():
    """基础设施口径交付面资源注册表别名。"""
    return list_prediction_delivery_surfaces()


@app.get("/api/v1/surfaces/{surface_id}")
def get_prediction_delivery_surface(surface_id: str):
    """读取单个 DeliverySurface 资源详情。"""
    try:
        return attach_branding({"success": True, "data": _delivery_surface_payload(surface_id)})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/surfaces/{surface_id}")
def get_measurement_delivery_surface(surface_id: str):
    """基础设施口径交付面资源详情别名。"""
    return get_prediction_delivery_surface(surface_id)


@app.get("/reports")
def list_report_infrastructure():
    """列出报告交付入口和可见 profile。"""
    return attach_branding(
        {
            "success": True,
            "data": {
                "profiles": prediction_systems_payload(),
                "jobEndpoint": "/api/v1/report/jobs",
                "markdownEndpoint": "/api/v1/report/markdown",
                "reportSchema": "contracts/fate/capabilities/schemas/report.schema.json",
                "webJobEndpoint": "/api/v1/report/jobs/web",
                "statusEndpoint": "/api/v1/report/jobs/{job_id}",
                "cancelEndpoint": "/api/v1/report/jobs/{job_id}/cancel",
                "idempotencyHeader": "Idempotency-Key",
            },
        }
    )


@app.get("/metadata")
def service_metadata():
    """测算基础设施元信息。"""
    return attach_branding(
        {
            "success": True,
            "data": {
                "service": "FateCat",
                "positioning": "面向 Agent 与应用开发者的测算基础设施",
                "capabilityProtocol": {
                    "schemaVersion": 1,
                    "defaultCapability": "bazi",
                    "registryEndpoint": "/capabilities",
                    "calculateEndpoint": "/capabilities/{capability_id}/calculate",
                    "providerRegistryEndpoint": "/providers",
                    "evaluationRegistryEndpoint": "/evaluations",
                    "observabilityRegistryEndpoint": "/observability",
                    "securityRegistryEndpoint": "/security",
                    "surfaceRegistryEndpoint": "/surfaces",
                },
                "developer": {
                    "openapi": "/openapi.json",
                    "interactiveDocs": "/docs",
                    "redoc": "/redoc",
                    "apiGuide": "docs/reference-materials/operations/测算基础设施 API 接入.md",
                    "developerPlatform": "contracts/fate/developer/developer-platform.json",
                    "sdkPackageBaseline": "docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md",
                    "sandboxTokenContract": "contracts/fate/developer/sandbox-token-contract.json",
                    "sandboxAccessGateway": "contracts/fate/developer/sandbox-access-gateway.json",
                    "apiChangelog": "contracts/fate/developer/api-changelog.json",
                    "developerPlatformGate": "bash scripts/developer-platform-gate.sh",
                    "sandboxGatewayGate": "bash scripts/sandbox-access-gateway-gate.sh",
                    "capabilityList": "/capabilities",
                    "capabilityDetail": "/capabilities/{capability_id}",
                    "capabilityCalculate": "/capabilities/{capability_id}/calculate",
                    "sandboxCapabilityCalculate": "/sandbox/capabilities/{capability_id}/calculate",
                    "providerList": "/providers",
                    "providerDetail": "/providers/{provider_id}",
                    "evaluationList": "/evaluations",
                    "evaluationDetail": "/evaluations/{evaluation_id}",
                    "observabilityList": "/observability",
                    "observabilityDetail": "/observability/{signal_id}",
                    "securityList": "/security",
                    "securityDetail": "/security/{control_id}",
                    "surfaceList": "/surfaces",
                    "surfaceDetail": "/surfaces/{surface_id}",
                    "reports": "/reports",
                    "errors": "/errors",
                },
                "surfaces": ["CLI", "Web", "FastAPI", "Telegram", "Agent Skill"],
                "quality": {
                    "health": "/health",
                    "readiness": "/ready",
                    "metrics": "/metrics",
                    "rateLimitPerMinute": RATE_LIMIT_PER_MINUTE,
                    "maxInflightCalculations": MAX_INFLIGHT_CALCULATIONS,
                    "reportJobQueueSize": REPORT_JOB_QUEUE_SIZE,
                    "reportJobStore": report_job_manager.backend_name,
                },
                "privacy": {
                    "birthPlaceDisplayPolicy": "默认示例使用北京/测试用户；公共行政区候选和用户主动提交的地区可在当前响应显示，不进入日志或默认持久化。",
                    "recordsEnabled": _records_enabled(),
                    "recordAccess": "记录接口需要 FATE_API_TOKEN、FATE_API_ADMIN_TOKEN 或 FATE_API_USER_TOKENS；用户 token 支持 user_id:token 与 user_id:token:record.read|record.list scoped 格式。",
                    "sensitiveValuePolicy": "响应、文档和日志不得输出真实 token、secret、DSN 或私钥内容。",
                },
                "productionGate": {
                    "localReadiness": "/ready",
                    "metrics": "/metrics",
                    "script": "scripts/production-readiness.sh --api-url <真实域名> --require-live-bot",
                    "externalConnectivity": "外部连通验证待执行",
                },
            },
        }
    )


def _validate_supported_bazi_options(req: BaziRequest) -> None:
    """拒绝当前主链尚未真实实现的业务选项。"""
    if req.options.calendarType != "solar":
        raise HTTPException(status_code=422, detail="calendarType=lunar 暂未实现；请使用 solar 公历输入。")
    if req.options.daylightSaving != "auto":
        raise HTTPException(status_code=422, detail="daylightSaving=on/off 暂未实现；请使用 auto。")
    if req.options.midnightMode != "early":
        raise HTTPException(status_code=422, detail="midnightMode=late 暂未实现；请使用 early。")


def _normalized_bazi_options(req: BaziRequest, *, report_system: str) -> dict[str, Any]:
    """记录本次计算真实采用的业务选项口径。"""
    return {
        "calendarType": "solar",
        "daylightSaving": "auto",
        "midnightMode": "early",
        "useTrueSolarTime": req.options.useTrueSolarTime,
        "reportSystem": report_system,
        "timeBasis": req.options.timeBasis,
        "foldChoice": req.options.foldChoice,
    }


@dataclass(frozen=True, slots=True)
class ParsedBaziRequest:
    wall_time: datetime
    engine_time: datetime
    location: ResolvedLocation
    normalized_time: NormalizedBirthTime


def _request_location(req: BaziRequest) -> ResolvedLocation:
    if not req.birthPlace:
        raise HTTPException(status_code=400, detail="birthPlace 必填（地点用于时区、真太阳时与经纬度计算）")
    try:
        if req.birthPlace.locationId:
            location = resolve_location(req.birthPlace.locationId)
            if location.timezone != req.birthPlace.timezone:
                raise ValueError("birthPlace.timezone 与 locationId 对应的 IANA 时区不一致")
            if (
                abs(location.longitude - req.birthPlace.longitude) > 0.000001
                or abs(location.latitude - req.birthPlace.latitude) > 0.000001
            ):
                raise ValueError("birthPlace 经纬度与 locationId 对应的 WGS84 坐标不一致")
            if (
                req.birthPlace.coordinatePrecision
                and req.birthPlace.coordinatePrecision != location.coordinate_precision
            ):
                raise ValueError("birthPlace.coordinatePrecision 与 locationId 对应的坐标精度不一致")
            return location
        location = resolve_coordinates(req.birthPlace.longitude, req.birthPlace.latitude)
        if location.timezone != req.birthPlace.timezone:
            raise ValueError(f"birthPlace.timezone 与 WGS84 坐标解析结果不一致；坐标对应 {location.timezone}")
        return ResolvedLocation(
            location_id=location.location_id,
            mode=location.mode,
            name=req.birthPlace.name,
            display_name=req.birthPlace.name,
            country_code=location.country_code,
            admin1_code=location.admin1_code,
            admin2_code=location.admin2_code,
            admin3_code=location.admin3_code,
            longitude=location.longitude,
            latitude=location.latitude,
            coordinate_system=req.birthPlace.coordinateSystem,
            timezone=location.timezone,
            coordinate_precision=req.birthPlace.coordinatePrecision or location.coordinate_precision,
            source=location.source,
            source_version=location.source_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _parse_bazi_request(req: BaziRequest) -> ParsedBaziRequest:
    _validate_supported_bazi_options(req)
    birth_time = req.birthTime.strip()
    if len(birth_time) == 5:
        birth_time = f"{birth_time}:00"
    try:
        wall_time = datetime.strptime(f"{req.birthDate.strip()} {birth_time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="出生日期或出生时间格式无效；日期使用 YYYY-MM-DD，时间使用 HH:MM 或 HH:MM:SS。",
        ) from exc
    location = _request_location(req)
    try:
        normalized_time = normalize_birth_time(
            wall_time,
            location,
            time_basis=req.options.timeBasis,
            fold_choice=req.options.foldChoice,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ParsedBaziRequest(
        wall_time=wall_time,
        engine_time=normalized_time.engine_beijing_time,
        location=location,
        normalized_time=normalized_time,
    )


def _build_bazi_data(
    result: dict,
    *,
    parsed: ParsedBaziRequest,
) -> BaziData:
    major_fortune = dict(result.get("majorFortune", {}))
    major_fortune["pillars"] = [
        {
            **pillar,
            "year": pillar.get("year", pillar.get("startYear")),
        }
        for pillar in major_fortune.get("pillars", [])
        if isinstance(pillar, dict)
    ]

    input_tz = ZoneInfo(parsed.normalized_time.input_timezone)
    input_time = parsed.wall_time.replace(tzinfo=input_tz, fold=parsed.normalized_time.fold)
    engine_tz = ZoneInfo("Asia/Shanghai")
    true_solar_time = None
    if result.get("inputTrace", {}).get("useTrueSolarTime"):
        true_solar_value = str(result.get("inputTrace", {}).get("trueSolarTime") or result.get("trueSolarTime") or "")
        if true_solar_value:
            true_solar_time = datetime.fromisoformat(true_solar_value).replace(tzinfo=engine_tz)
    return BaziData(
        timeInfo=TimeInfo(
            inputTime=input_time.isoformat(),
            trueSolarTime=true_solar_time.isoformat() if true_solar_time else None,
            lunarDate=f"{result['fourPillars']['year']['fullName']}年",
            solarTerm="",
        ),
        fourPillars=result["fourPillars"],
        hiddenStems=result.get("hiddenStems", {}),
        tenGods=result.get("tenGods", {}),
        fiveElements=result.get("fiveElements", {}),
        dayMaster=result.get("dayMaster", {}),
        majorFortune=major_fortune,
        annualFortune=result.get("annualFortune", []),
        voidBranches=result.get("voidInfo", {}),
    )


def _calculate_bazi_raw(req: BaziRequest, *, report_system: str = "bazi") -> tuple[dict, ParsedBaziRequest]:
    parsed = _parse_bazi_request(req)
    calculation = calculate_delivery_result(
        birth_dt=parsed.engine_time,
        gender=req.gender,
        longitude=parsed.location.longitude,
        latitude=parsed.location.latitude,
        birth_place=parsed.location.display_name,
        name=req.name,
        report_system=report_system,
        use_true_solar_time=req.options.useTrueSolarTime,
    )
    return calculation.data, parsed


@app.post("/api/v1/bazi/simple", deprecated=True)
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        result, _parsed = _run_with_calculation_slot(lambda: _calculate_bazi_raw(req, report_system="bazi"))

        return attach_branding({"success": True, "data": result})
    except HTTPException:
        raise
    except Exception as e:
        _log_business_exception("简化八字计算失败", error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/bazi/pure-analysis")
def calculate_bazi_pure_analysis(req: BaziRequest):
    """纯命理分析 - 仅返回配置约束下的核心字段。"""
    try:
        parsed = _parse_bazi_request(req)
        payload = PureAnalysisInput(
            birth_dt=parsed.engine_time,
            gender=req.gender,
            longitude=parsed.location.longitude,
            latitude=parsed.location.latitude,
            name=req.name,
            birth_place=parsed.location.display_name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = _run_with_calculation_slot(lambda: calculate_pure_analysis(payload))
        return attach_branding(
            {
                "success": True,
                "data": result,
                "meta": {
                    "calculatedAt": now_cn().isoformat(),
                    "profile": "pure_analysis",
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        _log_business_exception("纯分析计算失败", error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse, deprecated=True)
def calculate_bazi(
    req: BaziRequest,
    user_id: str | None = None,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """计算八字排盘"""
    try:
        principal: ApiPrincipal | None = None
        if user_id:
            principal = _require_record_access(x_fatecat_api_key, authorization)
            _require_scope(principal, RECORD_SCOPE_WRITE)
            _require_owner_or_admin(principal, user_id)
        result, parsed = _run_with_calculation_slot(lambda: _calculate_bazi_raw(req, report_system="bazi"))
        data = _build_bazi_data(result, parsed=parsed)

        # 保存到数据库
        record_id = None
        if user_id:
            record_id = db.save_record(
                user_id=user_id,
                biz_type="bazi",
                name=req.name,
                gender=req.gender,
                calendar_type=req.options.calendarType,
                birth_date=req.birthDate,
                birth_time=req.birthTime,
                birth_place=parsed.location.display_name,
                longitude=parsed.location.longitude,
                latitude=parsed.location.latitude,
                dst=0,
                true_solar=1 if req.options.useTrueSolarTime else 0,
                early_zi=1 if req.options.midnightMode == "early" else 0,
                biz_data={
                    "input": req.model_dump(),
                    "normalizedOptions": _normalized_bazi_options(req, report_system="bazi"),
                    "result": result,
                },
            )
            _log_audit_event(
                "record.create",
                principal=principal,
                target_type="UserRecord",
                target_id=record_id,
                metadata={
                    "bizType": "bazi",
                    "recordRetentionDays": RECORD_RETENTION_DAYS,
                    "retentionMode": "explicit_delete" if RECORD_RETENTION_DAYS == 0 else "time_bound",
                },
            )

        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), recordId=record_id),
            branding=_branding_model(),
        )
    except HTTPException:
        raise
    except Exception as e:
        _log_business_exception("八字 API 计算失败", error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


def _build_markdown_report_payload(req: BaziRequest) -> dict[str, Any]:
    parsed = _parse_bazi_request(req)
    attributes = {"reportSystem": normalize_report_system(req.options.reportSystem), "reportFormat": "markdown"}
    with trace_span("report.calculate", attributes=attributes):
        calculation = _run_with_calculation_slot(
            lambda: calculate_delivery_result(
                birth_dt=parsed.engine_time,
                gender=req.gender,
                longitude=parsed.location.longitude,
                latitude=parsed.location.latitude,
                birth_place=parsed.location.display_name,
                name=req.name,
                report_system=req.options.reportSystem,
                use_true_solar_time=req.options.useTrueSolarTime,
            )
        )
    with trace_span("report.render_markdown", attributes=attributes):
        markdown = generate_full_report(
            calculation.data,
            hide=calculation.report_hide,
            report_system=calculation.report_system,
        )
    return {
        "reportSystem": calculation.report_system,
        "markdown": markdown,
        **_markdown_report_gates(report_system=calculation.report_system, markdown=markdown),
    }


def _web_report_task_payload(form: WebReportForm) -> dict[str, Any]:
    return {
        "birthDate": form.birth_date,
        "birthTime": form.birth_time,
        "birthPlace": form.birth_place,
        "locationMode": form.location_mode,
        "locationId": form.location_id,
        "timeBasis": form.time_basis,
        "foldChoice": form.fold_choice,
        "gender": form.gender,
        "name": form.name,
        "reportSystem": form.report_system,
    }


def _web_report_task_from_payload(payload: dict[str, Any]):
    form = _web_form_from_payload(payload)
    return lambda: _run_with_calculation_slot(lambda: build_web_report_result(form))


def _markdown_report_task_payload(req: BaziRequest) -> dict[str, Any]:
    return req.model_dump(mode="json")


def _markdown_report_task_from_payload(payload: dict[str, Any]):
    req = BaziRequest.model_validate(payload)
    return lambda: _build_markdown_report_payload(req)


def _report_job_task_factories():
    return {
        "web": _web_report_task_from_payload,
        "markdown": _markdown_report_task_from_payload,
    }


report_job_manager = _build_report_job_manager()


@app.post("/api/v1/report/jobs")
def create_markdown_report_job(
    req: BaziRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    webhook_url: str | None = Header(default=None, alias="X-FateCat-Webhook-Url"),
    webhook_secret: str | None = Header(default=None, alias="X-FateCat-Webhook-Secret"),
):
    """提交标准 Markdown 报告生成任务。"""
    report_system = normalize_report_system(req.options.reportSystem)
    birth_place = public_birth_place(req.birthPlace.name) if req.birthPlace else ""
    webhook_config = _webhook_config_from_headers(webhook_url, webhook_secret)
    snapshot = _submit_report_job(
        kind="markdown",
        report_system=report_system,
        input_summary={
            "birthDate": req.birthDate,
            "birthTime": req.birthTime,
            "birthPlace": birth_place,
            "gender": req.gender,
            "name": req.name,
        },
        task=lambda: _build_markdown_report_payload(req),
        task_payload=_markdown_report_task_payload(req),
        idempotency_key=idempotency_key,
        webhook_config=webhook_config,
    )
    return JSONResponse(
        status_code=202,
        content=attach_branding(
            {
                "success": True,
                "data": _report_job_payload(snapshot, include_result=False),
                "meta": {"acceptedAt": now_cn().isoformat()},
            }
        ),
    )


@app.get("/api/v1/report/jobs/{job_id}")
def get_report_job(job_id: str):
    """查询 Markdown 报告任务状态；成功后返回 Markdown 结果。"""
    try:
        snapshot = report_job_manager.get(job_id)
    except ReportJobNotFound as exc:
        raise HTTPException(status_code=404, detail="报告任务不存在或已过期") from exc
    return attach_branding(
        {
            "success": True,
            "data": _report_job_payload(snapshot, include_result=True),
            "meta": {"checkedAt": now_cn().isoformat()},
        }
    )


@app.post("/api/v1/report/jobs/{job_id}/cancel")
def cancel_report_job(job_id: str):
    """取消报告任务；running 任务无法强杀线程，但完成后会丢弃结果。"""
    try:
        snapshot = report_job_manager.cancel(job_id)
    except ReportJobNotFound as exc:
        raise HTTPException(status_code=404, detail="报告任务不存在或已过期") from exc
    _log_audit_event(
        "report_job.cancel",
        target_type="CalculationJob",
        target_id=job_id,
        metadata={"status": snapshot.status, "ttlSeconds": REPORT_JOB_TTL_SECONDS},
    )
    return attach_branding(
        {
            "success": True,
            "data": _report_job_payload(snapshot, include_result=False),
            "meta": {"cancelledAt": now_cn().isoformat()},
        }
    )


@app.post("/api/v1/report/markdown")
def generate_markdown_report(req: BaziRequest):
    """生成指定体系的 Markdown 报告。"""
    try:
        data = _build_markdown_report_payload(req)
        return attach_branding(
            {
                "success": True,
                "data": data,
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        _log_business_exception("Markdown 报告生成失败", error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/liuyao/factor", response_model=LiuyaoFactorResponse)
def calculate_liuyao_factor(req: LiuyaoFactorRequest):
    """六爻量化因子 - 统一输出结构"""
    try:
        factor = generate_factor(
            item=req.item,
            timestamp=req.timestamp,
            method=req.method,
            seed=req.seed,
            cnts=req.cnts,
            cycle_hint=req.cycleHint,
        )
        data = LiuyaoFactorData(**factor.to_dict())
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )
    except Exception as e:
        _log_business_exception("六爻因子计算失败", error_type=type(e).__name__)
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.get("/api/v1/records/{record_id}")
def get_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    _require_scope(principal, RECORD_SCOPE_READ)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    _log_audit_event(
        "record.read",
        principal=principal,
        target_type="UserRecord",
        target_id=record_id,
        metadata={"bizType": record.get("bizType"), "recordRetentionDays": RECORD_RETENTION_DAYS},
    )
    return attach_branding({"success": True, "data": record})


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(
    user_id: str,
    biz_type: str = None,
    limit: int = Query(default=10, ge=1, le=100),
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取用户记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    _require_scope(principal, RECORD_SCOPE_LIST)
    _require_owner_or_admin(principal, user_id)
    records = db.get_user_records(user_id, biz_type, limit)
    _log_audit_event(
        "record.list",
        principal=principal,
        target_type="UserRecord",
        target_id=user_id,
        metadata={
            "bizType": biz_type or "all",
            "limit": limit,
            "recordCount": len(records),
            "recordRetentionDays": RECORD_RETENTION_DAYS,
        },
    )
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """删除记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    _require_scope(principal, RECORD_SCOPE_DELETE)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    if db.delete_record(record_id):
        _log_audit_event(
            "record.delete",
            principal=principal,
            target_type="UserRecord",
            target_id=record_id,
            metadata={"bizType": record.get("bizType"), "retentionMode": "explicit_delete"},
        )
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
