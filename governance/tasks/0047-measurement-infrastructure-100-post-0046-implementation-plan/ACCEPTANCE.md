# Task-Level Acceptance

本任务只验收“计划是否完整、真实、可执行”，不验收任何生产 live 功能。

# Validation Plan

| Check | Command | Expected |
| --- | --- | --- |
| Git diff whitespace | `git diff --check` | no output |
| Task docs validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0047-measurement-infrastructure-100-post-0046-implementation-plan --phase closeout` | success |
| Task tree validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | success or documented pre-existing issue |

# Review Gate

- 路线图不得保留“0046 待做、worktree 脏”的过期口径。
- 未来任务不得把尚未创建的目录编号写死为事实。
- 不得把 pending/live 外部验证写成完成。

# Runtime Verification Gate

本任务无 runtime 行为变更；运行时验证限于任务文档和路线图校验。生产 API/Bot/OIDC/SIEM/registry live 不在本任务执行范围内。

# Ship Readiness

- 任务包必需文件齐全。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已刷新。
- `governance/tasks/INDEX.md` 已登记 0047。
- Markdown whitespace 校验通过。

# Task Package Acceptance

- TP-01.01 Done：当前仓库和远端 CI 状态已记录。
- TP-02.01 Done：外部一手资料矩阵已记录。
- TP-03.01 Done：post-0046 剩余任务树已写入路线图。
- TP-04.01 Done：任务索引和校验状态已回填。

# Anti-Goals

- 不实现 Telegram live。
- 不实现 registry push/signature/attestation。
- 不接入 OIDC/SIEM/monitoring。
- 不改业务源码和 API 行为。
- 不伪造 Bot、registry、OIDC、SIEM 或监控证据；Acceptance 只记录真实 GitHub Actions 结果。

# Evidence Boundary

- 可以写：规划完成、路线图刷新、任务树可执行。
- 不可以写：Telegram live 已通过、registry attestation 已完成、OIDC/SIEM/monitoring 已接入、生产 100% 已完成。
