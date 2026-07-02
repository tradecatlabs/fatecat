# Task-Level Acceptance

0073 完成需要同时满足：

- `RESEARCH.md` 包含外部一手资料矩阵、FateCat 资源成熟度矩阵、完整任务树、执行顺序和验收口径。
- 主路线图新增 `0.9` 章节，并明确 0072 只覆盖 outbox worker lease、外部 live 待验证、100% 不是预测准确率。
- 任务包没有占位符。
- 任务文档 closeout 校验通过。

# Validation Plan

| Check | Command |
| --- | --- |
| 任务文档校验 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0073-measurement-infrastructure-100-post-0071-deep-research-plan --phase closeout` |
| 占位符扫描 | `rg -n "\\{\\{" governance/tasks/0073-measurement-infrastructure-100-post-0071-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| 关键口径扫描 | `rg -n "0072|外部连通验证待执行|不能声明|0.9" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0073-measurement-infrastructure-100-post-0071-deep-research-plan` |

# Review Gate

- 没有把 planning-only 文档写成代码交付。
- 没有把 0072 写成已完成。
- 没有把本地 baseline 写成生产闭环。
- 没有把外部系统写成已验证。

# Runtime Verification Gate

本任务只验证文档和任务包结构，不运行业务测试。全仓 `validate_tasks_tree.py` 可能受既有 0072 占位符影响，不能作为 0073 单任务完成门禁。

# Ship Readiness

0073 可在后续 Git 交付中与相关文档修改一并提交；提交前仍需由 `auto-github` 读取规则并重新检查完整 worktree。

# Task Package Acceptance

## TP-01 现状复核

Verify: `git status --short --branch`、任务索引和主路线图已读取。

Gate: 0071/0072 状态边界写清，未把 0072 写成完成。

- [x] 当前 Git/任务事实已写入 `CONTEXT.md`。

## TP-02 外部同构调研

Verify: `RESEARCH.md` 包含外部一手资料 source matrix。

Gate: 每个资料映射到 FateCat 资源域或验收门禁。

- [x] 外部资料矩阵已写入 `RESEARCH.md`。

## TP-03 FateCat 100% 计划

Verify: `RESEARCH.md` 和主路线图 `0.9` 包含资源矩阵、任务树、执行顺序和失败判定。

Gate: 计划不把本地 baseline 或外部 pending 写成生产完成。

- [x] 完整计划已写入 `RESEARCH.md` 与主路线图。

## TP-04 文档落盘与验证

Verify: `validate_task_docs.py --phase closeout`。

Gate: 0073 任务文档无占位符、递归节点和状态表可被 validator 识别。

- [x] 文档校验通过。

# Anti-Goals

- 不得修改业务代码。
- 不得虚构外部 live、生产凭证、CI、webhook、SIEM、OIDC、Vault/KMS 或第三方审计结果。
- 不得把 0072 outbox worker lease smoke 标记为 job execution worker lease 或生产完成。
