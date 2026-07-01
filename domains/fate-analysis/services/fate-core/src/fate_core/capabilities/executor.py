from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fate_core.capabilities.contracts import Capability, CapabilityInput, CapabilityResult
from fate_core.capabilities.registry import get_capability
from fate_core.usecases import calculate_almanac, calculate_meihua, calculate_pure_analysis, calculate_ziwei
from fate_core.usecases.calculate_almanac import build_almanac_input_from_payload
from fate_core.usecases.calculate_meihua import build_meihua_input_from_payload
from fate_core.usecases.calculate_pure_analysis import build_pure_analysis_input_from_payload
from fate_core.usecases.calculate_ziwei import build_ziwei_input_from_payload

ProviderBuilder = Callable[[dict[str, Any]], Any]
ProviderRunner = Callable[[Any], dict[str, Any]]


def _provider_handlers() -> dict[str, tuple[ProviderBuilder, ProviderRunner]]:
    """返回生产 provider 路由表。

    使用函数动态生成映射，保证测试 monkeypatch 模块级 usecase 时不会被导入期缓存绕过。
    """
    return {
        "fate_core.usecases.calculate_pure_analysis": (
            build_pure_analysis_input_from_payload,
            calculate_pure_analysis,
        ),
        "fate_core.usecases.calculate_almanac": (
            build_almanac_input_from_payload,
            calculate_almanac,
        ),
        "fate_core.usecases.calculate_ziwei": (
            build_ziwei_input_from_payload,
            calculate_ziwei,
        ),
        "fate_core.usecases.calculate_meihua": (
            build_meihua_input_from_payload,
            calculate_meihua,
        ),
    }


class CapabilityExecutor:
    """统一能力执行器。"""

    def execute(self, request: CapabilityInput) -> CapabilityResult:
        capability = get_capability(request.capability_id)
        self._validate_required_inputs(capability.input_required, request.payload, capability.capability_id)
        if capability.status != "production":
            raise ValueError(f"capability 尚未生产化: {capability.capability_id} ({capability.status})")
        handler = _provider_handlers().get(capability.provider)
        if handler is None:
            raise ValueError(f"capability 缺少生产 provider: {capability.capability_id} -> {capability.provider}")
        builder, runner = handler
        data = runner(builder(request.payload))
        evidence = data.get("analysisEvidence", {}) if isinstance(data.get("analysisEvidence"), dict) else {}
        return CapabilityResult(
            capability_id=capability.capability_id,
            status=capability.status,
            report_profile=capability.report_profile,
            data=data,
            evidence=evidence,
            risk=self._risk_payload(capability),
            metadata=self._metadata_payload(capability),
        )

    @staticmethod
    def _validate_required_inputs(required: tuple[str, ...], payload: dict[str, Any], capability_id: str) -> None:
        missing = [field for field in required if payload.get(field) in (None, "")]
        if missing:
            raise ValueError(f"{capability_id} 缺少必填字段: {', '.join(missing)}")

    @staticmethod
    def _risk_payload(capability: Capability) -> dict[str, Any]:
        return {
            "riskLevel": capability.risk_level,
            "disclaimerRequired": capability.disclaimer_required,
            "forbiddenClaims": list(capability.forbidden_claims),
        }

    @staticmethod
    def _metadata_payload(capability: Capability) -> dict[str, Any]:
        return {
            "maturity": {
                "level": capability.maturity_level,
                "status": capability.maturity_status,
                "summary": capability.maturity_summary,
            },
            "engine": {
                "provider": capability.provider,
                "engineVersion": capability.engine_version,
                "deterministic": capability.deterministic,
            },
            "evidencePolicy": capability.evidence_policy,
            "testGate": capability.test_gate,
        }
