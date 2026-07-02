# Task Overview

- Task ID: `0058`
- Slug: `measurement-infrastructure-webhook-outbox-redelivery-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第七个可验证切片：在 0056 SQLite persistent webhook outbox record baseline 和 0057 replayable report job recovery baseline 之后，为 report job webhook outbox 增加本地可验证的自动重投 baseline；让 failed/pending outbox record 在 manager 重建后可通过注册的 delivery resolver 重新投递并更新 outbox/event 状态。范围不包含公网 live webhook、external backend、分布式 worker lease、多副本锁、持久明文 webhook secret 或 exactly-once。`
- Status: `Done`

## In Scope

- 为 webhook outbox 增加本地重投入口，支持 SQLite manager 重建后扫描 pending/failed outbox record。
- 增加可注入 delivery resolver，用 job/outbox 摘要重建 callback 配置，不在 outbox 中保存明文 secret 或完整 URL。
- 增加 outbox redelivery 事件：至少覆盖重新调度、成功、失败。
- 增加本地 smoke，证明 persisted failed outbox 可在新 manager 中自动重投成功。
- 保持默认行为兼容：未提供 resolver 时不自动重投，只保留可审计 outbox 记录。
- 接入 quick local CI、回归测试、API 文档、roadmap、scripts/tests AGENTS 和任务索引。

## Out of Scope

- 不实现 Redis/Postgres/Temporal/Celery adapter。
- 不实现分布式 worker lease、抢占锁、多副本并发调度或 exactly-once。
- 不持久保存 webhook URL、webhook secret、请求 payload 正文或报告 Markdown。
- 不执行真实公网 webhook live smoke。
- 不声明 durable runtime 二期或 100% 测算基础设施完成。

## Task Package Tree

```text
TP-01 Redelivery 缺口复核
  TP-01.01 读取 roadmap、0054/0056/0057、report job webhook 源码和测试
TP-02 Webhook outbox redelivery baseline 实现
  TP-02.01 增加 outbox pending/failed 查询和 redelivery API
  TP-02.02 增加 delivery resolver 与重投调度逻辑
  TP-02.03 增加 redelivery 事件和隐私边界
TP-03 Smoke、测试与 CI
  TP-03.01 新增 webhook outbox redelivery smoke 与 shell wrapper
  TP-03.02 增加 regression tests，覆盖 resolver success、resolver missing 和 resolver error boundary
  TP-03.03 接入 local-ci quick
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 roadmap：`MI-NEXT-03` 剩余缺口中的 `跨进程 webhook 自动重投`，先落地单机 SQLite + resolver baseline。
- 对齐安全边界：outbox 仍只保存 target host hash 和投递摘要；真实 URL/secret 由运行时 resolver 提供，不进入持久 outbox。
- 对齐基础设施目标：webhook callback 从“持久记录可审计”推进到“失败记录可被新 manager 自动重投”。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 webhook outbox redelivery 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、任务事实、源码和测试。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 redelivery baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 outbox pending/failed 查询和 redelivery API。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 增加 delivery resolver 与重投调度逻辑。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-02.02 | 2 | No | No | 增加 redelivery 事件和隐私边界。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.03 | - | No | No | Smoke、测试与 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.03 | 3 | No | No | 新增 redelivery smoke 与 shell wrapper。 |
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
