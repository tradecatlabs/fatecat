# Planning Summary
0147 turns the runtime/event external live portion of the 100% infrastructure roadmap into an executable handoff. Current HEAD local gates prove that runtime backend contracts, Postgres adapter dry-run, multi-replica evidence grammar, runtime proof pack grammar, CloudEvents/AsyncAPI, replay examples, DLQ baseline and webhook outbox smokes are coherent. They do not prove that external Postgres, public webhook delivery, multi-replica soak or event platform replay/DLQ are live. Therefore the correct state is blocked with precise operator actions.

# Lifecycle Gates
| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | 0143 lists 0147 as runtime/event external live evidence. |
| PLAN | Done | This task package maps local readiness and 4 external blockers into five TP nodes. |
| BUILD | Done | Current HEAD quick local CI generated fresh runtime/event artifacts. |
| TEST | Done | quick local CI passed and focused regression reported `389 passed`. |
| REVIEW | Done | Non-claim, privacy, DSN/secret and exactly-once boundaries are explicit. |
| SHIP | Blocked | Postgres live, public webhook live, multi-replica soak and event platform proof are missing. |

执行纪律：不得跳过 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 中任何未闭合 gate。

# Simplest Path
1. Bind runtime/event readiness evidence to current HEAD.
2. Record what is locally passed: runtime backend, Postgres dry-run, multi-replica gate, runtime proof gate, event contract and webhook smokes.
3. Record what is externally missing: Postgres live, public webhook live, multi-replica soak and event platform replay/DLQ proof.
4. Keep 0147 blocked and hand off exact proof requirements to the operator.
5. After accepted external proof exists, rerun proof-ref/live-proof/certification gates.

# Split Strategy
| TP | Reason |
| --- | --- |
| TP-01 | Separates current local evidence from external live execution. |
| TP-02 | Postgres live has a distinct DB/worker proof chain and DSN privacy boundary. |
| TP-03 | Multi-replica and public webhook prove runtime operation and live delivery, not just schema. |
| TP-04 | Event platform replay/DLQ proves consumer/replay behavior beyond local contract baseline. |
| TP-05 | Final proof bundle binds runtime/event evidence back to certification. |

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| W1 | TP-01 | Done locally. |
| W2 | TP-02, TP-03, TP-04 | Blocked by external operator platform access and redacted proof refs. |
| W3 | TP-05 | Blocked by accepted runtime/event proof refs and live proofs. |

# Runtime Workflow Contract
No external runtime is started by this task package. Any future operator execution must produce redacted proof refs only. Proof must be validated through existing runtime/event and external validation gates before task status can move from `Blocked`.

# Next Executable Leaves
- TP-02.01, TP-03.01 and TP-04.01 are the next leaves, but all are blocked by missing external runtime/event platform evidence.
- Operator must provide redacted proof for external Postgres, worker leases, restart/heartbeat, public webhook delivery, multi-replica soak, event replay and DLQ.

# Dependency Graph
```text
TP-01.01 current HEAD runtime/event gates
  -> TP-02.01 Postgres runtime live proof blocked
  -> TP-03.01 multi-replica public webhook proof blocked
  -> TP-04.01 event replay DLQ proof blocked
TP-02.01 + TP-03.01 + TP-04.01
  -> TP-05.01 runtime/event proof bundle blocked
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
