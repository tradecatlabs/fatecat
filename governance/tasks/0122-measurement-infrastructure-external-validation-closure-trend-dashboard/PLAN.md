# Planning Summary

Add `ExternalValidationClosureTrendDashboard` as the local operations-control layer after work queue, proof-ref schema and category runbooks. The gate consumes existing JSON artifacts, validates source consistency, and emits blocked stale-alert dashboard data for owner/category/status follow-up.

# Lifecycle Gates

| Gate | Requirement |
| --- | --- |
| SPEC | Contract declares input kinds, required output fields, alert policy, trend policy, privacy boundary and non-claims |
| PLAN | Task package records scope, risks, proof point and rollback |
| BUILD | Script validates all upstream artifacts, category runbook coverage and dashboard output |
| TEST | Regression tests cover dashboard aggregation, proof-ref accepted boundary, missing runbook rejection, CLI and wiring |
| REVIEW | Stale alert cannot imply production live passed or evidence closure |
| SHIP | local quick CI passes before commit/push |

不得跳过 gate；未跑过的验证不得写成 passed。

# Simplest Path

Do not build notification delivery, external issue sync, persistent history database or public dashboard in this slice. A local JSON dashboard artifact is enough to make unresolved external evidence work visible and auditable.

# Split Strategy

| TP | Work |
| --- | --- |
| TP-01 | Confirm MI-100.A.04 scope and upstream artifacts |
| TP-02 | Implement contract, script and wrapper |
| TP-03 | Add regression tests, local-ci, certification and docs wiring |
| TP-04 | Run gates, review output and update task state |
| TP-05 | Commit/push and observe CI |

# Execution Waves

1. Contract/script/wrapper.
2. Regression tests and local-ci/certification wiring.
3. AGENTS/roadmap/task docs/index.
4. Targeted tests, secret scan, real gate chain and quick CI.
5. Commit, push and remote CI observation.

# Runtime Workflow Contract

```text
external-validation-closure-gate.json
  -> external-validation-closure-work-queue.json
  -> external-validation-proof-ref-gate.json
  -> external-validation-category-runbooks.json
  -> external-validation-closure-trend-dashboard.json
  -> later category live gates / real notification delivery
```

# Next Executable Leaves

- TP-04.01 Run targeted pytest and ruff.
- TP-04.02 Run secret scan and real dashboard gate chain.
- TP-04.03 Run quick CI.
- TP-05.01 Commit/push and observe CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `contracts/fate/audit/external-validation-closure-trend-dashboard.json`.
- Remove `scripts/external-validation-closure-trend-dashboard.py` and `.sh`.
- Remove local-ci/certification/test/AGENTS/roadmap wiring for closure trend dashboard.

# Future-Optimal Target End State

External validation closure should have a clear operator path: category runbook, proof-ref evidence, category live gate, trend/stale alert, certification. This task creates the local trend/stale alert layer only.

# Ponytail Existence Check

The new object exists because work queue and runbooks say what remains, but not how unresolved owners/categories are trended and surfaced. A local JSON dashboard gate is the lowest ownership-cost layer; real notification and public dashboard are deferred.
