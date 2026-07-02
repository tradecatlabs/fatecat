# Repo Evidence

- `governance/tasks/0071-measurement-infrastructure-postgres-live-smoke/STATUS.md` 记录 0071 已完成 Postgres migration/job live smoke baseline，但明确不证明生产多副本 worker、exactly-once、公网 webhook live 或外部 Vault/KMS。
- `contracts/fate/delivery/runtime-backends.json` 将 `backend.postgres` 保持为 `status=planned` external candidate。
- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` 已提供 `PostgresReportJobStore` 和 webhook outbox conditional claim/release 边界，本任务只新增 smoke 和 contract 接线，不改命理逻辑。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的最新 durable runtime 路线要求先收口 worker lease negative smoke，再推进 job execution worker lease。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不能泄露 DSN/secret | 脚本只从 env 读 DSN，summary 输出 host/database/schema hash，不输出 raw DSN、用户名、密码、URL、secret 或报告正文。 |
| 本地开发可无 Postgres | `--allow-missing` 输出 `blocked` summary 并 exit 0，供 local-ci preflight 使用。 |
| 真实验证需要数据库 | 使用一次性 Docker Postgres 或真实 Postgres DSN 运行 live smoke；无 DSN 不写 passed。 |
| 不声明生产 | `shipGate.status=blocked`，nonClaims 明确剩余边界。 |

# Change Boundary

- `scripts/postgres-worker-lease-smoke.py`
- `scripts/postgres-worker-lease-smoke.sh`
- `scripts/local-ci.sh`
- `scripts/runtime-backend-gate.py`
- `contracts/fate/delivery/*`
- `tests/regression/test_postgres_worker_lease_smoke.py`
- `tests/regression/test_runtime_backend_gate.py`
- `tests/regression/test_capability_protocol.py`
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `scripts/AGENTS.md`
- `contracts/fate/delivery/AGENTS.md`
- `domains/experience-delivery/services/fatecat-delivery/AGENTS.md`
- `governance/tasks/0072-*`
- `governance/tasks/INDEX.md`

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 outbox lease 当成 job execution lease | 生产 durable runtime 被夸大 | 文档、contract、summary 均写明 `does_not_prove_job_execution_worker_lease`。 |
| summary 泄露连接信息 | 安全事故 | `_safe_summary` 拦截 DSN 和 run id；测试扫描敏感模式。 |
| 无 Postgres 环境下误报通过 | 伪证 | `--allow-missing` 只输出 `status=blocked`。 |
| 并发 claim 非确定性 | flaky | 每轮只断言 winner count 必须为 1；race count 可调，默认 5。 |

# Assumptions and Falsification

- Assumption: `PostgresReportJobStore.claim_webhook_outbox_record` 使用数据库条件更新语义保证同一 outbox 记录同一时刻只能被一个 lease owner claim。
- Falsifier: real Postgres smoke 中任一 `duplicate_claim_negative_*` winner count 不等于 1。
- Assumption: 错误 owner release 不应清掉 winner lease。
- Falsifier: loser release 后 loser 可立即 claim 同一 outbox。
- Assumption: expired lease 可被其他 owner 重新 claim。
- Falsifier: 过期后第二个 store 无法 claim。

# Critical Ambiguities

- 本任务只覆盖 webhook outbox lease，不覆盖 job execution worker lease。
- Postgres smoke 使用一次性 schema，不覆盖生产连接池、迁移回滚、备份恢复、权限模型或长时间锁竞争。
- Exactly-once 不在本任务范围；后续只能按 at-least-once + idempotency + duplicate negative tests 证明。

# Debug Evidence Contract

- 调试模式: Optional

若 real Postgres smoke 失败，必须记录失败 check 名称、Postgres 环境、脚本参数、summary 路径和是否包含敏感输出；不得基于 allow-missing blocked artifact 宣称 live 通过。

# Task Package Context Map

| Artifact | Purpose |
| --- | --- |
| `scripts/postgres-worker-lease-smoke.py` | Worker lease negative smoke implementation |
| `contracts/fate/delivery/runtime-backends.json` | RuntimeBackend production boundary |
| `tests/regression/test_postgres_worker_lease_smoke.py` | Script/contract/docs regression |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | Operator-facing command and non-claim docs |

## TP-01 边界与证据目标

- Context: 0071 已证明 Postgres schema/job/outbox/config live path，但未证明多 worker 负例。
- Boundary: 本节点只定义 proof target，不实现 production worker。

## TP-02 Worker lease negative smoke 实现

- Context: 新脚本连接 Postgres，创建一次性 schema，模拟两个独立 store 并发 claim。
- Boundary: 输出必须脱敏，失败必须 fail-fast 或 blocked。

## TP-03 Contract、文档和测试接线

- Context: RuntimeBackend registry、gate、local-ci、docs 和 AGENTS 必须同口径。
- Boundary: `backend.postgres.status` 保持 `planned`。

## TP-04 验证、closeout 和交付

- Context: 语法、blocked preflight、real Postgres smoke、focused tests、secret/source checks、local-ci 和任务 validators 是最小证据。
- Boundary: 远端 CI 需要 commit/push 后刷新。
