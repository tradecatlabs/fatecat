# Planning Summary

Build a redacted external validation closure evidence summary as the next non-credential-dependent slice after 0127. The summary consumes existing external validation artifacts and emits one audit-ready rollup without executing live checks.

# Lifecycle Gates

- SPEC: scope, non-claims, upstream evidence chain and external blockers are explicit.
- PLAN: split into contract/script, local-ci/certification wiring, documentation, validation and delivery observation.
- BUILD: implement only the migration slice; no production live calls.
- TEST: run targeted pytest, lint/format, task docs validation, secret scan and quick CI.
- REVIEW: check future-optimal drift, Ponytail complexity, document drift and security/privacy.
- SHIP: commit/push and observe remote CI through outer delivery flow.

不得跳过 gate. If real external credentials are required, the task must stop at `外部连通验证待执行` instead of fabricating evidence.

# Simplest Path

Reuse existing 0119/0120/0121/0122/0123/0127 artifacts and add one bounded generator plus one wrapper. Do not introduce a new executor framework, storage layer, external dependency or live integration.

Existence check: a separate closure evidence summary is needed because trend dashboard answers owner/stale alert questions, while certification answers domain gate questions; neither provides audit-ready per-work-item operator closure state.

Selected ladder rung: project-native direct implementation using existing JSON contracts, scripts and local-ci pattern.

Skipped scope: real live execution, credential storage, third-party audit, external issue tracker, new provider logic, new report output.

Ceiling / upgrade path: when operators submit real evidence through a portal, this summary should become the read model for external validation closure status.

Do-not-simplify: keep raw URL/secret rejection, closure blocked state, source hashes and non-claims.

Minimal runnable check: focused regression tests plus quick local CI artifact.

Complexity review owner: `auto-review` with document-drift, security/privacy and ponytail-complexity lenses.

# Split Strategy

| Node | Purpose | Depends On |
| --- | --- | --- |
| TP-01 | Confirm scope and upstream evidence chain | - |
| TP-02 | Add contract/script/wrapper | TP-01 |
| TP-03 | Wire local-ci and certification | TP-02 |
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

- Inputs: work queue JSON, proof-ref gate JSON, category runbooks JSON, operator packet JSON, live proof gate JSON, closure trend dashboard JSON.
- Outputs: `external-validation-closure-evidence-summary.json`.
- External side effects: none.
- Secret handling: secret values and raw URLs are rejected; only variable names, credential names and placeholders are allowed.
- Evidence handling: summary includes source hashes, closure states and blocking reasons; real proof refs remain operator-supplied later.

# Next Executable Leaves

- No remaining local leaves after TP-05 succeeds.
- TP-06 is handled by outer Git/GitHub delivery flow after final validation.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol

- Revert the 0128 commit if the summary wiring breaks quick CI or remote CI.
- Since no runtime service, database migration, secret or external side effect is introduced, rollback is Git-only.
- If generated artifact semantics are wrong but local-ci is green, follow-up with a new task and keep non-claims in place until corrected.
