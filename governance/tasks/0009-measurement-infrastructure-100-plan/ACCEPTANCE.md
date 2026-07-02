# Task-Level Acceptance
- 新增完整实现计划文档。
- 文档必须基于成熟基础设施官方资料做同构分析。
- 文档必须覆盖 100% 目标终态、架构、主线、波次、最小首批切片、验收清单、风险。
- 任务容器必须记录本次规划工作，而不是误导为已经实现 100%。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 计划文档存在 | `test -f docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| 官方资料覆盖 | `rg -n "Stripe|Twilio|Plaid|Kubernetes|Terraform|Temporal|OpenTelemetry|OpenAI" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| 实现主线覆盖 | `rg -n "IMP-01|IMP-12|100% 验收清单" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| 索引同步 | `rg -n "测算基础设施100%实现计划.md" docs/reference-materials/README.md` |
| 任务文档 | `validate_task_docs.py --phase closeout` |
| 任务树 | `validate_tasks_tree.py --phase auto` |
| whitespace | `git diff --check` |

# Review Gate
- 不得把计划项说成已实现。
- 不得声明外部生产连通已验证。
- 不得把 OpenAI Evals 等外部平台当成唯一固定依赖。
- 不得把未来能力混入默认综合八字。

# Runtime Verification Gate
- 本任务只验证文档和任务容器；不运行业务 CI。
- 后续 Wave 1 实现任务必须另跑 quick CI、API contract、schema tests。

# Ship Readiness
- 本任务完成后不自动提交；等待用户审阅。
- 若用户要求提交，必须先跑 `git diff --check` 和任务树校验。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 官方资料与 FateCat 同构关系写入计划文档 |
| TP-02 | 实现计划文档和 README 索引落盘 |
| TP-03 | 任务容器 closeout 可校验 |

# Anti-Goals
- 不实现业务代码
- 不得虚构证据
- 不得越权补全未确认信息
