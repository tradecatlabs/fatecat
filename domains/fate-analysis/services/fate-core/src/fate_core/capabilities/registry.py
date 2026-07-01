from __future__ import annotations

import json
from functools import cache
from typing import Any

from fate_core.capabilities.contracts import Capability
from fate_core.support.paths import FATE_CAPABILITY_DIR

# Ponytail existence: registry loader is the single reader for capability JSON contracts.
# Owner: tradecatlabs/fate-core. Verification: test_capability_protocol.py.

VALID_STATUSES = {"planned", "experimental", "production"}
VALID_VISIBILITIES = {"default", "optional", "standalone", "hidden"}
VALID_RISK_LEVELS = {"folk_reference", "entertainment", "requires_disclaimer"}
VALID_MATURITY_LEVELS = {"L0", "L1", "L2", "L3", "L4"}


def _as_tuple(value: Any, field: str, capability_id: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{capability_id}.{field} 必须是数组")
    result = tuple(str(item).strip() for item in value if str(item).strip())
    if len(result) != len(value):
        raise ValueError(f"{capability_id}.{field} 不能包含空值")
    return result


def _parse_capability(raw: dict[str, Any]) -> Capability:
    capability_id = str(raw.get("capabilityId", "")).strip()
    if not capability_id:
        raise ValueError("capabilityId 不能为空")

    status = str(raw.get("status", "")).strip()
    if status not in VALID_STATUSES:
        raise ValueError(f"{capability_id}.status 非法: {status}")

    visibility = str(raw.get("defaultVisibility", "")).strip()
    if visibility not in VALID_VISIBILITIES:
        raise ValueError(f"{capability_id}.defaultVisibility 非法: {visibility}")

    risk_policy = raw.get("riskPolicy")
    if not isinstance(risk_policy, dict):
        raise ValueError(f"{capability_id}.riskPolicy 必须是对象")
    risk_level = str(risk_policy.get("riskLevel", "")).strip()
    if risk_level not in VALID_RISK_LEVELS:
        raise ValueError(f"{capability_id}.riskPolicy.riskLevel 非法: {risk_level}")

    engine = raw.get("engine")
    if not isinstance(engine, dict):
        raise ValueError(f"{capability_id}.engine 必须是对象")
    provider = str(engine.get("provider", "")).strip()
    if not provider:
        raise ValueError(f"{capability_id}.engine.provider 不能为空")
    engine_version = str(engine.get("engineVersion", "")).strip()
    if not engine_version:
        raise ValueError(f"{capability_id}.engine.engineVersion 不能为空")

    evidence = raw.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError(f"{capability_id}.evidence 必须是对象")

    evidence_policy = raw.get("evidencePolicy")
    if not isinstance(evidence_policy, dict):
        raise ValueError(f"{capability_id}.evidencePolicy 必须是对象")

    test_gate = raw.get("testGate")
    if not isinstance(test_gate, dict):
        raise ValueError(f"{capability_id}.testGate 必须是对象")
    commands = test_gate.get("commands")
    if not isinstance(commands, list):
        raise ValueError(f"{capability_id}.testGate.commands 必须是数组")

    maturity = raw.get("maturity")
    if not isinstance(maturity, dict):
        raise ValueError(f"{capability_id}.maturity 必须是对象")
    maturity_level = str(maturity.get("level", "")).strip()
    if maturity_level not in VALID_MATURITY_LEVELS:
        raise ValueError(f"{capability_id}.maturity.level 非法: {maturity_level}")
    maturity_status = str(maturity.get("status", "")).strip()
    if not maturity_status:
        raise ValueError(f"{capability_id}.maturity.status 不能为空")
    maturity_summary = str(maturity.get("summary", "")).strip()
    if not maturity_summary:
        raise ValueError(f"{capability_id}.maturity.summary 不能为空")

    report = raw.get("report")
    if not isinstance(report, dict):
        raise ValueError(f"{capability_id}.report 必须是对象")

    return Capability(
        capability_id=capability_id,
        name=str(raw.get("name", "")).strip() or capability_id,
        tradition=str(raw.get("tradition", "")).strip(),
        status=status,  # type: ignore[arg-type]
        default_visibility=visibility,  # type: ignore[arg-type]
        maturity_level=maturity_level,  # type: ignore[arg-type]
        maturity_status=maturity_status,
        maturity_summary=maturity_summary,
        input_required=_as_tuple(raw.get("inputRequired", []), "inputRequired", capability_id),
        input_optional=_as_tuple(raw.get("inputOptional", []), "inputOptional", capability_id),
        provider=provider,
        engine_version=engine_version,
        deterministic=bool(engine.get("deterministic", True)),
        report_profile=str(report.get("profile", "")).strip(),
        markdown_default=bool(report.get("markdownDefault", False)),
        evidence_required=bool(evidence.get("required", True)),
        evidence_policy=evidence_policy,
        test_gate=test_gate,
        risk_level=risk_level,  # type: ignore[arg-type]
        disclaimer_required=bool(risk_policy.get("disclaimerRequired", True)),
        forbidden_claims=_as_tuple(risk_policy.get("forbiddenClaims", []), "riskPolicy.forbiddenClaims", capability_id),
        description=str(raw.get("description", "")).strip(),
    )


@cache
def load_capability_registry() -> dict[str, Capability]:
    """加载并校验能力注册表。"""
    path = FATE_CAPABILITY_DIR / "registry.json"
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError("capability registry 必须是 JSON 对象")
    items = payload.get("capabilities")
    if not isinstance(items, list) or not items:
        raise ValueError("capability registry 缺少 capabilities")

    registry: dict[str, Capability] = {}
    for raw in items:
        if not isinstance(raw, dict):
            raise ValueError("capability item 必须是对象")
        capability = _parse_capability(raw)
        if capability.capability_id in registry:
            raise ValueError(f"重复 capabilityId: {capability.capability_id}")
        registry[capability.capability_id] = capability

    default_capabilities = [
        capability.capability_id for capability in registry.values() if capability.default_visibility == "default"
    ]
    if default_capabilities != ["bazi"]:
        raise ValueError("默认能力必须且只能是 bazi，禁止新体系混入默认报告")
    return registry


def list_capabilities() -> list[Capability]:
    """返回按 capability_id 排序的能力列表。"""
    return [load_capability_registry()[key] for key in sorted(load_capability_registry())]


def get_capability(capability_id: str) -> Capability:
    """读取单个能力注册项。"""
    normalized = str(capability_id).strip()
    registry = load_capability_registry()
    if normalized not in registry:
        raise ValueError(f"未知 capability: {capability_id}")
    return registry[normalized]
