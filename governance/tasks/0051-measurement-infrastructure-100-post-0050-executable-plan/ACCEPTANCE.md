# Task-Level Acceptance

0051 完成条件：主路线图必须包含 post-0050 的 100% 基础设施实现计划，明确当前完成面、剩余缺口、任务树、优先级和失败判定；任务包必须能通过文档校验。

# Validation Plan

| Check | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0051-measurement-infrastructure-100-post-0050-executable-plan --phase decompose` | pass |
| Task tree | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | pass |
| Diff hygiene | `git diff --check` | pass |

# Acceptance Criteria

- [x] 0050 完成状态被纳入路线图。
- [x] 0048 Bot live blocker 仍明确保留。
- [x] 路线图不再把 `MI-NEXT-02` 当成下一步待执行任务。
- [x] post-0050 任务树覆盖 durable runtime、control plane、developer platform、provider platform、evidence/eval、SRE、安全、多端同源和 audit package。
- [x] 失败判定明确禁止伪造外部证据。
- [x] 文档校验通过。

# Runtime Verification Gate

- 本任务只验证路线图和任务包结构。
- 不验证真实 Bot、OIDC、SIEM、监控平台或告警平台。
- 不验证 MI-NEXT-03 到 MI-NEXT-10 的业务实现。

# Ship Readiness

- 主路线图包含 post-0050 可执行实现计划。
- 0051 任务文档通过 validator。
- 任务索引包含 0051。
- 未把任何外部待验证项写成已完成。

# Task Package Acceptance

- TP-01.01 Done：当前 post-0050 状态已复核。
- TP-02.01 Done：外部 infra 同构资料已归纳。
- TP-03.01 Done：主路线图 `0.6` 已更新。
- TP-03.02 Done：0051 任务包和 INDEX 已更新。
- TP-04.01 Done：任务文档、任务树和 diff hygiene 均通过。

# Anti-Goals

- 不写业务代码。
- 不创建平行 roadmap。
- 不新增术数 capability。
- 不伪造外部 live evidence。
- 不把计划任务写成生产 100% 完成。

# Review Gate

- 计划不得宣称 FateCat 已 100%。
- 计划不得把外部连通项写成仓库内已验证。
- 计划不得鼓励绕过 capability/provider/evidence/evaluation 协议新增功能。
