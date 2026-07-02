# Task-Level Acceptance

- `ReportJobStore` 暴露 job execution lease 的最小接口；`PostgresReportJobStore` 使用数据库原子条件更新实现。
- `bash scripts/postgres-job-worker-lease-smoke.sh --allow-missing` 在无 DSN/psycopg 时写出 `status=blocked` summary 且 exit 0。
- 使用真实或一次性 Postgres DSN 运行 `bash scripts/postgres-job-worker-lease-smoke.sh` 时写出 `status=passed` summary。
- Passed summary 必须包含 `kind=fatecat.postgres_job_worker_lease_smoke`、`duplicateClaimRaceCount`、`duplicateClaimWinnerCount=1`、`wrongOwnerReleaseBlocked=true`、`leaseExpiryReclaim=true`、`terminalJobUnclaimable=true`、`shipGate.status=blocked`。
- Summary 不得包含 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- RuntimeBackend contract 从 `worker_lease_smoke_baseline` 推进到 `job_worker_lease_smoke_baseline`，但 `backend.postgres.status` 仍保持 `planned`。
- local-ci quick 包含 job worker lease allow-missing preflight 和 focused regression。

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/postgres-job-worker-lease-smoke.py domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` and `bash -n scripts/postgres-job-worker-lease-smoke.sh scripts/local-ci.sh` | pass |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0074.json` | status passed |
| Missing DSN preflight | `bash scripts/postgres-job-worker-lease-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-job-worker-lease-smoke-0074-blocked.json` | status blocked, exit 0 |
| Real Postgres smoke | Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-job-worker-lease-smoke.sh --race-count 6 --output-json /tmp/fatecat-postgres-job-worker-lease-smoke-0074.json` | status passed |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_postgres_job_worker_lease_smoke.py tests/regression/test_postgres_worker_lease_smoke.py tests/regression/test_postgres_job_store_live_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | pass |
| Ruff | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0074.json` | findingCount 0 |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0074` | pass |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | pass |

# Review Gate

- `backend.postgres.status=planned`。
- docs/contract/summary 明确不证明 exactly-once、公网 webhook live、外部 Vault/KMS、production ready。
- 默认 memory/sqlite 行为兼容。
- release 只允许 owner 匹配。
- terminal job 不可被 claim。
- Summary 不出现 raw DSN、用户名、密码、callback URL、secret、报告正文或用户输入。

# Runtime Verification Gate

- Blocked preflight 只用于本地缺外部环境时的巡检，不是 live evidence。
- Real smoke 必须使用真实或一次性 Postgres。
- `duplicate_claim_negative_*` checks 必须全部通过。
- `shipGate.status` 必须保持 `blocked`。

# Ship Readiness

- 本地实现和 quick local-ci 通过后可提交。
- 远端 CI 需要 commit/push 后刷新。
- 本任务只关闭 job lease primitive，不使 FateCat 达到 100% 基础设施。

# Task Package Acceptance

## TP-01 PRECHECK：边界、数据流和并发语义审查

Verify: current repo facts、runtime backend contract、0072 closeout 和 roadmap 已确认。

Gate: 明确 job execution lease 与 outbox lease、exactly-once、生产 ready 的边界。

- [x] precheck evidence 已写入 `CONTEXT.md`。

## TP-02 IMPLEMENT：Postgres job execution lease 接口与实现

Verify: `report_jobs.py` 新接口和 Postgres 实现通过语法与 focused tests。

Gate: duplicate claim、wrong owner release、expiry reclaim、terminal unclaimable 均可被脚本验证。

- [x] Store 接口和 Postgres 实现完成。

## TP-03 IMPLEMENT：Job worker lease smoke 脚本与 wrapper

Verify: `scripts/postgres-job-worker-lease-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON。

- [x] Smoke 实现完成。

## TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=job_worker_lease_smoke_baseline`。

- [x] Contract、文档和测试接线完成。

## TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan、task validators、remote CI。

Gate: 本地和远端证据齐全；仍不声明 production ready。

- [x] 验证和 closeout 完成。

# Anti-Goals

- 不声明 production ready。
- 不声明 exactly-once、公网 webhook live 或外部 Vault/KMS 完成。
- 不保存或输出真实 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 不改变默认 memory/sqlite backend。
