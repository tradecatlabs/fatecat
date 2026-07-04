# Planning Summary

Build a redacted all-category external validation operator execution packet as the next non-credential-dependent slice after 0126. The packet consumes existing external validation work queue, proof-ref gate and category runbooks, then emits a machine-readable operator handoff without executing live checks.

# Lifecycle Gates

- SPEC: scope, non-claims, upstream evidence chain and external blockers are explicit.
- PLAN: split into contract/script, command alignment, wiring, validation and delivery observation.
- BUILD: implement only the migration slice; no production live calls.
- TEST: run targeted pytest, lint/format, task docs validation, secret scan and quick CI.
- REVIEW: check future-optimal drift, Ponytail complexity, document drift and security/privacy.
- SHIP: commit/push and observe remote CI through outer delivery flow.

不得跳过 gate. If real external credentials are required, the task must stop at `外部连通验证待执行` instead of fabricating evidence.

# Simplest Path

Reuse the existing 0119/0120/0121 artifacts and add one bounded generator plus one wrapper. Do not introduce a new executor framework, new storage layer, external dependency or live integration.

Existence check: a separate all-category packet is needed because 0126 only covers production delivery live categories, while the remaining 100% infrastructure closure covers OTel, OIDC/SIEM, Vault/KMS, developer platform, certification and other external validation domains.

Selected ladder rung: project-native direct implementation using existing JSON contracts, scripts and local-ci pattern.

Skipped scope: real live execution, credential storage, third-party audit, external issue tracker, new provider logic, new report output.

Ceiling / upgrade path: when operators start submitting real evidence, this packet should feed proof-ref upload/attestation tooling or an external evidence portal.

Do-not-simplify: keep raw URL/secret rejection, packet gate blocked state, source hashes and non-claims.

Minimal runnable check: focused regression tests plus quick local CI artifact.

Complexity review owner: `auto-review` with document-drift, security/privacy and ponytail-complexity lenses.

# Split Strategy

| Node | Purpose | Depends On |
| --- | --- | --- |
| TP-01 | Confirm scope and upstream evidence chain | - |
| TP-02 | Add contract/script/wrapper | TP-01 |
| TP-03 | Fix command/env-var mismatches found during packet wiring | TP-02 |
| TP-04 | Wire local-ci, AGENTS and roadmap | TP-03 |
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

- Inputs: work queue JSON, proof-ref gate JSON, category runbooks JSON, optional expected commit.
- Outputs: `external-validation-operator-execution-packet.json`.
- External side effects: none.
- Secret handling: secret values are rejected; only variable names and placeholders are allowed.
- Evidence handling: packet includes source hashes and proof-ref bundle template; real proof refs remain operator-supplied later.

# Next Executable Leaves

- No remaining local leaves after TP-05 succeeds.
- TP-06 is handled by outer Git/GitHub delivery flow after final validation.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol

- Revert the 0127 commit if the packet wiring breaks quick CI or remote CI.
- Since no runtime service, database migration, secret or external side effect is introduced, rollback is Git-only.
- If generated artifact semantics are wrong but local-ci is green, follow-up with a new task and keep non-claims in place until corrected.
