# Task Overview

- Task ID: `0060`
- Slug: `measurement-infrastructure-webhook-outbox-lease-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第九个可验证切片：在 0058/0059 的 SQLite webhook outbox redelivery 与 encrypted config vault baseline 之后，为 SQLite webhook outbox 增加本地 claim/release lease baseline；避免多个 manager 重建时重复重投同一条 failed/pending webhook outbox record。本任务不实现 external backend、生产级分布式 worker lease、多副本锁、真实公网 webhook live smoke、外部 Vault/KMS 或 exactly-once。`
- Status: `In Progress`

## In Scope

- 为 `ReportJobStore` 增加 webhook outbox claim/release lease 接口。
- 为 SQLite outbox 表增加 lease owner、lease acquired/expires 字段和迁移。
- Manager redelivery 先 claim 再 dispatch，dispatch 结束 release；claim 失败不重投。
- 增加本地 smoke、回归测试、quick CI、API 文档、roadmap、AGENTS 和任务索引。

## Out of Scope

- 不实现 Redis/Postgres/Temporal/Celery adapter。
- 不实现生产级分布式 worker lease、多副本锁、clock skew 策略或 exactly-once。
- 不实现真实公网 webhook live smoke。
- 不改公开 webhook payload 和 API outbox 脱敏结构。
- 不把 SQLite lease baseline 声明为 external backend 或最终生产队列。

## Task Package Tree

```text
TP-01 Lease 缺口复核
  TP-01.01 读取 roadmap、0058/0059、report job/outbox 源码与 smoke
TP-02 SQLite outbox lease 实现
  TP-02.01 增加 store claim/release 接口和 SQLite lease schema
  TP-02.02 Manager redelivery 接入 claim/release
TP-03 Smoke、测试与 CI
  TP-03.01 新增 webhook outbox lease smoke 与 shell wrapper
  TP-03.02 增加 regression tests 覆盖 claim 冲突、release、重投一次和隐私
  TP-03.03 接入 local-ci quick
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 roadmap：`MI-NEXT-03` 剩余缺口中的 `生产级分布式 worker lease`，本任务只落本地 SQLite lease semantics baseline。
- 对齐 0058：redelivery 仍保留 resolver 路径。
- 对齐 0059：encrypted config vault 仍可作为无 resolver redelivery fallback。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 outbox lease 缺口和现有边界。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、任务事实、源码和 smoke。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 SQLite outbox lease baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 store claim/release 和 SQLite lease schema。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | Manager redelivery 接入 claim/release。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | Smoke、测试与 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 smoke 与 shell wrapper。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 增加 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并提交推送。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
