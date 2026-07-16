from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from threading import BoundedSemaphore, Event

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

import main  # noqa: E402
from main import app  # noqa: E402
from report_jobs import (  # noqa: E402
    ReportJobExecutionPolicy,
    ReportJobManager,
    ReportJobNonRetryableError,
    ReportJobQueueFull,
    ReportJobWebhookPolicy,
    SQLiteReportJobStore,
)
from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig  # noqa: E402
from webhook_config_store import FernetWebhookConfigCodec  # noqa: E402


def _fernet_key():
    from cryptography.fernet import Fernet

    return Fernet.generate_key().decode("ascii")


def _payload() -> dict:
    return {
        "name": "测试样本",
        "gender": "male",
        "birthDate": "1990-01-01",
        "birthTime": "08:00:00",
        "birthPlace": {
            "name": "北京市",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "timezone": "Asia/Shanghai",
        },
        "options": {
            "useTrueSolarTime": True,
            "daylightSaving": "auto",
            "midnightMode": "early",
            "calendarType": "solar",
            "timeBasis": "local_civil",
        },
    }


@pytest.fixture(autouse=True)
def _reset_rate_limit_windows():
    main._rate_limit_windows.clear()
    yield
    main._rate_limit_windows.clear()


def _wait_for_report_job(client: TestClient, job_id: str, *, timeout_seconds: float = 8.0) -> dict:
    deadline = time.monotonic() + timeout_seconds
    last_body = {}
    while time.monotonic() < deadline:
        response = client.get(f"/api/v1/report/jobs/{job_id}")
        assert response.status_code == 200
        last_body = response.json()
        status = last_body["data"]["status"]
        if status in {"succeeded", "failed", "expired"}:
            return last_body
        time.sleep(0.05)
    raise AssertionError(f"report job did not finish: {last_body}")


def _wait_for_manager_job(manager: ReportJobManager, job_id: str, *, timeout_seconds: float = 4.0):
    deadline = time.monotonic() + timeout_seconds
    last_snapshot = None
    while time.monotonic() < deadline:
        last_snapshot = manager.get(job_id)
        if last_snapshot.status in {"succeeded", "failed", "expired", "cancelled"}:
            return last_snapshot
        time.sleep(0.05)
    raise AssertionError(f"report manager job did not finish: {last_snapshot}")


def _wait_for_manager_event(
    manager: ReportJobManager,
    job_id: str,
    event_type: str,
    *,
    timeout_seconds: float = 4.0,
):
    deadline = time.monotonic() + timeout_seconds
    last_snapshot = None
    while time.monotonic() < deadline:
        last_snapshot = manager.get(job_id)
        if any(event.event_type == event_type for event in last_snapshot.events):
            return last_snapshot
        time.sleep(0.05)
    raise AssertionError(f"report manager event did not appear: {event_type} snapshot={last_snapshot}")


def _audit_events(caplog) -> list[dict]:
    events = []
    for record in caplog.records:
        try:
            payload = json.loads(record.getMessage())
        except json.JSONDecodeError:
            continue
        if payload.get("event") == "audit_event":
            events.append(payload)
    return events


def test_pure_analysis_api_returns_success():
    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["input"]["gender"] == "男"
    assert body["data"]["meta"]["genderCn"] == "乾造(男)"
    assert "jianChu" not in body["data"]


def test_pure_analysis_api_exposes_advanced_bazi_report_field_contract():
    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 200
    data = response.json()["data"]
    benchmark = data["baziBenchmark"]
    regular = benchmark["patternRegistry"]["regularPatternCandidates"]
    special = benchmark["patternRegistry"]["specialPatternCandidates"]
    combine = benchmark["combineTransformMatrix"]
    decision = benchmark["yongShenDecision"]
    fortune_matrix = benchmark["fortuneTriggerMatrix"]
    topics = benchmark["topicProfiles"]
    rule_depth = data["baziRuleDepth"]

    assert regular["schemaVersion"] == 1
    assert regular["riskBoundary"]
    assert regular["uncertaintyPolicy"]
    assert regular["candidates"]
    assert all(candidate["conditions"] and candidate["breaksWhen"] for candidate in regular["candidates"])
    assert all(candidate["status"] == "established" or candidate["uncertainty"] for candidate in regular["candidates"])

    assert special["schemaVersion"] == 1
    assert special["candidates"]
    assert special["riskBoundary"]
    assert all(candidate["status"] in {"candidate", "guarded", "not_supported"} for candidate in special["candidates"])
    assert all(candidate["breaksWhen"] and candidate["lifecycleGate"] for candidate in special["candidates"])

    assert combine["schemaVersion"] == 1
    assert combine["stateCatalog"]
    assert set(combine["stateContracts"]) >= set(combine["stateCatalog"])
    assert combine["riskBoundary"]
    assert all(candidate["state"] in combine["stateCatalog"] for candidate in combine["candidates"])

    assert decision["primaryStrategy"]
    assert decision["riskBoundary"]
    assert {item["strategy"] for item in decision["scoredStrategies"]} == {"调候", "扶抑", "通关", "病药"}
    assert all(item["evidenceFields"] and item["conflictPolicy"] for item in decision["scoredStrategies"])
    assert all(
        item["basis"] and item["scoreBasis"] and item["doesNotApplyWhen"] for item in decision["scoredStrategies"]
    )
    assert all(
        all(score_item["factor"] and score_item["evidenceField"] for score_item in item["scoreBasis"])
        for item in decision["scoredStrategies"]
    )
    assert decision["noAbsoluteConclusion"] is True
    assert len(decision["ranking"]) == len(decision["scoredStrategies"])
    assert decision["selectedCandidates"]
    assert all(item["strategy"] and item["tier"] and item["evidenceFields"] for item in decision["selectedCandidates"])
    assert decision["conflicts"]
    assert all(
        item["type"] and item["explanation"] and item["counterEvidence"] is not None for item in decision["conflicts"]
    )
    assert [item["rank"] for item in decision["ranking"]] == list(range(1, len(decision["ranking"]) + 1))
    assert [item["score"] for item in decision["ranking"]] == sorted(
        [item["score"] for item in decision["ranking"]],
        reverse=True,
    )
    assert [item["step"] for item in decision["decisionTrace"]] == [
        "score_strategies",
        "rank_by_score",
        "select_parallel_candidates",
        "attach_conflicts",
    ]

    assert fortune_matrix["schemaVersion"] == 1
    assert fortune_matrix["layerOrder"] == ["original_chart", "major_stage", "annual_trigger", "monthly_refinement"]
    assert fortune_matrix["riskBoundary"]
    assert {item["type"] for item in fortune_matrix["matrix"]} >= {
        "major_stage",
        "annual_trigger",
        "monthly_refinement",
        "fu_yin",
        "fan_yin",
        "sui_yun_bing_lin",
        "tian_ke_di_chong",
    }
    assert all(item["evidenceFields"] and item["doesNotApplyWhen"] for item in fortune_matrix["matrix"])

    assert {item["topic"] for item in topics} >= {"事业", "财运", "婚姻", "健康", "学业", "迁移", "家庭"}
    for item in topics:
        assert item["lifecycle"] == "beta"
        assert item["basis"]
        assert item["scoreBasis"]
        assert item["scoreTrace"]
        assert item["jointScoreInputs"]
        assert item["productionGate"]["status"] == "blocked"
        assert item["riskPolicy"]["disclaimerRequired"] is True
        assert item["riskPolicy"]["riskLevel"] == "high_topic_boundary"
        assert item["scoreTrace"]["cappedScore"] == item["score"]
        assert item["evidenceFields"]
        assert item["riskBoundary"]

    assert rule_depth["combinationStatements"]
    assert all(item["ruleIds"] and item["riskBoundary"] for item in rule_depth["combinationStatements"])


def test_health_adds_public_service_security_headers():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["x-request-id"]


def test_ready_and_metrics_endpoints_are_available():
    client = TestClient(app)
    ready_response = client.get("/ready")

    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "ready"

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    assert metrics_response.headers["content-type"].startswith("text/plain")
    assert "fatecat_requests_total" in metrics_response.text
    assert "fatecat_request_latency_seconds_bucket" in metrics_response.text
    assert "fatecat_request_latency_seconds_count" in metrics_response.text
    assert "fatecat_request_errors_total" in metrics_response.text
    assert "fatecat_inflight_requests" in metrics_response.text
    assert "fatecat_calculation_slots_in_use" in metrics_response.text
    assert "fatecat_calculation_slots_max" in metrics_response.text
    assert "fatecat_report_job_queue_size" in metrics_response.text
    assert "fatecat_report_job_queue_max" in metrics_response.text
    assert "fatecat_report_jobs" in metrics_response.text
    assert "fatecat_report_jobs_total" in metrics_response.text
    assert "fatecat_report_job_queue_wait_seconds" in metrics_response.text
    assert "fatecat_report_job_execution_duration_seconds" in metrics_response.text
    assert "fatecat_report_job_result_size_bytes" in metrics_response.text
    assert 'fatecat_report_job_store_backend_info{backend="memory"} 1' in metrics_response.text
    assert "fatecat_bot_queue_size" in metrics_response.text
    assert 'fatecat_bot_queue_scope_info{backend="memory",scope="single_process"} 1' in metrics_response.text
    assert "fatecat_bot_queue_max_size" in metrics_response.text
    assert "fatecat_bot_concurrent_requests" in metrics_response.text


def test_report_job_metrics_cover_the_full_terminal_lifecycle_without_payloads():
    started = Event()
    release = Event()

    def fail_task():
        raise RuntimeError("private failure detail")

    def blocking_task():
        started.set()
        release.wait(timeout=2)
        return {"markdown": "discarded private report"}

    manager = ReportJobManager(max_workers=1, queue_size=4, ttl_seconds=120)
    succeeded = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "private name", "birthPlace": "private place"},
        task=lambda: {"markdown": "private report body"},
    )
    assert _wait_for_manager_job(manager, succeeded.job_id).status == "succeeded"

    failed = manager.submit(kind="markdown", report_system="bazi", task=fail_task)
    assert _wait_for_manager_job(manager, failed.job_id).status == "failed"

    cancelled = manager.submit(kind="markdown", report_system="bazi", task=blocking_task)
    assert started.wait(timeout=2)
    assert manager.cancel(cancelled.job_id).status == "cancelled"
    release.set()

    with manager._lock:
        manager._jobs[succeeded.job_id].expires_monotonic = 0.0
    manager.cleanup_expired()

    snapshot = manager.metrics_snapshot()
    assert snapshot["terminalCounts"] == {
        "succeeded": 1,
        "failed": 1,
        "expired": 1,
        "cancelled": 1,
    }
    assert snapshot["histograms"]["queue_wait_seconds"]["count"] == 3
    assert snapshot["histograms"]["execution_duration_seconds"]["count"] == 3
    assert snapshot["histograms"]["result_size_bytes"]["count"] == 1
    assert snapshot["histograms"]["result_size_bytes"]["sum"] > 0

    serialized = json.dumps(snapshot, ensure_ascii=False)
    for private_value in (
        succeeded.job_id,
        "private name",
        "private place",
        "private report body",
        "private failure detail",
    ):
        assert private_value not in serialized


def test_business_error_logs_include_request_id(monkeypatch, caplog):
    def fail_pure_analysis(_payload):
        raise RuntimeError("forced regression error")

    caplog.set_level(logging.ERROR, logger="main")
    monkeypatch.setattr(main, "calculate_pure_analysis", fail_pure_analysis)

    response = TestClient(app).post(
        "/api/v1/bazi/pure-analysis",
        json=_payload(),
        headers={"X-Request-ID": "trace-test-123"},
    )

    assert response.status_code == 500
    assert response.headers["x-request-id"] == "trace-test-123"
    assert '"event":"business_error"' in caplog.text
    assert '"requestId":"trace-test-123"' in caplog.text
    assert '"errorType":"RuntimeError"' in caplog.text


def test_request_body_limit_rejects_oversized_payload(monkeypatch):
    monkeypatch.setattr(main, "MAX_REQUEST_BYTES", 32)

    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 413
    assert response.json()["error"] == "请求体过大"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-request-id"]


def test_request_body_limit_rejects_stream_without_content_length(monkeypatch):
    monkeypatch.setattr(main, "MAX_REQUEST_BYTES", 32)
    sent_messages = []
    body_messages = [
        {
            "type": "http.request",
            "body": b'{"name":"oversized-stream-body","gender":"male"}',
            "more_body": False,
        }
    ]

    async def receive():
        if body_messages:
            return body_messages.pop(0)
        return {"type": "http.disconnect"}

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/api/v1/bazi/pure-analysis",
        "raw_path": b"/api/v1/bazi/pure-analysis",
        "query_string": b"",
        "root_path": "",
        "headers": [(b"host", b"testserver"), (b"content-type", b"application/json")],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }

    asyncio.run(app(scope, receive, send))

    response_start = next(message for message in sent_messages if message["type"] == "http.response.start")
    headers = {name.lower(): value for name, value in response_start["headers"]}
    assert response_start["status"] == 413
    assert headers[b"x-content-type-options"] == b"nosniff"
    assert b"x-request-id" in headers


def test_request_body_limit_accepts_stream_without_content_length(monkeypatch):
    monkeypatch.setattr(main, "MAX_REQUEST_BYTES", 4096)
    sent_messages = []
    body_messages = [
        {
            "type": "http.request",
            "body": json.dumps(_payload()).encode(),
            "more_body": False,
        }
    ]

    async def receive():
        if body_messages:
            return body_messages.pop(0)
        return {"type": "http.disconnect"}

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/api/v1/bazi/pure-analysis",
        "raw_path": b"/api/v1/bazi/pure-analysis",
        "query_string": b"",
        "root_path": "",
        "headers": [(b"host", b"testserver"), (b"content-type", b"application/json")],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }

    asyncio.run(app(scope, receive, send))

    response_start = next(message for message in sent_messages if message["type"] == "http.response.start")
    response_body = b"".join(
        message.get("body", b"") for message in sent_messages if message["type"] == "http.response.body"
    )
    assert response_start["status"] == 200
    assert json.loads(response_body)["success"] is True


def test_rate_limit_rejects_excess_requests(monkeypatch):
    monkeypatch.setattr(main, "RATE_LIMIT_PER_MINUTE", 1)
    main._rate_limit_windows.clear()

    client = TestClient(app)
    first_response = client.get("/api/v1/report/systems")
    second_response = client.get("/api/v1/report/systems")

    main._rate_limit_windows.clear()
    assert first_response.status_code == 200
    assert second_response.status_code == 429
    assert second_response.json()["error"] == "请求过于频繁"
    assert second_response.headers["retry-after"]
    assert second_response.headers["x-content-type-options"] == "nosniff"
    assert second_response.headers["x-frame-options"] == "DENY"
    assert second_response.headers["x-request-id"]


def test_calculation_backpressure_rejects_when_slots_are_exhausted(monkeypatch):
    semaphore = BoundedSemaphore(1)
    assert semaphore.acquire(blocking=False)
    monkeypatch.setattr(main, "MAX_INFLIGHT_CALCULATIONS", 1)
    monkeypatch.setattr(main, "_calculation_slots", semaphore)
    monkeypatch.setattr(main, "_calculation_slots_in_use", 1)

    try:
        response = TestClient(app).post("/api/v1/bazi/simple", json=_payload())
    finally:
        semaphore.release()
        monkeypatch.setattr(main, "_calculation_slots_in_use", 0)

    assert response.status_code == 503
    assert response.json()["success"] is False
    assert response.json()["error"] == "服务繁忙，请稍后再试"


def test_simple_api_does_not_return_retired_jianchu_field():
    response = TestClient(app).post("/api/v1/bazi/simple", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "jianChu" not in body["data"]


def test_calculate_api_returns_success_with_record_id(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 42

    monkeypatch.setattr("main.db.save_record", fake_save_record)
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=_payload(),
        headers={"X-FateCat-API-Key": "test-token"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["recordId"] == 42
    assert saved["gender"] == "male"
    assert saved["birth_place"] == "北京市"


def test_calculate_record_keeps_raw_and_normalized_options(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 44

    payload = _payload()
    payload["options"]["useTrueSolarTime"] = False
    payload["options"]["reportSystem"] = "ziwei"

    monkeypatch.setattr("main.db.save_record", fake_save_record)
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=payload,
        headers={"X-FateCat-API-Key": "test-token"},
    )

    assert response.status_code == 200
    assert saved["calendar_type"] == "solar"
    assert saved["dst"] == 0
    assert saved["early_zi"] == 1
    assert saved["true_solar"] == 0
    assert saved["biz_data"]["input"]["options"]["useTrueSolarTime"] is False
    assert saved["biz_data"]["input"]["options"]["reportSystem"] == "ziwei"
    assert saved["biz_data"]["normalizedOptions"] == {
        "calendarType": "solar",
        "daylightSaving": "auto",
        "midnightMode": "early",
        "useTrueSolarTime": False,
        "reportSystem": "bazi",
        "timeBasis": "local_civil",
        "foldChoice": None,
    }


def test_calculate_api_rejects_unsupported_business_options():
    payload = _payload()
    payload["options"]["calendarType"] = "lunar"

    lunar_response = TestClient(app).post("/api/v1/bazi/calculate", json=payload)

    assert lunar_response.status_code == 422
    assert "calendarType=lunar" in lunar_response.text

    payload = _payload()
    payload["options"]["daylightSaving"] = "on"
    dst_response = TestClient(app).post("/api/v1/bazi/calculate", json=payload)

    assert dst_response.status_code == 422
    assert "daylightSaving" in dst_response.text

    payload = _payload()
    payload["options"]["midnightMode"] = "late"
    midnight_response = TestClient(app).post("/api/v1/bazi/calculate", json=payload)

    assert midnight_response.status_code == 422
    assert "midnightMode=late" in midnight_response.text


def test_location_api_exposes_stable_ids_timezone_precision_and_catalog_status():
    client = TestClient(app)

    search_response = client.get("/api/v1/locations", params={"q": "纽约", "mode": "overseas"})
    assert search_response.status_code == 200
    body = search_response.json()
    assert body["data"]["locations"][0]["locationId"] == "geonames:5128581"
    assert body["data"]["locations"][0]["timezone"] == "America/New_York"
    assert body["data"]["locations"][0]["coordinatePrecision"] == "locality_centroid"
    assert body["meta"]["catalog"]["recordCount"] > 160000

    detail_response = client.get("/api/v1/locations/geonames:5128581")
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["coordinateSystem"] == "WGS84"

    fuzzy_response = client.get("/api/v1/locations", params={"q": "西安长安", "mode": "domestic", "limit": 8})
    assert fuzzy_response.status_code == 200
    assert fuzzy_response.json()["data"]["locations"][0]["locationId"] == "cn:610116"

    single_character_response = client.get("/api/v1/locations", params={"q": "京", "mode": "domestic", "limit": 8})
    assert single_character_response.status_code == 200
    assert single_character_response.json()["data"]["count"] > 0


def test_bazi_api_normalizes_overseas_local_civil_time_and_rejects_timezone_mismatch():
    payload = _payload()
    payload["birthPlace"] = {
        "name": "纽约",
        "longitude": -74.00597,
        "latitude": 40.71427,
        "timezone": "America/New_York",
        "locationId": "geonames:5128581",
        "coordinateSystem": "WGS84",
        "coordinatePrecision": "locality_centroid",
    }
    payload["options"]["timeBasis"] = "local_civil"

    response = TestClient(app).post("/api/v1/bazi/calculate", json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["timeInfo"]["inputTime"] == "1990-01-01T08:00:00-05:00"

    payload["birthPlace"]["timezone"] = "Asia/Shanghai"
    mismatch = TestClient(app).post("/api/v1/bazi/calculate", json=payload)
    assert mismatch.status_code == 422
    assert "timezone" in mismatch.text

    payload["birthPlace"]["timezone"] = "America/New_York"
    payload["birthPlace"]["longitude"] = -73.0
    coordinate_mismatch = TestClient(app).post("/api/v1/bazi/calculate", json=payload)
    assert coordinate_mismatch.status_code == 422
    assert "WGS84 坐标不一致" in coordinate_mismatch.text


def test_simple_api_echoes_false_true_solar_option_consistently():
    payload = _payload()
    payload["options"]["useTrueSolarTime"] = False

    response = TestClient(app).post("/api/v1/bazi/simple", json=payload)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["input"]["options"]["useTrueSolarTime"] is False
    assert data["inputTrace"]["useTrueSolarTime"] is False


def test_user_token_can_write_only_own_record(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 43

    monkeypatch.setattr("main.db.save_record", fake_save_record)
    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv("FATE_API_USER_TOKENS", "u1:user-token")

    own_response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=_payload(),
        headers={"X-FateCat-API-Key": "user-token"},
    )
    other_response = TestClient(app).post(
        "/api/v1/bazi/calculate?user_id=u2",
        json=_payload(),
        headers={"X-FateCat-API-Key": "user-token"},
    )

    assert own_response.status_code == 200
    assert own_response.json()["meta"]["recordId"] == 43
    assert saved["user_id"] == "u1"
    assert other_response.status_code == 403
    assert other_response.json()["error"] == "无权访问该记录"


def test_calculate_api_rejects_record_write_without_token(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).post("/api/v1/bazi/calculate?user_id=u1", json=_payload())

    assert response.status_code == 403
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "未授权"


def test_record_read_requires_api_token(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "test-token")

    response = TestClient(app).get("/api/v1/records/1")

    assert response.status_code == 403
    assert response.json()["error"] == "未授权"


def test_record_interfaces_can_be_disabled(monkeypatch):
    monkeypatch.setenv("FATE_RECORDS_ENABLED", "false")
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")

    response = TestClient(app).get("/api/v1/records/1", headers={"X-FateCat-API-Key": "admin-token"})

    assert response.status_code == 403
    assert response.json()["error"] == "记录接口未启用"


def test_user_token_cannot_read_other_user_record(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv("FATE_API_USER_TOKENS", "u1:user-token")
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u2",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )

    response = TestClient(app).get("/api/v1/records/1", headers={"X-FateCat-API-Key": "user-token"})

    assert response.status_code == 403
    assert response.json()["error"] == "无权访问该记录"


def test_scoped_user_token_can_read_and_list_but_cannot_write_record(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv("FATE_API_USER_TOKENS", "u1:read-token:record.read|record.list")
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u1",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )
    monkeypatch.setattr("main.db.get_user_records", lambda _user_id, _biz_type, _limit: [])
    client = TestClient(app)

    read_response = client.get("/api/v1/records/1", headers={"X-FateCat-API-Key": "read-token"})
    list_response = client.get("/api/v1/user/u1/records", headers={"X-FateCat-API-Key": "read-token"})
    write_response = client.post(
        "/api/v1/bazi/calculate?user_id=u1",
        json=_payload(),
        headers={"X-FateCat-API-Key": "read-token"},
    )

    assert read_response.status_code == 200
    assert list_response.status_code == 200
    assert write_response.status_code == 403
    assert write_response.json()["error"] == "权限不足"


def test_scoped_user_token_requires_delete_scope(monkeypatch):
    deleted = []

    monkeypatch.setattr(main, "API_TOKEN", "")
    monkeypatch.setenv(
        "FATE_API_USER_TOKENS",
        "u1:read-token:record.read,u1:delete-token:record.delete",
    )
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u1",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )

    def fake_delete_record(record_id):
        deleted.append(record_id)
        return True

    monkeypatch.setattr("main.db.delete_record", fake_delete_record)
    client = TestClient(app)

    read_only_response = client.delete("/api/v1/records/1", headers={"X-FateCat-API-Key": "read-token"})
    delete_response = client.delete("/api/v1/records/1", headers={"X-FateCat-API-Key": "delete-token"})

    assert read_only_response.status_code == 403
    assert read_only_response.json()["error"] == "权限不足"
    assert delete_response.status_code == 200
    assert deleted == [1]


def test_admin_token_can_read_any_record(monkeypatch, caplog):
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")
    monkeypatch.setattr(
        "main.db.get_record",
        lambda _record_id: {
            "id": 1,
            "userId": "u2",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        },
    )
    caplog.set_level(logging.INFO, logger="main")

    response = TestClient(app).get("/api/v1/records/1", headers={"Authorization": "Bearer admin-token"})

    assert response.status_code == 200
    assert response.json()["data"]["userId"] == "u2"
    audit = next(item for item in _audit_events(caplog) if item["action"] == "record.read")
    audit_text = json.dumps(audit, ensure_ascii=False)
    assert audit["actorRole"] == "admin"
    assert audit["scopeCount"] == len(main.RECORD_SCOPES)
    assert audit["targetType"] == "UserRecord"
    assert audit["targetIdHash"]
    assert audit["metadata"]["bizType"] == "bazi"
    assert audit["metadata"]["recordRetentionDays"] == main.RECORD_RETENTION_DAYS
    assert "admin-token" not in audit_text
    assert "u2" not in audit_text


def test_user_records_limit_is_bounded(monkeypatch):
    monkeypatch.setattr(main, "API_TOKEN", "admin-token")

    response = TestClient(app).get(
        "/api/v1/user/u1/records?limit=-1",
        headers={"X-FateCat-API-Key": "admin-token"},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "请求参数无效"


def test_bazi_apis_reject_invalid_birth_datetime_as_validation_error():
    payload = _payload()
    payload["birthDate"] = "bad-date"
    client = TestClient(app, raise_server_exceptions=False)

    for path in [
        "/api/v1/bazi/simple",
        "/api/v1/bazi/pure-analysis",
        "/api/v1/bazi/calculate",
        "/api/v1/report/markdown",
    ]:
        response = client.post(path, json=payload)
        body = response.json()

        assert response.status_code == 422, path
        assert body["success"] is False
        assert body["error"] == "请求参数无效"


def test_calculate_api_internal_failure_returns_500_not_success_false_200(monkeypatch):
    def fail_calculation(*_args, **_kwargs):
        raise RuntimeError("forced calculation failure")

    monkeypatch.setattr(main, "_calculate_bazi_raw", fail_calculation)

    response = TestClient(app, raise_server_exceptions=False).post("/api/v1/bazi/calculate", json=_payload())
    body = response.json()

    assert response.status_code == 500
    assert body["success"] is False
    assert body["error"] == "服务器内部错误"


def test_system_optimization_report_does_not_advertise_unimplemented_routes_as_enabled():
    from system_optimization import get_complete_system_optimization

    response = TestClient(app).get("/graphql")
    assert response.status_code == 404

    report = get_complete_system_optimization()
    assert report["systemInfo"]["readyForProduction"] is False
    assert report["systemInfo"]["productionReadinessSource"] == "scripts/production-readiness.sh"
    assert report["documentationAndTesting"]["syntheticCoverageClaims"] is False
    assert "graphqlSupport" not in report["apiEnhancements"]
    assert "/graphql" in report["apiEnhancements"]["plannedNotAdvertisedAsEnabled"]


def test_markdown_report_api_gate_selects_ziwei_without_bazi_blocks():
    payload = _payload()
    payload["options"]["reportSystem"] = "ziwei"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 200
    body = response.json()
    markdown = body["data"]["markdown"]
    assert body["data"]["reportSystem"] == "ziwei"
    assert body["data"]["policyGate"]["status"] == "pass"
    assert body["data"]["policyGate"]["scope"] == "markdown-report:ziwei"
    assert body["data"]["policyGate"]["checkedFields"] == ["report.markdown"]
    assert body["data"]["snapshotGate"]["status"] == "pass"
    assert body["data"]["snapshotGate"]["reportSystem"] == "ziwei"
    assert "### 大限/流年联动" in body["data"]["snapshotGate"]["requiredHeadings"]
    assert "# 紫微斗数报告：测试样本" in markdown
    assert "## 紫微斗数" in markdown
    assert "### 入盘依据" in markdown
    assert "### 命宫与身宫" in markdown
    assert "## 紫微结构解读（依据版）" in markdown
    assert "### 主星组合" in markdown
    assert "### 三方四正" in markdown
    assert "### 四化落宫" in markdown
    assert "### 大限/流年联动" in markdown
    assert "## 紫微基础" not in markdown
    assert "八字排盘详情" not in markdown


def test_markdown_report_job_gate_api_returns_status_then_result():
    client = TestClient(app)
    response = client.post("/api/v1/report/jobs", json=_payload())

    assert response.status_code == 202
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] in {"queued", "running"}
    assert body["data"]["resourceType"] == "CalculationJob"
    assert body["data"]["apiVersion"] == "fatecat.tradecatlabs/v1"
    assert body["data"]["jobId"]
    assert body["data"]["id"] == body["data"]["jobId"]
    assert body["data"]["statusUrl"] == f"/api/v1/report/jobs/{body['data']['jobId']}"
    assert body["data"]["cancelUrl"] == f"/api/v1/report/jobs/{body['data']['jobId']}/cancel"
    assert body["data"]["links"]["self"] == f"/api/v1/report/jobs/{body['data']['jobId']}"
    assert body["data"]["links"]["cancel"] == f"/api/v1/report/jobs/{body['data']['jobId']}/cancel"

    final_body = _wait_for_report_job(client, body["data"]["jobId"])
    assert final_body["data"]["status"] == "succeeded"
    assert final_body["data"]["attempts"] == 1
    assert final_body["data"]["maxAttempts"] == 1
    assert final_body["data"]["attemptTimeoutSeconds"] is None
    assert final_body["data"]["retryBackoffSeconds"] == 0
    event_types = [item["eventType"] for item in final_body["data"]["events"]]
    assert event_types == ["job.queued", "job.running", "job.succeeded"]
    event_text = json.dumps(final_body["data"]["events"], ensure_ascii=False)
    assert "测试样本" not in event_text
    assert "北京" not in event_text
    assert final_body["data"]["result"]["reportSystem"] == "bazi"
    assert final_body["data"]["result"]["policyGate"]["status"] == "pass"
    assert final_body["data"]["result"]["snapshotGate"]["status"] == "pass"
    assert final_body["data"]["result"]["snapshotGate"]["reportSystem"] == "bazi"
    assert "# 命理排盘报告：测试样本" in final_body["data"]["result"]["markdown"]


def test_report_job_webhook_dispatcher_sends_signed_terminal_event():
    captured: dict[str, object] = {}

    def capture_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: int) -> int:
        captured["url"] = url
        captured["body"] = body
        captured["headers"] = dict(headers)
        captured["timeoutSeconds"] = timeout_seconds
        return 204

    dispatcher = HttpWebhookDispatcher(timeout_seconds=3, transport=capture_transport)
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        webhook_dispatcher=dispatcher.deliver,
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="test-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )

    final_snapshot = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_succeeded")
    assert final_snapshot.status == "succeeded"
    assert captured["url"] == "https://callback.example/webhook"
    assert captured["timeoutSeconds"] == 3
    body_text = captured["body"].decode("utf-8")  # type: ignore[union-attr]
    headers = captured["headers"]  # type: ignore[assignment]
    assert '"eventType":"report_job.terminal"' in body_text
    assert f'"jobId":"{created.job_id}"' in body_text
    assert '"status":"succeeded"' in body_text
    assert '"markdown":' not in body_text
    assert "# 命理排盘报告" not in body_text
    assert "测试样本" not in body_text
    assert "北京" not in body_text
    assert headers["X-FateCat-Webhook-Event"] == "report_job.terminal"
    assert str(headers["X-FateCat-Webhook-Signature"]).startswith("sha256=")
    assert "test-secret" not in body_text
    assert "test-secret" not in json.dumps(headers, ensure_ascii=False)


def test_report_job_webhook_dispatches_cancelled_terminal_event():
    started = Event()
    release = Event()
    statuses: list[str] = []

    def blocking_task():
        started.set()
        release.wait(timeout=2)
        return {"reportSystem": "bazi", "markdown": "discarded"}

    def capture_dispatch(snapshot, _config):
        statuses.append(snapshot.status)

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        webhook_dispatcher=capture_dispatch,
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        task=blocking_task,
        webhook_config=WebhookConfig(url="https://callback.example/webhook"),
    )
    started.wait(timeout=2)
    cancelled = manager.cancel(created.job_id)
    release.set()

    assert cancelled.status == "cancelled"
    assert statuses == ["cancelled"]


def test_report_job_webhook_retry_policy_retries_failed_callback():
    attempts: list[int] = []

    def flaky_dispatch(_snapshot, _config):
        attempts.append(len(attempts) + 1)
        if len(attempts) == 1:
            raise RuntimeError("callback failed with private details")
        return type("WebhookResult", (), {"status_code": 204, "event_type": "report_job.terminal"})()

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        webhook_dispatcher=flaky_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=2),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="retry-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )

    final_snapshot = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_succeeded")

    assert attempts == [1, 2]
    event_types = [event.event_type for event in final_snapshot.events]
    assert event_types == [
        "job.queued",
        "job.running",
        "job.succeeded",
        "webhook.delivery_attempt_failed",
        "webhook.delivery_retry_scheduled",
        "webhook.delivery_succeeded",
    ]
    attempt_failed = next(
        event for event in final_snapshot.events if event.event_type == "webhook.delivery_attempt_failed"
    )
    retry_scheduled = next(
        event for event in final_snapshot.events if event.event_type == "webhook.delivery_retry_scheduled"
    )
    succeeded = next(event for event in final_snapshot.events if event.event_type == "webhook.delivery_succeeded")
    assert attempt_failed.metadata["attempt"] == 1
    assert attempt_failed.metadata["maxAttempts"] == 2
    assert attempt_failed.metadata["errorType"] == "RuntimeError"
    assert attempt_failed.metadata["willRetry"] is True
    assert retry_scheduled.metadata["nextAttempt"] == 2
    assert succeeded.metadata["attempt"] == 2
    assert succeeded.metadata["statusCode"] == 204
    events_text = json.dumps([event.metadata for event in final_snapshot.events], ensure_ascii=False)
    assert "callback.example" not in events_text
    assert "retry-secret" not in events_text
    assert "测试样本" not in events_text
    assert "北京" not in events_text
    assert "private details" not in events_text


def test_report_job_webhook_retry_policy_records_final_failure_without_sensitive_metadata():
    attempts: list[int] = []

    def failing_dispatch(_snapshot, _config):
        attempts.append(len(attempts) + 1)
        raise RuntimeError("callback.example retry-secret 测试样本 北京")

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=2),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="retry-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )

    final_snapshot = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_failed")

    assert final_snapshot.status == "succeeded"
    assert attempts == [1, 2]
    event_types = [event.event_type for event in final_snapshot.events]
    assert event_types == [
        "job.queued",
        "job.running",
        "job.succeeded",
        "webhook.delivery_attempt_failed",
        "webhook.delivery_retry_scheduled",
        "webhook.delivery_attempt_failed",
        "webhook.delivery_failed",
    ]
    final_failure = final_snapshot.events[-1]
    assert final_failure.metadata["attempt"] == 2
    assert final_failure.metadata["maxAttempts"] == 2
    assert final_failure.metadata["errorType"] == "RuntimeError"
    assert "willRetry" not in final_failure.metadata
    events_text = json.dumps([event.metadata for event in final_snapshot.events], ensure_ascii=False)
    assert "callback.example" not in events_text
    assert "retry-secret" not in events_text
    assert "测试样本" not in events_text
    assert "北京" not in events_text


def test_report_job_webhook_default_policy_attempts_once_without_retry():
    attempts: list[int] = []

    def failing_dispatch(_snapshot, _config):
        attempts.append(len(attempts) + 1)
        raise RuntimeError("first attempt only")

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        webhook_dispatcher=failing_dispatch,
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        webhook_config=WebhookConfig(url="https://callback.example/webhook"),
        task=lambda: {"reportSystem": "bazi", "markdown": "done"},
    )

    final_snapshot = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_failed")

    assert attempts == [1]
    event_types = [event.event_type for event in final_snapshot.events]
    assert "webhook.delivery_retry_scheduled" not in event_types
    assert final_snapshot.events[-1].metadata["attempt"] == 1
    assert final_snapshot.events[-1].metadata["maxAttempts"] == 1


def test_sqlite_webhook_outbox_persists_success_and_failure_records(tmp_path):
    success_db = tmp_path / "report-jobs-success.sqlite"

    def success_dispatch(_snapshot, _config):
        return type("WebhookResult", (), {"status_code": 204, "event_type": "report_job.terminal"})()

    success_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(success_db),
        webhook_dispatcher=success_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=2),
    )
    success_created = success_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="sqlite-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    success_snapshot = _wait_for_manager_event(success_manager, success_created.job_id, "webhook.delivery_succeeded")

    assert len(success_snapshot.callback_outbox) == 1
    success_outbox = success_snapshot.callback_outbox[0]
    assert success_outbox.status == "succeeded"
    assert success_outbox.event_type == "report_job.terminal"
    assert success_outbox.job_status == "succeeded"
    assert success_outbox.attempts == 1
    assert success_outbox.max_attempts == 2
    assert success_outbox.signature_mode == "hmac-sha256"
    assert success_outbox.target_host_hash
    assert success_outbox.result_status_code == 204

    rebuilt_success = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(success_db),
    )
    loaded_success = rebuilt_success.get(success_created.job_id)
    assert loaded_success.callback_outbox[0].status == "succeeded"
    success_payload = main._report_job_payload(loaded_success, include_result=False)
    assert success_payload["webhookOutbox"][0]["status"] == "succeeded"
    success_text = json.dumps(success_payload["webhookOutbox"], ensure_ascii=False)
    assert "callback.example" not in success_text
    assert "sqlite-secret" not in success_text
    assert "测试样本" not in success_text
    assert "北京" not in success_text
    assert "# 命理排盘报告" not in success_text

    failure_db = tmp_path / "report-jobs-failure.sqlite"

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("callback.example sqlite-secret 测试样本 北京")

    failure_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(failure_db),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=2),
    )
    failure_created = failure_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="sqlite-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    failure_snapshot = _wait_for_manager_event(failure_manager, failure_created.job_id, "webhook.delivery_failed")

    assert len(failure_snapshot.callback_outbox) == 1
    failure_outbox = failure_snapshot.callback_outbox[0]
    assert failure_outbox.status == "failed"
    assert failure_outbox.event_type == "report_job.terminal"
    assert failure_outbox.job_status == "succeeded"
    assert failure_outbox.attempts == 2
    assert failure_outbox.max_attempts == 2
    assert failure_outbox.signature_mode == "hmac-sha256"
    assert failure_outbox.target_host_hash
    assert failure_outbox.last_error_type == "RuntimeError"
    assert failure_outbox.result_status_code is None

    rebuilt_failure = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(failure_db),
    )
    loaded_failure = rebuilt_failure.get(failure_created.job_id)
    assert loaded_failure.callback_outbox[0].status == "failed"
    failure_payload = main._report_job_payload(loaded_failure, include_result=False)
    assert failure_payload["webhookOutbox"][0]["status"] == "failed"
    failure_text = json.dumps(failure_payload["webhookOutbox"], ensure_ascii=False)
    assert "callback.example" not in failure_text
    assert "sqlite-secret" not in failure_text
    assert "测试样本" not in failure_text
    assert "北京" not in failure_text


def test_sqlite_webhook_outbox_redelivers_failed_record_after_manager_rebuild(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-redelivery.sqlite"
    first_attempts: list[int] = []

    def failing_dispatch(_snapshot, _config):
        first_attempts.append(len(first_attempts) + 1)
        raise RuntimeError("callback.example redelivery-secret 测试样本 北京")

    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="redelivery-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    failed_snapshot = _wait_for_manager_event(first_manager, created.job_id, "webhook.delivery_failed")

    assert first_attempts == [1]
    assert failed_snapshot.callback_outbox[0].status == "failed"

    redelivery_attempts: list[str] = []

    def success_dispatch(snapshot, config):
        redelivery_attempts.append(f"{snapshot.job_id}:{getattr(config, 'signature_mode', 'none')}")
        return type("WebhookResult", (), {"status_code": 204, "event_type": "report_job.terminal"})()

    def resolver(record, snapshot):
        assert record.outbox_id == failed_snapshot.callback_outbox[0].outbox_id
        assert snapshot.job_id == created.job_id
        return WebhookConfig(url="https://callback.example/webhook", secret="redelivery-secret")

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=success_dispatch,
        delivery_resolver=resolver,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    recovered = _wait_for_manager_event(rebuilt, created.job_id, "webhook.redelivery_succeeded")
    event_types = [event.event_type for event in recovered.events]

    assert redelivery_attempts == [f"{created.job_id}:hmac-sha256"]
    assert recovered.callback_outbox[0].status == "succeeded"
    assert recovered.callback_outbox[0].attempts == 1
    assert recovered.callback_outbox[0].result_status_code == 204
    assert "webhook.redelivery_scheduled" in event_types
    assert "webhook.delivery_succeeded" in event_types
    assert event_types[-1] == "webhook.redelivery_succeeded"
    payload = main._report_job_payload(recovered, include_result=False)
    serialized = json.dumps(
        {
            "events": [event.metadata for event in recovered.events],
            "outbox": payload["webhookOutbox"],
        },
        ensure_ascii=False,
    )
    assert "callback.example" not in serialized
    assert "redelivery-secret" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized
    assert "# 命理排盘报告" not in serialized


def test_sqlite_webhook_outbox_redelivery_skips_when_resolver_returns_none(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-redelivery-missing-config.sqlite"

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("redelivery config unavailable")

    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="missing-config-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "done"},
    )
    failed_snapshot = _wait_for_manager_event(first_manager, created.job_id, "webhook.delivery_failed")
    assert failed_snapshot.callback_outbox[0].status == "failed"

    redelivery_called = False

    def should_not_dispatch(_snapshot, _config):
        nonlocal redelivery_called
        redelivery_called = True
        raise AssertionError("resolver returned None, dispatcher must not be called")

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=should_not_dispatch,
        delivery_resolver=lambda _record, _snapshot: None,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    skipped = _wait_for_manager_event(rebuilt, created.job_id, "webhook.redelivery_skipped")
    event_types = [event.event_type for event in skipped.events]

    assert redelivery_called is False
    assert skipped.callback_outbox[0].status == "failed"
    assert "webhook.redelivery_skipped" in event_types
    assert "webhook.redelivery_succeeded" not in event_types
    assert "webhook.redelivery_failed" not in event_types
    serialized = json.dumps([event.metadata for event in skipped.events], ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "missing-config-secret" not in serialized


def test_sqlite_webhook_outbox_redelivery_records_resolver_error(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-redelivery-resolver-error.sqlite"

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("seed failure")

    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="resolver-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "done"},
    )
    failed_snapshot = _wait_for_manager_event(first_manager, created.job_id, "webhook.delivery_failed")
    assert failed_snapshot.callback_outbox[0].status == "failed"

    redelivery_called = False

    def should_not_dispatch(_snapshot, _config):
        nonlocal redelivery_called
        redelivery_called = True
        raise AssertionError("resolver failed, dispatcher must not be called")

    def resolver_raises(_record, _snapshot):
        raise RuntimeError("callback.example resolver-secret 测试样本 北京")

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=should_not_dispatch,
        delivery_resolver=resolver_raises,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    redelivery_failed = _wait_for_manager_event(rebuilt, created.job_id, "webhook.redelivery_failed")

    assert redelivery_called is False
    assert redelivery_failed.callback_outbox[0].status == "failed"
    failure_events = [event for event in redelivery_failed.events if event.event_type == "webhook.redelivery_failed"]
    assert failure_events[-1].metadata["reason"] == "config_resolution_failed"
    assert failure_events[-1].metadata["errorType"] == "RuntimeError"
    serialized = json.dumps([event.metadata for event in redelivery_failed.events], ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "resolver-secret" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized


def test_sqlite_webhook_config_vault_redelivers_without_external_resolver_and_deletes_on_success(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-config-vault.sqlite"
    codec = FernetWebhookConfigCodec(keys={"v1": _fernet_key()}, active_key_id="v1")

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("callback.example vault-secret 测试样本 北京")

    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path, webhook_config_codec=codec),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="vault-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    failed_snapshot = _wait_for_manager_event(first_manager, created.job_id, "webhook.delivery_failed")

    assert failed_snapshot.callback_outbox[0].status == "failed"
    assert SQLiteReportJobStore(db_path, webhook_config_codec=codec).count_webhook_delivery_configs() == 1
    raw_db_text = db_path.read_bytes().decode("latin1", errors="ignore")
    assert "callback.example" not in raw_db_text
    assert "vault-secret" not in raw_db_text
    assert "测试样本" not in raw_db_text
    assert "北京" not in raw_db_text
    assert "# 命理排盘报告" not in raw_db_text

    redelivery_attempts: list[str] = []

    def success_dispatch(snapshot, config):
        redelivery_attempts.append(f"{snapshot.job_id}:{config.signature_mode}")
        assert config.url == "https://callback.example/webhook"
        assert config.secret == "vault-secret"
        return type("WebhookResult", (), {"status_code": 204, "event_type": "report_job.terminal"})()

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path, webhook_config_codec=codec),
        webhook_dispatcher=success_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    redelivered = _wait_for_manager_event(rebuilt, created.job_id, "webhook.redelivery_succeeded")

    assert redelivery_attempts == [f"{created.job_id}:hmac-sha256"]
    assert redelivered.callback_outbox[0].status == "succeeded"
    assert SQLiteReportJobStore(db_path, webhook_config_codec=codec).count_webhook_delivery_configs() == 0
    payload = main._report_job_payload(redelivered, include_result=False)
    serialized = json.dumps(
        {
            "events": [event.metadata for event in redelivered.events],
            "outbox": payload["webhookOutbox"],
        },
        ensure_ascii=False,
    )
    assert "callback.example" not in serialized
    assert "vault-secret" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized


def test_sqlite_webhook_config_vault_rotates_key_before_redelivery(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-config-vault-rotation.sqlite"
    old_key = _fernet_key()
    new_key = _fernet_key()
    old_codec = FernetWebhookConfigCodec(keys={"old": old_key}, active_key_id="old")

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("rotation failure")

    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path, webhook_config_codec=old_codec),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="rotation-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "done"},
    )
    _wait_for_manager_event(first_manager, created.job_id, "webhook.delivery_failed")

    def current_key_id() -> str:
        with SQLiteReportJobStore(db_path)._connect() as conn:
            row = conn.execute("SELECT key_id FROM report_job_webhook_delivery_config").fetchone()
        return str(row["key_id"])

    assert current_key_id() == "old"
    new_codec = FernetWebhookConfigCodec(keys={"old": old_key, "new": new_key}, active_key_id="new")
    rotated_store = SQLiteReportJobStore(db_path, webhook_config_codec=new_codec)
    assert rotated_store.rotate_webhook_delivery_configs() == 1
    assert current_key_id() == "new"
    assert rotated_store.rotate_webhook_delivery_configs() == 0
    assert current_key_id() == "new"

    redelivery_attempts = 0

    def success_dispatch(_snapshot, config):
        nonlocal redelivery_attempts
        redelivery_attempts += 1
        assert config.secret == "rotation-secret"
        return type("WebhookResult", (), {"status_code": 204, "event_type": "report_job.terminal"})()

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path, webhook_config_codec=new_codec),
        webhook_dispatcher=success_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    redelivered = _wait_for_manager_event(rebuilt, created.job_id, "webhook.redelivery_succeeded")

    assert redelivery_attempts == 1
    assert redelivered.callback_outbox[0].status == "succeeded"
    assert SQLiteReportJobStore(db_path, webhook_config_codec=new_codec).count_webhook_delivery_configs() == 0


def test_sqlite_webhook_outbox_claim_release_lease_prevents_double_claim(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-outbox-lease.sqlite"

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("lease seed failure")

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="lease-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "done"},
    )
    failed = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_failed")
    record = failed.callback_outbox[0]
    store = SQLiteReportJobStore(db_path)

    claimed_by_a = store.claim_webhook_outbox_record(record, lease_owner="worker-a", lease_seconds=30)
    assert claimed_by_a is not None
    assert claimed_by_a.outbox_id == record.outbox_id
    assert store.load_redeliverable_webhook_outbox_records() == []
    assert store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30) is None

    store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-b")
    assert store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30) is None
    store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-a")

    claimed_by_b = store.claim_webhook_outbox_record(record, lease_owner="worker-b", lease_seconds=30)
    assert claimed_by_b is not None
    assert claimed_by_b.outbox_id == record.outbox_id
    store.release_webhook_outbox_record(record.outbox_id, lease_owner="worker-b")
    assert [item.outbox_id for item in store.load_redeliverable_webhook_outbox_records()] == [record.outbox_id]


def test_sqlite_webhook_outbox_lease_payload_stays_internal(tmp_path):
    db_path = tmp_path / "report-jobs-webhook-outbox-lease-payload.sqlite"

    def failing_dispatch(_snapshot, _config):
        raise RuntimeError("callback.example lease-secret 测试样本 北京")

    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        webhook_dispatcher=failing_dispatch,
        callback_policy=ReportJobWebhookPolicy(max_attempts=1),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本", "birthPlace": "北京"},
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="lease-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    failed = _wait_for_manager_event(manager, created.job_id, "webhook.delivery_failed")
    record = failed.callback_outbox[0]
    store = SQLiteReportJobStore(db_path)
    assert store.claim_webhook_outbox_record(record, lease_owner="worker-a", lease_seconds=30) is not None

    loaded = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    ).get(created.job_id)
    payload = main._report_job_payload(loaded, include_result=False)
    serialized = json.dumps(payload, ensure_ascii=False)

    assert "leaseOwner" not in serialized
    assert "leaseAcquiredAt" not in serialized
    assert "leaseExpiresAt" not in serialized
    assert "worker-a" not in serialized
    assert "callback.example" not in serialized
    assert "lease-secret" not in serialized
    assert "测试样本" not in json.dumps(payload["webhookOutbox"], ensure_ascii=False)


def test_sqlite_replayable_report_job_requeues_after_manager_rebuild(tmp_path):
    db_path = tmp_path / "report-jobs-replayable.sqlite"
    first_manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    original_blocker = Event()
    created = first_manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"case": "replayable"},
        task=lambda: original_blocker.wait(),
        task_payload={"fixture": "replayable"},
        idempotency_key="replayable-manager-rebuild",
    )
    deadline = time.monotonic() + 4.0
    while first_manager.get(created.job_id).status != "running" and time.monotonic() < deadline:
        time.sleep(0.01)

    def factory(payload):
        return lambda: {"reportSystem": "bazi", "markdown": f"# recovered {payload['fixture']}"}

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        task_factories={"markdown": factory},
    )
    recovered = _wait_for_manager_job(rebuilt, created.job_id)
    event_types = [event.event_type for event in recovered.events]

    assert recovered.status == "succeeded"
    assert recovered.attempts == 1
    assert recovered.result["markdown"] == "# recovered replayable"
    assert "job.recovered_requeued" in event_types
    assert "job.recovered_failed" not in event_types
    duplicate = rebuilt.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"case": "replayable"},
        task=lambda: {"reportSystem": "bazi", "markdown": "# duplicate"},
        task_payload={"fixture": "duplicate"},
        idempotency_key="replayable-manager-rebuild",
    )
    assert duplicate.job_id == created.job_id
    assert duplicate.status == "succeeded"


def test_markdown_report_job_idempotency_key_returns_existing_job():
    client = TestClient(app)
    headers = {"Idempotency-Key": "job-idempotency-regression"}
    first = client.post("/api/v1/report/jobs", json=_payload(), headers=headers)
    second = client.post("/api/v1/report/jobs", json=_payload(), headers=headers)

    assert first.status_code == 202
    assert second.status_code == 202
    first_data = first.json()["data"]
    second_data = second.json()["data"]
    assert first_data["jobId"] == second_data["jobId"]
    assert first_data["idempotencyKey"] == "job-idempotency-regression"
    assert second_data["idempotencyKey"] == "job-idempotency-regression"


def test_report_job_api_rejects_webhook_header_when_disabled():
    response = TestClient(app).post(
        "/api/v1/report/jobs",
        json=_payload(),
        headers={"X-FateCat-Webhook-Url": "https://callback.example/webhook"},
    )

    assert response.status_code == 403
    assert response.json()["error"] == "报告任务 webhook callback 未启用"


def test_report_job_api_accepts_webhook_headers_without_echoing_secret(monkeypatch, caplog):
    captured: list[tuple[object, object]] = []

    def capture_dispatch(snapshot, config):
        captured.append((snapshot, config))

    monkeypatch.setattr(main, "REPORT_JOB_WEBHOOKS_ENABLED", True)
    monkeypatch.setattr(main.report_job_manager, "webhook_dispatcher", capture_dispatch)
    caplog.set_level(logging.INFO, logger="main")
    response = TestClient(app).post(
        "/api/v1/report/jobs",
        json=_payload(),
        headers={
            "X-FateCat-Webhook-Url": "https://callback.example/webhook",
            "X-FateCat-Webhook-Secret": "api-secret-value",
        },
    )

    assert response.status_code == 202
    body = response.json()
    body_text = json.dumps(body, ensure_ascii=False)
    assert body["data"]["webhook"] == {"enabled": True, "signature": "hmac-sha256"}
    assert "api-secret-value" not in body_text
    final_body = _wait_for_report_job(TestClient(app), body["data"]["jobId"])
    assert final_body["data"]["webhook"] == {"enabled": True, "signature": "hmac-sha256"}
    assert "api-secret-value" not in json.dumps(final_body, ensure_ascii=False)
    assert captured
    assert captured[0][1].secret == "api-secret-value"
    events = _audit_events(caplog)
    submit_event = next(item for item in events if item["action"] == "report_job.submit")
    audit_text = json.dumps(submit_event, ensure_ascii=False)
    assert submit_event["metadata"]["webhookProvided"] is True
    assert submit_event["metadata"]["webhookSignature"] == "hmac-sha256"
    assert "api-secret-value" not in audit_text
    assert "callback.example" not in audit_text


def test_report_job_api_rejects_invalid_webhook_url_when_enabled(monkeypatch):
    monkeypatch.setattr(main, "REPORT_JOB_WEBHOOKS_ENABLED", True)
    response = TestClient(app).post(
        "/api/v1/report/jobs",
        json=_payload(),
        headers={"X-FateCat-Webhook-Url": "http://127.0.0.1/internal"},
    )

    assert response.status_code == 422
    assert "webhook URL" in response.json()["error"]


def test_sqlite_report_job_store_persists_finished_jobs_and_idempotency(tmp_path):
    db_path = tmp_path / "report-jobs.sqlite"
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
        execution_policy=ReportJobExecutionPolicy(max_attempts=3, attempt_timeout_seconds=5, retry_backoff_seconds=0),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本"},
        idempotency_key="sqlite-persist-regression",
        task=lambda: {"reportSystem": "bazi", "markdown": "persisted"},
    )

    final_snapshot = _wait_for_manager_job(manager, created.job_id)
    assert final_snapshot.status == "succeeded"
    assert final_snapshot.attempts == 1
    assert final_snapshot.max_attempts == 3
    assert final_snapshot.attempt_timeout_seconds == 5
    assert [event.event_type for event in final_snapshot.events] == ["job.queued", "job.running", "job.succeeded"]
    assert final_snapshot.result == {"reportSystem": "bazi", "markdown": "persisted"}

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    loaded = rebuilt.get(created.job_id)
    assert loaded.status == "succeeded"
    assert loaded.result == {"reportSystem": "bazi", "markdown": "persisted"}
    assert loaded.input_summary == {"name": "测试样本"}
    assert loaded.idempotency_key == "sqlite-persist-regression"
    assert loaded.attempts == 1
    assert loaded.max_attempts == 3
    assert loaded.attempt_timeout_seconds == 5
    assert loaded.retry_backoff_seconds == 0
    assert [event.event_type for event in loaded.events] == ["job.queued", "job.running", "job.succeeded"]

    duplicate = rebuilt.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "另一个样本"},
        idempotency_key="sqlite-persist-regression",
        task=lambda: {"reportSystem": "bazi", "markdown": "must not run"},
    )
    assert duplicate.job_id == created.job_id
    assert duplicate.status == "succeeded"
    assert duplicate.result == {"reportSystem": "bazi", "markdown": "persisted"}
    assert duplicate.max_attempts == 3
    assert [event.event_type for event in duplicate.events] == ["job.queued", "job.running", "job.succeeded"]


def test_report_job_retry_policy_retries_retryable_errors():
    attempts: list[int] = []
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        execution_policy=ReportJobExecutionPolicy(max_attempts=3),
    )

    def flaky_task():
        attempts.append(len(attempts) + 1)
        if len(attempts) == 1:
            raise RuntimeError("temporary provider failure")
        return {"reportSystem": "bazi", "markdown": "retried"}

    created = manager.submit(kind="markdown", report_system="bazi", task=flaky_task)
    final_snapshot = _wait_for_manager_job(manager, created.job_id)

    assert final_snapshot.status == "succeeded"
    assert final_snapshot.result == {"reportSystem": "bazi", "markdown": "retried"}
    assert final_snapshot.attempts == 2
    assert attempts == [1, 2]
    assert [event.event_type for event in final_snapshot.events] == [
        "job.queued",
        "job.running",
        "job.attempt_failed",
        "job.retry_scheduled",
        "job.succeeded",
    ]
    failure_event = next(event for event in final_snapshot.events if event.event_type == "job.attempt_failed")
    assert failure_event.metadata["attempt"] == 1
    assert failure_event.metadata["retryable"] is True
    assert failure_event.metadata["willRetry"] is True
    assert failure_event.metadata["errorType"] == "RuntimeError"
    assert "error" not in failure_event.metadata


def test_report_job_retry_policy_does_not_retry_non_retryable_errors():
    attempts: list[int] = []
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        execution_policy=ReportJobExecutionPolicy(max_attempts=3),
    )

    def fatal_task():
        attempts.append(len(attempts) + 1)
        raise ReportJobNonRetryableError("invalid request shape")

    created = manager.submit(kind="markdown", report_system="bazi", task=fatal_task)
    final_snapshot = _wait_for_manager_job(manager, created.job_id)

    assert final_snapshot.status == "failed"
    assert final_snapshot.attempts == 1
    assert attempts == [1]
    assert [event.event_type for event in final_snapshot.events] == [
        "job.queued",
        "job.running",
        "job.attempt_failed",
        "job.failed",
    ]
    failure_event = next(event for event in final_snapshot.events if event.event_type == "job.attempt_failed")
    assert failure_event.metadata["retryable"] is False
    assert failure_event.metadata["willRetry"] is False
    assert failure_event.metadata["errorType"] == "ReportJobNonRetryableError"
    assert "error" not in failure_event.metadata


def test_report_job_per_job_policy_controls_non_retryable_errors():
    class CustomFatalError(RuntimeError):
        pass

    attempts: list[int] = []
    manager = ReportJobManager(max_workers=1, queue_size=4, ttl_seconds=120)

    def fatal_task():
        attempts.append(len(attempts) + 1)
        raise CustomFatalError("custom fatal")

    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        task=fatal_task,
        execution_policy=ReportJobExecutionPolicy(
            max_attempts=3,
            non_retryable_exceptions=(CustomFatalError,),
        ),
    )
    final_snapshot = _wait_for_manager_job(manager, created.job_id)

    assert final_snapshot.status == "failed"
    assert final_snapshot.attempts == 1
    assert attempts == [1]
    failure_event = next(event for event in final_snapshot.events if event.event_type == "job.attempt_failed")
    assert failure_event.metadata["retryable"] is False
    assert failure_event.metadata["willRetry"] is False
    assert failure_event.metadata["errorType"] == "CustomFatalError"


def test_report_job_timeout_policy_marks_job_failed_without_result():
    started = Event()
    release = Event()
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        execution_policy=ReportJobExecutionPolicy(max_attempts=1, attempt_timeout_seconds=0.05),
    )

    def slow_task():
        started.set()
        release.wait(timeout=2)
        return {"reportSystem": "bazi", "markdown": "late"}

    created = manager.submit(kind="markdown", report_system="bazi", task=slow_task)
    assert started.wait(timeout=2)
    final_snapshot = _wait_for_manager_job(manager, created.job_id)
    release.set()

    assert final_snapshot.status == "failed"
    assert final_snapshot.result is None
    assert final_snapshot.attempts == 1
    assert [event.event_type for event in final_snapshot.events] == [
        "job.queued",
        "job.running",
        "job.attempt_timed_out",
        "job.failed",
    ]
    timeout_event = next(event for event in final_snapshot.events if event.event_type == "job.attempt_timed_out")
    assert timeout_event.metadata["timeoutSeconds"] == 0.05
    assert timeout_event.metadata["retryable"] is True
    assert timeout_event.metadata["willRetry"] is False


def test_sqlite_report_job_store_persists_cancelled_jobs(tmp_path):
    release = Event()
    db_path = tmp_path / "report-jobs.sqlite"
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本"},
        idempotency_key="sqlite-cancel-regression",
        task=lambda: release.wait(timeout=2) or {"reportSystem": "bazi", "markdown": "discarded"},
    )
    deadline = time.monotonic() + 2
    while manager.get(created.job_id).status != "running" and time.monotonic() < deadline:
        time.sleep(0.05)

    cancelled = manager.cancel(created.job_id)
    release.set()
    assert cancelled.status == "cancelled"

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    loaded = rebuilt.get(created.job_id)
    assert loaded.status == "cancelled"
    assert loaded.result is None
    assert loaded.idempotency_key == "sqlite-cancel-regression"


def test_sqlite_report_job_store_marks_active_jobs_failed_after_rebuild(tmp_path):
    release = Event()
    db_path = tmp_path / "report-jobs.sqlite"
    manager = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    created = manager.submit(
        kind="markdown",
        report_system="bazi",
        input_summary={"name": "测试样本"},
        idempotency_key="sqlite-rebuild-regression",
        task=lambda: release.wait(timeout=2) or {"reportSystem": "bazi", "markdown": "late"},
    )
    deadline = time.monotonic() + 2
    while manager.get(created.job_id).status != "running" and time.monotonic() < deadline:
        time.sleep(0.05)

    rebuilt = ReportJobManager(
        max_workers=1,
        queue_size=4,
        ttl_seconds=120,
        store=SQLiteReportJobStore(db_path),
    )
    loaded = rebuilt.get(created.job_id)
    release.set()
    assert loaded.status == "failed"
    assert loaded.error == "任务执行器已重启，未完成任务已终止"
    assert [event.event_type for event in loaded.events] == [
        "job.queued",
        "job.running",
        "job.recovered_failed",
    ]


def test_markdown_report_job_can_be_cancelled(monkeypatch, caplog):
    started = Event()
    release = Event()

    def blocking_report(_req):
        started.set()
        release.wait(timeout=2)
        return {"reportSystem": "bazi", "markdown": "should be discarded"}

    monkeypatch.setattr(main, "_build_markdown_report_payload", blocking_report)
    caplog.set_level(logging.INFO, logger="main")
    client = TestClient(app)
    response = client.post("/api/v1/report/jobs", json=_payload(), headers={"Idempotency-Key": "cancel-regression"})

    assert response.status_code == 202
    job_id = response.json()["data"]["jobId"]
    started.wait(timeout=2)
    cancel_response = client.post(f"/api/v1/report/jobs/{job_id}/cancel")
    release.set()

    assert cancel_response.status_code == 200
    assert cancel_response.json()["data"]["status"] == "cancelled"
    status_response = client.get(f"/api/v1/report/jobs/{job_id}")
    assert status_response.status_code == 200
    assert status_response.json()["data"]["status"] == "cancelled"
    assert "result" not in status_response.json()["data"]
    events = _audit_events(caplog)
    submit_event = next(item for item in events if item["action"] == "report_job.submit")
    cancel_event = next(item for item in events if item["action"] == "report_job.cancel")
    audit_text = json.dumps([submit_event, cancel_event], ensure_ascii=False)
    assert submit_event["targetType"] == "CalculationJob"
    assert submit_event["metadata"]["idempotencyKeyProvided"] is True
    assert cancel_event["targetType"] == "CalculationJob"
    assert cancel_event["metadata"]["status"] == "cancelled"
    assert job_id not in audit_text
    assert "cancel-regression" not in audit_text


def test_markdown_and_web_report_jobs_return_gates_and_do_not_write_records(monkeypatch):
    def fail_save_record(**_kwargs):
        raise AssertionError("report job must not write record storage")

    monkeypatch.setattr("main.db.save_record", fail_save_record)
    client = TestClient(app)

    standard_response = client.post("/api/v1/report/jobs", json=_payload())
    assert standard_response.status_code == 202
    standard_final = _wait_for_report_job(client, standard_response.json()["data"]["jobId"])

    web_response = client.post(
        "/api/v1/report/jobs/web",
        json={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京市朝阳区",
            "locationId": "cn:110105",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "bazi",
        },
    )
    assert web_response.status_code == 202
    web_final = _wait_for_report_job(client, web_response.json()["data"]["jobId"])

    assert standard_final["data"]["status"] == "succeeded"
    assert web_final["data"]["status"] == "succeeded"
    assert standard_final["data"]["result"]["policyGate"]["status"] == "pass"
    assert standard_final["data"]["result"]["snapshotGate"]["status"] == "pass"
    assert web_final["data"]["result"]["policyGate"]["status"] == "pass"
    assert web_final["data"]["result"]["snapshotGate"]["status"] == "pass"
    assert "# 命理排盘报告：测试样本" in standard_final["data"]["result"]["markdown"]
    assert "# 命理排盘报告：测试样本" in web_final["data"]["result"]["markdown"]


def test_web_report_job_api_renders_completed_job_in_web_page():
    client = TestClient(app)
    response = client.post(
        "/api/v1/report/jobs/web",
        json={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京市朝阳区",
            "locationId": "cn:110105",
            "gender": "male",
            "reportSystem": "bazi",
            "name": "异步样本",
        },
    )

    assert response.status_code == 202
    job_id = response.json()["data"]["jobId"]
    final_body = _wait_for_report_job(client, job_id)
    assert final_body["data"]["status"] == "succeeded"

    page = client.get("/web", params={"jobId": job_id})
    assert page.status_code == 200
    assert "任务状态：已完成" in page.text
    assert '<h2 id="markdown-output">Markdown 输出</h2>' in page.text
    assert "# 命理排盘报告：异步样本" in page.text


def test_report_job_api_rejects_when_queue_is_full(monkeypatch):
    def full_queue(**_kwargs):
        raise ReportJobQueueFull("报告队列已满，请稍后再试")

    monkeypatch.setattr(main.report_job_manager, "submit", full_queue)

    response = TestClient(app).post("/api/v1/report/jobs", json=_payload())

    assert response.status_code == 429
    assert response.json()["error"] == "报告队列已满，请稍后再试"


def test_bazi_markdown_report_keeps_high_risk_topic_profiles_out_of_default_report():
    response = TestClient(app).post("/api/v1/report/markdown", json=_payload())

    assert response.status_code == 200
    markdown = response.json()["data"]["markdown"]
    assert "# 命理排盘报告：测试样本" in markdown
    assert "专题 profile" not in markdown
    assert "topicProfiles" not in markdown
    assert "健康 profile" not in markdown
    assert "财运 profile" not in markdown
    for forbidden in ("医疗建议", "投资建议", "法律建议", "心理建议", "必然", "保证", "灾祸"):
        assert forbidden not in markdown


def test_markdown_report_api_rejects_retired_jianchu_system():
    payload = _payload()
    payload["options"]["reportSystem"] = "jianchu"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 422


def test_markdown_report_api_rejects_retired_bone_system():
    payload = _payload()
    payload["options"]["reportSystem"] = "bone"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 422


def test_report_systems_api_lists_enabled_and_planned_systems():
    response = TestClient(app).get("/api/v1/report/systems")

    assert response.status_code == 200
    body = response.json()
    systems = {item["id"]: item for item in body["data"]["systems"]}
    assert systems["bazi"]["enabled"] is True
    assert systems["ziwei"]["enabled"] is True
    assert systems["huangli"]["enabled"] is False
    assert systems["meihua"]["status"] == "production"
    assert systems["meihua"]["enabled"] is False
    assert systems["liuyao"]["status"] == "planned"
    assert systems["fengshui"]["group"] == "未来功能"


def test_capabilities_api_lists_almanac_as_standalone_production():
    response = TestClient(app).get("/api/v1/capabilities")

    assert response.status_code == 200
    body = response.json()
    capabilities = {item["capabilityId"]: item for item in body["data"]["capabilities"]}
    assert capabilities["bazi"]["defaultVisibility"] == "default"
    assert capabilities["bazi"]["maturity"]["level"] == "L4"
    assert capabilities["bazi"]["engine"]["provider"] == "fate_core.usecases.calculate_pure_analysis"
    assert capabilities["bazi"]["engine"]["engineVersion"] == "fate-core-bazi-v1"
    assert capabilities["bazi"]["provider"]["providerId"] == "fate_core.usecases.calculate_pure_analysis"
    assert capabilities["bazi"]["provider"]["health"]["status"] == "ready"
    assert capabilities["bazi"]["evidencePolicy"]["ruleIdRequired"] is True
    assert capabilities["bazi"]["testGate"]["status"] == "passing"
    assert capabilities["almanac"]["availability"] == "available"
    assert capabilities["almanac"]["status"] == "validated"
    assert capabilities["almanac"]["defaultVisibility"] == "standalone"
    assert capabilities["almanac"]["maturity"]["level"] == "L3"
    assert capabilities["almanac"]["capabilityApiEnabled"] is True
    assert capabilities["almanac"]["markdownReportEnabled"] is False
    assert capabilities["almanac"]["surfaces"] == {
        "capabilityApi": True,
        "markdownReport": False,
        "webForm": False,
    }
    assert capabilities["ziwei"]["status"] == "production"
    assert capabilities["ziwei"]["availability"] == "available"
    assert capabilities["ziwei"]["defaultVisibility"] == "standalone"
    assert capabilities["ziwei"]["maturity"]["level"] == "L4"
    assert capabilities["ziwei"]["engine"]["engineVersion"] == "fate-core-ziwei-v1"
    assert capabilities["ziwei"]["capabilityApiEnabled"] is True
    assert capabilities["ziwei"]["markdownReportEnabled"] is True
    assert capabilities["meihua"]["availability"] == "available"
    assert capabilities["meihua"]["status"] == "validated"
    assert capabilities["meihua"]["defaultVisibility"] == "standalone"
    assert capabilities["meihua"]["maturity"]["level"] == "L3"
    assert capabilities["meihua"]["capabilityApiEnabled"] is True
    assert capabilities["meihua"]["markdownReportEnabled"] is False
    assert capabilities["liuyao"]["maturity"]["level"] == "L0"
    assert capabilities["liuyao"]["availability"] == "planned"
    assert capabilities["liuyao"]["status"] == "registered"
    assert capabilities["liuyao"]["testGate"]["status"] == "blocked"
    assert capabilities["liuyao"]["provider"]["health"]["status"] == "blocked"


def test_measurement_infrastructure_capabilities_alias_matches_v1_contract():
    client = TestClient(app)
    canonical = client.get("/api/v1/capabilities")
    alias = client.get("/capabilities")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"]["capabilities"] == canonical.json()["data"]["capabilities"]


def test_capability_api_executes_almanac_without_enabling_markdown_system():
    response = TestClient(app).post(
        "/api/v1/capabilities/almanac",
        json={
            "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
            "eventType": "出行",
            "place": "北京",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["capabilityId"] == "almanac"
    assert body["reportProfile"] == "almanac"
    assert body["data"]["dateRange"]["days"] == 1
    assert body["data"]["days"][0]["timeSlots"]
    assert len(body["data"]["days"][0]["timeSlots"]) == 12
    assert body["data"]["days"][0]["scoreBreakdown"]
    assert body["evidence"]["source"] == "lunar-python"
    assert body["metadata"]["maturity"]["level"] == "L3"
    assert body["metadata"]["engine"]["engineVersion"] == "fate-core-almanac-v1"
    assert body["metadata"]["provider"]["providerId"] == "fate_core.usecases.calculate_almanac"
    assert body["metadata"]["provider"]["health"]["status"] == "ready"
    assert body["report"]["resourceType"] == "Report"
    assert body["report"]["capabilityId"] == "almanac"
    assert body["report"]["profile"] == "almanac"
    assert body["report"]["formats"] == ["json"]
    assert body["report"]["defaultFormat"] == "json"
    assert body["report"]["links"]["capability"] == "/capabilities/almanac"
    assert body["report"]["links"]["schemas"]["report"] == "contracts/fate/capabilities/schemas/report.schema.json"
    assert {section["id"] for section in body["report"]["sections"]} >= {"dateRange", "days"}
    assert body["report"]["evidenceRefs"]
    assert body["report"]["policyGate"]["status"] == "pass"
    assert body["report"]["policyGate"]["engine"] == "literal-substring-v1"
    assert body["report"]["policyGate"]["policySource"] == "result.risk.forbiddenClaims"
    assert body["report"]["policyGate"]["matches"] == []
    assert "report.risk.forbiddenClaims" in body["report"]["policyGate"]["excludedFields"]
    assert body["report"]["metadata"]["snapshotGate"] == "后续切片实现完整 report snapshot gate。"


def test_measurement_capability_calculate_alias_executes_same_executor():
    response = TestClient(app).post(
        "/capabilities/meihua/calculate",
        json={
            "question": "测试问题能否推进",
            "castMethod": "number",
            "castValue": "3,8,6",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["capabilityId"] == "meihua"
    assert body["data"]["hexagrams"]["movingLine"] == 5
    assert body["metadata"]["maturity"]["level"] == "L3"
    assert body["metadata"]["provider"]["providerId"] == "fate_core.usecases.calculate_meihua"
    assert body["report"]["resourceType"] == "Report"
    assert body["report"]["profile"] == "meihua"
    assert body["report"]["policyGate"]["status"] == "pass"
    assert {section["id"] for section in body["report"]["sections"]} >= {"hexagrams", "bodyUse"}


def test_capability_api_executes_meihua_without_enabling_markdown_system():
    response = TestClient(app).post(
        "/api/v1/capabilities/meihua",
        json={
            "question": "测试问题能否推进",
            "castMethod": "number",
            "castValue": "3,8,6",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["capabilityId"] == "meihua"
    assert body["reportProfile"] == "meihua"
    assert body["data"]["hexagrams"]["movingLine"] == 5
    assert body["evidence"]["items"]["cast"]["ruleIds"] == ["meihua.number_cast"]
    assert body["metadata"]["engine"]["provider"] == "fate_core.usecases.calculate_meihua"
    assert body["metadata"]["provider"]["health"]["checks"]["scope"] == "in-process"


def test_measurement_infrastructure_metadata_and_reports_are_available():
    client = TestClient(app)
    metadata_response = client.get("/metadata")
    reports_response = client.get("/reports")

    assert metadata_response.status_code == 200
    metadata = metadata_response.json()["data"]
    assert metadata["service"] == "FateCat"
    assert metadata["positioning"] == "面向 Agent 与应用开发者的测算基础设施"
    assert metadata["capabilityProtocol"]["registryEndpoint"] == "/capabilities"
    assert metadata["capabilityProtocol"]["providerRegistryEndpoint"] == "/providers"
    assert metadata["capabilityProtocol"]["evaluationRegistryEndpoint"] == "/evaluations"
    assert metadata["capabilityProtocol"]["observabilityRegistryEndpoint"] == "/observability"
    assert metadata["capabilityProtocol"]["securityRegistryEndpoint"] == "/security"
    assert metadata["capabilityProtocol"]["surfaceRegistryEndpoint"] == "/surfaces"
    assert metadata["developer"]["openapi"] == "/openapi.json"
    assert metadata["developer"]["capabilityDetail"] == "/capabilities/{capability_id}"
    assert metadata["developer"]["capabilityCalculate"] == "/capabilities/{capability_id}/calculate"
    assert metadata["developer"]["providerList"] == "/providers"
    assert metadata["developer"]["providerDetail"] == "/providers/{provider_id}"
    assert metadata["developer"]["evaluationList"] == "/evaluations"
    assert metadata["developer"]["evaluationDetail"] == "/evaluations/{evaluation_id}"
    assert metadata["developer"]["observabilityList"] == "/observability"
    assert metadata["developer"]["observabilityDetail"] == "/observability/{signal_id}"
    assert metadata["developer"]["securityList"] == "/security"
    assert metadata["developer"]["securityDetail"] == "/security/{control_id}"
    assert metadata["developer"]["surfaceList"] == "/surfaces"
    assert metadata["developer"]["surfaceDetail"] == "/surfaces/{surface_id}"
    assert metadata["developer"]["apiGuide"] == "docs/reference-materials/operations/测算基础设施 API 接入.md"
    assert metadata["developer"]["developerPlatform"] == "contracts/fate/developer/developer-platform.json"
    assert metadata["developer"]["sdkPackageBaseline"] == "docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md"
    assert metadata["developer"]["sandboxTokenContract"] == "contracts/fate/developer/sandbox-token-contract.json"
    assert metadata["developer"]["apiChangelog"] == "contracts/fate/developer/api-changelog.json"
    assert metadata["developer"]["developerPlatformGate"] == "bash scripts/developer-platform-gate.sh"
    assert metadata["developer"]["errors"] == "/errors"
    assert metadata["quality"]["health"] == "/health"
    assert metadata["quality"]["metrics"] == "/metrics"
    assert metadata["quality"]["reportJobStore"] == "memory"
    assert (
        metadata["privacy"]["birthPlaceDisplayPolicy"]
        == "默认示例使用北京/测试用户；公共行政区候选和用户主动提交的地区可在当前响应显示，不进入日志或默认持久化。"
    )
    assert metadata["productionGate"]["externalConnectivity"] == "外部连通验证待执行"

    assert reports_response.status_code == 200
    reports = reports_response.json()["data"]
    assert reports["jobEndpoint"] == "/api/v1/report/jobs"
    assert reports["markdownEndpoint"] == "/api/v1/report/markdown"
    assert reports["reportSchema"] == "contracts/fate/capabilities/schemas/report.schema.json"
    assert reports["cancelEndpoint"] == "/api/v1/report/jobs/{job_id}/cancel"
    assert reports["idempotencyHeader"] == "Idempotency-Key"
    assert {item["id"] for item in reports["profiles"]} >= {"bazi", "ziwei", "meihua"}


def test_measurement_capability_detail_exposes_resource_contract():
    response = TestClient(app).get("/capabilities/bazi")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["resourceType"] == "Capability"
    assert data["apiVersion"] == "fatecat.tradecatlabs/v1"
    assert data["id"] == "bazi"
    assert data["capabilityId"] == "bazi"
    assert data["availability"] == "available"
    assert data["status"] == "production"
    assert data["admission"] == {"executable": True, "reason": "能力可执行（availability=available）"}
    assert data["input"]["required"] == ["birthDateTime", "gender", "longitude", "latitude"]
    assert data["links"]["self"] == "/capabilities/bazi"
    assert data["links"]["calculate"] == "/capabilities/bazi/calculate"
    assert data["links"]["provider"] == "/providers/fate_core.usecases.calculate_pure_analysis"
    assert data["links"]["errors"] == "/errors"
    assert data["schemas"]["resource"] == "contracts/fate/capabilities/schemas/resource.schema.json"
    assert data["schemas"]["provider"] == "contracts/fate/capabilities/schemas/provider.schema.json"
    assert data["schemas"]["report"] == "contracts/fate/capabilities/schemas/report.schema.json"
    assert data["schemas"]["error"] == "contracts/fate/capabilities/schemas/error.schema.json"
    assert data["provider"]["providerId"] == "fate_core.usecases.calculate_pure_analysis"
    assert data["provider"]["interfaceVersion"] == "provider-protocol-v1"
    assert data["provider"]["health"]["status"] == "ready"
    assert data["risk"]["disclaimerRequired"] is True
    assert "替代医疗法律金融判断" in data["risk"]["forbiddenClaims"]


def test_planned_capability_detail_is_discoverable_but_not_executable():
    response = TestClient(app).get("/api/v1/capabilities/liuyao")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["resourceType"] == "Capability"
    assert data["capabilityId"] == "liuyao"
    assert data["availability"] == "planned"
    assert data["status"] == "registered"
    assert data["admission"]["executable"] is False
    assert data["admission"]["reason"] == "能力当前不可执行（availability=planned），只允许发现和审计"
    assert data["engine"]["provider"] == "planned.liuyao"
    assert data["provider"]["providerId"] == "planned.liuyao"
    assert data["provider"]["health"]["status"] == "blocked"
    assert data["testGate"]["status"] == "blocked"


def test_provider_resources_are_discoverable_and_linked_to_capabilities():
    client = TestClient(app)
    canonical = client.get("/api/v1/providers")
    alias = client.get("/providers")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]

    providers = {item["providerId"]: item for item in canonical.json()["data"]["providers"]}
    assert set(providers) == {
        "fate_core.usecases.calculate_pure_analysis",
        "fate_core.usecases.calculate_almanac",
        "fate_core.usecases.calculate_ziwei",
        "fate_core.usecases.calculate_meihua",
    }
    assert "planned.liuyao" not in providers

    bazi_provider = providers["fate_core.usecases.calculate_pure_analysis"]
    assert bazi_provider["resourceType"] == "Provider"
    assert bazi_provider["apiVersion"] == "fatecat.tradecatlabs/v1"
    assert bazi_provider["id"] == "fate_core.usecases.calculate_pure_analysis"
    assert bazi_provider["engineVersion"] == "fate-core-bazi-v1"
    assert bazi_provider["capabilities"] == ["bazi"]
    assert bazi_provider["interfaceVersion"] == "provider-protocol-v1"
    assert bazi_provider["versionLock"]["engineVersion"] == "fate-core-bazi-v1"
    assert bazi_provider["lifecycle"]["status"] == "active"
    assert bazi_provider["sourcePolicy"]["supplyChainRefs"] == [
        "tools/reference-repos/vendor_sources.json#lunar-python"
    ]
    assert bazi_provider["licensePolicy"]["productionUseAllowed"] is True
    assert "tests/regression/test_capability_protocol.py" in bazi_provider["resourceManifest"]["testRefs"]
    assert bazi_provider["promotionGate"]["status"] == "passing"
    assert bazi_provider["deprecation"]["status"] == "active"
    assert bazi_provider["health"]["status"] == "ready"
    assert bazi_provider["metadata"]["externalConnectivity"] == "外部连通验证待执行"
    assert bazi_provider["links"]["self"] == "/providers/fate_core.usecases.calculate_pure_analysis"

    detail = client.get("/providers/fate_core.usecases.calculate_pure_analysis")
    assert detail.status_code == 200
    assert detail.json()["data"] == bazi_provider


def test_measurement_error_catalog_is_discoverable_and_versioned():
    client = TestClient(app)
    canonical = client.get("/api/v1/errors")
    alias = client.get("/errors")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]
    catalog = canonical.json()["data"]
    assert catalog["schemaVersion"] == 1
    errors = {item["code"]: item for item in catalog["errors"]}
    assert errors["FC_CAPABILITY_NOT_FOUND"]["httpStatus"] == 400
    assert errors["FC_CAPABILITY_NOT_PRODUCTION"]["category"] == "capability"
    assert errors["FC_RATE_LIMITED"]["retryable"] is True
    assert errors["FC_TIMEOUT"]["httpStatus"] == 504


def test_evaluation_resources_are_discoverable_and_linked():
    client = TestClient(app)
    canonical = client.get("/api/v1/evaluations")
    alias = client.get("/evaluations")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]

    payload = canonical.json()["data"]
    assert payload["schemaVersion"] == 1
    assert payload["schemas"]["dataset"] == "contracts/fate/evaluations/schemas/dataset.schema.json"
    assert payload["schemas"]["evaluationRun"] == "contracts/fate/evaluations/schemas/evaluation-run.schema.json"
    assert payload["metadata"]["runner"]["command"] == "bash scripts/run-evaluations.sh"
    assert payload["metadata"]["runner"]["defaultMode"] == "all-local-required"
    assert payload["metadata"]["diffPolicy"] == "contracts/fate/evaluations/diff-policy.json"
    assert payload["metadata"]["coreQualityCorpusManifest"] == "contracts/fate/evaluations/core-quality-corpus.json"
    assert payload["metadata"]["reportDiffPolicy"] == "contracts/fate/evaluations/report-diff-policy.json"
    resources = {item["id"]: item for item in payload["resources"]}
    assert {
        "dataset.solar_terms_1900_2030",
        "dataset.bazi_golden_matrix",
        "dataset.ziwei_golden_cases",
        "dataset.bazi_ziwei_core_quality_corpus",
        "dataset.mingli_bench_offline",
        "run.local_ci_quick",
        "run.solar_terms_golden",
        "run.evaluation_dashboard_smoke",
        "run.core_quality_corpus_gate",
        "run.mingli_bench_offline",
    } <= set(resources)

    solar_terms = resources["dataset.solar_terms_1900_2030"]
    assert solar_terms["resourceType"] == "Dataset"
    assert solar_terms["usageRole"] == "evaluation_only"
    assert solar_terms["localAvailability"] == "tracked_in_repo"
    assert solar_terms["links"]["self"] == "/evaluations/dataset.solar_terms_1900_2030"

    mingli = resources["dataset.mingli_bench_offline"]
    assert mingli["status"] == "requires_reference_repo"
    assert mingli["metadata"]["releaseGate"] == "optional"
    assert "标准答案不得进入 production provider" in mingli["metadata"]["risk"]

    local_ci = resources["run.local_ci_quick"]
    assert local_ci["resourceType"] == "EvaluationRun"
    assert local_ci["releaseRequired"] is True
    assert local_ci["datasetIds"] == [
        "dataset.solar_terms_1900_2030",
        "dataset.bazi_golden_matrix",
        "dataset.ziwei_golden_cases",
        "dataset.bazi_ziwei_core_quality_corpus",
    ]
    assert local_ci["lastKnownStatusPolicy"] == "tracked_by_task_evidence"

    core_quality = resources["run.core_quality_corpus_gate"]
    assert core_quality["releaseRequired"] is True
    assert core_quality["datasetIds"] == ["dataset.bazi_ziwei_core_quality_corpus"]

    detail = client.get("/evaluations/run.solar_terms_golden")
    assert detail.status_code == 200
    assert detail.json()["data"] == resources["run.solar_terms_golden"]

    unknown = client.get("/api/v1/evaluations/not-found")
    assert unknown.status_code == 400


def test_observability_signals_are_discoverable_and_linked():
    client = TestClient(app)
    canonical = client.get("/api/v1/observability")
    alias = client.get("/observability")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]

    payload = canonical.json()["data"]
    assert payload["schemaVersion"] == 1
    assert payload["schemas"]["observabilitySignal"] == (
        "contracts/fate/observability/schemas/observability-signal.schema.json"
    )
    assert payload["metadata"]["smokeCommand"] == "bash scripts/observability-smoke.sh"
    assert "TestClient" in payload["metadata"]["smokeScope"]
    assert payload["metadata"]["traceSloSmokeCommand"] == "bash scripts/observability-trace-slo-smoke.sh"
    assert payload["metadata"]["sloGateCommand"] == "bash scripts/observability-slo-gate.sh"
    signals = {item["id"]: item for item in payload["signals"]}
    assert {
        "signal.health",
        "signal.readiness",
        "signal.http_request_metrics",
        "signal.job_and_queue_metrics",
        "signal.request_id_and_structured_logs",
        "signal.provider_report_traces",
        "signal.slo_and_alerts",
    } <= set(signals)

    health = signals["signal.health"]
    assert health["resourceType"] == "ObservabilitySignal"
    assert health["status"] == "available"
    assert health["endpoint"] == "/health"
    assert health["externalConnectivity"] == "not_required"

    metrics_signal = signals["signal.http_request_metrics"]
    assert metrics_signal["signalType"] == "metric"
    assert "fatecat_requests_total" in metrics_signal["fields"]
    assert "不得包含用户姓名" in metrics_signal["privacyBoundary"]

    traces = signals["signal.provider_report_traces"]
    assert traces["signalType"] == "trace"
    assert traces["status"] == "available"
    assert traces["endpoint"] == "application logs"
    assert traces["localVerification"]
    assert traces["externalConnectivity"] == "external_connectivity_pending"

    slo_alerts = signals["signal.slo_and_alerts"]
    assert slo_alerts["signalType"] == "slo"
    assert slo_alerts["status"] == "available"
    assert "alert-rules.json" in slo_alerts["endpoint"]

    detail = client.get("/observability/signal.http_request_metrics")
    assert detail.status_code == 200
    assert detail.json()["data"] == metrics_signal

    unknown = client.get("/api/v1/observability/not-found")
    assert unknown.status_code == 400


def test_security_controls_are_discoverable_and_linked():
    client = TestClient(app)
    canonical = client.get("/api/v1/security")
    alias = client.get("/security")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]

    payload = canonical.json()["data"]
    assert payload["schemaVersion"] == 1
    assert payload["schemas"]["securityControl"] == "contracts/fate/security/schemas/security-control.schema.json"
    assert payload["metadata"]["smokeCommand"] == "bash scripts/security-smoke.sh"
    assert "TestClient" in payload["metadata"]["smokeScope"]
    controls = {item["id"]: item for item in payload["controls"]}
    assert {
        "control.record_token_access",
        "control.cors_allowlist",
        "control.rate_limit",
        "control.request_body_limit",
        "control.response_security_headers",
        "control.rbac_policy",
        "control.production_identity_oidc",
        "control.external_siem_immutable_audit",
        "control.retention_cleanup_plan",
        "control.external_secret_provider_kms",
        "control.owasp_api_security_regression",
        "control.audit_event_log",
        "control.retention_policy",
        "control.privacy_fixture_policy",
        "control.source_hygiene_gate",
        "control.secret_scan_gate",
        "control.public_release_policy",
        "control.production_readiness_external",
    } <= set(controls)

    auth = controls["control.record_token_access"]
    assert auth["resourceType"] == "SecurityControl"
    assert auth["controlType"] == "auth"
    assert auth["status"] == "available"
    assert "FATE_API_USER_TOKENS" in auth["envVars"]
    assert auth["externalConnectivity"] == "not_required"
    assert auth["links"]["self"] == "/security/control.record_token_access"

    rbac = controls["control.rbac_policy"]
    assert rbac["resourceType"] == "SecurityControl"
    assert rbac["controlType"] == "rbac"
    assert rbac["status"] == "available"
    assert "FATE_API_USER_TOKENS" in rbac["envVars"]
    assert "record.read" in rbac["metadata"]["recordScopes"]
    assert "OAuth/OIDC" in rbac["metadata"]["risk"]

    identity = controls["control.production_identity_oidc"]
    assert identity["controlType"] == "identity"
    assert identity["status"] == "manual"
    assert "FATE_OIDC_JWKS_URL" in identity["envVars"]
    assert identity["externalConnectivity"] == "external_connectivity_pending"

    siem = controls["control.external_siem_immutable_audit"]
    assert siem["controlType"] == "siem"
    assert siem["status"] == "manual"
    assert "FATE_AUDIT_IMMUTABILITY_MODE" in siem["envVars"]

    cleanup = controls["control.retention_cleanup_plan"]
    assert cleanup["controlType"] == "retention"
    assert cleanup["status"] == "manual"
    assert "FATE_RECORD_RETENTION_AUTO_CLEANUP_ENABLED" in cleanup["envVars"]

    secret_provider = controls["control.external_secret_provider_kms"]
    assert secret_provider["controlType"] == "secret_provider"
    assert secret_provider["status"] == "manual"
    assert secret_provider["externalConnectivity"] == "external_connectivity_pending"
    assert "FATE_EXTERNAL_SECRET_PROVIDER_EVIDENCE" in secret_provider["envVars"]
    assert "external-secret-provider-gate.sh" in " ".join(secret_provider["localVerification"])

    owasp = controls["control.owasp_api_security_regression"]
    assert owasp["controlType"] == "owasp_api_regression"
    assert owasp["status"] == "available"
    assert "bash scripts/production-security-gate.sh" in owasp["localVerification"]

    privacy = controls["control.privacy_fixture_policy"]
    assert privacy["controlType"] == "privacy"
    assert "默认示例只使用北京/测试用户" in privacy["privacyBoundary"]
    assert "公共行政区候选" in privacy["privacyBoundary"]
    assert privacy["localVerification"] == ["bash scripts/check-privacy-fixtures.sh"]

    secret_scan = controls["control.secret_scan_gate"]
    assert secret_scan["controlType"] == "secret_scan"
    assert secret_scan["status"] == "available"
    assert "scripts/secret-scan.sh" in secret_scan["implementationRefs"]
    assert "疑似密钥原文" in secret_scan["privacyBoundary"]
    assert payload["metadata"]["secretScanCommand"].startswith("bash scripts/secret-scan.sh")

    audit_log = controls["control.audit_event_log"]
    assert audit_log["controlType"] == "audit_log"
    assert audit_log["status"] == "available"
    assert "FATE_AUDIT_EVENT_RETENTION_DAYS" in audit_log["envVars"]
    assert "recordId" in audit_log["privacyBoundary"]

    retention = controls["control.retention_policy"]
    assert retention["controlType"] == "retention"
    assert "FATE_REPORT_JOB_TTL_SECONDS" in retention["envVars"]
    assert "显式删除" in retention["metadata"]["risk"]

    readiness = controls["control.production_readiness_external"]
    assert readiness["controlType"] == "production_readiness"
    assert readiness["status"] == "manual"
    assert readiness["externalConnectivity"] == "external_connectivity_pending"
    assert "FATE_BOT_TOKEN" in readiness["envVars"]

    detail = client.get("/security/control.source_hygiene_gate")
    assert detail.status_code == 200
    assert detail.json()["data"] == controls["control.source_hygiene_gate"]

    unknown = client.get("/api/v1/security/not-found")
    assert unknown.status_code == 400


def test_delivery_surfaces_are_discoverable_and_linked():
    client = TestClient(app)
    canonical = client.get("/api/v1/surfaces")
    alias = client.get("/surfaces")

    assert canonical.status_code == 200
    assert alias.status_code == 200
    assert alias.json()["data"] == canonical.json()["data"]

    payload = canonical.json()["data"]
    assert payload["schemaVersion"] == 1
    assert payload["schemas"]["deliverySurface"] == "contracts/fate/delivery/schemas/delivery-surface.schema.json"
    assert payload["schemas"]["releaseGate"] == "contracts/fate/delivery/schemas/release-gate.schema.json"
    assert payload["releaseGate"]["id"] == "gate.live_release"
    assert payload["releaseGate"]["shipGateStatus"] == "blocked"
    surfaces = {item["id"]: item for item in payload["surfaces"]}
    assert {
        "surface.fastapi",
        "surface.web",
        "surface.telegram_bot",
        "surface.cli",
        "surface.agent_skill",
        "surface.huggingface_space",
    } <= set(surfaces)

    api_surface = surfaces["surface.fastapi"]
    assert api_surface["resourceType"] == "DeliverySurface"
    assert api_surface["surfaceType"] == "api"
    assert api_surface["status"] == "available"
    assert "/api/v1/report/markdown" in api_surface["entrypoints"]
    assert "markdown" in api_surface["supportedOutputs"]
    assert "calculate_delivery_result" in " ".join(api_surface["canonicalChain"])

    web_surface = surfaces["surface.web"]
    assert web_surface["surfaceType"] == "web"
    assert "/web" in web_surface["entrypoints"]
    assert "build_web_report_result" in " ".join(web_surface["canonicalChain"])
    assert "不得由前端自行拼装核心报告" in web_surface["privacyBoundary"]

    bot_surface = surfaces["surface.telegram_bot"]
    assert bot_surface["surfaceType"] == "bot"
    assert bot_surface["externalConnectivity"] == "requires_real_credentials"
    assert "live token" in bot_surface["metadata"]["sameSourceScope"]

    cli_surface = surfaces["surface.cli"]
    assert cli_surface["status"] == "partial"
    assert cli_surface["supportedOutputs"] == ["json"]
    assert "不生成标准 Markdown" in cli_surface["metadata"]["sameSourceScope"]

    hosted = surfaces["surface.huggingface_space"]
    assert hosted["status"] == "manual"
    assert hosted["externalConnectivity"] == "requires_hosted_platform"

    detail = client.get("/surfaces/surface.web")
    assert detail.status_code == 200
    assert detail.json()["data"] == web_surface

    unknown = client.get("/api/v1/surfaces/not-found")
    assert unknown.status_code == 400


def test_measurement_infrastructure_openapi_exposes_developer_entrypoints():
    response = TestClient(app).get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/metadata" in paths
    assert "/capabilities" in paths
    assert "/capabilities/{capability_id}" in paths
    assert "/capabilities/{capability_id}/calculate" in paths
    assert "/providers" in paths
    assert "/providers/{provider_id}" in paths
    assert "/errors" in paths
    assert "/evaluations" in paths
    assert "/evaluations/{evaluation_id}" in paths
    assert "/observability" in paths
    assert "/observability/{signal_id}" in paths
    assert "/security" in paths
    assert "/security/{control_id}" in paths
    assert "/surfaces" in paths
    assert "/surfaces/{surface_id}" in paths
    assert "/api/v1/report/jobs/{job_id}/cancel" in paths
    assert "/reports" in paths


def test_markdown_report_displays_submitted_birth_place():
    payload = _payload()
    payload["birthPlace"] = {
        "name": "上海市",
        "longitude": 121.4737,
        "latitude": 31.2304,
        "timezone": "Asia/Shanghai",
    }

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 200
    markdown = response.json()["data"]["markdown"]
    assert "出生地区" in markdown
    assert "上海市" in markdown
    assert "已填写（非北京地区已隐藏）" not in markdown
