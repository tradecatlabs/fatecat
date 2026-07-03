#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SECURITY_DIR = REPO_ROOT / "contracts" / "fate" / "security"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "security" / "production-security-gate.json"
)

REQUIRED_CONTROL_IDS = {
    "control.production_identity_oidc",
    "control.external_siem_immutable_audit",
    "control.retention_cleanup_plan",
    "control.external_secret_provider_kms",
    "control.owasp_api_security_regression",
}
REQUIRED_OWASP_IDS = {f"API{index}" for index in range(1, 11)}
SENSITIVE_WORDS = {"token", "secret", "password", "dsn", "private_key", "BEGIN RSA"}


class GateFailure(RuntimeError):
    """生产安全准入门禁失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _assert_no_sensitive_values(checks: list[dict[str, Any]], payload: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False)
    bad_values = []
    for word in SENSITIVE_WORDS:
        marker = f"{word}="
        if marker in rendered:
            bad_values.append(marker)
    _check(checks, "no_inline_sensitive_values", not bad_values, ",".join(sorted(bad_values)) or "clean")


def run_gate() -> dict[str, Any]:
    schema = _load_json(SECURITY_DIR / "schemas" / "security-control.schema.json")
    registry = _load_json(SECURITY_DIR / "registry.json")
    policy = _load_json(SECURITY_DIR / "production-security-policy.json")
    controls = {item["id"]: item for item in registry["controls"]}
    checks: list[dict[str, Any]] = []

    _check(checks, "schema_allows_identity", "identity" in schema["allowedControlType"], "identity")
    _check(checks, "schema_allows_siem", "siem" in schema["allowedControlType"], "siem")
    _check(
        checks,
        "schema_allows_owasp_regression",
        "owasp_api_regression" in schema["allowedControlType"],
        "owasp_api_regression",
    )
    _check(
        checks,
        "schema_allows_secret_provider",
        "secret_provider" in schema["allowedControlType"],
        "secret_provider",
    )
    _check(
        checks,
        "required_controls_present",
        REQUIRED_CONTROL_IDS <= set(controls),
        str(sorted(REQUIRED_CONTROL_IDS - set(controls))),
    )

    identity = controls["control.production_identity_oidc"]
    _check(checks, "identity_control_type", identity["controlType"] == "identity", identity["controlType"])
    _check(checks, "identity_manual_status", identity["status"] == "manual", identity["status"])
    _check(
        checks,
        "identity_external_pending",
        identity["externalConnectivity"] == "external_connectivity_pending",
        identity["externalConnectivity"],
    )
    _check(
        checks,
        "identity_oidc_envs",
        set(policy["identity"]["admissionEnvVars"]) <= set(identity["envVars"]),
        str(sorted(set(policy["identity"]["admissionEnvVars"]) - set(identity["envVars"]))),
    )
    _check(
        checks,
        "identity_boundary_names_scoped_token",
        "scoped token" in policy["identity"]["localFallbackBoundary"],
        policy["identity"]["localFallbackBoundary"],
    )

    siem = controls["control.external_siem_immutable_audit"]
    _check(checks, "siem_control_type", siem["controlType"] == "siem", siem["controlType"])
    _check(checks, "siem_manual_status", siem["status"] == "manual", siem["status"])
    _check(
        checks,
        "siem_external_pending",
        siem["externalConnectivity"] == "external_connectivity_pending",
        siem["externalConnectivity"],
    )
    _check(
        checks,
        "siem_envs",
        set(policy["siem"]["admissionEnvVars"]) <= set(siem["envVars"]),
        str(sorted(set(policy["siem"]["admissionEnvVars"]) - set(siem["envVars"]))),
    )
    _check(checks, "siem_requires_immutable_audit", policy["siem"]["immutableAuditRequired"] is True, "required")
    _check(
        checks,
        "siem_privacy_boundary",
        "报告正文" in policy["siem"]["privacyBoundary"] and "token" in policy["siem"]["privacyBoundary"],
        policy["siem"]["privacyBoundary"],
    )

    retention = controls["control.retention_cleanup_plan"]
    _check(checks, "retention_cleanup_control_type", retention["controlType"] == "retention", retention["controlType"])
    _check(checks, "retention_cleanup_manual_status", retention["status"] == "manual", retention["status"])
    _check(
        checks,
        "retention_cleanup_envs",
        set(policy["retention"]["admissionEnvVars"]) <= set(retention["envVars"]),
        str(sorted(set(policy["retention"]["admissionEnvVars"]) - set(retention["envVars"]))),
    )
    _check(
        checks,
        "retention_current_mode_explicit_delete",
        policy["retention"]["currentRecordMode"] == "explicit_delete",
        policy["retention"]["currentRecordMode"],
    )
    _check(
        checks,
        "retention_target_requires_cleanup",
        "cleanup" in policy["retention"]["targetRecordMode"],
        policy["retention"]["targetRecordMode"],
    )

    secret_provider = controls["control.external_secret_provider_kms"]
    _check(
        checks,
        "secret_provider_control_type",
        secret_provider["controlType"] == "secret_provider",
        secret_provider["controlType"],
    )
    _check(checks, "secret_provider_manual_status", secret_provider["status"] == "manual", secret_provider["status"])
    _check(
        checks,
        "secret_provider_external_pending",
        secret_provider["externalConnectivity"] == "external_connectivity_pending",
        secret_provider["externalConnectivity"],
    )
    _check(
        checks,
        "secret_provider_envs",
        set(policy["secretProvider"]["admissionEnvVars"]) <= set(secret_provider["envVars"]),
        str(sorted(set(policy["secretProvider"]["admissionEnvVars"]) - set(secret_provider["envVars"]))),
    )
    _check(
        checks,
        "secret_provider_boundary_names_local_fernet",
        "FATE_WEBHOOK_CONFIG_FERNET_KEYS" in policy["secretProvider"]["localBoundary"]
        and "不得宣称" in policy["secretProvider"]["localBoundary"],
        policy["secretProvider"]["localBoundary"],
    )

    owasp = controls["control.owasp_api_security_regression"]
    _check(checks, "owasp_control_type", owasp["controlType"] == "owasp_api_regression", owasp["controlType"])
    _check(checks, "owasp_available", owasp["status"] == "available", owasp["status"])
    _check(
        checks,
        "owasp_local_verification",
        "bash scripts/production-security-gate.sh" in owasp["localVerification"],
        "present",
    )

    owasp_items = policy["owaspApiSecurityTop10_2023"]
    owasp_ids = {item["id"] for item in owasp_items}
    _check(checks, "owasp_top10_complete", owasp_ids == REQUIRED_OWASP_IDS, str(sorted(REQUIRED_OWASP_IDS - owasp_ids)))
    for item in owasp_items:
        _check(checks, f"{item['id']}:name", bool(item.get("name")), "present")
        _check(checks, f"{item['id']}:local_coverage", bool(item.get("localCoverage")), "present")

    _check(
        checks,
        "registry_gate_metadata",
        registry["metadata"].get("productionSecurityGateCommand") == "bash scripts/production-security-gate.sh",
        registry["metadata"].get("productionSecurityGateCommand", ""),
    )
    _check(
        checks,
        "policy_release_gate_command",
        policy["releaseGate"]["localCommand"] == "bash scripts/production-security-gate.sh",
        policy["releaseGate"].get("localCommand", ""),
    )
    _check(checks, "policy_quick_ci_required", policy["releaseGate"]["quickCiRequired"] is True, "required")
    _check(
        checks,
        "policy_blocks_without_external_evidence",
        {
            "external_oidc_or_idp",
            "external_siem_or_immutable_audit_storage",
            "time_based_record_retention_cleanup",
            "external_secret_provider_or_kms",
            "production_live_smoke",
        }
        <= set(policy["releaseGate"]["blocksPublicReleaseWithoutExternalEvidence"]),
        "required blockers present",
    )
    _assert_no_sensitive_values(checks, policy)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "controls": sorted(REQUIRED_CONTROL_IDS),
        "owaspCoverageCount": len(owasp_items),
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "gate output 只保存检查名、状态和摘要；不得输出真实 token、secret、DSN、SIEM endpoint、请求体、用户输入或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="验证生产身份、SIEM、retention 与 OWASP API 回归包准入 contract。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "controls": len(summary["controls"]),
                    "owaspCoverageCount": summary["owaspCoverageCount"],
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except GateFailure as exc:
        print(f"production security gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
