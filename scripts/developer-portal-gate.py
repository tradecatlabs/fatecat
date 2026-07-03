#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import py_compile
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
DEVELOPER_ROOT = REPO_ROOT / "contracts" / "fate" / "developer"
DEFAULT_PORTAL = DEVELOPER_ROOT / "developer-portal.json"
DEFAULT_PLATFORM = DEVELOPER_ROOT / "developer-platform.json"
DEFAULT_SDK_RELEASE = DEVELOPER_ROOT / "sdk-release-baseline.json"
DEFAULT_SANDBOX = DEVELOPER_ROOT / "sandbox.json"
DEFAULT_SANDBOX_GATEWAY = DEVELOPER_ROOT / "sandbox-access-gateway.json"
DEFAULT_SNAPSHOT = DEVELOPER_ROOT / "sandbox-output-snapshot.json"
DEFAULT_CHANGELOG = DEVELOPER_ROOT / "api-changelog.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "developer-portal-gate.json"
)

EXPORT_OPENAPI_PATH = REPO_ROOT / "scripts" / "export-openapi.py"
DEVELOPER_PLATFORM_GATE_PATH = REPO_ROOT / "scripts" / "developer-platform-gate.py"
DEVELOPER_DOCS_SMOKE_PATH = REPO_ROOT / "scripts" / "developer-docs-smoke.py"

FORBIDDEN_FRAGMENTS = [
    "\u6d4e\u5357\u5e02\u5386\u4e0b\u533a",
    "\u6df1\u5733",
    "\u5f20\u4e09",
    "sk-live",
    "xoxb-",
    "BEGIN RSA",
    "BEGIN OPENSSH",
    "DATABASE_URL=",
    "DB_DSN=",
    "postgres://",
]


class DeveloperPortalGateError(RuntimeError):
    """开发者门户 release baseline gate 未满足预期。"""


def _load_script_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise DeveloperPortalGateError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export_openapi = _load_script_module("fatecat_export_openapi_for_portal_gate", EXPORT_OPENAPI_PATH)
developer_platform_gate = _load_script_module(
    "fatecat_developer_platform_gate_for_portal_gate", DEVELOPER_PLATFORM_GATE_PATH
)
developer_docs_smoke = _load_script_module("fatecat_developer_docs_smoke_for_portal_gate", DEVELOPER_DOCS_SMOKE_PATH)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DeveloperPortalGateError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DeveloperPortalGateError(f"JSON 格式错误: {path}: {exc}") from exc


def _repo_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise DeveloperPortalGateError(f"路径必须是仓库相对路径且不得越界: {relative_path}")
    resolved = (REPO_ROOT / path).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise DeveloperPortalGateError(f"路径越过仓库根: {relative_path}") from exc
    return resolved


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise DeveloperPortalGateError(f"{name}: {details}")


def _load_app():
    for path in (str(export_openapi.DELIVERY_SRC), str(export_openapi.FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from main import app  # noqa: PLC0415

    return app


def _scrub_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _scrub_dynamic(item) for key, item in value.items() if key != "calculatedAt"}
    if isinstance(value, list):
        return [_scrub_dynamic(item) for item in value]
    return value


def _canonical_digest(value: Any) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _stable_shape(response_body: dict[str, Any]) -> dict[str, Any]:
    data = response_body.get("data")
    shape: dict[str, Any] = {
        "success": response_body.get("success"),
        "capabilityId": response_body.get("capabilityId"),
        "reportProfile": response_body.get("reportProfile"),
    }
    if isinstance(data, dict):
        if isinstance(data.get("dateRange"), dict):
            shape["dateRangeDays"] = data["dateRange"].get("days")
        if isinstance(data.get("days"), list):
            days = data["days"]
            shape["dayCount"] = len(days)
            shape["firstDayTimeSlotCount"] = len(days[0].get("timeSlots", [])) if days else 0
        if isinstance(data.get("hexagrams"), dict):
            shape["hexagramKeys"] = sorted(data["hexagrams"].keys())
    return shape


def _assert_shape(expected: dict[str, Any], actual: dict[str, Any], fixture_id: str) -> None:
    for key, value in expected.items():
        if actual.get(key) != value:
            raise DeveloperPortalGateError(
                f"snapshot shape mismatch for {fixture_id}: {key} expected={value!r} actual={actual.get(key)!r}"
            )


def _validate_portal(portal: dict[str, Any], platform: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    _check(checks, "portal:schema", portal.get("schemaVersion") == 1, str(portal.get("schemaVersion")))
    _check(checks, "portal:kind", portal.get("kind") == "fatecat.developer_portal", str(portal.get("kind")))
    _check(checks, "portal:status", portal["status"] == "local_release_baseline", portal["status"])
    _check(
        checks,
        "portal:external_status",
        portal["externalPortalStatus"] == "not_implemented",
        portal["externalPortalStatus"],
    )
    _check(checks, "portal:human_doc", _repo_path(portal["humanPortal"]).exists(), portal["humanPortal"])
    _check(
        checks,
        "portal:platform_link",
        platform["developerPortal"]["machineContract"] == _rel(DEFAULT_PORTAL),
        platform["developerPortal"]["machineContract"],
    )
    required_contracts = set(portal["machineContracts"].values())
    expected_contracts = {
        _rel(DEFAULT_PLATFORM),
        _rel(DEFAULT_SDK_RELEASE),
        _rel(DEFAULT_SANDBOX),
        "contracts/fate/developer/sandbox-token-contract.json",
        _rel(DEFAULT_SANDBOX_GATEWAY),
        _rel(DEFAULT_SNAPSHOT),
        _rel(DEFAULT_CHANGELOG),
    }
    _check(
        checks, "portal:machine_contracts", expected_contracts <= required_contracts, str(sorted(required_contracts))
    )
    for contract_path in required_contracts:
        _check(checks, f"portal:contract_exists:{contract_path}", _repo_path(contract_path).exists(), contract_path)


def _run_sdk_smokes(sdk_release: dict[str, Any], checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    _check(checks, "sdk_release:schema", sdk_release.get("schemaVersion") == 1, str(sdk_release.get("schemaVersion")))
    _check(
        checks,
        "sdk_release:kind",
        sdk_release.get("kind") == "fatecat.sdk_release_baseline",
        str(sdk_release.get("kind")),
    )
    _check(checks, "sdk_release:status", sdk_release["status"] == "local_release_candidate", sdk_release["status"])
    _check(
        checks,
        "sdk_release:not_published",
        sdk_release["packageRegistryStatus"] == "not_published",
        sdk_release["packageRegistryStatus"],
    )

    candidates = sdk_release.get("packageCandidates")
    _check(checks, "sdk_release:candidates", isinstance(candidates, list) and len(candidates) >= 4, str(candidates))
    results: list[dict[str, Any]] = []
    for item in candidates:
        source_path = _repo_path(item["sourcePath"])
        _check(checks, f"sdk:{item['candidateName']}:source", source_path.exists(), item["sourcePath"])
        _check(checks, f"sdk:{item['candidateName']}:publish", item.get("publishEvidence") is None, "not_published")
        smoke_type = item["smoke"]["type"]
        result = {"candidateName": item["candidateName"], "language": item["language"], "smoke": smoke_type}
        if smoke_type == "python_compile":
            py_compile.compile(str(source_path), doraise=True)
            result["status"] = "passed"
        elif smoke_type == "bash_syntax":
            completed = subprocess.run(
                ["bash", "-n", str(source_path)], cwd=REPO_ROOT, capture_output=True, text=True, timeout=30
            )
            _check(
                checks, f"sdk:{item['candidateName']}:bash_syntax", completed.returncode == 0, completed.stderr or "ok"
            )
            result["status"] = "passed"
        elif smoke_type == "node_syntax_or_shape":
            node_bin = shutil.which("node")
            if node_bin:
                completed = subprocess.run(
                    [node_bin, "--check", str(source_path)],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                _check(
                    checks,
                    f"sdk:{item['candidateName']}:node_syntax",
                    completed.returncode == 0,
                    completed.stderr or "ok",
                )
                result["status"] = "passed"
            else:
                _check(
                    checks,
                    f"sdk:{item['candidateName']}:node_shape",
                    "fetch(" in source_path.read_text(encoding="utf-8"),
                    "node unavailable; validated fetch shape",
                )
                result["status"] = "passed_shape_only"
        elif smoke_type == "json_shape":
            payload = _load_json(source_path)
            _check(
                checks,
                f"sdk:{item['candidateName']}:tool",
                payload.get("tool") == "fatecat.capabilities.calculate",
                "tool shape",
            )
            result["status"] = "passed"
        else:
            raise DeveloperPortalGateError(f"unknown SDK smoke type: {smoke_type}")
        results.append(result)
    return results


def _validate_snapshot(
    *,
    sandbox: dict[str, Any],
    snapshot: dict[str, Any],
    checks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    _check(checks, "snapshot:schema", snapshot.get("schemaVersion") == 1, str(snapshot.get("schemaVersion")))
    _check(
        checks,
        "snapshot:kind",
        snapshot.get("kind") == "fatecat.sandbox_output_snapshot",
        str(snapshot.get("kind")),
    )
    _check(checks, "snapshot:status", snapshot["status"] == "local_fixed_snapshot", snapshot["status"])
    _check(
        checks,
        "snapshot:no_report_body_boundary",
        "full response bodies" in snapshot["privacyBoundary"],
        snapshot["privacyBoundary"],
    )

    fixtures_by_id = {item["id"]: item for item in sandbox["fixtures"]}
    snapshot_items = snapshot.get("fixtures")
    _check(
        checks,
        "snapshot:fixtures",
        isinstance(snapshot_items, list) and len(snapshot_items) == len(fixtures_by_id),
        str(len(snapshot_items or [])),
    )

    app = _load_app()
    client = TestClient(app)
    results: list[dict[str, Any]] = []
    for item in snapshot_items:
        fixture = fixtures_by_id.get(item["fixtureId"])
        _check(checks, f"snapshot:{item['fixtureId']}:fixture", fixture is not None, item["fixtureId"])
        assert fixture is not None
        response = client.request(fixture["method"], fixture["endpoint"], json=fixture["request"])
        _check(
            checks,
            f"snapshot:{item['fixtureId']}:status",
            response.status_code == fixture["expected"]["httpStatus"],
            str(response.status_code),
        )
        body = response.json()
        digest = _canonical_digest(_scrub_dynamic(body))
        _check(checks, f"snapshot:{item['fixtureId']}:digest", digest == item["responseSha256"], digest)
        actual_shape = _stable_shape(body)
        _assert_shape(item["stableShape"], actual_shape, item["fixtureId"])
        results.append(
            {
                "fixtureId": item["fixtureId"],
                "capabilityId": item["capabilityId"],
                "digest": digest,
                "status": "passed",
            }
        )
    return results


def _validate_changelog(changelog: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    entry_ids = {entry["id"] for entry in changelog.get("entries", [])}
    _check(
        checks,
        "changelog:0086_entry",
        "api-changelog.0086.developer-portal-sdk-release-baseline" in entry_ids,
        str(sorted(entry_ids)),
    )
    for entry in changelog.get("entries", []):
        for evidence_path in entry.get("evidence", []):
            _check(
                checks,
                f"changelog:{entry['id']}:evidence:{evidence_path}",
                _repo_path(evidence_path).exists(),
                evidence_path,
            )


def _validate_privacy(paths: list[Path], checks: list[dict[str, Any]]) -> None:
    findings: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_FRAGMENTS:
            if fragment in text:
                findings.append(f"{_rel(path)}:{fragment}")
    _check(checks, "privacy:forbidden_fragments", not findings, ",".join(findings) or "none")


def run_gate(
    *,
    portal_path: Path = DEFAULT_PORTAL,
    platform_path: Path = DEFAULT_PLATFORM,
    sdk_release_path: Path = DEFAULT_SDK_RELEASE,
    sandbox_path: Path = DEFAULT_SANDBOX,
    snapshot_path: Path = DEFAULT_SNAPSHOT,
    changelog_path: Path = DEFAULT_CHANGELOG,
) -> dict[str, Any]:
    portal = _load_json(portal_path)
    platform = _load_json(platform_path)
    sdk_release = _load_json(sdk_release_path)
    sandbox = _load_json(sandbox_path)
    snapshot = _load_json(snapshot_path)
    changelog = _load_json(changelog_path)
    checks: list[dict[str, Any]] = []

    _validate_portal(portal, platform, checks)
    sdk_smokes = _run_sdk_smokes(sdk_release, checks)
    snapshot_results = _validate_snapshot(sandbox=sandbox, snapshot=snapshot, checks=checks)
    _validate_changelog(changelog, checks)
    platform_summary = developer_platform_gate.run_gate()
    docs_summary = developer_docs_smoke.run_smoke()
    _check(checks, "platform_gate:passed", platform_summary["status"] == "passed", platform_summary["status"])
    _check(checks, "docs_smoke:passed", docs_summary["status"] == "passed", docs_summary["status"])
    _validate_privacy(
        [
            portal_path,
            platform_path,
            sdk_release_path,
            sandbox_path,
            snapshot_path,
            changelog_path,
            _repo_path(portal["humanPortal"]),
            _repo_path(platform["sdkReleaseBaseline"]["humanGuide"]),
        ],
        checks,
    )

    return {
        "schemaVersion": 1,
        "kind": "fatecat.developer_portal_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "portal": _rel(portal_path),
        "sdkReleaseBaseline": _rel(sdk_release_path),
        "sandboxOutputSnapshot": _rel(snapshot_path),
        "summary": {
            "sdkPackageCandidates": len(sdk_smokes),
            "sandboxSnapshots": len(snapshot_results),
            "checks": len(checks),
            "externalPortalLive": False,
            "publishedSdkPackages": 0,
            "liveSandboxTokenService": False,
        },
        "sdkSmokes": sdk_smokes,
        "sandboxSnapshots": snapshot_results,
        "checks": checks,
        "privacyBoundary": portal["privacyBoundary"],
        "limitations": portal["limitations"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 FateCat developer portal and SDK release baseline。")
    parser.add_argument("--portal", type=Path, default=DEFAULT_PORTAL, help="developer portal contract path")
    parser.add_argument("--platform", type=Path, default=DEFAULT_PLATFORM, help="developer platform contract path")
    parser.add_argument("--sdk-release", type=Path, default=DEFAULT_SDK_RELEASE, help="SDK release baseline path")
    parser.add_argument("--sandbox", type=Path, default=DEFAULT_SANDBOX, help="sandbox fixture contract path")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT, help="sandbox output snapshot path")
    parser.add_argument("--api-changelog", type=Path, default=DEFAULT_CHANGELOG, help="API changelog contract path")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            portal_path=args.portal,
            platform_path=args.platform,
            sdk_release_path=args.sdk_release,
            sandbox_path=args.sandbox,
            snapshot_path=args.snapshot,
            changelog_path=args.api_changelog,
        )
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], **summary["summary"]}, ensure_ascii=False))
        return 0
    except (
        DeveloperPortalGateError,
        developer_platform_gate.DeveloperPlatformGateError,
        developer_docs_smoke.DeveloperDocsSmokeError,
        export_openapi.OpenAPIExportError,
        py_compile.PyCompileError,
    ) as exc:
        error_summary = {
            "schemaVersion": 1,
            "kind": "fatecat.developer_portal_gate",
            "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "status": "failed",
            "error": str(exc),
        }
        write_summary(error_summary, args.output_json)
        print(f"developer portal gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
