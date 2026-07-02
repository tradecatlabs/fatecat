# Task Status

- Overall Status: `Done`

# Next Executable Leaves

- None. 本地 0070 切片完成；真实外部 Postgres live 和多副本 worker 仍是后续任务。

# Task Package Status Table

| ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 现有 store 接口、SQLite 行为、runtime backend contract 和配置门禁已复核。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | `sed` / `rg` / `json.tool` 已确认 Postgres 当前仍是 planned contract baseline。 | - | - |
| TP-02 | ROOT | 1 | TP-01.01 | No | Done | Postgres SQL/helper、adapter 和配置门禁已完成。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.01 | No | Done | `POSTGRES_REPORT_JOB_SCHEMA_SQL` 覆盖 job/event/outbox/config 表、索引、upsert 和 claim SQL。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | `PostgresReportJobStore` 实现 `ReportJobStore` 方法，`psycopg` 仅在 postgres store 被选择时需要。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | `main.py` 支持 `FATE_REPORT_JOB_STORE=postgres`；`production-readiness.sh` 对缺 DSN/缺 live verification fail-fast。 | - | - |
| TP-03 | ROOT | 1 | TP-02.03 | No | Done | Dry-run、回归测试、contract gate 和 local-ci 接线已完成。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | `bash scripts/postgres-job-store-dry-run.sh --output-json /tmp/fatecat-postgres-job-store-dry-run-0070.json` 通过，`shipGate.status=blocked`。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | focused regression 覆盖 SQL、optional dependency、隐私和配置 fail-fast。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | `scripts/local-ci.sh --profile quick` 生成 `artifacts.postgresJobStoreDryRun`。 | - | - |
| TP-04 | ROOT | 1 | TP-03.03 | No | Done | AGENTS、roadmap、operations docs、任务索引和任务文档已同步。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | 文档明确 adapter baseline，不宣称 external live 或 production ready。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | focused validation、secret scan、production-readiness negative checks 和 quick local-ci 已通过；Git push/remote CI 待本次提交后刷新。 | - | - |

# Blockers

- 无本地实现阻断。
- 真实 Postgres live、生产多副本 worker、外部 Vault/KMS 和公网 webhook live 属于后续外部验证待执行。

# Runtime State

- Current branch: `main`
- Current task: `0070-measurement-infrastructure-postgres-job-store-adapter`
- Git delivery evidence: pending until this task package is committed and pushed.

# Remaining Risks

- 本任务不能证明真实外部 Postgres 连通。
- 本任务不能证明生产多副本 worker lease、exactly-once、跨副本 crash recovery 或公网 webhook live。
- `psycopg` optional dependency 是否安装只影响 postgres store 运行路径，不能破坏 memory/sqlite quick CI。

# Recent Evidence

| Evidence | Result |
| --- | --- |
| `git status --short --branch` | clean at task start |
| `git log -3 --oneline` | latest `8cdf4e3` |
| `sed` report_jobs/main/runtime-backends | Postgres remains planned contract baseline |
| `rg` report job store usage | single store extension point confirmed |
| `.venv/bin/python -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/postgres-job-store-dry-run.py` | passed |
| `bash -n scripts/postgres-job-store-dry-run.sh scripts/local-ci.sh scripts/production-readiness.sh` | passed |
| `bash scripts/postgres-job-store-dry-run.sh --output-json /tmp/fatecat-postgres-job-store-dry-run-0070.json` | passed; summary `status=passed`, `checks=22`, `shipGate.status=blocked` |
| `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0070.json` | passed; summary `checks=91` |
| `.venv/bin/python -m pytest -q tests/regression/test_runtime_backend_gate.py tests/regression/test_postgres_job_store_adapter.py tests/regression/test_capability_protocol.py` | passed; `32 passed in 0.60s` |
| `.venv/bin/python -m ruff check ...` | passed |
| `.venv/bin/python -m ruff format --check ...` | passed after formatting `scripts/runtime-backend-gate.py` |
| `bash scripts/check-source-hygiene.sh` | passed |
| `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0070.json` | passed; `findingCount=0` |
| `env ... bash scripts/production-readiness.sh --skip-bootstrap` | default static readiness passed |
| `env ... FATE_REPORT_JOB_STORE=postgres bash scripts/production-readiness.sh --skip-bootstrap` | failed as expected without DSN |
| `env ... FATE_REPORT_JOB_STORE=postgres FATE_REPORT_JOB_DATABASE_URL='__redacted_external_postgres_dsn__' bash scripts/production-readiness.sh --skip-bootstrap` | failed as expected without `FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED=1` |
| `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0070` | passed; focused regression `189 passed in 105.64s` |
