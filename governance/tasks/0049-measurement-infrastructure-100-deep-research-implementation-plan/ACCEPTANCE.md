# Task-Level Acceptance

本任务完成条件是：主路线图新增一套可复核的 100% 测算基础设施实现计划补强，且明确区分已完成、本地 baseline、外部连通待验证和后续实现。

# Validation Plan

| Check | Command | Expected |
| --- | --- | --- |
| Markdown whitespace | `git diff --check` | success |
| Task docs validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0049-measurement-infrastructure-100-deep-research-implementation-plan --phase decompose` | success |
| Task tree validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | success |

# Acceptance Criteria

- [x] 外部基础设施资料均使用一手/官方资料链接。
- [x] 已把资料映射为 FateCat resource model。
- [x] 已给出实现波次和下一步执行顺序。
- [x] 已明确 100% 完成判定。
- [x] 未把 0048 Bot live、registry attestation、OIDC/SIEM、监控告警写成已完成。
- [x] 本任务文档校验通过。

# Review Gate

- 不得伪造外部平台验证。
- 不得把计划文档替代为生产验收。
- 不得新增与主路线图竞争的平行事实源。

# Runtime Verification Gate

- 校验必须来自真实命令输出。
- `git diff --check` 必须通过。
- `validate_task_docs.py` 必须通过。
- `validate_tasks_tree.py` 必须通过或明确记录失败原因。

# Task Package Acceptance

- TP-01.01 Done：已复核当前路线图、任务索引和 0048 阻断。
- TP-02.01 Done：已登记外部一手资料来源。
- TP-03.01 Done：主路线图已新增深度调研补强章节。
- TP-04.01 Done：`git diff --check`、`validate_task_docs.py`、`validate_tasks_tree.py` 均通过。

# Anti-Goals

- 不执行 registry push。
- 不执行真实 Bot live smoke。
- 不配置 OIDC/SIEM/监控平台。
- 不把计划写成生产 100% 完成。

# Ship Readiness

本任务不要求提交推送。后续若进入版本控制，必须先补 `STATUS.md` 的校验证据并保持 worktree clean。
