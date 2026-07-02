# Planning Summary

本任务继续 `MI-NEXT-03`，把 report job webhook callback 从“一次性附属投递”推进到“有策略、有事件轨迹、可审计的本地 callback delivery baseline”。它不是生产级持久 outbox，也不替代 external backend。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 webhook retry/outbox trail baseline 解释为生产持久 outbox、external backend 或真实公网 webhook live smoke。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 `MI-100.02.04 callback retry/outbox` 的本地 baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | webhook policy、manager retry 状态机和 env 入口完成 | Done |
| TEST | focused tests 覆盖 retry success、final failure、default once 和隐私边界 | Done |
| REVIEW | 确认默认行为兼容、隐私安全和文档不过度声明 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

复用现有 `ReportJobManager._dispatch_terminal_webhook()`，在 manager 内增加小型 `ReportJobWebhookPolicy`，默认 `maxAttempts=1`。`HttpWebhookDispatcher` 仍只负责一次 HTTP 投递；manager 负责 attempt loop、backoff 和 event history。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 webhook policy 与 retry 状态机。
- TP-03：补测试和文档。
- TP-04：验证与交付。

# Future-Optimal Contract

- target end state: callback delivery 有持久 outbox、幂等事件、retry policy、签名、可观测和审计。
- real constraints: 当前只有单进程 manager、memory/sqlite event store 和本地 webhook dispatcher。
- inertia constraints: 不能继续让 callback failure 只靠一条最终失败事件表达。
- kill list: 无限 retry、把 webhook secret/URL 写入事件、把本地 retry 宣称为持久 outbox、吞掉 callback 失败无证据。
- proof point: tests 证明 webhook 第一次失败后可重试成功，最终失败有 attempt trail，默认仍只投递一次。
- falsifier: 默认 webhook 成功路径事件序列破坏，或 event metadata 出现 URL/secret/用户输入/原始异常文本。
- migration slice: 先建立 delivery attempt 语义；后续持久 outbox/external backend 复用同一 event trail。

# Ponytail Contract

- existence check: callback retry/outbox trail 是基础设施异步副作用投递的必要对象。
- selected ladder rung: 复用现有 manager/dispatcher，新增小型 policy dataclass。
- skipped scope: 不引入 Temporal/Celery/Redis/Postgres，不建持久 outbox 表。
- ceiling / upgrade path: 需要跨进程恢复、幂等锁和大规模 callback 时，升级 external backend/outbox 表。
- minimal runnable check: focused pytest + webhook smoke + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + docs diff + task docs + validation evidence + commit/push。
- evidence required: focused tests、webhook smoke、validators、ruff、local-ci、git status。
- stop conditions: webhook event 泄露隐私、默认行为回归、文档将本地 baseline 夸大为生产持久 outbox。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: 不需要。
- Source-of-truth updates: API 文档、roadmap、deployment docs、production-readiness、delivery AGENTS、task index。
- Contract/catalog/schema impact: 不新增独立 JSON schema；API/event contract tests 保护新增事件字段。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02 | 实现 policy 和 retry 状态机。 |
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

- 回滚代码：还原 `report_jobs.py`、`main.py`、`test_api_contracts.py` 和 `production-readiness.sh` 中 webhook policy 相关 diff。
- 回滚文档：移除 0054 任务包、INDEX 行和文档更新。
- 事件兼容：新增事件只追加，不修改已有 job event 表结构。
