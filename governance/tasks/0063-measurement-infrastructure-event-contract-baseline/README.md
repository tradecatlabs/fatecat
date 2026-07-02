# Task Overview

- Task ID: `0063`
- Slug: `measurement-infrastructure-event-contract-baseline`
- Objective: `执行 0061 后续任务树的 Event Platform P0 切片：为 job/webhook/evaluation/release 事件新增 CloudEvents envelope 与 AsyncAPI 风格事件契约基线，提供 schema、registry、examples、event contract gate、回归测试和文档 closeout；本任务不实现真实公网 webhook live delivery、不连接外部 broker、不声明事件平台已生产。`
- Status: `Done`

## In Scope

- 新增 AsyncEvent schema、event registry、AsyncAPI 风格静态文档和 CloudEvents synthetic examples。
- 更新 delivery registry、resource schema、delivery AGENTS、scripts AGENTS、API 文档和 100% roadmap。
- 新增 `event-contract-gate` Python/sh wrapper、回归测试，并接入 `local-ci --profile quick` artifact。
- 运行 focused tests、task validators、lint、secret scan 和 quick local CI。

## Out of Scope

- 不实现真实公网 webhook live delivery。
- 不连接 Kafka、NATS、RabbitMQ、Redis Streams 或其他外部 broker。
- 不实现事件订阅 API、消费者 SDK、生产投递重试或 exactly-once。
- 不读取、不输出、不保存真实 webhook URL、secret、token、用户输入、出生地区、报告正文或生产事件日志。

## Requirement Alignment

- 对齐 0061 推荐任务：`0063 CloudEvents/AsyncAPI baseline`，要求 `event schema、examples、docs smoke`，不能只写自然语言事件说明。
- 对齐基础设施定位：事件是开发者平台与审计链路资源，不是命理算法实现。
- 对齐 CloudEvents：事件示例必须具备 `id/source/specversion/type` 必备上下文字段。
- 对齐 AsyncAPI：以 `channels + operations + messages` 形式登记消息驱动接口。
- 对齐不可伪造原则：本轮只证明 contract baseline，本地 gate 不能替代真实 receiver、broker 或公网投递证据。

## Task Package Tree

```text
TP-01 Event contract context
  TP-01.01 复核 0061/0062、delivery registry、report job/webhook/evaluation/release 事件事实
TP-02 Contract baseline
  TP-02.01 新增 AsyncEvent schema、registry、AsyncAPI 文档和 synthetic examples
  TP-02.02 更新 resource schema、delivery registry 和 delivery AGENTS
TP-03 Gate、测试和 CI
  TP-03.01 新增 event-contract-gate Python/sh wrapper
  TP-03.02 新增 regression tests 覆盖 gate、CloudEvents examples 和 registry links
  TP-03.03 接入 local-ci quick artifact
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、scripts AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 并收口
```

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核事件契约落点和现有运行时事实。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 0061/0062、delivery contracts、report job/webhook/evaluation/release 事件事实和官方标准资料。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 新增 AsyncEvent contract baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 AsyncEvent schema、registry、AsyncAPI 文档和 synthetic examples。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 更新 resource schema、delivery registry 和 delivery AGENTS。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | Gate、测试和 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 event-contract-gate。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 新增 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并收口。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
