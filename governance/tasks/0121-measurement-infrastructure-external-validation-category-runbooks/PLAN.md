# Planning Summary

Add `ExternalValidationCategoryRunbooks` as the operator-facing control-plane layer after work queue and proof-ref schema. The gate consumes the work queue, validates every category has a known runbook profile, and emits blocked runbooks for live evidence collection.

# Lifecycle Gates

| Gate | Requirement |
| --- | --- |
| SPEC | Contract declares required runbook fields, known categories, privacy boundary and non-claims |
| PLAN | Task package records scope, risks, proof point and rollback |
| BUILD | Script validates work queue, category coverage and runbook output |
| TEST | Regression tests cover category coverage, unknown category, privacy and wiring |
| REVIEW | Runbook ready cannot imply production live passed |
| SHIP | local quick CI passes before commit/push |

不得跳过 gate；未跑过的验证不得写成 passed。

# Simplest Path

Do not build an upload API, notification system, issue tracker sync or dashboard in this slice. A local JSON runbook artifact is enough to make later category live work executable.

# Split Strategy

| TP | Work |
| --- | --- |
| TP-01 | Confirm MI-100.A.03 scope and current category set |
| TP-02 | Implement contract, script, wrapper and certification wiring |
| TP-03 | Add regression tests and local-ci artifact |
| TP-04 | Update AGENTS, roadmap, task index and task docs |
| TP-05 | Run gates, review output, commit/push, observe CI |

# Execution Waves

1. Contract/script/wrapper/certification wiring.
2. Regression tests and local-ci wiring.
3. AGENTS/roadmap/task docs/index.
4. Targeted tests, secret scan, real gate chain and quick CI.
5. Commit, push and remote CI observation.

# Runtime Workflow Contract

```text
external-validation-closure-work-queue.json
  -> external-validation-proof-ref-gate.json
  -> external-validation-category-runbooks.json
  -> later category live gates and stale owner alert
```

# Next Executable Leaves

- TP-04.01 Run targeted pytest and ruff.
- TP-04.02 Run secret scan and real category runbooks gate chain.
- TP-04.03 Run quick CI.
- TP-05.01 Commit/push and observe CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `contracts/fate/audit/external-validation-category-runbooks.json`.
- Remove `scripts/external-validation-category-runbooks.py` and `.sh`.
- Remove local-ci/certification/test/AGENTS/roadmap wiring for category runbooks.

# Future-Optimal Target End State

External validation closure should have a clear operator path: category runbook, proof-ref evidence, category live gate, trend/stale alert, certification. This task creates the runbook layer only.

# Ponytail Existence Check

The new object exists because proof-ref schema alone says how evidence is shaped, not how each category collects it. A local JSON runbook gate is the lowest ownership-cost layer; notification and dashboard are deferred.
