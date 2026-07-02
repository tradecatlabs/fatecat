# Task Overview

- Task ID: `0061`
- Slug: `measurement-infrastructure-100-post-0060-deep-research-plan`
- Objective: `基于当前 main、0060 之后的 durable runtime 状态和外部基础设施一手资料，制作 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、任务树、执行顺序和不可伪造验收口径；本任务只落盘规划，不实现业务代码。`
- Status: `In Progress`

## In Scope

- 复核当前 `main...origin/main`、最新 0060 任务事实和 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 基于外部基础设施一手资料，重新定义 FateCat 100% 测算基础设施的资源、能力域、门禁和证据要求。
- 产出 0061 调研文档、后续任务树、执行优先级和不可伪造验收口径。
- 刷新 roadmap 中 post-0060 后续计划，并让任务索引可追踪。

## Out of Scope

- 不实现业务代码、外部 backend、OIDC、SIEM、OTel collector、SDK package 或新测算体系。
- 不声明测算基础设施 100% 已完成。
- 不伪造 Bot token、公网 webhook、外部 Vault/KMS、生产监控、真实 IdP 或第三方审计证据。
- 不切换分支、不改写 Git 历史、不修改运行态数据。

## Task Package Tree

```text
TP-01 当前事实复核
  TP-01.01 读取 git 状态、最新提交、roadmap、任务索引和 0060 closeout 事实
TP-02 外部基础设施调研
  TP-02.01 复核 API、事件、工作流、观测、安全、供应链、SRE、控制面资料
  TP-02.02 把成熟基础设施范式映射到 FateCat 资源模型
TP-03 100% 实现蓝图落盘
  TP-03.01 新增 0061 RESEARCH 调研矩阵
  TP-03.02 刷新 100% roadmap post-0060 实现计划
  TP-03.03 明确后续任务树、优先级、失败判定和证据口径
TP-04 验证与收口
  TP-04.01 清理任务文档占位符，更新 TODO/STATUS/ACCEPTANCE
  TP-04.02 运行任务文档校验、关键词检查和 git 状态复核
```

## Requirement Alignment

- 对齐用户要求：`$auto-tasks`、深度调研、查询资料、制作达到 100% 基础设施所需完整实现计划。
- 对齐 roadmap：0060 之后仍缺 external backend、公网 webhook live、外部 secret storage、AsyncAPI/CloudEvents、OTel/SLO、OIDC/SIEM/retention、developer platform、provider drift、bazi/ziwei corpus 和 audit handoff。
- 对齐项目定位：FateCat 是面向 Agent 与应用开发者的测算基础设施，不是功能堆叠型命理工具。
- 对齐不可伪造原则：所有外部项必须标记真实证据或 `外部连通验证待执行`。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核当前仓库事实和 0060 后状态。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 读取 git、roadmap、任务索引和 0060 证据。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | Yes | 外部基础设施资料调研和映射。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 1 | Yes | Yes | 复核成熟基础设施资料。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 映射到 FateCat 资源模型。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | 100% 实现蓝图落盘。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 RESEARCH 调研矩阵。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 刷新 roadmap。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 固定后续任务树和证据口径。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 验证与收口。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 清理任务文档并更新状态。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 执行任务文档和 git 状态验证。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `RESEARCH.md`
4. `PLAN.md`
5. `ACCEPTANCE.md`
6. `ACCEPTANCE_CHECKLIST.md`
7. `TODO.md`
8. `STATUS.md`
