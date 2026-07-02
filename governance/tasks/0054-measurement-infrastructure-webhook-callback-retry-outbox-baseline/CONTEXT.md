# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`9f9bbb0 feat: add report job retry policy`
- 0052 已完成 `CalculationJob event history` 首切片。
- 0053 已完成 report job 本地 retry/timeout policy 首切片。
- roadmap 当前仍列出 `callback retry/outbox`、`external backend` 和 `restart recovery` 为 `MI-NEXT-03` 剩余缺口。
- 当前 webhook callback 已有 URL 校验、签名、payload 隐私边界和本地 smoke。
- 当前 `_dispatch_terminal_webhook` 只投递一次；失败只写 `webhook.delivery_failed`，没有 retry attempt trail。
- 当前 workflow 只有 `workflow_dispatch`，push 不自动产生 GitHub Actions run；本地验证必须如实记录。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 默认行为不能破坏现有 webhook callback | 默认 `webhookMaxAttempts=1`，backoff 0。 |
| webhook retry 不能伪装成持久 outbox | 文档写明当前只是本地 callback retry/outbox trail baseline。 |
| callback 副作用可能重复 | 文档要求接收方按 `eventId` 幂等；默认不重试。 |
| 不泄露用户输入或 endpoint | event metadata 只记录 attempt、errorType、statusCode、eventType、willRetry 等安全字段。 |
| 不新增外部 runtime | 复用现有 `ReportJobManager` 和 `HttpWebhookDispatcher`。 |

## Change Boundary

允许修改：

- `report_jobs.py` webhook policy、callback retry 状态机和事件轨迹。
- `main.py` env vars 和 manager 初始化。
- report job/webhook focused tests。
- production-readiness env validation。
- API/deployment/roadmap/AGENTS 文档。
- `governance/tasks/0054-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- external backend、Temporal/Celery/Redis/Postgres adapter。
- 跨进程持久 outbox 表。
- Web HTML 视觉或 Bot 文案。
- 真实生产 token、真实 webhook endpoint 或公网 live smoke。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| retry 产生重复 callback | 接收方重复处理事件 | 默认 1 次；显式启用才重试；文档要求接收端按 `eventId` 幂等。 |
| retry 阻塞 report worker | worker 被外部 callback 拖慢 | max attempts 有上限；backoff 有上限；默认不重试。 |
| 误宣称持久 outbox 完成 | 审计风险 | 文档保留 persistent outbox、external backend、真实公网 live smoke 缺口。 |
| event 泄露敏感信息 | 隐私风险 | event metadata 不记录 URL、secret、Markdown、姓名、地区、请求体或原始异常文本。 |

## Assumptions and Falsification

- 假设：本轮可以先做进程内 webhook retry baseline，不引入外部队列。
  - 推翻条件：retry 会破坏默认 callback 成功路径或测试出现不可控 flakiness，则缩小为 policy contract。
- 假设：`HttpWebhookDispatcher` 继续负责单次投递，retry 由 `ReportJobManager` 编排。
  - 推翻条件：dispatcher 层更适合保留 retry 状态且不影响事件写入，则改为 dispatcher 返回 attempt evidence。
- 假设：webhook delivery event history 是 callback outbox 的最小本地证据轨迹。
  - 推翻条件：审计要求跨进程持久待投递列表，则本任务不宣称 outbox，仅宣称 retry event trail。

## Critical Ambiguities

- 持久 outbox 表与 external backend 仍留到后续任务。
- 接收方幂等键是否需要从 `eventId` 升级到独立 delivery id，后续再决策。
- 真实公网 webhook live smoke 需要外部 endpoint，不在本地仓库内伪造。

## Debug Evidence Contract

- 调试模式: Optional
- 若 webhook retry 测试 flaky，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0053、report job/webhook 源码、测试、API 文档和 production-readiness。 |
| TP-02.01 | 修改 webhook policy 模型、manager 初始化和 env vars。 |
| TP-02.02 | 修改 `_dispatch_terminal_webhook` 状态机，写入 delivery attempt/retry events。 |
| TP-03.01 | 修改 `tests/regression/test_api_contracts.py` 和 webhook smoke。 |
| TP-03.02 | 修改 docs、AGENTS、production-readiness 和 INDEX。 |
| TP-04.01 | 运行 validators、pytest、ruff、local-ci 和 git 检查。 |
