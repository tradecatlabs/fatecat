from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from threading import BoundedSemaphore

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
from report_jobs import ReportJobQueueFull  # noqa: E402


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


def test_admin_token_can_read_any_record(monkeypatch):
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

    response = TestClient(app).get("/api/v1/records/1", headers={"Authorization": "Bearer admin-token"})

    assert response.status_code == 200
    assert response.json()["data"]["userId"] == "u2"


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


def test_markdown_report_api_selects_ziwei_without_bazi_blocks():
    payload = _payload()
    payload["options"]["reportSystem"] = "ziwei"

    response = TestClient(app).post("/api/v1/report/markdown", json=payload)

    assert response.status_code == 200
    body = response.json()
    markdown = body["data"]["markdown"]
    assert body["data"]["reportSystem"] == "ziwei"
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


def test_markdown_report_job_api_returns_status_then_result():
    client = TestClient(app)
    response = client.post("/api/v1/report/jobs", json=_payload())

    assert response.status_code == 202
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] in {"queued", "running"}
    assert body["data"]["jobId"]
    assert body["data"]["statusUrl"] == f"/api/v1/report/jobs/{body['data']['jobId']}"

    final_body = _wait_for_report_job(client, body["data"]["jobId"])
    assert final_body["data"]["status"] == "succeeded"
    assert final_body["data"]["result"]["reportSystem"] == "bazi"
    assert "# 命理排盘报告：测试样本" in final_body["data"]["result"]["markdown"]


def test_markdown_report_jobs_do_not_write_records(monkeypatch):
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


def test_measurement_infrastructure_metadata_and_reports_are_available():
    client = TestClient(app)
    metadata_response = client.get("/metadata")
    reports_response = client.get("/reports")

    assert metadata_response.status_code == 200
    metadata = metadata_response.json()["data"]
    assert metadata["service"] == "FateCat"
    assert metadata["positioning"] == "面向 Agent 与应用开发者的测算基础设施"
    assert metadata["capabilityProtocol"]["registryEndpoint"] == "/capabilities"
    assert metadata["developer"]["openapi"] == "/openapi.json"
    assert metadata["developer"]["capabilityCalculate"] == "/capabilities/{capability_id}/calculate"
    assert metadata["developer"]["apiGuide"] == "docs/reference-materials/operations/测算基础设施 API 接入.md"
    assert metadata["quality"]["health"] == "/health"
    assert metadata["quality"]["metrics"] == "/metrics"
    assert metadata["privacy"]["birthPlaceDisplayPolicy"] == "公开 Web 示例和用户界面不得展示北京以外的真实地区名称。"
    assert metadata["productionGate"]["externalConnectivity"] == "外部连通验证待执行"

    assert reports_response.status_code == 200
    reports = reports_response.json()["data"]
    assert reports["jobEndpoint"] == "/api/v1/report/jobs"
    assert reports["markdownEndpoint"] == "/api/v1/report/markdown"
    assert {item["id"] for item in reports["profiles"]} >= {"bazi", "ziwei", "meihua"}


def test_measurement_infrastructure_openapi_exposes_developer_entrypoints():
    response = TestClient(app).get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/metadata" in paths
    assert "/capabilities" in paths
    assert "/capabilities/{capability_id}/calculate" in paths
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
