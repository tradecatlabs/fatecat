# Planning Summary

本任务继续 `MI-NEXT-03`，把 report job 的重建语义从“所有 active callable 丢失后失败”推进到“已声明 `task_payload` 且存在 `task_factory` 的生产报告任务可重新入队执行”。这是 external backend 之前的最小可验证迁移台阶。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 replayable SQLite baseline 解释为 external backend、分布式 worker 或 exactly-once。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖本地可重建任务 baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | task_payload、factory、requeue 和 API submit 接入完成 | Done |
| TEST | focused tests 覆盖 replayable success 和 non-replayable failure | Done |
| REVIEW | 确认隐私安全、兼容 0055/0056 和 quick CI 稳定 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

新增可选 `task_payload` 字段并持久化到 SQLite。`ReportJobManager` 接受 `task_factories` 映射；重建 queued/running 任务时，如果存在 payload 和 factory，则把任务恢复为 queued、追加 `job.recovered_requeued` 事件并放回本地队列；否则继续标 failed。Web/Markdown submit 路径传入可序列化 payload 和对应 factory。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 replayable task baseline。
- TP-03：补 smoke、测试和 quick CI。
- TP-04：文档、验证与交付。

# Future-Optimal Contract

- target end state: durable runtime 可基于外部 backend 恢复、重试、续跑和审计长任务。
- real constraints: 当前只有 memory/sqlite 单机 baseline，生产报告任务输入结构化可重建。
- inertia constraints: 不围绕 Python callable 做序列化假象，不把 active job 全部失败当作最终状态。
- kill list: pickle callable、持久 secret、保存 webhook URL、声称分布式/Exactly-once 已完成。
- proof point: SQLite queued/running + payload + factory 在新 manager 中重新入队并成功完成。
- falsifier: 无 payload 任务被错误重跑、payload 泄露 secret/正文、quick CI flaky。
- migration slice: 先把执行意图资源化；后续 external backend/lease/worker adapter 复用该契约。

# Ponytail Contract

- existence check: replayable task payload 是从本地 SQLite baseline 走向 external backend 的必要对象。
- selected ladder rung: 复用现有 manager/store，只新增最小字段、factory map 和 smoke。
- skipped scope: 不引入外部队列，不新增加密 secret vault，不实现 worker lease。
- ceiling / upgrade path: 需要多副本生产时升级为 external backend + lease + encrypted callback config。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: code diff + smoke + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、secret scan、local-ci、git status。
- stop conditions: task payload 必须保存 secret 或完整报告正文才能通过，则停止并重新设计。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: quick local CI 增加 replayable recovery smoke。
- Source-of-truth updates: API 文档、roadmap、scripts/tests AGENTS、task index。
- Contract/catalog/schema impact: `CalculationJob` 行为增加 replayable recovery 语义，由 regression test 保护。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02, TP-02.03 | 实现 replayable baseline。 |
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

- 回滚代码：移除 task_payload/factory/requeue/API submit/smoke/local-ci/test 变更。
- 回滚文档：移除 0057 任务包、INDEX 行和文档更新。
- DB schema 只新增列；回滚不需要迁移现有业务数据。
