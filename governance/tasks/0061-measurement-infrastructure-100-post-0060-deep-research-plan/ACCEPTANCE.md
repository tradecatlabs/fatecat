# Task-Level Acceptance

- 0061 任务包无模板占位符。
- `RESEARCH.md` 覆盖成熟基础设施一手资料、FateCat 映射、当前完成面、剩余缺口和后续任务树。
- roadmap 增加 post-0060 深度调研实现蓝图。
- 后续任务按可执行顺序列出，并明确每项不可伪造的验收证据。
- 文档明确 100% 是基础设施成熟度，不是预测准确率。
- 文档明确真实 Bot、webhook、OIDC、SIEM、OTel backend、Vault/KMS、审计等外部项仍需外部连通验证。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0061-measurement-infrastructure-100-post-0060-deep-research-plan --phase decompose` | pass |
| task tree | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown` | pass |
| placeholder scan | `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0061-measurement-infrastructure-100-post-0060-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | no matches |
| roadmap keywords | `rg -n "Post-0060 深度调研|0061|external backend|AsyncAPI|CloudEvents|OTel|OIDC|AuditHandoff" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0061-measurement-infrastructure-100-post-0060-deep-research-plan` | matches |
| git status | `git status --short --branch` | only intended docs/task files changed before commit |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | 当前事实来自 git、roadmap、任务索引和 0060 证据，不脑补已完成项。 |
| 完整性 | 覆盖 API、事件、durable runtime、control plane、provider、eval、observability、security、developer platform、release、audit。 |
| 可执行性 | 后续任务可拆成 0062 起的单切片，不是空泛口号。 |
| 风险边界 | 所有外部依赖都标注外部连通验证待执行。 |
| 不夸大 | 不把计划、contract 或本地 baseline 写成生产 100%。 |

# Runtime Verification Gate

- 本地可验证：任务文档结构、占位符清理、roadmap/INDEX 同步。
- 外部连通验证待执行：Bot live、公网 webhook、external backend、外部 Vault/KMS、OIDC/IdP、SIEM、OTel backend、第三方审计。

# Ship Readiness

- TODO 全部勾选。
- STATUS 全节点 Done。
- 验证命令写入 STATUS Recent Evidence。
- 如果用户要求提交推送，交给 `auto-github` 读取其规则后执行。

# Task Package Acceptance

- 任务目录包含 README、CONTEXT、PLAN、ACCEPTANCE、ACCEPTANCE_CHECKLIST、TODO、STATUS、RESEARCH。
- `INDEX.md` 包含 0061 行。
- roadmap 包含 0061 post-0060 深度调研蓝图。
- 任务文档可由 `validate_task_docs.py --phase decompose` 复核。

# Anti-Goals

- 不得实现业务代码。
- 不得声明 external backend、生产分布式 worker、真实公网 webhook、外部 Vault/KMS、OIDC、SIEM、OTel backend 或第三方审计已完成。
- 不得把 100% 写成预测命中率。
