# Planning Summary

目标终态：CalculationJob 的外部 Postgres runtime 不只证明“数据库可写、worker 可恢复”，还必须能证明终态 webhook callback 能通过真实 HTTP 出口投递，并在 Postgres outbox 中留下成功证据。

Real constraints:

- 真实公网 webhook endpoint 和真实 Postgres DSN 不能伪造。
- webhook URL/secret/DSN 不能进入 Git、日志、summary 或任务文档。
- 现有 API、Web、Bot 默认行为不能被本任务改变。
- `backend.postgres.status` 在 exactly-once、多副本、Vault/KMS 和公网证据全部完成前必须保持 `planned`。

Inertia constraints:

- 现有 SQLite redelivery smoke 只能证明本地机制，不能替代公网 live。
- 0075 worker restart smoke 不能被重新解释成 webhook live。
- task 文档和 roadmap 里旧的 `future public webhook live` 必须同步为 0076 的明确门禁。

Wrong concept / wrong boundary:

- 错误概念：用 mocked transport 或本地 callback.example 证明公网 live。
- 正确边界：本地 CI 只证明脚本、blocked preflight 和契约；live passed 只能来自真实 endpoint。

Proof point:

- `bash scripts/postgres-public-webhook-live-smoke.sh --allow-missing` 能生成 blocked summary。
- 在真实 `FATE_REPORT_JOB_DATABASE_URL` + `FATE_WEBHOOK_LIVE_URL` 环境下，脚本能生成 `status=passed`，且 outbox `succeeded`、事件包含 `webhook.delivery_succeeded`。

Falsifier:

- summary 包含 DSN、URL、secret、报告正文、姓名或出生地区。
- 无真实外部配置时脚本退出为 passed。
- contract 将 Postgres 提升为 production ready 或 exactly-once。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0076 不能标记 Done。

- SPEC：锁定 live smoke、blocked preflight、隐私和 non-claims。
- PLAN：选择最小切片：新增脚本与 contract 接线，不改业务报告生成。
- BUILD：只复用现有 manager/store/dispatcher，不新增 webhook 协议。
- TEST：跑 blocked preflight、focused tests、runtime backend gate、ruff、quick CI。
- REVIEW：检查 future-optimal drift、ponytail complexity、document drift、secret leakage。
- SHIP：提交推送并用远端 CI 验证当前 commit。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | live smoke 与 non-claims 明确 | Done |
| PLAN | 任务树、风险字段和验证命令写入任务包 | Done |
| BUILD | 脚本、wrapper、contract、docs、tests 完成 | In Progress |
| TEST | blocked preflight、focused tests、quick CI、validators 执行 | Not Started |
| REVIEW | 不泄露 secret、不夸大 production ready、不引入无用抽象 | Not Started |
| SHIP | commit/push，刷新远端 CI evidence | Not Started |

# Simplest Path

直接新增一个 live smoke 工具：

1. 读取 `FATE_REPORT_JOB_DATABASE_URL`、`FATE_WEBHOOK_LIVE_URL`、可选 `FATE_WEBHOOK_LIVE_SECRET`、可选 allowlist。
2. 使用 disposable schema 初始化 Postgres store。
3. 使用 `ReportJobManager.submit()` 提交一条固定脱敏 report job。
4. 使用 `HttpWebhookDispatcher` 对真实 URL 发起 HTTPS POST。
5. 轮询 snapshot，验证 `succeeded`、outbox `succeeded`、事件包含 `webhook.delivery_succeeded`。
6. 输出脱敏 JSON，保留 ship gate 为 blocked，直到其余生产证据完成。

# Split Strategy

递归任务节点定义：

| Node ID | Type | Depends On | Deliverable | Gate |
| --- | --- | --- | --- | --- |
| TP-01 | PRECHECK | none | 当前缺口、边界和风险记录 | 不把 mock/本地 callback 当 live |
| TP-02 | IMPLEMENT | TP-01 | `postgres-public-webhook-live-smoke.py/.sh` | allow-missing blocked + live path |
| TP-03 | VERIFY | TP-02 | contracts/docs/local-ci/tests/AGENTS 接线 | Postgres 仍 planned |
| TP-04 | TEST | TP-03 | 本地验证证据 | 不泄密，测试通过 |
| TP-05 | SHIP | TP-04 | closeout、commit、push、远端 CI | 当前 commit CI 通过 |

按风险面拆分为五个节点：

- PRECHECK：边界和现有机制事实。
- IMPLEMENT：脚本和 wrapper。
- VERIFY：contracts/docs/local-ci/tests。
- TEST：本地和可选 live 验证。
- SHIP：版本控制和远端 CI。

# Execution Waves

| Wave | Nodes | Gate |
| --- | --- | --- |
| W1 | TP-01 | 当前缺口和边界清楚。 |
| W2 | TP-02, TP-03 | 代码、契约、文档同步。 |
| W3 | TP-04 | 本地验证通过且不泄密。 |
| W4 | TP-05 | clean git、push、远端 CI。 |

# Runtime Workflow Contract

risk_level: high
affected_flows: async report job terminal callback, Postgres job store, webhook outbox, live release readiness
users_roles: operator with external DSN/webhook endpoint; developer running local CI; auditor reviewing evidence
external_contracts: `FATE_REPORT_JOB_DATABASE_URL`, `FATE_WEBHOOK_LIVE_URL`, optional `FATE_WEBHOOK_LIVE_SECRET`, public HTTPS webhook endpoint
data_flow: static sanitized report job -> Postgres job/outbox -> HttpWebhookDispatcher -> external endpoint -> Postgres outbox result -> redacted summary
control_flow: CLI preflight -> optional blocked summary -> manager submit -> worker execute -> terminal webhook dispatch -> summary validation
state_changes: disposable Postgres schema is created and dropped by default; outbox and job records are temporary
side_effects: real HTTPS POST to operator-provided endpoint when live env vars exist
concurrency_idempotency: one generated job per smoke run; no exactly-once claim
consistency_model: Postgres transactional job/outbox persistence plus HTTP callback best-effort delivery
failure_recovery: live failures produce failed/blocked summary without leaking runtime values
storage_cache_compatibility: no production schema migration beyond existing Postgres ReportJobStore schema
performance_cost: one job and one webhook callback per live run; no unbounded loops
observability: summary records checks, status, event types, outbox status, target fingerprint and ship gate
rollout: local CI runs allow-missing only; live mode is operator-driven
rollback: remove script/local-ci/contract references; no persisted repo data

# Next Executable Leaves

- TP-02：新增 smoke 脚本与 wrapper。

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- 删除 `scripts/postgres-public-webhook-live-smoke.py` 与 `.sh`。
- 恢复 `contracts/fate/delivery/runtime-backends.json`、schema/gate/local-ci、docs、AGENTS 和 regression tests 中的 0076 引用。
- 恢复 `governance/tasks/INDEX.md` 当前任务行和本任务目录。
