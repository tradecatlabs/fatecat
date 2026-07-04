# Planning Summary

0141 refreshes the complete 100% measurement infrastructure implementation plan after 0140. The strict conclusion is unchanged: FateCat has a strong local control plane and audit rehearsal chain, but cannot claim 100% until external live evidence, public developer platform evidence, core domain quality evidence and independent audit closure are all attached to the same release commit.

# Lifecycle Gates

不得跳过 gate。0141 完成只代表 post-0140 规划文档切片完成，不代表生产 live、certification、third-party audit 或 100% 测算基础设施完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Scope limited to research and planning; no production/live execution | Done |
| PLAN | External infrastructure source matrix mapped to FateCat resources | Done |
| BUILD | `RESEARCH.md`, task docs and roadmap section written | Done |
| TEST | Task docs validator and no-overclaim scans pass | Done |
| REVIEW | Future-optimal, Ponytail and document-drift review recorded | Done |
| SHIP | Commit/push only if separately requested | Not part of this task |

# Simplest Path

1. Reuse the existing 100% roadmap as the main truth source.
2. Add a post-0140 section instead of rewriting historical plan sections.
3. Keep detailed source matrix and task tree inside this task package.
4. Separate local executable work from external operator work.
5. Validate that no local planning artifact claims production completion.

# Split Strategy

| Node | Split Reason |
| --- | --- |
| TP-01 | Current evidence must be stable before any new plan is credible. |
| TP-02 | External infrastructure patterns prevent the plan from becoming a feature wishlist. |
| TP-03 | 100% needs an admission model, not only a checklist. |
| TP-04 | Future execution needs a task tree with dependencies and blockers. |
| TP-05 | Roadmap and task package must agree. |
| TP-06 | Planning closeout must prove no placeholder and no overclaim remains. |

# Execution Waves

| Wave | Leaves | Result |
| --- | --- | --- |
| W1 | TP-01, TP-02 | Current baseline and external research captured. |
| W2 | TP-03, TP-04 | Admission model, maturity matrix and implementation tree written. |
| W3 | TP-05 | Task package and roadmap updated. |
| W4 | TP-06 | Validation and no-overclaim review. |

# Runtime Workflow Contract

Allowed:

- Read Git state, roadmap, tasks, contracts and public official infrastructure references.
- Edit task docs and roadmap.
- Run task document validation and text scans.

Forbidden:

- Production deployment, live smoke execution, tracker issue mutation, proof-ref/live proof submission.
- Reading or storing real secrets, raw URLs, webhook secrets, DSNs, production logs, report bodies or user input.
- Modifying business code, provider algorithms, API behavior, CI workflow or runtime scripts.

# Next Executable Leaves

After 0141 validation, the next practical leaves are:

1. `0138` external proof/live execution remains blocked until operator credentials and proof bundles exist.
2. `0142` core bazi/ziwei professional quality corpus expansion is the best local next slice.
3. `0143` production live delivery execution should run when real API/HF/Bot/webhook credentials are available.
4. `0144` developer public platform live should run when public portal/SDK/sandbox token issuer can be validated.
5. `0145` SRE/security live evidence should run when OTel/OIDC/SIEM/Vault/KMS environments exist.

# Dependency Graph

```text
TP-01 -> TP-03
TP-02 -> TP-03
TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol

- Remove `governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh/`.
- Remove the 0141 row from `governance/tasks/INDEX.md`.
- Remove the post-0140 section appended to `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
- Do not touch existing 0001-0140 task history or runtime code.

# Future-Optimal Task Contract

Target end state: FateCat is a measurement infrastructure platform where every calculation capability, provider, job, report, evidence item, dataset, evaluation run, delivery surface, security control, observability signal, release artifact and audit result is discoverable, versioned, policy-gated, externally verifiable and reproducible.

Real constraints: external live proof requires real domains, tokens, IdP/SIEM/OTel/Vault/KMS/Postgres/webhook receiver, developer portal and third-party auditor authority.

Inertia constraints: historical local gates are valuable evidence but cannot define 100%; adding more divination modules does not solve infrastructure maturity.

Wrong concept / wrong boundary: treating 100% as "more prediction systems" instead of "resourceized, observable, secure, auditable platform maturity".

Kill list: dry-run as live proof, rehearsal as audit completion, planned capability execution, raw secret evidence, report body evidence, live proof without proof-ref binding.

Proof point: `RESEARCH.md` defines admission levels, resource gaps, full task tree and explicit non-claim rules.

Falsifier: a future implementer cannot determine next task owner, evidence, blocker or gate from this plan.

Migration slice: planning-only post-0140 refresh prepares 0142+ local quality work and external closure work.

Rejected short-term patches: do not add another runtime script, do not mark certification passed, do not hide external blockers, do not implement new divination modules in this planning task.

# Ponytail Task Contract

Existence check: 0140 changed the audit chain; a post-0140 plan is needed so the next work targets true remaining blockers instead of stale post-0135 ordering.

Selected ladder rung: project-native docs/task package and roadmap section. No new code object is needed.

Skipped scope: production live execution, API or provider implementation, external account setup, CI changes and runtime gates.

Ceiling / upgrade path: once real external evidence exists, turn the plan into execution tasks and certification proof refresh.

Do-not-simplify: external blockers, domain quality gaps, developer platform gaps and audit closure must stay explicit.

Minimal runnable check: task-doc validator, placeholder scan and no-overclaim scan.

# Document-Driven Task Contract

Operating model update: not required; project positioning already states measurement infrastructure.

Toolchain model update: not required; no new command or script is introduced.

Process update: not required; this is a plan refresh.

Source-of-truth updates: task package, task index and main 100% roadmap.

Local README/AGENTS impact: not required; no architecture boundary changed.

Contract/catalog/schema impact: not required; no schema changed.

ADR/Gate/module-context impact: not required; no new gate implemented.

Documentation exemption reason: runtime behavior unchanged.

Validation evidence: task docs validation, placeholder scan and no-overclaim scan.
