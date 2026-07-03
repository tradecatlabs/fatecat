# Task-Level Acceptance
- `RESEARCH.md` captures the post-0117 infrastructure research and maps it to FateCat resource domains.
- The main roadmap contains a post-0117 section with complete implementation waves and next tasks.
- The task package is complete and validates.
- No statement claims external live, production 100%, third-party audit, OIDC/SIEM/OTel/Vault/KMS/Bot/API/HF evidence is complete.

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Research exists | `test -s governance/tasks/0118-measurement-infrastructure-100-post-0117-deep-research-plan/RESEARCH.md` | pass |
| Roadmap updated | `rg -n "Post-0117|MI-100\\.A|External Validation Closure" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | finds new section |
| No fake live wording | `rg -n "外部连通验证待执行|不能伪造|canClaim100Percent=false" governance/tasks/0118-measurement-infrastructure-100-post-0117-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | finds non-claim language |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0118-measurement-infrastructure-100-post-0117-deep-research-plan --phase closeout` | pass |
| Combined quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-post-0117-infra-plan-final` | passed; 300 focused regression tests passed |

# Review Gate
- Confirm the plan is not a generic wish list: each domain has concrete next action and evidence.
- Confirm the plan does not add a parallel roadmap truth source.
- Confirm external systems remain pending unless evidence exists.

# Runtime Verification Gate
- No runtime live verification is in scope.
- Any live task derived from this plan must use real credentials and redacted evidence.

# Ship Readiness
- Required docs validate.
- Worktree can be committed together with 0117 closure profile expansion.

# Task Package Acceptance
- `README.md`, `CONTEXT.md`, `PLAN.md`, `ACCEPTANCE.md`, `ACCEPTANCE_CHECKLIST.md`, `TODO.md`, `STATUS.md` exist and contain no placeholders.
- `RESEARCH.md` is the handoff artifact for the next execution wave.

# Anti-Goals
- No new production claim.
- No external credential use.
- No business-code implementation.
- No "feature count equals infrastructure" framing.
