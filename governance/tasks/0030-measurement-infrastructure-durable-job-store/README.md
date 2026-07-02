# Task Overview
- Task ID: `0030`
- Slug: `measurement-infrastructure-durable-job-store`
- Objective: `把报告任务运行面从纯内存队列推进为本地可验证持久 job store baseline：新增 ReportJobStore 抽象与 SQLite backend，保持默认内存模式兼容，支持任务元数据、状态、结果、幂等键、取消和 TTL 过期跨 manager 重建可查询；补环境变量、文档、回归测试、任务 closeout。不实现 webhook、retry policy、分布式 worker、外部队列或生产多副本锁。`
- Status: `Done`

## In Scope
- 在 `report_jobs.py` 内新增 `ReportJobStore`、`InMemoryReportJobStore` 和 `SQLiteReportJobStore`。
- 保持默认 `memory` 后端和现有 API/Web 调用行为兼容。
- 新增 `FATE_REPORT_JOB_STORE=memory|sqlite` 与 `FATE_REPORT_JOB_DB_PATH` 配置。
- SQLite backend 持久化任务 metadata、status、result、input summary、idempotency key、取消状态和 TTL 过期状态。
- manager 重建时可查询已完成/失败/取消/过期任务；遗留 `queued/running` 任务标记为 `failed`，避免伪造跨进程继续执行。
- `/metadata` 与 `/metrics` 暴露 job store backend。
- 更新 production-readiness、env example、API 文档、observability/security registry、roadmap、AGENTS 和回归测试。

## Out of Scope
- 不实现 webhook callback、签名、重试或模拟器。
- 不实现 retry/timeout/non-retryable error policy。
- 不实现外部队列、Redis、Celery、RQ、Temporal 或多副本抢任务锁。
- 不保证 queued/running callable 跨进程继续执行。
- 不改变 report job API response shape、Markdown 生成逻辑、Web UI 或 Bot 行为。
- 不保存真实 token、请求体之外的新敏感字段或生产凭证。

## Task Package Tree
```text
TP-01 Job store 现状和边界确认
  TP-01.01 盘点 report job manager、API、metrics、文档和测试
  TP-01.02 回填任务契约、风险和验证计划
TP-02 Runtime job store baseline
  TP-02.01 新增 ReportJobStore 抽象、memory store 和 SQLite store
  TP-02.02 接入 ReportJobManager 持久化、重建恢复、幂等和取消
  TP-02.03 接入 main.py 环境变量、metadata、metrics 和 production-readiness
TP-03 回归测试与文档
  TP-03.01 新增 SQLite 持久化、幂等、取消和重建失败回归
  TP-03.02 更新 env example、API 文档、registry、roadmap 和 AGENTS
TP-04 验证收口
  TP-04.01 执行 JSON、focused tests、shell syntax、ruff/format、secret scan、quick CI、diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-03.01 Job store 抽象` 与 `MI-03.02 SQLite job backend`。
- 本任务只完成单副本本地持久状态 baseline；`MI-03.03` webhook、`MI-03.04` retry policy、`MI-03.05` restart recovery 的“继续执行”能力仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确 job store 范围 | 不扩成分布式任务系统 |
| TP-02 | BUILD | 实现 memory/sqlite store baseline | 默认 memory 不回归，SQLite 可跨 manager 查询 |
| TP-03 | TEST/DOC | 回归测试和文档同步 | 任务状态、幂等和取消被测试锁住 |
| TP-04 | SHIP | 执行门禁和 closeout | quick CI 与 validators 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
