# Task Overview

- Task ID: `0053`
- Slug: `measurement-infrastructure-report-job-retry-timeout-policy`
- Objective: `执行 MI-NEXT-03 durable runtime 二期的第二个可验证切片：为 CalculationJob/report job 增加声明式 retry/timeout/non-retryable policy、本地事件证据、API 可见字段、回归测试与文档说明；不实现 callback retry/outbox、external backend、分布式 worker 或生产级硬中断。`
- Status: `Done`

## In Scope

- 新增 report job execution policy：`maxAttempts`、`attemptTimeoutSeconds`、`retryBackoffSeconds`、non-retryable error。
- 让 report job 状态机在 retry、timeout、non-retryable 场景写入可审计 events。
- 让 API `CalculationJob` payload 暴露执行策略与已尝试次数。
- 增加 focused regression tests，覆盖 retry 成功、non-retryable 不重试、timeout 失败。
- 同步 API 文档、roadmap、deployment docs、production-readiness 和任务索引。

## Out of Scope

- 不实现 webhook callback retry/outbox。
- 不实现 external backend、Temporal/Celery/Redis/Postgres adapter。
- 不实现跨进程继续执行或生产多副本锁。
- 不承诺 Python callable 被物理强杀；当前 timeout 是本地任务状态超时 baseline。
- 不改变 Markdown 报告正文、命理计算核心、Web HTML 视觉或 Bot 文案。

## Task Package Tree

```text
TP-01 当前 runtime policy 缺口复核
  TP-01.01 读取 0052、roadmap、report job 源码、API 文档和生产预检
TP-02 Retry/timeout policy 实现
  TP-02.01 新增 execution policy 模型、job 字段、SQLite schema 兼容和 API payload 字段
  TP-02.02 修改状态机，支持 retry、timeout、non-retryable 事件和最终状态
TP-03 回归测试与文档同步
  TP-03.01 增加 retry 成功、non-retryable 不重试、timeout 失败和 SQLite policy persistence 测试
  TP-03.02 更新 API 文档、roadmap、deployment docs、production-readiness、AGENTS 和 INDEX
TP-04 验收与交付
  TP-04.01 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 0051/0052 后续路线图：`MI-100.02.02 retry/timeout/non-retryable policy`。
- 对齐基础设施同构：重试必须是声明式策略，不能隐藏在异常处理里。
- 对齐当前架构：继续复用 `ReportJobManager` 和 `ReportJobStore`，不引入新 runtime。
- 对齐安全边界：事件 metadata 不记录姓名、出生地区、Markdown 正文、请求体或 secret。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 retry/timeout policy 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 0052、roadmap、源码、API 文档和生产预检。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 retry/timeout policy。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 execution policy 模型、job 字段、SQLite schema 和 API 字段。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 修改状态机支持 retry、timeout、non-retryable。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | 补测试和文档。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 增加 policy 回归测试。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 更新文档、预检、AGENTS 和任务索引。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.02 | - | No | No | 验收和交付。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.02 | 4 | No | No | 运行验证并提交推送。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
