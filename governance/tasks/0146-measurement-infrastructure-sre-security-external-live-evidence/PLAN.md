# Planning Summary
0146 turns the SRE/security external live portion of the 100% infrastructure roadmap into an executable handoff. Current HEAD local gates prove that contracts, dry-run configs, staged gates, negative evidence rejection and local readiness are coherent. They do not prove that external observability, IdP, SIEM, Vault/KMS or production retention cleanup are live. Therefore the correct state is blocked with precise operator actions.

# Lifecycle Gates
| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | 0143 lists 0146 as SRE/security external live evidence. |
| PLAN | Done | This task package maps local readiness and 6 external blockers into five TP nodes. |
| BUILD | Done | Current HEAD quick local CI generated fresh SRE/security artifacts. |
| TEST | Done | quick local CI passed and focused regression reported `389 passed`. |
| REVIEW | Done | Non-claim, privacy and secret boundaries are explicit. |
| SHIP | Blocked | OTel/SLO/alert, OIDC/IdP, SIEM, Vault/KMS and retention cleanup live proof is missing. |

执行纪律：不得跳过 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 中任何未闭合 gate。

# Simplest Path
1. Bind SRE/security readiness evidence to current HEAD.
2. Record what is locally passed: security, externalization, secret provider, retention, SLO, OTel collector and OTel backend gates.
3. Record what is externally missing: observability live backend, IdP, SIEM, external secret provider and retention cleanup proof.
4. Keep 0146 blocked and hand off exact proof requirements to the operator.
5. After accepted external proof exists, rerun proof-ref/live-proof/certification gates.

# Split Strategy
| TP | Reason |
| --- | --- |
| TP-01 | Separates current local evidence from external live execution. |
| TP-02 | Observability/OTel/SLO has a distinct SRE proof chain and backend proof schema. |
| TP-03 | Identity/SIEM/security externalization has distinct security proof and privacy boundaries. |
| TP-04 | Secret provider and retention cleanup have key-management and deletion-risk boundaries. |
| TP-05 | Final proof bundle binds all SRE/security evidence back to certification. |

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| W1 | TP-01 | Done locally. |
| W2 | TP-02, TP-03, TP-04 | Blocked by external operator platform access and redacted proof refs. |
| W3 | TP-05 | Blocked by accepted SRE/security proof refs and live proofs. |

# Runtime Workflow Contract
No external runtime is started by this task package. Any future operator execution must produce redacted proof refs only. Proof must be validated through existing SRE/security and external validation gates before task status can move from `Blocked`.

# Next Executable Leaves
- TP-02.01, TP-03.01 and TP-04.01 are the next leaves, but all are blocked by missing external SRE/security platform evidence.
- Operator must provide redacted proof for OTel/SLO/alert/error-budget/incident-drill, OIDC/IdP, SIEM/immutable audit, Vault/KMS/secret provider and retention cleanup.

# Dependency Graph
```text
TP-01.01 current HEAD SRE/security gates
  -> TP-02.01 OTel backend SLO live proof blocked
  -> TP-03.01 OIDC SIEM security proof blocked
  -> TP-04.01 Vault KMS retention proof blocked
TP-02.01 + TP-03.01 + TP-04.01
  -> TP-05.01 SRE/security proof bundle blocked
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
