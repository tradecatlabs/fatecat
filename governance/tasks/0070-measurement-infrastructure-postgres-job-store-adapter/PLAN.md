# Planning Summary

本任务把 0062 的 Postgres external backend contract baseline 推进到可执行 adapter baseline。正确终态是 Postgres 成为 `ReportJobStore` 的可选外部实现，并能用数据库事务和条件更新承载 job state、event history、idempotency、webhook outbox 和 outbox lease；本轮不做真实数据库 live，因此 ship gate 必须保持 external live blocked。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0070 不能标记 Done。

| Gate | Evidence |
| --- | --- |
| SPEC | 现有 store 接口、SQLite 行为和 runtime backend contract 已复核。 |
| PLAN | 本任务文档定义范围、非目标、任务树、验证命令和阻断语义。 |
| BUILD | Postgres adapter、SQL helper、dry-run smoke、config gate、contract 和 docs 完成。 |
| TEST | py_compile、bash -n、dry-run、focused pytest、ruff、secret scan、quick local-ci 通过。 |
| REVIEW | 检查无 DSN 泄露、无 live 伪声明、无 silent fallback、claim SQL 有 owner/expiry。 |
| SHIP | 提交推送后记录远端 Acceptance 当前 commit 结果。 |

# Simplest Path

- 不引入 SQLAlchemy 或新任务系统；只实现 `ReportJobStore` 适配层。
- 不要求本地安装/启动 Postgres；dry-run 校验 SQL 形状和 privacy。
- `psycopg` 作为 optional dependency，只在 postgres store 被选择时需要。
- 优先保持 SQLite 行为不变，减少 ReportJobManager 改动面。

# Split Strategy

1. 先冻结接口和 contract 事实。
2. 再新增 Postgres SQL/adapter。
3. 再接入配置、dry-run 和 tests。
4. 最后同步文档、roadmap、任务包和版本证据。

# Execution Waves

| Wave | Tasks |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01、TP-02.02、TP-02.03 |
| 3 | TP-03.01、TP-03.02、TP-03.03 |
| 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract

- 本地 dry-run：`bash scripts/postgres-job-store-dry-run.sh --output-json <path>`
- 可选真实 live：后续任务用真实 `FATE_REPORT_JOB_DATABASE_URL` 运行 Postgres migration/job smoke；本任务不执行。
- 应用配置：`FATE_REPORT_JOB_STORE=postgres` + `FATE_REPORT_JOB_DATABASE_URL`。
- 缺 DSN 或缺 `psycopg`：启动失败并给出明确错误。

# Next Executable Leaves

- None. 本地实现、文档和门禁切片已完成；真实 Postgres live、多副本 worker 和公网 webhook live 进入后续任务。

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚 Postgres adapter、dry-run 脚本、contract/local-ci 接线和文档。
- 保留 SQLite/memory 现有路径。
- 不执行 `git reset --hard` 或破坏性命令。

## Target End State

FateCat 具备 Postgres ReportJobStore adapter baseline：生产操作者可以显式选择 postgres store，系统不会静默 fallback；审计人员可以复核 SQL、contract 和 dry-run artifact；真实外部数据库 live 仍需后续凭证与环境。

## Future-Optimal Framing

- 正确终态：durable runtime 的 source of truth 是外部事务型 backend 或 workflow engine，而不是单机 SQLite。
- 本轮切片：先实现 Postgres store adapter baseline，为后续真实 DB smoke 和多副本 worker lease 提供接口落点。
- Proof point：dry-run 和 tests 证明 adapter/SQL/config 可用且不泄露 DSN。
- Falsifier：contract 或 dry-run 说 external live complete，但没有真实 DB 证据。

## Ponytail Existence Check

- `PostgresReportJobStore` 应该存在：Postgres 是已选 first external adapter path。
- SQL dry-run 应该存在：真实 DB 缺失时仍需审计 SQL/隐私/claim 结构。
- regression tests 应该存在：防止 silent fallback、DSN 泄露和 contract overclaim 回潮。
- 不新增独立任务系统：当前最小充分对象是 `ReportJobStore` adapter。
