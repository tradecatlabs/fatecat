# Planning Summary

本任务继续 `MI-NEXT-03`，把 webhook redelivery 从“需要运行时 resolver 提供配置”推进到“本地 SQLite 可保存加密 callback config 并恢复投递”。这是外部 Vault/KMS、external backend 和生产 worker lease 之前的最小安全迁移台阶。

# Lifecycle Gates

禁止跳过任何 gate；如果某 gate 失败，不能把任务标为 Done。不得把本地 encrypted config vault baseline 解释为外部 Vault/KMS、external backend、分布式 worker、真实公网 webhook live smoke 或 exactly-once。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖本地 SQLite encrypted delivery config vault baseline | Done |
| PLAN | 任务包和边界落盘 | Done |
| BUILD | Fernet codec、SQLite vault、rotation 和 manager fallback 完成 | Done |
| TEST | focused tests 覆盖密文、重投、删除和 rotation | Done |
| REVIEW | 确认隐私安全、依赖合理、兼容 0058 和 quick CI 稳定 | Done |
| SHIP | validators、local-ci、commit/push 完成 | Done |

# Simplest Path

复用现有 `ReportJobWebhookOutboxRecord`、`ReportJobSnapshot`、SQLite store 和 webhook dispatcher。新增一个薄 `webhook_config_store.py` 承载 Fernet codec 和解密后运行时 config；SQLite store 增加 encrypted config 表与 save/load/delete/rotate 方法；Manager 在 outbox 创建时保存密文，redelivery 时优先使用外部 resolver，否则使用 store 中 encrypted config。

# Split Strategy

- TP-01：复核缺口。
- TP-02：实现 encrypted config vault baseline。
- TP-03：补 smoke、测试和 quick CI。
- TP-04：文档、验证与交付。

# Future-Optimal Contract

- target end state: durable runtime 支持外部 secret backend、任务恢复、webhook 持久投递、event history、worker lease 和审计。
- real constraints: 当前只有 memory/sqlite 单机 baseline，不能读取真实 secret backend。
- inertia constraints: 不把明文 persistence、runtime resolver 或本地 SQLite vault 当最终生产 secret 管理。
- kill list: 自研密码学、明文 secret、完整 URL 输出、claim external Vault/KMS。
- proof point: SQLite failed outbox record 的 encrypted config 可在新 manager 中解密并自动重投成功，成功后删除，rotation 可验证。
- falsifier: 原始 SQLite 含明文、rotation 失效、无 resolver 时 redelivery 不工作、quick CI flaky。
- migration slice: 先稳定 encrypted config contract；后续可把 store 后端替换成 KMS/Vault 或 external backend。

# Ponytail Contract

- existence check: 持久 callback secret 加密/轮换是从本地 redelivery 走向生产事件交付的必要对象。
- selected ladder rung: 复用成熟 `cryptography` / Fernet，项目内只做 codec/store/manager glue。
- skipped scope: 不引入外部 Vault/KMS，不做云 secret manager，不做多副本 lease。
- ceiling / upgrade path: 需要真实生产时升级为外部 KMS/Vault + external backend + lease。
- minimal runnable check: smoke CLI + focused pytest + local-ci。

# Runtime Workflow Contract

- allowed tools: `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`validate_task_docs.py`、`validate_tasks_tree.py`、`git`、`pip install`。
- forbidden actions: 不切分支、不 rebase、不删除用户文件、不读取真实 `.env`、不输出 secret。
- expected output schema: dependency diff + code diff + smoke + wrapper + docs diff + task docs + validation evidence + commit/push。
- evidence required: smoke CLI、focused tests、validators、ruff、secret scan、local-ci、git status。
- stop conditions: 需要提交真实 key 或明文 secret 才能通过，则停止并重新设计。

# Document-Driven Contract

- Operating model update: 不需要。
- Toolchain model update: 新增 runtime dependency，需要同步 `pyproject.toml`、requirements 和 lock。
- Process update: quick local CI 增加 webhook encrypted config vault smoke。
- Source-of-truth updates: API 文档、roadmap、scripts/tests AGENTS、task index。
- Contract/catalog/schema impact: `CalculationJob` webhook redelivery 行为增加 encrypted config fallback，由 regression test 保护。
- Documentation exemption reason: 无。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核当前状态。 |
| 2 | TP-02.01, TP-02.02, TP-02.03 | 实现 encrypted config vault baseline。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Smoke、测试和 CI。 |
| 4 | TP-04.01, TP-04.02 | 文档、验收和交付。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-01.01 | 读取 roadmap、0056/0058、webhook/report job 源码、依赖和测试。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚代码：移除 encrypted config codec、SQLite config 表方法、manager fallback、smoke、local-ci 和 test 变更。
- 回滚依赖：移除 `cryptography` dependency 与 lock 行。
- 回滚文档：移除 0059 任务包、INDEX 行和文档更新。
- DB schema 新增表为 optional；回滚不影响已有 report job/outbox 表。
