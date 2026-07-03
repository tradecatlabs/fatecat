from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREND_GATE_PATH = ROOT / "scripts" / "provider-drift-trend-gate.py"
SCANNER_PATH = ROOT / "scripts" / "provider-drift-scanner.py"
BASELINE_PATH = ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-baseline.json"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-trend-contract.json"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _current_drift_report() -> dict:
    scanner = _load_module(SCANNER_PATH, "fatecat_provider_drift_scanner_for_trend_tests")
    return scanner.run_scanner()


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def test_provider_drift_trend_gate_passes_current_baseline(tmp_path):
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate")
    output_json = tmp_path / "provider-drift-trend.json"

    exit_code = trend.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["kind"] == "fatecat.provider_drift_trend_report"
    assert stored["status"] == "passed"
    assert stored["baseline"]["baselineId"] == "provider-source-license-baseline-2026-07-03"
    assert stored["current"]["providerCount"] == 4
    assert stored["current"]["scannerFindingCount"] == 0
    assert stored["findingCount"] == 0
    assert {row["status"] for row in stored["providerTrend"]} == {"passed"}


def test_provider_drift_baseline_fingerprints_are_reproducible():
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate_repro")
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    provider_schema = json.loads(
        (ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "provider.schema.json").read_text(encoding="utf-8")
    )

    assert contract["baselineKind"] == baseline["kind"]
    assert "provider-drift-baseline.json" in contract["baselinePath"]
    assert "provider drift trend gate" in " ".join(provider_schema["invariants"])
    for provider in baseline["providers"]:
        normalized = trend._provider_snapshot(provider)
        assert normalized["fingerprints"] == provider["fingerprints"]


def test_provider_drift_trend_rejects_missing_provider_baseline(tmp_path):
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate_missing_provider")
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    baseline["providers"] = baseline["providers"][:-1]
    baseline["providerCount"] = len(baseline["providers"])
    baseline_path = _write_json(tmp_path / "baseline-missing-provider.json", baseline)
    report_path = _write_json(tmp_path / "drift-report.json", _current_drift_report())

    summary = trend.run_gate(baseline_path=baseline_path, scanner_report_path=report_path)

    assert summary["status"] == "failed"
    assert any(item["name"] == "provider_set_matches_baseline" for item in summary["findings"])


def test_provider_drift_trend_rejects_license_regression(tmp_path):
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate_license")
    report = _current_drift_report()
    report["providers"][0]["license"]["productionUseAllowed"] = False
    report_path = _write_json(tmp_path / "drift-report-license-regression.json", report)

    summary = trend.run_gate(scanner_report_path=report_path)

    assert summary["status"] == "failed"
    finding_names = {item["name"] for item in summary["findings"]}
    assert any(name.endswith(":license_production_allowed") for name in finding_names)
    assert any(name.endswith(":fingerprint:licenseFingerprint") for name in finding_names)


def test_provider_drift_trend_rejects_vendor_hash_drift(tmp_path):
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate_vendor")
    report = _current_drift_report()
    for provider in report["providers"]:
        if provider["supplyChain"]:
            provider["supplyChain"][0]["snapshotSha256"] = "0" * 64
            break
    report_path = _write_json(tmp_path / "drift-report-vendor-drift.json", report)

    summary = trend.run_gate(scanner_report_path=report_path)

    assert summary["status"] == "failed"
    assert any(item["name"].endswith(":fingerprint:vendorFingerprint") for item in summary["findings"])


def test_provider_drift_trend_rejects_failed_scanner_report(tmp_path):
    trend = _load_module(TREND_GATE_PATH, "fatecat_provider_drift_trend_gate_scanner_failed")
    report = _current_drift_report()
    report["status"] = "failed"
    report["findingCount"] = 1
    report["findings"] = [{"severity": "block", "name": "synthetic", "details": "test"}]
    report_path = _write_json(tmp_path / "drift-report-failed.json", report)

    summary = trend.run_gate(scanner_report_path=report_path)

    assert summary["status"] == "failed"
    assert any(item["name"] == "scanner_report_passed" for item in summary["findings"])


def test_provider_drift_trend_gate_is_wired_into_local_ci_and_docs():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    contracts_agents = (ROOT / "contracts" / "fate" / "capabilities" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")

    assert "provider-drift-trend-gate.sh" in local_ci
    assert "--scanner-report-json" in local_ci
    assert "provider-drift-trend-gate.py" in scripts_agents
    assert "provider-drift-baseline.json" in contracts_agents
    assert "test_provider_drift_trend_gate.py" in tests_agents
