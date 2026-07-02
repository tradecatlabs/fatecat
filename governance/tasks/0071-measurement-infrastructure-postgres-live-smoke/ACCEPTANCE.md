# Acceptance

## Task-Level Acceptance

- `scripts/postgres-job-store-live-smoke.sh` can run against a real or disposable Postgres DSN from `FATE_REPORT_JOB_DATABASE_URL`.
- The passed live smoke proves schema initialization, job roundtrip, event idempotency, task payload persistence, webhook outbox claim/release, encrypted delivery config and cleanup.
- `--allow-missing` produces a machine-readable `blocked` artifact when DSN or optional dependency is unavailable.
- `production-readiness.sh` rejects `FATE_REPORT_JOB_STORE=postgres` unless a passed live smoke evidence JSON is supplied; it cannot accept a boolean flag alone.
- Runtime backend contract uses `implementationStatus=live_smoke_baseline`, while `backend.postgres.status` remains `planned` and blocked claims remain explicit.
- local-ci quick includes the live-smoke preflight artifact and still passes without real external DSN.
- Secret scan finds zero tracked first-party findings.

# Task Package Acceptance

| Task Package | Acceptance |
| --- | --- |
| TP-01.01 | 0070 boundary and runtime backend contract are documented. |
| TP-02.01 | live smoke script validates schema/job/event/outbox/config against Postgres. |
| TP-02.02 | production-readiness requires passed live smoke evidence JSON. |
| TP-02.03 | runtime backend contract records `live_smoke_baseline` without production overclaim. |
| TP-03.01 | regression tests cover missing DSN, privacy, scripts and contract wiring. |
| TP-03.02 | `--allow-missing` blocked artifact works for local-ci without DSN. |
| TP-03.03 | disposable Postgres smoke passes and evidence is redacted. |
| TP-04.01 | docs and AGENTS are synchronized. |
| TP-04.02 | local-ci, validators, git delivery and remote CI evidence are completed or explicitly pending. |

## Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/postgres-job-store-live-smoke.py ...` and `bash -n ...` | pass |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0071.json` | status passed |
| Missing DSN preflight | `bash scripts/postgres-job-store-live-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-job-store-live-smoke-0071-blocked.json` | status blocked, exit 0 |
| Real Postgres live smoke | Docker Postgres + `FATE_REPORT_JOB_DATABASE_URL=... bash scripts/postgres-job-store-live-smoke.sh --output-json /tmp/fatecat-postgres-job-store-live-smoke-0071.json` | status passed, 16 checks |
| Production readiness positive | env with passed evidence JSON | pass |
| Production readiness negative | env without evidence JSON | fail as expected |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_postgres_job_store_live_smoke.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | 32 passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0071.json` | findingCount 0 |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0071` | passed, 193 focused regression tests |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | pass |

# Review Gate

- No raw DSN, username, password, webhook URL, webhook secret or report body appears in tracked code outputs or evidence JSON.
- Documentation and contract wording explicitly keep production multi-replica worker, exactly-once, public webhook live and external Vault/KMS as pending.
- Existing default memory/sqlite behavior remains compatible.
- New tests cover missing DSN, no sensitive output, script registration, contract state and production-readiness gate wiring.

# Runtime Verification Gate

- Live smoke output must include `kind=fatecat.postgres_job_store_live_smoke`.
- Passed live smoke must include `status=passed`, `checks=16` and `shipGate.status=blocked`.
- Missing DSN preflight must include `status=blocked` and must not return a false pass.
- Production readiness must reject Postgres mode without `FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE`.
- local-ci summary must expose `artifacts.postgresJobStoreLiveSmoke`.

# Ship Readiness

- Local implementation and quick local-ci are ready for commit.
- Remote CI evidence must be refreshed after commit and push.
- This task does not make FateCat 100% infrastructure complete; it closes one durable runtime proof point.

# Global Acceptance Standards

- Evidence is command-backed, not inferred.
- External production validation remains labeled as pending unless actual credentials/platforms are used.
- All task package files contain no unresolved placeholders.

# Anti-Goals

- 不声明 production ready。
- 不声明生产多副本 worker lease、exactly-once、公网 webhook live 或外部 Vault/KMS 完成。
- 不保存或输出真实 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 不改变默认 memory/sqlite backend。
