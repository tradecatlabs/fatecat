# Task Status

- Overall Status: `Done`

# Next Executable Leaves

- None. 本地 0071 切片完成；提交推送和远端 CI 属于 git delivery 收口步骤。

# Task Package Status Table

| ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 0070 adapter baseline、runtime backend contract 和本地运行条件已复核。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | `git status --short --branch`、`rg` 和 0070 closeout 证明当前切片只新增 live evidence path。 | - | - |
| TP-02 | ROOT | 1 | TP-01.01 | No | Done | live smoke script、production gate 和 contract sync 已完成。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.01 | No | Done | `scripts/postgres-job-store-live-smoke.py` 与 `.sh` 已新增；real Docker Postgres smoke 通过。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | `production-readiness.sh` 正负门禁已验证；缺 evidence JSON 会 fail-fast。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | runtime backend gate 通过，checks=92；contract 使用 `live_smoke_baseline`。 | - | - |
| TP-03 | ROOT | 1 | TP-02.03 | No | Done | 回归测试、blocked preflight 和 real live smoke 已完成。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | focused regression `32 passed in 0.27s`。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | `/tmp/fatecat-postgres-job-store-live-smoke-0071-blocked.json` status=blocked，reason=missing env。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | `/tmp/fatecat-postgres-job-store-live-smoke-0071.json` status=passed，checks=16，shipGate=blocked。 | - | - |
| TP-04 | ROOT | 1 | TP-03.03 | No | Done | 文档同步、quick local-ci 和任务 closeout 文档已完成。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | AGENTS、operations docs、roadmap、contract 和 task index 口径已同步。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0071` 通过，focused regression `193 passed in 82.83s`；任务 validators 待本文件落盘后执行。 | - | - |

# Blockers

- 无本地实现阻断。
- 生产级分布式 worker lease、exactly-once、公网 webhook live、外部 Vault/KMS、生产密钥生命周期仍是后续任务。
- 远端 CI evidence 需要本任务提交推送后刷新。

# Runtime State

- Current branch: `main`
- Current task: `0071-measurement-infrastructure-postgres-live-smoke`
- Local evidence directory: `/tmp/fatecat-local-ci-0071`
- Git delivery evidence: pending until commit/push.

# Remaining Risks

- Disposable Postgres live smoke 不等于生产 HA Postgres、连接池、备份恢复、迁移回滚或权限模型已验证。
- Outbox claim/release smoke 不等于生产多副本 worker lease 或 exactly-once。
- Encrypted delivery config smoke 使用本地 Fernet codec，不等于外部 Vault/KMS 或 secret lifecycle 已完成。
- Public webhook live delivery 仍需真实接收端和签名验证日志。

# Recent Evidence

| Evidence | Result |
| --- | --- |
| `.venv/bin/python -m pip install 'psycopg[binary]>=3.1.0'` | installed psycopg 3.3.4 in local venv for disposable Postgres smoke |
| `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0071.json` | passed; checks=92; externalCandidate=backend.postgres |
| `bash scripts/postgres-job-store-live-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-job-store-live-smoke-0071-blocked.json` | passed as blocked preflight; missing `FATE_REPORT_JOB_DATABASE_URL` |
| Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-job-store-live-smoke.sh --output-json /tmp/fatecat-postgres-job-store-live-smoke-0071.json` | passed; checks=16; `shipGate.status=blocked`; forbidden marker check passed |
| `.venv/bin/python -m pytest -q tests/regression/test_postgres_job_store_live_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | passed; `32 passed in 0.27s` |
| `.venv/bin/python -m ruff check ...` | passed |
| `.venv/bin/python -m ruff format --check ...` | passed |
| `.venv/bin/python -m py_compile ...` and `bash -n ...` | passed |
| `bash scripts/check-source-hygiene.sh` | passed |
| `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0071.json` | passed; findingCount=0 |
| `env ... FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE=/tmp/fatecat-postgres-job-store-live-smoke-0071.json bash scripts/production-readiness.sh --skip-bootstrap` | passed static readiness; external API/Bot live skipped |
| `env ... FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED=1 bash scripts/production-readiness.sh --skip-bootstrap` | failed as expected without evidence JSON |
| `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0071` | passed; focused regression `193 passed in 82.83s` |
