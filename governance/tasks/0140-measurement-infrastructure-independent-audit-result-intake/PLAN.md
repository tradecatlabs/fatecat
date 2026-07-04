# Planning Summary
The correct target is a first-class independent audit result intake layer: schema, gate, local-ci artifact, rehearsal checklist wiring, regression tests and non-claim boundaries. This task completes the local control plane only; real external audit execution remains outside this environment.

## Target End State
第三方审计结果成为 FateCat 测算基础设施的一等证据资源：有契约、有 gate、有 local-ci artifact、有 rehearsal checklist 显式状态，有测试证明 accepted/rejected/pending 三种结果不会被误解释为 100% 生产完成。

## Real Constraints
- 真实第三方审计人员、签名结果和外部凭证当前不可在本环境验证。
- 不能输出真实 URL、token、secret、DSN、审计人员身份或报告正文。
- 不能把结构接受的审计结果当成 release/certification 通过。

## Inertia Constraints Removed
- 删除 third-party rehearsal 中对 independent result 的硬编码 blocked 语义。
- 不再把“独立审计结果”作为自由文本口径留在文档里。

# Lifecycle Gates
不得跳过任何 gate；独立审计结果 intake、third-party rehearsal、release proof、external proof/live proof 和 certification 必须各自独立闭合，不能互相替代。

| Lifecycle | Required Result | Current Result |
| --- | --- | --- |
| SPEC | Independent audit result intake scope and non-claims defined | Done |
| PLAN | Contract, gate, rehearsal bridge and local-ci wiring selected | Done |
| BUILD | Scripts/contracts/tests/docs implemented | Done |
| TEST | Focused regression and quick local-ci passed | Done |
| REVIEW | No production/audit overclaim | Done |
| SHIP | Commit/push after final git review | Pending |

# Simplest Path
1. Add one independent audit result gate following existing external-validation gate style.
2. Keep default behavior pending/blocked without a real bundle.
3. Feed gate output into third-party audit rehearsal.
4. Prove accepted independent gate does not bypass external pending.
5. Document remaining external blockers.

# Split Strategy
Use five top-level leaves: inspect gap, implement gate, wire rehearsal/local-ci, validate/docs, closeout evidence.

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| Wave 1 | TP-01 | Done |
| Wave 2 | TP-02 | Done |
| Wave 3 | TP-03 | Done |
| Wave 4 | TP-04, TP-05 | Done |

# Runtime Workflow Contract
- Real auditors submit a redacted `fatecat.independent_audit_result_bundle`.
- The bundle must use artifact/evidence refs and hashes, not raw URLs or identities.
- Gate output is consumed by third-party audit rehearsal.
- Release/certification remains blocked unless all aggregate gates also pass.

# Next Executable Leaves
- None for local control-plane work.
- Future external leaf: authorized auditor submits real redacted result bundle.

# Dependency Graph
```text
TP-01 current rehearsal gap
  -> TP-02 independent audit result gate
  -> TP-03 rehearsal/local-ci wiring
  -> TP-04 tests/docs
  -> TP-05 task evidence closeout
```

# Rollback Protocol
- Revert `contracts/fate/audit/independent-audit-result.json`.
- Revert `scripts/independent-audit-result-gate.*`.
- Revert rehearsal/local-ci/test/AGENTS/roadmap wiring.
- No external system rollback is needed because this task created no external result or live request.
