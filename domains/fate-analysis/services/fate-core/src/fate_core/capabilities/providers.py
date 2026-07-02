from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

from fate_core.capabilities.contracts import Capability
from fate_core.usecases import calculate_almanac, calculate_meihua, calculate_pure_analysis, calculate_ziwei
from fate_core.usecases.calculate_almanac import build_almanac_input_from_payload
from fate_core.usecases.calculate_meihua import build_meihua_input_from_payload
from fate_core.usecases.calculate_pure_analysis import build_pure_analysis_input_from_payload
from fate_core.usecases.calculate_ziwei import build_ziwei_input_from_payload

# Ponytail existence: provider objects are the runtime boundary between capability
# admission and concrete calculation usecases. They deliberately wrap existing
# mature usecases instead of reimplementing divination algorithms.
# Owner: tradecatlabs/fate-core. Verification: test_capability_protocol.py.

ProviderBuilder = Callable[[dict[str, Any]], Any]
ProviderRunner = Callable[[Any], dict[str, Any]]


@dataclass(frozen=True)
class ProviderMetadata:
    """生产 provider 可审计元信息。"""

    provider_id: str
    engine_version: str
    deterministic: bool
    source: str
    capabilities: tuple[str, ...]
    interface_version: str = "provider-protocol-v1"
    adapter_type: str = "usecase-adapter"
    version_lock: dict[str, Any] = field(default_factory=dict)
    lifecycle: dict[str, Any] = field(default_factory=dict)
    source_policy: dict[str, Any] = field(default_factory=dict)
    license_policy: dict[str, Any] = field(default_factory=dict)
    resource_manifest: dict[str, Any] = field(default_factory=dict)
    promotion_gate: dict[str, Any] = field(default_factory=dict)
    deprecation: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "providerId": self.provider_id,
            "engineVersion": self.engine_version,
            "deterministic": self.deterministic,
            "source": self.source,
            "capabilities": list(self.capabilities),
            "interfaceVersion": self.interface_version,
            "adapterType": self.adapter_type,
            "versionLock": self.version_lock,
            "lifecycle": self.lifecycle,
            "sourcePolicy": self.source_policy,
            "licensePolicy": self.license_policy,
            "resourceManifest": self.resource_manifest,
            "promotionGate": self.promotion_gate,
            "deprecation": self.deprecation,
        }


@dataclass(frozen=True)
class ProviderHealth:
    """provider 本地健康状态。

    本轮只做进程内静态健康，不探测外部网络、真实 token 或远端服务。
    """

    status: str
    checks: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checks": self.checks,
        }


class ProviderProtocol(Protocol):
    """统一 production capability provider 协议。"""

    @property
    def provider_id(self) -> str:
        """provider 稳定 ID。"""
        ...

    @property
    def engine_version(self) -> str:
        """底层引擎版本。"""
        ...

    @property
    def deterministic(self) -> bool:
        """相同输入是否应给出确定性输出。"""
        ...

    def validate(self, raw_payload: dict[str, Any]) -> Any:
        """校验并归一化输入。"""
        ...

    def calculate(self, normalized_input: Any) -> dict[str, Any]:
        """执行计算并返回结构化结果。"""
        ...

    def metadata(self) -> ProviderMetadata:
        """返回可审计 provider 元信息。"""
        ...

    def health(self) -> ProviderHealth:
        """返回本地 provider 健康状态。"""
        ...


@dataclass(frozen=True)
class UsecaseProvider:
    """把现有 usecase 包装成统一 provider。"""

    provider_id: str
    engine_version: str
    deterministic: bool
    source: str
    capabilities: tuple[str, ...]
    builder: ProviderBuilder
    runner: ProviderRunner
    source_type: str = "project_owned"
    source_refs: tuple[str, ...] = ()
    supply_chain_refs: tuple[str, ...] = ()
    license_policy: dict[str, Any] = field(default_factory=dict)
    lifecycle_stage: str = "production"
    lifecycle_owner: str = "tradecatlabs/fate-core"
    runtime_refs: tuple[str, ...] = ()
    contract_refs: tuple[str, ...] = ()
    test_refs: tuple[str, ...] = ()

    def validate(self, raw_payload: dict[str, Any]) -> Any:
        return self.builder(raw_payload)

    def calculate(self, normalized_input: Any) -> dict[str, Any]:
        result = self.runner(normalized_input)
        if not isinstance(result, dict):
            raise ValueError(f"{self.provider_id} provider 必须返回 dict")
        return result

    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            provider_id=self.provider_id,
            engine_version=self.engine_version,
            deterministic=self.deterministic,
            source=self.source,
            capabilities=self.capabilities,
            version_lock={
                "engineVersion": self.engine_version,
                "interfaceVersion": "provider-protocol-v1",
                "deterministic": self.deterministic,
            },
            lifecycle={
                "stage": self.lifecycle_stage,
                "status": "active",
                "owner": self.lifecycle_owner,
                "promotionRequired": True,
            },
            source_policy={
                "sourceType": self.source_type,
                "sourceRefs": list(self.source_refs or (self.source,)),
                "supplyChainRefs": list(self.supply_chain_refs),
                "gluePrinciple": "provider 只包装成熟 usecase 或已登记供应链资产，自研代码只做适配和编排",
            },
            license_policy=self._license_policy(),
            resource_manifest={
                "runtimeRefs": list(self.runtime_refs),
                "contractRefs": list(self.contract_refs or ("contracts/fate/capabilities/registry.json",)),
                "testRefs": list(
                    self.test_refs
                    or (
                        "tests/regression/test_capability_protocol.py",
                        "tests/regression/test_api_contracts.py",
                    )
                ),
                "supplyChainRefs": list(self.supply_chain_refs),
            },
            promotion_gate={
                "status": "passing",
                "commands": [
                    ".venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k provider",
                    "bash scripts/provider-lifecycle-gate.sh",
                ],
                "releaseRequired": True,
            },
            deprecation={
                "status": "active",
                "replacementProvider": None,
                "removalNotBefore": None,
                "policy": "任何 provider 退役必须先登记 replacement、迁移窗口和 release note；不得直接删除生产 provider。",
            },
        )

    def _license_policy(self) -> dict[str, Any]:
        if self.license_policy:
            return self.license_policy
        return {
            "license": "MIT",
            "licenseStatus": "project_repo_license",
            "auditRequired": False,
            "distributionAllowed": True,
            "productionUseAllowed": True,
            "evidence": ["LICENSE", "pyproject.toml"],
        }

    def health(self) -> ProviderHealth:
        return ProviderHealth(
            status="ready",
            checks={
                "builder": getattr(self.builder, "__name__", "callable"),
                "runner": getattr(self.runner, "__name__", "callable"),
                "deterministic": self.deterministic,
                "scope": "in-process",
            },
        )


def build_provider_registry() -> dict[str, UsecaseProvider]:
    """返回 production provider registry。

    使用函数动态构建，保证测试 monkeypatch 模块级 usecase 时不会被导入期缓存绕过。
    """

    return {
        "fate_core.usecases.calculate_pure_analysis": UsecaseProvider(
            provider_id="fate_core.usecases.calculate_pure_analysis",
            engine_version="fate-core-bazi-v1",
            deterministic=True,
            source="fate_core.usecases.calculate_pure_analysis",
            capabilities=("bazi",),
            builder=build_pure_analysis_input_from_payload,
            runner=calculate_pure_analysis,
            source_type="project_owned_adapter",
            source_refs=(
                "domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py",
                "domains/fate-analysis/services/fate-core/src/fate_core/providers",
            ),
            supply_chain_refs=("tools/reference-repos/vendor_sources.json#lunar-python",),
            runtime_refs=(
                "domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py",
                "domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_bazi.py",
            ),
        ),
        "fate_core.usecases.calculate_almanac": UsecaseProvider(
            provider_id="fate_core.usecases.calculate_almanac",
            engine_version="fate-core-almanac-v1",
            deterministic=True,
            source="fate_core.usecases.calculate_almanac",
            capabilities=("almanac",),
            builder=build_almanac_input_from_payload,
            runner=calculate_almanac,
            source_type="project_owned_adapter",
            source_refs=("domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_almanac.py",),
            supply_chain_refs=("tools/reference-repos/vendor_sources.json#lunar-python",),
            lifecycle_stage="validated",
            runtime_refs=("domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_almanac.py",),
        ),
        "fate_core.usecases.calculate_ziwei": UsecaseProvider(
            provider_id="fate_core.usecases.calculate_ziwei",
            engine_version="fate-core-ziwei-v1",
            deterministic=True,
            source="fate_core.usecases.calculate_ziwei",
            capabilities=("ziwei",),
            builder=build_ziwei_input_from_payload,
            runner=calculate_ziwei,
            source_type="registered_vendor_adapter",
            source_refs=(
                "domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_ziwei.py",
                "domains/fate-analysis/services/fate-core/src/fate_core/adapters/ziwei_iztro.py",
            ),
            supply_chain_refs=("tools/reference-repos/vendor_sources.json#iztro",),
            runtime_refs=(
                "domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_ziwei.py",
                "domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_integrations/fortel_ziwei_integration.py",
            ),
        ),
        "fate_core.usecases.calculate_meihua": UsecaseProvider(
            provider_id="fate_core.usecases.calculate_meihua",
            engine_version="fate-core-meihua-v1",
            deterministic=True,
            source="fate_core.usecases.calculate_meihua",
            capabilities=("meihua",),
            builder=build_meihua_input_from_payload,
            runner=calculate_meihua,
            source_type="project_owned_algorithm",
            source_refs=("domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_meihua.py",),
            lifecycle_stage="validated",
            runtime_refs=("domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_meihua.py",),
        ),
    }


def list_providers() -> list[ProviderProtocol]:
    """列出按 provider_id 排序的生产 provider。"""

    registry = build_provider_registry()
    return [registry[key] for key in sorted(registry)]


def get_provider(provider_id: str) -> ProviderProtocol:
    """读取生产 provider。"""

    normalized = str(provider_id).strip()
    registry = build_provider_registry()
    if normalized not in registry:
        raise ValueError(f"缺少生产 provider: {provider_id}")
    return registry[normalized]


def get_provider_for_capability(capability: Capability) -> ProviderProtocol:
    """按 capability 的 engine.provider 读取 provider，并校验版本契约。"""

    provider = get_provider(capability.provider)
    metadata = provider.metadata()
    if metadata.engine_version != capability.engine_version:
        raise ValueError(
            f"{capability.capability_id} provider engineVersion 不一致: "
            f"{metadata.engine_version} != {capability.engine_version}"
        )
    if capability.capability_id not in metadata.capabilities:
        raise ValueError(f"{metadata.provider_id} provider 未声明支持 {capability.capability_id}")
    return provider
