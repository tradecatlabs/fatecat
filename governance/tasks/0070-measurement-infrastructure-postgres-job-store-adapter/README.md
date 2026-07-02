# Task Overview

- Task ID: `0070`
- Slug: `measurement-infrastructure-postgres-job-store-adapter`
- Objective: `执行 MI-100.01 Durable Runtime 的 Postgres job store adapter 切片：在不伪造真实外部数据库 live 的前提下，为 CalculationJob/ReportJobStore 新增可选 Postgres adapter、Postgres DDL/migration dry-run、webhook outbox transactional claim/release 语义、配置入口和回归门禁；真实 Postgres 连通、生产多副本 worker、外部 Vault/KMS 与公网 webhook live 仍保留为外部验证待执行。`
- Status: `Done`

## In Scope

- 复核 `ReportJobStore`、`SQLiteReportJobStore`、`runtime-backends.json` 和生产配置门禁，确认 Postgres 适配点。
- 新增可选 `PostgresReportJobStore`，实现与 SQLite store 对齐的 job/event/outbox/config persistence 方法。
- 新增 Postgres DDL/migration SQL 与 dry-run smoke，验证 SQL、隐私边界和 claim/release 语义，不需要真实 DSN。
- `main.py` 支持 `FATE_REPORT_JOB_STORE=postgres`，缺少 `FATE_REPORT_JOB_DATABASE_URL` 或缺少 `psycopg` 时 fail-fast，不静默 fallback。
- 更新 runtime backend contract、production readiness、local-ci、测试、AGENTS、roadmap 和 0070 任务文档。

## Out of Scope

- 不连接真实 Postgres，不声明 external backend live verified。
- 不实现生产多副本 worker 调度器、跨副本 crash recovery、exactly-once 或公网 webhook live。
- 不引入真实 DSN、用户名、密码、token、证书、私钥、外部 Vault/KMS 凭证或生产日志。
- 不重写 ReportJobManager 状态机，不把 Postgres 适配层改成另一套任务系统。

## Task Package Tree

```text
TP-01 Context and contract
  TP-01.01 复核 ReportJobStore 接口、SQLite 行为和 runtime backend contract
TP-02 Postgres store implementation
  TP-02.01 新增 Postgres DDL 与 SQL helper
  TP-02.02 新增 PostgresReportJobStore 可选适配层
  TP-02.03 接入 main.py 配置和 production-readiness fail-fast
TP-03 Gates and tests
  TP-03.01 新增 Postgres dry-run smoke 脚本
  TP-03.02 新增 regression tests 覆盖 SQL、隐私和配置接线
  TP-03.03 接入 local-ci 与 runtime backend contract
TP-04 Documentation and closeout
  TP-04.01 同步 AGENTS、roadmap 和任务索引
  TP-04.02 运行 focused validation、quick local-ci、任务 validators 并收口
```

## Requirement Alignment

- 对齐 MI-100.01.02：从 contract baseline 推进到 Postgres ReportJobStore adapter baseline。
- 对齐胶水原则：优先使用 Postgres 事务和条件更新做 claim/release，自研代码只做 `ReportJobStore` 适配。
- 对齐不可伪造证据口径：dry-run 只证明 SQL/contract 可检查，不证明真实外部数据库 live。

## Task Package Overview

| Task Package ID | Parent | Priority | Type | Leaf | Depends On | Objective |
| --- | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | P0 | analysis | Yes | - | 明确 Postgres adapter 应贴合现有 store 接口和 0062 contract。 |
| TP-02.01 | TP-02 | P0 | build | Yes | TP-01.01 | 新增 Postgres schema/migration SQL 与 dry-run helper。 |
| TP-02.02 | TP-02 | P0 | build | Yes | TP-02.01 | 新增 `PostgresReportJobStore`，实现持久化和 outbox claim/release。 |
| TP-02.03 | TP-02 | P0 | build | Yes | TP-02.02 | 接入 `FATE_REPORT_JOB_STORE=postgres` 配置并 fail-fast。 |
| TP-03.01 | TP-03 | P0 | test | Yes | TP-02.03 | 新增 Postgres store dry-run smoke。 |
| TP-03.02 | TP-03 | P0 | test | Yes | TP-03.01 | 新增回归测试覆盖 SQL/contract/config。 |
| TP-03.03 | TP-03 | P0 | integration | Yes | TP-03.02 | 接入 local-ci 与 runtime backend contract 状态。 |
| TP-04.01 | TP-04 | P0 | docs | Yes | TP-03.03 | 同步目录说明、roadmap 和任务文档。 |
| TP-04.02 | TP-04 | P0 | closeout | Yes | TP-04.01 | 运行验证、任务校验、版本交付和远端 CI。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
