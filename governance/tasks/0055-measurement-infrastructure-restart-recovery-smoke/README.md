# Task Overview

- Task ID: `0055`
- Slug: `measurement-infrastructure-restart-recovery-smoke`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第四个可验证切片：把 SQLite report job manager rebuild/restart recovery 行为提升为可独立运行的本地 smoke、local-ci 门禁和文档证据；不实现跨进程继续执行、external backend、分布式 worker 或生产级任务恢复。`
- Status: `Done`

## In Scope

- 新增 `report-job-restart-recovery-smoke` 脚本，验证 SQLite backend 在 manager 重建后把旧 `running` / `queued` job 标记为 `failed`。
- 验证 `job.recovered_failed` 事件历史可读取、幂等键仍指向同一 job、隐私边界不泄露用户输入。
- 把 smoke 接入 quick local CI。
- 增加 regression test 覆盖脚本与 CLI 输出。
- 同步 API 文档、roadmap、scripts AGENTS、任务索引和 0055 closeout 文档。

## Out of Scope

- 不实现未完成任务跨进程继续执行。
- 不实现 external backend、Temporal/Celery/Redis/Postgres adapter。
- 不实现多副本抢锁、分布式 worker、生产硬 timeout 或 persistent callback outbox。
- 不读取真实 `.env`、token、secret、生产数据库或公网服务。

## Task Package Tree

```text
TP-01 Restart recovery 缺口复核
  TP-01.01 读取 roadmap、0054、report job 源码、现有 SQLite rebuild tests 和 local-ci
TP-02 Restart recovery smoke 实现
  TP-02.01 新增 Python smoke 和 shell wrapper
  TP-02.02 接入 local-ci quick 门禁
TP-03 回归测试与文档同步
  TP-03.01 增加 smoke regression test
  TP-03.02 更新 API 文档、roadmap、scripts AGENTS 和 INDEX
TP-04 验收与交付
  TP-04.01 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 0051/0054 后续路线图：`MI-100.02.03 restart recovery smoke`。
- 对齐 durable runtime 目标：重启后不能让旧 running/queued job 假装仍可继续执行。
- 对齐当前架构：复用 `SQLiteReportJobStore` 和 `ReportJobManager._load_persisted_jobs()` 行为，不新增 runtime。
- 对齐安全边界：smoke 只使用北京/测试样本，不输出 Markdown 正文、姓名、出生地区、token、secret 或 DSN。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 restart recovery 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、0054、源码、测试和 local-ci。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 restart recovery smoke。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 Python smoke 和 shell wrapper。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 接入 local-ci quick 门禁。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | 补测试和文档。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 增加 smoke regression test。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 更新文档、AGENTS 和任务索引。 |
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
