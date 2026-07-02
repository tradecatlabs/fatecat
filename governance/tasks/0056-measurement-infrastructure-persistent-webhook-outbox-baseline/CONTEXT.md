# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`3d3918d feat: add report job restart recovery smoke`
- 0054 已完成本地 webhook callback retry/outbox trail 首切片，但 outbox 仍只是事件轨迹。
- 0055 已完成 SQLite manager rebuild 的 restart-safe failure smoke。
- roadmap 当前仍列出 `persistent callback outbox`、`external backend` 和 `生产级跨进程继续执行` 为 `MI-NEXT-03` 剩余缺口。
- `report_jobs.py` 当前 webhook dispatch 会同步投递并写入 `webhook.delivery_*` 事件，不存在独立 outbox 表。
- `WebhookConfig.secret` 只允许驻留内存，不能写入 job store、audit log 或响应体。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 不保存 webhook secret | outbox 记录只保存 signature mode，不保存 secret。 |
| 不输出 webhook URL | event metadata 和 API 只输出 host hash / signature / status，不输出完整 URL。 |
| 不声明自动重投 | 文档和 smoke 明确当前只是持久状态 baseline。 |
| quick CI 可重复 | smoke 使用临时 SQLite 与可注入 transport，不访问公网。 |
| 默认 behavior 稳定 | memory store 保持 no-op outbox，不影响无 SQLite 场景。 |

## Change Boundary

允许修改：

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `scripts/webhook-outbox-smoke.py`
- `scripts/webhook-outbox-smoke.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_api_contracts.py`
- `tests/regression/test_webhook_outbox_smoke.py`
- API/roadmap/scripts/tests AGENTS 文档。
- `governance/tasks/0056-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- webhook URL 校验策略。
- external backend、生产多副本 worker、真实公网 webhook live smoke。
- Web HTML 视觉、Bot 文案或生产 secret。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| outbox 被误读成可自动重投 | 审计风险 | 文档和 smoke boundary 写明只是本地持久状态 baseline。 |
| 泄露 URL/secret/用户输入 | 安全风险 | API/event/smoke 只暴露脱敏摘要，测试禁止敏感字符串。 |
| 同步 dispatch 变复杂 | 可靠性风险 | 复用现有 dispatch loop，只包一层 outbox record update。 |
| SQLite migration 影响旧 DB | 升级风险 | 使用 `_ensure_column` / `CREATE TABLE IF NOT EXISTS`，只新增表。 |

## Assumptions and Falsification

- 假设：当前最小 persistent outbox 验收是 SQLite 中有独立 record，能记录 pending/succeeded/failed 和 attempts，并跨 manager rebuild 读取。
  - 推翻条件：要求重启后自动重投，则必须新增持久 callback config、secret 加密和 worker lease，本任务不冒充。
- 假设：不保存完整 URL/secret 是当前安全边界。
  - 推翻条件：后续设计引入加密 key 与 secret vault 后，可升级为可重投 outbox。

## Critical Ambiguities

- external backend 具体选型仍未决策。
- 生产 webhook secret 加密/轮换方案未决策。
- 多副本 outbox worker lease、重投去重、接收方 SLA 不在本任务内。

## Debug Evidence Contract

- 调试模式: Optional
- 若 outbox 持久化与现有 dispatch 事件冲突，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0054/0055、report job/webhook 源码、测试和 local-ci。 |
| TP-02.01 | 修改 report job store 和 SQLite schema。 |
| TP-02.02 | 修改 webhook dispatch 生命周期 outbox 写入。 |
| TP-02.03 | 修改 main API payload。 |
| TP-03.01 | 新增 webhook outbox smoke。 |
| TP-03.02 | 新增 regression tests。 |
| TP-03.03 | 修改 `scripts/local-ci.sh`。 |
| TP-04.01 | 修改文档、AGENTS 和 INDEX。 |
| TP-04.02 | 运行 validators、pytest、ruff、local-ci 和 git 检查。 |
