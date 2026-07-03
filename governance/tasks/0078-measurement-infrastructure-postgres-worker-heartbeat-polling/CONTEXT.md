# Repo Evidence

| Evidence | Observation |
| --- | --- |
| `governance/tasks/0077-.../RESEARCH.md` | 0078 是 post-0076 后第一个不依赖外部平台的 P0 实现切片。 |
| `scripts/postgres-job-worker-lease-smoke.py` | 已证明 duplicate job claim、wrong owner release、lease expiry reclaim 和 terminal unclaimable。 |
| `scripts/postgres-external-worker-restart-smoke.py` | 已证明 stale running job expired lease 后可由 restart manager 恢复，但仍声明不证明 heartbeat/polling。 |
| `report_jobs.py` | 有 `claim_job_for_execution`、`release_job_execution_lease` 和 manager restart recovery；无 renew heartbeat，无空闲 polling timeout loop。 |
| `contracts/fate/delivery/runtime-backends.json` | Postgres backend still blocks production multi-replica/exactly-once/external Vault-KMS/public webhook passed. |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不新增重 runtime dependency | 复用现有 Thread/Queue/Postgres adapter。 |
| 不伪造外部 live | smoke 支持 `--allow-missing` blocked summary；真实 DSN 才执行 live path。 |
| 不声明 exactly-once | 只声明 heartbeat/polling smoke baseline 与 at-least-once + idempotency 边界。 |
| 保护现有 memory/sqlite 行为 | 默认 store renew 为 no-op success；polling 只消费 replayable payload。 |
| 文档驱动 | runtime backend contract、operations docs、task docs 必须同步。 |

# Change Boundary

- 允许修改 `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`。
- 允许新增 `scripts/postgres-worker-heartbeat-polling-smoke.py` 和 `.sh`。
- 允许新增/修改 regression tests、runtime backend contract/schema/gate、local-ci、operations docs、AGENTS、task docs。
- 不修改核心八字/紫微算法。
- 不修改外部 secret、生产配置或 CI secret。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Heartbeat thread 泄漏 | worker 长期运行资源泄漏 | 使用 `Event` stop + daemon thread，finally stop。 |
| Polling 重复入队 | 同一 job 被重复执行或队列膨胀 | 只把不在 `_jobs` 且有 task payload/factory 的 job 入队；queue full 标记 failed。 |
| Claim 失败 busy loop | 空闲 worker 高 CPU 或 DB 打爆 | 增加 poll interval/backoff，claim 失败时延后重新尝试。 |
| Renew 误续他人 lease | 破坏 worker isolation | SQL 限定 `job_id`、`lease_owner`、`status='running'`。 |
| 过度声明 | 审计判定伪证 | smoke summary 和 contract nonClaims 明确不证明 production ready/exactly-once/public webhook live/Vault-KMS。 |

# Assumptions and Falsification

- Assumption: Postgres adapter 是当前 external backend 首选切片；Temporal 等仍是 future orchestrator。
- Assumption: heartbeat/polling 能在现有 manager/store 内以最小改动落地。
- Falsifier: 如果 smoke 无法证明长任务 lease 未被抢占，heartbeat 实现不合格。
- Falsifier: 如果外部 seeded queued job 不能在 manager 已启动后被 polling 执行，DB polling 不合格。
- Falsifier: 如果 allow-missing 输出含 DSN/token/secret 或用户输入，隐私 gate 不合格。

# Critical Ambiguities

- 真实生产 worker 数、部署拓扑和 Postgres 参数未指定；本任务只做 smoke baseline。
- exactly-once 语义不在本任务内解决；后续只能从 at-least-once + idempotent side effects 继续推进。

# Debug Evidence Contract

- 调试模式: Optional

若 smoke、focused tests 或 CI 失败，记录最小失败命令、根因、修复和回归证据；不得把失败环境写成代码通过。

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0074/0075/0076 task docs、runtime backend contract。 |
| TP-01.02 | `report_jobs.py` manager/store implementation。 |
| TP-02.01 | Base `ReportJobStore` interface。 |
| TP-02.02 | `PostgresReportJobStore` SQL and lease columns。 |
| TP-03.01 | `_load_persisted_jobs`、`_try_requeue_recovered_job`、`_worker_loop`。 |
| TP-03.02 | `_run_job` execution loop and terminal paths。 |
| TP-03.03 | Queue polling timeout and claim failure behavior。 |
| TP-04.01 | Existing postgres smoke script patterns。 |
| TP-04.02 | `scripts/local-ci.sh` artifact conventions。 |
| TP-04.03 | runtime backend contract/schema/gate/docs。 |
| TP-05.01 | regression test patterns for allow-missing and wiring。 |
| TP-05.02 | focused validation commands。 |
| TP-05.03 | Git/GitHub delivery evidence。 |
