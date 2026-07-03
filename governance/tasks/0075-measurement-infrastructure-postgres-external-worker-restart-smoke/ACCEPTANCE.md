# Task-Level Acceptance

- `ReportJobManager._run_job()` must claim job execution lease before running a task.
- Claim failure must prevent task execution.
- Terminal completion must release the job execution lease for the active owner.
- `bash scripts/postgres-external-worker-restart-smoke.sh --allow-missing` must write `status=blocked` summary and exit 0 when DSN/psycopg is missing.
- With a real or disposable Postgres DSN, `bash scripts/postgres-external-worker-restart-smoke.sh` must write `status=passed`.
- Passed summary must include `kind=fatecat.postgres_external_worker_restart_smoke`、`executionCount=1`、`persistedStatus=succeeded`、`recoveredFromExpiredLease=true`、`duplicateExecutionBlocked=true`、`shipGate.status=blocked`。
- Summary must not contain DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- RuntimeBackend contract advances to `external_worker_restart_smoke_baseline`, but `backend.postgres.status` remains `planned`。
- local-ci quick includes external worker restart allow-missing preflight and focused regression。

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/postgres-external-worker-restart-smoke.py domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` and `bash -n scripts/postgres-external-worker-restart-smoke.sh scripts/local-ci.sh` | pass |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0075.json` | status passed |
| Missing DSN preflight | `bash scripts/postgres-external-worker-restart-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-external-worker-restart-smoke-0075-blocked.json` | status blocked, exit 0 |
| Real Postgres smoke | Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-external-worker-restart-smoke.sh --output-json /tmp/fatecat-postgres-external-worker-restart-smoke-0075.json` | status passed |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_postgres_external_worker_restart_smoke.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_postgres_job_worker_lease_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | pass |
| Ruff | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0075` | pass |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | pass |

# Review Gate

- `backend.postgres.status=planned`。
- docs/contract/summary 明确不证明 exactly-once、公网 webhook live、外部 Vault/KMS、production ready。
- 默认 memory/sqlite 行为兼容。
- Manager 执行路径必须 claim-before-execute。
- Summary 不出现 raw DSN、用户名、密码、callback URL、secret、报告正文或用户输入。

# Runtime Verification Gate

- Blocked preflight 只用于本地缺外部环境时的巡检，不是 live evidence。
- Real smoke 必须使用真实或一次性 Postgres。
- `executionCount` 必须等于 1。
- `persistedStatus` 必须为 `succeeded`。
- `shipGate.status` 必须保持 `blocked`。

# Ship Readiness

- 本地实现和 quick local-ci 通过后可提交。
- 远端 CI 需要 commit/push 后刷新。
- 本任务只关闭 expired lease external worker restart smoke，不使 FateCat 达到 100% 基础设施。

# Task Package Acceptance

## TP-01 PRECHECK：边界、数据流和执行语义审查

Verify: current repo facts、runtime backend contract、0074 closeout 和 roadmap 已确认。

Gate: 明确 crash/restart external backend worker 与 exactly-once、webhook live、Vault/KMS 的边界。

- [x] precheck evidence 已写入 `CONTEXT.md`。

## TP-02 IMPLEMENT：ReportJobManager job execution lease 接线

Verify: `_run_job()` 执行前 claim，terminal 后 release，memory/sqlite 兼容。

Gate: claim 失败不执行 task；现有本地 recovery smoke 不回归。

- [x] Manager claim-before-execute 完成。

## TP-03 IMPLEMENT：Postgres external worker restart smoke

Verify: `scripts/postgres-external-worker-restart-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON。

- [x] Smoke 实现完成。

## TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=external_worker_restart_smoke_baseline`。

- [x] Contract、文档和测试接线完成。

## TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、task validators、remote CI。

Gate: 本地和远端证据齐全；仍不声明 production ready。

- [x] 验证和 closeout 完成。

# Anti-Goals

- 不声明 production ready。
- 不声明 exactly-once、公网 webhook live 或外部 Vault/KMS 完成。
- 不保存或输出真实 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 不实现后台 polling/heartbeat/renew。
