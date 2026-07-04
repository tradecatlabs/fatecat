# Planning Summary

Add `ExternalValidationProofRefGate` as a local control-plane contract between work queue and future live category gates. The gate accepts an optional operator-supplied redacted evidence bundle, validates schema and bindings, and emits a blocked summary that certification can consume.

# Lifecycle Gates

| Gate | Requirement |
| --- | --- |
| SPEC | Contract and schema declare proof-ref bundle fields, privacy boundary and non-claims |
| PLAN | Task package records scope, risks, proof point and rollback |
| BUILD | Script validates work queue, optional evidence bundle, negative cases and summary |
| TEST | Regression tests cover pending mode, accepted redacted bundle, anti-forgery and wiring |
| REVIEW | Schema accepted cannot imply production live passed |
| SHIP | local quick CI passes before commit/push |

不得跳过 gate；未跑过的验证不得写成 passed。

# Simplest Path

Do not build an evidence database, dashboard, upload API or notification workflow in this slice. A local JSON schema and verifier are sufficient to make later category runbooks auditable.

# Split Strategy

| TP | Work |
| --- | --- |
| TP-01 | Confirm MI-100.A.02 scope and existing gate patterns |
| TP-02 | Implement contract, schema, script, wrapper and certification wiring |
| TP-03 | Add regression tests and local-ci artifact |
| TP-04 | Update AGENTS, roadmap, task index and task docs |
| TP-05 | Run gates, review output, commit/push, observe CI |

# Execution Waves

1. Contract/schema/script/wrapper/certification wiring.
2. Regression tests and local-ci wiring.
3. AGENTS/roadmap/task docs/index.
4. Targeted tests, secret scan, real gate chain and quick CI.
5. Commit, push and remote CI observation.

# Runtime Workflow Contract

```text
current-audit-bundle/pending-external-validations.json
  -> external-validation-closure-gate.json
  -> external-validation-closure-work-queue.json
  -> external-validation-proof-ref-gate.json
  -> later category live gates and third-party audit
```

# Next Executable Leaves

- TP-04.01 Run targeted pytest and ruff.
- TP-04.02 Run secret scan and real proof-ref gate chain.
- TP-04.03 Run quick CI.
- TP-05.01 Commit/push and observe CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `contracts/fate/audit/external-validation-proof-ref.json`.
- Remove `contracts/fate/audit/schemas/external-validation-proof-ref.schema.json`.
- Remove `scripts/external-validation-proof-ref-gate.py` and `.sh`.
- Remove local-ci/certification/test/AGENTS/roadmap wiring for proof-ref.

# Future-Optimal Target End State

External validation should behave like infrastructure reconciliation: desired state is the work queue, observed state is proof-ref plus category live evidence, and ship state is derived by gates. This task creates the proof-ref contract layer only.

# Ponytail Existence Check

The new object exists because operator evidence needs a stable, privacy-safe, reviewable format before external live categories can be closed. A local JSON gate is the lowest ownership-cost layer; an upload service is intentionally deferred.
