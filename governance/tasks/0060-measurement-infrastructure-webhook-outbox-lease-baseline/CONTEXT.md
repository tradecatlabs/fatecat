# Context

## Current State

- 0058 已实现 SQLite webhook outbox redelivery baseline，但多个 manager 同时重建时缺少 outbox claim 语义。
- 0059 已实现 SQLite encrypted webhook delivery config vault baseline，可在没有外部 resolver 时恢复 callback URL/secret。
- 当前剩余 durable runtime 缺口仍包括 external backend、生产级分布式 worker lease、真实公网 webhook live smoke、外部 Vault/KMS 和生产密钥生命周期。

## Decision

本任务先实现 SQLite 本地 outbox lease baseline：通过 atomic claim/release 防止本地多 manager 重投同一条 outbox。它是进入 external backend 之前的可验证迁移台阶，不是生产多副本最终方案。

## Source Files

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `scripts/webhook-outbox-redelivery-smoke.py`
- `scripts/webhook-config-vault-smoke.py`
- `tests/regression/test_api_contracts.py`
- `scripts/local-ci.sh`

## Boundaries

- 不在 API payload 中输出 lease owner 或 lease 时间。
- lease owner 不得包含 secret、URL、用户输入或报告正文。
- SQLite lease 只证明本地 claim/release 语义，不证明跨云、多副本、external backend 或 exactly-once。

# Repo Evidence

| Evidence | Current Fact |
| --- | --- |
| `git status --short --branch` | clean at 0060 start |
| `governance/tasks/INDEX.md` | 0058/0059 已 Done，0060 正在新增 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | durable runtime 仍缺 external backend、生产级分布式 worker lease、真实公网 webhook live smoke、外部 Vault/KMS |
| `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | redelivery 会扫描 failed/pending outbox，但 0060 前没有 claim/release |
| `scripts/webhook-config-vault-smoke.py` | 可生成 failed outbox + encrypted config vault，本任务可复用模式 |

# Constraints Matrix

| Constraint | Impact |
| --- | --- |
| 不切换分支 | 所有改动留在当前 `main` |
| 不伪造 external backend | 文档必须保持本地 SQLite baseline 口径 |
| 不暴露内部 lease | API payload 不新增 lease owner/expires |
| 不输出 secret | smoke summary 和 events 不包含 URL/secret/用户输入 |
| 不新增依赖 | 使用 SQLite atomic update |

# Change Boundary

允许修改：

- `report_jobs.py`
- `main.py`
- `scripts/local-ci.sh`
- `scripts/webhook-outbox-lease-smoke.*`
- `tests/regression/*`
- `docs/reference-materials/*`
- `AGENTS.md` 局部目录文档
- `governance/tasks/0060-*` 与 `governance/tasks/INDEX.md`

禁止修改：

- 命理计算核心。
- Web 视觉布局。
- 生产 secret、真实外部配置。
- 退役路径或 unrelated cleanup。

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| claim 失败仍 dispatch 导致双发 | manager 必须先 claim 成功再解析 config/dispatch |
| lease 永久占用 | release 后清理；后续真实生产再实现 lease expiry worker |
| API 暴露内部 owner | payload 测试保护 |
| 本地 baseline 被误读为生产分布式 lease | docs/roadmap/AGENTS 明确边界 |

# Assumptions and Falsification

- Assumption: SQLite atomic conditional update 足以证明本地 claim/release 语义。
- Falsifier: 两个不同 owner 都能 claim 同一条未过期 outbox。
- Assumption: lease 字段不需要进入 public API。
- Falsifier: `webhookOutbox[]` payload 出现 `leaseOwner`、`leaseExpiresAt` 或类似字段。

# Critical Ambiguities

- 真实 external backend 选型仍未决定；本任务不做 Redis/Postgres/Temporal/Celery 选型承诺。
- 生产 worker lease 的时钟偏移、owner heartbeat、worker crash recovery 仍待后续任务。

# Debug Evidence Contract

- 调试模式: Optional
- 该任务是新增 baseline，不是 bugfix；若出现 flaky 或 CI-only failure，再升级为 Required 并维护 `DEBUG.md`。

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01.01 | roadmap、0058/0059、report_jobs、smoke |
| TP-02.01 | `ReportJobStore`、`SQLiteReportJobStore` |
| TP-02.02 | `ReportJobManager._redeliver_webhook_outbox_record` |
| TP-03.01 | existing smoke scripts |
| TP-03.02 | `tests/regression/test_api_contracts.py` |
| TP-03.03 | `scripts/local-ci.sh` |
| TP-04.01 | docs、AGENTS、INDEX |
| TP-04.02 | validators、pytest、ruff、secret scan、local-ci、git |
