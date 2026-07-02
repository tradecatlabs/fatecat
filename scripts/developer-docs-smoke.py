#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import py_compile
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_OPENAPI_PATH = REPO_ROOT / "scripts" / "export-openapi.py"
SANDBOX_PATH = REPO_ROOT / "contracts" / "fate" / "developer" / "sandbox.json"
EXAMPLES_DIR = REPO_ROOT / "docs" / "reference-materials" / "developer" / "examples"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "docs-smoke.json"
DEFAULT_OPENAPI_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "openapi.json"
EXAMPLE_FILES = {
    "curl_sandbox": EXAMPLES_DIR / "curl-sandbox.sh",
    "python_client": EXAMPLES_DIR / "python-client.py",
    "node_client": EXAMPLES_DIR / "node-client.mjs",
    "agent_tool_call": EXAMPLES_DIR / "agent-tool-call.json",
}


class DeveloperDocsSmokeError(RuntimeError):
    """开发者文档 smoke 未满足预期。"""


def _load_export_openapi_module():
    spec = importlib.util.spec_from_file_location("fatecat_export_openapi", EXPORT_OPENAPI_PATH)
    if spec is None or spec.loader is None:
        raise DeveloperDocsSmokeError(f"cannot load {EXPORT_OPENAPI_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export_openapi = _load_export_openapi_module()


def _load_app():
    for path in (str(export_openapi.DELIVERY_SRC), str(export_openapi.FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from main import app  # noqa: PLC0415

    return app


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise DeveloperDocsSmokeError(f"{name}: {details}")


def _read_sandbox() -> dict[str, Any]:
    with SANDBOX_PATH.open(encoding="utf-8") as fh:
        sandbox = json.load(fh)
    if sandbox.get("schemaVersion") != 1:
        raise DeveloperDocsSmokeError("sandbox schemaVersion must be 1")
    fixtures = sandbox.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise DeveloperDocsSmokeError("sandbox fixtures must be a non-empty list")
    return sandbox


def _assert_expected_response(fixture: dict[str, Any], body: dict[str, Any]) -> None:
    expected = fixture["expected"]
    if body.get("success") is not expected.get("success"):
        raise DeveloperDocsSmokeError(f"{fixture['id']} success mismatch")
    if body.get("capabilityId") != expected.get("capabilityId"):
        raise DeveloperDocsSmokeError(f"{fixture['id']} top-level capabilityId mismatch")
    if body.get("reportProfile") != expected.get("reportProfile"):
        raise DeveloperDocsSmokeError(f"{fixture['id']} top-level reportProfile mismatch")

    data = body.get("data")
    if not isinstance(data, dict):
        raise DeveloperDocsSmokeError(f"{fixture['id']} data must be object")
    if data.get("capabilityId") != expected.get("capabilityId"):
        raise DeveloperDocsSmokeError(f"{fixture['id']} capabilityId mismatch")

    data_checks = expected.get("dataChecks") or {}
    if "dateRangeDays" in data_checks:
        date_range = data.get("dateRange", {})
        if date_range.get("days") != data_checks["dateRangeDays"]:
            raise DeveloperDocsSmokeError(f"{fixture['id']} dateRange.days mismatch")
    if "timeSlotCount" in data_checks:
        days = data.get("days", [])
        first_day = days[0] if days else {}
        if len(first_day.get("timeSlots", [])) != data_checks["timeSlotCount"]:
            raise DeveloperDocsSmokeError(f"{fixture['id']} time slot count mismatch")


def _run_sandbox_fixtures(client: TestClient, checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sandbox = _read_sandbox()
    _check("北京" in sandbox["privacyBoundary"], "sandbox_privacy_boundary", "北京-only boundary", checks)
    results = []
    for fixture in sandbox["fixtures"]:
        response = client.request(fixture["method"], fixture["endpoint"], json=fixture["request"])
        expected_status = fixture["expected"]["httpStatus"]
        _check(
            response.status_code == expected_status,
            f"sandbox_{fixture['id']}_status",
            f"status={response.status_code}",
            checks,
        )
        body = response.json()
        _assert_expected_response(fixture, body)
        results.append(
            {
                "id": fixture["id"],
                "capabilityId": fixture["capabilityId"],
                "status": "passed",
                "endpoint": fixture["endpoint"],
            }
        )
    return results


def _validate_examples(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for name, path in EXAMPLE_FILES.items():
        _check(path.exists(), f"example_{name}_exists", str(path), checks)
        results.append({"name": name, "path": str(path)})

    shell_result = subprocess.run(
        ["bash", "-n", str(EXAMPLE_FILES["curl_sandbox"])],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    _check(shell_result.returncode == 0, "example_curl_bash_syntax", shell_result.stderr or "ok", checks)

    py_compile.compile(str(EXAMPLE_FILES["python_client"]), doraise=True)
    _check(True, "example_python_compile", "ok", checks)

    with EXAMPLE_FILES["agent_tool_call"].open(encoding="utf-8") as fh:
        agent_call = json.load(fh)
    _check(agent_call.get("tool") == "fatecat.capabilities.calculate", "example_agent_tool_shape", "ok", checks)

    node_text = EXAMPLE_FILES["node_client"].read_text(encoding="utf-8")
    _check("fetch(" in node_text, "example_node_fetch_shape", "ok", checks)
    return results


def run_smoke(*, output_openapi: Path = DEFAULT_OPENAPI_JSON) -> dict[str, Any]:
    app = _load_app()
    client = TestClient(app)
    checks: list[dict[str, Any]] = []

    schema = client.get("/openapi.json").json()
    export_openapi.validate_openapi_schema(schema)
    output_openapi.parent.mkdir(parents=True, exist_ok=True)
    with output_openapi.open("w", encoding="utf-8") as fh:
        json.dump(schema, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    _check(True, "openapi_required_paths", f"required={len(export_openapi.REQUIRED_PATHS)}", checks)

    fixtures = _run_sandbox_fixtures(client, checks)
    examples = _validate_examples(checks)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "openapi": {
            "output": str(output_openapi),
            "version": schema.get("openapi"),
            "pathCount": len(schema.get("paths", {})),
            "requiredPathCount": len(export_openapi.REQUIRED_PATHS),
        },
        "fixtures": fixtures,
        "examples": examples,
        "checks": checks,
        "privacyBoundary": "developer docs smoke 只保存路径、检查名和状态；不得保存真实 token、secret、非北京真实地区、生产 URL、用户输入或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行开发者文档、OpenAPI 和 sandbox fixture smoke。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    parser.add_argument("--openapi-json", type=Path, default=DEFAULT_OPENAPI_JSON, help="OpenAPI JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke(output_openapi=args.openapi_json)
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "checks": len(summary["checks"])}, ensure_ascii=False))
        return 0
    except (DeveloperDocsSmokeError, export_openapi.OpenAPIExportError, py_compile.PyCompileError) as exc:
        print(f"developer docs smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
