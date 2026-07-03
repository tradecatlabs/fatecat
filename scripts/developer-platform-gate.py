#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEVELOPER_ROOT = REPO_ROOT / "contracts" / "fate" / "developer"
DEFAULT_PLATFORM = DEVELOPER_ROOT / "developer-platform.json"
DEFAULT_SANDBOX = DEVELOPER_ROOT / "sandbox.json"
DEFAULT_TOKEN_CONTRACT = DEVELOPER_ROOT / "sandbox-token-contract.json"
DEFAULT_SANDBOX_GATEWAY = DEVELOPER_ROOT / "sandbox-access-gateway.json"
DEFAULT_CHANGELOG = DEVELOPER_ROOT / "api-changelog.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "developer-platform-gate.json"
)


class DeveloperPlatformGateError(RuntimeError):
    """开发者平台 gate 未满足预期。"""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DeveloperPlatformGateError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DeveloperPlatformGateError(f"JSON 格式错误: {path}: {exc}") from exc


def _repo_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise DeveloperPlatformGateError(f"路径必须是仓库相对路径且不得越界: {relative_path}")
    resolved = (REPO_ROOT / path).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise DeveloperPlatformGateError(f"路径越过仓库根: {relative_path}") from exc
    return resolved


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise DeveloperPlatformGateError(f"{name}: {details}")


def _birth_place(input_payload: dict[str, Any]) -> str | None:
    value = input_payload.get("birthPlace") or input_payload.get("place")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        name = value.get("name")
        return str(name) if name is not None else None
    return None


def _validate_sdk_package_baseline(platform: dict[str, Any], checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sdk = platform["sdkPackageBaseline"]
    _check(checks, "sdk:release_status", sdk["releaseStatus"] == "baseline_not_published", sdk["releaseStatus"])
    _check(
        checks,
        "sdk:package_registry_status",
        sdk["packageRegistryStatus"] == "not_published",
        sdk["packageRegistryStatus"],
    )
    _check(
        checks,
        "sdk:not_published_boundary",
        "not a released" in sdk["notPublishedBoundary"],
        sdk["notPublishedBoundary"],
    )
    _check(checks, "sdk:human_guide_exists", _repo_path(sdk["humanGuide"]).exists(), sdk["humanGuide"])
    packages = sdk.get("packageCandidates")
    _check(
        checks, "sdk:package_candidates", isinstance(packages, list) and len(packages) >= 4, str(len(packages or []))
    )
    results: list[dict[str, Any]] = []
    for item in packages:
        package_id = f"{item['language']}:{item['candidateName']}"
        _check(checks, f"sdk:{package_id}:status", item["status"] == "installable_example", item["status"])
        _check(checks, f"sdk:{package_id}:source_exists", _repo_path(item["sourcePath"]).exists(), item["sourcePath"])
        _check(
            checks,
            f"sdk:{package_id}:not_published",
            item.get("publishEvidence") is None,
            str(item.get("publishEvidence")),
        )
        results.append(
            {
                "language": item["language"],
                "candidateName": item["candidateName"],
                "status": item["status"],
                "sourcePath": item["sourcePath"],
            }
        )
    return results


def _validate_sandbox_token_contract(
    contract: dict[str, Any], sandbox: dict[str, Any], gateway_path: Path, checks: list[dict[str, Any]]
) -> None:
    _check(checks, "token:schema", contract.get("schemaVersion") == 1, str(contract.get("schemaVersion")))
    _check(checks, "token:kind", contract.get("kind") == "fatecat.sandbox_token_contract", str(contract.get("kind")))
    _check(checks, "token:status", contract["status"] == "contract_only", contract["status"])
    _check(
        checks, "token:live_status", contract["liveServiceStatus"] == "not_implemented", contract["liveServiceStatus"]
    )
    _check(
        checks,
        "token:local_gateway_link",
        contract["localGatewayContract"] == _rel(gateway_path),
        contract["localGatewayContract"],
    )
    _check(
        checks,
        "token:material_policy",
        contract["tokenMaterialPolicy"] == "no_real_tokens_in_repo",
        contract["tokenMaterialPolicy"],
    )
    _check(
        checks,
        "token:header_shape",
        "<sandbox-token>" in contract["authorizationHeaderShape"],
        contract["authorizationHeaderShape"],
    )
    required_claims = set(contract["tokenClaims"]["required"])
    _check(
        checks, "token:required_claims", {"scope", "sandbox", "exp"} <= required_claims, str(sorted(required_claims))
    )
    _check(
        checks,
        "token:forbidden_claims",
        {"production_access", "admin", "secret_material"} <= set(contract["tokenClaims"]["forbidden"]),
        str(contract["tokenClaims"]["forbidden"]),
    )
    fixture_ids = {item["id"] for item in sandbox["fixtures"]}
    for scope in contract["scopes"]:
        _check(
            checks,
            f"token:scope:{scope['scope']}:fixture",
            scope["sandboxFixtureId"] in fixture_ids,
            scope["sandboxFixtureId"],
        )
        _check(
            checks,
            f"token:scope:{scope['scope']}:endpoint",
            scope["allowedEndpoint"].startswith("/capabilities/"),
            scope["allowedEndpoint"],
        )
        _check(
            checks,
            f"token:scope:{scope['scope']}:gateway_endpoint",
            scope["localGatewayEndpoint"].startswith("/sandbox/capabilities/"),
            scope["localGatewayEndpoint"],
        )
    _check(
        checks,
        "token:negative_rules",
        len(contract.get("negativeRules", [])) >= 3,
        str(contract.get("negativeRules", [])),
    )


def _validate_sandbox_gateway_contract(
    gateway: dict[str, Any], token_contract: dict[str, Any], sandbox: dict[str, Any], checks: list[dict[str, Any]]
) -> None:
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
        "gateway:gate_command",
        gateway["validation"]["gateCommand"] == "bash scripts/sandbox-access-gateway-gate.sh",
        gateway["validation"]["gateCommand"],
    )
    token_scopes = {item["scope"] for item in token_contract["scopes"]}
    fixture_ids = {item["id"] for item in sandbox["fixtures"]}
    for rule in gateway.get("scopeRules", []):
        _check(checks, f"gateway:scope:{rule['scope']}:token", rule["scope"] in token_scopes, rule["scope"])
        _check(
            checks,
            f"gateway:scope:{rule['scope']}:fixture",
            rule["fixtureId"] in fixture_ids,
            rule["fixtureId"],
        )
        _check(
            checks,
            f"gateway:scope:{rule['scope']}:endpoint",
            rule["gatewayEndpoint"].startswith("/sandbox/capabilities/"),
            rule["gatewayEndpoint"],
        )


def _validate_api_changelog(changelog: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    _check(checks, "changelog:schema", changelog.get("schemaVersion") == 1, str(changelog.get("schemaVersion")))
    _check(checks, "changelog:kind", changelog.get("kind") == "fatecat.api_changelog", str(changelog.get("kind")))
    _check(checks, "changelog:version", changelog["currentApiVersion"] == "v1", changelog["currentApiVersion"])
    _check(
        checks, "changelog:human_guide_exists", _repo_path(changelog["humanGuide"]).exists(), changelog["humanGuide"]
    )
    policy = changelog["compatibilityPolicy"]
    _check(
        checks,
        "changelog:breaking_policy",
        "Breaking changes require" in policy["breakingChangePolicy"],
        policy["breakingChangePolicy"],
    )
    entries = changelog.get("entries")
    _check(checks, "changelog:entries", isinstance(entries, list) and len(entries) >= 2, str(len(entries or [])))
    entry_ids = {entry["id"] for entry in entries}
    _check(
        checks,
        "changelog:0067_entry",
        "api-changelog.0067.developer-platform-contract" in entry_ids,
        str(sorted(entry_ids)),
    )
    for entry in entries:
        _check(
            checks,
            f"changelog:{entry['id']}:compatibility",
            entry["compatibility"] == "backward_compatible",
            entry["compatibility"],
        )
        if entry["migrationRequired"]:
            _check(
                checks,
                f"changelog:{entry['id']}:migration",
                bool(entry.get("migrationGuide")),
                "migration guide required",
            )
        for evidence_path in entry.get("evidence", []):
            _check(
                checks,
                f"changelog:{entry['id']}:evidence:{evidence_path}",
                _repo_path(evidence_path).exists(),
                evidence_path,
            )


def _validate_sandbox(sandbox: dict[str, Any], checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    _check(checks, "sandbox:schema", sandbox.get("schemaVersion") == 1, str(sandbox.get("schemaVersion")))
    _check(checks, "sandbox:privacy", "北京" in sandbox["privacyBoundary"], sandbox["privacyBoundary"])
    fixtures = sandbox.get("fixtures")
    _check(checks, "sandbox:fixtures", isinstance(fixtures, list) and len(fixtures) >= 2, str(len(fixtures or [])))
    results: list[dict[str, Any]] = []
    for fixture in fixtures:
        _check(checks, f"sandbox:{fixture['id']}:method", fixture["method"] == "POST", fixture["method"])
        _check(
            checks,
            f"sandbox:{fixture['id']}:birth_place",
            _birth_place(fixture["request"]) == "北京" or "测试" in json.dumps(fixture["request"], ensure_ascii=False),
            json.dumps(fixture["request"], ensure_ascii=False),
        )
        _check(
            checks,
            f"sandbox:{fixture['id']}:expected_success",
            fixture["expected"]["success"] is True,
            str(fixture["expected"]),
        )
        results.append({"id": fixture["id"], "capabilityId": fixture["capabilityId"], "endpoint": fixture["endpoint"]})
    return results


def run_gate(
    *,
    platform_path: Path = DEFAULT_PLATFORM,
    sandbox_path: Path = DEFAULT_SANDBOX,
    sandbox_auth_contract_path: Path = DEFAULT_TOKEN_CONTRACT,
    sandbox_gateway_path: Path = DEFAULT_SANDBOX_GATEWAY,
    changelog_path: Path = DEFAULT_CHANGELOG,
) -> dict[str, Any]:
    platform = _load_json(platform_path)
    sandbox = _load_json(sandbox_path)
    token_contract = _load_json(sandbox_auth_contract_path)
    sandbox_gateway = _load_json(sandbox_gateway_path)
    changelog = _load_json(changelog_path)
    checks: list[dict[str, Any]] = []

    _check(checks, "platform:schema", platform.get("schemaVersion") == 1, str(platform.get("schemaVersion")))
    _check(checks, "platform:kind", platform.get("kind") == "fatecat.developer_platform", str(platform.get("kind")))
    _check(checks, "platform:status", platform["status"] == "baseline", platform["status"])
    _check(checks, "platform:privacy", "real tokens" in platform["privacyBoundary"], platform["privacyBoundary"])
    _check(
        checks,
        "platform:token_contract_link",
        platform["sandbox"]["tokenContract"] == _rel(sandbox_auth_contract_path),
        platform["sandbox"]["tokenContract"],
    )
    _check(
        checks,
        "platform:sandbox_gateway_link",
        platform["sandbox"]["accessGatewayContract"] == _rel(sandbox_gateway_path),
        platform["sandbox"]["accessGatewayContract"],
    )
    _check(
        checks,
        "platform:sandbox_gateway_command",
        platform["validation"]["sandboxGatewayGateCommand"] == "bash scripts/sandbox-access-gateway-gate.sh",
        platform["validation"]["sandboxGatewayGateCommand"],
    )
    _check(
        checks,
        "platform:changelog_link",
        platform["apiChangelog"]["machineContract"] == _rel(changelog_path),
        platform["apiChangelog"]["machineContract"],
    )
    _check(
        checks,
        "platform:live_sandbox_not_implemented",
        platform["sandbox"]["livePublicSandboxStatus"] == "not_implemented",
        platform["sandbox"]["livePublicSandboxStatus"],
    )
    _check(
        checks,
        "platform:gate_command",
        platform["validation"]["gateCommand"] == "bash scripts/developer-platform-gate.sh",
        platform["validation"]["gateCommand"],
    )

    sdk_packages = _validate_sdk_package_baseline(platform, checks)
    sandbox_fixtures = _validate_sandbox(sandbox, checks)
    _validate_sandbox_token_contract(token_contract, sandbox, sandbox_gateway_path, checks)
    _validate_sandbox_gateway_contract(sandbox_gateway, token_contract, sandbox, checks)
    _validate_api_changelog(changelog, checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.developer_platform_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "platform": _rel(platform_path),
        "sandboxTokenContract": _rel(sandbox_auth_contract_path),
        "sandboxAccessGateway": _rel(sandbox_gateway_path),
        "apiChangelog": _rel(changelog_path),
        "summary": {
            "sdkPackageCandidates": len(sdk_packages),
            "sandboxFixtures": len(sandbox_fixtures),
            "checks": len(checks),
            "publishedSdkPackages": 0,
            "liveSandboxTokenService": False,
            "localSandboxGateway": True,
        },
        "sdkPackages": sdk_packages,
        "sandboxFixtures": sandbox_fixtures,
        "checks": checks,
        "privacyBoundary": platform["privacyBoundary"],
        "limitations": platform["limitations"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 FateCat developer platform baseline。")
    parser.add_argument("--platform", type=Path, default=DEFAULT_PLATFORM, help="developer platform contract path")
    parser.add_argument("--sandbox", type=Path, default=DEFAULT_SANDBOX, help="sandbox fixture contract path")
    parser.add_argument(
        "--sandbox-token-contract", type=Path, default=DEFAULT_TOKEN_CONTRACT, help="sandbox token contract path"
    )
    parser.add_argument(
        "--sandbox-gateway", type=Path, default=DEFAULT_SANDBOX_GATEWAY, help="sandbox access gateway contract path"
    )
    parser.add_argument("--api-changelog", type=Path, default=DEFAULT_CHANGELOG, help="API changelog contract path")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            platform_path=args.platform,
            sandbox_path=args.sandbox,
            sandbox_auth_contract_path=args.sandbox_token_contract,
            sandbox_gateway_path=args.sandbox_gateway,
            changelog_path=args.api_changelog,
        )
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], **summary["summary"]}, ensure_ascii=False))
        return 0
    except DeveloperPlatformGateError as exc:
        error_summary = {
            "schemaVersion": 1,
            "kind": "fatecat.developer_platform_gate",
            "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "status": "failed",
            "error": str(exc),
        }
        write_summary(error_summary, args.output_json)
        print(f"developer platform gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
