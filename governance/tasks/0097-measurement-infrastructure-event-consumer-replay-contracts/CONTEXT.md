# Repo Evidence
| Evidence | Result |
| --- | --- |
| `contracts/fate/delivery/events.json` | 已有 5 个 job/webhook/evaluation/release AsyncEvent。 |
| `contracts/fate/delivery/events.asyncapi.json` | 已有 AsyncAPI 3.1 static document baseline。 |
| `contracts/fate/delivery/schemas/async-event.schema.json` | 已有 CloudEvents/AsyncAPI 字段基线。 |
| `scripts/event-contract-gate.py` | 已有 event contract gate，0097 前主要校验 schema/channel/message/example。 |
| `tests/regression/test_event_contract_gate.py` | 已有 4 个基础 regression。 |
| `scripts/run-evaluations.py` | 真实 evaluation producer 路径；0097 修正旧 registry 断链路径。 |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不新增平行事件系统 | 继续复用 `events.json` 和 `event-contract-gate.py`。 |
| 不依赖外部账号 | 所有验证为本地 contract/gate/test。 |
| 不泄露隐私或凭证 | 示例只保存 synthetic/redacted refs，不保存 payload 正文。 |
| 不夸大生产能力 | 外部 broker、公网 webhook live、真实 DLQ/worker 明确 out of scope。 |

# Critical Ambiguities
- 是否要接入真实 broker：本任务明确不做，只做本地 consumer/replay contract baseline。
- 是否要实现生产 replay worker：本任务不做，只登记策略和脱敏示例。
- 是否要把 webhook live 改成 passed：不做，仍保持 `requires_real_receiver` 和 `外部连通验证待执行`。

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 现有 AsyncEvent registry 是事件契约唯一真相源 | 出现另一个事件 contract registry 或 gate。 |
| required consumer contract 足以推进 Next-02 本地切片 | event gate 或 regression 不能证明缺 consumer 会失败。 |
| replay/DLQ 可以先作为 policy baseline | 任务试图声明生产 replay/DLQ worker 已完成。 |

# Change Boundary
- 修改 `contracts/fate/delivery/events.json`、`schemas/async-event.schema.json` 和新增 `examples/event-replay/*.json`。
- 修改 `scripts/event-contract-gate.py` 与 `tests/regression/test_event_contract_gate.py`。
- 修改相关 AGENTS、API 接入文档、路线图和任务文档。
- 不修改 runtime webhook/job 执行逻辑，不修改 production delivery API。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| 契约字段增加但 gate 未覆盖 | gate 增加 required field、producer path、consumer、replay/DLQ 示例检查。 |
| 示例保存敏感信息 | replay examples 走 `_contains_sensitive_example_value` 和 secret scan。 |
| 文档把本地 contract 写成生产事件平台 | AGENTS/API/roadmap 明确外部 broker 和 live delivery 未完成。 |

# Debug Evidence Contract
- 调试模式: Optional
- Not required. 本任务是 contract/gate 增强，不是复现缺陷修复。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | Existing event registry, AsyncAPI document, schema, gate and tests. |
| TP-02.01 | `events.json` consumer compatibility and per-event consumer contract. |
| TP-02.02 | Replay/DLQ policy and redacted fixture examples. |
| TP-03.01 | `scripts/event-contract-gate.py` validation expansion. |
| TP-03.02 | `tests/regression/test_event_contract_gate.py` positive and negative coverage. |
| TP-04.01 | AGENTS, API docs, roadmap and task package sync. |
| TP-05.01 | Final validation and delivery evidence. |
