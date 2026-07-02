# Task Overview

- Task ID: `0062`
- Slug: `measurement-infrastructure-runtime-backend-contract`
- Objective: `执行 0061 后续任务树的第一个 P0 切片：为 CalculationJob durable runtime 新增 external backend contract baseline，登记 memory/sqlite/postgres/temporal/redis_queue 的成熟度、生产边界、证据要求和迁移路径，新增 runtime backend gate、回归测试、文档和任务 closeout；本任务不实现真实 Postgres/Temporal adapter、不声明 external backend 已生产。`
- Status: `Done`

## In Scope

- 新增 RuntimeBackend schema 与 registry，登记 memory、sqlite、postgres、temporal、redis_queue。
- 更新 delivery registry、resource schema 和 AGENTS，让 RuntimeBackend 成为可发现资源。
- 新增 `runtime-backend-gate` 脚本和回归测试，接入 quick local CI artifact。
- 更新 API 接入文档、100% roadmap、scripts/delivery AGENTS 和任务索引。

## Out of Scope

- 不实现 Postgres、Temporal、Redis adapter。
- 不连接真实数据库或外部服务。
- 不实现生产级分布式 worker lease、exactly-once、真实公网 webhook live delivery。
- 不把 SQLite local lease 写成 external backend。
- 不读取、不输出、不保存真实 DSN、token、secret 或生产日志。

## Task Package Tree

```text
TP-01 Runtime backend 缺口复核
  TP-01.01 读取 0061、roadmap、delivery contracts、job store docs 和 gate 风格
TP-02 Contract baseline
  TP-02.01 新增 RuntimeBackend schema、registry 和 resource schema link
  TP-02.02 更新 delivery registry 与 delivery AGENTS
TP-03 Gate、测试和 CI
  TP-03.01 新增 runtime-backend-gate Python/sh wrapper
  TP-03.02 新增 regression tests 覆盖 contract、CLI 和边界声明
  TP-03.03 接入 local-ci quick artifact
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、scripts AGENTS 和任务索引
  TP-04.02 运行 focused tests、validators、lint/hygiene 和 quick local CI
```

## Requirement Alignment

- 对齐 0061 推荐任务：`0062 durable runtime external backend contract`。
- 对齐 100% roadmap：`CalculationJob` 仍缺 external backend、生产级分布式 worker lease、真实 crash/restart 证据。
- 对齐胶水原则：首个 external adapter 候选使用 Postgres 这类成熟基础设施；Temporal 只登记为后续长流程 orchestrator；Redis queue 不作为 source of truth。
- 对齐不可伪造原则：contract gate 通过不等于外部 backend 已生产。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核当前 durable runtime 缺口和契约落点。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 0061、roadmap、delivery contracts、job store docs 和 gate 风格。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 新增 RuntimeBackend contract baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 schema、registry、resource schema link。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 更新 delivery registry 与 AGENTS。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | Gate、测试和 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 runtime-backend-gate。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 新增 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并收口。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
