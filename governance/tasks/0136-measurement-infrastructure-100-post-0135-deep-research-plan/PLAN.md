# Planning Summary

0136 refreshes the 100% measurement infrastructure plan after 0135. The current local/release chain is strong enough for planning: current release proof and current audit bundle for `4710659` pass, while certification, external validation closure, tracker issue evidence and independent audit remain blocked. Therefore the next phase is not another local dry-run bridge; it is closing real external evidence and hardening the platform around resource control, production operations, developer access and domain quality.

# Lifecycle Gates

不得跳过 gate。规划完成只代表 0136 文档切片完成，不代表生产 live、certification、third-party audit 或 100% 测算基础设施完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Scope is planning only; no live/prod execution | Done |
| PLAN | External source matrix and FateCat domains mapped | Done |
| BUILD | Task package and roadmap section written | Done |
| TEST | Task docs and no-overclaim checks | Done after validation |
| REVIEW | Future-optimal, ponytail and document-drift review | Done |
| SHIP | Commit/push only if separately requested | Not part of task |

# Simplest Path

1. Keep existing roadmap as truth source.
2. Append a post-0135 section instead of rewriting history.
3. Use current `/tmp` evidence to define what is really passed and what remains blocked.
4. Convert external infrastructure standards into FateCat resource domains and next executable tasks.
5. Do not add a new script, schema or service for a planning-only task.

# Split Strategy

| Node | Split Reason |
| --- | --- |
| TP-01 | Establish current release/audit/certification/rehearsal truth before planning. |
| TP-02 | Ground the plan in official infrastructure patterns, not intuition. |
| TP-03 | Translate source patterns into FateCat resource maturity gaps. |
| TP-04 | Produce executable task tree and wave order. |
| TP-05 | Land docs in task package and roadmap. |
| TP-06 | Validate that docs are complete and do not overclaim. |

# Execution Waves

| Wave | Leaves | Result |
| --- | --- | --- |
| W1 | TP-01, TP-02 | Current baseline and external research captured. |
| W2 | TP-03, TP-04 | Maturity matrix and implementation plan created. |
| W3 | TP-05 | Task package and roadmap landed. |
| W4 | TP-06 | Validation and no-overclaim review. |

# Runtime Workflow Contract

Allowed:

- Read Git state, task docs, contracts and `/tmp` evidence JSON.
- Use web/curl to inspect official infrastructure references.
- Edit task docs and roadmap.
- Run task-doc validation and text scans.

Forbidden:

- Real production live calls.
- Reading real secrets or `.env` values.
- Creating tracker issues.
- Triggering deployment, release or external audit.
- Modifying business code, API behavior, provider algorithms or CI workflows.

# Next Executable Leaves

No remaining planning leaves after validation.

Recommended next implementation sequence:

1. `0137 measurement-infrastructure-external-tracker-issue-creation-execution`: operator creates real tracker issues from 0131 package and submits redacted issue evidence bundle.
2. `0138 measurement-infrastructure-external-proof-ref-live-proof-execution`: execute 22 work-item runbooks and submit proof-ref/live proof bundles.
3. `0139 measurement-infrastructure-production-live-delivery-execution`: run production API/HF/Bot/webhook live evidence bundle with real credentials and endpoints.
4. `0140 measurement-infrastructure-independent-audit-result-intake`: ingest independent auditor result into third-party audit rehearsal/certification gate.
5. `0141 measurement-infrastructure-developer-public-platform-live`: close public developer portal, SDK/package, sandbox token and public docs smoke.
6. `0142 bazi-ziwei-professional-quality-corpus-expansion`: expand expert/anonymous corpus and report golden diff for core capabilities.

# Dependency Graph

```text
TP-01 -> TP-03
TP-02 -> TP-03
TP-03 -> TP-04 -> TP-05 -> TP-06
```

# Rollback Protocol
- Remove `governance/tasks/0136-measurement-infrastructure-100-post-0135-deep-research-plan/`.
- Remove the 0136 row from `governance/tasks/INDEX.md`.
- Remove the post-0135 section appended to `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
- Do not touch existing 0001-0135 task history or business code.

# Future-Optimal Task Contract

Target end state: FateCat is a resourceized measurement infrastructure: capabilities, providers, jobs, reports, evidence, datasets, evaluations, delivery surfaces, security controls, observability signals, release artifacts and audit handoff are discoverable, executable, observable, policy-gated and externally verifiable.
Real constraints: production live evidence requires real domains, tokens, IdP/SIEM/OTel/Vault/KMS/Postgres/webhook receiver, tracker permissions and third-party auditor authority.
Inertia constraints: existing local dry-run gates and historical roadmap sections cannot define 100%; they are inputs, not completion proof.
Wrong concept / wrong boundary: treating 100% as “more prediction modules” instead of platform infrastructure maturity.
Kill list: local dry-run as production proof, certification without external evidence, audit rehearsal without independent auditor result, planned capability execution, raw secret or user-data evidence.
Proof point: task package and roadmap define exact current evidence, maturity gaps, next tasks and no-overclaim gates.
Falsifier: any next task cannot be executed or validated because this plan lacks owner, evidence, dependency or gate.
Migration slice: planning-only post-0135 refresh prepares external closure tasks 0137+.
Rejected short-term patches: do not add another summary script, do not mark certification passed, do not hide external blockers, do not implement new divination modules in this infrastructure slice.
Future-optimal review owner: `auto-review` with future-optimal-drift, ponytail-complexity and document-drift lenses.

# Ponytail Task Contract

Existence check: 0135 changed the audit evidence baseline; a post-0135 plan is needed so next work targets real external closure instead of stale local bridge tasks.
Selected ladder rung: project-native documentation/task package; no new service, schema, dependency or script.
Skipped scope: production live execution, tracker issue creation, provider implementation, external account setup and code changes.
Ceiling / upgrade path: once real external evidence is available, convert this plan into closure execution tasks and certification proof refresh.
Do-not-simplify: release/audit/certification/external blockers must stay explicit.
Minimal runnable check: task-doc validator, placeholder scan, no-overclaim scan and current evidence JSON inspection.
Complexity review owner: `auto-review` ponytail-complexity.

# Document-Driven Task Contract

Operating model update: not needed; project positioning already states measurement infrastructure.
Toolchain model update: not needed; no new command or script is introduced.
Process update: not needed; this is a planning refresh.
Source-of-truth updates: updated roadmap and task index.
Local README/AGENTS impact: not needed; no architecture boundary changed.
Contract/catalog/schema impact: not needed; no schema changed.
ADR/Gate/module-context impact: not needed; no new gate implemented.
Documentation exemption reason: runtime behavior unchanged.
Validation evidence: task docs validation, placeholder scan, no-overclaim scan and current evidence JSON summary.
