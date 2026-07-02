# Task-Level Acceptance

- `bash scripts/postgres-worker-lease-smoke.sh --allow-missing` 在无 DSN/psycopg 时写出 `status=blocked` summary 且 exit 0。
- 使用真实或一次性 Postgres DSN 运行 `bash scripts/postgres-worker-lease-smoke.sh` 时写出 `status=passed` summary。
- Passed summary 必须包含 `kind=fatecat.postgres_worker_lease_smoke`、`duplicateClaimRaceCount`、`duplicateClaimWinnerCount=1`、`loserReleaseBlocked=true`、`leaseExpiryReclaim=true`、`shipGate.status=blocked`。
- Summary 不得包含 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- RuntimeBackend contract 从 `live_smoke_baseline` 提升为 `worker_lease_smoke_baseline`，但 `backend.postgres.status` 仍保持 `planned`。
- local-ci quick 包含 worker lease allow-missing preflight 和 focused regression。

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/postgres-worker-lease-smoke.py` and `bash -n scripts/postgres-worker-lease-smoke.sh scripts/local-ci.sh` | pass |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0072.json` | status passed |
| Missing DSN preflight | `bash scripts/postgres-worker-lease-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-worker-lease-smoke-0072-blocked.json` | status blocked, exit 0 |
| Real Postgres live smoke | Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-worker-lease-smoke.sh --race-count 6 --output-json /tmp/fatecat-postgres-worker-lease-smoke-0072.json` | status passed, 16 checks |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_postgres_worker_lease_smoke.py tests/regression/test_postgres_job_store_live_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | pass |
| Ruff | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0072.json` | findingCount 0 |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0072` | pass |
| Task docs | `validate_task_docs.py --phase closeout` | pass |

# Review Gate

- No raw DSN, username, password, callback URL, webhook secret, lease owner, report body or user input appears in summary or docs examples.
- Documentation and contract wording explicitly keep job execution worker lease, exactly-once, public webhook live and external Vault/KMS as pending.
- Default `memory` / `sqlite` behavior remains compatible.
- `backend.postgres.status` remains `planned`.

# Runtime Verification Gate

- Blocked preflight is acceptable for local-ci only; it cannot be used as real external evidence.
- Real smoke must use actual Postgres and passed summary.
- `duplicate_claim_negative_*` checks must all pass.
- `shipGate.status` remains `blocked`.

# Ship Readiness

- Local implementation and quick local-ci are ready for commit after validations.
- Remote CI evidence must be refreshed after commit and push.
- This task does not make FateCat 100% infrastructure complete; it closes one durable runtime proof point.

# Task Package Acceptance

## TP-01 边界与证据目标

Verify: 0071 closeout、runtime backend contract 和 roadmap 已确认。

Gate: 本任务只证明 Postgres webhook outbox lease negative path。

- [x] 0071 后缺口和 non-claims 已写入任务包。

## TP-02 Worker lease negative smoke 实现

Verify: `scripts/postgres-worker-lease-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: duplicate claim、错误 owner release、lease expiry reclaim 均被脚本验证。

- [x] Worker lease smoke 实现完成。

## TP-03 Contract、文档和测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=worker_lease_smoke_baseline`。

- [x] Contract、文档和测试接线完成。

## TP-04 验证、closeout 和交付

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan 和 task validator。

Gate: 本地验证通过，远端 CI 后续由 Git 交付刷新。

- [x] 验证和 closeout 完成。

# Anti-Goals

- 不声明 production ready。
- 不声明 job execution worker lease、exactly-once、公网 webhook live 或外部 Vault/KMS 完成。
- 不保存或输出真实 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 不改变默认 memory/sqlite backend。
