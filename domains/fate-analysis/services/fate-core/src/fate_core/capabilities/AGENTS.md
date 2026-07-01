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
└── registry.py
```

## 职责边界

- `contracts.py`：定义 `Capability`、`CapabilityInput`、`CapabilityResult` 等统一数据结构。
- `registry.py`：加载并校验 `contracts/fate/capabilities/registry.json`，确保默认能力只能是 `bazi`。
- `executor.py`：按 `engine.provider` 执行生产化 capability；planned / experimental 能力必须拒绝执行，避免伪装成生产能力。
- `__init__.py`：对外暴露稳定导入入口。

## 依赖方向

- 允许依赖 `fate_core.usecases` 和 `fate_core.support.paths`。
- 禁止依赖 Telegram、FastAPI、Bot、Web UI 或数据库。
- 新增体系时先登记 registry，再补 provider/usecase，最后才允许切到 `production`。
