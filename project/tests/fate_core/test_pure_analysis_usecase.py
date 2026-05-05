import importlib
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "modules" / "fate_core" / "src"))

from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis  # noqa: E402

pure_analysis_module = importlib.import_module("fate_core.usecases.calculate_pure_analysis")


def test_calculate_pure_analysis_projects_profile(monkeypatch):
    captured_payload = {}

    class FakeCalculator:
        def _translate_to_chinese(self, value):
            return value

        def _json_safe(self, value):
            return value

    def fake_build_runtime(payload):
        captured_payload["gender"] = payload.gender

        class Runtime:
            calculator = FakeCalculator()

        return Runtime()

    def fake_build_base(_runtime):
        return {
            "input": {"name": "测试"},
            "meta": {"calculateTime": "2026-04-14 00:00:00"},
            "fourPillars": {"day": {"fullName": "甲子"}},
        }

    def fake_build_fortune(_runtime):
        return {
            "majorFortune": {"pillars": []},
        }

    def fake_build_classical(_runtime):
        return {
            "yongShen": {"note": "测试"},
            "ziweiChart": {"should": "drop"},
            "liuyaoHexagram": {"should": "drop"},
        }

    monkeypatch.setattr(pure_analysis_module, "build_pure_analysis_runtime", fake_build_runtime)
    monkeypatch.setattr(pure_analysis_module, "build_base_chart_section", fake_build_base)
    monkeypatch.setattr(pure_analysis_module, "build_fortune_section", fake_build_fortune)
    monkeypatch.setattr(pure_analysis_module, "build_classical_section", fake_build_classical)

    result = calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime(1990, 5, 15, 14, 30, 0),
            gender="男",
            longitude=113.93,
            latitude=22.54,
            name="测试",
            birth_place="深圳南山",
        )
    )

    assert result["input"]["name"] == "测试"
    assert captured_payload["gender"] == "male"
    assert "fourPillars" in result
    assert "majorFortune" in result
    assert "yongShen" in result
    assert "ziweiChart" not in result
    assert "liuyaoHexagram" not in result
