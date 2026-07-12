from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
TEST_SECRET = "test_webhook_secret_for_fatecat_2026"

for source_dir in (DELIVERY_SRC, FATE_CORE_SRC):
    if str(source_dir) not in sys.path:
        sys.path.insert(0, str(source_dir))

import _paths  # noqa: E402
import main  # noqa: E402
from telegram_webhook import (  # noqa: E402
    TELEGRAM_DELIVERY_PATH,
    TelegramWebhookConfig,
    TelegramWebhookQueueFull,
    TelegramWebhookRuntime,
    TelegramWebhookUnauthorized,
)


class FakeBot:
    def __init__(self) -> None:
        self.webhook_kwargs: dict[str, Any] | None = None

    async def set_webhook(self, **kwargs: Any) -> bool:
        self.webhook_kwargs = kwargs
        return True


class FakeApplication:
    def __init__(self, update_queue: asyncio.Queue[object], *, initialize_error: Exception | None = None) -> None:
        self.bot = FakeBot()
        self.update_queue = update_queue
        self.initialize_error = initialize_error
        self.running = False
        self.initialized = False
        self.shutdown_called = False

    async def initialize(self) -> None:
        if self.initialize_error is not None:
            raise self.initialize_error
        self.initialized = True

    async def start(self) -> None:
        self.running = True

    async def stop(self) -> None:
        self.running = False

    async def shutdown(self) -> None:
        self.shutdown_called = True


def _config(
    *,
    queue_size: int = 2,
    retry_seconds: int = 30,
    retry_max_seconds: int = 900,
    retry_jitter_percent: int = 20,
) -> TelegramWebhookConfig:
    return TelegramWebhookConfig(
        enabled=True,
        token="123456:test-token",
        secret=TEST_SECRET,
        url=f"https://example.hf.space{TELEGRAM_DELIVERY_PATH}",
        queue_size=queue_size,
        dedupe_size=2,
        max_connections=4,
        retry_seconds=retry_seconds,
        retry_max_seconds=retry_max_seconds,
        retry_jitter_percent=retry_jitter_percent,
    )


def _runtime(*, queue_size: int = 2) -> tuple[TelegramWebhookRuntime, list[FakeApplication]]:
    applications: list[FakeApplication] = []

    def factory(_token: str, update_queue: asyncio.Queue[object]) -> FakeApplication:
        application = FakeApplication(update_queue)
        applications.append(application)
        return application

    async def configure_commands(_application: FakeApplication) -> None:
        return None

    return (
        TelegramWebhookRuntime(
            _config(queue_size=queue_size),
            application_factory=factory,
            command_configurer=configure_commands,
        ),
        applications,
    )


def test_telegram_webhook_config_is_disabled_by_default(monkeypatch: pytest.MonkeyPatch):
    for name in (
        "FATE_TELEGRAM_WEBHOOK_ENABLED",
        "FATE_BOT_TOKEN",
        "FATE_TELEGRAM_WEBHOOK_SECRET",
        "FATE_TELEGRAM_WEBHOOK_URL",
        "SPACE_HOST",
    ):
        monkeypatch.delenv(name, raising=False)

    config = TelegramWebhookConfig.from_env()

    assert config.enabled is False
    assert "test-token" not in repr(config)


def test_bot_dependency_check_accepts_platform_token_without_local_env(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    monkeypatch.setattr(_paths, "ENV_FILE", tmp_path / "missing.env")
    monkeypatch.setenv("FATE_BOT_TOKEN", "123456:platform-token")

    result = _paths.check_dependencies()

    assert result["ok"] is True
    assert not any("配置文件" in error for error in result["errors"])


def test_telegram_webhook_config_derives_hf_url(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FATE_TELEGRAM_WEBHOOK_ENABLED", "1")
    monkeypatch.setenv("FATE_BOT_TOKEN", "123456:test-token")
    monkeypatch.setenv("FATE_TELEGRAM_WEBHOOK_SECRET", TEST_SECRET)
    monkeypatch.setenv("SPACE_HOST", "tradecatlabs-fatecat.hf.space")
    monkeypatch.delenv("FATE_TELEGRAM_WEBHOOK_URL", raising=False)

    config = TelegramWebhookConfig.from_env()

    assert config.url == f"https://tradecatlabs-fatecat.hf.space{TELEGRAM_DELIVERY_PATH}"


def test_telegram_webhook_config_rejects_missing_secret(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FATE_TELEGRAM_WEBHOOK_ENABLED", "1")
    monkeypatch.setenv("FATE_BOT_TOKEN", "123456:test-token")
    monkeypatch.delenv("FATE_TELEGRAM_WEBHOOK_SECRET", raising=False)
    monkeypatch.setenv("SPACE_HOST", "tradecatlabs-fatecat.hf.space")

    with pytest.raises(RuntimeError, match="FATE_TELEGRAM_WEBHOOK_SECRET"):
        TelegramWebhookConfig.from_env()


def test_telegram_webhook_config_rejects_short_secret(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FATE_TELEGRAM_WEBHOOK_ENABLED", "1")
    monkeypatch.setenv("FATE_BOT_TOKEN", "123456:test-token")
    monkeypatch.setenv("FATE_TELEGRAM_WEBHOOK_SECRET", "too-short")
    monkeypatch.setenv("SPACE_HOST", "tradecatlabs-fatecat.hf.space")

    with pytest.raises(RuntimeError, match="32-256"):
        TelegramWebhookConfig.from_env()


@pytest.mark.asyncio
async def test_telegram_webhook_runtime_registers_and_queues_updates():
    runtime, applications = _runtime()

    await runtime.start()
    application = applications[0]
    assert runtime.ready is True
    assert application.bot.webhook_kwargs == {
        "url": f"https://example.hf.space{TELEGRAM_DELIVERY_PATH}",
        "secret_token": TEST_SECRET,
        "allowed_updates": ["message", "callback_query"],
        "drop_pending_updates": False,
        "max_connections": 4,
    }

    assert await runtime.enqueue({"update_id": 1001}, TEST_SECRET) == "accepted"
    assert await runtime.enqueue({"update_id": 1001}, TEST_SECRET) == "duplicate"
    assert application.update_queue.qsize() == 1
    assert runtime.status()["acceptedTotal"] == 1
    assert runtime.status()["duplicateTotal"] == 1

    with pytest.raises(TelegramWebhookUnauthorized):
        await runtime.enqueue({"update_id": 1002}, "wrong-secret")

    await runtime.stop()
    assert runtime.ready is False
    assert application.shutdown_called is True


@pytest.mark.asyncio
async def test_telegram_webhook_runtime_returns_backpressure_when_queue_is_full():
    runtime, _applications = _runtime(queue_size=1)
    await runtime.start()

    assert await runtime.enqueue({"update_id": 2001}, TEST_SECRET) == "accepted"
    with pytest.raises(TelegramWebhookQueueFull):
        await runtime.enqueue({"update_id": 2002}, TEST_SECRET)
    assert runtime.status()["queueFullTotal"] == 1

    await runtime.stop()


@pytest.mark.asyncio
async def test_telegram_webhook_managed_start_retries_without_blocking_api():
    applications: list[FakeApplication] = []

    def factory(_token: str, update_queue: asyncio.Queue[object]) -> FakeApplication:
        initialize_error = TimeoutError("temporary") if not applications else None
        application = FakeApplication(update_queue, initialize_error=initialize_error)
        applications.append(application)
        return application

    async def configure_commands(_application: FakeApplication) -> None:
        return None

    runtime = TelegramWebhookRuntime(
        _config(retry_seconds=0, retry_max_seconds=0, retry_jitter_percent=0),
        application_factory=factory,
        command_configurer=configure_commands,
    )

    await runtime.start_managed()
    for _ in range(20):
        if runtime.ready:
            break
        await asyncio.sleep(0)

    assert runtime.ready is True
    assert runtime.status()["startFailureTotal"] == 1
    assert runtime.status()["lastStartError"] == ""
    await runtime.stop()


@pytest.mark.asyncio
async def test_telegram_webhook_retry_uses_bounded_exponential_backoff():
    delays: list[float] = []
    attempts = 0

    async def sleep(delay: float) -> None:
        delays.append(delay)

    def factory(_token: str, update_queue: asyncio.Queue[object]) -> FakeApplication:
        nonlocal attempts
        attempts += 1
        error = TimeoutError("temporary") if attempts < 4 else None
        return FakeApplication(update_queue, initialize_error=error)

    async def configure_commands(_application: FakeApplication) -> None:
        return None

    runtime = TelegramWebhookRuntime(
        _config(retry_seconds=5, retry_max_seconds=12, retry_jitter_percent=0),
        application_factory=factory,
        command_configurer=configure_commands,
        sleep=sleep,
    )

    await runtime.start_managed()
    for _ in range(20):
        if runtime.ready:
            break
        await asyncio.sleep(0)

    assert runtime.ready is True
    assert delays == [5, 10, 12]
    assert runtime.status()["retryAttempt"] == 0
    assert runtime.status()["nextRetrySeconds"] == 0.0
    await runtime.stop()


def test_telegram_webhook_retry_does_not_build_unbounded_exponents():
    runtime = TelegramWebhookRuntime(
        _config(retry_seconds=5, retry_max_seconds=12, retry_jitter_percent=0),
    )

    assert runtime._retry_delay(1_000_000) == 12


def test_telegram_webhook_http_surface_is_disabled_without_configuration():
    client = TestClient(main.app)

    response = client.post(
        TELEGRAM_DELIVERY_PATH,
        json={"update_id": 1},
        headers={"X-Telegram-Bot-Api-Secret-Token": TEST_SECRET},
    )

    assert response.status_code == 404
    assert TELEGRAM_DELIVERY_PATH in client.get("/openapi.json").json()["paths"]
    assert client.get("/ready").json()["checks"]["telegramWebhook"] == "disabled"
    metrics = client.get("/metrics").text
    assert "fatecat_telegram_webhook_enabled 0" in metrics
    assert "fatecat_telegram_webhook_ready 0" in metrics


def test_core_readiness_reports_degraded_telegram_without_returning_503(monkeypatch: pytest.MonkeyPatch):
    class DegradedRuntime:
        def status(self) -> dict[str, int | float | bool | str]:
            return {
                "enabled": True,
                "ready": False,
                "startFailureTotal": 3,
                "lastStartError": "TimedOut",
            }

    monkeypatch.setattr(main, "telegram_webhook_runtime", DegradedRuntime())

    response = TestClient(main.app).get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["telegramWebhook"] == "not_ready"
    assert response.json()["degraded"] is True
    assert response.json()["degradedSurfaces"] == ["telegramWebhook"]


def test_telegram_webhook_http_surface_accepts_authenticated_update(monkeypatch: pytest.MonkeyPatch):
    class FakeRuntime:
        enabled = True

        async def enqueue(self, payload: dict[str, Any], supplied_secret: str | None) -> str:
            assert payload == {"update_id": 3001}
            assert supplied_secret == TEST_SECRET
            return "accepted"

    monkeypatch.setattr(main, "telegram_webhook_runtime", FakeRuntime())

    response = TestClient(main.app).post(
        TELEGRAM_DELIVERY_PATH,
        json={"update_id": 3001},
        headers={"X-Telegram-Bot-Api-Secret-Token": TEST_SECRET},
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}


@pytest.mark.parametrize(
    ("runtime_error", "expected_status", "expected_error"),
    [
        (TelegramWebhookUnauthorized("拒绝"), 403, "Telegram Webhook 未授权"),
        (TelegramWebhookQueueFull("已满"), 503, None),
    ],
)
def test_telegram_webhook_http_surface_maps_runtime_failures(
    monkeypatch: pytest.MonkeyPatch,
    runtime_error: Exception,
    expected_status: int,
    expected_error: str | None,
):
    class FakeRuntime:
        enabled = True

        async def enqueue(self, _payload: dict[str, Any], _supplied_secret: str | None) -> str:
            raise runtime_error

    monkeypatch.setattr(main, "telegram_webhook_runtime", FakeRuntime())

    response = TestClient(main.app).post(
        TELEGRAM_DELIVERY_PATH,
        json={"update_id": 3002},
        headers={"X-Telegram-Bot-Api-Secret-Token": TEST_SECRET},
    )

    assert response.status_code == expected_status
    if expected_error is not None:
        assert response.json()["error"] == expected_error
    else:
        assert response.json() == {"status": "queue_full"}
    if expected_status == 503:
        assert response.headers["Retry-After"] == "1"


def test_fastapi_lifespan_starts_and_stops_telegram_runtime(monkeypatch: pytest.MonkeyPatch):
    class FakeRuntime:
        enabled = False

        def __init__(self) -> None:
            self.started = False
            self.stopped = False

        async def start_managed(self) -> None:
            self.started = True

        async def stop(self) -> None:
            self.stopped = True

        def status(self) -> dict[str, int | bool | str]:
            return {"enabled": False, "ready": False}

    runtime = FakeRuntime()
    monkeypatch.setattr(main, "telegram_webhook_runtime", runtime)

    with TestClient(main.app) as client:
        assert client.get("/health").status_code == 200
        assert runtime.started is True

    assert runtime.stopped is True
