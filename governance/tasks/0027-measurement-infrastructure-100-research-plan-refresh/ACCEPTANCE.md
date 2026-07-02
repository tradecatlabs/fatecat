# Task-Level Acceptance
- 主路线图必须引用可复核的官方基础设施资料。
- 主路线图必须区分本地 worktree 已落地、仍待实现、外部连通验证待执行。
- 主路线图必须给出 D0-D10 基础设施域、剩余任务树、下一批任务和总验收清单。
- 任务包必须无占位符，能够通过 auto-tasks closeout 验证。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 任务文档 closeout | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh --phase closeout` |
| 全任务树 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` |
| 占位符扫描 | `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| 空白检查 | `git diff --check -- docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh governance/tasks/INDEX.md` |

# Review Gate
- 检查是否误称当前 dirty worktree 已远端验证。
- 检查是否把外部 live smoke 写成已完成。
- 检查是否把新增术数功能堆叠误当成基础设施主线。

# Runtime Verification Gate
- 本任务不启动服务；只做文档和任务包验证。
- validator 必须通过。

# Ship Readiness
- 本任务可关闭为计划交付完成。
- 后续实现必须另开任务，不得把本任务当作功能实现完成证据。

# Task Package Acceptance
| Item | Criteria | Evidence |
| --- | --- | --- |
| 外部调研矩阵 | 至少覆盖 API、workflow、catalog、controller、provider、observability、SRE、supply chain、security、ML/eval | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 第 1 节 |
| 当前事实盘点 | 明确本地已落地与未完成生产化事项 | 同文档第 3 节 |
| 100% 验收域 | D0-D10 每个域有目标、必须完成、完成证据 | 同文档第 4 节 |
| 剩余任务树 | MI-100 任务树能继续拆成 `0028+` | 同文档第 5、6 节 |
| 证据口径 | 不伪造远端 CI、生产 API、Bot、OIDC/SIEM、SBOM 等 | 同文档第 8 节 |

# Anti-Goals
- 不实现业务代码。
- 不提交、不推送。
- 不伪造远端 CI 或生产 live smoke。
- 不把后续任务写成已完成。
