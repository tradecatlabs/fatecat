# Planning Summary

Use the existing external validation closure plan as input and add one local control-plane layer: `ExternalValidationClosureWorkQueue`. The work queue groups closure occurrences by `(owner, category)`, adds dispatch fields, preserves blocked semantics, and produces a privacy-safe artifact for audit and follow-up live work.

# Lifecycle Gates

| Gate | Requirement |
| --- | --- |
| SPEC | Contract declares input/output fields and non-claims |
| PLAN | Task package records scope, risks, proof point, rollback |
| BUILD | Script validates closure plan and emits deterministic work items |
| TEST | Regression tests cover contract, grouping, privacy, invalid input and wiring |
| REVIEW | Work queue cannot imply external live passed |
| SHIP | local quick CI passes before commit/push |

不得跳过 gate；未跑过的验证不得写成 passed。

# Simplest Path

Do not create a database, dashboard, issue tracker integration, proof verifier or notification system in this slice. A JSON work queue artifact is enough to make the next live closure steps assignable and auditable.

# Split Strategy

| TP | Work |
| --- | --- |
| TP-01 | Confirm source contract and roadmap scope |
| TP-02 | Implement JSON contract and script |
| TP-03 | Add regression tests and local-ci wiring |
| TP-04 | Update task/docs/roadmap |
| TP-05 | Run gates and ship |

# Execution Waves

1. Contract/script/wrapper/local-ci.
2. Regression tests and targeted lint/format.
3. Roadmap/task docs/index.
4. Full local quick CI, commit, push, CI observation.

# Runtime Workflow Contract

```text
current-audit-bundle/pending-external-validations.json
  -> external-validation-closure-gate.json
  -> external-validation-closure-work-queue.json
  -> later proof-ref verifier and live closure evidence
```

The work queue step must not connect to external systems.

# Next Executable Leaves

- TP-05.01 Run real closure gate + work queue against latest local-ci pending bundle.
- TP-05.02 Run full quick CI.
- TP-05.03 Commit/push and observe remote CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `contracts/fate/audit/external-validation-closure-work-queue.json`.
- Remove `scripts/external-validation-closure-work-queue.py` and `.sh`.
- Remove local-ci artifact wiring and regression test.
- Restore AGENTS/roadmap/index/task entry for this slice.

# Future-Optimal Target End State

External validation closure should behave like infrastructure control plane: desired state is a set of external validations, current state is proof-ref status, and reconciliation is performed by category-specific live gates. This task only adds the owner work queue layer because proof verification requires real external evidence.

# Ponytail Existence Check

The new object exists because 402 pending occurrences cannot be operationally closed from a flat list. The selected ladder rung is a small local JSON gate, not a persistent service, because no production credential or multi-user workflow is available in this slice.
