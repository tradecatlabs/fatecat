# Planning Summary
Execute only the external tracker creation slice after 0136. The correct end state is not “FateCat 100% infrastructure”; it is “current-HEAD external validation work items have real GitHub issue handles and a redacted gate-accepted evidence bundle.”

# Lifecycle Gates
不得跳过任何 gate；每个 gate 必须有命令、文件或外部 tracker 证据。

| Lifecycle | Required Result | Actual Result |
| --- | --- | --- |
| SPEC | Scope excludes live proof, proof-ref, certification and third-party audit closure | Done |
| PLAN | Current HEAD package -> issue creation -> redacted evidence -> gate accepted | Done |
| BUILD | Create 22 GitHub tracker issues and generate evidence bundle | Done |
| TEST | Run issue evidence gate and focused regression | Done |
| REVIEW | Confirm no overclaiming and no secret-bearing evidence | Done |
| SHIP | Keep ship gate blocked until later live/cert/audit tasks | Blocked as expected |

# Simplest Path
1. Generate current HEAD local CI evidence.
2. Confirm tracker access and no duplicate `[External Validation]` issues.
3. Create missing labels and 22 tracker issues.
4. Generate redacted evidence bundle.
5. Run issue evidence gate.
6. Store only redacted evidence in the task package.

# Split Strategy
No sub-task directories were needed. The task is a single external tracker execution slice with six bounded TP lines.

# Execution Waves
| Wave | Scope | Status |
| --- | --- | --- |
| Wave 1 | Current HEAD/package/tracker preflight | Done |
| Wave 2 | Issue and label creation | Done |
| Wave 3 | Evidence bundle and gate | Done |
| Wave 4 | Task package closeout | Done |

# Runtime Workflow Contract
- External side effect owner: authorized GitHub CLI session.
- Evidence truth source: `TRACKER_ISSUE_EVIDENCE_GATE.json`.
- Non-claim: no live proof, no proof-ref upload, no certification closure, no third-party audit closure.

# Next Executable Leaves
- None inside 0137 after gate acceptance.
- Next separate task should handle proof-ref/live proof/certification/audit closure using real production credentials and authorized external operators.

# Dependency Graph
```text
0136 current HEAD import package
  -> 0137 GitHub issue creation
  -> redacted evidence bundle
  -> issue evidence gate accepted
  -> later proof-ref/live/cert/audit tasks
```

# Rollback Protocol
- Repository rollback: revert this task package and `INDEX.md`/roadmap documentation changes.
- External tracker rollback: close created GitHub issues with an explicit superseded/rollback note; do not delete evidence silently.
- Do not rewrite GitHub issue numbers or stored refs.
