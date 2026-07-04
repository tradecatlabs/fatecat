# Planning Summary

Build a redacted third-party audit rehearsal package as the next non-credential-dependent slice after 0128. The package consumes existing release/audit/certification/closure artifacts and emits one auditor-facing JSON/Markdown bundle without executing live checks.

# Lifecycle Gates

- SPEC: scope, inputs, non-claims and external blockers are explicit.
- PLAN: split into contract/script, local-ci wiring, documentation, validation and delivery observation.
- BUILD: implement only the rehearsal aggregation slice; no production live calls.
- TEST: run targeted pytest, lint/format, task docs validation, secret scan and quick CI.
- REVIEW: check document drift, security/privacy, future-optimal drift and Ponytail complexity.
- SHIP: commit/push and observe remote CI through outer delivery flow.

不得跳过 gate. If real external credentials are required, the task must stop at `外部连通验证待执行` instead of fabricating evidence.

# Simplest Path

Reuse existing JSON artifacts and add one bounded generator plus one wrapper. Do not introduce a new storage layer, portal, issue tracker, external auditor integration or live executor.

Existence check: a separate rehearsal package is needed because `current-audit-bundle` explains evidence, `certification` explains domain readiness, and `closure evidence summary` explains external work items; none provides a single auditor checklist combining all three.

Selected ladder rung: project-native direct implementation using existing JSON contracts, scripts and local-ci pattern.

Skipped scope: real live execution, credential storage, third-party signed result, external issue tracker, new provider logic and new report output.

Ceiling / upgrade path: when an external auditor portal or signed review artifact exists, this rehearsal package becomes the input model for that workflow.

Do-not-simplify: keep raw URL/secret rejection, rehearsal blocked state, input hashes and non-claims.

Minimal runnable check: focused regression tests plus quick local CI artifact.

Complexity review owner: `auto-review` with document-drift, security/privacy and ponytail-complexity lenses.

# Split Strategy

| Node | Purpose | Depends On |
| --- | --- | --- |
| TP-01 | Confirm scope and evidence chain | - |
| TP-02 | Add contract/script/wrapper | TP-01 |
| TP-03 | Wire local-ci and regression | TP-02 |
| TP-04 | Wire AGENTS, roadmap and task index | TP-03 |
| TP-05 | Run validation gates | TP-04 |
| TP-06 | Commit/push and observe CI | TP-05 |

# Execution Waves

```text
Wave 1: TP-01
Wave 2: TP-02
Wave 3: TP-03
Wave 4: TP-04
Wave 5: TP-05
Wave 6: TP-06
```

# Runtime Workflow Contract

- Inputs: current audit bundle JSON, audit dry-run JSON, current release proof JSON, certification JSON, external closure evidence summary JSON.
- Outputs: `third-party-audit-rehearsal.json` and `THIRD_PARTY_AUDIT_REHEARSAL.md`.
- External side effects: none.
- Secret handling: secret values and raw URLs are rejected; only variable names, status, counts and IDs are allowed.
- Evidence handling: rehearsal includes source hashes, checklist states and blocking reasons; real third-party audit result remains external.

# Next Executable Leaves

- TP-05 remains pending until validation gates pass.
- TP-06 is handled by outer Git/GitHub delivery flow after final validation.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol

- Revert the 0129 commit if rehearsal wiring breaks quick CI or remote CI.
- Since no runtime service, database migration, secret or external side effect is introduced, rollback is Git-only.
- If generated artifact semantics are wrong but local-ci is green, follow up with a new task and keep non-claims in place until corrected.
