# Planning Summary
0097 是 0095 Wave A Next-02 的本地可执行切片。目标不是接入事件中间件，而是让已有 CloudEvents/AsyncAPI contract 能证明 producer/consumer compatibility、replay policy 和 DLQ policy 的本地可复核边界。

# Lifecycle Gates
不得跳过 gate；如果 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP 任一 gate 缺验证证据，0097 不得 closeout。

| Gate | Requirement | Status |
| --- | --- | --- |
| SPEC | 明确只做本地 contract baseline，不做 broker/live/worker | Done |
| PLAN | 复用现有 events registry 和 gate | Done |
| BUILD | 增加 consumerContract、replayPolicy、DLQ 示例和 gate 检查 | Done |
| TEST | event gate 与 focused regression 通过 | Done |
| REVIEW | 文档不夸大生产能力，隐私边界清楚 | Done |
| SHIP | closeout validator、secret scan、quick local-ci 通过后提交 | Done |

# Simplest Path
1. 在 `events.json` 内增加 top-level `consumerCompatibility` 与 `replayPolicy`。
2. 给每个 event 增加 `consumerContract`，不新建独立平台对象。
3. 在既有 `event-contract-gate.py` 内扩展校验。
4. 用 regression 负例证明 gate 会拒绝断链 producer 和缺 required consumer。

# Split Strategy
- `TP-01` 复核现状。
- `TP-02` 修改契约和示例。
- `TP-03` 修改 gate/test。
- `TP-04` 文档同步。
- `TP-05` 验证、提交与推送。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01, TP-02.02 |
| 3 | TP-03.01, TP-03.02 |
| 4 | TP-04.01 |
| 5 | TP-05.01 |

# Runtime Workflow Contract
| Field | Value |
| --- | --- |
| Allowed tools | shell read/test, apply_patch edits, git after validation |
| Forbidden actions | branch switch, destructive git, external broker/live webhook, secret output |
| Evidence required | event gate JSON, focused pytest, task validator, secret scan, quick local-ci |
| Stop condition | Gate/test failure that requires design change or external credentials |

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-05.01
TP-01.01 -> TP-02.02 -> TP-03.01
```

# Rollback Protocol
- Revert event contract/schema/gate/test/doc changes from this task.
- Remove `contracts/fate/delivery/examples/event-replay/` if 0097 is rolled back.
- Do not alter prior 0063 event baseline or runtime webhook/job logic.
