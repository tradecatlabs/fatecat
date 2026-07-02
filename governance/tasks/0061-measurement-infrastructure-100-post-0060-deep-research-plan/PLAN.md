# Planning Summary

0061 的目标不是继续堆功能，而是把 0060 之后的 100% 基础设施路线压成可执行蓝图。终态是：任何后续测算体系、交付面、外部依赖和发布行为，都必须通过资源契约、provider 生命周期、durable runtime、事件契约、observability、安全门禁、评测门禁和审计证据闭环。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0061 不能标记为 Done，也不能把 roadmap 更新视为可执行实现已完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 0061 只做调研与计划，不实现业务代码 | Done |
| PLAN | 任务树、边界、调研源和验收口径写入任务包 | Done |
| BUILD | RESEARCH 与 roadmap post-0060 实现蓝图落盘 | Done |
| TEST | task docs validator、占位符扫描、关键词检查通过 | Done |
| REVIEW | 确认不夸大 100%、不伪造外部证据、后续任务可执行 | Done |
| SHIP | 当前任务文档可提交；commit/push 由后续 git 交付任务处理 | Done |

# Future-Optimal Contract

- target end state: FateCat 是面向 Agent 和应用开发者的测算基础设施，所有能力都是可发现、可执行、可审计、可观测、可回滚的资源。
- real constraints: 当前仍缺真实外部 backend、Bot token、公网 webhook 接收端、OIDC/IdP、SIEM、OTel backend、Vault/KMS 和第三方审计权限。
- inertia constraints: 不把本地 SQLite baseline、文档契约或 dry-run 当成生产闭环。
- kill list: 功能堆叠、绕过 capability executor、外部证据伪造、100% 口径夸大、真实用户样例污染。
- proof point: 后续任务树的每个节点都有最小交付物和不可伪造证据。
- falsifier: 后续任何任务无法回答“证据从哪里来”和“不能伪造什么”，则 0061 计划不合格。
- migration slice: 0062 从 durable runtime external backend contract 开始，把最大 P0 缺口转成可执行切片。

# Simplest Path

不创建新抽象、不改业务代码。只在 0061 任务包中沉淀完整调研矩阵，并在 100% roadmap 增加 post-0060 执行蓝图。后续真正实现从 0062 开始按单一可验收切片推进。

# Split Strategy

- TP-01：先锁当前仓库事实，避免重复规划。
- TP-02：用成熟基础设施同构资料定义 FateCat 需要具备什么。
- TP-03：把调研转成后续任务树和 roadmap。
- TP-04：校验任务文档、清占位符、记录状态。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01, TP-02.01 | 并行复核仓库事实与外部资料。 |
| 2 | TP-02.02 | 完成 FateCat 同构映射。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | 落盘调研、roadmap 和后续任务树。 |
| 4 | TP-04.01, TP-04.02 | 文档收口和验证。 |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`git status`、`git log`、`validate_task_docs.py`、`validate_tasks_tree.py`、web research |
| forbidden actions | 不切换分支、不删除文件、不修改业务代码、不读取真实 secret、不声明外部 live 已通过 |
| expected output | 0061 task package + `RESEARCH.md` + roadmap post-0060 implementation blueprint |
| required evidence | git 状态、任务文档 validator、占位符扫描、roadmap/INDEX 关键词检查 |
| stop condition | 需要真实外部凭证或生产账号才能判断时，标记外部连通验证待执行，不阻塞本计划任务 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | No remaining executable leaves. |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中 0061 新增段落。
- 删除 `governance/tasks/0061-measurement-infrastructure-100-post-0060-deep-research-plan/`。
- 恢复 `governance/tasks/INDEX.md` 当前任务行。
- 不得影响其他任务目录。
