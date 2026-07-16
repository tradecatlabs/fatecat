# AGENTS.md - fate_core capabilities

## 目录用途

`fate_core/capabilities/` 是统一测算能力协议的运行时边界：它只负责能力注册、输入契约、执行路由、输出包装和风险边界，不承载具体命理算法细节。

## 目录结构

```text
capabilities/
├── AGENTS.md
├── __init__.py
├── contracts.py
├── executor.py
├── providers.py
├── report_policy.py
└── registry.py
```

## 职责边界

- `contracts.py`：定义 `Capability`、`CapabilityInput`、`CapabilityResult` 等统一数据结构。
- `registry.py`：加载并校验 `contracts/fate/capabilities/registry.json`，确保默认能力只能是 `bazi`。
- `providers.py`：定义 `ProviderProtocol`、provider registry、metadata、本地 health、versionLock、lifecycle、source/license/resource manifest、promotionGate 和 deprecation；只包装现有 production usecase，不承载算法；provider 本地依赖执行由 `scripts/provider-dependency-smoke.sh` 验证。
- `report_policy.py`：定义 Report policy gate 的最小禁止性断语扫描器；只扫描调用方传入的生成内容摘要，不能扫描风险清单自身。
- `executor.py`：先按 registry 的 `availability` 做 admission，再通过 provider registry 执行可用 capability；planned / unavailable 能力必须拒绝执行，成熟度不得替代可执行性；执行时通过 `fate_core.observability.trace_span` 发出本地 capability/provider span，不记录输入 payload。
- `__init__.py`：对外暴露稳定导入入口。

## 依赖方向

- 允许依赖 `fate_core.usecases` 和 `fate_core.support.paths`。
- 允许依赖 `fate_core.observability` 记录低敏 span。
- 禁止依赖 Telegram、FastAPI、Bot、Web UI 或数据库。
- 新增体系时先登记 registry，再补 provider/usecase 和 provider lifecycle metadata，通过 `scripts/provider-lifecycle-gate.sh` 与 `scripts/provider-dependency-smoke.sh` 后才允许切到 `production`。
