# Planning Summary
0098 把 retention 从“本地 SQLite cleanup baseline”推进为“生产 cleanup staged evidence gate”。正确终态是 scheduler、Postgres cleanup 和 SIEM/log retention 都有脱敏 proof-ref，可被 gate 验证；本轮只做 contract/gate，不做 live。

# Lifecycle Gates
不得跳过 gate；如果 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP 任一 gate 缺验证证据，0098 不得 closeout。

| Gate | Requirement | Status |
| --- | --- | --- |
| SPEC | 明确 staged gate 边界，不做生产删除 | Done |
| PLAN | 复用 0091/0083 的 retention/security contract | Done |
| BUILD | 新增 contract、gate、wrapper、tests、local-ci 接线 | Done |
| TEST | focused gate/tests 已通过 | Done |
| REVIEW | 文档不声明 live passed | In Progress |
| SHIP | quick local-ci 和 closeout validator 通过后提交 | Pending |

# Simplest Path
新增一个薄 gate：读取 contract、验证 registry/policy 接线、拒绝负例、可选验证脱敏 evidence JSON。它不接外部服务，也不调用 cleanup runtime。

# Split Strategy
- TP-01：复核现状。
- TP-02：新增 contract/gate。
- TP-03：接线和测试。
- TP-04：验证和交付。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01, TP-02.02 |
| 3 | TP-03.01, TP-03.02 |
| 4 | TP-04.01 |

# Runtime Workflow Contract
| Field | Value |
| --- | --- |
| Allowed tools | shell read/test, apply_patch edits, git after validation |
| Forbidden actions | external DB/scheduler/SIEM connection, production delete, secret output |
| Evidence required | gate JSON, focused pytest, secret scan, quick local-ci, task validator |
| Stop condition | gate/test failure that changes evidence schema |

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| TP-04.01 | Run final validators and update closeout. |

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol
- Remove 0098 contract/gate/test/doc wiring.
- Keep 0091 local retention cleanup baseline unchanged.
