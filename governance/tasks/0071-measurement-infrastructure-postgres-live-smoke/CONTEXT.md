# Context

## Repo Evidence

| Evidence | Observation |
| --- | --- |
| `git status --short --branch` | task start was `## main...origin/main`; current worktree contains 0071 scoped changes. |
| 0070 closeout | `PostgresReportJobStore` adapter and dry-run baseline existed before this task. |
| `contracts/fate/delivery/runtime-backends.json` | Postgres is external candidate, but remains `status=planned`; 0071 changes only `implementationStatus` to `live_smoke_baseline`. |
| `scripts/local-ci.sh` | quick profile is the local aggregate gate and now records a blocked live-smoke preflight artifact when no DSN is available. |
| `/tmp/fatecat-postgres-job-store-live-smoke-0071.json` | disposable Docker Postgres smoke passed with 16 checks and `shipGate.status=blocked`. |
| `/tmp/fatecat-local-ci-0071/summary.json` | quick local-ci passed with 193 focused regression tests. |

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| DSN secrecy | Read only from env; never print or store raw DSN. |
| Evidence privacy | Hash target database/host/schema and check for forbidden markers before writing summary. |
| Mature reuse | Reuse existing `PostgresReportJobStore`, `FernetWebhookConfigCodec`, FastAPI/job models and Docker Postgres for live smoke. |
| Production truth | Do not mark production ready, exactly-once, public webhook live or Vault/KMS complete. |
| Default compatibility | Keep memory/sqlite default behavior unchanged. |
| Auditability | Add tests and docs so contract, scripts, local-ci and production gate agree. |

## Change Boundary

- Allowed: `scripts/`, `tests/regression/`, `contracts/fate/delivery/`, related AGENTS, operations docs, roadmap and this task package.
- Not touched: provider algorithms, report rendering, API route semantics outside runtime backend readiness, production deployment credentials, `.env`, external secret stores.

## Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Raw DSN or webhook secret leak | Security blocker | `_safe_summary` forbidden value check, secret scan, regression tests. |
| One-time DB smoke overclaimed as production | Audit blocker | `shipGate.status=blocked`, blocked claims in contract, production-readiness evidence gate. |
| Missing local Postgres causes false failure | Developer friction | `--allow-missing` returns `blocked` summary and exit 0 for local-ci preflight. |
| `psycopg` optional dependency breaks default mode | Runtime regression | Tests keep missing-dependency blocked path explicit; default backend unchanged. |
| Contract drift | Audit confusion | Runtime backend gate, schema tests, AGENTS/docs sync. |

# Assumptions and Falsification

- Assumption: 0070 `PostgresReportJobStore` is the right extension point. Falsifier: real smoke cannot create schema or roundtrip job/outbox/config through the existing store.
- Assumption: one-time schema on disposable Postgres is enough for migration/job live smoke baseline. Falsifier: production readiness would require multi-replica worker lease or public webhook live evidence, which this task explicitly does not claim.
- Assumption: local-ci should not require a real DSN. Falsifier: release gate for production would require explicit evidence JSON, handled by `production-readiness.sh`.

## Critical Ambiguities

- Real production Postgres connection, pooling, HA, backup and migration ownership remain outside this task.
- Public webhook receiver and external Vault/KMS ownership remain outside this task.
- Multi-replica worker lease semantics and duplicate claim negative tests remain future production runtime work.

# Debug Evidence Contract

- 调试模式: Optional
- This is a planned infrastructure slice, not a bugfix. Failures encountered during implementation were resolved through focused regression and smoke reruns; evidence is recorded in STATUS.md.

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0070 closeout, current git status and runtime backend contract. |
| TP-02.01 | Existing `PostgresReportJobStore`, `FernetWebhookConfigCodec`, live smoke script path. |
| TP-02.02 | `scripts/production-readiness.sh` Postgres branch and evidence JSON policy. |
| TP-02.03 | `contracts/fate/delivery/runtime-backends.json`, schema, delivery registry and runtime backend gate. |
| TP-03.01 | Regression tests for live smoke, privacy and contract wiring. |
| TP-03.02 | Missing env/optional dependency blocked artifact behavior. |
| TP-03.03 | Disposable Docker Postgres live smoke evidence. |
| TP-04.01 | AGENTS, operations docs, roadmap and task index. |
| TP-04.02 | Local CI, task validators and git delivery evidence. |
