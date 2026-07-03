# Planning Summary
本任务把 0093/0094 之后的 100% 基础设施路线图刷新为可执行状态。计划不再按“新增术数模块”排序，而按基础设施资源域排序：核心质量、事件平台、运行时、安全、可观测、开发者平台、发布审计。

# Lifecycle Gates
| Gate | 要求 | 状态 |
| --- | --- | --- |
| SPEC | 明确本任务只做 post-0094 调研与计划，不实现业务代码 | Done |
| PLAN | 输出资源成熟度矩阵、执行波次、不可伪造证据 | Done |
| BUILD | 更新主路线图和 0095 任务文档 | Done |
| TEST | 任务文档校验和引用检查 | Done |
| REVIEW | 确认没有把 pending 外部项写成完成 | Done |
| SHIP | 任务可交给后续实现切片使用 | Done |

不得跳过 gate；任一 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP gate 缺证据时，0095 不得 closeout。

# Simplest Path
1. 复用已有主路线图，不新建平行路线图。
2. 复用已有 core corpus、report diff、MingLi-Bench 资产，不新建评测体系。
3. 先做本地可执行 Wave A，再等外部凭证推进 Wave B。

# Split Strategy
- TP-01 只收集事实和资料。
- TP-02 负责把资料压成 FateCat 资源模型和实现波次。
- TP-03 负责落盘。
- TP-04 负责验证文档契约。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| 1 | TP-01.01、TP-01.02 |
| 2 | TP-02.01、TP-02.02 |
| 3 | TP-03.01、TP-03.02 |
| 4 | TP-04.01 |

# Runtime Workflow Contract
- No runtime worker required。
- No business code execution required。
- Evidence is file-based: roadmap、RESEARCH、task docs、validation output。

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01
```

# Future-Optimal Task Contract
| Field | Value |
| --- | --- |
| Target end state | FateCat 100% 以资源、契约、控制面、证据闭环定义，不以功能堆叠定义。 |
| Real constraints | 当前 worktree、既有路线图、外部 live 需要真实环境、用户要求制作完整计划。 |
| Inertia constraints | 旧任务编号、历史路线图段落、已有局部 baseline 不能决定终态。 |
| Wrong concept / wrong boundary | “更多术数模块 = 基础设施 100%” 是错误边界。 |
| Kill list | 删除计划中的伪完成表述；避免平行路线图。 |
| Proof point | post-0094 计划落入主路线图和 0095 任务目录。 |
| Falsifier | 若后续发现外部 live 证据已真实存在但计划仍列 pending，需重开计划。 |
| Migration slice | 本轮只刷新计划，下一轮按 Wave A 执行核心质量切片。 |
| Rejected short-term patches | 不把 0092 原文复制为新计划；不把外部待验证写成完成。 |
| Future-optimal review owner | `auto-review` document-drift / future-optimal-drift。 |

# Ponytail Task Contract
| Field | Value |
| --- | --- |
| Existence check | 0093/0094 完成后，主路线图需要 post-0094 最新剩余路径，便于继续执行。 |
| Selected ladder rung | Project-native documentation/task package，不新增运行时抽象。 |
| Skipped scope | 不实现 0096+ 业务/门禁，不接入外部 live。 |
| Ceiling / upgrade path | 当 0096+ 实现后，应再次刷新 current release/audit 证据，而不是依赖本计划。 |
| Do-not-simplify | 不删除外部 pending 边界、不隐藏隐私和生产证据缺口。 |
| Minimal runnable check | `validate_task_docs.py --phase decompose` 和路线图引用检查。 |
| Complexity review owner | `auto-review` ponytail-complexity。 |

# Document-Driven Task Contract
| Field | Value |
| --- | --- |
| Operating model update | not needed：基础设施定位不变。 |
| Toolchain model update | not needed：不新增命令或脚本。 |
| Process update | not needed：不改变开发流程。 |
| Source-of-truth updates | updated：主路线图和 0095 task package。 |
| Local README/AGENTS impact | not needed：不改变目录边界或命令职责。 |
| Contract/catalog/schema impact | not needed：不改契约/schema。 |
| ADR/Gate/module-context impact | not needed：不新增架构决策或门禁。 |
| Documentation exemption reason | 除主路线图和任务文档外，无长期事实变化。 |
| Validation evidence | `validate_task_docs.py` 与 `rg` 检查。 |

# Rollback Protocol
- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 本次追加段。
- 删除或恢复 `governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/`。
- 恢复 `governance/tasks/INDEX.md` 的 0095 行。
