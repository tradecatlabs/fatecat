# Planning Summary
Post-0149 的正确结论是：FateCat 的本地基础设施控制面继续变强，但 100% 仍被真实外部证据阻断。0149 解决了“核心质量专家评审如何进入仓库和 CI”的 intake 问题，没有解决“专家已经评审通过”本身。

因此 0150 的目标不是 final certification，而是把当前证据状态重新压缩成下一批可执行工作：

1. 关闭 0149 的文档漂移。
2. 更新 post-0149 roadmap。
3. 明确剩余 blocked domains。
4. 保持 100% 只能由 accepted external evidence + final release + independent audit + certification 共同证明。

# Lifecycle Gates
不得跳过 gate。0150 是 planning-only slice；它不能替代真实生产 live、专家评审、外部 benchmark、独立审计或 final certification。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | Active goal requires task-tree-driven continuation toward 100% infrastructure. |
| PLAN | In Progress | This task package defines post-0149 target, split and validation plan. |
| BUILD | Pending | Roadmap post-0149 section and task package fill. |
| TEST | Pending | Task docs validation, roadmap marker check, certification baseline, diff check. |
| REVIEW | Pending | Self-review against non-claim and blocker preservation. |
| SHIP | Pending | Commit, push and remote Acceptance after validation. |

# Simplest Path
Do not create a new control plane or new certification mechanism. Reuse:

- `measurement-infrastructure-certification.py`
- current local-ci artifact `/tmp/fatecat-local-ci-0149-final`
- 0149 task package
- roadmap canonical file
- external validation proof-ref/live-proof gates

# Split Strategy
| Node | Type | Reason |
| --- | --- | --- |
| TP-01 | Fact/source baseline | Prevent stale post-0147 plan from hiding post-0149 truth. |
| TP-02 | Gap matrix | Convert certification blockers into explicit evidence classes. |
| TP-03 | Execution tree | Decide what can run next versus what needs operator credentials. |
| TP-04 | Documentation/validation | Keep planning artifact auditable and machine-checked. |

# Execution Waves
```text
Wave 1: TP-01.01, TP-01.02
Wave 2: TP-02.01, TP-02.02
Wave 3: TP-03.01, TP-03.02
Wave 4: TP-04.01, TP-04.02
```

# Runtime Workflow Contract
Future execution must use existing gates:

- Human quality evidence -> `scripts/core-quality-human-review-gate.sh --review-evidence-json <bundle>`
- External proof refs -> `scripts/external-validation-proof-ref-gate.sh --proof-ref-bundle <bundle>`
- Live proofs -> `scripts/external-validation-live-proof-gate.sh --live-evidence-bundle <bundle>`
- Final release -> `scripts/current-release-proof.sh`
- Final audit -> `scripts/current-audit-bundle.sh`
- Final claim -> `scripts/measurement-infrastructure-certification.py --require-certified`

# Next Executable Leaves
For this task:

- TP-04.01 update roadmap and task docs.
- TP-04.02 run validation.

For the project after 0150:

1. External operator path: close 0144/0145/0146/0147 proof-ref/live proof work items with real credentials.
2. Core quality path: provide accepted expert rubric disposition, external benchmark aggregate and no-leak signoff to 0149 gate.
3. Release path: after all external evidence is accepted, regenerate final current-release-proof and current-audit-bundle for the final commit.
4. Audit path: provide independent audit result bundle and run certification with `--require-certified`.
5. Only after those pass, start production admission templates for new divination systems.

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.02
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01
TP-04.01 -> TP-04.02
```

# Rollback Protocol
- Revert only 0150 task directory, its INDEX row, the 0149 delivery evidence doc sync if rejected, and the post-0149 roadmap section.
- Do not revert 0149 code, contracts, tests or CI wiring.
- Do not delete local-ci artifacts under `/tmp`; they are evidence, not source.
