import asyncio
import json
import logging
import os
import secrets
import sys
import time
import uuid
from collections import defaultdict, deque
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime
from threading import BoundedSemaphore, Lock
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

from _paths import FATE_CORE_SRC_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from service_config import cors_allow_origins, env_flag, env_int
from utils.timezone import now_cn

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
TRUST_PROXY_HEADERS = env_flag("FATE_TRUST_PROXY_HEADERS")
ENABLE_HSTS = env_flag("FATE_ENABLE_HSTS")

import db_v2 as db  # noqa: E402
from calculation_service import calculate_delivery_result  # noqa: E402
from fate_core.capabilities import CapabilityExecutor, CapabilityInput, list_capabilities  # noqa: E402
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis  # noqa: E402
from liuyao_factors import generate_factor  # noqa: E402
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
from report_jobs import ReportJobManager, ReportJobNotFound, ReportJobQueueFull, ReportJobSnapshot  # noqa: E402
from web_forms import WebReportForm, WebReportJobView, WebReportResult  # noqa: E402
from web_report_service import build_web_report_result, validate_web_report_form  # noqa: E402
from web_ui import render_web_report_page  # noqa: E402

logger = logging.getLogger(__name__)
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
_RATE_LIMIT_EXEMPT_PATHS = {"/health", "/live", "/ready", "/metrics"}
_REQUEST_LATENCY_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
_BODY_LIMIT_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
report_job_manager = ReportJobManager(
    max_workers=REPORT_JOB_WORKERS,
    queue_size=REPORT_JOB_QUEUE_SIZE,
    ttl_seconds=REPORT_JOB_TTL_SECONDS,
)


def _records_enabled() -> bool:
    return os.getenv("FATE_RECORDS_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}


if _records_enabled():
    db.ensure_db()


@dataclass(frozen=True)
class ApiPrincipal:
    role: str
    user_id: str | None = None

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


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


def _user_tokens() -> dict[str, str]:
    raw = os.getenv("FATE_API_USER_TOKENS", "").strip()
    if not raw:
        return {}

    mapping: dict[str, str] = {}
    for item in raw.split(","):
        user_id, sep, token = item.strip().partition(":")
        if sep and user_id.strip() and token.strip():
            mapping[user_id.strip()] = token.strip()
    return mapping


def _require_record_access(x_api_key: str | None, authorization: str | None) -> ApiPrincipal:
    if not _records_enabled():
        raise HTTPException(status_code=403, detail="记录接口未启用")
    admin_tokens = _admin_tokens()
    user_tokens = _user_tokens()
    if not admin_tokens and not user_tokens:
        raise HTTPException(status_code=403, detail="记录接口未启用")
    supplied = _extract_auth_token(x_api_key, authorization)
    if not supplied:
        raise HTTPException(status_code=403, detail="未授权")
    for token in admin_tokens:
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="admin")
    for user_id, token in user_tokens.items():
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="user", user_id=user_id)
    raise HTTPException(status_code=403, detail="未授权")


def _require_owner_or_admin(principal: ApiPrincipal, user_id: str) -> None:
    if principal.is_admin:
        return
    if principal.user_id == user_id:
        return
    raise HTTPException(status_code=403, detail="无权访问该记录")


app = FastAPI(title="八字排盘服务", version="1.0.0")
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
        "jobId": snapshot.job_id,
        "kind": snapshot.kind,
        "status": snapshot.status,
        "reportSystem": snapshot.report_system,
        "queuePosition": snapshot.queue_position,
        "createdAt": snapshot.created_at,
        "startedAt": snapshot.started_at,
        "finishedAt": snapshot.finished_at,
        "expiresAt": snapshot.expires_at,
        "error": snapshot.error,
        "statusUrl": f"/api/v1/report/jobs/{snapshot.job_id}",
        "input": snapshot.input_summary,
    }
    if include_result and snapshot.status == "succeeded":
        payload["result"] = _serialize_report_job_result(snapshot.result)
    return payload


def _serialize_report_job_result(result: Any) -> dict[str, Any] | None:
    if isinstance(result, WebReportResult):
        return {
            "reportSystem": result.report_system,
            "reportSystemLabel": result.report_system_label,
            "markdown": result.markdown,
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
    }


def _capabilities_payload() -> dict[str, Any]:
    markdown_enabled_ids = set(enabled_report_system_ids())
    return {"capabilities": [_capability_item_payload(item, markdown_enabled_ids) for item in list_capabilities()]}


def _submit_report_job(
    *,
    kind: str,
    report_system: str,
    task,
    input_summary: dict[str, Any],
) -> ReportJobSnapshot:
    try:
        return report_job_manager.submit(
            kind=kind,
            report_system=report_system,
            task=task,
            input_summary=input_summary,
        )
    except ReportJobQueueFull as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc


def _apply_public_response_headers(response: Response, request_id: str) -> Response:
    response.headers["X-Request-ID"] = request_id
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
    started = time.perf_counter()
    try:
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


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


@app.get("/live")
def live():
    return attach_branding({"status": "live"})


@app.get("/ready")
def ready():
    checks = {"database": "disabled" if not _records_enabled() else "ok", "capabilities": "ok"}
    try:
        if _records_enabled():
            db.ensure_db()
        list_capabilities()
    except Exception as exc:
        _log_business_exception("readiness 检查失败", error_type=type(exc).__name__)
        return JSONResponse(
            status_code=503,
            content=attach_branding({"status": "not_ready", "checks": checks, "error": str(exc)}),
        )
    return attach_branding({"status": "ready", "checks": checks})


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
            "# HELP fatecat_report_job_queue_size Current Web/API report jobs waiting in memory queue.",
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
        ]
    )
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")


@app.get("/web", response_class=HTMLResponse)
def web_report(
    birthDate: str | None = None,
    birthTime: str | None = None,
    birthPlace: str | None = None,
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
        gender=gender,
        name=name,
        report_system=reportSystem,
        submitted=submitted,
        job=job,
    )


@app.post("/api/v1/report/jobs/web")
def create_web_report_job(payload: dict[str, Any]):
    """提交 Web 表单报告任务；公开工作台默认使用该异步入口。"""
    form = _web_form_from_payload(payload)
    try:
        validated = validate_web_report_form(form)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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


@app.post("/api/v1/capabilities/{capability_id}")
def execute_prediction_capability(capability_id: str, payload: dict[str, Any]):
    """执行已生产化的独立 capability。"""
    try:
        result = _run_with_calculation_slot(
            lambda: CapabilityExecutor().execute(CapabilityInput(capability_id=capability_id, payload=payload))
        )
        return attach_branding(
            {
                "success": True,
                "capabilityId": result.capability_id,
                "status": result.status,
                "reportProfile": result.report_profile,
                "data": result.data,
                "evidence": result.evidence,
                "risk": result.risk,
                "metadata": result.metadata,
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/capabilities/{capability_id}/calculate")
def calculate_measurement_capability(capability_id: str, payload: dict[str, Any]):
    """基础设施口径 capability 执行别名。"""
    return execute_prediction_capability(capability_id, payload)


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
                "webJobEndpoint": "/api/v1/report/jobs/web",
                "statusEndpoint": "/api/v1/report/jobs/{job_id}",
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
                },
                "surfaces": ["CLI", "Web", "FastAPI", "Telegram", "Agent Skill"],
                "quality": {
                    "health": "/health",
                    "readiness": "/ready",
                    "metrics": "/metrics",
                    "rateLimitPerMinute": RATE_LIMIT_PER_MINUTE,
                    "maxInflightCalculations": MAX_INFLIGHT_CALCULATIONS,
                    "reportJobQueueSize": REPORT_JOB_QUEUE_SIZE,
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
    }


def _parse_bazi_request(req: BaziRequest) -> tuple[datetime, float, float]:
    _validate_supported_bazi_options(req)
    birth_time = req.birthTime.strip()
    if len(birth_time) == 5:
        birth_time = f"{birth_time}:00"
    try:
        birth_dt = datetime.strptime(f"{req.birthDate.strip()} {birth_time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="出生日期或出生时间格式无效；日期使用 YYYY-MM-DD，时间使用 HH:MM 或 HH:MM:SS。",
        ) from exc
    if not req.birthPlace:
        raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
    return birth_dt, req.birthPlace.longitude, req.birthPlace.latitude


def _build_bazi_data(result: dict, *, birth_dt: datetime, true_solar_time: datetime | None, timezone: str) -> BaziData:
    major_fortune = dict(result.get("majorFortune", {}))
    major_fortune["pillars"] = [
        {
            **pillar,
            "year": pillar.get("year", pillar.get("startYear")),
        }
        for pillar in major_fortune.get("pillars", [])
        if isinstance(pillar, dict)
    ]

    tz = ZoneInfo(timezone)
    return BaziData(
        timeInfo=TimeInfo(
            inputTime=birth_dt.replace(tzinfo=tz).isoformat(),
            trueSolarTime=true_solar_time.replace(tzinfo=tz).isoformat() if true_solar_time else None,
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


def _calculate_bazi_raw(req: BaziRequest, *, report_system: str = "bazi") -> tuple[dict, Any, datetime]:
    birth_dt, longitude, latitude = _parse_bazi_request(req)
    calculation = calculate_delivery_result(
        birth_dt=birth_dt,
        gender=req.gender,
        longitude=longitude,
        latitude=latitude,
        birth_place=req.birthPlace.name,
        name=req.name,
        report_system=report_system,
        use_true_solar_time=req.options.useTrueSolarTime,
    )
    if calculation.calculator is None:
        raise RuntimeError("_calculate_bazi_raw 只用于 bazi 体系")
    return calculation.data, calculation.calculator, birth_dt


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        result, _calculator, _birth_dt = _run_with_calculation_slot(
            lambda: _calculate_bazi_raw(req, report_system="bazi")
        )

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
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        payload = PureAnalysisInput(
            birth_dt=birth_dt,
            gender=req.gender,
            longitude=longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
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


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(
    req: BaziRequest,
    user_id: str | None = None,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """计算八字排盘"""
    try:
        if user_id:
            principal = _require_record_access(x_fatecat_api_key, authorization)
            _require_owner_or_admin(principal, user_id)
        result, calculator, birth_dt = _run_with_calculation_slot(
            lambda: _calculate_bazi_raw(req, report_system="bazi")
        )

        ts_dt = calculator.true_solar_time if req.options.useTrueSolarTime else birth_dt
        data = _build_bazi_data(
            result,
            birth_dt=birth_dt,
            true_solar_time=ts_dt if req.options.useTrueSolarTime else None,
            timezone=req.birthPlace.timezone,
        )

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
                birth_place=req.birthPlace.name,
                longitude=req.birthPlace.longitude,
                latitude=req.birthPlace.latitude,
                dst=0,
                true_solar=1 if req.options.useTrueSolarTime else 0,
                early_zi=1 if req.options.midnightMode == "early" else 0,
                biz_data={
                    "input": req.model_dump(),
                    "normalizedOptions": _normalized_bazi_options(req, report_system="bazi"),
                    "result": result,
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
    birth_dt, longitude, latitude = _parse_bazi_request(req)
    calculation = _run_with_calculation_slot(
        lambda: calculate_delivery_result(
            birth_dt=birth_dt,
            gender=req.gender,
            longitude=longitude,
            latitude=latitude,
            birth_place=req.birthPlace.name,
            name=req.name,
            report_system=req.options.reportSystem,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
    )
    markdown = generate_full_report(
        calculation.data,
        hide=calculation.report_hide,
        report_system=calculation.report_system,
    )
    return {
        "reportSystem": calculation.report_system,
        "markdown": markdown,
    }


@app.post("/api/v1/report/jobs")
def create_markdown_report_job(req: BaziRequest):
    """提交标准 Markdown 报告生成任务。"""
    report_system = normalize_report_system(req.options.reportSystem)
    birth_place = public_birth_place(req.birthPlace.name) if req.birthPlace else ""
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
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
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
    _require_owner_or_admin(principal, user_id)
    records = db.get_user_records(user_id, biz_type, limit)
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """删除记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    if db.delete_record(record_id):
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
