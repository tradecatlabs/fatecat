#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEVELOPER_ROOT = REPO_ROOT / "contracts" / "fate" / "developer"
DEFAULT_GATEWAY = DEVELOPER_ROOT / "sandbox-access-gateway.json"
DEFAULT_TOKEN_CONTRACT = DEVELOPER_ROOT / "sandbox-token-contract.json"
DEFAULT_SANDBOX = DEVELOPER_ROOT / "sandbox.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "sandbox-access-gateway-gate.json"
)


class SandboxGatewayGateError(RuntimeError):
    """sandbox access gateway gate 未满足预期。"""


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


@contextmanager
def temporary_attr(obj, name: str, value):
    old_value = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old_value)


class JsonCaptureHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.INFO)
        self.payloads: list[dict[str, Any]] = []

    def emit(self, record: logging.LogRecord) -> None:
        try:
            payload = json.loads(record.getMessage())
        except json.JSONDecodeError:
            return
        if isinstance(payload, dict):
            self.payloads.append(payload)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SandboxGatewayGateError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SandboxGatewayGateError(f"JSON 格式错误: {path}: {exc}") from exc


def _load_main():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import main  # noqa: PLC0415

    return main


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise SandboxGatewayGateError(f"{name}: {details}")


def _fixture_by_id(sandbox: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    for fixture in sandbox.get("fixtures", []):
        if fixture.get("id") == fixture_id:
            return fixture
    raise SandboxGatewayGateError(f"缺少 sandbox fixture: {fixture_id}")


def _response_json(response) -> dict[str, Any]:
    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise SandboxGatewayGateError(f"响应不是 JSON: status={response.status_code}") from exc
    if not isinstance(payload, dict):
        raise SandboxGatewayGateError("响应 JSON 必须是 object")
    return payload


def _assert_no_sensitive_values(payload: dict[str, Any], *, token_value: str, subject: str) -> None:
    serialized = json.dumps(payload, ensure_ascii=False)
    forbidden = [token_value, subject, "password=", "secret=", "BEGIN RSA", "BEGIN OPENSSH"]
    leaked = [item for item in forbidden if item and item in serialized]
    if leaked:
        raise SandboxGatewayGateError("gate 输出包含敏感值或未脱敏主体")


def run_gate(
    *,
    gateway_path: Path = DEFAULT_GATEWAY,
    token_contract_path: Path = DEFAULT_TOKEN_CONTRACT,
    sandbox_path: Path = DEFAULT_SANDBOX,
) -> dict[str, Any]:
    gateway = _load_json(gateway_path)
    token_contract = _load_json(token_contract_path)
    sandbox = _load_json(sandbox_path)
    main = _load_main()
    client = TestClient(main.app)
    checks: list[dict[str, Any]] = []

    _check(checks, "gateway:schema", gateway.get("schemaVersion") == 1, str(gateway.get("schemaVersion")))
    _check(checks, "gateway:kind", gateway.get("kind") == "fatecat.sandbox_access_gateway", str(gateway.get("kind")))
    _check(checks, "gateway:status", gateway["status"] == "local_gateway_baseline", gateway["status"])
    _check(
        checks,
        "gateway:live_public_token_service",
        gateway["livePublicTokenServiceStatus"] == "not_implemented",
        gateway["livePublicTokenServiceStatus"],
    )
    _check(
        checks,
        "gateway:token_material_policy",
        gateway["tokenMaterialPolicy"] == "no_real_tokens_in_repo",
        gateway["tokenMaterialPolicy"],
    )
    _check(
        checks,
        "token:gateway_link",
        token_contract["localGatewayContract"] == "contracts/fate/developer/sandbox-access-gateway.json",
        token_contract.get("localGatewayContract", ""),
    )

    scope_rules = gateway.get("scopeRules", [])
    _check(checks, "gateway:scope_rules", isinstance(scope_rules, list) and len(scope_rules) >= 2, str(scope_rules))
    almanac_rule = next(item for item in scope_rules if item["capabilityId"] == "almanac")
    meihua_rule = next(item for item in scope_rules if item["capabilityId"] == "meihua")
    almanac_fixture = _fixture_by_id(sandbox, almanac_rule["fixtureId"])

    openapi = client.get("/openapi.json")
    paths = openapi.json().get("paths", {})
    _check(
        checks,
        "openapi:sandbox_gateway_path",
        "/api/v1/sandbox/capabilities/{capability_id}/calculate" in paths,
        str(sorted(path for path in paths if "sandbox" in path)),
    )

    subject = "sandbox-smoke-subject"
    sample_bearer = "local-sandbox-test-credential"
    allowed_env = f"{subject}:{sample_bearer}:{almanac_rule['scope']}"
    wrong_scope_env = f"{subject}:{sample_bearer}:{meihua_rule['scope']}"

    with temporary_env({"FATE_SANDBOX_TOKENS": allowed_env}):
        missing = client.post(almanac_rule["gatewayEndpoint"], json=almanac_fixture["request"])
    _check(checks, "auth:missing_token_rejected", missing.status_code == 403, f"status={missing.status_code}")

    with temporary_env({"FATE_SANDBOX_TOKENS": wrong_scope_env}):
        forbidden = client.post(
            almanac_rule["gatewayEndpoint"],
            json=almanac_fixture["request"],
            headers={"Authorization": f"Bearer {sample_bearer}"},
        )
    _check(checks, "auth:wrong_scope_rejected", forbidden.status_code == 403, f"status={forbidden.status_code}")

    capture = JsonCaptureHandler()
    main.logger.addHandler(capture)
    old_level = main.logger.level
    main.logger.setLevel(logging.INFO)
    try:
        with temporary_env({"FATE_SANDBOX_TOKENS": allowed_env}):
            ok = client.post(
                almanac_rule["gatewayEndpoint"],
                json=almanac_fixture["request"],
                headers={"Authorization": f"Bearer {sample_bearer}", "X-Request-ID": "sandbox-gateway-smoke"},
            )
    finally:
        main.logger.setLevel(old_level)
        main.logger.removeHandler(capture)
    ok_body = _response_json(ok)
    _check(checks, "auth:allowed_scope_executes", ok.status_code == 200, f"status={ok.status_code}")
    _check(checks, "response:success", ok_body.get("success") is True, str(ok_body.get("success")))
    _check(checks, "response:capability", ok_body.get("capabilityId") == "almanac", str(ok_body.get("capabilityId")))
    _check(
        checks,
        "response:sandbox_scope",
        ok_body.get("sandbox", {}).get("scope") == almanac_rule["scope"],
        str(ok_body.get("sandbox", {})),
    )

    audit_events = [item for item in capture.payloads if item.get("event") == "audit_event"]
    _check(checks, "audit:event_emitted", len(audit_events) >= 1, str(audit_events))
    audit_text = json.dumps(audit_events, ensure_ascii=False)
    _check(checks, "audit:no_token_value", sample_bearer not in audit_text, "token redacted")
    _check(checks, "audit:no_raw_subject", subject not in audit_text, "subject hashed")

    with (
        temporary_env({"FATE_SANDBOX_TOKENS": allowed_env}),
        temporary_attr(main, "RATE_LIMIT_PER_MINUTE", 1),
    ):
        main._rate_limit_windows.clear()
        first = client.post(
            almanac_rule["gatewayEndpoint"],
            json=almanac_fixture["request"],
            headers={"Authorization": f"Bearer {sample_bearer}"},
        )
        second = client.post(
            almanac_rule["gatewayEndpoint"],
            json=almanac_fixture["request"],
            headers={"Authorization": f"Bearer {sample_bearer}"},
        )
        main._rate_limit_windows.clear()
    _check(checks, "rate_limit:first_request", first.status_code == 200, f"status={first.status_code}")
    _check(checks, "rate_limit:second_request", second.status_code == 429, f"status={second.status_code}")
    _check(checks, "rate_limit:retry_after", second.headers.get("retry-after") is not None, "present")

    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.sandbox_access_gateway_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "localGatewayExecutable": True,
        "scopeRules": len(scope_rules),
        "rateLimitEvidence": {
            "firstStatus": first.status_code,
            "secondStatus": second.status_code,
            "retryAfterHeader": second.headers.get("retry-after") is not None,
        },
        "auditEvidence": {
            "eventCaptured": len(audit_events) >= 1,
            "action": "sandbox.capability.calculate",
            "redacted": True,
        },
        "livePublicTokenService": False,
        "externalIssuerStatus": "not_implemented",
        "privacyBoundary": "summary records only status, check names and counts; it never stores token values, subjects, request bodies, report bodies, production URLs or secrets.",
        "limitations": [
            "This proves local sandbox gateway semantics only.",
            "This does not prove a public sandbox token issuer, revocation service or production API gateway is live.",
        ],
    }
    _assert_no_sensitive_values(summary, token_value=sample_bearer, subject=subject)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验本地 sandbox access gateway、scope、限流和审计脱敏。")
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY, help="sandbox access gateway contract。")
    parser.add_argument("--token-contract", type=Path, default=DEFAULT_TOKEN_CONTRACT, help="sandbox token contract。")
    parser.add_argument("--sandbox", type=Path, default=DEFAULT_SANDBOX, help="sandbox fixture contract。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            gateway_path=args.gateway, token_contract_path=args.token_contract, sandbox_path=args.sandbox
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "checks": len(summary["checks"]),
                    "localGatewayExecutable": summary["localGatewayExecutable"],
                    "livePublicTokenService": summary["livePublicTokenService"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except SandboxGatewayGateError as exc:
        print(f"sandbox gateway gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
