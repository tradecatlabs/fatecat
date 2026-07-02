#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "webhook" / "smoke.json"


class WebhookSmokeError(RuntimeError):
    """本地 webhook smoke 未满足预期。"""


def _load_runtime():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from report_jobs import ReportJobManager  # noqa: PLC0415
    from webhook_callbacks import HttpWebhookDispatcher, WebhookConfig  # noqa: PLC0415

    return ReportJobManager, HttpWebhookDispatcher, WebhookConfig


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise WebhookSmokeError(f"{name}: {details}")


def run_smoke() -> dict[str, Any]:
    ReportJobManager, HttpWebhookDispatcher, WebhookConfig = _load_runtime()
    checks: list[dict[str, Any]] = []
    captured: dict[str, Any] = {}

    def capture_transport(url: str, body: bytes, headers: dict[str, str], timeout_seconds: int) -> int:
        captured["url"] = url
        captured["body"] = body.decode("utf-8")
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
        webhook_config=WebhookConfig(url="https://callback.example/webhook", secret="smoke-secret"),
        task=lambda: {"reportSystem": "bazi", "markdown": "# 命理排盘报告：测试样本"},
    )
    deadline = time.monotonic() + 4
    snapshot = None
    while time.monotonic() < deadline:
        snapshot = manager.get(created.job_id)
        if snapshot.status in {"succeeded", "failed", "cancelled", "expired"}:
            break
        time.sleep(0.05)
    if snapshot is None:
        raise WebhookSmokeError("job snapshot missing")

    body_text = str(captured.get("body", ""))
    headers = captured.get("headers") if isinstance(captured.get("headers"), dict) else {}
    _check(snapshot.status == "succeeded", "job_succeeded", f"status={snapshot.status}", checks)
    _check(captured.get("url") == "https://callback.example/webhook", "callback_url", str(captured.get("url")), checks)
    _check('"eventType":"report_job.terminal"' in body_text, "event_type", "report_job.terminal", checks)
    _check(f'"jobId":"{created.job_id}"' in body_text, "job_id", "present", checks)
    _check('"status":"succeeded"' in body_text, "terminal_status", "succeeded", checks)
    _check('"markdown":' not in body_text, "no_markdown_body", "report body field omitted", checks)
    _check("# 命理排盘报告" not in body_text, "no_report_text", "report text omitted", checks)
    _check("测试样本" not in body_text, "no_name", "user name omitted", checks)
    _check("北京" not in body_text, "no_birth_place", "birth place omitted", checks)
    _check(str(headers.get("X-FateCat-Webhook-Signature", "")).startswith("sha256="), "signature", "sha256", checks)
    _check("smoke-secret" not in json.dumps(captured, ensure_ascii=False), "no_secret_echo", "secret omitted", checks)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "privacyBoundary": "本地 smoke 使用可注入 transport，不访问公网；payload 不包含 Markdown 正文、姓名、出生地区或 webhook secret。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地 report job webhook smoke，并输出机器可读 JSON。")
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
    except WebhookSmokeError as exc:
        print(f"webhook smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
