# Task-Level Acceptance
| 验收项 | 命令 / 证据 | 通过标准 |
| --- | --- | --- |
| 任务文档无占位符 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan --phase decompose` | `placeholders=[]` 且 exit 0。 |
| 任务文档结构合规 | 同上 | exit 0。 |
| 主路线图已更新 | `rg -n "Post-0094|Wave A|Next-01" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 找到 post-0094 计划段。 |
| 调研结果已落盘 | `rg -n "外部基础设施同构资料|100% 资源成熟度矩阵|Post-0094 完整实现计划" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md` | 找到核心段落。 |
| 不伪造外部 live | `rg -n "外部连通验证待执行|不能伪造|不能由 dry-run 替代" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md` | 外部边界明确。 |

# Validation Plan
1. 运行 `validate_task_docs.py --phase decompose`。
2. 确认 validator 返回 `placeholders=[]`。
3. 运行路线图和 RESEARCH 引用检查。
4. 运行 `git diff --stat` 复核只改文档/任务计划。

# Review Gate
- 不得把 0093/0094 之后未做的任务写成完成。
- 不得把真实 Bot/API/OIDC/SIEM/OTel/Vault/KMS/multi-replica live 写成已通过。
- 不得创建新的路线图真相源。
- 不得修改业务代码或测试门禁。

# Runtime Verification Gate
- Not applicable：本任务没有 runtime 行为变更。
- 文档门禁必须通过。

# Ship Readiness
- 任务文档合规。
- 主路线图可作为后续任务输入。
- 下一步实现切片明确为 Wave A 的 `八字/紫微 corpus/report diff expansion`。

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 当前 git、路线图、0093/0094 和 core quality 资产已记录。 |
| TP-01.02 | 外部一手资料矩阵已写入 RESEARCH。 |
| TP-02.01 | 资源成熟度矩阵覆盖核心基础设施域。 |
| TP-02.02 | 执行波次区分本地可执行与外部 live。 |
| TP-03.01 | 主路线图追加 post-0094 计划。 |
| TP-03.02 | 0095 task docs 和 RESEARCH 无占位符。 |
| TP-04.01 | task docs 校验通过。 |

# Anti-Goals
- 不得修改 `domains/`、`scripts/`、`contracts/` 的行为。
- 不得虚构证据。
- 不得把计划当成交付完成证明。
