# Task Overview
- Task ID: `0012`
- Slug: `measurement-infrastructure-wave2-provider-protocol`
- Objective: `执行测算基础设施 100% 实现计划 Wave 2 的第一个切片：把 CapabilityExecutor 从散落函数路由提升为统一 ProviderProtocol / provider registry，先接入 bazi、ziwei、almanac、meihua 四个生产 capability，并暴露 provider metadata、health 与标准错误归一化边界。`
- Status: `Done`

## In Scope
- 新增运行时 `ProviderProtocol`、`ProviderMetadata`、`ProviderHealth` 与 provider registry。
- 将 `bazi`、`ziwei`、`almanac`、`meihua` 四个 production capability 从函数路由改为 provider 对象执行。
- `CapabilityExecutor` 继续保持现有输入输出行为，但 metadata 增加 provider 资源信息和 health。
- planned capability 继续拒绝执行，不能因为 provider registry 存在而绕过 admission gate。
- 更新 capability 协议测试、API contract 测试、局部 AGENTS 和 100% 实现计划状态。

## Out of Scope
- 不实现 Redis/Celery/Temporal 等跨进程执行后端。
- 不改具体八字、紫微、黄历、梅花计算算法。
- 不把六爻、奇门、大六壬、风水九星、姓名合婚切到 production。
- 不改 Web/Bot 报告结构和默认 Markdown 体系。
- 不承诺外部生产域名、真实 token 或 Bot live smoke。

## Task Package Tree
```text
TP-01 provider-contract-runtime
├── TP-01.01 define-provider-protocol
└── TP-01.02 add-provider-registry
TP-02 executor-migration
├── TP-02.01 route-production-capabilities-through-providers
└── TP-02.02 normalize-provider-errors-and-metadata
TP-03 contracts-docs-tests
├── TP-03.01 update-regression-tests
└── TP-03.02 update-docs-and-agents
TP-04 validation-closeout
├── TP-04.01 run-local-gates
└── TP-04.02 close-task-docs
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 IMP-03：执行器与 Provider 层。
- 延续 0010/0011：resource/API/job 已有第一版，本轮把 `CapabilityExecutor` 后方的执行边界资源化。
- 对齐基础设施定位：所有 production capability 必须能报告 provider metadata、engineVersion、deterministic 和 health。
- 对齐安全边界：planned 能力只能发现和审计，不允许执行。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | Provider 协议和注册表 | `fate_core/capabilities/providers.py` |
| TP-02 | Executor 改造 | `fate_core/capabilities/executor.py` |
| TP-03 | 回归和文档 | `test_capability_protocol.py`、`test_api_contracts.py`、AGENTS、100% 计划 |
| TP-04 | 验证和收口 | pytest、ruff、mypy、quick CI、task validators |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
