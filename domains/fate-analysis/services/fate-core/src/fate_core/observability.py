from __future__ import annotations

import json
import logging
import re
import secrets
import time
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import Any

TRACEPARENT_VERSION = "00"
TRACE_FLAGS_DEFAULT = "01"
_TRACE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_SPAN_ID_RE = re.compile(r"^[0-9a-f]{16}$")
_TRACE_FLAGS_RE = re.compile(r"^[0-9a-f]{2}$")
_trace_context: ContextVar[TraceContext | None] = ContextVar("fatecat_trace_context", default=None)
logger = logging.getLogger("fate_core.observability")


@dataclass(frozen=True)
class TraceContext:
    """W3C trace context 的最小本地表示。"""

    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    trace_flags: str = TRACE_FLAGS_DEFAULT

    def traceparent(self) -> str:
        return f"{TRACEPARENT_VERSION}-{self.trace_id}-{self.span_id}-{self.trace_flags}"


def _new_trace_id() -> str:
    while True:
        value = secrets.token_hex(16)
        if value != "0" * 32:
            return value


def _new_span_id() -> str:
    while True:
        value = secrets.token_hex(8)
        if value != "0" * 16:
            return value


def _valid_trace_id(value: str) -> bool:
    return bool(_TRACE_ID_RE.fullmatch(value)) and value != "0" * 32


def _valid_span_id(value: str) -> bool:
    return bool(_SPAN_ID_RE.fullmatch(value)) and value != "0" * 16


def _valid_trace_flags(value: str) -> bool:
    return bool(_TRACE_FLAGS_RE.fullmatch(value))


def new_trace_context() -> TraceContext:
    return TraceContext(trace_id=_new_trace_id(), span_id=_new_span_id())


def trace_context_from_traceparent(value: str | None) -> TraceContext:
    """解析 W3C traceparent；非法输入时生成新 trace，避免传播坏上下文。"""

    raw = (value or "").strip().lower()
    parts = raw.split("-")
    if (
        len(parts) == 4
        and parts[0] == TRACEPARENT_VERSION
        and _valid_trace_id(parts[1])
        and _valid_span_id(parts[2])
        and _valid_trace_flags(parts[3])
    ):
        return TraceContext(
            trace_id=parts[1],
            span_id=_new_span_id(),
            parent_span_id=parts[2],
            trace_flags=parts[3],
        )
    return new_trace_context()


def set_trace_context(context: TraceContext | None) -> Token[TraceContext | None]:
    return _trace_context.set(context)


def reset_trace_context(token: Token[TraceContext | None]) -> None:
    _trace_context.reset(token)


def current_trace_context() -> TraceContext | None:
    return _trace_context.get()


def current_trace_id() -> str:
    context = current_trace_context()
    return context.trace_id if context else "-"


def current_traceparent() -> str | None:
    context = current_trace_context()
    return context.traceparent() if context else None


def _sanitize_attribute(value: Any) -> Any:
    if isinstance(value, str):
        return value[:160]
    if isinstance(value, bool | int | float) or value is None:
        return value
    if isinstance(value, tuple | list):
        return [_sanitize_attribute(item) for item in value[:8]]
    return str(value)[:160]


def _sanitize_attributes(attributes: dict[str, Any] | None) -> dict[str, Any]:
    if not attributes:
        return {}
    return {str(key)[:80]: _sanitize_attribute(value) for key, value in sorted(attributes.items())}


def _emit_span(payload: dict[str, Any]) -> None:
    logger.info(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


@contextmanager
def trace_span(
    span_name: str,
    *,
    span_kind: str = "internal",
    attributes: dict[str, Any] | None = None,
):
    """记录 OpenTelemetry 语义兼容的本地 span 日志。

    当前实现只做本地结构化日志，不接外部 collector；字段保持低敏感度。
    """

    parent = current_trace_context() or new_trace_context()
    span = TraceContext(
        trace_id=parent.trace_id,
        span_id=_new_span_id(),
        parent_span_id=parent.span_id,
        trace_flags=parent.trace_flags,
    )
    token = set_trace_context(span)
    started = time.perf_counter()
    status = "ok"
    error_type: str | None = None
    try:
        yield span
    except Exception as exc:
        status = "error"
        error_type = type(exc).__name__
        raise
    finally:
        duration_ms = round((time.perf_counter() - started) * 1000, 3)
        payload: dict[str, Any] = {
            "event": "trace_span",
            "traceId": span.trace_id,
            "spanId": span.span_id,
            "parentSpanId": span.parent_span_id,
            "spanName": span_name,
            "spanKind": span_kind,
            "status": status,
            "durationMs": duration_ms,
            "attributes": _sanitize_attributes(attributes),
            "traceSemantic": "w3c-trace-context-local-otel-compatible",
        }
        if error_type:
            payload["errorType"] = error_type
        reset_trace_context(token)
        _emit_span(payload)
