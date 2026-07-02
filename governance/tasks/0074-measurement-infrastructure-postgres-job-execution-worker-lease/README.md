# Task Overview

- Task ID: `0074`
- Slug: `measurement-infrastructure-postgres-job-execution-worker-lease`
- Objective: 执行 MI-100.01 Durable Runtime 的 Postgres job execution worker lease 切片：在 0072 Postgres webhook outbox worker lease negative smoke 之后，为 `PostgresReportJobStore` 增加 queued/running job 执行 claim/release lease 的最小接口、真实或一次性 Postgres smoke、契约门禁、回归测试和文档证据；必须证明多 worker 对同一 queued job 的并发 claim 只有一个成功、错误 owner 不能 release、lease 过期后可重 claim；不得声明 exactly-once、公网 webhook live、外部 Vault/KMS 或 production ready。
- Status: `In Progress`

## In Scope

- 为 `ReportJobStore` 增加 job execution lease 的最小接口，并在 `PostgresReportJobStore` 落地。
- 使用 Postgres 条件更新或等价数据库原子语义证明 queued/running job 的 claim/release 边界。
- 新增 `scripts/postgres-job-worker-lease-smoke.py` 与 `.sh`，支持 `--allow-missing` blocked preflight。
- smoke summary 必须脱敏，不输出 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 将 job worker lease baseline 接入 runtime backend contract、runtime backend gate、local-ci quick preflight、focused regression、operations docs、roadmap 和 AGENTS。
- 保持 `backend.postgres.status=planned`，只把 implementation status 推进到 job execution worker lease smoke baseline。

## Out of Scope

- 不实现 exactly-once。
- 不实现真实公网 webhook live smoke。
- 不接入外部 Vault/KMS 或生产 secret manager。
- 不引入 Temporal、Redis queue 或新的 production worker 编排器。
- 不改变默认 `memory` / `sqlite` backend 行为。
- 不声明生产多副本 durable runtime 已完成。

## Task Package Tree

```text
TP-01 PRECHECK：边界、数据流和并发语义审查
TP-02 IMPLEMENT：Postgres job execution lease 接口与实现
TP-03 IMPLEMENT：Job worker lease smoke 脚本与 wrapper
TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线
TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据
```

## Requirement Alignment

| Requirement | Implementation Plan |
| --- | --- |
| 多 worker job claim negative | 两个独立 `PostgresReportJobStore` / 连接并发 claim 同一 queued job，winner count 必须为 1。 |
| 错误 owner release 负例 | loser release 后，原 winner lease 仍有效；loser 不能接管未过期 lease。 |
| lease expiry reclaim | 未完成 job lease 到期后，其他 worker 可重新 claim。 |
| 不泄露敏感信息 | summary 只输出 hash、check 名和 non-claims，拦截 DSN、secret、run id、报告正文。 |
| 不伪造生产 | summary、contract、docs 均保留 `production_ready`、`exactly_once`、`public_webhook_live`、`external_vault_kms` blocked claims。 |

## Task Package Overview

| Node | Status | Evidence |
| --- | --- | --- |
| TP-01 | In Progress | 当前 repo facts 已确认：Postgres 只有 webhook outbox lease，未有 job execution lease。 |
| TP-02 | Not Started | 等待 TP-01 完成。 |
| TP-03 | Not Started | 等待 TP-02 完成。 |
| TP-04 | Not Started | 等待 TP-02/TP-03 完成。 |
| TP-05 | Not Started | 等待 TP-04 完成。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
