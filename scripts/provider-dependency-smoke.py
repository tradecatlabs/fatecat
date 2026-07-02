#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "providers" / "dependency-smoke.json"
)

SAMPLE_PAYLOADS: dict[str, dict[str, Any]] = {
    "bazi": {
        "birthDateTime": "1990-01-01 08:00:00",
        "gender": "male",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "name": "测试用户",
        "birthPlace": "北京市",
        "useTrueSolarTime": True,
    },
    "ziwei": {
        "birthDateTime": "1990-01-01 08:00:00",
        "gender": "male",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "name": "测试用户",
        "birthPlace": "北京市",
        "useTrueSolarTime": True,
    },
    "almanac": {
        "dateRange": {"start": "2026-07-02", "end": "2026-07-04"},
        "eventType": "开业",
        "place": "北京市",
    },
    "meihua": {
        "question": "测试问题",
        "castMethod": "number",
        "castValue": "3,8",
        "place": "北京市",
    },
}

EXPECTED_DATA_KEYS: dict[str, tuple[str, ...]] = {
    "bazi": ("fourPillars", "analysisEvidence", "accuracyGuards"),
    "ziwei": ("ziweiChart", "analysisEvidence", "ziweiGoldenGuards"),
    "almanac": ("days", "recommendations", "analysisEvidence"),
    "meihua": ("hexagrams", "bodyUse", "analysisEvidence"),
}


class ProviderDependencySmokeError(RuntimeError):
    """provider dependency smoke 未满足预期。"""


def _load_runtime():
    if str(FATE_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(FATE_CORE_SRC))
    from fate_core.capabilities import (  # noqa: PLC0415
        CapabilityExecutor,
        CapabilityInput,
        get_provider_for_capability,
        list_capabilities,
    )

    return CapabilityExecutor, CapabilityInput, get_provider_for_capability, list_capabilities


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise ProviderDependencySmokeError(f"{name}: {details}")


def run_smoke() -> dict[str, Any]:
    CapabilityExecutor, CapabilityInput, get_provider_for_capability, list_capabilities = _load_runtime()
    executor = CapabilityExecutor()
    checks: list[dict[str, Any]] = []
    provider_results: list[dict[str, Any]] = []

    production_capabilities = [item for item in list_capabilities() if item.status == "production"]
    _check(checks, "production_capability_count", bool(production_capabilities), str(len(production_capabilities)))

    for capability in production_capabilities:
        capability_id = capability.capability_id
        payload = SAMPLE_PAYLOADS.get(capability_id)
        _check(checks, f"{capability_id}:fixture_exists", payload is not None, "脱敏固定样例存在")

        provider = get_provider_for_capability(capability)
        provider_metadata = provider.metadata().as_dict()
        provider_health = provider.health().as_dict()
        _check(
            checks,
            f"{capability_id}:provider_health_ready",
            provider_health.get("status") == "ready",
            str(provider_health.get("status")),
        )

        started = time.perf_counter()
        result = executor.execute(CapabilityInput(capability_id=capability_id, payload=payload or {}))
        duration_ms = round((time.perf_counter() - started) * 1000, 3)

        data = result.data
        evidence = result.evidence
        _check(checks, f"{capability_id}:status_production", result.status == "production", result.status)
        _check(checks, f"{capability_id}:data_is_dict", isinstance(data, dict), type(data).__name__)
        _check(checks, f"{capability_id}:evidence_is_dict", isinstance(evidence, dict), type(evidence).__name__)
        for key in EXPECTED_DATA_KEYS.get(capability_id, ()):
            _check(checks, f"{capability_id}:data_key:{key}", key in data, "present")

        provider_results.append(
            {
                "capabilityId": capability_id,
                "providerId": provider_metadata["providerId"],
                "engineVersion": provider_metadata["engineVersion"],
                "healthStatus": provider_health.get("status"),
                "dependencyRefs": provider_metadata.get("sourcePolicy", {}).get("supplyChainRefs", []),
                "durationMs": duration_ms,
                "dataKeys": sorted(data.keys())[:24],
                "evidenceKeys": sorted(evidence.keys()),
            }
        )

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "smokeScope": "local_dependency_fixture_execution",
        "externalConnectivity": "外部连通验证待执行",
        "capabilityCount": len(production_capabilities),
        "providerCount": len({item["providerId"] for item in provider_results}),
        "providers": provider_results,
        "checks": checks,
        "privacyBoundary": "provider dependency smoke 只使用北京/测试用户脱敏固定样例，不读取真实 .env、token、secret、DSN、用户报告正文或生产外部账号。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 production provider dependency smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "providers": summary["providerCount"]}, ensure_ascii=False))
        return 0
    except ProviderDependencySmokeError as exc:
        print(f"provider dependency smoke error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
