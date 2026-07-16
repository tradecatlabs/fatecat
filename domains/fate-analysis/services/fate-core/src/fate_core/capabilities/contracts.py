from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# Ponytail existence: capability contracts are consumed by registry, executor, and tests.
# Owner: tradecatlabs/fate-core. Verification: test_capability_protocol.py.

CapabilityAvailability = Literal["available", "unavailable", "planned"]
CapabilityMaturityStatus = Literal["registered", "experimental", "validated", "production"]
Visibility = Literal["default", "optional", "standalone", "hidden"]
RiskLevel = Literal["folk_reference", "entertainment", "requires_disclaimer"]
MaturityLevel = Literal["L0", "L1", "L2", "L3", "L4"]


@dataclass(frozen=True)
class Capability:
    """测算能力注册项。"""

    capability_id: str
    name: str
    tradition: str
    availability: CapabilityAvailability
    default_visibility: Visibility
    maturity_level: MaturityLevel
    maturity_status: CapabilityMaturityStatus
    maturity_summary: str
    input_required: tuple[str, ...]
    input_optional: tuple[str, ...]
    provider: str
    engine_version: str
    deterministic: bool
    report_profile: str
    markdown_default: bool
    evidence_required: bool
    evidence_policy: dict[str, Any]
    test_gate: dict[str, Any]
    risk_level: RiskLevel
    disclaimer_required: bool
    forbidden_claims: tuple[str, ...]
    description: str = ""

    @property
    def status(self) -> CapabilityMaturityStatus:
        """兼容旧消费者的成熟度投影；执行准入必须读取 availability。"""

        return self.maturity_status


@dataclass(frozen=True)
class CapabilityInput:
    """统一能力执行输入。"""

    capability_id: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class CapabilityResult:
    """统一能力执行输出。"""

    capability_id: str
    availability: CapabilityAvailability
    status: CapabilityMaturityStatus
    report_profile: str
    data: dict[str, Any]
    evidence: dict[str, Any]
    risk: dict[str, Any]
    metadata: dict[str, Any]
