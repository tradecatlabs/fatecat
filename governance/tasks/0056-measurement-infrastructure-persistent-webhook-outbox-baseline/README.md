# Task Overview

- Task ID: `0056`
- Slug: `measurement-infrastructure-persistent-webhook-outbox-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第五个可验证切片：为 report job webhook callback 增加 SQLite 本地持久 outbox baseline、API 可见状态、smoke、quick CI 门禁和文档证据；不实现公网 live webhook、跨进程自动重投、external backend、生产多副本 worker 或加密 secret 存储。`
- Status: `Done`

## In Scope

- 在 `ReportJobStore` / `SQLiteReportJobStore` 中增加 webhook outbox record 的持久化能力。
- 在 `ReportJobManager` webhook dispatch 前后记录 outbox pending / succeeded / failed 状态。
- 在 `CalculationJob` API payload 中暴露脱敏 outbox 状态摘要。
- 新增 `webhook-outbox-smoke` 脚本，验证 SQLite outbox 记录跨 manager 重建可读取。
- 把 smoke 接入 quick local CI，并补 regression test。
- 同步 API 文档、roadmap、scripts/tests AGENTS、任务索引和 0056 closeout 文档。

## Out of Scope

- 不保存 webhook secret。
- 不保存完整 webhook URL 或 payload 正文到 event metadata。
- 不实现跨进程自动重投或后台 outbox worker。
- 不实现 external backend、Temporal/Celery/Redis/Postgres adapter。
- 不执行真实公网 webhook live smoke。

## Task Package Tree

```text
TP-01 Persistent webhook outbox 缺口复核
  TP-01.01 读取 roadmap、0054/0055、report job/webhook 源码、测试和 local-ci
TP-02 SQLite outbox baseline 实现
  TP-02.01 增加 outbox record 模型、store 接口和 SQLite 表
  TP-02.02 在 webhook dispatch 生命周期写入 outbox 状态
  TP-02.03 在 API payload 暴露脱敏 outbox 摘要
TP-03 Smoke、测试与 CI
  TP-03.01 新增 webhook outbox smoke 与 shell wrapper
  TP-03.02 增加 regression tests
  TP-03.03 接入 local-ci quick
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 roadmap：`MI-100.02.04 callback retry/outbox` 的 persistent outbox baseline。
- 对齐安全边界：outbox 只保存脱敏 delivery 状态，不保存 webhook secret、报告正文、用户输入或完整 callback URL。
- 对齐基础设施目标：callback delivery 不再只有事件日志，而是具备独立可查询的持久资源记录。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 persistent outbox 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、任务事实、源码、测试和 local-ci。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 SQLite outbox baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 outbox record 模型、store 接口和 SQLite 表。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | webhook dispatch 生命周期写入 outbox 状态。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-02.02 | 2 | No | No | API payload 暴露脱敏 outbox 摘要。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.03 | - | No | No | Smoke、测试与 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.03 | 3 | No | No | 新增 webhook outbox smoke 与 shell wrapper。 |
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
