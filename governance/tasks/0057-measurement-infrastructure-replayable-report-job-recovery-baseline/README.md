# Task Overview

- Task ID: `0057`
- Slug: `measurement-infrastructure-replayable-report-job-recovery-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第六个可验证切片：为 report job 增加可序列化 task payload、task factory 和 SQLite manager 重建后重新入队执行 baseline；让 Web/Markdown 两类生产报告任务具备本地跨 manager 重建继续执行能力。范围不包含 external backend、分布式 worker lease、多副本锁、持久 webhook secret 或真实公网 webhook live smoke。`
- Status: `Done`

## In Scope

- 在 `ReportJobManager` / `SQLiteReportJobStore` 中增加可选 `task_payload` 持久化。
- 增加 `task_factories` 注册入口，让可序列化任务能在 manager 重建后恢复 callable。
- 对 Web 报告任务和标准 Markdown 报告任务传入可重建 payload。
- 增加本地 smoke，证明 SQLite 中 queued/running 可重建任务会重新入队并成功完成。
- 保持无 payload 的遗留/非可重建任务继续安全失败，兼容 0055 restart-safe failure 语义。
- 接入 quick local CI、回归测试、API 文档、roadmap、scripts/tests AGENTS 和任务索引。

## Out of Scope

- 不实现 Redis/Postgres/Temporal/Celery adapter。
- 不实现分布式 worker lease、抢占锁、多副本并发调度或生产级 exactly-once。
- 不持久保存 webhook URL、webhook secret 或请求 payload 正文。
- 不执行真实公网 webhook live smoke。
- 不声明 durable runtime 二期完成。

## Task Package Tree

```text
TP-01 Recovery 缺口复核
  TP-01.01 读取 roadmap、0055/0056、report job 源码、API submit 路径和测试
TP-02 Replayable task baseline 实现
  TP-02.01 增加 task_payload 持久化和 store schema
  TP-02.02 增加 task_factories 与重建重新入队逻辑
  TP-02.03 Web/Markdown 报告任务接入可重建 payload
TP-03 Smoke、测试与 CI
  TP-03.01 新增 replayable recovery smoke 与 shell wrapper
  TP-03.02 增加 regression tests，覆盖 requeue success 和 non-replayable failure
  TP-03.03 接入 local-ci quick
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 roadmap：`MI-100.02.05 external backend decision and adapter` 之前的本地可恢复执行基线。
- 对齐安全边界：只持久保存可重建的任务输入摘要/结构化 payload，不保存 Python callable、webhook secret、完整 callback URL 或报告正文。
- 对齐基础设施目标：长任务不再只能在 manager 重建后终止，生产报告任务具备可审计的恢复执行路径。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 replayable report job 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、任务事实、源码、API submit 路径和测试。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 replayable task baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 task_payload 持久化和 store schema。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 增加 task_factories 与重建重新入队逻辑。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-02.02 | 2 | No | No | Web/Markdown 报告任务接入可重建 payload。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.03 | - | No | No | Smoke、测试与 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.03 | 3 | No | No | 新增 replayable recovery smoke 与 shell wrapper。 |
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
