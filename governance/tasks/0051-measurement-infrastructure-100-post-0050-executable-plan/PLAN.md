# Planning Summary

本任务只做计划落盘，不实现业务代码。目标是把 post-0050 的剩余工作从“很多待优化项”压成基础设施资源模型和可执行任务树。

# Lifecycle Gates

禁止跳过任何 gate；不得把本任务的规划落盘扩大解释为测算基础设施 100% 已完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 100% 是基础设施成熟度，不是预测命中率或模块数量 | Done |
| RESEARCH | 查询并归纳成熟 infra 同构资料 | Done |
| PLAN | 输出 post-0050 任务树、优先级和失败判定 | Done |
| BUILD | 更新主路线图和任务包 | Done |
| TEST | 运行文档/任务校验 | Done |
| REVIEW | 确认可执行计划不伪造完成状态 | Done |
| SHIP | 交给后续 MI-NEXT-03 等实现任务 | Done |

# Simplest Path

复用现有主路线图 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`，新增 post-0050 `0.6` 章节；不新建平行计划，不改业务代码。

# Split Strategy

- TP-01：复核当前仓库事实、0050 完成状态和 0048 阻断状态。
- TP-02：调研成熟 infra 范式并抽象 FateCat 对应能力。
- TP-03：把 post-0050 可执行计划写入主路线图和 0051 任务包。
- TP-04：运行文档校验并回填状态。

# Future-Optimal Contract

Target end state: FateCat 成为测算基础设施，所有测算体系都作为 capability/provider/resource 进入统一控制面，并具备可恢复运行、证据化输出、评测、观测、安全、供应链和审计闭环。

Real constraints: Bot live、OIDC、SIEM、监控平台、告警平台、真实 token 和第三方审计需要外部权限；不能在仓库内伪造。

Inertia constraints: 过去按术数模块推进、按报告页面推进、按脚本推进的组织方式不能决定终态。

Wrong concept / wrong boundary: “多加几个术数模块就等于基础设施”是错误边界；正确边界是能力协议和生产控制面。

Kill list: 无 evidence 的能力声明、绕过 executor 的执行路径、只靠本地 baseline 的生产结论、没有 live evidence 的外部完成状态。

Proof point: 主路线图含 post-0050 资源模型、任务树、优先级和失败判定；任务包和索引可通过 validator。

Falsifier: 如果路线图仍把已完成/未完成混写，或下一步任务不能映射到 infra 域，则本计划失败。

Migration slice: 本轮只补可执行计划；后续按 MI-NEXT-03 到 MI-NEXT-10 分别实现。

Rejected short-term patches: 不直接开始六爻/奇门等新功能；不把 0050 的一次 attestation 写成所有未来 release 自动完成；不把 0048 blocker 淡化。

# Ponytail Contract

Existence check: 用户要求制作完整实现计划；现有 0049 计划在 0050 完成后需要 post-0050 视角刷新。

Selected ladder rung: 复用现有路线图与 governance/tasks，不新建平行规划体系。

Skipped scope: 不写代码、不配置外部平台、不新增业务接口、不新增目录架构。

Ceiling / upgrade path: 后续每个 MI-NEXT 需要独立任务包、实现、测试和 closeout。

Do-not-simplify: 不简化外部 live evidence、不简化隐私安全、不简化 release proof。

Minimal runnable check: `validate_task_docs.py`、`validate_tasks_tree.py`、`git diff --check`。

Complexity review owner: `auto-review` 可在后续执行 `document-drift` 和 `future-optimal-drift` 审查。

# Runtime Workflow Contract

- risk_level: low
- affected_flows: docs, roadmap, task governance
- state_changes: 文档和任务索引
- side_effects: 无生产副作用
- rollback: revert roadmap `0.6` section、删除 0051 任务目录、恢复任务索引行

# Document-Driven Contract

Operating model update: not needed；项目定位不变。

Toolchain model update: not needed；未新增命令或工具链。

Process update: not needed；沿用现有任务治理流程。

Source-of-truth updates: updated；主路线图和任务索引已更新。

Local README/AGENTS impact: not needed；未改变目录职责或入口命令。

Contract/catalog/schema impact: not needed；本轮只做计划，不改契约 schema。

ADR/Gate/module-context impact: not needed；未形成新架构决策，只刷新执行计划。

Documentation exemption reason: 不适用；已更新主路线图。

Validation evidence: `validate_task_docs.py --phase decompose` passed；`validate_tasks_tree.py --phase auto` passed；`git diff --check` passed。

# Execution Waves

| Wave | Nodes | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01 | 当前状态复核 | Done |
| 2 | TP-02.01 | 外部 infra 同构调研 | Done |
| 3 | TP-03.01, TP-03.02 | 计划和任务包落盘 | Done |
| 4 | TP-04.01 | 验证与收口 | Done |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| None | 0051 已完成；下一步按主路线图进入 `MI-NEXT-03` durable runtime 二期。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol

- 恢复主路线图新增的 `0.6` post-0050 章节。
- 删除 0051 任务目录和任务索引行。
- 保留 0050 已完成状态，不回滚真实远端 workflow 事实。
