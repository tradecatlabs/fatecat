#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
CONTROL_PLANE_REGISTRY = REPO_ROOT / "contracts" / "fate" / "control-plane" / "registry.json"
CONTROL_PLANE_SCHEMA = REPO_ROOT / "contracts" / "fate" / "control-plane" / "schemas" / "control-plane.schema.json"
CAPABILITY_REGISTRY = REPO_ROOT / "contracts" / "fate" / "capabilities" / "registry.json"
EVALUATION_REGISTRY = REPO_ROOT / "contracts" / "fate" / "evaluations" / "registry.json"
RELEASE_GATE = REPO_ROOT / "contracts" / "fate" / "delivery" / "release-gate.json"
PROVIDER_LIFECYCLE_GATE = REPO_ROOT / "scripts" / "provider-lifecycle-gate.py"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "control-plane-gate.json"


class ControlPlaneGateError(RuntimeError):
    """control-plane gate 未满足预期。"""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(condition: bool, name: str, detail: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": detail})
    if not condition:
        raise ControlPlaneGateError(f"{name}: {detail}")


def _repo_path_exists(ref: str) -> bool:
    if not ref or ref.startswith("/") or "://" in ref or ref.startswith("runtime:"):
        return True
    if ref.startswith("python -m ") or ref.startswith("bash "):
        return True
    if "<" in ref or ">" in ref:
        command_path = ref.split()[1] if ref.startswith("bash ") and len(ref.split()) > 1 else ""
        return bool(command_path and (REPO_ROOT / command_path).exists())
    return (REPO_ROOT / ref).exists()


def _load_runtime():
    if str(FATE_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(FATE_CORE_SRC))
    from fate_core.capabilities import list_capabilities, list_providers  # noqa: PLC0415

    return list_capabilities, list_providers


def _load_provider_lifecycle_gate():
    spec = importlib.util.spec_from_file_location("fatecat_provider_lifecycle_gate", PROVIDER_LIFECYCLE_GATE)
    if spec is None or spec.loader is None:
        raise ControlPlaneGateError("provider lifecycle gate import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_registry_shape(
    registry: dict[str, Any], schema: dict[str, Any], checks: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    for field_name in schema["requiredRegistryFields"]:
        _check(field_name in registry, f"registry.required.{field_name}", "present", checks)

    resources = registry.get("resources", [])
    _check(isinstance(resources, list) and bool(resources), "registry.resources.non_empty", "resources present", checks)
    by_id: dict[str, dict[str, Any]] = {}
    for resource in resources:
        resource_id = str(resource.get("id", ""))
        _check(resource_id not in by_id, f"resource.unique.{resource_id}", "unique id", checks)
        by_id[resource_id] = resource
        for field_name in schema["requiredResourceFields"]:
            _check(field_name in resource, f"{resource_id}.required.{field_name}", "present", checks)
        _check(
            resource["resourceType"] in schema["allowedResourceTypes"],
            f"{resource_id}.resource_type",
            resource["resourceType"],
            checks,
        )
        for field_name in schema["requiredSpecFields"]:
            _check(field_name in resource["spec"], f"{resource_id}.spec.{field_name}", "present", checks)
        for field_name in schema["requiredAdmissionFields"]:
            _check(
                field_name in resource["spec"]["admission"], f"{resource_id}.admission.{field_name}", "present", checks
            )
        for field_name in schema["requiredGateFields"]:
            _check(field_name in resource["spec"]["gate"], f"{resource_id}.gate.{field_name}", "present", checks)
        for field_name in schema["requiredStatusFields"]:
            _check(field_name in resource["status"], f"{resource_id}.status.{field_name}", "present", checks)
        for field_name in schema["requiredReconciliationFields"]:
            _check(
                field_name in resource["status"]["reconciliation"],
                f"{resource_id}.reconciliation.{field_name}",
                "present",
                checks,
            )
        _check(
            resource["status"]["phase"] in schema["allowedPhase"],
            f"{resource_id}.phase",
            resource["status"]["phase"],
            checks,
        )
        _check(
            resource["status"]["lastKnownStatePolicy"] in schema["allowedLastKnownStatePolicy"],
            f"{resource_id}.last_known_state_policy",
            resource["status"]["lastKnownStatePolicy"],
            checks,
        )
        _check(
            resource["status"]["reconciliation"]["status"] in schema["allowedReconciliationStatus"],
            f"{resource_id}.reconciliation.status",
            resource["status"]["reconciliation"]["status"],
            checks,
        )
        for link_name, link_ref in resource["links"].items():
            _check(_repo_path_exists(str(link_ref)), f"{resource_id}.link.{link_name}", str(link_ref), checks)
    return by_id


def _validate_capabilities(resource: dict[str, Any], checks: list[dict[str, Any]]) -> dict[str, int]:
    registry = _load_json(CAPABILITY_REGISTRY)
    capabilities = registry["capabilities"]
    counts = Counter(item["status"] for item in capabilities)
    desired = resource["spec"]["desiredState"]
    default_ids = [item["capabilityId"] for item in capabilities if item["defaultVisibility"] == "default"]

    _check(len(capabilities) == desired["totalCapabilities"], "capability.count.total", str(len(capabilities)), checks)
    _check(
        counts["production"] == desired["productionCapabilities"],
        "capability.count.production",
        str(counts["production"]),
        checks,
    )
    _check(
        counts["planned"] == desired["plannedCapabilities"], "capability.count.planned", str(counts["planned"]), checks
    )
    _check(default_ids == [desired["defaultCapabilityId"]], "capability.default.only", ",".join(default_ids), checks)

    for item in capabilities:
        capability_id = item["capabilityId"]
        if item["status"] == "production":
            _check(item["testGate"]["status"] == "passing", f"{capability_id}.production.test_gate", "passing", checks)
            _check(
                not item["engine"]["provider"].startswith("planned."),
                f"{capability_id}.production.provider",
                item["engine"]["provider"],
                checks,
            )
            _check(
                item["engine"]["engineVersion"] != "planned-v0",
                f"{capability_id}.production.engine",
                item["engine"]["engineVersion"],
                checks,
            )
        if item["status"] == "planned":
            _check(
                item["maturity"]["level"] == "L0",
                f"{capability_id}.planned.maturity",
                item["maturity"]["level"],
                checks,
            )
            _check(
                item["testGate"]["status"] == "blocked",
                f"{capability_id}.planned.test_gate",
                item["testGate"]["status"],
                checks,
            )
            _check(
                item["engine"]["provider"].startswith("planned."),
                f"{capability_id}.planned.provider",
                item["engine"]["provider"],
                checks,
            )
            _check(
                item["engine"]["engineVersion"] == "planned-v0",
                f"{capability_id}.planned.engine",
                item["engine"]["engineVersion"],
                checks,
            )
            _check(
                item["report"]["markdownDefault"] is False, f"{capability_id}.planned.markdown_default", "false", checks
            )
    return {"total": len(capabilities), "production": counts["production"], "planned": counts["planned"]}


def _validate_providers(resource: dict[str, Any], checks: list[dict[str, Any]]) -> dict[str, int]:
    list_capabilities, list_providers = _load_runtime()
    production_provider_ids = {item.provider for item in list_capabilities() if item.status == "production"}
    runtime_provider_ids = {provider.metadata().provider_id for provider in list_providers()}
    desired = resource["spec"]["desiredState"]

    _check(
        len(runtime_provider_ids) == desired["productionProviderCount"],
        "provider.count.production",
        str(len(runtime_provider_ids)),
        checks,
    )
    _check(
        runtime_provider_ids == production_provider_ids,
        "provider.coverage.production",
        ",".join(sorted(runtime_provider_ids)),
        checks,
    )

    lifecycle_gate = _load_provider_lifecycle_gate().run_gate()
    _check(lifecycle_gate["status"] == "passed", "provider.lifecycle_gate", lifecycle_gate["status"], checks)
    _check(
        lifecycle_gate["providerCount"] == desired["productionProviderCount"],
        "provider.lifecycle_gate.count",
        str(lifecycle_gate["providerCount"]),
        checks,
    )
    return {"productionProviders": len(runtime_provider_ids)}


def _validate_release_gate(resource: dict[str, Any], checks: list[dict[str, Any]]) -> dict[str, Any]:
    release_gate = _load_json(RELEASE_GATE)
    desired = resource["spec"]["desiredState"]

    _check(
        release_gate["resourceType"] == "ReleaseGate",
        "release_gate.resource_type",
        release_gate["resourceType"],
        checks,
    )
    _check(
        len(release_gate["requiredEvidence"]) == desired["requiredEvidenceCount"],
        "release_gate.required_evidence_count",
        str(len(release_gate["requiredEvidence"])),
        checks,
    )
    _check("shipGate" in release_gate, "release_gate.ship_gate", "present", checks)
    _check(
        release_gate["shipGate"]["status"] in {"blocked", "pass", "passed"},
        "release_gate.ship_gate_status",
        release_gate["shipGate"]["status"],
        checks,
    )
    _check(bool(release_gate["externalVerification"]), "release_gate.external_verification", "non-empty", checks)
    _check("token" in release_gate["metadata"]["privacy"], "release_gate.privacy_boundary", "token boundary", checks)
    return {"requiredEvidence": len(release_gate["requiredEvidence"]), "shipGate": release_gate["shipGate"]["status"]}


def _validate_evaluation_runs(resource: dict[str, Any], checks: list[dict[str, Any]]) -> dict[str, int]:
    registry = _load_json(EVALUATION_REGISTRY)
    resources = registry["resources"]
    dataset_ids = {item["id"] for item in resources if item["resourceType"] == "Dataset"}
    run_ids = {item["id"] for item in resources if item["resourceType"] == "EvaluationRun"}
    desired = resource["spec"]["desiredState"]

    _check(len(dataset_ids) == desired["datasetCount"], "evaluation.dataset_count", str(len(dataset_ids)), checks)
    _check(len(run_ids) == desired["evaluationRunCount"], "evaluation.run_count", str(len(run_ids)), checks)
    _check(set(desired["requiredRunIds"]) <= run_ids, "evaluation.required_runs", ",".join(sorted(run_ids)), checks)
    for item in resources:
        if item["resourceType"] == "Dataset":
            _check(item["usageRole"] == "evaluation_only", f"{item['id']}.usage_role", item["usageRole"], checks)
        if item["resourceType"] == "EvaluationRun":
            _check(set(item["datasetIds"]) <= dataset_ids, f"{item['id']}.dataset_links", "valid", checks)
            _check(bool(item["commands"]), f"{item['id']}.commands", "non-empty", checks)
    return {"datasets": len(dataset_ids), "evaluationRuns": len(run_ids)}


def run_gate() -> dict[str, Any]:
    schema = _load_json(CONTROL_PLANE_SCHEMA)
    registry = _load_json(CONTROL_PLANE_REGISTRY)
    checks: list[dict[str, Any]] = []
    resources = _validate_registry_shape(registry, schema, checks)

    expected_ids = {
        "control.capabilities",
        "control.providers",
        "control.release_gate",
        "control.evaluation_runs",
    }
    _check(set(resources) == expected_ids, "control_plane.resource_ids", ",".join(sorted(resources)), checks)

    observed = {
        "capabilities": _validate_capabilities(resources["control.capabilities"], checks),
        "providers": _validate_providers(resources["control.providers"], checks),
        "releaseGate": _validate_release_gate(resources["control.release_gate"], checks),
        "evaluationRuns": _validate_evaluation_runs(resources["control.evaluation_runs"], checks),
    }

    return {
        "schemaVersion": 1,
        "kind": "fatecat.control_plane_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "resourceCount": len(resources),
        "observed": observed,
        "checks": checks,
        "privacyBoundary": "control-plane gate reads contracts, provider metadata and registry manifests only; it does not read or output token, secret, DSN, production log, report body or real user input.",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat control-plane resource reconciliation gate。")
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
                    "resources": summary["resourceCount"],
                    "checks": len(summary["checks"]),
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except ControlPlaneGateError as exc:
        print(f"control-plane gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
