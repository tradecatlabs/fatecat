# Task Overview

- Task ID: `0076`
- Slug: `measurement-infrastructure-postgres-public-webhook-live-smoke`
- Objective: 执行 MI-100 Durable Runtime 的公网 webhook live smoke 切片：在 Postgres external backend worker restart baseline 之后，新增需要真实 Postgres DSN 与公网 HTTPS webhook endpoint 的 live smoke 工具，验证 report job 终态事件能通过真实 HTTP webhook 投递并持久化 outbox 成功状态；无外部配置时必须输出 blocked summary，不泄露 DSN、URL、secret、报告正文或用户输入，不声明 exactly-once、多副本 production ready 或外部 Vault/KMS 已完成。
- Status: `In Progress`

## In Scope

- 新增 Postgres public webhook live smoke 脚本与 shell wrapper。
- smoke 使用真实 `FATE_REPORT_JOB_DATABASE_URL` 和真实公网 `FATE_WEBHOOK_LIVE_URL`，通过 `ReportJobManager`、`PostgresReportJobStore` 和 `HttpWebhookDispatcher` 执行一条终态 report job callback。
- 缺少 DSN、webhook URL、可选依赖或外部连通条件时，`--allow-missing` 输出 `status=blocked` 的脱敏 summary。
- summary 只输出 host/url/database hash、状态、事件类型、outbox 状态和 ship gate，不输出 DSN、URL、secret、报告正文、姓名、出生地区或生产路径。
- 同步 runtime backend contract、schema/gate/local-ci、operations docs、roadmap、AGENTS 和 regression tests。

## Out of Scope

- 不实现 exactly-once。
- 不声明 Postgres 多副本 production ready。
- 不接入外部 Vault/KMS 或生产 secret manager。
- 不实现 webhook 接收端；该 smoke 只消费外部提供的公网 HTTPS endpoint。
- 不把 blocked preflight 写成 live passed。
- 不改变默认 Web/API/Bot 报告业务逻辑。

## Task Package Tree

```text
TP-01 PRECHECK：公网 webhook live 边界和当前 runtime 能力审查
TP-02 IMPLEMENT：Postgres public webhook live smoke 脚本与 wrapper
TP-03 VERIFY：契约、schema、gate、local-ci、文档和 AGENTS 接线
TP-04 TEST：blocked preflight、focused regression、runtime backend gate 和 quick CI
TP-05 SHIP：任务 closeout、提交推送和远端 CI 证据
```

## Requirement Alignment

| Requirement | Handling |
| --- | --- |
| 真实公网 webhook live smoke | 新脚本要求真实 Postgres DSN 与公网 HTTPS webhook URL；无配置只 blocked。 |
| 复用成熟/现有能力 | 复用 `ReportJobManager`、`PostgresReportJobStore`、`HttpWebhookDispatcher`、HMAC header 与 outbox。 |
| 不泄露敏感信息 | summary 做敏感值扫描，只保留 hash/fingerprint。 |
| 不夸大生产结论 | contract 保持 `backend.postgres.status=planned`，`shipGate.status=blocked`，non-claims 写明 exactly-once、多副本、Vault/KMS 未完成。 |
| 可审计验证 | wrapper、contract gate、regression tests、quick CI 和 task validators 组成最小证据链。 |

## Task Package Overview

| Node ID | Status | Purpose |
| --- | --- | --- |
| TP-01 | Done | 锁定 webhook live 与 production ready 的边界。 |
| TP-02 | In Progress | 新增脚本、wrapper 和脱敏 summary。 |
| TP-03 | Pending | 同步 contracts/docs/local-ci/AGENTS。 |
| TP-04 | Pending | 跑 blocked preflight、测试、lint 和 CI。 |
| TP-05 | Pending | closeout、提交推送、远端 CI。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
