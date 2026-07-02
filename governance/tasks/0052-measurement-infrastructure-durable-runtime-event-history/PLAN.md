# Planning Summary

本任务把 `MI-NEXT-03 durable runtime 二期` 拆成第一个可交付切片：先让 `CalculationJob` 有可审计 event history。这样后续 retry/timeout、callback retry/outbox 和 external backend 可以基于同一条历史轨迹继续演进，而不是继续只看最终状态。

# Lifecycle Gates

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 确认 0051 路线图中 `MI-NEXT-03` 的第一缺口是 job event history | Done |
| PLAN | 拆出 event history 独立任务，明确不实现 retry/outbox/external backend | Done |
| BUILD | 在 report job manager、store 和 API envelope 中实现事件记录与输出 | Done |
| TEST | 用 focused pytest 覆盖 success、SQLite rebuild、recovered failed 和隐私断言 | Done |
| REVIEW | 检查代码边界、文档口径、隐私、安全和性能 | Done |
| SHIP | 通过任务文档校验、diff hygiene、必要 lint/test 后提交推送 | Done |

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。

# Simplest Path

最简单可靠路径是复用已有 `ReportJobManager` 状态转移点，在每个关键状态变化后 append event。这样不新增后台 worker、不引入外部依赖、不改变任务执行模型，只增加审计历史。

# Split Strategy

- `TP-01` 只确认现状和边界。
- `TP-02` 只做代码实现。
- `TP-03` 做测试和文档同步。
- `TP-04` 做验证和交付。

# Future-Optimal Contract

- target end state: 所有长流程测算任务都具备可恢复、可重试、可回放、可审计的事件历史。
- real constraints: 当前公开 API、SQLite baseline、memory default 和 webhook baseline 已存在。
- inertia constraints: 不能因为当前只有单进程实现，就把 event history 设计成临时日志字符串。
- kill list: 隐式事件、只写日志不进 job resource、把 SQLite baseline 宣称为分布式 runtime。
- proof point: API 返回 `CalculationJobEvent`，SQLite 重建后仍能读取事件历史。
- falsifier: event history 泄露用户姓名/地区/Markdown，或无法跨 manager 读取 SQLite events。
- migration slice: 先引入 event table 和 API events 字段，后续 retry/outbox/external backend 复用事件历史。

# Ponytail Contract

- existence check: event history 是 durable runtime 的必要对象，因为只看最终状态无法审计执行过程。
- selected ladder rung: 复用现有 manager/store 抽象，不新增任务框架或外部依赖。
- skipped scope: 不新增 Temporal/Celery/Redis/Postgres；不做 CloudEvents 全量迁移。
- ceiling / upgrade path: 当需要多副本、retry/outbox 和恢复执行时，再引入 external backend 或 durable workflow engine。
- minimal runnable check: focused pytest 证明 events 在 API 和 SQLite persistence 中可见。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`git status`、`validate_task_docs.py`、`validate_tasks_tree.py`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: task docs + code diff + validation evidence + git delivery state。
- evidence required: pytest 输出、task validators 输出、diff hygiene、git status。
- stop conditions: event history 泄露用户隐私、API 回归失败、任务文档校验失败。

# Document-Driven Contract

- Operating model update: 不需要更新项目操作模型；当前是 existing roadmap 的实现切片。
- Toolchain model update: 不新增工具链。
- Process update: 不新增流程。
- Source-of-truth updates: API 文档、roadmap、delivery AGENTS、task index。
- Contract/catalog/schema impact: 本切片不新增 JSON schema 文件；API envelope 字段由回归测试保护。
- Documentation exemption reason: 无；文档必须同步。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核边界。 |
| 2 | TP-02.01, TP-02.02 | 实现 event history。 |
| 3 | TP-03.01, TP-03.02 | 测试和文档。 |
| 4 | TP-04.01 | 验收和交付。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-04.01 | 完成 docs 同步后运行 focused tests、validators、lint/hygiene 和 git 检查。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol

- 回滚代码：还原 `report_jobs.py`、`main.py`、`test_api_contracts.py` 中 event history 相关 diff。
- 回滚文档：移除 0052 任务包、INDEX 行、API 文档和 roadmap 的 0052 说明。
- 数据兼容：SQLite 新增表是附加表；如需禁用，旧 job table 仍可被读取。
