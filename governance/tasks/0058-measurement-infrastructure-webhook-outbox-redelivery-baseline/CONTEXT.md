# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`e0f3602 feat: add replayable report job recovery baseline`
- 0054 已完成本地 webhook callback retry/outbox trail。
- 0056 已完成 SQLite persistent webhook outbox record baseline，但 smoke 明确不证明跨进程自动重投。
- 0057 已完成 replayable report job recovery baseline。
- roadmap 当前仍列出 `external backend`、`生产级分布式 worker lease` 和 `跨进程 webhook 自动重投` 为 `MI-NEXT-03` 剩余缺口。
- `report_jobs.py` 当前能保存 outbox record，但缺少 manager 重建后基于 outbox record 的 redelivery 调度。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 不保存 webhook secret | 持久 outbox 继续只保存摘要；重投由可注入 resolver 在运行时提供配置。 |
| 不保存完整 webhook URL | outbox 只保存 target host hash；summary 和 API 不回显 URL。 |
| 不访问公网 | smoke 使用可注入 dispatcher 和示例 URL，不执行真实网络。 |
| 默认兼容 | 未提供 resolver 时不自动重投，只保留 outbox record。 |
| 不冒充分布式 | 文档和 smoke boundary 写清只是本地 SQLite baseline。 |
| quick CI 可重复 | 使用临时 SQLite 和固定 resolver/dispatcher。 |

## Change Boundary

允许修改：

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/webhook-outbox-redelivery-smoke.py`
- `scripts/webhook-outbox-redelivery-smoke.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_api_contracts.py`
- `tests/regression/test_webhook_outbox_redelivery_smoke.py`
- API/roadmap/scripts/tests AGENTS 文档。
- `governance/tasks/0058-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- webhook URL 校验策略。
- 持久保存明文 secret 或完整 URL。
- external backend、生产多副本 worker lease、真实公网 webhook live smoke。
- Web HTML 视觉、Bot 文案或生产 secret。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| redelivery baseline 被误读成 exactly-once | 审计风险 | 文档和 smoke boundary 写明不是 exactly-once/分布式。 |
| resolver 泄露 secret 或 URL | 安全风险 | summary/API 不输出 resolver 配置；secret scan 覆盖。 |
| 自动重投造成重复回调 | 集成风险 | 仅终态 outbox 且由 policy 限制 attempts；仍不宣称 exactly-once。 |
| manager init 阻塞 | 稳定性风险 | redelivery 使用后台线程或有限循环，不阻塞提交路径。 |
| 与现有 retry 事件冲突 | 可审计风险 | 新增明确 redelivery 事件类型，保留旧事件语义。 |

## Assumptions and Falsification

- 假设：跨进程自动重投可以先通过 runtime resolver + SQLite outbox 摘要实现本地 baseline。
  - 推翻条件：安全要求禁止 resolver 在本地重建 callback 配置，则本任务只能停在 outbox audit record。
- 假设：failed/pending outbox record 的重投可复用现有 dispatcher 和 callback policy。
  - 推翻条件：现有 outbox record 缺少构造 terminal snapshot 的必要字段，则需要新增最小 snapshot reconstruction。
- 假设：本任务不需要持久明文 secret。
  - 推翻条件：必须无需 resolver 自动投递真实公网 webhook，则需要独立设计 encrypted secret storage，本任务不做。

## Critical Ambiguities

- external backend 具体选型仍未决策。
- webhook secret 加密、轮换、租户隔离和权限模型仍未决策。
- 分布式 worker lease、抢占锁、幂等投递和 exactly-once 不在本任务内。

## Debug Evidence Contract

- 调试模式: Optional
- 若 redelivery 与 existing retry/outbox 事件冲突，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0054/0056/0057、report job webhook 源码和测试。 |
| TP-02.01 | 修改 store 查询和 manager redelivery 入口。 |
| TP-02.02 | 增加 resolver 和调度逻辑。 |
| TP-02.03 | 增加 redelivery 事件和隐私边界。 |
| TP-03.01 | 新增 webhook outbox redelivery smoke。 |
| TP-03.02 | 新增 regression tests。 |
| TP-03.03 | 修改 `scripts/local-ci.sh`。 |
| TP-04.01 | 修改文档、AGENTS 和 INDEX。 |
| TP-04.02 | 运行 validators、pytest、ruff、secret scan、local-ci 和 git 检查。 |
