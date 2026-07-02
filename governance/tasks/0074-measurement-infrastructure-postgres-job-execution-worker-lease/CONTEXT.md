# Repo Evidence

- `governance/tasks/0072-measurement-infrastructure-postgres-worker-lease-negative-smoke/STATUS.md` 记录 0072 已完成 Postgres webhook outbox worker lease negative smoke，但明确不证明 job execution worker lease、exactly-once、公网 webhook live 或外部 Vault/KMS。
- `contracts/fate/delivery/runtime-backends.json` 当前 `backend.postgres.implementationStatus=worker_lease_smoke_baseline`，`status=planned`。
- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` 当前 `ReportJobStore` 只有 `claim_webhook_outbox_record` / `release_webhook_outbox_record`，没有 queued/running job execution claim/release。
- `ReportJobManager._worker_loop()` 当前从进程内 `Queue` 取 job id 后执行，不能证明跨进程/多 worker job claim 互斥。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 0.9 推荐执行顺序第 1 项是 `Postgres job execution worker lease`。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 高风险异步状态变更 | 任务拆为 PRECHECK/IMPLEMENT/VERIFY/OPERATE/CLOSEOUT，必须记录并发、幂等、失败恢复和 non-claims。 |
| 不能破坏 memory/sqlite | 默认 backend 行为保持不变；新增接口默认 no-op / conservative，生产 claim 只在 Postgres smoke 中证明。 |
| 不能泄露 DSN/secret | 脚本只从 env 读取 DSN，summary 只写 hash、check 名和状态，不输出连接串或用户输入。 |
| 本地可无 Postgres | `--allow-missing` 只能写 `status=blocked` 并 exit 0，不能作为 live pass。 |
| 不能夸大结论 | `backend.postgres.status` 保持 `planned`；summary `shipGate.status=blocked`。 |

# Change Boundary

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/postgres-job-worker-lease-smoke.py`
- `scripts/postgres-job-worker-lease-smoke.sh`
- `scripts/local-ci.sh`
- `scripts/runtime-backend-gate.py`
- `contracts/fate/delivery/runtime-backends.json`
- `contracts/fate/delivery/registry.json`
- `contracts/fate/delivery/schemas/runtime-backend.schema.json`
- `tests/regression/test_postgres_job_worker_lease_smoke.py`
- `tests/regression/test_runtime_backend_gate.py`
- `tests/regression/test_capability_protocol.py`
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `domains/experience-delivery/services/fatecat-delivery/AGENTS.md`
- `contracts/fate/delivery/AGENTS.md`
- `scripts/AGENTS.md`
- `governance/tasks/0074-*`
- `governance/tasks/INDEX.md`

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| job lease 被误写成 exactly-once | 生产语义被夸大 | contract/docs/summary 均写 `does_not_prove_exactly_once`。 |
| claim/release 更新覆盖终态 job | 已完成任务被错误重入 | claim 条件仅允许 `queued/running` 且 lease 可用；smoke 覆盖 terminal non-claim。 |
| 错误 owner release | 多 worker 可能重复执行 | release 必须匹配 owner；smoke 验证 loser release 无效。 |
| lease expiry 语义误伤长任务 | 运行中任务被其他 worker 抢走 | 本任务只证明 lease primitive；生产续租/心跳留给后续，不声明 production ready。 |
| summary 泄露连接信息 | 安全事故 | `_safe_summary` 拦截敏感模式和 forbidden runtime values。 |

# Assumptions and Falsification

- Assumption: Postgres conditional update can atomically claim a queued/running job for one lease owner.
- Falsifier: real Postgres smoke 中任一 duplicate claim race 出现两个 winner。
- Assumption: release must match active lease owner.
- Falsifier: loser release 后 loser 能在未过期 lease 上 claim 同一 job。
- Assumption: terminal job is not executable and must not be claimable.
- Falsifier: succeeded/failed/cancelled/expired job 被 `claim_job_for_execution` 返回。
- Assumption: expired running job lease can be reclaimed by another worker.
- Falsifier: lease expiry 后第二个 worker 无法 claim。

# Engineering Change Safety

| Field | Value |
| --- | --- |
| risk_level | high |
| affected_flows | CalculationJob / ReportJob durable runtime、Postgres backend smoke、local-ci quick |
| external_contracts | `contracts/fate/delivery/runtime-backends.json`、runtime backend gate |
| data_flow | `_ReportJob` persisted into `report_jobs`; claim updates lease columns and returns claimed job row |
| control_flow | multiple workers call `claim_job_for_execution`; only owner with active lease may release |
| state_changes | queued/running job lease owner/acquired/expires fields change; terminal states remain unclaimable |
| side_effects | DB writes only; no external webhook live call |
| concurrency_idempotency | duplicate claim negative, wrong owner release negative, expiry reclaim smoke |
| consistency_model | Postgres row-level conditional update in one transaction |
| failure_recovery | allow lease expiry reclaim; crash restart execution remains later task |
| performance_cost | indexed status/lease query; no unbounded scan in smoke |
| observability | summary JSON plus runtime backend gate limits |
| rollout | optional Postgres-only capability; default backend unchanged |
| rollback | remove job lease columns/logic references and revert implementationStatus |
| required_tests | focused unit/contract tests, real disposable Postgres smoke, local-ci quick |

# Future-Optimal Contract

- Target end state: `CalculationJob` durable runtime has external backend, worker coordination, event history, retry/outbox, webhook delivery, secret lifecycle, observability and audit evidence.
- Real constraints: 当前无生产 webhook receiver、外部 Vault/KMS、Temporal worker 或真实多副本部署窗口；只能用 disposable/真实 Postgres smoke 证明 primitive。
- Inertia constraints: 不能因为现有 manager 使用内存 queue，就把 job execution lease 降级成 docs-only 或 outbox lease alias。
- Wrong concept / wrong boundary: outbox worker lease 不是 job execution worker lease；job lease 也不是 exactly-once。
- Kill list: allow-missing 伪通过、production ready 伪声明、DSN 泄露、用 SQLite local queue 假装分布式 worker。
- Proof point: real Postgres smoke 显示 duplicate job claim winner count 为 1、wrong owner release blocked、lease expiry reclaim true。
- Falsifier: 任何 race 产生两个 winner，或 terminal job 被 claim，或 loser release 后可抢未过期 lease。
- Migration slice: 本轮只增加 Postgres job lease primitive 和 smoke；下一轮才能做 crash/restart execution worker。
- Rejected short-term patches: 不通过 sleep/进程锁模拟分布式锁；不把 outbox lease 方法重命名复用为 job lease。
- Future-optimal review owner: `auto-review` with future-optimal-drift and reliability/concurrency lenses。

# Ponytail Contract

- Existence check: 0.9 路线图把 job execution worker lease 列为下一 P0；这是 external backend production 的必要 primitive。
- Selected ladder rung: project-native capability using mature Postgres conditional update / row-level semantics; no new worker framework yet。
- Skipped scope: Temporal, Redis queue, heartbeat续租, exactly-once, public webhook live, Vault/KMS, production deployment。
- Ceiling / upgrade path: lease primitive 不足以证明生产多副本执行；后续需 crash/restart worker smoke、heartbeat/renew、idempotent execution 和 live webhook。
- Do-not-simplify: release 必须 owner 匹配；terminal job 必须不可 claim；summary 必须脱敏。
- Minimal runnable check: focused tests + disposable Postgres smoke。
- Complexity review owner: `auto-review` with ponytail-complexity and feature-change-safety。

# Document-Driven Contract

| Field | Status |
| --- | --- |
| Operating model update | not needed: 项目定位不变。 |
| Toolchain model update | updated: 新增 smoke 脚本和 local-ci artifact 时同步 scripts/AGENTS 与 docs。 |
| Process update | not needed: 仍沿用 runtime backend gate / local-ci / task closeout 流程。 |
| Source-of-truth updates | updated: runtime backend contract、roadmap、operations docs、任务包。 |
| Local README/AGENTS impact | updated: `scripts/AGENTS.md`、`domains/.../AGENTS.md`、`contracts/.../AGENTS.md`。 |
| Contract/catalog/schema impact | updated: runtime backend registry/schema/gate。 |
| ADR/Gate/module-context impact | updated: runtime backend gate。 |
| Documentation exemption reason | none: 本任务改变 runtime contract 和 toolchain，必须同步文档。 |
| Validation evidence | focused tests、real Postgres smoke、local-ci、validators。 |

# Debug Evidence Contract

- 调试模式: Optional
- 失败时必须记录：失败 check 名称、脚本参数、summary 路径、是否包含敏感输出、Postgres 版本/启动方式。
- 不允许用 allow-missing blocked artifact 替代 real smoke。

# Critical Ambiguities

- 本任务证明 job lease primitive，不证明 worker 真正从 DB 拉取并执行业务任务。
- Crash/restart with external backend 仍是后续任务。
- Exactly-once 仍不声明；未来应按 at-least-once + idempotency + duplicate negative tests 表达。

# Task Package Context Map

| Artifact | Purpose |
| --- | --- |
| `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | Store abstraction and Postgres job lease implementation |
| `scripts/postgres-job-worker-lease-smoke.py` | Real/disposable Postgres job worker lease smoke |
| `contracts/fate/delivery/runtime-backends.json` | RuntimeBackend production boundary |
| `tests/regression/test_postgres_job_worker_lease_smoke.py` | Script/contract/docs regression |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | Operator command and non-claim docs |
