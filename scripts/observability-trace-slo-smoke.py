#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
SLO_GATE_PATH = REPO_ROOT / "scripts" / "observability-slo-gate.py"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "observability" / "trace-slo-smoke.json"
)


class ObservabilityTraceSloSmokeError(RuntimeError):
    """本地 trace/SLO smoke 未满足预期。"""


def _load_slo_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_observability_slo_gate", SLO_GATE_PATH)
    if spec is None or spec.loader is None:
        raise ObservabilityTraceSloSmokeError(f"cannot load {SLO_GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_app():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import main  # noqa: PLC0415

    return main.app, logging.getLogger("main"), logging.getLogger("fate_core.observability")


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise ObservabilityTraceSloSmokeError(f"{name}: {details}")


def _payload() -> dict[str, Any]:
    return {
        "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
        "eventType": "出行",
        "place": "北京",
    }


def _bazi_payload() -> dict[str, Any]:
    return {
        "name": "测试用户",
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


def _span_events(log_text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in log_text.splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("event") == "trace_span":
            events.append(payload)
    return events


def run_smoke() -> dict[str, Any]:
    app, main_logger, trace_logger = _load_app()
    checks: list[dict[str, Any]] = []
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    previous_main_level = main_logger.level
    previous_trace_level = trace_logger.level
    main_logger.addHandler(handler)
    trace_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)
    trace_logger.setLevel(logging.INFO)

    try:
        client = TestClient(app)
        traceparent = "00-11111111111111111111111111111111-2222222222222222-01"
        response = client.post(
            "/capabilities/almanac/calculate",
            json=_payload(),
            headers={"X-Request-ID": "trace-slo-capability", "traceparent": traceparent},
        )
        _check(response.status_code == 200, "capability_status", str(response.status_code), checks)
        _check(
            response.headers.get("x-trace-id") == "11111111111111111111111111111111",
            "trace_id_propagated",
            str(response.headers.get("x-trace-id")),
            checks,
        )
        _check(response.headers.get("traceparent", "").startswith("00-111111"), "traceparent_header", "present", checks)

        report_response = client.post(
            "/api/v1/report/markdown",
            json=_bazi_payload(),
            headers={"X-Request-ID": "trace-slo-report"},
        )
        _check(report_response.status_code == 200, "report_status", str(report_response.status_code), checks)

        log_text = log_stream.getvalue()
        spans = _span_events(log_text)
        span_names = {item.get("spanName") for item in spans}
        for required in {
            "http.request",
            "capability.execute",
            "provider.validate",
            "provider.calculate",
            "report.calculate",
            "report.render_markdown",
        }:
            _check(required in span_names, f"span_{required}", str(sorted(span_names)), checks)

        _check('"traceId":"11111111111111111111111111111111"' in log_text, "log_trace_id", "trace id in logs", checks)
        _check("birthPlace" not in log_text, "no_birth_place_in_spans", "birthPlace absent", checks)
        _check("测试用户" not in log_text, "no_name_in_spans", "name absent", checks)
        spans_json = json.dumps(spans, ensure_ascii=False)
        _check("命理排盘报告" not in spans_json, "no_report_title_in_spans", "report title absent", checks)
        _check("第一卷" not in spans_json, "no_report_body_in_spans", "report body absent", checks)

        slo_gate = _load_slo_gate_module()
        gate_summary = slo_gate.run_gate()
        _check(gate_summary["status"] == "passed", "slo_gate_status", gate_summary["status"], checks)

        return {
            "schemaVersion": 1,
            "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "status": "passed",
            "spanCount": len(spans),
            "spanNames": sorted(str(item) for item in span_names if item),
            "sloObjectives": gate_summary["objectives"],
            "alertRules": gate_summary["alertRules"],
            "checks": checks,
            "externalConnectivity": "外部连通验证待执行",
            "privacyBoundary": "smoke 只捕获本地结构化 span 日志，验证 trace ID、span 名称、状态和 policy；不保存用户输入、报告正文、token、secret 或 DSN。",
        }
    finally:
        main_logger.removeHandler(handler)
        trace_logger.removeHandler(handler)
        main_logger.setLevel(previous_main_level)
        trace_logger.setLevel(previous_trace_level)


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 trace/SLO/alert smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "spans": summary["spanCount"],
                    "sloObjectives": summary["sloObjectives"],
                    "alertRules": summary["alertRules"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ObservabilityTraceSloSmokeError, OSError, json.JSONDecodeError) as exc:
        print(f"observability trace/slo smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
