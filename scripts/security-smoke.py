#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "security" / "smoke.json"
FILE_GATES = [
    ["bash", "scripts/check-privacy-fixtures.sh"],
    ["bash", "scripts/check-source-hygiene.sh"],
    ["bash", "scripts/check-public-release-policy.sh"],
]


class SecuritySmokeError(RuntimeError):
    """本地安全 smoke 未满足预期。"""


@contextmanager
def temporary_attr(obj, name: str, value):
    old_value = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old_value)


@contextmanager
def temporary_env(values: dict[str, str | None]):
    old_values = {key: os.environ.get(key) for key in values}
    for key, value in values.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    try:
        yield
    finally:
        for key, value in old_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _load_main():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import main  # noqa: PLC0415

    return main


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise SecuritySmokeError(f"{name}: {details}")


def _run_file_gates(checks: list[dict[str, Any]]) -> None:
    for command in FILE_GATES:
        result = subprocess.run(command, cwd=REPO_ROOT, check=False, capture_output=True, text=True, timeout=120)
        name = "file_gate_" + Path(command[1]).stem.replace("-", "_")
        _check(
            result.returncode == 0,
            name,
            (result.stdout + result.stderr)[-1000:] or f"exitCode={result.returncode}",
            checks,
        )


def run_smoke(*, run_file_gates: bool = True) -> dict[str, Any]:
    main = _load_main()
    checks: list[dict[str, Any]] = []
    client = TestClient(main.app)

    health = client.get("/health", headers={"X-Request-ID": "security-smoke-health"})
    _check(health.status_code == 200, "health_status", f"status={health.status_code}", checks)
    _check(
        health.headers.get("x-content-type-options") == "nosniff",
        "header_nosniff",
        health.headers.get("x-content-type-options", ""),
        checks,
    )
    _check(
        health.headers.get("x-frame-options") == "DENY",
        "header_frame_options",
        health.headers.get("x-frame-options", ""),
        checks,
    )
    _check(
        health.headers.get("referrer-policy") == "no-referrer",
        "header_referrer_policy",
        health.headers.get("referrer-policy", ""),
        checks,
    )
    _check(
        "frame-ancestors 'none'" in health.headers.get("content-security-policy", ""), "header_csp", "present", checks
    )
    _check(
        health.headers.get("x-request-id") == "security-smoke-health",
        "header_request_id",
        health.headers.get("x-request-id", ""),
        checks,
    )

    with temporary_attr(main, "MAX_REQUEST_BYTES", 32):
        too_large = client.post("/api/v1/bazi/pure-analysis", json={"name": "oversized-body-for-security-smoke"})
    _check(too_large.status_code == 413, "request_body_limit", f"status={too_large.status_code}", checks)

    with temporary_attr(main, "RATE_LIMIT_PER_MINUTE", 1):
        main._rate_limit_windows.clear()
        first = client.get("/api/v1/report/systems")
        second = client.get("/api/v1/report/systems")
        main._rate_limit_windows.clear()
    _check(first.status_code == 200, "rate_limit_first_request", f"status={first.status_code}", checks)
    _check(second.status_code == 429, "rate_limit_rejects_second_request", f"status={second.status_code}", checks)
    _check(second.headers.get("retry-after") is not None, "rate_limit_retry_after", "present", checks)

    with temporary_env({"FATE_RECORDS_ENABLED": "false"}), temporary_attr(main, "API_TOKEN", "admin-token"):
        disabled_records = client.get("/api/v1/records/1", headers={"X-FateCat-API-Key": "admin-token"})
    _check(
        disabled_records.status_code == 403, "records_can_be_disabled", f"status={disabled_records.status_code}", checks
    )
    _check("记录接口未启用" in disabled_records.text, "records_disabled_error", "present", checks)

    original_get_record = main.db.get_record
    try:
        main.db.get_record = lambda _record_id: {
            "id": 1,
            "userId": "u2",
            "bizType": "bazi",
            "input": {},
            "bizData": {},
            "createdAt": "2026-05-06T00:00:00+08:00",
        }
        with (
            temporary_env({"FATE_RECORDS_ENABLED": "true", "FATE_API_USER_TOKENS": "u1:user-token"}),
            temporary_attr(main, "API_TOKEN", ""),
        ):
            forbidden = client.get("/api/v1/records/1", headers={"X-FateCat-API-Key": "user-token"})
        _check(forbidden.status_code == 403, "user_token_owner_boundary", f"status={forbidden.status_code}", checks)
        _check("无权访问该记录" in forbidden.text, "user_token_owner_error", "present", checks)
    finally:
        main.db.get_record = original_get_record

    registry = client.get("/security", headers={"X-Request-ID": "security-smoke-registry"})
    registry_data = registry.json()["data"]
    _check(registry.status_code == 200, "security_registry_status", f"status={registry.status_code}", checks)
    _check(
        registry_data["metadata"]["smokeCommand"] == "bash scripts/security-smoke.sh",
        "security_registry_smoke_command",
        registry_data["metadata"].get("smokeCommand", ""),
        checks,
    )

    if run_file_gates:
        _run_file_gates(checks)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "fileGates": run_file_gates,
        "privacyBoundary": "smoke 只保存检查名、状态和摘要；不得输出真实 token、secret、DSN、请求体、用户输入或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行本地安全、隐私与发布门禁 smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    parser.add_argument("--skip-file-gates", action="store_true", help="跳过 privacy/source/public-release 文件门禁。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke(run_file_gates=not args.skip_file_gates)
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
        return 0
    except SecuritySmokeError as exc:
        print(f"security smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
