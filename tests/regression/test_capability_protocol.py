from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

import fate_core.capabilities.providers as capability_providers
import fate_core.capabilities.registry as capability_registry
from fate_core.capabilities import (
    CapabilityExecutor,
    CapabilityInput,
    get_capability,
    get_provider_for_capability,
    list_capabilities,
    list_providers,
)
from fate_core.capabilities.report_policy import (
    build_markdown_report_policy_gate,
    build_markdown_snapshot_gate,
    build_report_policy_gate,
)

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_DIR = ROOT / "contracts" / "fate" / "capabilities"
DELIVERY_DIR = ROOT / "contracts" / "fate" / "delivery"
EVALUATION_DIR = ROOT / "contracts" / "fate" / "evaluations"
OBSERVABILITY_DIR = ROOT / "contracts" / "fate" / "observability"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_capability_registry_keeps_bazi_as_only_default_production_entry():
    capabilities = list_capabilities()
    by_id = {item.capability_id: item for item in capabilities}

    assert by_id["bazi"].status == "production"
    assert by_id["bazi"].default_visibility == "default"
    assert by_id["bazi"].maturity_level == "L4"
    assert by_id["bazi"].engine_version == "fate-core-bazi-v1"
    assert by_id["bazi"].deterministic is True
    assert by_id["bazi"].evidence_policy["ruleIdRequired"] is True
    assert by_id["bazi"].test_gate["status"] == "passing"
    assert by_id["almanac"].status == "production"
    assert by_id["almanac"].default_visibility == "standalone"
    assert by_id["almanac"].maturity_level == "L3"
    assert by_id["ziwei"].status == "production"
    assert by_id["ziwei"].default_visibility == "standalone"
    assert by_id["ziwei"].maturity_level == "L4"
    assert by_id["ziwei"].engine_version == "fate-core-ziwei-v1"
    assert by_id["meihua"].status == "production"
    assert by_id["meihua"].default_visibility == "standalone"
    assert by_id["meihua"].maturity_level == "L3"
    assert [item.capability_id for item in capabilities if item.default_visibility == "default"] == ["bazi"]
    for capability_id in ["liuyao", "qimen", "daliuren", "fengshui_nine_stars", "name_marriage"]:
        assert by_id[capability_id].status == "planned"
        assert by_id[capability_id].default_visibility == "standalone"
        assert by_id[capability_id].maturity_level == "L0"
        assert by_id[capability_id].engine_version == "planned-v0"
        assert by_id[capability_id].test_gate["status"] == "blocked"


def test_capability_profiles_match_registry_and_do_not_pollute_default_markdown():
    registry_ids = {item.capability_id for item in list_capabilities()}
    profile_paths = sorted((CAPABILITY_DIR / "profiles").glob("*.json"))
    profile_ids = set()

    for path in profile_paths:
        profile = _load_json(path)
        profile_ids.add(profile["capabilityId"])
        if profile["capabilityId"] == "bazi":
            assert profile["markdownDefault"] is True
            assert profile["visibility"] == "default"
        else:
            assert profile["markdownDefault"] is False
            assert profile["visibility"] == "standalone"

    assert profile_ids == registry_ids


def test_capability_schemas_define_required_protocol_boundaries():
    schema = _load_json(CAPABILITY_DIR / "schemas" / "capability.schema.json")
    resource_schema = _load_json(CAPABILITY_DIR / "schemas" / "resource.schema.json")
    provider_schema = _load_json(CAPABILITY_DIR / "schemas" / "provider.schema.json")
    report_schema = _load_json(CAPABILITY_DIR / "schemas" / "report.schema.json")
    error_schema = _load_json(CAPABILITY_DIR / "schemas" / "error.schema.json")
    error_catalog = _load_json(CAPABILITY_DIR / "errors.json")

    assert "capabilityId" in schema["requiredCapabilityFields"]
    assert "maturity" in schema["requiredCapabilityFields"]
    assert "evidencePolicy" in schema["requiredCapabilityFields"]
    assert "testGate" in schema["requiredCapabilityFields"]
    assert schema["allowedStatus"] == ["planned", "experimental", "production"]
    assert schema["allowedMaturityLevel"] == ["L0", "L1", "L2", "L3", "L4"]
    assert "engineVersion" in schema["requiredEngineFields"]
    assert "defaultVisibility=default 必须且只能用于 bazi" in schema["invariants"]
    assert (
        "production 能力必须 testGate.status=passing 且 testGate.commands 至少包含一个本地回归入口"
        in schema["invariants"]
    )
    assert (
        "planned 能力必须 maturity.level=L0、testGate.status=blocked、provider=planned.*、engineVersion=planned-v0"
        in schema["invariants"]
    )
    assert "Capability" in resource_schema["resourceTypes"]
    assert "Provider" in resource_schema["resourceTypes"]
    assert "CalculationJob" in resource_schema["resourceTypes"]
    assert "schemas" in resource_schema["capabilityResourceFields"]
    assert "admission" in resource_schema["capabilityResourceFields"]
    assert "provider" in resource_schema["capabilityResourceFields"]
    assert "providerId" in resource_schema["providerResourceFields"]
    assert "health" in resource_schema["providerResourceFields"]
    assert "Report" in resource_schema["resourceTypes"]
    assert "sections" in resource_schema["reportResourceFields"]
    assert "evidenceRefs" in resource_schema["reportResourceFields"]
    assert "policyGate" in resource_schema["reportResourceFields"]
    assert "Dataset" in resource_schema["resourceTypes"]
    assert "EvaluationRun" in resource_schema["resourceTypes"]
    assert "ObservabilitySignal" in resource_schema["resourceTypes"]
    assert "SecurityControl" in resource_schema["resourceTypes"]
    assert "DeliverySurface" in resource_schema["resourceTypes"]
    assert "ReleaseGate" in resource_schema["resourceTypes"]
    assert "usageRole" in resource_schema["datasetResourceFields"]
    assert "localAvailability" in resource_schema["datasetResourceFields"]
    assert "datasetIds" in resource_schema["evaluationRunResourceFields"]
    assert "lastKnownStatusPolicy" in resource_schema["evaluationRunResourceFields"]
    assert "signalType" in resource_schema["observabilitySignalResourceFields"]
    assert "privacyBoundary" in resource_schema["observabilitySignalResourceFields"]
    assert "controlType" in resource_schema["securityControlResourceFields"]
    assert "implementationRefs" in resource_schema["securityControlResourceFields"]
    assert "externalConnectivity" in resource_schema["securityControlResourceFields"]
    assert "surfaceType" in resource_schema["deliverySurfaceResourceFields"]
    assert "canonicalChain" in resource_schema["deliverySurfaceResourceFields"]
    assert "outputContracts" in resource_schema["deliverySurfaceResourceFields"]
    assert "requiredEvidence" in resource_schema["releaseGateResourceFields"]
    assert "shipGate" in resource_schema["releaseGateResourceFields"]
    assert "providerId" in provider_schema["requiredProviderFields"]
    assert "engineVersion" in provider_schema["requiredProviderFields"]
    assert "health" in provider_schema["requiredProviderFields"]
    for field_name in (
        "versionLock",
        "lifecycle",
        "sourcePolicy",
        "licensePolicy",
        "resourceManifest",
        "promotionGate",
        "deprecation",
    ):
        assert field_name in provider_schema["requiredProviderFields"]
        assert field_name in resource_schema["providerResourceFields"]
    assert provider_schema["allowedLifecycleStage"] == ["validated", "production", "deprecated"]
    assert provider_schema["allowedPromotionGateStatus"] == ["passing", "blocked", "manual"]
    assert (
        "health.status=ready 只表示本地进程内 adapter 可用，不表示真实外部连通验证完成" in provider_schema["invariants"]
    )
    assert (
        "production provider 的 sourcePolicy.supplyChainRefs 若指向 vendor_sources，目标条目必须 productionUseAllowed=true"
        in provider_schema["invariants"]
    )
    assert "capabilityId" in report_schema["requiredReportFields"]
    assert "sections" in report_schema["requiredReportFields"]
    assert "evidenceRefs" in report_schema["requiredReportFields"]
    assert "policyGate" in report_schema["requiredReportFields"]
    assert report_schema["requiredMarkdownResultFields"] == ["reportSystem", "markdown", "policyGate", "snapshotGate"]
    assert set(report_schema["requiredPolicyGateFields"]) >= {
        "version",
        "status",
        "checkedFields",
        "excludedFields",
        "matches",
    }
    assert set(report_schema["requiredSnapshotGateFields"]) >= {
        "version",
        "status",
        "reportSystem",
        "requiredHeadings",
        "missingHeadings",
        "headings",
    }
    assert report_schema["allowedPolicyGateStatus"] == ["pass", "fail"]
    assert report_schema["allowedSnapshotGateStatus"] == ["pass", "fail"]
    assert "Report envelope 只保存交付摘要和引用，不复制完整 data" in report_schema["invariants"]
    assert "policyGate 必须排除 risk.forbiddenClaims，避免风险清单自触发" in report_schema["invariants"]
    assert "Markdown report policyGate 必须扫描用户可见 Markdown 正文" in report_schema["invariants"]
    assert "cancelled" in resource_schema["calculationJobStatuses"]
    assert "idempotencyKey" in resource_schema["calculationJobFields"]
    assert "cancelUrl" in resource_schema["calculationJobFields"]
    assert "code" in error_schema["requiredErrorFields"]
    assert "retryable" in error_schema["requiredErrorFields"]
    error_codes = {item["code"] for item in error_catalog["errors"]}
    assert {
        "FC_CAPABILITY_NOT_FOUND",
        "FC_CAPABILITY_NOT_PRODUCTION",
        "FC_INPUT_INVALID",
        "FC_RATE_LIMITED",
        "FC_TIMEOUT",
    } <= error_codes


def test_evaluation_resource_schemas_define_dataset_and_run_boundaries():
    dataset_schema = _load_json(EVALUATION_DIR / "schemas" / "dataset.schema.json")
    run_schema = _load_json(EVALUATION_DIR / "schemas" / "evaluation-run.schema.json")
    diff_policy = _load_json(EVALUATION_DIR / "diff-policy.json")

    assert dataset_schema["requiredDatasetFields"] == [
        "resourceType",
        "apiVersion",
        "id",
        "name",
        "domain",
        "datasetType",
        "usageRole",
        "status",
        "localAvailability",
        "privacyClass",
        "sourceRef",
        "paths",
        "commands",
        "links",
        "metadata",
    ]
    assert "evaluation_only" in dataset_schema["allowedUsageRole"]
    assert "requires_reference_repo" in dataset_schema["allowedLocalAvailability"]
    assert "benchmark Dataset 不得把标准答案注入生产推理路径" in dataset_schema["invariants"]

    assert "datasetIds" in run_schema["requiredEvaluationRunFields"]
    assert "releaseRequired" in run_schema["requiredEvaluationRunFields"]
    assert "lastKnownStatusPolicy" in run_schema["requiredEvaluationRunFields"]
    assert "offline_benchmark" in run_schema["allowedRunType"]
    assert "tracked_by_task_evidence" in run_schema["allowedLastKnownStatusPolicy"]
    assert run_schema["runnerSummaryFields"] == [
        "schemaVersion",
        "generatedAt",
        "registry",
        "gitCommit",
        "selection",
        "dryRun",
        "summary",
        "runs",
    ]
    assert "EvaluationRun resource 是运行入口和门禁口径，不伪造当前 commit 的运行结果" in run_schema["invariants"]
    assert (
        "本地 runner 必须白名单执行 registry.commands，禁止 shell=True、旧路径 fallback 和真实 secret 注入"
        in (run_schema["invariants"])
    )
    assert diff_policy["thresholds"] == {
        "maxNewFailedRuns": 0,
        "maxMissingRuns": 0,
        "maxFailedCommands": 0,
    }
    assert "benchmark 标准答案" in diff_policy["privacyBoundary"]


def test_evaluation_registry_resources_are_traceable_and_do_not_pollute_production_inputs():
    registry = _load_json(EVALUATION_DIR / "registry.json")
    resources = {item["id"]: item for item in registry["resources"]}

    assert registry["schemas"]["dataset"] == "contracts/fate/evaluations/schemas/dataset.schema.json"
    assert registry["schemas"]["evaluationRun"] == "contracts/fate/evaluations/schemas/evaluation-run.schema.json"
    assert registry["metadata"]["runner"]["command"] == "bash scripts/run-evaluations.sh"
    assert registry["metadata"]["runner"]["defaultMode"] == "all-local-required"
    assert "shell=True" in registry["metadata"]["runner"]["safety"]
    assert registry["metadata"]["diffPolicy"] == "contracts/fate/evaluations/diff-policy.json"
    assert {
        "dataset.solar_terms_1900_2030",
        "dataset.bazi_golden_matrix",
        "dataset.ziwei_golden_cases",
        "dataset.mingli_bench_offline",
        "run.local_ci_quick",
        "run.solar_terms_golden",
        "run.evaluation_dashboard_smoke",
        "run.mingli_bench_offline",
    } <= set(resources)

    dataset_ids = {item_id for item_id, item in resources.items() if item["resourceType"] == "Dataset"}
    for item in resources.values():
        assert item["apiVersion"] == "fatecat.tradecatlabs/v1"
        assert item["links"]["collection"] == "/evaluations"
        assert item["metadata"]["externalConnectivity"]
        if item["resourceType"] == "Dataset":
            assert item["usageRole"] == "evaluation_only"
            assert item["commands"]
            assert item["paths"]
            if item["localAvailability"] == "tracked_in_repo":
                for relative_path in item["paths"]:
                    assert (ROOT / relative_path).exists(), relative_path
            continue

        assert item["resourceType"] == "EvaluationRun"
        assert set(item["datasetIds"]) <= dataset_ids
        assert item["commands"]
        assert item["lastKnownStatusPolicy"] in {
            "not_embedded",
            "tracked_by_task_evidence",
            "tracked_by_ci",
            "external_connectivity_pending",
        }

    mingli_dataset = resources["dataset.mingli_bench_offline"]
    assert mingli_dataset["status"] == "requires_reference_repo"
    assert mingli_dataset["localAvailability"] == "requires_reference_repo"
    assert mingli_dataset["metadata"]["releaseGate"] == "optional"
    assert "标准答案不得进入 production provider" in mingli_dataset["metadata"]["risk"]

    local_ci = resources["run.local_ci_quick"]
    assert local_ci["releaseRequired"] is True
    assert local_ci["gateType"] == "required"
    assert local_ci["lastKnownStatusPolicy"] == "tracked_by_task_evidence"


def test_observability_signal_schema_and_registry_define_available_and_planned_boundaries():
    schema = _load_json(OBSERVABILITY_DIR / "schemas" / "observability-signal.schema.json")
    registry = _load_json(OBSERVABILITY_DIR / "registry.json")
    signals = {item["id"]: item for item in registry["signals"]}

    assert schema["requiredObservabilitySignalFields"] == [
        "resourceType",
        "apiVersion",
        "id",
        "name",
        "signalType",
        "status",
        "endpoint",
        "fields",
        "localVerification",
        "privacyBoundary",
        "externalConnectivity",
        "links",
        "metadata",
    ]
    assert schema["allowedSignalType"] == ["health", "readiness", "metric", "log", "trace", "slo", "alert"]
    assert schema["allowedStatus"] == ["available", "planned", "blocked"]
    assert "planned 信号不得写成生产已验证能力" in schema["invariants"]
    assert "日志类信号不得记录真实 token、secret、DSN、私钥或用户隐私样例" in schema["invariants"]

    assert registry["schemas"]["observabilitySignal"] == (
        "contracts/fate/observability/schemas/observability-signal.schema.json"
    )
    assert registry["metadata"]["smokeCommand"] == "bash scripts/observability-smoke.sh"
    assert "TestClient" in registry["metadata"]["smokeScope"]
    assert registry["metadata"]["traceSloSmokeCommand"] == "bash scripts/observability-trace-slo-smoke.sh"
    assert registry["metadata"]["sloGateCommand"] == "bash scripts/observability-slo-gate.sh"
    assert registry["schemas"]["sloPolicy"] == "contracts/fate/observability/slo-policy.json"
    assert registry["schemas"]["alertRules"] == "contracts/fate/observability/alert-rules.json"
    assert {
        "signal.health",
        "signal.readiness",
        "signal.http_request_metrics",
        "signal.job_and_queue_metrics",
        "signal.request_id_and_structured_logs",
        "signal.provider_report_traces",
        "signal.slo_and_alerts",
    } <= set(signals)

    for item in signals.values():
        assert item["resourceType"] == "ObservabilitySignal"
        assert item["apiVersion"] == "fatecat.tradecatlabs/v1"
        assert item["links"]["collection"] == "/observability"
        assert item["privacyBoundary"]
        assert item["externalConnectivity"]
        assert item["metadata"]["risk"]
        if item["status"] == "available":
            assert item["localVerification"]
            assert item["endpoint"] != "not_available"
            continue
        assert item["status"] == "planned"
        assert item["localVerification"] == []
        assert item["endpoint"] == "not_available"
        assert item["externalConnectivity"] in {"requires_collector", "requires_production_traffic"}

    http_metrics = signals["signal.http_request_metrics"]
    assert http_metrics["status"] == "available"
    assert "fatecat_requests_total" in http_metrics["fields"]
    assert "不得包含用户姓名" in http_metrics["privacyBoundary"]

    traces = signals["signal.provider_report_traces"]
    assert traces["status"] == "available"
    assert traces["endpoint"] == "application logs"
    assert "traceId" in traces["fields"]
    assert traces["externalConnectivity"] == "external_connectivity_pending"
    assert "collector" in traces["metadata"]["risk"]

    slo_alerts = signals["signal.slo_and_alerts"]
    assert slo_alerts["status"] == "available"
    assert "contracts/fate/observability/slo-policy.json" in slo_alerts["endpoint"]
    assert slo_alerts["externalConnectivity"] == "external_connectivity_pending"


def test_security_control_schema_and_registry_define_gate_boundaries():
    schema = _load_json(SECURITY_DIR / "schemas" / "security-control.schema.json")
    registry = _load_json(SECURITY_DIR / "registry.json")
    controls = {item["id"]: item for item in registry["controls"]}

    assert schema["requiredSecurityControlFields"] == [
        "resourceType",
        "apiVersion",
        "id",
        "name",
        "controlType",
        "status",
        "scope",
        "envVars",
        "implementationRefs",
        "localVerification",
        "privacyBoundary",
        "externalConnectivity",
        "links",
        "metadata",
    ]
    assert {
        "audit_log",
        "auth",
        "cors",
        "rate_limit",
        "request_limit",
        "headers",
        "identity",
        "siem",
        "owasp_api_regression",
        "privacy",
        "rbac",
        "retention",
        "webhook_signature",
        "source_hygiene",
        "secret_scan",
        "release_gate",
        "production_readiness",
    } == set(schema["allowedControlType"])
    assert (
        "SecurityControl resource 只登记控制契约，不保存真实 token、secret、DSN、私钥、证书或 webhook 地址"
        in schema["invariants"]
    )
    assert "release_gate 不得伪造当前 commit 的远端 CI、live smoke 或外部生产验证结果" in schema["invariants"]

    assert registry["schemas"]["securityControl"] == "contracts/fate/security/schemas/security-control.schema.json"
    assert registry["metadata"]["smokeCommand"] == "bash scripts/security-smoke.sh"
    assert "TestClient" in registry["metadata"]["smokeScope"]
    assert {
        "control.record_token_access",
        "control.cors_allowlist",
        "control.rate_limit",
        "control.request_body_limit",
        "control.response_security_headers",
        "control.rbac_policy",
        "control.production_identity_oidc",
        "control.external_siem_immutable_audit",
        "control.retention_cleanup_plan",
        "control.owasp_api_security_regression",
        "control.audit_event_log",
        "control.retention_policy",
        "control.privacy_fixture_policy",
        "control.source_hygiene_gate",
        "control.secret_scan_gate",
        "control.public_release_policy",
        "control.production_readiness_external",
    } <= set(controls)

    for item in controls.values():
        assert item["resourceType"] == "SecurityControl"
        assert item["apiVersion"] == "fatecat.tradecatlabs/v1"
        assert item["links"]["collection"] == "/security"
        assert item["implementationRefs"]
        assert item["privacyBoundary"]
        assert item["externalConnectivity"]
        assert item["metadata"]["risk"]
        assert item["metadata"]["threatModel"]
        if item["status"] == "available":
            assert item["localVerification"]
            continue
        assert item["status"] == "manual"
        assert item["externalConnectivity"] in schema["allowedExternalConnectivity"]
        assert item["externalConnectivity"] != "not_required"

    auth = controls["control.record_token_access"]
    assert "FATE_API_USER_TOKENS" in auth["envVars"]
    assert auth["externalConnectivity"] == "not_required"
    assert "自己的记录" in auth["privacyBoundary"]

    rbac = controls["control.rbac_policy"]
    assert rbac["controlType"] == "rbac"
    assert rbac["status"] == "available"
    assert "record.delete" in rbac["metadata"]["recordScopes"]
    assert "OAuth/OIDC" in rbac["metadata"]["risk"]

    identity = controls["control.production_identity_oidc"]
    assert identity["controlType"] == "identity"
    assert identity["status"] == "manual"
    assert "FATE_OIDC_ISSUER" in identity["envVars"]
    assert "scoped token" in identity["metadata"]["risk"]

    siem = controls["control.external_siem_immutable_audit"]
    assert siem["controlType"] == "siem"
    assert siem["status"] == "manual"
    assert "FATE_AUDIT_SIEM_ENDPOINT" in siem["envVars"]
    assert "不可变审计" in siem["metadata"]["risk"]

    cleanup = controls["control.retention_cleanup_plan"]
    assert cleanup["controlType"] == "retention"
    assert cleanup["status"] == "manual"
    assert "FATE_RECORD_RETENTION_AUTO_CLEANUP_ENABLED" in cleanup["envVars"]
    assert cleanup["metadata"]["currentRecordMode"] == "explicit_delete"

    owasp = controls["control.owasp_api_security_regression"]
    assert owasp["controlType"] == "owasp_api_regression"
    assert owasp["status"] == "available"
    assert "scripts/production-security-gate.py" in owasp["implementationRefs"]

    release_gate = controls["control.public_release_policy"]
    assert release_gate["controlType"] == "release_gate"
    assert "scripts/check-public-release-policy.sh" in release_gate["implementationRefs"]

    secret_scan = controls["control.secret_scan_gate"]
    assert secret_scan["controlType"] == "secret_scan"
    assert secret_scan["status"] == "available"
    assert secret_scan["externalConnectivity"] == "not_required"
    assert "scripts/secret-scan.py" in secret_scan["implementationRefs"]
    assert "疑似密钥原文" in secret_scan["privacyBoundary"]
    assert registry["metadata"]["secretScanCommand"].startswith("bash scripts/secret-scan.sh")

    audit_log = controls["control.audit_event_log"]
    assert audit_log["controlType"] == "audit_log"
    assert audit_log["status"] == "available"
    assert "FATE_AUDIT_LOG_ENABLED" in audit_log["envVars"]
    assert "请求体" in audit_log["privacyBoundary"]

    retention = controls["control.retention_policy"]
    assert retention["controlType"] == "retention"
    assert "FATE_RECORD_RETENTION_DAYS" in retention["envVars"]
    assert "explicit_delete" in retention["metadata"]["risk"] or "显式删除" in retention["metadata"]["risk"]

    production = controls["control.production_readiness_external"]
    assert production["status"] == "manual"
    assert production["externalConnectivity"] == "external_connectivity_pending"
    assert "真实 token" in production["metadata"]["failureMode"]


def test_delivery_surface_schema_and_registry_define_same_source_boundaries():
    schema = _load_json(DELIVERY_DIR / "schemas" / "delivery-surface.schema.json")
    registry = _load_json(DELIVERY_DIR / "registry.json")
    release_schema = _load_json(DELIVERY_DIR / "schemas" / "release-gate.schema.json")
    release_gate = _load_json(DELIVERY_DIR / "release-gate.json")
    surfaces = {item["id"]: item for item in registry["surfaces"]}

    assert schema["requiredDeliverySurfaceFields"] == [
        "resourceType",
        "apiVersion",
        "id",
        "name",
        "surfaceType",
        "status",
        "entrypoints",
        "supportedOutputs",
        "supportedReportSystems",
        "canonicalChain",
        "outputContracts",
        "localVerification",
        "privacyBoundary",
        "externalConnectivity",
        "links",
        "metadata",
    ]
    assert schema["allowedSurfaceType"] == ["api", "web", "bot", "cli", "skill", "hosted_web"]
    assert schema["allowedStatus"] == ["available", "partial", "manual", "planned", "blocked"]
    assert "partial surface 必须在 metadata.sameSourceScope 中说明未覆盖的输出边界" in schema["invariants"]
    assert any(
        item.startswith("Web/API/Bot 的 Markdown 报告不得绕过 calculation_service.calculate_delivery_result")
        for item in schema["invariants"]
    )

    assert registry["schemas"]["deliverySurface"] == "contracts/fate/delivery/schemas/delivery-surface.schema.json"
    assert registry["schemas"]["releaseGate"] == "contracts/fate/delivery/schemas/release-gate.schema.json"
    assert registry["releaseGate"]["id"] == "gate.live_release"
    assert registry["releaseGate"]["contract"] == "contracts/fate/delivery/release-gate.json"
    assert release_schema["requiredShipGateFields"] == ["status", "blockingItems", "policy"]
    assert release_gate["resourceType"] == "ReleaseGate"
    assert release_gate["shipGate"]["status"] == "blocked"
    assert {item["id"] for item in release_gate["requiredEvidence"]} >= {
        "evidence.production_api_live",
        "evidence.hf_space_live",
        "evidence.telegram_bot_live",
        "evidence.container_digest",
        "evidence.sbom_artifact",
        "evidence.provenance_artifact",
        "evidence.clean_git_state",
    }
    assert {
        "surface.fastapi",
        "surface.web",
        "surface.telegram_bot",
        "surface.cli",
        "surface.agent_skill",
        "surface.huggingface_space",
    } <= set(surfaces)

    for item in surfaces.values():
        assert item["resourceType"] == "DeliverySurface"
        assert item["apiVersion"] == "fatecat.tradecatlabs/v1"
        assert item["links"]["collection"] == "/surfaces"
        assert item["entrypoints"]
        assert item["canonicalChain"]
        assert item["outputContracts"]
        assert item["privacyBoundary"]
        assert item["externalConnectivity"]
        assert item["metadata"]["sameSourceScope"]
        assert item["metadata"]["risk"]
        if item["status"] == "available":
            assert item["localVerification"]
            assert item["externalConnectivity"] in {"not_required", "requires_real_credentials"}
            continue
        if item["status"] == "partial":
            assert (
                "不生成标准 Markdown" in item["metadata"]["sameSourceScope"]
                or "不是独立线上服务" in item["metadata"]["sameSourceScope"]
            )
            continue
        assert item["status"] == "manual"
        assert item["externalConnectivity"] == "requires_hosted_platform"

    web = surfaces["surface.web"]
    assert web["surfaceType"] == "web"
    assert "/web" in web["entrypoints"]
    assert "build_web_report_result" in " ".join(web["canonicalChain"])

    bot = surfaces["surface.telegram_bot"]
    assert bot["surfaceType"] == "bot"
    assert bot["externalConnectivity"] == "requires_real_credentials"
    assert "真实 Telegram API" in bot["metadata"]["sameSourceScope"]

    cli = surfaces["surface.cli"]
    assert cli["status"] == "partial"
    assert cli["supportedOutputs"] == ["json"]
    assert "不生成标准 Markdown" in cli["metadata"]["sameSourceScope"]


def test_capability_registry_enforces_infrastructure_admission_rules():
    for item in list_capabilities():
        assert item.test_gate["releaseRequired"] is True
        assert set(item.evidence_policy) >= {
            "ruleIdRequired",
            "sourceRequired",
            "calculationTraceRequired",
            "noScientificCertainty",
        }
        assert isinstance(item.evidence_policy["ruleIdRequired"], bool)

        if item.status == "production":
            assert item.test_gate["status"] == "passing"
            assert item.test_gate["commands"]
            assert item.maturity_level in {"L3", "L4"}
            assert not item.provider.startswith("planned.")
            assert item.engine_version != "planned-v0"
            continue

        if item.status == "planned":
            assert item.maturity_level == "L0"
            assert item.test_gate["status"] == "blocked"
            assert item.test_gate["commands"] == []
            assert item.provider.startswith("planned.")
            assert item.engine_version == "planned-v0"


def test_capability_output_schema_requires_report_envelope_and_evidence_refs():
    output_schema = _load_json(CAPABILITY_DIR / "schemas" / "output.schema.json")
    evidence_schema = _load_json(CAPABILITY_DIR / "schemas" / "evidence.schema.json")

    assert "report" in output_schema["requiredFields"]
    assert "report 保存 Report resource envelope" in output_schema["reportRule"]
    assert "evidenceRefFields" in evidence_schema
    assert set(evidence_schema["evidenceRefFields"]) >= {"id", "source", "ruleIds"}
    assert "evidenceRefs 只保存可跳转引用" in evidence_schema["evidenceRefsRule"]


def test_report_policy_gate_flags_forbidden_claims_and_excludes_policy_list():
    gate = build_report_policy_gate(
        content={
            "sections": [
                {
                    "id": "summary",
                    "title": "此处不得写必死断语",
                }
            ],
            "risk": {
                "forbiddenClaims": ["确定未来"],
            },
        },
        forbidden_claims=["必死", "确定未来"],
        checked_fields=["report.sections", "report.risk"],
        excluded_fields=["report.risk.forbiddenClaims"],
    )

    assert gate["status"] == "fail"
    assert gate["forbiddenClaimsCount"] == 2
    assert gate["matches"] == [
        {
            "claim": "必死",
            "path": "report.sections[0].title",
            "excerpt": "此处不得写必死断语",
        }
    ]

    clean_gate = build_report_policy_gate(
        content={"sections": [{"id": "summary", "title": "仅保留民俗参考边界"}]},
        forbidden_claims=["必死"],
        checked_fields=["report.sections"],
        excluded_fields=["report.risk.forbiddenClaims"],
    )

    assert clean_gate["status"] == "pass"
    assert clean_gate["matches"] == []


def test_markdown_report_policy_gate_scans_visible_markdown_body():
    gate = build_markdown_report_policy_gate(
        markdown="# 命理排盘报告：测试\n\n这里出现必死断语",
        forbidden_claims=["必死"],
        report_system="bazi",
    )

    assert gate["status"] == "fail"
    assert gate["scope"] == "markdown-report:bazi"
    assert gate["checkedFields"] == ["report.markdown"]
    assert gate["matches"][0]["path"] == "report.markdown"

    clean_gate = build_markdown_report_policy_gate(
        markdown="# 命理排盘报告：测试\n\n仅供传统文化参考。",
        forbidden_claims=["必死"],
        report_system="bazi",
    )
    assert clean_gate["status"] == "pass"
    assert clean_gate["matches"] == []


def test_markdown_snapshot_gate_locks_core_headings_without_full_body_hash():
    bazi_markdown = "\n".join(
        [
            "# 命理排盘报告：测试",
            "## 第一卷：先天命格（静态分析）",
            "## 第二卷：后天运路（动态趋势）",
            "## 第三卷：民俗与建议（生活应用）",
        ]
    )
    bazi_gate = build_markdown_snapshot_gate(markdown=bazi_markdown, report_system="bazi")

    assert bazi_gate["status"] == "pass"
    assert bazi_gate["contentCoverage"].startswith("Markdown heading structure only")
    assert bazi_gate["headingCount"] == 4
    assert bazi_gate["missingHeadings"] == []

    broken_gate = build_markdown_snapshot_gate(markdown="# 命理排盘报告：测试\n", report_system="bazi")
    assert broken_gate["status"] == "fail"
    assert "## 第一卷：先天命格（静态分析）" in broken_gate["missingHeadings"]


def test_provider_registry_covers_all_production_capabilities_and_excludes_planned():
    providers = {provider.metadata().provider_id: provider for provider in list_providers()}
    production_capabilities = [item for item in list_capabilities() if item.status == "production"]

    assert set(providers) == {item.provider for item in production_capabilities}
    assert "planned.liuyao" not in providers

    for capability in production_capabilities:
        provider = get_provider_for_capability(capability)
        metadata = provider.metadata()
        health = provider.health()
        assert metadata.provider_id == capability.provider
        assert metadata.engine_version == capability.engine_version
        assert capability.capability_id in metadata.capabilities
        assert metadata.interface_version == "provider-protocol-v1"
        assert metadata.adapter_type == "usecase-adapter"
        metadata_payload = metadata.as_dict()
        assert metadata_payload["versionLock"]["engineVersion"] == capability.engine_version
        assert metadata_payload["lifecycle"]["status"] == "active"
        assert metadata_payload["sourcePolicy"]["sourceRefs"]
        assert metadata_payload["licensePolicy"]["productionUseAllowed"] is True
        assert metadata_payload["resourceManifest"]["runtimeRefs"]
        assert metadata_payload["promotionGate"]["status"] == "passing"
        assert metadata_payload["deprecation"]["status"] == "active"
        assert health.status == "ready"
        assert health.checks["scope"] == "in-process"


def test_capability_registry_rejects_production_capability_without_passing_gate():
    bazi = get_capability("bazi")
    broken = replace(bazi, test_gate={**bazi.test_gate, "status": "blocked"})

    with pytest.raises(ValueError, match="testGate.status=passing"):
        capability_registry._validate_capability_admission(broken)


def test_capability_registry_rejects_planned_capability_with_real_provider():
    liuyao = get_capability("liuyao")
    broken = replace(liuyao, provider="fate_core.usecases.calculate_liuyao")

    with pytest.raises(ValueError, match=r"planned\.\* provider"):
        capability_registry._validate_capability_admission(broken)


def test_planned_capability_cannot_execute_as_production():
    with pytest.raises(ValueError, match="尚未生产化"):
        CapabilityExecutor().execute(
            CapabilityInput(
                capability_id="liuyao",
                payload={
                    "question": "测试问题",
                    "castMethod": "time",
                    "castTime": "2026-05-08 08:00:00",
                },
            )
        )


def test_almanac_capability_executes_as_standalone_production():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="almanac",
            payload={
                "dateRange": {"start": "2026-05-08", "end": "2026-05-10"},
                "eventType": "出行",
                "place": "北京",
            },
        )
    )

    assert result.capability_id == "almanac"
    assert result.status == "production"
    assert result.report_profile == "almanac"
    assert result.data["capabilityId"] == "almanac"
    assert result.data["dateRange"]["days"] == 3
    assert result.data["eventTerms"] == ["出行"]
    assert result.data["place"] == "北京"
    assert result.data["days"][0]["timeSlots"]
    assert len(result.data["days"][0]["timeSlots"]) == 12
    assert [slot["zhi"] for slot in result.data["days"][0]["timeSlots"]].count("子") == 1
    assert "scoreBreakdown" in result.data["days"][0]
    assert "xiu" in result.data["days"][0]
    assert result.evidence["source"] == "lunar-python"
    assert "almanac.time_yi_ji" in result.evidence["items"]["2026-05-08"]["ruleIds"]
    assert "almanac.zhi_xing_auxiliary" in result.evidence["items"]["2026-05-08"]["ruleIds"]
    assert set(result.evidence["items"]) == {"2026-05-08", "2026-05-09", "2026-05-10"}
    assert result.risk["disclaimerRequired"] is True
    assert result.metadata["maturity"]["level"] == "L3"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_almanac"
    assert result.metadata["engine"]["engineVersion"] == "fate-core-almanac-v1"
    assert result.metadata["provider"]["providerId"] == "fate_core.usecases.calculate_almanac"
    assert result.metadata["provider"]["interfaceVersion"] == "provider-protocol-v1"
    assert result.metadata["provider"]["health"]["status"] == "ready"
    assert result.metadata["evidencePolicy"]["ruleIdRequired"] is True
    assert result.metadata["testGate"]["status"] == "passing"
    assert get_capability("almanac").default_visibility == "standalone"


def test_almanac_capability_displays_submitted_place():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="almanac",
            payload={
                "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
                "eventType": "出行",
                "place": "上海市",
            },
        )
    )

    assert result.data["place"] == "上海市"
    assert "已填写（非北京地区已隐藏）" not in json.dumps(result.data, ensure_ascii=False)


def test_meihua_capability_executes_number_cast_as_standalone_production():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="meihua",
            payload={
                "question": "测试问题能否推进",
                "castMethod": "number",
                "castValue": "3,8,6",
            },
        )
    )

    assert result.capability_id == "meihua"
    assert result.status == "production"
    assert result.report_profile == "meihua"
    assert result.data["capabilityId"] == "meihua"
    assert result.data["castMethod"] == "数字起卦"
    assert result.data["hexagrams"]["movingLine"] == 5
    assert result.data["judgementBoundary"]
    assert "meihua.number_cast" in result.evidence["items"]["cast"]["ruleIds"]
    assert "meihua.body_use" in result.evidence["items"]["bodyUse"]["ruleIds"]


def test_ziwei_capability_delegates_to_ziwei_usecase(monkeypatch):
    expected_data = {
        "capabilityId": "ziwei",
        "ziweiChart": {"palaces": []},
        "analysisEvidence": {"items": {"ziweiChart": {"ruleIds": ["ziwei.iztro_chart"]}}},
    }

    monkeypatch.setattr(capability_providers, "calculate_ziwei", lambda payload: expected_data)
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
            },
        )
    )

    assert result.capability_id == "ziwei"
    assert result.status == "production"
    assert result.report_profile == "ziwei"
    assert result.data == expected_data
    assert result.evidence == expected_data["analysisEvidence"]
    assert result.metadata["maturity"]["level"] == "L4"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_ziwei"
    assert result.metadata["provider"]["providerId"] == "fate_core.usecases.calculate_ziwei"
    assert result.metadata["provider"]["health"]["checks"]["runner"] == "<lambda>"
    assert result.metadata["testGate"]["status"] == "passing"


def test_ziwei_capability_preserves_complete_iztro_palace_schema():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
                "name": "测试样本",
            },
        )
    )

    data = result.data
    assert data["capabilityId"] == "ziwei"
    assert data["meta"]["legacyZiweiBasic"] == "disabled"
    assert "ziweiBasic" not in data
    assert data["inputTrace"]["originalTime"] == "1990-01-01 08:00:00"
    assert data["inputTrace"]["trueSolarTime"]
    assert data["inputTrace"]["fixLeap"] is True
    assert data["fiveElementsClass"]
    assert data["starInfluence"] == data["fiveElementsClass"]
    interpretation = data["ziweiInterpretation"]
    assert interpretation["interpretationBoundary"]
    assert interpretation["mainStarCombinations"]
    assert interpretation["lifeBody"]
    assert interpretation["surroundedPalaces"]["life"]
    assert interpretation["mutagenPlacements"]
    assert len(interpretation["fortuneLinks"]) == 5

    palaces = data["palaceAnalysis"]
    assert len(palaces) == 12
    for palace in palaces:
        for field in [
            "index",
            "name",
            "heavenlyStem",
            "earthlyBranch",
            "isBodyPalace",
            "isOriginalPalace",
            "changsheng12",
            "boshi12",
            "jiangqian12",
            "suiqian12",
            "decadal",
            "ages",
        ]:
            assert field in palace
        assert isinstance(palace["majorStars"], list)
        assert isinstance(palace["minorStars"], list)
        assert isinstance(palace["adjectiveStars"], list)

    assert len(data["starPositions"]) == 12
    assert result.evidence["coverage"]["palaceCount"] == 12
    assert result.evidence["coverage"]["hasInterpretation"] is True
    assert "ziwei.palace_metadata" in result.evidence["items"]["ziweiChart"]["ruleIds"]
    assert "ziwei.time_index" in result.evidence["items"]["timePipeline"]["ruleIds"]
    assert "ziwei.surrounded_palaces" in result.evidence["items"]["interpretation"]["ruleIds"]


def test_bazi_capability_delegates_to_pure_analysis(monkeypatch):
    expected_data = {"analysisEvidence": {"items": {"dayMaster": {"ruleIds": ["bazi.month_command_priority"]}}}}

    monkeypatch.setattr(capability_providers, "calculate_pure_analysis", lambda payload: expected_data)
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="bazi",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
            },
        )
    )

    assert result.capability_id == "bazi"
    assert result.status == "production"
    assert result.report_profile == get_capability("bazi").report_profile
    assert result.data == expected_data
    assert result.evidence == expected_data["analysisEvidence"]
    assert result.metadata["maturity"]["level"] == "L4"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_pure_analysis"
    assert result.metadata["provider"]["providerId"] == "fate_core.usecases.calculate_pure_analysis"
    assert result.metadata["provider"]["health"]["checks"]["runner"] == "<lambda>"
    assert result.metadata["testGate"]["status"] == "passing"
    assert result.risk["disclaimerRequired"] is True
