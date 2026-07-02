# Task Overview

- Task ID: `0071`
- Slug: `measurement-infrastructure-postgres-live-smoke`
- Objective: 执行 MI-100.02 Durable Runtime 的 Postgres migration/job live smoke 切片：在 0070 PostgresReportJobStore adapter baseline 之后，新增可连接真实或一次性 Postgres 的 live smoke 工具，验证 schema 初始化、job/event/idempotency/task payload、webhook outbox claim/release 和 encrypted delivery config 基本读写；证据 JSON 必须脱敏，不输出 DSN、用户名、密码、callback URL、webhook secret 或报告正文；若缺少 DSN/psycopg/Postgres 环境则明确标记外部连通验证待执行，不伪造 production ready、多副本 worker、exactly-once、外部 Vault/KMS 或公网 webhook live。
- Status: `Done`

## In Scope

- 新增 `scripts/postgres-job-store-live-smoke.py` 与 `.sh` wrapper。
- 使用现有 `PostgresReportJobStore` 连接真实或一次性 Postgres，验证 schema 初始化、job roundtrip、event idempotency、task payload、webhook outbox claim/release、encrypted delivery config 和 cleanup。
- 输出脱敏 JSON evidence：只输出 hash、检查项和 gate 状态，不输出 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- 在缺少 DSN/psycopg/Postgres 环境时通过 `--allow-missing` 生成 `blocked` artifact，供 local-ci 与审计识别“外部连通验证待执行”。
- 更新 runtime backend contract、production-readiness gate、local-ci、回归测试、AGENTS 和路线图。

## Out of Scope

- 不声明 Postgres backend 已 production ready。
- 不证明生产多副本 worker lease、exactly-once、公网 webhook live delivery、外部 Vault/KMS、生产密钥生命周期或真实生产域名。
- 不引入 Temporal、Redis queue、外部 secret manager 或新的任务系统。
- 不改变默认 memory/sqlite 本地运行路径。

## Task Package Tree

```text
TP-01 Context and boundary
  TP-01.01 Confirm post-0070 boundary and runtime conditions
TP-02 Live smoke implementation
  TP-02.01 Add Postgres live smoke script and wrapper
  TP-02.02 Add production-readiness evidence gate
  TP-02.03 Update runtime backend contracts and discovery
TP-03 Tests and live evidence
  TP-03.01 Add regression tests
  TP-03.02 Run allow-missing blocked preflight
  TP-03.03 Run disposable Postgres live smoke
TP-04 Docs and closeout
  TP-04.01 Sync AGENTS, operations docs, roadmap and task index
  TP-04.02 Run validation, local-ci, task validators and git delivery
```

## Requirement Alignment

- 用户要求从测算基础设施视角推进 100% 实现计划，本任务对应 durable runtime 的 external database live smoke proof point。
- 本任务复用 0070 已实现的 `PostgresReportJobStore`，只新增 live evidence 工具和门禁，不重写 store。
- 本任务保持“证据可审计但不夸大”：一次性 Postgres live smoke 只证明真实数据库 schema/job/outbox/config 路径，不证明生产分布式运行。

## Task Package Overview

| ID | Name | Status | Verify | Gate |
| --- | --- | --- | --- | --- |
| TP-01.01 | Boundary Review | Done | `git status`、`rg`、existing docs | 不改变 0070 adapter 边界 |
| TP-02.01 | Live Smoke Tool | Done | py_compile、real Docker Postgres smoke | JSON 脱敏且 `shipGate.status=blocked` |
| TP-02.02 | Production Gate | Done | 正负 production-readiness 命令 | 不能只靠布尔变量声明通过 |
| TP-02.03 | Contract Sync | Done | runtime backend gate、schema tests | `implementationStatus=live_smoke_baseline` 且 status 仍为 planned |
| TP-03.01 | Regression Tests | Done | focused pytest | live-smoke/privacy/contract covered |
| TP-03.02 | Blocked Preflight | Done | `--allow-missing` | 无 DSN 时生成 blocked artifact |
| TP-03.03 | Real Live Smoke | Done | disposable Docker Postgres | schema/job/event/outbox/config checks passed |
| TP-04.01 | Docs Sync | Done | diff/rg | 文档不夸大 production readiness |
| TP-04.02 | Closeout Validation | Done | quick local-ci、validators | 本地门禁通过；远端 CI 待提交推送后刷新 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
