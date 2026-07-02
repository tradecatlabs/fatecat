# Task-Level Acceptance
- 100% 路线图必须包含外部基础设施官方资料同构映射。
- 路线图必须反映当前 0009-0044 真实状态，不能把 pending 3 项写成完成。
- 路线图必须给出后续可执行任务顺序，且每项有验收证据。
- 任务包必须通过 auto-tasks closeout 校验。

# Validation Plan
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0045-measurement-infrastructure-100-final-plan-refresh --phase closeout`
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto`
- `git diff --check`

# Review Gate
- 检查是否存在“已完成/已通过”但没有命令、文件或外部链接证据的表述。
- 检查是否把未来功能、外部连通、真实 token、远端 CI 误写为仓库内已完成。
- 检查 roadmap 是否仍保持单一真相源，而不是新增冲突文档。

# Runtime Verification Gate
不需要运行服务。本任务只更新规划文档。

# Ship Readiness
任务 closeout 后可以作为后续 0046+ 实施依据；不代表 FateCat 已达到 100% 生产基础设施。

# Task Package Acceptance
- TP-01.01：官方资料链接已写入 roadmap。
- TP-02.01：当前 live release gate 剩余缺口已写入 roadmap。
- TP-03.01：后续 0046+ 任务树已写入 roadmap。
- TP-04.01：校验命令通过。

# Anti-Goals
- 不得修改业务代码
- 不得虚构证据
- 不得越权补全未确认信息
