#!/usr/bin/env python3
"""测试 FateCat CLI 的输入归一化与输出行为。"""

import json
import sys
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modules" / "fate_core" / "src"))

from fate_core.cli import _build_pure_analysis_input, _load_json_payload, _normalize_payload, main
from fate_core.support import get_branding_payload


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

    monkeypatch.setattr("fate_core.cli.calculate_pure_analysis", lambda payload: expected_result)

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
