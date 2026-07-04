# Task-Level Acceptance

- `RESEARCH.md` records official infrastructure sources and maps them to FateCat implementation domains.
- `PLAN.md` defines post-0135 implementation waves and next executable tasks.
- Main roadmap has a post-0135 section with current evidence baseline, resource maturity matrix and no-overclaim rules.
- `TODO.md` and `STATUS.md` show all planning leaves complete.
- Task docs validate in `decompose` or stricter phase.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0136-measurement-infrastructure-100-post-0135-deep-research-plan --phase decompose` | pass |
| Placeholder scan | `rg "\\{\\{" governance/tasks/0136-measurement-infrastructure-100-post-0135-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | no result |
| No-overclaim scan | Targeted review of the 0136 task package and roadmap post-0135 section | only conditional gate language is allowed; no current completion claim |
| Current evidence sanity | JSON inspection of `/tmp/fatecat-current-release-audit-chain-refresh-4710659` | release/audit passed, certification/rehearsal/external closure blocked as documented |

# Review Gate

- Future-optimal drift: plan must describe the correct end state as a resourceized measurement infrastructure, not a pile of extra metaphysics modules.
- Ponytail complexity: this task must not add scripts, schemas, services or code when planning docs are enough.
- Document drift: roadmap, task index and task docs must agree.
- Security/privacy: no secret, DSN, webhook secret, token, raw production URL, user report body or birth data may appear.

# Runtime Verification Gate

No runtime service is changed. Runtime verification for this task is limited to current evidence JSON inspection and task/document validation.

# Ship Readiness

- Planning docs complete.
- Validators pass.
- No business code changed.
- External blockers remain explicit.
- Commit/push is not part of this task unless a separate git delivery request is issued.

# Task Package Acceptance

| Node | Acceptance |
| --- | --- |
| TP-01 | Current evidence baseline is recorded with exact paths and gate status. |
| TP-02 | Official source matrix covers platform engineering, API/events, control plane, SRE, security, supply chain, developer platform and durable execution. |
| TP-03 | Resource maturity matrix distinguishes local baseline, production gap and external blocker. |
| TP-04 | Implementation task tree gives concrete next tasks and wave order. |
| TP-05 | Task package and roadmap are updated. |
| TP-06 | Validation and no-overclaim review pass. |

# Anti-Goals
- 不得修改业务代码、部署代码或 CI workflow。
- 不得虚构证据
- 不得越权补全未确认信息
- 不得声明 FateCat 已经 100% 测算基础设施。
- 不得把 third-party audit rehearsal `status=passed` 误写成 `rehearsalGate=passed`。
