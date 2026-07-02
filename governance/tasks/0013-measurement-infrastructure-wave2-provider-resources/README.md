# Task Overview
- Task ID: `0013`
- Slug: `measurement-infrastructure-wave2-provider-resources`
- Objective: `执行测算基础设施 100% 实现计划 Wave 2 的第二个切片：把已落地的 production provider registry 资源化，新增 Provider schema、/providers 与 /providers/{provider_id} 发现入口、metadata 链接、API 回归测试和文档说明。`
- Status: `Done`

## In Scope
- 新增 provider schema 资产，描述 Provider resource 字段。
- 新增 `/api/v1/providers`、`/providers`、`/api/v1/providers/{provider_id}`、`/providers/{provider_id}`。
- `/metadata` 暴露 provider list/detail 入口。
- `Capability` resource links 增加 provider 资源链接。
- 更新 API 回归测试、API 接入文档、100% 实现计划和 0013 任务文档。

## Out of Scope
- 不实现跨进程 provider health。
- 不探测外部 API/token/Bot/webhook。
- 不新增 provider 后端或异步执行引擎。
- 不改变 provider registry 或 capability 计算结果。
- 不将 planned capability 生成生产 provider。

## Task Package Tree
```text
TP-01 provider-resource-contract
├── TP-01.01 add-provider-schema
└── TP-01.02 expose-provider-schema-ref
TP-02 provider-api
├── TP-02.01 add-provider-list-and-detail
└── TP-02.02 link-capability-to-provider
TP-03 tests-and-docs
├── TP-03.01 add-provider-api-regression
└── TP-03.02 update-api-docs-and-roadmap
TP-04 validation-closeout
├── TP-04.01 run-local-gates
└── TP-04.02 close-task-docs
```

## Requirement Alignment
- 对齐 100% 实现计划 IMP-01：Provider 作为基础设施资源。
- 对齐 IMP-02：外部开发者通过发现 API 接入，不读源码。
- 对齐 0012：provider registry 已存在，本轮只暴露资源接口。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | Provider schema | `contracts/fate/capabilities/schemas/provider.schema.json` |
| TP-02 | Provider API | `main.py` |
| TP-03 | 回归和文档 | `test_api_contracts.py`、API 接入文档、100% 计划 |
| TP-04 | 验证和收口 | pytest、ruff、mypy、quick CI、task validators |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
