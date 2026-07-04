# Planning Summary
0151 的目标是补齐“提交外部证据前的总审计视图”。现有链路已经能生成 proof-ref gate、live proof gate、operator packet、人审 gate、第三方审计预演和 certification，但缺少一个统一入口回答：

- 当前 commit 需要提交哪些 evidence bundle？
- 哪些 bundle schema 已准备好？
- 哪些 artifact hash 仍是 operator 待填？
- 哪些 operator command 已有稳定 hash？
- 哪些 gate 仍在 blocking？

# Lifecycle Gates
不得跳过 gate；0151 必须完成 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 后才可交付。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | 0150 roadmap 6.40 指定 0151 为下一批本地/审计任务。 |
| PLAN | Done | 0151 task package defines tree, scope and validation. |
| BUILD | In Progress | contract/script/tests/local-ci/docs. |
| TEST | Pending | targeted pytest, script smoke, local-ci quick or focused gate, task docs validation, diff check. |
| REVIEW | Pending | Self-review non-claim, sensitive output and gate semantics. |
| SHIP | Pending | Commit, push and remote Acceptance. |

# Simplest Path
不新增新的 external evidence truth source。只读取现有 JSON summary：

- `external-validation-closure-work-queue.json`
- `external-validation-proof-ref-gate.json`
- `external-validation-live-proof-gate.json`
- `external-validation-operator-execution-packet.json`
- `core-quality-human-review-gate.json`
- `third-party-audit-rehearsal.json`
- `measurement-infrastructure-certification.json`

# Split Strategy
| Node | Type | Reason |
| --- | --- | --- |
| TP-01 | Existing-state audit | 防止重复造 proof/live/human review gate。 |
| TP-02 | Contract | 让 readiness audit 输出可复核。 |
| TP-03 | Implementation | 产出可执行脚本、测试和 CI artifact。 |
| TP-04 | Documentation | 保证新入口可发现。 |
| TP-05 | Verification/ship | 用真实命令和远端 CI 证明。 |

# Execution Waves
```text
Wave 1: TP-01.01, TP-01.02
Wave 2: TP-02.01, TP-02.02
Wave 3: TP-03.01, TP-03.02, TP-03.03
Wave 4: TP-04.01, TP-04.02
Wave 5: TP-05.01, TP-05.02
```

# Runtime Workflow Contract
```bash
bash scripts/external-evidence-submission-readiness-audit.sh \
  --work-queue-json <external-validation-closure-work-queue.json> \
  --proof-ref-gate-json <external-validation-proof-ref-gate.json> \
  --live-proof-gate-json <external-validation-live-proof-gate.json> \
  --operator-packet-json <external-validation-operator-execution-packet.json> \
  --core-quality-human-review-json <core-quality-human-review-gate.json> \
  --third-party-audit-rehearsal-json <third-party-audit-rehearsal.json> \
  --certification-json <measurement-infrastructure-certification.json>
```

# Next Executable Leaves
- TP-03.01 finish contract/script/wrapper.
- TP-03.02 run and fix regression tests.
- TP-03.03 ensure local-ci summary includes the readiness artifact.
- TP-05.01 run validation.

# Dependency Graph
```text
TP-01.01 -> TP-02.02
TP-01.02 -> TP-03.03
TP-02.01 -> TP-04.02
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-05.01
TP-03.03 -> TP-05.01
TP-04.01 -> TP-05.01
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- Revert only 0151 task directory, readiness audit contract/script/test, local-ci wiring, AGENTS and roadmap lines.
- Do not revert existing proof-ref/live/human review/certification gates.
