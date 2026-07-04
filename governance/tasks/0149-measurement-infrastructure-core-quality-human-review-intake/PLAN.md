# Planning Summary
0149 的本质是把核心质量的“人工外部评审”从不可执行口头项变成基础设施资源。正确终态不是仓库里写“专家说通过”，而是：

1. 仓库定义可接收的脱敏 evidence bundle。
2. 本地 gate 默认 blocked，防止无证据过关。
3. 真实 bundle 到位时只接收 refs/hash/aggregate/status，不接收原始正文或隐私数据。
4. certification 必须消费该 gate，避免核心质量绕过人工/外部证据。

不得跳过 gate。0149 本地切片完成不代表真实专家评审或外部 benchmark 完成。

# Lifecycle Gates
不得跳过 gate；尤其不得用 synthetic fixture、文档声明或本地 blocked-as-expected 结果替代真实外部专家评审、外部 benchmark aggregate 和 no-leak signoff。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | 0148 roadmap defined core quality human review/external benchmark as next node. |
| PLAN | Done | This task tree separates local intake infrastructure from external evidence closure. |
| BUILD | Done | Contract/script/wrapper/tests/wiring added. |
| TEST | Pending | Focused tests and quick local CI must pass after edits. |
| REVIEW | Done with blockers | Self-review encoded in negative tests and non-claim boundaries. |
| SHIP | Pending | Commit/push/remote Acceptance pending. |

# Simplest Path
Reuse the existing evaluation registry, local-ci, certification aggregator and external evidence pattern. Do not introduce a new review platform or external connector. Do not run real expert review inside the repo.

# Split Strategy
| Node | Type | Reason |
| --- | --- | --- |
| TP-01 | Discovery | Confirms the real missing object is intake, not another corpus. |
| TP-02 | Implementation | Adds the minimal gate and contract. |
| TP-03 | Wiring | Makes the gate count in infrastructure evidence. |
| TP-04 | External closure | Keeps real human/external evidence separate and blocked. |
| TP-05 | Delivery | Verifies and ships the local slice. |

# Execution Waves
```text
Wave 1: TP-01.01
Wave 2: TP-02.01, TP-02.02
Wave 3: TP-03.01, TP-03.02
Wave 4: TP-05.01
Wave 5: TP-05.02
Blocked external wave: TP-04.01, TP-04.02
```

# Runtime Workflow Contract
Future operator bundle must:

- use `kind=fatecat.core_quality_human_review_bundle`;
- bind to current commit;
- cover every dimension in `professional-quality-rubric.v1`;
- include only artifact/evidence refs and sha256 values;
- include external benchmark aggregate only;
- include no-leak signoff;
- avoid all forbidden fragments.

# Next Executable Leaves
- TP-05.01 local validation.
- TP-04.01 and TP-04.02 are blocked until external human/operator evidence exists.

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.01 -> TP-02.02
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-05.01
TP-05.01 -> TP-05.02
TP-04.01 -> TP-04.02
TP-04.02 -> future certification acceptance
```

# Rollback Protocol
- Remove the new gate contract/script/test and wiring changes.
- Remove 0149 task directory and INDEX row.
- Do not touch existing core corpus, rubric, MingLi-Bench data or provider code.
