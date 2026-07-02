# Planning Summary

本任务继续 `MI-NEXT-03`，把 SQLite report job restart recovery 从“隐藏在 API contract tests 里的行为”推进到“可独立运行、可进 local-ci、可输出机器可读证据的 smoke”。它证明的是 restart-safe failure 和事件可审计，不是跨进程继续执行。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 SQLite restart recovery smoke 解释为 external backend、分布式 worker 或任务 resume execution。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 `MI-100.02.03 restart recovery smoke` 本地 baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | restart recovery smoke 和 local-ci 接入完成 | Done |
| TEST | focused tests 覆盖 smoke summary 与 CLI | Done |
| REVIEW | 确认隐私安全、语义不夸大和 quick CI 稳定 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

新增一个自包含 smoke：创建临时 SQLite store，提交 blocking job，等待 running，重建 manager，断言旧 job failed 且存在 `job.recovered_failed`；随后释放原 blocking task。这个路径复用现有 runtime，不引入新抽象。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 smoke 和 local-ci。
- TP-03：补测试和文档。
- TP-04：验证与交付。

# Future-Optimal Contract

- target end state: durable runtime 具备可恢复、可重试、可回放、可审计的任务控制面。
- real constraints: 当前只有 memory/sqlite 单进程 baseline。
- inertia constraints: 不能因为 unit test 已有而缺少独立 release smoke。
- kill list: 把 failed recovery 写成 resume、输出用户输入、依赖真实 `.env`、使用全局 DB。
- proof point: 独立脚本输出 `status=passed`，包含 recovered_failed event 和 privacy boundary。
- falsifier: smoke 无法稳定复现 running job rebuild，或输出泄露姓名/地区/Markdown。
- migration slice: 先将 restart-safe failure 证据化；后续 external backend 决策再实现继续执行。

# Ponytail Contract

- existence check: restart recovery smoke 是 durable runtime 发布门禁的必要对象。
- selected ladder rung: 复用现有 manager/store，新建小脚本。
- skipped scope: 不新增 external backend，不改状态机。
- ceiling / upgrade path: 需要任务继续执行时，升级 external backend/worker lease。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: script + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、local-ci、git status。
- stop conditions: smoke flaky、隐私泄露、文档将本地 baseline 夸大为 production resume。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 不需要。
- Process update: quick local CI 增加 restart recovery smoke。
- Source-of-truth updates: API 文档、roadmap、scripts AGENTS、task index。
- Contract/catalog/schema impact: 不新增 JSON schema；smoke summary 由 regression test 保护。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02 | 实现 smoke 与 local-ci 接入。 |
| 3 | TP-03.01, TP-03.02 | 测试和文档。 |
| 4 | TP-04.01 | 验收和交付。 |

# Next Executable Leaves

None. 0055 closeout completed.

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol

- 回滚代码：移除 restart recovery smoke 脚本、local-ci step 和 regression test。
- 回滚文档：移除 0055 任务包、INDEX 行和文档更新。
- 无 DB schema 变更。
