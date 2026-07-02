# Task Overview

- Task ID: `0052`
- Slug: `measurement-infrastructure-durable-runtime-event-history`
- Objective: `执行 MI-NEXT-03 durable runtime 二期的首个可验证切片：为 CalculationJob 增加内存/SQLite 可审计 event history，API 返回 CalculationJobEvent，并同步任务、文档和回归测试；不实现 retry/timeout、callback retry/outbox、external backend 或分布式 worker。`
- Status: `Done`

## In Scope

- 为 report job 状态机补充 `ReportJobEvent` 模型。
- 让 `memory` 与 `sqlite` job store 都能保存并读取按顺序排列的 job event history。
- 在异步报告 job API 响应中暴露 `CalculationJobEvent` 列表。
- 覆盖成功、SQLite 重建、旧 running/queued recovery failed 和隐私脱敏回归。
- 同步 API 文档、路线图和 delivery 模块边界说明。

## Out of Scope

- 不实现 retry/timeout/non-retryable policy。
- 不实现 webhook callback retry/outbox。
- 不接 Temporal、Celery、Redis、Postgres 或其他 external backend。
- 不实现跨进程继续执行、生产多副本锁或分布式 worker。
- 不把 webhook payload 改成 CloudEvents/AsyncAPI 完整规范；本切片只先补 job event history。

## Task Package Tree

```text
TP-01 当前 durable runtime 缺口复核
  TP-01.01 读取既有 job store、webhook baseline、API 文档、roadmap 与当前 diff
TP-02 CalculationJob event history 实现
  TP-02.01 增加 ReportJobEvent 模型、memory/sqlite event store 和状态机事件写入
  TP-02.02 在 API CalculationJob 响应中暴露 CalculationJobEvent
TP-03 回归测试与文档同步
  TP-03.01 增加 report job event history、SQLite persistence 和隐私回归断言
  TP-03.02 更新 API 文档、roadmap、delivery AGENTS 和任务索引
TP-04 验收与交付
  TP-04.01 运行 focused tests、task docs validators、lint/hygiene 和 git 交付检查
```

## Requirement Alignment

- 对齐用户要求：持续推进 100% 测算基础设施实现计划，优先处理 durable runtime。
- 对齐 0051 路线图：`MI-NEXT-03` 需要 job event history、retry/timeout、restart recovery 和 callback retry；本任务只完成第一个可验证切片。
- 对齐基础设施同构资料：Temporal 类 durable execution 的核心能力之一是 event history；Stripe 类异步交付强调幂等和事件可审计。
- 对齐项目边界：本地 SQLite 是单副本持久状态 baseline，不能伪装成生产分布式任务系统。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 durable runtime 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取既有 job store、webhook、API 文档和 roadmap。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 CalculationJob event history。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 event 模型、store 和状态机事件写入。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | API 响应暴露 CalculationJobEvent。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | 补回归测试和文档同步。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 增加 event history、SQLite persistence 和隐私回归断言。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 更新 API 文档、roadmap、delivery AGENTS 和任务索引。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.02 | - | No | No | 校验并交付。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.02 | 4 | No | No | 运行 focused tests、任务文档校验、lint/hygiene 与 git 检查。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
