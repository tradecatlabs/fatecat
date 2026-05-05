from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
TELEGRAM_SRC = ROOT / "modules" / "telegram" / "src"
FATE_CORE_SRC = ROOT / "modules" / "fate_core" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

from main import app  # noqa: E402


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


def test_pure_analysis_api_returns_success():
    response = TestClient(app).post("/api/v1/bazi/pure-analysis", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["input"]["gender"] == "男"
    assert body["data"]["meta"]["genderCn"] == "乾造(男)"


def test_calculate_api_returns_success_with_record_id(monkeypatch):
    saved = {}

    def fake_save_record(**kwargs):
        saved.update(kwargs)
        return 42

    monkeypatch.setattr("main.db.save_record", fake_save_record)

    response = TestClient(app).post("/api/v1/bazi/calculate?user_id=u1", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["meta"]["recordId"] == 42
    assert saved["gender"] == "male"
    assert saved["birth_place"] == "北京市"
