from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNER_PATH = ROOT / "scripts" / "provider-drift-scanner.py"


def _load_scanner_module():
    spec = importlib.util.spec_from_file_location("fatecat_provider_drift_scanner", SCANNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_provider_drift_scanner_generates_drift_report(tmp_path):
    scanner = _load_scanner_module()
    output_json = tmp_path / "provider-drift-report.json"

    summary = scanner.run_scanner()
    scanner.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.provider_drift_report"
    assert stored["status"] == "passed"
    assert stored["providerCount"] == 4
    assert stored["capabilityCount"] == 4
    assert stored["findingCount"] == 0
    assert stored["spanCount"] >= 12
    assert {item["providerId"] for item in stored["providers"]} == {
        "fate_core.usecases.calculate_almanac",
        "fate_core.usecases.calculate_meihua",
        "fate_core.usecases.calculate_pure_analysis",
        "fate_core.usecases.calculate_ziwei",
    }
    for provider in stored["providers"]:
        assert provider["driftStatus"] == "passed"
        for trace_summary in provider["traceSpans"].values():
            assert trace_summary["hasValidate"] is True
            assert trace_summary["hasCalculate"] is True
        assert provider["license"]["productionUseAllowed"] is True


def test_provider_drift_scanner_cli_writes_summary(tmp_path):
    scanner = _load_scanner_module()
    output_json = tmp_path / "provider-drift-report-cli.json"

    exit_code = scanner.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["findingCount"] == 0


def test_provider_drift_contract_is_enforced_by_scanner():
    contract = json.loads(
        (ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-contract.json").read_text(encoding="utf-8")
    )

    assert contract["reportKind"] == "fatecat.provider_drift_report"
    assert {"provider.validate", "provider.calculate"} <= set(contract["requiredTraceSpanNames"])
    assert "contracts/fate/observability/registry.json" in contract["requiredLocalSources"]
