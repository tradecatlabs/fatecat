# Task Overview

- Task ID: `0054`
- Slug: `measurement-infrastructure-webhook-callback-retry-outbox-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第三个可验证切片：为 report job webhook callback 增加本地有限 retry、retry/outbox 事件轨迹、生产预检配置、回归测试和文档说明；不实现跨进程持久 outbox、external backend、真实公网 webhook live smoke 或多副本 worker。`
- Status: `Done`

## In Scope

- 新增 webhook callback delivery policy：`maxAttempts`、`retryBackoffSeconds`。
- webhook 终态投递失败时写入可审计 events，并在有限次数内重试。
- 成功投递记录 attempt、maxAttempts、statusCode、eventType。
- 生产预检校验 webhook retry 相关 env var。
- 同步 API 文档、roadmap、deployment docs、delivery AGENTS 和任务索引。
- 增加 focused tests，覆盖一次失败后成功、全部失败、默认一次投递和隐私边界。

## Out of Scope

- 不实现跨进程持久 outbox 表。
- 不实现 Temporal/Celery/Redis/Postgres external backend。
- 不执行真实公网 webhook live smoke。
- 不改变 webhook payload 隐私边界。
- 不改变 Markdown 报告正文、命理计算核心、Web HTML 视觉或 Bot 文案。

## Task Package Tree

```text
TP-01 当前 webhook retry/outbox 缺口复核
  TP-01.01 读取 0053、roadmap、report job/webhook 源码、测试和生产预检
TP-02 Webhook delivery policy 实现
  TP-02.01 新增 webhook policy 模型、manager 配置和 env 入口
  TP-02.02 修改 webhook 投递状态机，支持有限 retry 与事件轨迹
TP-03 回归测试与文档同步
  TP-03.01 增加 webhook retry success、final failure、default once tests
  TP-03.02 更新 API 文档、roadmap、deployment docs、production-readiness、AGENTS 和 INDEX
TP-04 验收与交付
  TP-04.01 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 0051/0053 后续路线图：`MI-100.02.04 callback retry/outbox`。
- 对齐基础设施同构：外部 callback 属于副作用投递，必须具备有限 retry 和可审计事件。
- 对齐当前架构：继续复用 `ReportJobManager`、`ReportJobStore` 和现有 webhook dispatcher，不新增新 runtime。
- 对齐安全边界：event metadata 不记录 webhook URL、webhook secret、Markdown 正文、姓名、出生地区、请求体或原始异常文本。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 webhook retry/outbox 当前缺口。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 0053、roadmap、源码、测试和生产预检。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现 webhook retry/outbox baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 webhook policy 模型、manager 配置和 env 入口。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 修改 webhook 投递状态机支持 retry 与事件轨迹。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | 补测试和文档。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 增加 webhook retry 回归测试。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 更新文档、预检、AGENTS 和任务索引。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.02 | - | No | No | 验收和交付。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.02 | 4 | No | No | 运行验证并提交推送。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
