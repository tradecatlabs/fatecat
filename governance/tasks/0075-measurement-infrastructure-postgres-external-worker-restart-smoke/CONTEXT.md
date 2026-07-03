# Repo Evidence

- `contracts/fate/delivery/runtime-backends.json` 当前 `backend.postgres.implementationStatus=job_worker_lease_smoke_baseline`，`status=planned`，`nextTask` 指向 crash/restart external backend worker 或外部 webhook/Vault live evidence。
- 任务创建时，`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 0.9 推荐执行顺序第 1 项是 Crash/restart external backend worker；closeout 后已刷新为 public webhook / external secret / worker hardening 后续项。
- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` 已有 `ReportJobStore.claim_job_for_execution()` 和 `PostgresReportJobStore.claim_job_for_execution()`，但 `ReportJobManager._run_job()` 当前仍在本地锁内直接把 queued job 改成 running，没有执行前 claim。
- `ReportJobManager._load_persisted_jobs()` 已能基于 `task_payload` 和 `task_factories` 将 active job 重新入队；这是 external worker restart smoke 的可复用入口。
- `scripts/postgres-job-worker-lease-smoke.py` 已证明 job lease primitive：duplicate claim 只能一个成功、wrong owner release 被拦截、lease expiry 后可重 claim、terminal job 不可 claim。
- `governance/tasks/INDEX.md` 当前 `0074` 仍显示 `In Progress`，与 0074 task docs / commit / remote CI 事实不一致，需要修正为 `Done`。

> Closeout note: 上述 Repo Evidence 是 0075 创建时的 precheck 事实。0075 closeout 后，`backend.postgres.implementationStatus=external_worker_restart_smoke_baseline`，roadmap 已把 crash/restart external worker 从下一步移除，`ReportJobManager._run_job()` 已执行前 claim，`0074` INDEX 状态已修正为 `Done`。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 高风险异步执行路径 | 先接最小 lease claim，不改 submit API、不引入后台 DB polling。 |
| 兼容 memory/sqlite | base store claim 保守返回 queued/running job；sqlite 行为保持本地单副本 baseline。 |
| Postgres 外部证据 | `--allow-missing` 只能 blocked，真实 smoke 必须使用一次性或真实 Postgres。 |
| 不泄露 DSN/secret | summary 只写 hash、check 名、状态和非敏感计数。 |
| 不夸大生产 | backend.postgres 仍保持 `planned`，summary `shipGate.status=blocked`。 |

# Change Boundary

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/postgres-external-worker-restart-smoke.py`
- `scripts/postgres-external-worker-restart-smoke.sh`
- `scripts/local-ci.sh`
- `scripts/runtime-backend-gate.py`
- `contracts/fate/delivery/runtime-backends.json`
- `contracts/fate/delivery/registry.json`
- `contracts/fate/delivery/schemas/runtime-backend.schema.json`
- `tests/regression/test_postgres_external_worker_restart_smoke.py`
- Existing focused regression tests for runtime backend and postgres worker lease
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `domains/experience-delivery/services/fatecat-delivery/AGENTS.md`
- `contracts/fate/delivery/AGENTS.md`
- `scripts/AGENTS.md`
- `governance/tasks/0075-*`
- `governance/tasks/INDEX.md`

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| `_run_job` claim 接线导致 memory/sqlite 行为回归 | 报告任务不执行 | base store claim 保持原本单进程语义，focused tests 覆盖现有 smoke。 |
| claim 失败后本地 queue 不再重试 | 过早启动的 worker 可能错过未过期 lease | 本任务只证明 crash 后 lease expired restart；heartbeat/polling 作为后续升级，不声明 production ready。 |
| 两个 manager 都执行 task | 外部 backend worker 不可用 | Postgres smoke 必须证明 execution count 为 1。 |
| 终态文档夸大 | 审计误判 | contract/docs/summary 保留 exactly-once、webhook live、Vault/KMS、production ready blocked claims。 |
| smoke 泄露连接信息 | 安全事故 | `_safe_summary` 拦截敏感模式和 forbidden runtime values。 |

# Assumptions and Falsification

- Assumption: `ReportJobManager._run_job()` 执行前调用 store claim 后，两个 manager 对同一 Postgres job 只有一个能执行。
- Falsifier: real Postgres external worker restart smoke 中 execution count 大于 1。
- Assumption: stale running job 的过期 lease 可被 restarted manager 重新 claim 并执行。
- Falsifier: lease expiry 后 persisted job 没有进入 `succeeded`。
- Assumption: 不改变 memory/sqlite 默认行为。
- Falsifier: 现有 report job restart/replayable recovery smoke 或 focused regression 失败。

# Engineering Change Safety

| Field | Value |
| --- | --- |
| risk_level | high |
| affected_flows | CalculationJob / ReportJobManager async execution、Postgres backend recovery smoke |
| external_contracts | `contracts/fate/delivery/runtime-backends.json`、runtime backend gate |
| data_flow | persisted `_ReportJob` with `task_payload` -> manager rebuild -> queue -> lease claim -> task execution -> persisted result |
| control_flow | multiple managers may load same active job; only successful lease claimer may execute |
| state_changes | queued/running job claim updates lease and status; terminal result persists; lease cleared on terminal when owner matches |
| side_effects | DB writes only; no external webhook live call |
| concurrency_idempotency | two manager restart smoke, duplicate execution count check |
| consistency_model | Postgres row-level conditional update in one transaction |
| failure_recovery | stale running job with expired lease can be re-executed from payload |
| performance_cost | one claim update per job execution; no polling loop in this slice |
| observability | job events + smoke summary JSON + runtime backend gate limits |
| rollout | optional Postgres-only capability; default backend unchanged |
| rollback | remove `_run_job` claim接线、新 smoke 和 contract status bump |
| required_tests | focused regression, blocked preflight, real Docker Postgres smoke, quick local-ci |

# Future-Optimal Contract

- Target end state: `CalculationJob` durable runtime supports external backend worker coordination, crash recovery, retry/outbox, event history, webhook callback, secret lifecycle, observability and audit evidence.
- Real constraints: 当前可用一次性 Docker Postgres 证明 DB-backed worker restart；公网 webhook、外部 Vault/KMS、真实多副本部署和 exactly-once 不在本环境内。
- Inertia constraints: 现有 manager 本地队列不是 external worker source of truth；不能因为改动小就跳过 store lease。
- Wrong concept / wrong boundary: job lease primitive 不是 crash/restart worker；crash/restart smoke 仍不是 exactly-once。
- Kill list: manager 执行路径绕过 claim、docs-only crash recovery、allow-missing 伪通过、production ready 夸大。
- Proof point: real Postgres smoke 显示 expired leased running job 被两个 restarted managers 中一个执行成功，execution count 为 1。
- Falsifier: 两个 manager 都执行、job 未成功恢复、summary 泄露敏感信息、backend.postgres 被标成 production ready。
- Migration slice: 本轮只把 manager 执行路径接入 lease 并证明 expired lease restart；后续再做 heartbeat/polling、webhook live、Vault/KMS。
- Rejected short-term patches: 不用 sleep/进程锁模拟分布式执行；不把 0074 primitive 改名冒充 crash recovery。
- Future-optimal review owner: `auto-review` with future-optimal-drift and reliability/concurrency lenses。

# Ponytail Contract

- Existence check: 0.9 路线图明确 0074 后下一步是 crash/restart external backend worker；这是 external backend production 的必要证据。
- Selected ladder rung: project-native capability using existing `ReportJobManager` + mature Postgres conditional update; no new workflow framework yet。
- Skipped scope: Temporal/Redis worker、heartbeat/renew、DB polling daemon、exactly-once、公网 webhook、Vault/KMS、production deployment。
- Ceiling / upgrade path: 只能证明 expired lease restart；后续需要 heartbeat、polling、at-least-once/idempotency、public webhook 和 external secret provider。
- Do-not-simplify: claim-before-execute、owner-matched release、terminal non-claim、sensitive summary protection、blocked preflight 不可删除。
- Minimal runnable check: focused tests + disposable Postgres external worker restart smoke + local-ci quick。
- Complexity review owner: `auto-review` with ponytail-complexity and feature-change-safety。

# Document-Driven Contract

| Field | Status |
| --- | --- |
| Operating model update | not needed: 项目定位不变。 |
| Toolchain model update | updated: 新增 Postgres external worker restart smoke 和 local-ci artifact。 |
| Process update | not needed: 仍沿用 runtime backend gate / local-ci / task closeout。 |
| Source-of-truth updates | updated: runtime backend contract、roadmap、operations docs、任务包。 |
| Local README/AGENTS impact | updated: scripts、delivery service、delivery contract AGENTS。 |
| Contract/catalog/schema impact | updated: runtime backend registry/schema/gate。 |
| ADR/Gate/module-context impact | updated: runtime backend gate。 |
| Documentation exemption reason | none: 本任务改变 runtime behavior 和 toolchain，必须同步文档。 |
| Validation evidence | focused tests、real Postgres smoke、local-ci、validators。 |

# Critical Ambiguities

- 本任务证明 expired lease 后 external backend worker restart，不证明 lease 未过期时的自动延迟重试。
- 本任务证明 at-most-one execution in smoke，不声明 exactly-once。
- Public webhook live 和外部 Vault/KMS 仍是外部连通验证待执行。

# Debug Evidence Contract

- 调试模式: Optional
- 失败时必须记录：失败 check、summary 路径、Postgres 版本/启动方式、是否发生重复执行、是否泄露敏感值。
- 不允许用 allow-missing blocked artifact 替代 real Postgres smoke。

# Task Package Context Map

| Artifact | Purpose |
| --- | --- |
| `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | Manager execution path and store lease implementation |
| `scripts/postgres-external-worker-restart-smoke.py` | Real/disposable Postgres external worker restart smoke |
| `contracts/fate/delivery/runtime-backends.json` | RuntimeBackend production boundary |
| `tests/regression/test_postgres_external_worker_restart_smoke.py` | Script/contract/docs regression |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | Operator command and non-claim docs |
