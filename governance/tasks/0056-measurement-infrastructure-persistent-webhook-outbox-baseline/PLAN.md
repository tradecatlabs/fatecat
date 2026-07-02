# Planning Summary

本任务继续 `MI-NEXT-03`，把 webhook callback 从“事件轨迹里能看到 attempt”推进到“SQLite 中存在独立持久 outbox record”。它证明的是 outbox 状态可审计和可跨 manager 读取，不证明外部 backend、重启自动重投或公网 live callback。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 SQLite outbox baseline 解释为 external backend、生产级重投或分布式 worker。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 persistent webhook outbox 本地 baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | outbox store、dispatch 写入、API payload 和 smoke 完成 | Done |
| TEST | focused tests 覆盖 outbox succeeded/failed、CLI 和隐私边界 | Done |
| REVIEW | 确认隐私安全、语义不夸大和 quick CI 稳定 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

新增一个轻量 outbox record：terminal webhook dispatch 开始前写 `pending`，每次 attempt 更新 attempts，成功写 `succeeded`，最终失败写 `failed`。SQLite store 持久化该 record；memory store no-op。API 返回脱敏摘要，smoke 用临时 SQLite 验证跨 manager rebuild 可读。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 outbox baseline。
- TP-03：补 smoke、测试和 quick CI。
- TP-04：文档、验证与交付。

# Future-Optimal Contract

- target end state: durable runtime 具备可恢复、可重试、可回放、可审计的 callback outbox 控制面。
- real constraints: 当前只有 memory/sqlite 单进程 baseline，webhook secret 只驻留内存。
- inertia constraints: 不能把 event history 当成 outbox，也不能把同步 dispatch 当成持久队列。
- kill list: 保存 webhook secret、输出完整 callback URL、声称重启自动重投、依赖公网。
- proof point: SQLite outbox record 跨 manager rebuild 可读取，summary 不泄露敏感信息。
- falsifier: outbox 记录无法稳定写入、API 泄露 URL/secret/用户输入，或 quick CI flaky。
- migration slice: 先将 outbox 记录资源化；后续 external backend/secret vault/worker lease 再实现自动重投。

# Ponytail Contract

- existence check: persistent outbox 是 durable runtime 发布门禁的必要对象。
- selected ladder rung: 复用现有 manager/store，新建最小 dataclass、SQLite 表和 smoke。
- skipped scope: 不新增 external backend，不新增 worker lease，不存 secret。
- ceiling / upgrade path: 需要重启自动重投时，升级 encrypted callback config + external outbox worker。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + smoke + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、local-ci、git status。
- stop conditions: outbox 设计需要持久保存 secret 才能满足验收，或文档无法避免能力夸大。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: quick local CI 增加 webhook outbox smoke。
- Source-of-truth updates: API 文档、roadmap、scripts/tests AGENTS、task index。
- Contract/catalog/schema impact: API payload 增加 `webhookOutbox` 脱敏摘要，由 regression test 保护。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02, TP-02.03 | 实现 outbox baseline。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Smoke、测试和 CI。 |
| 4 | TP-04.01, TP-04.02 | 文档、验收和交付。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | None. |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚代码：移除 outbox record/store/API/smoke/local-ci/test 变更。
- 回滚文档：移除 0056 任务包、INDEX 行和文档更新。
- DB schema 只新增表；回滚不需要迁移现有业务数据。
