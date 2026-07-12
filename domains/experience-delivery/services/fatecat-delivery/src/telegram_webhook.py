"""Telegram Webhook 交付运行时。"""

from __future__ import annotations

import asyncio
import logging
import math
import os
import random
import re
import secrets
from collections import deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from threading import Lock
from typing import Any
from urllib.parse import urlparse

from telegram import Update

from service_config import env_flag, env_int

TELEGRAM_DELIVERY_PATH = "/api/v1/integrations/telegram/webhook"
TELEGRAM_ALLOWED_UPDATES = ("message", "callback_query")
_SECRET_PATTERN = re.compile(r"^[A-Za-z0-9_-]{32,256}$")
logger = logging.getLogger(__name__)


class TelegramWebhookError(RuntimeError):
    """Telegram Webhook 可预期错误。"""


class TelegramWebhookDisabled(TelegramWebhookError):
    """Webhook 未启用。"""


class TelegramWebhookUnauthorized(TelegramWebhookError):
    """Webhook Secret 校验失败。"""


class TelegramWebhookQueueFull(TelegramWebhookError):
    """Webhook 更新队列已满。"""


class TelegramWebhookInvalidUpdate(TelegramWebhookError):
    """Telegram Update 无效。"""


@dataclass(frozen=True, repr=False)
class TelegramWebhookConfig:
    enabled: bool
    token: str = field(default="", repr=False)
    secret: str = field(default="", repr=False)
    url: str = ""
    queue_size: int = 20
    dedupe_size: int = 2048
    max_connections: int = 4
    retry_seconds: int = 30
    retry_max_seconds: int = 900
    retry_jitter_percent: int = 20

    @classmethod
    def from_env(cls) -> TelegramWebhookConfig:
        enabled = env_flag("FATE_TELEGRAM_WEBHOOK_ENABLED")
        token = os.getenv("FATE_BOT_TOKEN", "").strip()
        secret = os.getenv("FATE_TELEGRAM_WEBHOOK_SECRET", "").strip()
        explicit_url = os.getenv("FATE_TELEGRAM_WEBHOOK_URL", "").strip()
        space_host = os.getenv("SPACE_HOST", "").strip().strip("/")
        url = explicit_url or (f"https://{space_host}{TELEGRAM_DELIVERY_PATH}" if space_host else "")
        config = cls(
            enabled=enabled,
            token=token,
            secret=secret,
            url=url,
            queue_size=env_int("FATE_TELEGRAM_WEBHOOK_QUEUE_SIZE", 20, minimum=1),
            dedupe_size=env_int("FATE_TELEGRAM_WEBHOOK_DEDUPE_SIZE", 2048, minimum=1),
            max_connections=env_int("FATE_TELEGRAM_WEBHOOK_MAX_CONNECTIONS", 4, minimum=1),
            retry_seconds=env_int("FATE_TELEGRAM_WEBHOOK_RETRY_SECONDS", 30, minimum=5),
            retry_max_seconds=env_int("FATE_TELEGRAM_WEBHOOK_RETRY_MAX_SECONDS", 900, minimum=5),
            retry_jitter_percent=env_int("FATE_TELEGRAM_WEBHOOK_RETRY_JITTER_PERCENT", 20, minimum=0),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.enabled:
            return
        if not self.token:
            raise RuntimeError("启用 Telegram Webhook 时必须配置 FATE_BOT_TOKEN")
        if not _SECRET_PATTERN.fullmatch(self.secret):
            raise RuntimeError("FATE_TELEGRAM_WEBHOOK_SECRET 必须为 32-256 位字母、数字、下划线或连字符")
        parsed = urlparse(self.url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path != TELEGRAM_DELIVERY_PATH:
            raise RuntimeError(f"FATE_TELEGRAM_WEBHOOK_URL 必须是 HTTPS 地址且路径为 {TELEGRAM_DELIVERY_PATH}")
        if self.max_connections > 100:
            raise RuntimeError("FATE_TELEGRAM_WEBHOOK_MAX_CONNECTIONS 不能超过 100")
        if self.retry_max_seconds < self.retry_seconds:
            raise RuntimeError("FATE_TELEGRAM_WEBHOOK_RETRY_MAX_SECONDS 不能小于基础重试间隔")
        if self.retry_jitter_percent > 100:
            raise RuntimeError("FATE_TELEGRAM_WEBHOOK_RETRY_JITTER_PERCENT 不能超过 100")


ApplicationFactory = Callable[[str, asyncio.Queue[object]], Any]
SleepFunction = Callable[[float], Awaitable[None]]


def _build_application(token: str, update_queue: asyncio.Queue[object]) -> Any:
    from bot import build_bot_application

    return build_bot_application(
        token,
        update_queue=update_queue,
        stop_on_health_failure=False,
    )


async def _configure_commands(application: Any) -> None:
    from bot import configure_bot_commands

    await configure_bot_commands(application)


class TelegramWebhookRuntime:
    """在 FastAPI 生命周期内运行 Telegram Application。"""

    def __init__(
        self,
        config: TelegramWebhookConfig,
        *,
        application_factory: ApplicationFactory = _build_application,
        command_configurer: Callable[[Any], Any] = _configure_commands,
        sleep: SleepFunction = asyncio.sleep,
        jitter_source: Callable[[], float] = lambda: random.uniform(-1.0, 1.0),
    ) -> None:
        self.config = config
        self._application_factory = application_factory
        self._command_configurer = command_configurer
        self._sleep = sleep
        self._jitter_source = jitter_source
        self._application: Any | None = None
        self._retry_task: asyncio.Task[None] | None = None
        self._stopping = False
        self._accepted_update_ids: deque[int] = deque()
        self._accepted_update_id_set: set[int] = set()
        self._stats_lock = Lock()
        self._accepted_total = 0
        self._duplicate_total = 0
        self._queue_full_total = 0
        self._unauthorized_total = 0
        self._invalid_total = 0
        self._start_failure_total = 0
        self._last_start_error = ""
        self._retry_attempt = 0
        self._next_retry_seconds = 0.0

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    @property
    def ready(self) -> bool:
        return bool(self._application is not None and getattr(self._application, "running", False))

    async def start(self) -> None:
        if not self.enabled:
            return
        update_queue: asyncio.Queue[object] = asyncio.Queue(maxsize=self.config.queue_size)
        application = self._application_factory(self.config.token, update_queue)
        initialized = False
        try:
            await application.initialize()
            initialized = True
            await self._command_configurer(application)
            await application.start()
            registered = await application.bot.set_webhook(
                url=self.config.url,
                secret_token=self.config.secret,
                allowed_updates=list(TELEGRAM_ALLOWED_UPDATES),
                drop_pending_updates=False,
                max_connections=self.config.max_connections,
            )
            if not registered:
                raise RuntimeError("Telegram setWebhook 返回失败")
        except BaseException:
            if getattr(application, "running", False):
                await application.stop()
            if initialized:
                await application.shutdown()
            raise
        self._application = application
        self._last_start_error = ""
        self._retry_attempt = 0
        self._next_retry_seconds = 0.0

    async def start_managed(self) -> None:
        """启动 Webhook；外部瞬时故障由后台重试，不阻断 Web/API。"""
        self._stopping = False
        if not self.enabled:
            return
        try:
            await self.start()
        except Exception as exc:
            self._record_start_failure(exc)
            self._retry_task = asyncio.create_task(self._retry_until_ready(), name="telegram-webhook-retry")

    def _record_start_failure(self, exc: Exception) -> None:
        error_name = type(exc).__name__
        with self._stats_lock:
            self._start_failure_total += 1
            self._last_start_error = error_name
        logger.warning(
            "Telegram Webhook 启动失败: %s",
            error_name,
        )

    def _retry_delay(self, attempt: int) -> float:
        if self.config.retry_seconds <= 0:
            base = 0.0
        else:
            max_exponent = max(0, math.ceil(math.log2(self.config.retry_max_seconds / self.config.retry_seconds)))
            base = min(self.config.retry_seconds * (2 ** min(attempt, max_exponent)), self.config.retry_max_seconds)
        jitter_ratio = self.config.retry_jitter_percent / 100
        return max(0.0, base * (1 + jitter_ratio * self._jitter_source()))

    async def _retry_until_ready(self) -> None:
        while not self._stopping and not self.ready:
            delay = self._retry_delay(self._retry_attempt)
            self._next_retry_seconds = round(delay, 3)
            logger.warning(
                "Telegram Webhook 将在 %.3f 秒后重试，attempt=%s",
                delay,
                self._retry_attempt + 1,
            )
            await self._sleep(delay)
            if self._stopping:
                return
            try:
                await self.start()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self._record_start_failure(exc)
                self._retry_attempt += 1
            else:
                logger.info("Telegram Webhook 后台重试成功")
                return

    async def stop(self) -> None:
        self._stopping = True
        retry_task = self._retry_task
        self._retry_task = None
        if retry_task is not None and not retry_task.done():
            retry_task.cancel()
            try:
                await retry_task
            except asyncio.CancelledError:
                pass
        application = self._application
        self._application = None
        if application is None:
            return
        if getattr(application, "running", False):
            await application.stop()
        await application.shutdown()

    async def enqueue(self, payload: dict[str, Any], supplied_secret: str | None) -> str:
        if not self.enabled or self._application is None:
            raise TelegramWebhookDisabled("Telegram Webhook 未启用")
        if not supplied_secret or not secrets.compare_digest(supplied_secret, self.config.secret):
            with self._stats_lock:
                self._unauthorized_total += 1
            raise TelegramWebhookUnauthorized("Telegram Webhook 未授权")
        try:
            update = Update.de_json(payload, self._application.bot)
        except Exception as exc:
            with self._stats_lock:
                self._invalid_total += 1
            raise TelegramWebhookInvalidUpdate("Telegram Update 格式无效") from exc
        if update.update_id is None:
            with self._stats_lock:
                self._invalid_total += 1
            raise TelegramWebhookInvalidUpdate("Telegram Update 缺少 update_id")
        if update.update_id in self._accepted_update_id_set:
            with self._stats_lock:
                self._duplicate_total += 1
            return "duplicate"
        try:
            self._application.update_queue.put_nowait(update)
        except asyncio.QueueFull as exc:
            with self._stats_lock:
                self._queue_full_total += 1
            raise TelegramWebhookQueueFull("Telegram Webhook 队列已满") from exc
        self._remember_update_id(update.update_id)
        with self._stats_lock:
            self._accepted_total += 1
        return "accepted"

    def _remember_update_id(self, update_id: int) -> None:
        self._accepted_update_ids.append(update_id)
        self._accepted_update_id_set.add(update_id)
        while len(self._accepted_update_ids) > self.config.dedupe_size:
            expired = self._accepted_update_ids.popleft()
            self._accepted_update_id_set.discard(expired)

    def status(self) -> dict[str, int | float | bool | str]:
        application = self._application
        queue = getattr(application, "update_queue", None) if application is not None else None
        with self._stats_lock:
            return {
                "enabled": self.enabled,
                "ready": self.ready,
                "mode": "webhook" if self.enabled else "disabled",
                "queueDepth": queue.qsize() if queue is not None else 0,
                "queueCapacity": self.config.queue_size,
                "acceptedTotal": self._accepted_total,
                "duplicateTotal": self._duplicate_total,
                "queueFullTotal": self._queue_full_total,
                "unauthorizedTotal": self._unauthorized_total,
                "invalidTotal": self._invalid_total,
                "startFailureTotal": self._start_failure_total,
                "lastStartError": self._last_start_error,
                "retryAttempt": self._retry_attempt,
                "nextRetrySeconds": self._next_retry_seconds,
            }


__all__ = [
    "TELEGRAM_DELIVERY_PATH",
    "TelegramWebhookConfig",
    "TelegramWebhookDisabled",
    "TelegramWebhookInvalidUpdate",
    "TelegramWebhookQueueFull",
    "TelegramWebhookRuntime",
    "TelegramWebhookUnauthorized",
]
