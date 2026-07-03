#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SECURITY_DIR = REPO_ROOT / "contracts" / "fate" / "security"
CONTRACT_PATH = SECURITY_DIR / "external-secret-provider-contract.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "security" / "external-secret-provider-gate.json"
)

CONTROL_ID = "control.external_secret_provider_kms"
SENSITIVE_FRAGMENTS = {
    "BEGIN RSA",
    "BEGIN OPENSSH",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "password=",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}


class GateFailure(RuntimeError):
    """外部 secret provider 证据门禁失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive_fragments(checks: list[dict[str, Any]], name: str, payload: Any) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    _check(checks, name, not bad, ",".join(bad) or "clean")


def _scalar_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_scalar_values(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_scalar_values(item))
        return result
    return [str(value)]


def _contains_forbidden(value: Any, forbidden: list[str]) -> bool:
    text = " ".join(_scalar_values(value)).lower()
    return any(fragment.lower() in text for fragment in forbidden)


def _require_fields(area: str, payload: dict[str, Any], fields: list[str]) -> None:
    missing = [field for field in fields if field not in payload or payload[field] in ("", None, [])]
    if missing:
        raise GateFailure(f"{area}: missing fields {missing}")


def validate_external_secret_evidence(evidence: dict[str, Any], contract: dict[str, Any]) -> None:
    status = evidence.get("status")
    if status == "external_connectivity_pending":
        return
    if status != "external_live_passed":
        raise GateFailure(f"evidence: unsupported status {status!r}")

    secret_provider = evidence.get("secretProvider")
    if not isinstance(secret_provider, dict):
        raise GateFailure("secretProvider: required for external_live_passed")

    schema = contract["controls"]["externalSecretProvider"]["liveEvidenceSchema"]
    _require_fields("secretProvider", secret_provider, schema["requiredFields"])
    if secret_provider["mode"] != schema["requiredMode"]:
        raise GateFailure("secretProvider: mode is not external_secret_provider")
    if secret_provider["verificationStatus"] != schema["requiredVerificationStatus"]:
        raise GateFailure("secretProvider: verificationStatus is not passed_external_secret_provider_check")
    if secret_provider["redactionBoundary"] != schema["requiredRedactionBoundary"]:
        raise GateFailure("secretProvider: redactionBoundary must be redacted_no_secret_values")
    if secret_provider["providerType"] in schema["forbiddenProviderValues"]:
        raise GateFailure("secretProvider: forbidden providerType")
    allowed_provider_types = contract["controls"]["externalSecretProvider"]["allowedProviderTypes"]
    if secret_provider["providerType"] not in allowed_provider_types:
        raise GateFailure("secretProvider: unsupported providerType")
    if _contains_forbidden(secret_provider, schema["forbiddenProofFragments"]):
        raise GateFailure("secretProvider: forbidden local key, placeholder or secret proof")


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        case_id = case["id"]
        expected = case["expectedErrorContains"]
        try:
            validate_external_secret_evidence(case["evidence"], contract)
        except GateFailure as exc:
            message = str(exc)
            _check(checks, f"negative:{case_id}", expected in message, message)
            rejected.append(case_id)
        else:
            raise GateFailure(f"negative:{case_id}: fake evidence was accepted")
    return rejected


def _validate_contract(checks: list[dict[str, Any]], contract: dict[str, Any]) -> None:
    _check(
        checks,
        "contract_id",
        contract["contractId"] == "contract.external_secret_provider_evidence",
        contract["contractId"],
    )
    _check(checks, "contract_status", contract["status"] == "dry_run_contract", contract["status"])
    _check(
        checks,
        "contract_external_pending",
        contract["externalConnectivity"] == "external_connectivity_pending",
        contract["externalConnectivity"],
    )
    _check(
        checks,
        "contract_controls",
        {"localFernetWebhookConfig", "externalSecretProvider"} <= set(contract["controls"]),
        str(sorted({"localFernetWebhookConfig", "externalSecretProvider"} - set(contract["controls"]))),
    )
    local_control = contract["controls"]["localFernetWebhookConfig"]
    _check(checks, "local_control_id", local_control["controlId"] == CONTROL_ID, local_control["controlId"])
    _check(
        checks,
        "local_baseline_not_external",
        local_control["baselineMode"] == "local_fernet_encrypted_config_vault",
        local_control["baselineMode"],
    )
    external_control = contract["controls"]["externalSecretProvider"]
    _check(checks, "external_control_id", external_control["controlId"] == CONTROL_ID, external_control["controlId"])
    _check(
        checks,
        "external_live_schema",
        bool(external_control.get("liveEvidenceSchema", {}).get("requiredFields")),
        "present",
    )
    _check(
        checks,
        "allowed_provider_types",
        {"hashicorp_vault", "aws_kms", "gcp_secret_manager", "azure_key_vault"}
        <= set(external_control["allowedProviderTypes"]),
        str(external_control["allowedProviderTypes"]),
    )
    _check(
        checks,
        "negative_cases_present",
        len(contract["negativeEvidenceCases"]) >= 3,
        str(len(contract["negativeEvidenceCases"])),
    )
    _assert_no_sensitive_fragments(checks, "contract_no_sensitive_fragments", contract)


def _validate_registry_and_policy(
    checks: list[dict[str, Any]], registry: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any]
) -> None:
    _check(checks, "schema_allows_secret_provider", "secret_provider" in schema["allowedControlType"], "present")
    controls = {item["id"]: item for item in registry["controls"]}
    _check(checks, "registry_control_present", CONTROL_ID in controls, str(sorted(controls)))
    control = controls[CONTROL_ID]
    _check(checks, "registry_control_type", control["controlType"] == "secret_provider", control["controlType"])
    _check(checks, "registry_manual_status", control["status"] == "manual", control["status"])
    _check(
        checks,
        "registry_external_pending",
        control["externalConnectivity"] == "external_connectivity_pending",
        control["externalConnectivity"],
    )
    _check(
        checks,
        "registry_gate_linked",
        "bash scripts/external-secret-provider-gate.sh" in control["localVerification"],
        str(control["localVerification"]),
    )
    metadata = registry["metadata"]
    _check(
        checks,
        "registry_external_secret_provider_gate_command",
        metadata.get("externalSecretProviderGateCommand") == "bash scripts/external-secret-provider-gate.sh",
        metadata.get("externalSecretProviderGateCommand", ""),
    )
    _check(
        checks,
        "registry_external_secret_provider_contract",
        metadata.get("externalSecretProviderEvidenceContract")
        == "contracts/fate/security/external-secret-provider-contract.json",
        metadata.get("externalSecretProviderEvidenceContract", ""),
    )
    _check(
        checks,
        "policy_secret_provider_contract",
        policy["releaseGate"].get("externalSecretProviderEvidenceContract")
        == "contracts/fate/security/external-secret-provider-contract.json",
        policy["releaseGate"].get("externalSecretProviderEvidenceContract", ""),
    )
    _check(
        checks,
        "policy_secret_provider_gate",
        policy["releaseGate"].get("externalSecretProviderGateCommand")
        == "bash scripts/external-secret-provider-gate.sh",
        policy["releaseGate"].get("externalSecretProviderGateCommand", ""),
    )


def run_gate(evidence_json: Path | None = None) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    schema = _load_json(SECURITY_DIR / "schemas" / "security-control.schema.json")
    registry = _load_json(SECURITY_DIR / "registry.json")
    policy = _load_json(SECURITY_DIR / "production-security-policy.json")
    checks: list[dict[str, Any]] = []

    _validate_contract(checks, contract)
    _validate_registry_and_policy(checks, registry, schema, policy)
    rejected_negative_cases = _validate_negative_cases(checks, contract)

    live_evidence_status = "外部连通验证待执行"
    if evidence_json is not None:
        evidence = _load_json(evidence_json)
        _assert_no_sensitive_fragments(checks, "evidence_no_sensitive_fragments", evidence)
        validate_external_secret_evidence(evidence, contract)
        live_evidence_status = (
            "external_live_passed" if evidence.get("status") == "external_live_passed" else live_evidence_status
        )

    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_secret_provider_gate_summary",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "contract": "contracts/fate/security/external-secret-provider-contract.json",
        "controls": [CONTROL_ID],
        "negativeEvidenceRejected": rejected_negative_cases,
        "liveEvidenceStatus": live_evidence_status,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "summary 只保存检查名、状态和脱敏摘要；不得输出真实 secret、token、DSN、webhook URL、provider endpoint、KMS key 原值、请求体、用户输入、审计 payload 或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="验证外部 secret provider / Vault / KMS 证据契约和反伪造边界。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    parser.add_argument(
        "--evidence-json", type=Path, default=None, help="可选外部 live evidence JSON；默认只验证 pending contract。"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(args.evidence_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "controls": len(summary["controls"]),
                    "negativeEvidenceRejected": len(summary["negativeEvidenceRejected"]),
                    "liveEvidenceStatus": summary["liveEvidenceStatus"],
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except GateFailure as exc:
        print(f"external secret provider gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
