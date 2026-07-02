# Acceptance

## Task-Level Acceptance

- `PostgresReportJobStore` exists and implements the `ReportJobStore` persistence methods used by `ReportJobManager`.
- Postgres DDL covers `report_jobs`, `report_job_events`, `report_job_webhook_outbox`, and `report_job_webhook_delivery_config`.
- Postgres webhook outbox claim/release uses conditional update with `lease_owner` and `lease_expires_at`.
- `main.py` supports `FATE_REPORT_JOB_STORE=postgres` and requires `FATE_REPORT_JOB_DATABASE_URL`.
- Missing `psycopg` or missing DSN fails explicitly when postgres is selected; memory/sqlite behavior remains unchanged.
- A local dry-run smoke validates SQL/contract/privacy without connecting to a real database.
- Runtime backend contract advances Postgres from pure `contract_baseline` to adapter baseline without claiming live production readiness.
- `scripts/local-ci.sh --profile quick` runs the Postgres dry-run gate.

## Task Package Acceptance

| Task Package | Acceptance |
| --- | --- |
| TP-01.01 | Existing store interface and runtime backend gap are documented. |
| TP-02.01 | Postgres DDL/helper contains required tables, indexes, upsert and claim/release SQL. |
| TP-02.02 | `PostgresReportJobStore` implements job/event/outbox/config store methods. |
| TP-02.03 | Config entry is explicit and fail-fast; no silent fallback. |
| TP-03.01 | Dry-run smoke writes machine-readable JSON and contains no DSN/secret values. |
| TP-03.02 | Regression tests cover adapter import, SQL shape, missing dependency/DSN, and contract status. |
| TP-03.03 | local-ci and runtime backend gate include the new dry-run evidence. |
| TP-04.01 | AGENTS and roadmap describe the adapter baseline and pending live verification. |
| TP-04.02 | focused validation, quick local-ci, task validators, commit/push and remote CI are completed or pending evidence is explicitly marked. |

## Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Python compile | `.venv/bin/python -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/postgres-job-store-dry-run.py` | passed |
| Shell syntax | `bash -n scripts/postgres-job-store-dry-run.sh scripts/local-ci.sh scripts/production-readiness.sh` | passed |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0070.json` | passed |
| Postgres dry-run | `bash scripts/postgres-job-store-dry-run.sh --output-json /tmp/fatecat-postgres-job-store-dry-run-0070.json` | passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_runtime_backend_gate.py tests/regression/test_postgres_job_store_adapter.py` | passed |
| Ruff | `.venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/postgres-job-store-dry-run.py tests/regression/test_postgres_job_store_adapter.py` | passed |
| Format check | `.venv/bin/python -m ruff format --check domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/postgres-job-store-dry-run.py tests/regression/test_postgres_job_store_adapter.py` | passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0070.json` | passed |
| Task validators | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | passed |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0070` | passed |

# Review Gate

- BLOCK if Postgres backend can be selected without explicit DSN.
- BLOCK if missing `psycopg` silently falls back to memory/sqlite.
- BLOCK if dry-run output contains a DSN, password, token, private key, callback URL or real report body.
- BLOCK if contract says `external_live_verified` or `production_ready` without real database evidence.
- BLOCK if claim/release SQL lacks owner and expiry conditions.

# Runtime Verification Gate

- Dry-run output must include `kind=fatecat.postgres_job_store_dry_run`.
- Dry-run must report `status=passed` only when required tables/indexes/claim SQL/privacy checks pass.
- Dry-run must report `shipGate.status=blocked` until `FATE_REPORT_JOB_DATABASE_URL` live smoke is executed against a real database.
- local-ci summary must expose `artifacts.postgresJobStoreDryRun`.

# Ship Readiness

- Local focused validation: passed.
- quick local-ci: passed at `/tmp/fatecat-local-ci-0070`.
- Commit/push: pending until this task package is committed.
- Remote CI current commit: pending after push; cannot be recorded inside the commit before that run exists.

# Anti-Goals

- 不得伪造真实 Postgres live。
- 不得保存或输出真实 DSN。
- 不得把 adapter baseline 写成 production multi-replica durable runtime 完成。
