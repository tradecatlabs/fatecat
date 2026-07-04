# Repo Evidence

| Fact | Evidence |
| --- | --- |
| Current branch | `main` |
| Current baseline commit before this task | `8b59d99 docs: close production live delivery task` |
| 0124 status | `governance/tasks/0124-measurement-infrastructure-production-live-delivery-evidence-bundle/STATUS.md` says `Overall Status: Done`. |
| 0124 remote CI | Acceptance `28694370390` and Container `28694370250` passed for commit `8b59d99`. |
| Live state | Production API/HF/Bot/public webhook/multi-surface live evidence remains external connectivity pending. |

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No production credentials in repo | Plan only; no live request execution. |
| No raw endpoints/secrets in evidence | Use proof-ref and redacted artifact language only. |
| Main roadmap is truth source | Append section `6.20`; do not create a parallel roadmap. |
| 0124 is a completed local slice | Record it as completed but keep production live pending. |

# Change Boundary

In scope:

- Add task package `0125`.
- Update `governance/tasks/INDEX.md`.
- Update main roadmap with post-0124 live readiness section.

Out of scope:

- Production API/HF/Bot/webhook calls.
- Business code, runtime code or delivery code changes.
- New external dependencies.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Live pending is misread as completed | Use `外部连通验证待执行` and explicit non-claim language. |
| Plan drifts from current 0124 facts | Reference final commit and remote CI run IDs in task context/status. |
| Too much plan, no execution | Plan produces exact next local task and exact external live closure path. |

# Assumptions and Falsification

| Assumption | Falsifier | Response |
| --- | --- | --- |
| No real external credentials are available in this worktree. | User supplies production token/URL/DSN/webhook receiver and authorizes live run. | Skip operator packet and execute corresponding live workstream. |
| 0124 is the correct bridge from live summaries to 0123. | A new live summary type cannot be represented by 0124 schema. | Add a new adapter category without weakening 0123 live proof gate. |
| Main roadmap remains the living plan. | Governance moves roadmap truth source elsewhere. | Update references and task package map. |

# Critical Ambiguities

- Real production credential availability is unknown.
- Third-party audit operator availability is unknown.
- Public developer portal and SDK publication channel are not yet selected.

# Debug Evidence Contract

- 调试模式: `Optional`

This is a planning task, not a bugfix. If validation fails, record failing command and fix the task package format before closeout.

# Task Package Context Map

| Path | Role |
| --- | --- |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Main living plan and task tree truth source. |
| `governance/tasks/0124-measurement-infrastructure-production-live-delivery-evidence-bundle/` | Upstream completed task evidence. |
| `contracts/fate/audit/production-live-delivery-evidence-bundle.json` | 0124 assembler contract. |
| `scripts/production-live-delivery-evidence-bundle.py` | 0124 live summary adapter. |
| `scripts/external-validation-live-proof-gate.py` | Authoritative live proof verifier. |
