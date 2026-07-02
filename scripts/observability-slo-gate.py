#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVABILITY_DIR = REPO_ROOT / "contracts" / "fate" / "observability"
DEFAULT_REGISTRY = OBSERVABILITY_DIR / "registry.json"
DEFAULT_SLO_POLICY = OBSERVABILITY_DIR / "slo-policy.json"
DEFAULT_ALERT_RULES = OBSERVABILITY_DIR / "alert-rules.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "observability" / "slo-gate.json"

REQUIRED_SLO_IDS = {"slo.availability", "slo.latency_p95", "slo.report_job_success", "slo.provider_success"}
REQUIRED_ALERT_IDS = {
    "alert.error_budget_burn",
    "alert.queue_depth",
    "alert.provider_outage",
    "alert.secret_scan_failure",
    "alert.evaluation_regression",
}
REQUIRED_TRACE_FIELDS = {"traceId", "spanId", "parentSpanId", "spanName", "durationMs", "status"}
REQUIRED_METRIC_SOURCES = {
    "fatecat_requests_total",
    "fatecat_request_errors_total",
    "fatecat_request_latency_seconds_bucket",
    "fatecat_report_jobs",
}


class ObservabilitySloGateError(RuntimeError):
    """观测 SLO/alert gate 未满足预期。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ObservabilitySloGateError(f"JSON 顶层必须是 object: {path}")
    return payload


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise ObservabilitySloGateError(f"{name}: {details}")


def run_gate(
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    slo_policy_path: Path = DEFAULT_SLO_POLICY,
    alert_rules_path: Path = DEFAULT_ALERT_RULES,
) -> dict[str, Any]:
    registry = load_json(registry_path)
    slo_policy = load_json(slo_policy_path)
    alert_rules = load_json(alert_rules_path)
    checks: list[dict[str, Any]] = []

    signals = {item["id"]: item for item in registry.get("signals", [])}
    _check("signal.provider_report_traces" in signals, "registry_trace_signal", "present", checks)
    _check("signal.slo_and_alerts" in signals, "registry_slo_signal", "present", checks)

    trace_signal = signals["signal.provider_report_traces"]
    slo_signal = signals["signal.slo_and_alerts"]
    _check(trace_signal["status"] == "available", "trace_signal_available", trace_signal["status"], checks)
    _check(slo_signal["status"] == "available", "slo_signal_available", slo_signal["status"], checks)
    _check(
        REQUIRED_TRACE_FIELDS <= set(trace_signal.get("fields", [])),
        "trace_fields",
        str(sorted(REQUIRED_TRACE_FIELDS - set(trace_signal.get("fields", [])))),
        checks,
    )
    _check(bool(trace_signal.get("localVerification")), "trace_local_verification", "non-empty", checks)
    _check(bool(slo_signal.get("localVerification")), "slo_local_verification", "non-empty", checks)

    objectives = {item["id"]: item for item in slo_policy.get("objectives", [])}
    _check(
        REQUIRED_SLO_IDS <= set(objectives), "required_slo_ids", str(sorted(REQUIRED_SLO_IDS - set(objectives))), checks
    )
    for slo_id, item in sorted(objectives.items()):
        _check(item.get("releaseGate") == "required", f"{slo_id}:release_gate", str(item.get("releaseGate")), checks)
        metric_source = str(item.get("metricSource") or "")
        if metric_source.startswith("fatecat_"):
            _check(metric_source in REQUIRED_METRIC_SOURCES, f"{slo_id}:metric_source", metric_source, checks)

    rules = {item["id"]: item for item in alert_rules.get("rules", [])}
    _check(
        REQUIRED_ALERT_IDS <= set(rules),
        "required_alert_ids",
        str(sorted(REQUIRED_ALERT_IDS - set(rules))),
        checks,
    )
    for rule_id, item in sorted(rules.items()):
        _check(
            item.get("severity") in {"critical", "warning"}, f"{rule_id}:severity", str(item.get("severity")), checks
        )
        _check(bool(item.get("condition")), f"{rule_id}:condition", "present", checks)
        _check(bool(item.get("runbook")), f"{rule_id}:runbook", "present", checks)
        _check(bool(item.get("signals")), f"{rule_id}:signals", "present", checks)

    privacy_text = " ".join(
        [
            str(registry.get("metadata", {}).get("defaultResponseRule", "")),
            str(slo_policy.get("privacyBoundary", "")),
            str(alert_rules.get("privacyBoundary", "")),
            str(trace_signal.get("privacyBoundary", "")),
            str(slo_signal.get("privacyBoundary", "")),
        ]
    )
    for forbidden in ("token", "secret", "DSN", "报告正文"):
        _check(forbidden in privacy_text, f"privacy_mentions_{forbidden}", "mentioned", checks)

    return {
        "schemaVersion": 1,
        "generatedAt": utc_now(),
        "status": "passed",
        "signals": len(signals),
        "objectives": len(objectives),
        "alertRules": len(rules),
        "checks": checks,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "gate 只读取 registry、SLO policy 和 alert rules，不读取真实日志、指标快照、用户输入、token、secret、DSN 或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验本地 observability trace/SLO/alert policy baseline。")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="observability registry JSON。")
    parser.add_argument("--slo-policy", type=Path, default=DEFAULT_SLO_POLICY, help="SLO policy JSON。")
    parser.add_argument("--alert-rules", type=Path, default=DEFAULT_ALERT_RULES, help="alert rules JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            registry_path=args.registry, slo_policy_path=args.slo_policy, alert_rules_path=args.alert_rules
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "objectives": summary["objectives"],
                    "alertRules": summary["alertRules"],
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ObservabilitySloGateError, OSError, json.JSONDecodeError) as exc:
        print(f"observability slo gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
