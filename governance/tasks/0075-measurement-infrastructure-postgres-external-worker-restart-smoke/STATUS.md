# Task Status

- Overall Status: `Done`

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无；等待 commit/push 后刷新远端 CI evidence。 |

# Task Package Status Table

| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | `git status --short --branch`、runtime backend contract、0074 closeout 与 roadmap 已审查；0074 index drift 已修正。 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | `ReportJobManager._run_job()` 执行前 claim job execution lease；terminal/cancel/failure path release 当前 owner lease。 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 新增 `scripts/postgres-external-worker-restart-smoke.py`/`.sh`；real Docker Postgres smoke passed。 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | RuntimeBackend contract/schema/gate、local-ci、operations docs、roadmap、AGENTS 与 regression tests 已接线。 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | Done | syntax、blocked preflight、real Postgres smoke、focused tests、ruff、local-ci quick、task docs validator 与 tasks tree validator 通过。 | - | - |

# Blockers

- 无 0075 当前实现 blocker。
- 全局剩余：公网 webhook live、外部 Vault/KMS、生产密钥生命周期、heartbeat/polling worker、长期多副本运行、exactly-once、真实生产部署仍待后续。

# Runtime State

- Current branch: `main`
- Current task: `0075-measurement-infrastructure-postgres-external-worker-restart-smoke`
- Blocked preflight artifact: `/tmp/fatecat-postgres-external-worker-restart-smoke-0075-blocked.json`
- Real smoke artifact: `/tmp/fatecat-postgres-external-worker-restart-smoke-0075.json`
- Local CI artifact directory: `/tmp/fatecat-local-ci-0075`

# Recent Evidence

| Evidence | Result |
| --- | --- |
| `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate-0075.json` | passed；backends=5；checks=95 |
| `bash scripts/postgres-external-worker-restart-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-external-worker-restart-smoke-0075-blocked.json` | status=blocked；exit 0；缺 DSN 时不伪造 live |
| Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-external-worker-restart-smoke.sh --output-json /tmp/fatecat-postgres-external-worker-restart-smoke-0075.json` | passed；checks=11；executionCount=1；persistedStatus=succeeded；shipGate=blocked |
| `.venv/bin/python -m pytest -q tests/regression/test_postgres_external_worker_restart_smoke.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_postgres_worker_lease_smoke.py tests/regression/test_postgres_job_worker_lease_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | 42 passed |
| `.venv/bin/python -m ruff check .` / `.venv/bin/python -m ruff format --check .` | passed |
| `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0075` | passed；205 focused regression passed；evidence dir `/tmp/fatecat-local-ci-0075` |
| `validate_task_docs.py --task-dir governance/tasks/0075-measurement-infrastructure-postgres-external-worker-restart-smoke --phase closeout` | ok=true |
| `validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | ok=true；task_total=75；valid=75 |
