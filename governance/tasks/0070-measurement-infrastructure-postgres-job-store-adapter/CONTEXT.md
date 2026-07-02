# Context

## Current Facts

- `ReportJobStore` 是 report job 持久化的唯一接口，当前有 `InMemoryReportJobStore` 和 `SQLiteReportJobStore`。
- `contracts/fate/delivery/runtime-backends.json` 已选择 `backend.postgres` 作为 first external adapter path，但状态仍是 `planned` / `contract_baseline`。
- `main.py` 当前只允许 `FATE_REPORT_JOB_STORE=memory|sqlite`，其他值 fail-fast。
- `scripts/production-readiness.sh` 当前只允许 `memory|sqlite`，多副本时拒绝本地 store。
- 现有 SQLite store 已覆盖 job state、event history、idempotency、task payload、webhook outbox、encrypted webhook config 和本地 outbox lease。

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不伪造外部 live | 本轮只做 adapter + SQL dry-run；真实 `FATE_REPORT_JOB_DATABASE_URL` 连通验证仍标记外部连通验证待执行。 |
| 不泄露 DSN | contract、日志、dry-run、tests 和 docs 只写 env var 名，不输出值。 |
| 复用现有接口 | `PostgresReportJobStore` 必须实现 `ReportJobStore` 方法，不改 `ReportJobManager` 业务状态机。 |
| 可选依赖 | `psycopg` 只在选择 postgres store 时导入；缺依赖时报明确错误。 |
| 生产准入 | `production-readiness` 可识别 postgres，但没有 live verification 时仍不允许多副本宣称 ready。 |
| Change boundary | 只改 report job store、配置门禁、contracts/scripts/tests/docs/task。 |
| Debug Evidence Contract | Optional；若 adapter/smoke/CI 失败，再补最小复现、根因和回归证据。 |

## Change Boundary

- 允许修改：`domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`、`main.py`、`contracts/fate/delivery/runtime-backends.json`、runtime backend scripts/tests、`scripts/local-ci.sh`、`scripts/production-readiness.sh`、相关 `AGENTS.md`、roadmap 和 0070 任务文档。
- 禁止修改：八字/紫微算法、报告结构、真实外部凭证、公网服务配置、用户数据样例、外部 Bot/live evidence。

## Repo Evidence

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `contracts/fate/delivery/runtime-backends.json`
- `contracts/fate/delivery/schemas/runtime-backend.schema.json`
- `scripts/runtime-backend-gate.py`
- `scripts/production-readiness.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_runtime_backend_gate.py`
- `tests/regression/test_api_contracts.py`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

## Critical Ambiguities

- `Postgres adapter implemented` 不等于 `external database live verified`。
- `workerLease=transactional_outbox_claim` 只能说明 outbox record claim/release 语义，不等于全局 job worker exactly-once。
- 缺少 `psycopg` 或 DSN 时，选择 `FATE_REPORT_JOB_STORE=postgres` 必须失败，而不是回退到 SQLite 或 memory。

## Debug Evidence Contract

- 调试模式: Optional
- 本任务是 feature baseline，不是已复现 bug；若出现失败，必须记录失败命令、根因和回归验证。

## Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Postgres 配置被误认为生产 ready | contract 和 dry-run 输出继续保留 external live pending。 |
| DSN/密码泄露进文档或 artifact | secret scan、dry-run pattern 和测试禁止 sensitive assignment/value。 |
| adapter 与 SQLite 行为漂移 | 回归测试复用 store 方法语义并检查 SQL upsert/claim/release。 |
| 引入硬依赖导致本地 quick CI 失败 | psycopg optional import，只在 postgres store 实例化时需要。 |

## Assumptions and Falsification

- 假设：当前最小有效切片是 Postgres store 代码与 migration dry-run，不需要真实 DB。
- 证伪条件：`FATE_REPORT_JOB_STORE=postgres` 静默 fallback、dry-run 输出真实 DSN、runtime backend contract 写成 live verified、或 Postgres claim SQL 缺少 owner/expiry 条件。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | `ReportJobStore`、`SQLiteReportJobStore`、runtime backend contract。 |
| TP-02.01 | Postgres DDL、index、upsert、claim/release SQL。 |
| TP-02.02 | `PostgresReportJobStore` optional adapter。 |
| TP-02.03 | `main.py`、`production-readiness.sh` 配置入口。 |
| TP-03.01 | Postgres dry-run smoke 脚本。 |
| TP-03.02 | regression tests。 |
| TP-03.03 | local-ci、runtime backend contract/gate。 |
| TP-04.01 | AGENTS、roadmap、任务文档。 |
| TP-04.02 | focused validation、quick local-ci、GitHub Actions。 |
