# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Deep research | `RESEARCH.md` contains official/fact-standard sources with current version facts where visible. |
| Complete implementation plan | Roadmap includes post-0105 resource maturity, execution waves, next task order and falsifiers. |
| Current-state honesty | Current HEAD remote CI absence is recorded as missing/pending, not passed. |
| No fake production readiness | Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/multi-replica live remain pending without real evidence. |
| Task package hygiene | `validate_task_docs.py --phase decompose` passes and no task placeholders remain. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Placeholder scan | `rg -n "\\{\\{" governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | No output. |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan --phase decompose` | Pass. |
| Roadmap references | `rg -n "Post-0105|0106|current remote CI|OpenAPI 3.2.0|AsyncAPI 3.1.0|外部连通验证待执行" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan` | Expected references present. |
| Git/CI evidence | `git status --short --branch && gh run list --commit HEAD --limit 10 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt` | Clean or scoped docs diff; current run list result recorded honestly. |

# Review Gate
- The plan must distinguish `passed`, `blocked`, `pending`, `missing` and `external live required`.
- The plan must not claim live production capability without live evidence.
- The plan must not create a second source of truth outside the main roadmap.
- The plan must not hide that workflows are manual and current HEAD has no visible Actions run.

# Runtime Verification Gate
Not applicable: this planning task has no runtime behavior change. Required verification is documentation validation, placeholder scan and reference scan.

# Ship Readiness
Ready to ship when docs validator passes, roadmap wording is internally consistent, and worktree diff is scoped to docs/task planning files.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Official/fact-standard source matrix is present in `RESEARCH.md`. |
| TP-01.02 | Each source maps to a FateCat resource/gate or is explicitly scoped out. |
| TP-02.01 | Main roadmap and 0104/0105 task facts are reflected. |
| TP-02.02 | Remote CI absence for current HEAD is recorded as missing/pending. |
| TP-03.01 | Resource maturity matrix covers release, evaluation, evidence, runtime, security, observability, delivery and audit. |
| TP-03.02 | Execution waves, next tasks and anti-forgery standards are present. |
| TP-04.01 | `RESEARCH.md`, task docs and main roadmap are updated. |
| TP-04.02 | Validator and placeholder/reference checks pass. |

# Anti-Goals
- 不得修改业务代码、运行脚本、workflow 触发行为或生产配置
- 不得虚构证据
- 不得越权补全未确认信息
