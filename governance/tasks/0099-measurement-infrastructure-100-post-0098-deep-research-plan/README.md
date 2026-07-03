# Task Overview
- Task ID: `0099`
- Slug: `measurement-infrastructure-100-post-0098-deep-research-plan`
- Objective: `基于当前 worktree、0098 retention staged gate 本地 closeout 事实和外部基础设施官方资料，制作 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、执行波次、验收门禁和不可伪造证据口径；本任务只做调研与规划落盘，不实现业务功能。`
- Status: `Done`

## In Scope
- 查询并整理基础设施同构资料，优先使用官方或事实标准来源。
- 复核当前仓库已有 100% 路线图、0095/0096/0097/0098 任务状态和当前 worktree。
- 输出 post-0098 资源成熟度矩阵、剩余差距、执行波次和完整任务树。
- 更新主路线图，记录 0098 本地 closeout 已通过，同时保留外部 live pending 边界。
- 回填本任务任务包并通过 `auto-tasks` 文档校验。

## Out of Scope
- 不实现新的业务代码、capability provider、外部 live smoke 或生产部署。
- 不连接真实 Bot、OIDC、SIEM、OTel backend、Vault/KMS、Postgres 生产库或 webhook 接收端。
- 不把任何外部待验证项写成已完成。
- 不修改 0098 业务实现本身，只在规划中引用其验证事实。

## Task Package Tree
```text
TP-01 调研基础设施同构资料
  TP-01.01 查询官方资料和事实标准
  TP-01.02 提炼 FateCat 映射原则
TP-02 复核仓库当前状态
  TP-02.01 读取主路线图与 0095-0098 任务事实
  TP-02.02 识别当前 worktree 对计划的影响
TP-03 制作 100% 完整实现计划
  TP-03.01 定义资源成熟度矩阵
  TP-03.02 定义执行波次、任务树和不可伪造证据
TP-04 落盘与验证
  TP-04.01 更新 RESEARCH、任务包和主路线图
  TP-04.02 运行文档校验与引用检查
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 深度调研查询资料 | `RESEARCH.md` 记录官方资料、同构提炼和 FateCat 映射。 |
| 制作 100% 基础设施完整实现计划 | 主路线图新增 post-0098 计划，本任务文档沉淀任务树和验收标准。 |
| 当前 worktree 事实 | 计划明确 0098 本地 closeout 已通过，但外部 live 仍待执行。 |
| 不伪造结果 | 所有外部 live、真实生产凭证、第三方审计均标注待执行。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | Source matrix written in `RESEARCH.md`. |
| TP-01.02 | Done | Infrastructure mapping written. |
| TP-02.01 | Done | Roadmap and 0095/0098 docs read. |
| TP-02.02 | Done | Current worktree impact recorded. |
| TP-03.01 | Done | Resource maturity matrix written. |
| TP-03.02 | Done | Waves and falsifiers written. |
| TP-04.01 | Done | Roadmap/task docs patched and references present. |
| TP-04.02 | Done | Validator passed with placeholders empty. |

## Reading Order
1. README.md
2. RESEARCH.md
3. CONTEXT.md
4. PLAN.md
5. ACCEPTANCE.md
6. ACCEPTANCE_CHECKLIST.md
7. TODO.md
8. STATUS.md
