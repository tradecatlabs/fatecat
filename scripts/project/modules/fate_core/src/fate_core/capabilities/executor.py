from __future__ import annotations

from typing import Any

from fate_core.capabilities.contracts import Capability, CapabilityInput, CapabilityResult
from fate_core.capabilities.registry import get_capability
from fate_core.usecases import calculate_almanac, calculate_pure_analysis
from fate_core.usecases.calculate_almanac import build_almanac_input_from_payload
from fate_core.usecases.calculate_pure_analysis import build_pure_analysis_input_from_payload


class CapabilityExecutor:
    """统一能力执行器。"""

    def execute(self, request: CapabilityInput) -> CapabilityResult:
        capability = get_capability(request.capability_id)
        self._validate_required_inputs(capability.input_required, request.payload, capability.capability_id)
        if capability.status != "production":
            raise ValueError(f"capability 尚未生产化: {capability.capability_id} ({capability.status})")
        if capability.capability_id == "bazi":
            data = calculate_pure_analysis(build_pure_analysis_input_from_payload(request.payload))
            evidence = data.get("analysisEvidence", {}) if isinstance(data.get("analysisEvidence"), dict) else {}
            return CapabilityResult(
                capability_id=capability.capability_id,
                status=capability.status,
                report_profile=capability.report_profile,
                data=data,
                evidence=evidence,
                risk=self._risk_payload(capability),
            )
        if capability.capability_id == "almanac":
            data = calculate_almanac(build_almanac_input_from_payload(request.payload))
            evidence = data.get("analysisEvidence", {}) if isinstance(data.get("analysisEvidence"), dict) else {}
            return CapabilityResult(
                capability_id=capability.capability_id,
                status=capability.status,
                report_profile=capability.report_profile,
                data=data,
                evidence=evidence,
                risk=self._risk_payload(capability),
            )
        raise ValueError(f"capability 缺少生产 provider: {capability.capability_id}")

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
