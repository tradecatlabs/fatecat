# Task-Level Acceptance
- 0077 必须是 planning-only 任务，不能改业务代码。
- `RESEARCH.md` 必须列出外部一手资料和 FateCat 同构映射。
- 主路线图必须追加 post-0076 最新执行计划，明确下一步可执行任务和外部阻断项。
- 计划必须区分“本地可执行”和“外部连通验证待执行”。
- 不能把 0076 public webhook live smoke gate 写成真实 live passed、production ready、exactly-once 或长期多副本 ready。

# Validation Plan
| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| 任务文档结构 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0077-measurement-infrastructure-100-post-0076-deep-research-plan --phase decompose` | exit 0 |
| 占位符检查 | `rg "\\{\\{" governance/tasks/0077-measurement-infrastructure-100-post-0076-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 无结果 |
| 任务索引 | `rg "0077" governance/tasks/INDEX.md` | 指向 `measurement-infrastructure-100-post-0076-deep-research-plan` |
| 外部证据口径 | 人工复核 `RESEARCH.md` 与主路线图 `0.10` | 外部 token/endpoint/平台均标记待执行 |

# Review Gate
- document-drift: 主路线图、任务索引和 0077 文档必须一致。
- future-optimal-drift: 计划必须服务“测算基础设施”终态，不能退化成堆功能模块。
- ponytail-complexity: 不新增平行 roadmap、runtime、contract 或抽象。
- evidence-integrity: 所有已完成/未完成结论必须有文件、命令或外部资料链接支持。

# Runtime Verification Gate
本任务不执行 runtime live gate。后续实现任务必须分别补齐：
- Postgres worker heartbeat/polling smoke。
- 公网 webhook live passed evidence。
- External secret provider dry-run/live evidence。
- OTel backend/SLO evidence。
- OIDC/SIEM/retention live evidence。
- Bot live smoke。

# Ship Readiness
Ready for commit after:
- task docs validator 通过；
- 主路线图 0.10 存在；
- 无模板占位符；
- Git diff 仅包含规划文档与任务索引；
- 未声明任何外部 live 已完成。

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 当前 Git/worktree 和 0076 closeout facts 已记录。 |
| TP-01.02 | 既有路线图和 runtime backend contract 已复核。 |
| TP-02.01 | 官方资料 source matrix 已写入 `RESEARCH.md`。 |
| TP-02.02 | FateCat 同构能力域已归纳。 |
| TP-03.01 | 100% 完成门禁和失败判定已写清。 |
| TP-03.02 | 后续任务顺序可以直接转成 0078+ 任务包。 |
| TP-03.03 | 外部连通验证待执行项未被伪造成完成。 |
| TP-04.01 | 主路线图追加最新 0.10 章节。 |
| TP-04.02 | 0077 任务目录无占位符并包含 `RESEARCH.md`。 |
| TP-04.03 | 校验命令通过。 |

# Anti-Goals
- 不得修改业务代码。
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把本地 dry-run 写成外部 live。
