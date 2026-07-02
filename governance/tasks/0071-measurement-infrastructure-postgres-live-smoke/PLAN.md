# Planning Summary

0071 是 0070 Postgres adapter 之后的最小生产基础设施切片：不再停留在 SQL dry-run，而是用真实或一次性 Postgres 执行 migration/job/outbox/config 路径；同时保持 ship gate blocked，避免把 smoke 证据夸大成 production readiness。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0071 不能标记 Done。

| Phase | Gate | Result |
| --- | --- | --- |
| SPEC | Scope excludes production multi-replica/exactly-once/public webhook/Vault | Done |
| PLAN | Task tree and evidence path fixed | Done |
| BUILD | live smoke script, production gate and contract sync implemented | Done |
| TEST | focused tests, real disposable Postgres smoke, secret scan and quick local-ci | Done |
| REVIEW | docs/contract wording checked for overclaiming | Done |
| SHIP | commit/push and remote CI evidence | Pending until git delivery step |

# Simplest Path

Reuse the existing `PostgresReportJobStore` and build one smoke harness around it. Do not create a second migration framework, queue system, database abstraction or provider layer.

# Split Strategy

- TP-01 protects boundary and avoids accidental scope creep.
- TP-02 implements the minimal live evidence path.
- TP-03 proves behavior through tests and actual disposable Postgres.
- TP-04 synchronizes documentation and closes validation.

# Execution Waves

| Wave | Leaves | Parallel |
| --- | --- | --- |
| 1 | TP-01.01 | No |
| 2 | TP-02.01, TP-02.02, TP-02.03 | Partially |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Partially |
| 4 | TP-04.01, TP-04.02 | No |

# Dependency Graph

```text
TP-01.01
  -> TP-02.01
  -> TP-02.02
  -> TP-02.03
  -> TP-03.01
  -> TP-03.02
  -> TP-03.03
  -> TP-04.01
  -> TP-04.02
```

# Runtime Workflow Contract

- Live smoke command: `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-job-store-live-smoke.sh --output-json <path>`.
- Local missing-env preflight: `bash scripts/postgres-job-store-live-smoke.sh --allow-missing --output-json <path>`.
- Runtime backend gate: `bash scripts/runtime-backend-gate.sh --output-json <path>`.
- Production readiness: `FATE_REPORT_JOB_STORE=postgres` requires both DSN env and passed live smoke evidence JSON.

# Next Executable Leaves

- None for local implementation. Submit, push and refresh remote CI evidence after closeout validation.

# Rollback Protocol

- Revert 0071 scripts, tests, contract/doc wording and local-ci wiring as a single scoped rollback.
- Keep 0070 Postgres adapter and dry-run baseline intact unless the live smoke reveals an adapter bug.
- Do not use destructive git history rewrites.

# Future-Optimal Target End State

The final durable runtime should have an external source of truth, migration evidence, production multi-replica worker lease, crash/restart smoke, duplicate claim negative tests, public webhook live delivery and external secret lifecycle. This task is a proof point toward that end state, not a substitute for it.

# Rejected Short-Term Patches

- Do not mark `FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED=1` as sufficient without evidence JSON.
- Do not add an allowlist exception for smoke secrets when variable naming can avoid scanner false positives.
- Do not make local-ci require a real DSN.
- Do not change default backend to Postgres.
