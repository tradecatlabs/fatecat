# Task-Level Acceptance
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 必须新增 post-0142/post-0143 深度调研刷新。
- roadmap 必须明确：0142 本地质量证据已完成，但 22 个 external validation work items 仍 pending。
- roadmap 必须包含成熟基础设施官方资料映射和后续任务树。
- `governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan/` 必须无模板占位符。
- 0143 只能声明 planning closeout，不得声明外部 live、第三方审计或 100% certification 完成。

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan --phase closeout` | pass |
| Placeholder scan | `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | no matches |
| Roadmap keywords | `rg -n "Post-0142|0144|0145|0146|0147|0148|0149|external proof/live|developer public platform|SRE/security" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | matches |
| Git diff check | `git diff --stat` | docs/task package only |

# Review Gate
Review must confirm:
- planning-only scope is clear.
- official references are recorded as URLs.
- external pending state is not softened or hidden.
- next tasks are actionable and ordered by blocker dependency.

# Runtime Verification Gate
Runtime verification is not applicable for this planning task. Existing runtime evidence is only consumed as context:
- local CI `/tmp/fatecat-local-ci-20260704233925` passed.
- external proof/live gates remain blocked with zero accepted proof/live evidence.

# Ship Readiness
Planning package is shippable after validator and placeholder scan pass. Product 100% ship gate remains blocked until external proof/live, live surfaces, SRE/security, runtime/event, human review, release proof and audit certification are all accepted.

# Task Package Acceptance
| TP | Acceptance |
| --- | --- |
| TP-01 | Current evidence table records remote CI, local CI and external pending counts. |
| TP-02 | Official source mapping covers platform engineering, API, async/event, control plane, provider, durable runtime, observability, SRE, security and supply chain. |
| TP-03 | Roadmap has post-0142/post-0143 section with next task queue. |
| TP-04 | Task package validates and no placeholders remain. |

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
