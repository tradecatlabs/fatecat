from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

if str(DELIVERY_SRC) not in sys.path:
    sys.path.insert(0, str(DELIVERY_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

from calculation_service import calculate_delivery_result  # noqa: E402
from main import app  # noqa: E402
from web_forms import WebReportForm  # noqa: E402
from web_report_service import build_web_report_result  # noqa: E402


def _api_payload() -> dict:
    return {
        "name": "一致性样本",
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
            "reportSystem": "bazi",
        },
    }


def _sample_birth_dt() -> datetime:
    return datetime(1990, 1, 1, 8, 0, 0)


def test_api_bot_shared_service_and_web_bazi_canonical_fields_are_consistent():
    payload = _api_payload()

    api_response = TestClient(app).post("/api/v1/bazi/simple", json=payload)
    assert api_response.status_code == 200
    api_data = api_response.json()["data"]

    bot_path_calculation = calculate_delivery_result(
        birth_dt=_sample_birth_dt(),
        gender="male",
        longitude=116.4074,
        latitude=39.9042,
        birth_place="北京市",
        name="一致性样本",
        report_system="bazi",
        use_true_solar_time=True,
    )

    web_result = build_web_report_result(
        WebReportForm(
            birth_date="1990-01-01",
            birth_time="08:00",
            birth_place="北京市",
            location_mode="domestic",
            time_basis="beijing_time",
            gender="male",
            name="一致性样本",
            report_system="bazi",
            submitted="1",
        )
    )

    assert api_data["fourPillars"] == bot_path_calculation.data["fourPillars"]
    assert web_result.workbench["fourPillars"] == api_data["fourPillars"]
    assert api_data["inputTrace"]["useTrueSolarTime"] is True
    assert bot_path_calculation.data["inputTrace"]["useTrueSolarTime"] is True
    assert web_result.input_payload["useTrueSolarTime"] is True


def test_delivery_entrypoints_do_not_bypass_canonical_calculation_service():
    main_text = (DELIVERY_SRC / "main.py").read_text(encoding="utf-8")
    web_text = (DELIVERY_SRC / "web_report_service.py").read_text(encoding="utf-8")
    bot_text = (DELIVERY_SRC / "bot.py").read_text(encoding="utf-8")

    assert "from calculation_service import calculate_delivery_result" in main_text
    assert "from calculation_service import calculate_delivery_result" in web_text
    assert "from calculation_service import calculate_delivery_result" in bot_text
    assert "from bazi_calculator import BaziCalculator" not in main_text
    assert "from bazi_calculator import BaziCalculator" not in web_text
    assert "from bazi_calculator import BaziCalculator" not in bot_text
