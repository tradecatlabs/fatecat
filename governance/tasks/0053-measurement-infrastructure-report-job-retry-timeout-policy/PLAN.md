# Planning Summary

本任务继续 `MI-NEXT-03`，把 report job 从“失败即终态”推进到“声明式执行策略”：默认不重试，显式配置后支持有限 retry、attempt timeout 和 non-retryable error。它是 durable runtime 的第二个本地可验证切片，不是生产分布式工作流。

# Lifecycle Gates

禁止跳过任何 gate；不得把本地 retry/timeout baseline 解释为生产硬中断或 external backend。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 `MI-100.02.02 retry/timeout/non-retryable policy` | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | policy 模型、状态机、API 字段和 SQLite schema 完成 | Done |
| TEST | focused tests 覆盖 retry、non-retryable、timeout、persistence | Done |
| REVIEW | 确认默认行为兼容、隐私安全和文档不过度声明 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

复用现有 `ReportJobManager`，在 `_run_job` 内部循环执行 attempt；默认 `maxAttempts=1`，所以现有行为保持不变。timeout 只在显式配置时使用 daemon attempt thread 管理任务状态，不引入新 worker runtime。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 policy 与状态机。
- TP-03：补测试和文档。
- TP-04：验证与交付。

# Future-Optimal Contract

- target end state: 所有长流程任务都由可审计 policy 控制重试、超时和不可重试错误。
- real constraints: 当前只有单进程 worker 和 SQLite baseline；不能伪装成生产 durable workflow。
- inertia constraints: 不能继续只靠裸 `except Exception` 作为长期错误策略。
- kill list: 隐式无限重试、无界 timeout、记录请求体、timeout 后宣称 callable 已被强杀。
- proof point: tests 证明 retry 成功、non-retryable 不重试、timeout 失败且 events 可审计。
- falsifier: 默认成功路径事件序列变化或 API 报告任务回归失败。
- migration slice: 先把 policy 进入 job resource；后续 callback retry/outbox 和 external backend 复用同一语义。

# Ponytail Contract

- existence check: retry/timeout policy 是基础设施任务控制面的必要对象。
- selected ladder rung: 复用现有 manager/store，新增小型 policy dataclass。
- skipped scope: 不引入 Temporal/Celery/Redis/Postgres，不做 hard kill。
- ceiling / upgrade path: 需要生产硬 timeout、多副本和 outbox 时，升级 external backend。
- minimal runnable check: focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + docs diff + task docs + validation evidence + commit/push。
- evidence required: focused tests、validators、ruff、local-ci、git status。
- stop conditions: 默认路径回归、timeout 测试不稳定、隐私泄漏、docs validator 失败。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: 不需要。
- Source-of-truth updates: API 文档、roadmap、deployment docs、production-readiness、delivery AGENTS、task index。
- Contract/catalog/schema impact: 不新增独立 JSON schema；API contract tests 保护新增字段。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02 | 实现 policy 和状态机。 |
| 3 | TP-03.01, TP-03.02 | 测试和文档。 |
| 4 | TP-04.01 | 验收和交付。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-01.01 | 复核当前源码、roadmap 和文档。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol

- 回滚代码：还原 `report_jobs.py`、`main.py`、`test_api_contracts.py` 和 `production-readiness.sh` 中 policy 相关 diff。
- 回滚文档：移除 0053 任务包、INDEX 行和文档更新。
- SQLite 兼容：新增列带默认值，回滚代码后旧 job table 仍可读取基础字段。
