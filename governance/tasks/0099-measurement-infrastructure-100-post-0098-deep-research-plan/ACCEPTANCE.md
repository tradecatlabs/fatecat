# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Deep research | `RESEARCH.md` cites official/fact-standard infra sources and maps each source to FateCat resources. |
| Complete implementation plan | Roadmap includes post-0098 resource maturity, execution waves, remaining tasks, and falsifiers. |
| Current-state honesty | 0098 local closeout is distinguished from external live completion. |
| No fake production readiness | All Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/multi-replica live items remain pending without real evidence. |
| Task package hygiene | `validate_task_docs.py --phase decompose` passes and no task placeholders remain. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Placeholder scan | `rg -n "\\{\\{" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | No output. |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan --phase decompose` | Pass. |
| Roadmap references | `rg -n "Post-0098|0099|外部连通验证待执行|0098 .*final" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan` | Expected references present. |

# Review Gate
- The plan must distinguish `passed`, `blocked`, `pending` and `in-progress`.
- The plan must not claim live production capability without live evidence.
- The plan must not create a second source of truth outside the main roadmap.
- The plan must not hide that external live evidence remains pending after 0098 local closeout.

# Runtime Verification Gate
- Not applicable: this planning task has no runtime behavior change.
- Required local verification is documentation validation and reference scan.

# Ship Readiness
- Ready to ship when docs validator passes and roadmap wording is internally consistent.
- This task does not require quick local-ci because it changes planning docs only.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Official/fact-standard source matrix is present in `RESEARCH.md`. |
| TP-01.02 | Each infrastructure source maps to a FateCat resource/gate. |
| TP-02.01 | Main roadmap and 0095/0098 task facts are reflected. |
| TP-02.02 | Dirty worktree and 0098 pending state are recorded. |
| TP-03.01 | Resource maturity matrix covers core infrastructure resources. |
| TP-03.02 | Execution waves, task tree and anti-forgery standards are present. |
| TP-04.01 | `RESEARCH.md`, task docs and main roadmap are updated. |
| TP-04.02 | Validator and placeholder/reference checks pass. |

# Anti-Goals
- Do not implement new runtime behavior in this planning task.
- Do not claim 0098 external live is complete because local closeout passed.
- Do not mark external live checks as passed without real external evidence.
- Do not create a second roadmap source of truth.
