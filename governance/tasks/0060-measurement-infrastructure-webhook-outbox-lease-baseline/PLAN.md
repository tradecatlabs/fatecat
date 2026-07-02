# Planning Summary

本任务把 webhook outbox redelivery 从“所有 manager 都会扫描 failed/pending record”推进到“必须先 claim lease 才能重投”。这减少本地重复副作用，是 external backend 之前的最小可验证 worker coordination baseline。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把 SQLite lease baseline 解释为 external backend、生产级分布式 worker lease、多副本锁、真实公网 webhook live smoke 或 exactly-once。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确只覆盖 SQLite 本地 lease baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | Store claim/release、SQLite schema、manager redelivery 接入完成 | Done |
| TEST | focused tests 覆盖 claim 冲突、release 和重投一次 | Done |
| REVIEW | 确认不暴露 lease 内部字段、不夸大生产能力 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Future-Optimal Contract

- target end state: durable runtime 使用 external backend 和生产 worker lease 支持可恢复、可审计、可协调的异步任务和 webhook 投递。
- real constraints: 当前只有 memory/sqlite 单机 baseline，不能伪造 external backend。
- inertia constraints: SQLite lease 不能成为“生产分布式 worker lease”概念替代品。
- kill list: 双发 webhook、无 claim 重投、公开 lease owner、claim 失败仍 dispatch、claim 文档夸大。
- proof point: 同一 SQLite failed outbox 只能被一个 lease owner claim；另一个 owner claim 失败；release 后可重新 claim；manager redelivery 只 dispatch 一次。
- falsifier: 两个 owner 同时可 claim、claim 失败仍投递、lease 字段进入 API payload、quick CI flaky。
- migration slice: 本地 SQLite lease contract 稳定后，后续可替换为 external backend worker lease。

# Simplest Path

复用现有 `ReportJobWebhookOutboxRecord` 与 SQLite outbox 表，新增内部 lease columns 和 store claim/release 方法。Manager redelivery 只在 claim 成功后继续读取 resolver/encrypted config 并 dispatch；无 claim 则跳过，不改变公开 API outbox payload。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 lease schema、claim/release 和 manager 接入。
- TP-03：补 smoke、测试和 quick CI。
- TP-04：文档、验证与交付。

# Ponytail Contract

- existence check: webhook outbox 是副作用出口；没有 claim/release 会在多 manager 重建时产生重复投递风险。
- selected ladder rung: 复用 SQLite atomic update，不新增外部依赖。
- skipped scope: 不引入 Redis/Postgres/Temporal/Celery，不做生产分布式 lease。
- ceiling / upgrade path: 真实生产升级 external backend + durable worker lease + idempotent receiver。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要新增依赖。
- Process update: quick local CI 增加 webhook outbox lease smoke。
- Source-of-truth updates: API 文档、roadmap、scripts/tests/delivery AGENTS、task index。
- Contract/catalog/schema impact: `CalculationJobWebhookOutbox` 公开 payload 不增加 lease 字段；内部 SQLite schema 增加 lease 列。
- Documentation exemption reason: 无。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + smoke + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、secret scan、local-ci、git status。
- stop conditions: 需要真实外部 backend 或真实 secret 才能通过，则停止并重新设计。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02 | 实现 lease baseline。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Smoke、测试和 CI。 |
| 4 | TP-04.01, TP-04.02 | 文档、验收和交付。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-01.01 | 读取 roadmap、0058/0059、webhook/report job 源码和 smoke。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚代码：移除 claim/release 接口、SQLite lease columns 使用、manager claim/release、smoke、local-ci 和 tests。
- DB schema 新增列为 optional；回滚不影响现有 outbox record 读写。
