# Task Overview

- Task ID: `0072`
- Slug: `measurement-infrastructure-postgres-worker-lease-negative-smoke`
- Objective: 执行 MI-100 Durable Runtime 的 Postgres worker lease negative smoke 切片：在 0071 Postgres migration/job live smoke baseline 之后，新增可连接真实或一次性 Postgres 的多 worker outbox lease 竞争 smoke，用两个独立 `PostgresReportJobStore` / 连接模拟多副本 worker，并验证同一 webhook outbox 记录在并发 claim 下只能一个 worker 成功、失败 worker 不能错误 release、lease 过期后可被其他 worker 重新 claim；证据 JSON 必须脱敏，不输出 DSN、用户名、密码、callback URL、webhook secret 或报告正文；无 DSN/psycopg/Postgres 时明确 blocked，不伪造 production ready、exactly-once、公网 webhook live 或外部 Vault/KMS。
- Status: `Done`

## In Scope

- 新增 `scripts/postgres-worker-lease-smoke.py` 与 `scripts/postgres-worker-lease-smoke.sh`。
- 使用两个独立 `PostgresReportJobStore` / 连接验证 webhook outbox duplicate claim negative path。
- 验证错误 owner 不能 release winner lease、lease 过期后其他 owner 可重新 claim。
- 将 worker lease smoke 接入 `runtime-backends` contract、runtime backend gate、local-ci quick preflight 和 focused regression。
- 同步 operations docs、roadmap、AGENTS 和任务索引。

## Out of Scope

- 不实现 job execution worker lease。
- 不声明 exactly-once。
- 不连接公网 webhook 接收端。
- 不接外部 Vault/KMS 或生产 secret manager。
- 不改变默认 `memory` / `sqlite` 行为。
- 不保存或输出真实 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。

## Task Package Tree

```text
TP-01 边界与证据目标
TP-02 Worker lease negative smoke 实现
TP-03 Contract、文档和测试接线
TP-04 验证、closeout 和交付
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 真实或一次性 Postgres 可验证 | `postgres-worker-lease-smoke.sh` 从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN。 |
| 多 worker 竞争 | 两个独立 `PostgresReportJobStore` / 连接通过 `ThreadPoolExecutor` 和 barrier 同时 claim。 |
| duplicate claim 负例 | 每轮 `duplicate_claim_negative_*` 要求 winner count 必须为 1。 |
| 错误 owner release 负例 | loser release 后再次 claim 仍必须失败。 |
| lease expiry reclaim | lease 过期后另一个 owner 必须可重新 claim。 |
| 脱敏证据 | summary 只输出 hash、check 名和 non-claims，并用 `_safe_summary` 拦截敏感值。 |
| 不伪造生产 | `shipGate.status=blocked`，nonClaims 明确 job execution worker lease、exactly-once、公网 webhook live、外部 Vault/KMS 未证明。 |

## Task Package Overview

| Node | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 0071 后 durable runtime 缺口已确认。 |
| TP-02 | Done | 新脚本和 wrapper 已实现。 |
| TP-03 | Done | contract、docs、AGENTS、local-ci、focused regression 已接线。 |
| TP-04 | Done | syntax、blocked preflight、real Postgres smoke、focused tests 和 task docs validator 已执行。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
