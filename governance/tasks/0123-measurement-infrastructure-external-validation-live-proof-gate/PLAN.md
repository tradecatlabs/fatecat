# Planning Summary

Add `ExternalValidationLiveProofGate` as the bridge between proof-ref structure acceptance and category live closure. It validates redacted live evidence summaries without executing production checks or over-claiming infrastructure completion.

# Lifecycle Gates

| Gate | Requirement |
| --- | --- |
| SPEC | Contract and schema declare input kinds, live proof fields, source binding, redaction boundary and non-claims |
| PLAN | Task package records target state, out-of-scope and proof point |
| BUILD | Script validates work queue, proof-ref gate, category runbooks and optional live evidence bundle |
| TEST | Regression tests cover pending mode, accepted live proof, missing proof-ref rejection, raw URL/placeholder rejection, CLI and wiring |
| REVIEW | Gate cannot claim external truth or third-party audit |
| SHIP | local quick CI passes before commit/push |

不得跳过 SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 任一 gate；未验证的结论不得写成 passed。

# Simplest Path

A local JSON gate is sufficient. No database, issue tracker, notification delivery, external credential use or public dashboard is introduced in this slice.

# Split Strategy

| TP | Work |
| --- | --- |
| TP-01 | Confirm 0123 scope and upstream artifacts |
| TP-02 | Implement contract, schema, script and wrapper |
| TP-03 | Wire local-ci, certification, closure trend dashboard and docs |
| TP-04 | Run targeted tests, ruff, secret scan, real gate chain and quick CI |
| TP-05 | Commit/push and observe remote CI |

# Execution Waves

1. Contract/schema/script/wrapper.
2. local-ci/certification/closure trend/docs wiring.
3. Targeted ruff/pytest/secret scan and real local gate chain.
4. Quick local CI.
5. Commit, push and remote CI observation.

# Runtime Workflow Contract

```text
external-validation-closure-work-queue.json
  -> external-validation-proof-ref-gate.json
  -> external-validation-category-runbooks.json
  -> external-validation-live-proof-gate.json
  -> external-validation-closure-trend-dashboard.json
  -> measurement-infrastructure-certification.json
```

# Next Executable Leaves

- TP-04.01 Run quick local CI.
- TP-04.02 Update task status/checklist with final evidence.
- TP-05.01 Commit, push and observe remote CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `contracts/fate/audit/external-validation-live-proof-gate.json`.
- Remove `contracts/fate/audit/schemas/external-validation-live-evidence.schema.json`.
- Remove `scripts/external-validation-live-proof-gate.py` and `.sh`.
- Remove local-ci/certification/trend/test/AGENTS/roadmap wiring for live proof gate.

# Future-Optimal Target End State

External validation must be closeable by evidence, not by text TODOs. The correct long-term model is a proof chain: closure occurrence -> work item -> proof-ref -> category runbook -> live proof -> audit/certification.

# Ponytail Existence Check

The object exists because proof-ref acceptance is structurally weaker than live proof acceptance. A separate gate prevents false closure while keeping the ownership surface small.
