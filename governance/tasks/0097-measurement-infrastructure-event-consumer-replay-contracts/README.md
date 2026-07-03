# Task Overview
- Task ID: `0097`
- Slug: `measurement-infrastructure-event-consumer-replay-contracts`
- Objective: `执行 0095 Wave A Next-02：在现有 CloudEvents/AsyncAPI 事件契约 baseline 上，补齐本地可验证的 producer/consumer compatibility、replay/DLQ 策略和负向测试；复用 contracts/fate/delivery/events.json、events.asyncapi.json、async-event.schema.json 与 scripts/event-contract-gate.py，不连接真实 broker、不声明公网 webhook live delivery、不实现生产队列；新增或强化机器可读策略、示例、gate、regression tests、文档和任务 closeout。`
- Status: `Done`

## In Scope
- 增强 `contracts/fate/delivery/events.json` 的 consumer compatibility、每事件 `consumerContract`、replay policy 与 dead-letter policy。
- 新增脱敏 replay request 和 dead-letter record 合成示例。
- 增强 `scripts/event-contract-gate.py`，验证 producer path、required consumer、additive compatibility、replay source、DLQ 和示例脱敏。
- 增加 regression 正向和负向测试。
- 同步 delivery/scripts/tests AGENTS、API 接入文档、100% 路线图和任务包。

## Out of Scope
- 不接入 Kafka、NATS、RabbitMQ、Redis Streams 或任何真实 broker。
- 不声明公网 webhook live delivery、真实订阅端或事件平台生产可用。
- 不实现生产队列、生产 DLQ 存储、真实重放 worker 或 exactly-once。
- 不保存真实事件流、完整 payload、用户输入、报告正文、真实 webhook URL、secret、token、DSN 或生产日志。

## Task Package Tree
```text
TP-01 复核现有事件契约
  TP-01.01 读取 events registry、AsyncAPI、schema、gate、tests、docs
TP-02 增强事件契约
  TP-02.01 增加 consumer compatibility 与 per-event consumerContract
  TP-02.02 增加 replay/DLQ policy 和脱敏 replay 示例
TP-03 增强 gate 与测试
  TP-03.01 强化 event-contract gate
  TP-03.02 增加 regression 正向和负向测试
TP-04 文档同步
  TP-04.01 同步 AGENTS、API 接入文档、路线图和任务包
TP-05 验证与收口
  TP-05.01 运行 focused gate/tests、隐私/安全/任务校验和 quick local-ci
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 复用现有事件契约 | 只增强 `contracts/fate/delivery/events.json`、schema 和既有 gate。 |
| consumer compatibility | 每个事件增加 `consumerContract.requiredConsumers`，gate 拒绝只有 future consumer 的契约。 |
| replay/DLQ | 新增 `replayPolicy`、dead-letter policy 和两个脱敏 contract fixture。 |
| negative tests | regression 覆盖缺 required consumer、缺 producer path 和敏感 replay 示例检测。 |
| 不夸大生产能力 | 文档明确外部 broker、公网 webhook live、生产 DLQ/worker 仍待外部验证。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | 已读取现有事件契约、gate、tests 和 API 文档。 |
| TP-02.01 | Done | `events.json` 增加 consumer compatibility 和 per-event consumerContract。 |
| TP-02.02 | Done | `replayPolicy` 与 `examples/event-replay/*.json` 已新增。 |
| TP-03.01 | Done | `event-contract-gate.py` 检查数提升到 243。 |
| TP-03.02 | Done | 聚焦 regression 11 passed。 |
| TP-04.01 | Done | AGENTS、API 文档、路线图已同步。 |
| TP-05.01 | Done | closeout validator、secret scan、quick local-ci、diff check 通过。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
