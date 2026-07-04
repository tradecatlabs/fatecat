# Planning Summary

Build a redacted external validation issue export package as the next non-credential-dependent slice after 0129. The package consumes work queue, category runbooks, operator execution packet and closure evidence summary, then emits tracker-ready JSON/Markdown issue templates without creating real issues or executing live checks.

# Lifecycle Gates

- SPEC: scope, inputs, non-claims and external blockers are explicit.
- PLAN: split into contract/script, local-ci wiring, documentation, validation and delivery observation.
- BUILD: implement only the issue export slice; no tracker API or production live calls.
- TEST: run targeted pytest, lint/format, task docs validation, secret scan and quick CI.
- REVIEW: check document drift, security/privacy, future-optimal drift and Ponytail complexity.
- SHIP: commit/push and observe remote CI through outer delivery flow.

不得跳过 gate. If real external credentials or tracker permissions are required, the task must stop at `外部连通验证待执行` instead of fabricating evidence.

# Simplest Path

Reuse existing JSON artifacts and add one bounded generator plus one wrapper. Do not introduce a new tracker client, storage layer, external auditor integration or live executor.

Existence check: issue export is needed because operator packet is machine/operator oriented and third-party audit rehearsal is auditor oriented; neither provides tracker-ready work cards that can be assigned and closed one by one.

Selected ladder rung: project-native direct implementation using existing JSON contracts, scripts and local-ci pattern.

Skipped scope: real issue creation, credential storage, external tracker sync, new provider logic and new report output.

Ceiling / upgrade path: when a real issue tracker integration exists, this issue export becomes the import model and validation fixture for that workflow.

Do-not-simplify: keep raw URL/secret rejection, issue blocked state, source hashes and non-claims.

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

- Inputs: external validation closure work queue JSON, category runbooks JSON, operator packet JSON, closure evidence summary JSON.
- Outputs: `external-validation-issue-export.json` and `EXTERNAL_VALIDATION_ISSUE_EXPORT.md`.
- External side effects: none.
- Secret handling: secret values and raw URLs are rejected; only variable names, owner/category IDs, command templates, hashes and closure conditions are allowed.
- Evidence handling: issue export includes source hashes, issue template bodies and blocking reasons; real issue creation and live execution remain external.

# Next Executable Leaves

- TP-05 remains pending until validation gates pass.
- TP-06 is handled by outer Git/GitHub delivery flow after final validation.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol

- Revert the 0130 commit if issue export wiring breaks quick CI or remote CI.
- Since no runtime service, database migration, secret or external side effect is introduced, rollback is Git-only.
- If generated artifact semantics are wrong but local-ci is green, follow up with a new task and keep non-claims in place until corrected.
