# Planning Summary

本任务把“测算基础设施 100%”从聊天中的目标口径转成可复核路线图补强：用基础设施领域的一手资料建立同构模型，再映射为 FateCat 的资源对象、实现波次、完成判定和下一步执行顺序。

# Lifecycle Gates

禁止跳过任何 gate；不得把本任务的规划落盘扩大解释为测算基础设施 100% 已完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 100% 是基础设施成熟度，不是预测准确率或模块数量 | Done |
| RESEARCH | 外部资料来自一手/官方文档，并可回链 | Done |
| PLAN | 资源模型、实现波次和完成判定写入主路线图 | Done |
| BUILD | 只更新文档和任务包，不改业务代码 | Done |
| TEST | Markdown whitespace 和任务文档校验通过 | Done |
| REVIEW | 不把外部待验证项写成完成 | Done |
| SHIP | 可作为后续 MI-NEXT 任务的执行依据 | Done |

# Simplest Path

复用现有主路线图 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`，新增 `0.5` 深度调研补强章节；不新建平行 roadmap，避免多个事实源漂移。

# Split Strategy

- TP-01：复核现有路线图、任务索引、0048 阻断事实和 contracts 资源。
- TP-02：调研外部基础设施一手资料。
- TP-03：把调研结论映射为 FateCat resource model、wave 和 done gate。
- TP-04：运行校验并更新任务状态。

# Execution Waves

| Wave | Nodes | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01 | 仓库现状和现有路线图复核 | Done |
| 2 | TP-02.01 | 外部一手资料调研与能力域映射 | Done |
| 3 | TP-03.01 | 主路线图 `0.5` 深度调研补强落盘 | Done |
| 4 | TP-04.01 | 文档校验与状态收口 | Done |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| None | 0049 已完成；下一步进入 `MI-NEXT-02` registry digest/attestation 实现任务。 |

# Future-Optimal Contract

Target end state: FateCat 成为测算基础设施，而不是命理功能合集。所有体系都以 capability/provider/report/evidence/job/evaluation/release artifact 资源运行。

Real constraints: 真实 Bot token、registry push、OIDC、SIEM、监控、告警和第三方审计需要外部环境；本任务只能计划，不能伪造完成。

Inertia constraints: 旧路线图已覆盖很多项，但缺少统一资源模型和基础设施同构定义；不能因为已有计划就停止补强。

Kill list: “功能越多越像基础设施”“本地 baseline 等于生产 100%”“Bot dry-run 等于 live”“SBOM 本地生成等于 registry attestation”。

Proof point: 主路线图新增外部资料矩阵、资源模型、实现波次、下一步执行顺序和完成判定。

Falsifier: 后续无法从路线图直接创建 `MI-NEXT-*` 实现任务，或审计人员仍需依赖聊天记录理解 100% 定义。

Migration slice: 本轮只改文档；下一轮应执行 `MI-NEXT-02` registry digest/attestation，0048 继续等待真实 Bot token。

# Ponytail Contract

Existence check: 用户明确要求深度调研并制作完整实现计划；现有 0047 路线图需要更强的同构资源模型和完成判定。

Selected ladder rung: 更新现有主路线图 + 新增任务包证据。

Skipped scope: 不实现 registry attestation、durable runtime、OTel collector、OIDC/SIEM 或 golden corpus。

Ceiling / upgrade path: 后续每个 wave 必须拆成独立 `governance/tasks/<id>-<slug>`，并用真实验证闭环。

Minimal runnable check: `git diff --check`、`validate_task_docs.py`、`validate_tasks_tree.py`。

# Runtime Workflow Contract

- risk_level: low
- affected_flows: docs, roadmap, task governance
- state_changes: 文档和任务索引
- side_effects: 外部 web 调研，无生产副作用
- rollback: revert roadmap `0.5` section、删除 0049 任务目录、恢复任务索引行

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01
```

# Rollback Protocol

- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中新增的 `0.5` 章节。
- 删除 `governance/tasks/0049-measurement-infrastructure-100-deep-research-implementation-plan/`。
- 恢复 `governance/tasks/INDEX.md` 中的 0049 行。
