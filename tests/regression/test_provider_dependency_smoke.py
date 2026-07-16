from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "provider-dependency-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_provider_dependency_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_provider_dependency_smoke_executes_available_capabilities(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "provider-dependency-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["smokeScope"] == "local_dependency_fixture_execution"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert stored["providerCount"] == 4
    assert {item["capabilityId"] for item in stored["providers"]} == {"almanac", "bazi", "meihua", "ziwei"}
    assert all(item["healthStatus"] == "ready" for item in stored["providers"])
    assert "token" in stored["privacyBoundary"]


def test_provider_dependency_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "provider-dependency-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
