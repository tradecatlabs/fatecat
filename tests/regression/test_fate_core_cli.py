#!/usr/bin/env python3
"""测试 FateCat CLI 的输入归一化与输出行为。"""

import json
import sys
from io import StringIO
from types import SimpleNamespace

import fate_core.cli as fate_cli
from fate_core.cli import _build_pure_analysis_input, _load_json_payload, _normalize_payload, main
from fate_core.support import get_branding_payload
from fate_core.usecases.calculate_pure_analysis import parse_datetime


def test_normalize_payload_supports_api_request_shape():
    payload = {
        "birthDate": "1990-01-01",
        "birthTime": "08:00:00",
        "gender": "男",
        "birthPlace": {
            "name": "北京市",
            "longitude": 116.4074,
            "latitude": 39.9042,
        },
        "options": {
            "useTrueSolarTime": False,
        },
    }

    normalized = _normalize_payload(payload)

    assert normalized["birthDateTime"] == "1990-01-01 08:00:00"
    assert normalized["birthPlace"] == "北京市"
    assert normalized["longitude"] == 116.4074
    assert normalized["latitude"] == 39.9042
    assert normalized["useTrueSolarTime"] is False


def test_build_pure_analysis_input_accepts_flat_aliases():
    pure_input = _build_pure_analysis_input(
        {
            "birth_datetime": "1990-01-01T08:00:00",
            "sex": "女",
            "lng": 121.4737,
            "lat": 31.2304,
            "birth_place": "上海市",
            "use_true_solar_time": True,
        }
    )

    assert pure_input.birth_dt.isoformat() == "1990-01-01T08:00:00"
    assert pure_input.gender == "female"
    assert pure_input.longitude == 121.4737
    assert pure_input.latitude == 31.2304
    assert pure_input.birth_place == "上海市"
    assert pure_input.use_true_solar_time is True


def test_parse_datetime_converts_aware_input_to_default_local_time():
    assert parse_datetime("1990-01-01T00:00:00Z").isoformat() == "1990-01-01T08:00:00"
    assert parse_datetime("1990-01-01T08:00:00+08:00").isoformat() == "1990-01-01T08:00:00"


def test_parse_datetime_respects_explicit_target_timezone():
    assert parse_datetime("1990-01-01T00:00:00Z", target_timezone="UTC").isoformat() == "1990-01-01T00:00:00"
    assert parse_datetime("1990-01-01T00:00:00Z", target_timezone="Asia/Hong_Kong").isoformat() == "1990-01-01T08:00:00"


def test_build_pure_analysis_input_uses_birth_place_timezone_for_aware_input():
    pure_input = _build_pure_analysis_input(
        {
            "birthDateTime": "1990-01-01T00:00:00Z",
            "gender": "男",
            "birthPlace": {
                "name": "UTC测试地",
                "longitude": 0,
                "latitude": 0,
                "timezone": "UTC",
            },
        }
    )

    assert pure_input.birth_dt.isoformat() == "1990-01-01T00:00:00"


def test_build_pure_analysis_input_normalizes_chinese_gender():
    pure_input = _build_pure_analysis_input(
        {
            "birthDateTime": "1990-01-01 08:00:00",
            "gender": "男",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "birthPlace": "北京市",
        }
    )

    assert pure_input.gender == "male"


def test_load_json_payload_ignores_empty_non_tty_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", StringIO(""))

    payload = _load_json_payload(
        SimpleNamespace(
            input_json=None,
            input_file=None,
            birth_datetime="1990-01-01 08:00:00",
            gender="男",
            longitude=116.4074,
            latitude=39.9042,
            name="测试样本",
            birth_place="北京市",
            use_true_solar_time=True,
        )
    )

    assert payload["birthDateTime"] == "1990-01-01 08:00:00"
    assert payload["gender"] == "男"


def test_main_pure_analysis_reads_inline_json(monkeypatch, capsys):
    expected_result = {"fourPillars": {"day": {"stem": "甲"}}}

    monkeypatch.setattr(fate_cli, "calculate_pure_analysis", lambda payload: expected_result)

    exit_code = main(
        [
            "pure-analysis",
            "--input-json",
            json.dumps(
                {
                    "birthDateTime": "1990-01-01 08:00:00",
                    "gender": "男",
                    "longitude": 116.4074,
                    "latitude": 39.9042,
                    "birthPlace": "北京市",
                },
                ensure_ascii=False,
            ),
        ]
    )

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert next(iter(result)) == "disclaimer"
    assert "本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。" in result["disclaimer"]
    assert result["success"] is True
    assert result["profile"] == "pure_analysis"
    assert result["data"] == expected_result
    assert result["branding"] == get_branding_payload()


def test_main_capabilities_lists_registry(capsys):
    exit_code = main(["capabilities"])

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result["success"] is True
    assert result["runtime"]["distributionMode"] == "enterprise_repo"
    assert result["runtime"]["providerAssetsAvailable"] is True
    capability_ids = {item["capabilityId"] for item in result["capabilities"]}
    assert "bazi" in capability_ids
    assert "liuyao" in capability_ids
    assert next(item for item in result["capabilities"] if item["capabilityId"] == "bazi")["status"] == "production"
    assert next(item for item in result["capabilities"] if item["capabilityId"] == "almanac")["status"] == "production"
    assert next(item for item in result["capabilities"] if item["capabilityId"] == "ziwei")["status"] == "production"
    assert next(item for item in result["capabilities"] if item["capabilityId"] == "meihua")["status"] == "production"


def test_main_capability_rejects_planned_system(capsys):
    exit_code = main(
        [
            "capability",
            "liuyao",
            "--input-json",
            json.dumps(
                {
                    "question": "测试问题",
                    "castMethod": "time",
                    "castTime": "2026-05-08 08:00:00",
                },
                ensure_ascii=False,
            ),
        ]
    )

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 1
    assert result["success"] is False
    assert "尚未生产化" in result["error"]


def test_main_capability_executes_bazi_via_executor(monkeypatch, capsys):
    class FakeExecutor:
        def execute(self, request):
            return type(
                "Result",
                (),
                {
                    "capability_id": request.capability_id,
                    "status": "production",
                    "report_profile": "bazi",
                    "data": {"ok": True},
                    "evidence": {"items": {}},
                    "risk": {"disclaimerRequired": True},
                },
            )()

    monkeypatch.setattr(fate_cli, "CapabilityExecutor", FakeExecutor)
    exit_code = main(
        [
            "capability",
            "bazi",
            "--input-json",
            json.dumps(
                {
                    "birthDateTime": "1990-01-01 08:00:00",
                    "gender": "男",
                    "longitude": 116.4074,
                    "latitude": 39.9042,
                    "birthPlace": "北京",
                },
                ensure_ascii=False,
            ),
        ]
    )

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result["success"] is True
    assert result["capabilityId"] == "bazi"
    assert result["reportProfile"] == "bazi"
    assert result["data"] == {"ok": True}


def test_main_capability_executes_almanac(capsys):
    exit_code = main(
        [
            "capability",
            "almanac",
            "--input-json",
            json.dumps(
                {
                    "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
                    "eventType": "出行",
                    "place": "北京",
                },
                ensure_ascii=False,
            ),
        ]
    )

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result["success"] is True
    assert result["capabilityId"] == "almanac"
    assert result["reportProfile"] == "almanac"
    assert result["data"]["dateRange"]["days"] == 1
    assert result["evidence"]["source"] == "lunar-python"


def test_main_capability_executes_meihua(capsys):
    exit_code = main(
        [
            "capability",
            "meihua",
            "--input-json",
            json.dumps(
                {
                    "question": "测试问题能否推进",
                    "castMethod": "number",
                    "castValue": "3,8,6",
                },
                ensure_ascii=False,
            ),
        ]
    )

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result["success"] is True
    assert result["capabilityId"] == "meihua"
    assert result["reportProfile"] == "meihua"
    assert result["data"]["hexagrams"]["movingLine"] == 5
