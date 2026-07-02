from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_OPENAPI_PATH = ROOT / "scripts" / "export-openapi.py"
DEVELOPER_DOCS_SMOKE_PATH = ROOT / "scripts" / "developer-docs-smoke.py"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_export_openapi_writes_required_schema(tmp_path):
    exporter = _load_module("fatecat_export_openapi_test", EXPORT_OPENAPI_PATH)
    output = tmp_path / "openapi.json"

    summary = exporter.export_openapi(output)
    schema = json.loads(output.read_text(encoding="utf-8"))

    assert summary["status"] == "passed"
    assert schema["openapi"].startswith("3.")
    assert set(exporter.REQUIRED_PATHS).issubset(schema["paths"])
    assert summary["pathCount"] == len(schema["paths"])


def test_developer_docs_smoke_executes_sandbox_and_examples(tmp_path):
    smoke = _load_module("fatecat_developer_docs_smoke_test", DEVELOPER_DOCS_SMOKE_PATH)
    output_json = tmp_path / "docs-smoke.json"
    openapi_json = tmp_path / "openapi.json"

    summary = smoke.run_smoke(output_openapi=openapi_json)
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["status"] == "passed"
    assert openapi_json.exists()
    assert {item["capabilityId"] for item in stored["fixtures"]} == {"almanac", "meihua"}
    assert {item["name"] for item in stored["examples"]} == {
        "agent_tool_call",
        "curl_sandbox",
        "node_client",
        "python_client",
    }
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["openapi_required_paths"]["ok"] is True
    assert checks["example_curl_bash_syntax"]["ok"] is True
    assert checks["example_python_compile"]["ok"] is True
    assert "token" in stored["privacyBoundary"]
