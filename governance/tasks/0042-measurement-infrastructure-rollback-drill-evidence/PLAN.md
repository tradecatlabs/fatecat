# Planning Summary
把 rollback drill 从“给一个路径就通过”推进为本地 dry-run 可审计证据：先生成 JSON，再让 live gate 校验 JSON 内容，最后接入 public-release。

# Lifecycle Gates
| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | rollback dry-run 与真实生产回滚边界明确 | Done |
| PLAN | 任务树、验收和反证写入任务包 | Done |
| BUILD | 脚本、gate 接入、测试、文档完成 | In Progress |
| TEST | JSON、shell、pytest、public-release smoke | Pending |
| REVIEW | 不伪造生产回滚 | Pending |
| SHIP | closeout packet 生成 | Pending |

禁止跳过任何 gate；不得把 dry-run rollback drill 说成真实生产回滚已执行。

# Simplest Path
复用现有 `--rollback-evidence-path` 参数，不新增 required evidence ID；新增本地生成器和 JSON 内容校验。

# Split Strategy
- TP-01 做现状盘点。
- TP-02 做生成器。
- TP-03 做 live gate 校验。
- TP-04 做 public-release 接入。
- TP-05 做验证 closeout。

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| 1 | TP-01.01 | Done |
| 2 | TP-02.01 | In Progress |
| 3 | TP-03.01 | Pending |
| 4 | TP-04.01 | Pending |
| 5 | TP-05.01 | Pending |

# Runtime Workflow Contract
- risk_level: medium
- affected_flows: public release gate, live release gate
- external_contracts: `contracts/fate/delivery/release-gate.json`
- data_flow: rollback-drill writes JSON; public-release/live-release consume it
- state_changes: filesystem artifacts only under configured output directories
- side_effects: no remote calls beyond existing optional production readiness
- rollback: revert script/test/doc changes and remove 0042 task row if needed
- required_tests: targeted pytest, shell syntax, rollback script smoke, public-release smoke

# Next Executable Leaves
TP-02.01

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01 -> TP-05.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
