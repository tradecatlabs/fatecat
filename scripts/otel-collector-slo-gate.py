#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVABILITY_DIR = REPO_ROOT / "contracts" / "fate" / "observability"
DEFAULT_REGISTRY = OBSERVABILITY_DIR / "registry.json"
DEFAULT_SCHEMA = OBSERVABILITY_DIR / "schemas" / "observability-signal.schema.json"
DEFAULT_COLLECTOR_CONFIG = OBSERVABILITY_DIR / "otel-collector.dry-run.yaml"
DEFAULT_SLO_EVIDENCE = OBSERVABILITY_DIR / "slo-evidence-contract.json"
DEFAULT_SLO_POLICY = OBSERVABILITY_DIR / "slo-policy.json"
DEFAULT_ALERT_RULES = OBSERVABILITY_DIR / "alert-rules.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "observability" / "otel-collector-slo-gate.json"
)
SLO_GATE_PATH = REPO_ROOT / "scripts" / "observability-slo-gate.py"

REQUIRED_RECEIVERS = {"otlp"}
REQUIRED_PROCESSORS = {"memory_limiter", "batch", "resource"}
REQUIRED_EXPORTERS = {"debug", "prometheus"}
REQUIRED_PIPELINES = {"traces", "metrics", "logs"}
REQUIRED_DRY_RUN_CHECKS = {"collector_config_parse", "local_trace_slo_smoke", "slo_policy_gate"}
REQUIRED_LIVE_EVIDENCE = {
    "collector_runtime",
    "trace_backend",
    "metrics_backend",
    "alert_platform",
    "error_budget",
}
SENSITIVE_CONFIG_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"https?://",
        r"authorization",
        r"api[_-]?key",
        r"token",
        r"secret",
        r"password",
        r"passwd",
        r"dsn",
        r"database_url",
        r"begin rsa",
        r"begin openssh",
    )
]


class OTelCollectorSloGateError(RuntimeError):
    """OTel collector/SLO adapter contract gate 未满足预期。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise OTelCollectorSloGateError(f"JSON 顶层必须是 object: {path}")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = yaml.safe_load(fh)
    if not isinstance(payload, dict):
        raise OTelCollectorSloGateError(f"YAML 顶层必须是 object: {path}")
    return payload


def _load_slo_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_observability_slo_gate_for_otel", SLO_GATE_PATH)
    if spec is None or spec.loader is None:
        raise OTelCollectorSloGateError(f"cannot load {SLO_GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise OTelCollectorSloGateError(f"{name}: {details}")


def _as_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OTelCollectorSloGateError(f"{label} 必须是 object")
    return value


def _as_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise OTelCollectorSloGateError(f"{label} 必须是 list")
    return value


def _scan_config_text(config: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    runtime_config = {key: value for key, value in config.items() if key != "fatecat"}
    text = yaml.safe_dump(runtime_config, allow_unicode=True, sort_keys=True)
    for pattern in SENSITIVE_CONFIG_PATTERNS:
        match = pattern.search(text)
        _check(match is None, f"collector_config_no_{pattern.pattern}", "absent", checks)


def _validate_collector_config(config: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    _check(config.get("mode") == "dry-run-contract", "collector_mode", str(config.get("mode")), checks)
    _scan_config_text(config, checks)

    receivers = _as_dict(config.get("receivers"), "receivers")
    processors = _as_dict(config.get("processors"), "processors")
    exporters = _as_dict(config.get("exporters"), "exporters")
    service = _as_dict(config.get("service"), "service")
    pipelines = _as_dict(service.get("pipelines"), "service.pipelines")

    _check(REQUIRED_RECEIVERS <= set(receivers), "collector_required_receivers", str(sorted(receivers)), checks)
    _check(REQUIRED_PROCESSORS <= set(processors), "collector_required_processors", str(sorted(processors)), checks)
    _check(REQUIRED_EXPORTERS <= set(exporters), "collector_required_exporters", str(sorted(exporters)), checks)
    _check(REQUIRED_PIPELINES <= set(pipelines), "collector_required_pipelines", str(sorted(pipelines)), checks)

    otlp = _as_dict(receivers["otlp"], "receivers.otlp")
    protocols = _as_dict(otlp.get("protocols"), "receivers.otlp.protocols")
    _check({"grpc", "http"} <= set(protocols), "collector_otlp_protocols", str(sorted(protocols)), checks)
    for protocol in ("grpc", "http"):
        endpoint = str(_as_dict(protocols[protocol], f"receivers.otlp.protocols.{protocol}").get("endpoint") or "")
        _check(endpoint.startswith("127.0.0.1:"), f"collector_{protocol}_loopback_endpoint", endpoint, checks)

    for pipeline_name in sorted(REQUIRED_PIPELINES):
        pipeline = _as_dict(pipelines[pipeline_name], f"service.pipelines.{pipeline_name}")
        pipeline_receivers = set(_as_list(pipeline.get("receivers"), f"{pipeline_name}.receivers"))
        pipeline_processors = set(_as_list(pipeline.get("processors"), f"{pipeline_name}.processors"))
        pipeline_exporters = set(_as_list(pipeline.get("exporters"), f"{pipeline_name}.exporters"))
        _check(
            "otlp" in pipeline_receivers, f"{pipeline_name}_uses_otlp_receiver", str(sorted(pipeline_receivers)), checks
        )
        _check(
            {"memory_limiter", "batch"} <= pipeline_processors,
            f"{pipeline_name}_uses_safety_processors",
            str(sorted(pipeline_processors)),
            checks,
        )
        _check(
            "debug" in pipeline_exporters,
            f"{pipeline_name}_uses_debug_exporter",
            str(sorted(pipeline_exporters)),
            checks,
        )
        _check(
            not any(exporter.startswith("otlp") for exporter in pipeline_exporters),
            f"{pipeline_name}_no_external_otlp_exporter",
            str(sorted(pipeline_exporters)),
            checks,
        )

    fatecat = _as_dict(config.get("fatecat"), "fatecat")
    _check(
        fatecat.get("externalConnectivity") == "external_connectivity_pending",
        "collector_external_pending",
        str(fatecat.get("externalConnectivity")),
        checks,
    )
    _check("外部连通验证待执行" in str(fatecat.get("liveEvidence")), "collector_live_pending_text", "present", checks)
    privacy = str(fatecat.get("privacyBoundary") or "")
    for term in ("user input", "token", "secret", "DSN", "report body"):
        _check(term in privacy, f"collector_privacy_mentions_{term}", "mentioned", checks)


def _validate_slo_evidence(evidence: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    _check(evidence.get("kind") == "SloEvidenceContract", "slo_evidence_kind", str(evidence.get("kind")), checks)
    _check(
        evidence.get("collectorConfig") == "contracts/fate/observability/otel-collector.dry-run.yaml",
        "slo_evidence_collector_link",
        str(evidence.get("collectorConfig")),
        checks,
    )
    dry_run = _as_dict(evidence.get("dryRunEvidence"), "dryRunEvidence")
    _check(dry_run.get("status") == "available", "slo_dry_run_available", str(dry_run.get("status")), checks)
    dry_run_checks = {
        str(item.get("id")) for item in _as_list(dry_run.get("requiredChecks"), "dryRunEvidence.requiredChecks")
    }
    _check(
        REQUIRED_DRY_RUN_CHECKS <= dry_run_checks,
        "slo_required_dry_run_checks",
        str(sorted(REQUIRED_DRY_RUN_CHECKS - dry_run_checks)),
        checks,
    )

    live = _as_dict(evidence.get("liveEvidence"), "liveEvidence")
    _check(
        live.get("status") == "external_connectivity_pending",
        "slo_live_pending_status",
        str(live.get("status")),
        checks,
    )
    _check("外部连通验证待执行" in str(live.get("message")), "slo_live_pending_text", "present", checks)
    live_items = {
        str(item.get("id"))
        for item in _as_list(live.get("requiredBeforeProduction"), "liveEvidence.requiredBeforeProduction")
    }
    _check(
        REQUIRED_LIVE_EVIDENCE <= live_items,
        "slo_required_live_evidence",
        str(sorted(REQUIRED_LIVE_EVIDENCE - live_items)),
        checks,
    )

    forbidden = _as_dict(evidence.get("forbiddenClaimBoundary"), "forbiddenClaimBoundary")
    must_not_claim = {
        str(item) for item in _as_list(forbidden.get("mustNotClaim"), "forbiddenClaimBoundary.mustNotClaim")
    }
    for claim in ("trace backend live", "collector runtime live", "production SLO computed", "alert live"):
        _check(claim in must_not_claim, f"slo_forbidden_claim_{claim}", "present", checks)
    _check(
        evidence.get("externalConnectivity") == "external_connectivity_pending",
        "slo_external_pending",
        str(evidence.get("externalConnectivity")),
        checks,
    )
    privacy = str(evidence.get("privacyBoundary") or "")
    for term in ("user input", "birth place", "report body", "token", "secret", "DSN"):
        _check(term in privacy, f"slo_privacy_mentions_{term}", "mentioned", checks)


def _validate_registry_links(registry: dict[str, Any], schema: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    schemas = _as_dict(registry.get("schemas"), "registry.schemas")
    _check(
        schemas.get("otelCollectorDryRunConfig") == "contracts/fate/observability/otel-collector.dry-run.yaml",
        "registry_collector_schema_link",
        str(schemas.get("otelCollectorDryRunConfig")),
        checks,
    )
    _check(
        schemas.get("sloEvidenceContract") == "contracts/fate/observability/slo-evidence-contract.json",
        "registry_slo_evidence_link",
        str(schemas.get("sloEvidenceContract")),
        checks,
    )
    signals = {item.get("id"): item for item in _as_list(registry.get("signals"), "registry.signals")}
    for signal_id in ("signal.otel_collector_dry_run", "signal.slo_evidence_contract"):
        _check(signal_id in signals, f"registry_signal_{signal_id}", "present", checks)
        signal = _as_dict(signals[signal_id], signal_id)
        _check(signal.get("status") == "available", f"{signal_id}_available", str(signal.get("status")), checks)
        _check(
            signal.get("externalConnectivity") == "external_connectivity_pending",
            f"{signal_id}_external_pending",
            str(signal.get("externalConnectivity")),
            checks,
        )
        _check(bool(signal.get("localVerification")), f"{signal_id}_local_verification", "non-empty", checks)

    metadata = _as_dict(registry.get("metadata"), "registry.metadata")
    _check(
        metadata.get("otelCollectorSloGateCommand") == "bash scripts/otel-collector-slo-gate.sh",
        "registry_otel_gate_command",
        str(metadata.get("otelCollectorSloGateCommand")),
        checks,
    )
    _check(
        "外部连通验证待执行" in str(metadata.get("otelCollectorBoundary")), "registry_otel_boundary", "present", checks
    )
    _check(
        "otelCollectorAdapterFields" in schema,
        "schema_otel_collector_adapter_fields",
        "present",
        checks,
    )
    _check(
        "OTel collector dry-run config 不得被解释为真实 collector runtime、trace backend、metrics backend 或 alert live 已完成"
        in schema.get("invariants", []),
        "schema_otel_invariant",
        "present",
        checks,
    )


def run_gate(
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    schema_path: Path = DEFAULT_SCHEMA,
    collector_config_path: Path = DEFAULT_COLLECTOR_CONFIG,
    slo_evidence_path: Path = DEFAULT_SLO_EVIDENCE,
    slo_policy_path: Path = DEFAULT_SLO_POLICY,
    alert_rules_path: Path = DEFAULT_ALERT_RULES,
) -> dict[str, Any]:
    registry = load_json(registry_path)
    schema = load_json(schema_path)
    collector_config = load_yaml(collector_config_path)
    slo_evidence = load_json(slo_evidence_path)
    checks: list[dict[str, Any]] = []

    _validate_collector_config(collector_config, checks)
    _validate_slo_evidence(slo_evidence, checks)
    _validate_registry_links(registry, schema, checks)

    slo_gate = _load_slo_gate_module()
    slo_gate_summary = slo_gate.run_gate(
        registry_path=registry_path,
        slo_policy_path=slo_policy_path,
        alert_rules_path=alert_rules_path,
    )
    _check(slo_gate_summary["status"] == "passed", "existing_slo_gate_status", slo_gate_summary["status"], checks)

    pipelines = _as_dict(_as_dict(collector_config["service"], "service")["pipelines"], "service.pipelines")
    dry_run_checks = _as_list(
        _as_dict(slo_evidence["dryRunEvidence"], "dryRunEvidence")["requiredChecks"],
        "dryRunEvidence.requiredChecks",
    )
    live_evidence = _as_dict(slo_evidence["liveEvidence"], "liveEvidence")
    return {
        "schemaVersion": 1,
        "generatedAt": utc_now(),
        "status": "passed",
        "collectorMode": collector_config.get("mode"),
        "pipelines": len(pipelines),
        "dryRunEvidenceChecks": len(dry_run_checks),
        "liveEvidenceStatus": live_evidence.get("status"),
        "checks": checks,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "gate 只读取 dry-run collector config、SLO evidence contract、registry、schema、SLO policy 和 alert rules；不读取真实 logs、metrics、traces、用户输入、token、secret、DSN 或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 OTel collector dry-run config 与 SLO evidence contract。")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="observability registry JSON。")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="observability signal schema JSON。")
    parser.add_argument(
        "--collector-config", type=Path, default=DEFAULT_COLLECTOR_CONFIG, help="collector dry-run YAML。"
    )
    parser.add_argument("--slo-evidence", type=Path, default=DEFAULT_SLO_EVIDENCE, help="SLO evidence contract JSON。")
    parser.add_argument("--slo-policy", type=Path, default=DEFAULT_SLO_POLICY, help="SLO policy JSON。")
    parser.add_argument("--alert-rules", type=Path, default=DEFAULT_ALERT_RULES, help="alert rules JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            registry_path=args.registry,
            schema_path=args.schema,
            collector_config_path=args.collector_config,
            slo_evidence_path=args.slo_evidence,
            slo_policy_path=args.slo_policy,
            alert_rules_path=args.alert_rules,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "collectorMode": summary["collectorMode"],
                    "pipelines": summary["pipelines"],
                    "dryRunEvidenceChecks": summary["dryRunEvidenceChecks"],
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (OTelCollectorSloGateError, OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"otel collector slo gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
