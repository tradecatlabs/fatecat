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
from report_jobs import ReportJobManager, ReportJobQueueFull, SQLiteReportJobStore  # noqa: E402
from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig  # noqa: E402


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
    assert 'fatecat_report_job_store_backend_info{backend="memory"} 1' in metrics_response.text
    assert "fatecat_bot_queue_size" in metrics_response.text
    assert 'fatecat_bot_queue_scope_info{backend="memory",scope="single_process"} 1' in metrics_response.text
    assert "fatecat_bot_queue_max_size" in metrics_response.text
    assert "fatecat_bot_concurrent_requests" in metrics_response.text


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
    assert "## 八字排盘详情" not in markdown


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

    final_snapshot = _wait_for_manager_job(manager, created.job_id)
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
            "birthPlace": "北京",
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
            "birthPlace": "北京",
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
    assert capabilities["almanac"]["status"] == "production"
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
    assert capabilities["ziwei"]["defaultVisibility"] == "standalone"
    assert capabilities["ziwei"]["maturity"]["level"] == "L4"
    assert capabilities["ziwei"]["engine"]["engineVersion"] == "fate-core-ziwei-v1"
    assert capabilities["ziwei"]["capabilityApiEnabled"] is True
    assert capabilities["ziwei"]["markdownReportEnabled"] is True
    assert capabilities["meihua"]["status"] == "production"
    assert capabilities["meihua"]["defaultVisibility"] == "standalone"
    assert capabilities["meihua"]["maturity"]["level"] == "L3"
    assert capabilities["meihua"]["capabilityApiEnabled"] is True
    assert capabilities["meihua"]["markdownReportEnabled"] is False
    assert capabilities["liuyao"]["maturity"]["level"] == "L0"
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
    assert metadata["developer"]["errors"] == "/errors"
    assert metadata["quality"]["health"] == "/health"
    assert metadata["quality"]["metrics"] == "/metrics"
    assert metadata["quality"]["reportJobStore"] == "memory"
    assert metadata["privacy"]["birthPlaceDisplayPolicy"] == "公开 Web 示例和用户界面不得展示北京以外的真实地区名称。"
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
    assert data["admission"] == {"executable": True, "reason": "production capability"}
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
    assert data["status"] == "planned"
    assert data["admission"]["executable"] is False
    assert data["admission"]["reason"] == "能力尚未生产化，当前只允许发现和审计"
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
    resources = {item["id"]: item for item in payload["resources"]}
    assert {
        "dataset.solar_terms_1900_2030",
        "dataset.bazi_golden_matrix",
        "dataset.ziwei_golden_cases",
        "dataset.mingli_bench_offline",
        "run.local_ci_quick",
        "run.solar_terms_golden",
        "run.evaluation_dashboard_smoke",
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
    ]
    assert local_ci["lastKnownStatusPolicy"] == "tracked_by_task_evidence"

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

    owasp = controls["control.owasp_api_security_regression"]
    assert owasp["controlType"] == "owasp_api_regression"
    assert owasp["status"] == "available"
    assert "bash scripts/production-security-gate.sh" in owasp["localVerification"]

    privacy = controls["control.privacy_fixture_policy"]
    assert privacy["controlType"] == "privacy"
    assert "北京以外" in privacy["privacyBoundary"]
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
    assert "已填写（非北京地区已隐藏）" in markdown
    assert "上海市" not in markdown
