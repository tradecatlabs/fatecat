# Task Overview
- Task ID: `0109`
- Slug: `measurement-infrastructure-100-post-0108-deep-research-plan`
- Objective: `基于当前 main worktree、0108 release artifact proof 任务状态、现有基础设施契约与外部官方资料，制作 FateCat 达到 100% 测算基础设施所需的完整实现计划、任务树、验收门禁、外部阻断项和不可伪造证据口径；本任务只做调研与计划落盘，不实现业务代码。`
- Status: `Done`

## In Scope
- 查询并整理基础设施官方或事实标准资料，更新 0108 之后的同构映射。
- 复核当前 `main`、0108 任务事实、远端 Actions final-head 状态和主路线图。
- 输出 post-0108 资源缺口矩阵、完整执行波次、下一批任务建议和不可伪造证据口径。
- 更新主路线图，明确 0108 release proof 仍需 final-head Acceptance terminal success 与 current-release-proof 聚合验证。
- 回填本任务任务包并通过 `auto-tasks` 文档校验。

## Out of Scope
- 不实现新的业务代码、capability provider、workflow、脚本或生产部署。
- 不触发真实生产 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS。
- 不把 local-ci、dry-run、staged gate、in_progress run 或 blocked bundle 写成 100% 完成。
- 不修改 0108 任务实现，只记录其状态漂移并把修复列为 W0。

## Task Package Tree
```text
TP-01 调研取证
  TP-01.01 官方资料版本快照
  TP-01.02 当前仓库与远端状态快照
TP-02 100% 基础设施模型收敛
  TP-02.01 资源模型和缺口矩阵
  TP-02.02 不可伪造验收口径
TP-03 完整实现计划
  TP-03.01 执行波次和优先级
  TP-03.02 最短下一步与阻断项
TP-04 落盘与验证
  TP-04.01 更新 RESEARCH、任务包和主路线图
  TP-04.02 运行文档校验、占位符检查和状态检查
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| `$auto-tasks` | 已创建 0109 任务容器并按任务树落盘。 |
| 深度调研查询资料 | `RESEARCH.md` 记录官方资料、版本事实和 FateCat 映射。 |
| 制作 100% 基础设施完整实现计划 | 主路线图新增 post-0108 计划，任务包沉淀执行波次和验收口径。 |
| 基于当前 worktree | 记录 `main` 当前 HEAD、0108 状态、final-head Container success 和 Acceptance in_progress。 |
| 不伪造生产完成 | 所有外部 live、第三方审计、in_progress 远端 run 均按证据状态标注。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | Source matrix written in `RESEARCH.md`. |
| TP-01.02 | Done | Git/gh/task index facts written. |
| TP-02.01 | Done | Resource gap matrix written. |
| TP-02.02 | Done | Anti-forgery evidence rules written. |
| TP-03.01 | Done | W0-W9 implementation waves written. |
| TP-03.02 | Done | Shortest next path and blockers written. |
| TP-04.01 | Done | Roadmap/task docs patched. |
| TP-04.02 | Done | Validator and scans planned/executed. |

## Reading Order
1. README.md
2. RESEARCH.md
3. CONTEXT.md
4. PLAN.md
5. ACCEPTANCE.md
6. ACCEPTANCE_CHECKLIST.md
7. TODO.md
8. STATUS.md
