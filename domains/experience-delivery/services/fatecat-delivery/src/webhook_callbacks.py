"""报告任务 webhook 回调。

该模块只负责把已完成的 CalculationJob 终态事件投递给调用方配置的回调 URL。
它不保存 webhook secret，不发送报告正文，也不实现持久重试队列。
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from report_jobs import ReportJobSnapshot
from utils.timezone import now_cn

WEBHOOK_EVENT_TYPE_REPORT_JOB_TERMINAL = "report_job.terminal"
WEBHOOK_SIGNATURE_HEADER = "X-FateCat-Webhook-Signature"
WEBHOOK_TIMESTAMP_HEADER = "X-FateCat-Webhook-Timestamp"
WEBHOOK_EVENT_HEADER = "X-FateCat-Webhook-Event"

WebhookTransport = Callable[[str, bytes, Mapping[str, str], int], int]


class WebhookDeliveryError(RuntimeError):
    """webhook 投递失败。"""


@dataclass(frozen=True)
class WebhookConfig:
    """单个报告任务的回调配置。

    `secret` 只驻留内存，不能写入 job store、audit log 或响应体。
    """

    url: str
    secret: str | None = None
    allowed_hosts: tuple[str, ...] = ()
    allow_http: bool = False

    def __post_init__(self) -> None:
        normalized_url = validate_webhook_url(
            self.url,
            allowed_hosts=self.allowed_hosts,
            allow_http=self.allow_http,
        )
        object.__setattr__(self, "url", normalized_url)
        normalized_secret = str(self.secret or "").strip() or None
        object.__setattr__(self, "secret", normalized_secret)

    @property
    def signature_mode(self) -> str:
        return "hmac-sha256" if self.secret else "none"


@dataclass(frozen=True)
class WebhookDeliveryResult:
    status_code: int
    event_id: str
    event_type: str


class HttpWebhookDispatcher:
    """标准库 HTTP webhook 投递器。"""

    def __init__(
        self,
        *,
        timeout_seconds: int = 5,
        transport: WebhookTransport | None = None,
    ) -> None:
        self.timeout_seconds = max(1, int(timeout_seconds))
        self._transport = transport or _urlopen_transport

    def deliver(self, snapshot: ReportJobSnapshot, config: WebhookConfig) -> WebhookDeliveryResult:
        payload = build_report_job_webhook_payload(snapshot)
        event_id = str(payload["eventId"])
        body = encode_webhook_payload(payload)
        timestamp = str(int(time.time()))
        headers = build_webhook_headers(
            event_type=WEBHOOK_EVENT_TYPE_REPORT_JOB_TERMINAL,
            body=body,
            timestamp=timestamp,
            secret=config.secret,
        )
        status_code = self._transport(config.url, body, headers, self.timeout_seconds)
        if status_code >= 400:
            raise WebhookDeliveryError(f"webhook endpoint returned HTTP {status_code}")
        return WebhookDeliveryResult(
            status_code=status_code,
            event_id=event_id,
            event_type=WEBHOOK_EVENT_TYPE_REPORT_JOB_TERMINAL,
        )


def build_report_job_webhook_payload(snapshot: ReportJobSnapshot) -> dict[str, Any]:
    """构造不含报告正文和用户输入的任务终态事件。"""

    terminal_statuses = {"succeeded", "failed", "cancelled"}
    if snapshot.status not in terminal_statuses:
        raise ValueError(f"webhook 只支持终态任务: {snapshot.status}")
    status_url = f"/api/v1/report/jobs/{snapshot.job_id}"
    cancel_url = f"/api/v1/report/jobs/{snapshot.job_id}/cancel"
    event_id = f"evt_{snapshot.job_id}_{snapshot.status}"
    return {
        "resourceType": "WebhookEvent",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "eventType": WEBHOOK_EVENT_TYPE_REPORT_JOB_TERMINAL,
        "eventId": event_id,
        "id": event_id,
        "createdAt": now_cn().isoformat(),
        "links": {
            "job": status_url,
            "cancel": cancel_url,
        },
        "metadata": {
            "source": "report_job_manager",
            "privacyBoundary": "terminal event excludes report markdown, user input and webhook secret",
        },
        "data": {
            "resourceType": "CalculationJob",
            "jobId": snapshot.job_id,
            "kind": snapshot.kind,
            "status": snapshot.status,
            "reportSystem": snapshot.report_system,
            "createdAt": snapshot.created_at,
            "startedAt": snapshot.started_at,
            "finishedAt": snapshot.finished_at,
            "expiresAt": snapshot.expires_at,
            "statusUrl": status_url,
            "cancelUrl": cancel_url,
            "resultAvailable": snapshot.status == "succeeded" and snapshot.result is not None,
            "error": _truncate_error(snapshot.error),
        },
    }


def encode_webhook_payload(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def build_webhook_headers(
    *,
    event_type: str,
    body: bytes,
    timestamp: str,
    secret: str | None,
) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        WEBHOOK_EVENT_HEADER: event_type,
        WEBHOOK_TIMESTAMP_HEADER: timestamp,
        "User-Agent": "FateCat-Webhook/1.0",
    }
    if secret:
        headers[WEBHOOK_SIGNATURE_HEADER] = sign_webhook_body(body=body, secret=secret)
    return headers


def sign_webhook_body(*, body: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def validate_webhook_url(
    url: str,
    *,
    allowed_hosts: tuple[str, ...] = (),
    allow_http: bool = False,
) -> str:
    normalized = str(url or "").strip()
    if not normalized:
        raise ValueError("webhook URL 不能为空")
    if len(normalized) > 2048:
        raise ValueError("webhook URL 过长")
    parsed = urllib.parse.urlparse(normalized)
    allowed_schemes = {"https"} | ({"http"} if allow_http else set())
    if parsed.scheme not in allowed_schemes:
        raise ValueError("webhook URL 必须使用 https；本地调试需显式开启 http")
    if not parsed.hostname:
        raise ValueError("webhook URL 缺少 host")
    if parsed.username or parsed.password:
        raise ValueError("webhook URL 不允许包含用户名或密码")
    hostname = parsed.hostname.lower()
    _reject_private_hostname(hostname)
    if allowed_hosts and not _host_allowed(hostname, allowed_hosts):
        raise ValueError("webhook URL host 不在 allowlist")
    return normalized


def parse_allowed_hosts(raw_value: str | None) -> tuple[str, ...]:
    if not raw_value:
        return ()
    return tuple(item.strip().lower() for item in raw_value.split(",") if item.strip())


def _urlopen_transport(url: str, body: bytes, headers: Mapping[str, str], timeout_seconds: int) -> int:
    request = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
            response.read(1024)
            return int(response.getcode())
    except urllib.error.HTTPError as exc:
        return int(exc.code)
    except urllib.error.URLError as exc:
        raise WebhookDeliveryError(str(exc.reason)) from exc


def _reject_private_hostname(hostname: str) -> None:
    blocked_names = {"localhost", "localhost.localdomain"}
    if hostname in blocked_names or hostname.endswith(".localhost"):
        raise ValueError("webhook URL 不允许指向本机地址")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return
    if (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_multicast
        or address.is_unspecified
    ):
        raise ValueError("webhook URL 不允许指向内网、保留或本机地址")


def _host_allowed(hostname: str, allowed_hosts: tuple[str, ...]) -> bool:
    for item in allowed_hosts:
        allowed = item.strip().lower()
        if not allowed:
            continue
        if allowed.startswith("*.") and hostname.endswith(allowed[1:]):
            return True
        if hostname == allowed:
            return True
    return False


def _truncate_error(error: str | None) -> str | None:
    if not error:
        return None
    normalized = " ".join(str(error).split())
    return normalized[:240]
