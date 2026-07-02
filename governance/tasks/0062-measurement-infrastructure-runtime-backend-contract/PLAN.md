# Planning Summary

本任务把 0061 规划中的 `durable runtime external backend contract` 落成可验证基线：先定义 RuntimeBackend 资源，再用本地 gate 防止 contract 漂移和生产口径夸大。正确终态是外部 backend 可由后续 adapter 任务实现，而不是本轮把 Postgres/Temporal 名字写进文档后假装完成。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0062 不能标记 Done，也不能声明 external backend 已生产。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确只做 RuntimeBackend contract baseline | Done |
| PLAN | 任务树、边界、验证计划落盘 | Done |
| BUILD | schema、registry、gate、tests、local-ci、docs 接线完成 | Done |
| TEST | focused tests、gate CLI、validators、ruff/secret scan、quick local CI 通过 | Done |
| REVIEW | 不夸大 external backend、SQLite、Redis、Temporal 能力 | Done |
| SHIP | commit/push 后可进入下一切片 | Done |

# Future-Optimal Contract

- target end state: CalculationJob durable runtime 可在 external backend 上恢复、协调、审计和回滚。
- real constraints: 当前只具备 memory/sqlite 本地 baseline，缺真实 external database/service。
- inertia constraints: SQLite local lease 不能替代生产分布式 worker lease。
- kill list: Postgres planned 写成 available、Redis queue 写成 source of truth、Temporal 写成当前 job store adapter、registry 泄露 DSN。
- proof point: gate summary 证明 5 个 backend 都被登记，Postgres 是 planned candidate，Redis 是 not_selected auxiliary only。
- falsifier: `runtime-backend-gate` 允许 Postgres implemented/production_ready 或 Redis source_of_truth。
- migration slice: 后续 0063/implementation task 可在 contract 基础上新增 Postgres adapter 和迁移 smoke。

# Simplest Path

复用 `contracts/fate/delivery/` 资源目录，不新增新顶层目录；用一个 JSON registry、一个 schema、一个 Python gate 和一个 shell wrapper 完成 contract baseline。测试复用现有 importlib 脚本测试模式。

# Split Strategy

- TP-01：确认缺口和落点。
- TP-02：实现资源契约。
- TP-03：实现 gate、测试和 local-ci。
- TP-04：文档、验证、收口。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核上下文。 |
| 2 | TP-02.01, TP-02.02 | 新增 contract baseline。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate、测试、local-ci。 |
| 4 | TP-04.01, TP-04.02 | 文档与验收。 |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`secret-scan`、task validators、git |
| forbidden actions | 不切换分支、不连接真实 DB/service、不读取真实 `.env`、不输出 secret |
| expected output | RuntimeBackend registry/schema/gate/test/docs/task closeout |
| required evidence | gate CLI、pytest、task validators、ruff、secret scan、quick local CI |
| stop condition | 需要真实 external DB/service 才能验证时，标记外部连通验证待执行，不阻塞 contract baseline |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无；0062 已完成，下一切片应从 external backend adapter 或 async contract 任务开始。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 删除 `contracts/fate/delivery/runtime-backends.json` 与 schema。
- 从 delivery registry/resource schema/local-ci/tests/scripts/docs/AGENTS/roadmap 移除 RuntimeBackend 引用。
- 删除 0062 任务包和 INDEX 行。
