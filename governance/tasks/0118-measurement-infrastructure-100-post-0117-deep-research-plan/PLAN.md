# Planning Summary

0118 refreshes the 100% measurement infrastructure implementation plan after 0117. The important new fact is that external pending items are no longer just scattered text: 0116 created closure plans and 0117 made routing mostly actionable. The next implementation plan must therefore shift from "find pending items" to "close resource domains with evidence".

# Lifecycle Gates
不得跳过 gate；规划完成不等于生产完成。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | Confirm post-0117 objective and non-live boundary | Done |
| PLAN | Map official infra patterns to FateCat resource domains | Done |
| BUILD | Write research report, roadmap section and task package | Done |
| TEST | Validate task docs and text evidence | Pending |
| REVIEW | Confirm no fake 100% or live passed claim | Done |
| SHIP | Commit/push handled by version-control step | Pending |

# Simplest Path
1. Reuse the existing roadmap as truth source.
2. Summarize official infrastructure patterns only where they change FateCat implementation decisions.
3. Define resource-domain workstreams with next tasks and evidence gates.
4. Keep all external live domains blocked until real proof exists.

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | Establish current repo and 0117 closure evidence baseline. |
| TP-02 | Research external infrastructure patterns and versions. |
| TP-03 | Convert research into a post-0117 task tree. |
| TP-04 | Update roadmap/task docs and validate package. |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `git status`, web research, `apply_patch`, task-doc validator.
- Forbidden actions: live external validation, secret access, branch switch, destructive git, production deployment.
- Evidence: official source URLs, roadmap diff, task docs validator, local search checks.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | No remaining executable leaves after validation. |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Remove `governance/tasks/0118-measurement-infrastructure-100-post-0117-deep-research-plan/`.
- Remove the 0118 row from `governance/tasks/INDEX.md`.
- Remove the post-0117 roadmap section from `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.

# Future-Optimal Task Contract
Target end state: FateCat 100% is a resourceized measurement infrastructure with control plane, runtime plane, event plane, quality/eval plane, developer platform, SRE, security, release proof and audit certification.
Real constraints: External live proof requires real tokens, domains, IdP/SIEM/OTel/Vault/KMS/Postgres/webhook receiver and third-party audit authority.
Inertia constraints: Existing long roadmap sections and old MI-NEXT labels cannot prevent a cleaner post-0117 closure-domain task tree.
Wrong concept / wrong boundary: Treating 100% as "more divination modules" instead of infrastructure maturity.
Kill list: Fake live claims, local dry-run as production proof, scattered external TODOs without owner.
Proof point: `RESEARCH.md` and roadmap section define owner/evidence/blocker per domain.
Falsifier: Any domain lacks a concrete next task or evidence gate.
Migration slice: Planning-only slice prepares the next executable P0 tasks.
Rejected short-term patches: Do not add feature modules, do not write "100% done", do not replace live proof with docs.
Future-optimal review owner: `auto-review` with document-drift and future-optimal-drift lenses.

# Ponytail Task Contract
Existence check: 0117 changed the closure state enough that the 100% plan must be refreshed; otherwise next work will chase stale tasks.
Selected ladder rung: Project-native documentation and task package, no new framework or service.
Skipped scope: Production live execution, new capability implementation, external account setup.
Ceiling / upgrade path: Once external systems are provided, convert this plan into live closure execution tasks rather than more planning.
Do-not-simplify: External evidence, security/privacy, release proof and audit gates cannot be removed.
Minimal runnable check: Task docs validator plus roadmap/content grep.
Complexity review owner: `auto-review` ponytail-complexity.

# Document-Driven Task Contract
Operating model update: not needed; positioning already in README/SKILL and requirement docs.
Toolchain model update: not needed; no new command or script.
Process update: not needed; this is a planning refresh.
Source-of-truth updates: updated roadmap and task index.
Local README/AGENTS impact: not needed; no architecture boundary changed.
Contract/catalog/schema impact: not needed; no schema changed.
ADR/Gate/module-context impact: not needed; no new decision gate implemented.
Documentation exemption reason: code/runtime behavior unchanged.
Validation evidence: task docs validator and grep checks.
