# Planning Summary

本任务继续 `MI-NEXT-03`，把 webhook outbox 从“SQLite 可审计记录”推进到“SQLite manager 重建后可通过运行时 resolver 自动重投”。这是 external backend 和生产级 worker lease 之前的最小可验证迁移台阶。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 redelivery baseline 解释为 external backend、分布式 worker、真实公网 webhook live smoke 或 exactly-once。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖本地 SQLite outbox redelivery baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | outbox 查询、resolver、redelivery 事件和调度完成 | Done |
| TEST | focused tests 覆盖 redelivery success、resolver missing 和 resolver error boundary | Done |
| REVIEW | 确认隐私安全、兼容 0054/0056/0057 和 quick CI 稳定 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

复用现有 `ReportJobWebhookOutboxRecord`、`ReportJobSnapshot` 和 `webhook_dispatcher`。Store 增加 pending/failed outbox 查询；Manager 接受 `delivery_resolver`，启动时扫描 redeliverable outbox record。能解析配置则重建最小终态 snapshot 并复用现有 dispatch/retry 逻辑；不能解析则保留 record，不失败、不泄露配置。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 redelivery baseline。
- TP-03：补 smoke、测试和 quick CI。
- TP-04：文档、验证与交付。

# Future-Optimal Contract

- target end state: durable runtime 支持 external backend、任务恢复、webhook 持久投递、event history、worker lease 和审计。
- real constraints: 当前只有 memory/sqlite 单机 baseline，不能保存明文 secret。
- inertia constraints: 不把“只记录 outbox”当最终状态，不用明文持久 secret 换自动化。
- kill list: 持久明文 secret、完整 URL 输出、声称 exactly-once、引入未决外部队列。
- proof point: SQLite failed outbox record 在新 manager 中由 resolver 自动重投成功，并留下 redelivery 事件。
- falsifier: 无 resolver 时被错误投递、summary 泄露 secret/URL、quick CI flaky。
- migration slice: 先把 outbox redelivery 编排契约稳定下来；后续 external backend/lease/encrypted secret storage 可替换 resolver。

# Ponytail Contract

- existence check: webhook outbox redelivery 是从 callback audit trail 走向生产事件交付的必要对象。
- selected ladder rung: 复用现有 manager/store/dispatcher，只新增最小查询、resolver 和 smoke。
- skipped scope: 不引入外部队列，不新增 secret vault，不实现 worker lease。
- ceiling / upgrade path: 需要真实多副本生产时升级为 external backend + lease + encrypted callback config。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + smoke + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、secret scan、local-ci、git status。
- stop conditions: redelivery 必须持久明文 secret 或完整 URL 才能通过，则停止并重新设计。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: quick local CI 增加 webhook outbox redelivery smoke。
- Source-of-truth updates: API 文档、roadmap、scripts/tests AGENTS、task index。
- Contract/catalog/schema impact: `CalculationJob` webhook outbox 行为增加 redelivery baseline，由 regression test 保护。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02, TP-02.03 | 实现 redelivery baseline。 |
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

- 回滚代码：移除 redelivery 查询、resolver、事件、smoke、local-ci 和 test 变更。
- 回滚文档：移除 0058 任务包、INDEX 行和文档更新。
- DB schema 不新增强制列；回滚无需迁移现有业务数据。
