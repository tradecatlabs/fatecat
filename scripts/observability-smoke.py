#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "observability" / "smoke.json"
REQUIRED_METRICS = [
    "fatecat_requests_total",
    "fatecat_request_latency_seconds_bucket",
    "fatecat_request_errors_total",
    "fatecat_inflight_requests",
    "fatecat_report_job_queue_size",
    "fatecat_report_job_store_backend_info",
    "fatecat_bot_queue_size",
]


class ObservabilitySmokeError(RuntimeError):
    """本地观测 smoke 未满足预期。"""


def _load_app():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import main  # noqa: PLC0415

    return main.app, logging.getLogger("main")


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise ObservabilitySmokeError(f"{name}: {details}")


def run_smoke() -> dict[str, Any]:
    app, logger = _load_app()
    checks: list[dict[str, Any]] = []
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    previous_level = logger.level
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    try:
        client = TestClient(app)

        health = client.get("/health", headers={"X-Request-ID": "obs-smoke-health"})
        _check(health.status_code == 200, "health_status", f"status={health.status_code}", checks)
        _check(
            health.headers.get("x-request-id") == "obs-smoke-health",
            "health_request_id",
            f"x-request-id={health.headers.get('x-request-id')}",
            checks,
        )

        ready = client.get("/ready", headers={"X-Request-ID": "obs-smoke-ready"})
        ready_body = ready.json()
        _check(ready.status_code == 200, "ready_status", f"status={ready.status_code}", checks)
        _check(ready_body.get("status") == "ready", "ready_body", f"body.status={ready_body.get('status')}", checks)

        metrics = client.get("/metrics", headers={"X-Request-ID": "obs-smoke-metrics"})
        metrics_text = metrics.text
        _check(metrics.status_code == 200, "metrics_status", f"status={metrics.status_code}", checks)
        for metric_name in REQUIRED_METRICS:
            _check(metric_name in metrics_text, f"metric_{metric_name}", "present", checks)

        registry = client.get("/observability", headers={"X-Request-ID": "obs-smoke-registry"})
        registry_data = registry.json()["data"]
        _check(registry.status_code == 200, "registry_status", f"status={registry.status_code}", checks)
        _check(
            registry_data["metadata"]["smokeCommand"] == "bash scripts/observability-smoke.sh",
            "registry_smoke_command",
            registry_data["metadata"].get("smokeCommand", ""),
            checks,
        )

        log_text = log_stream.getvalue()
        _check('"event":"http_request"' in log_text, "structured_http_request_log", "http_request log emitted", checks)
        _check("obs-smoke-health" in log_text, "structured_log_request_id", "request id propagated to logs", checks)
        _check('"traceId":"' in log_text, "structured_log_trace_id", "trace id propagated to logs", checks)

        return {
            "schemaVersion": 1,
            "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "status": "passed",
            "checks": checks,
            "privacyBoundary": "smoke 只验证端点、指标名、request-id 和结构化日志字段，不保存用户输入、报告正文、token、secret 或 DSN。",
        }
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 Observability smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
        return 0
    except ObservabilitySmokeError as exc:
        print(f"observability smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
