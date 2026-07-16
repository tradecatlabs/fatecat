from __future__ import annotations

from typing import Any

from fate_core.capabilities.contracts import Capability, CapabilityInput, CapabilityResult
from fate_core.capabilities.providers import get_provider_for_capability
from fate_core.capabilities.registry import get_capability
from fate_core.observability import trace_span


class CapabilityExecutor:
    """统一能力执行器。"""

    def execute(self, request: CapabilityInput) -> CapabilityResult:
        capability = get_capability(request.capability_id)
        with trace_span("capability.execute", attributes={"capabilityId": capability.capability_id}):
            self._validate_required_inputs(capability.input_required, request.payload, capability.capability_id)
            if capability.availability != "available":
                availability_reason = "尚未生产化" if capability.availability == "planned" else "当前不可用"
                raise ValueError(
                    f"capability 不可执行（{availability_reason}）: {capability.capability_id} "
                    f"(availability={capability.availability}, maturity={capability.maturity_status})"
                )
            provider = get_provider_for_capability(capability)
            attributes = {"capabilityId": capability.capability_id, "providerId": provider.provider_id}
            with trace_span("provider.validate", attributes=attributes):
                normalized_input = provider.validate(request.payload)
            with trace_span("provider.calculate", attributes=attributes):
                data = provider.calculate(normalized_input)
            evidence = data.get("analysisEvidence", {}) if isinstance(data.get("analysisEvidence"), dict) else {}
            return CapabilityResult(
                capability_id=capability.capability_id,
                availability=capability.availability,
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
        provider = get_provider_for_capability(capability)
        provider_metadata = provider.metadata().as_dict()
        provider_health = provider.health().as_dict()
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
            "provider": {
                **provider_metadata,
                "health": provider_health,
            },
            "evidencePolicy": capability.evidence_policy,
            "testGate": capability.test_gate,
        }
