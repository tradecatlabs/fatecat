# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Deep research | `RESEARCH.md` contains official/fact-standard sources with current version facts where visible. |
| Complete implementation plan | Roadmap includes post-0108 resource model, implementation waves, next task order and falsifiers. |
| Current-state honesty | Container success and Acceptance in_progress are recorded distinctly. |
| No fake production readiness | Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/multi-replica live remain pending without real evidence. |
| Task package hygiene | `validate_task_docs.py --phase decompose` passes and no task placeholders remain. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Placeholder scan | `rg -n "\\{\\{" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | No output. |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan --phase decompose` | Pass. |
| Roadmap references | `rg -n "Post-0108|0109|W0|current-release-proof|OpenAPI 3.2.0|AsyncAPI 3.1.0|CycloneDX specification 当前版本为 1.7" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan` | Expected references present. |
| Git/CI evidence | `git status --short --branch && gh run list --commit $(git rev-parse HEAD) --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt` | Scoped docs diff; current run list result recorded honestly. |

# Review Gate
- The plan must distinguish `success`, `in_progress`, `pending`, `blocked` and `external live required`.
- The plan must not claim live production capability without live evidence.
- The plan must not create a second source of truth outside the main roadmap.
- The plan must not hide 0108 task index/status drift.

# Runtime Verification Gate
Not applicable: this planning task has no runtime behavior change. Required verification is documentation validation, placeholder scan, reference scan and GitHub run status snapshot.

# Ship Readiness
Ready to ship when docs validator passes, roadmap wording is internally consistent, and worktree diff is scoped to docs/task planning files.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Official/fact-standard source matrix is present in `RESEARCH.md`. |
| TP-01.02 | Git/gh/task index snapshot is present and honest. |
| TP-02.01 | Resource gap matrix covers release, capability, provider, runtime, evidence, evaluation, security, observability, delivery, developer and audit. |
| TP-02.02 | Anti-forgery standards cover in_progress, dry-run, staged gate, local-ci and external live. |
| TP-03.01 | W0-W9 implementation waves are present. |
| TP-03.02 | Next P0 is W0 release truth finalizer. |
| TP-04.01 | `RESEARCH.md`, task docs and main roadmap are updated. |
| TP-04.02 | Validator and placeholder/reference checks pass. |

# Anti-Goals
- 不得修改业务代码、运行脚本、workflow 触发行为或生产配置。
- 不得虚构远端 CI、release artifact、Bot live 或外部平台证据。
- 不得越权补全未确认信息。
