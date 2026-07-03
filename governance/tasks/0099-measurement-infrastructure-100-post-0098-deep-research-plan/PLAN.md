# Planning Summary
本任务把“100% 测算基础设施”从口号收敛为可执行路线：以 Capability、Provider、CalculationJob、Event、ReportProfile、Evidence、Dataset、EvaluationRun、DeliverySurface、ObservabilitySignal、SecurityControl、ReleaseArtifact、AuditHandoff 等资源对象为骨架，对照基础设施成熟体系补齐剩余门禁。

# Lifecycle Gates
| Gate | Requirement | Status |
| --- | --- | --- |
| SPEC | 明确只做 post-0098 调研与计划，不实现业务代码 | Done |
| PLAN | 输出外部资料、资源成熟度、任务树和不可伪造证据 | In Progress |
| BUILD | 更新 `RESEARCH.md`、任务文档和主路线图 | In Progress |
| TEST | 任务文档校验与占位符检查 | Not Started |
| REVIEW | 确认没有把 external pending 写成 live done | Done |
| SHIP | 规划可交给后续实现切片使用 | Done |

不得跳过 gate；任一 gate 缺证据时，本任务不能 closeout。

# Simplest Path
1. 不新建第二份路线图，只增强现有主路线图。
2. 不发明新 infra 分类，复用行业成熟模式映射到现有 FateCat 资源。
3. 不阻塞在外部凭证，拆成本地 Wave A 和外部 Wave B。
4. 不把计划写成“已完成”，所有 live 事项必须有证据或标注待执行。

# Split Strategy
- TP-01 负责外部资料与同构映射。
- TP-02 负责当前仓库事实和 0098 状态校正。
- TP-03 负责完整计划结构。
- TP-04 负责落盘、校验和自审。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| 1 | TP-01.01、TP-02.01、TP-02.02 |
| 2 | TP-01.02、TP-03.01 |
| 3 | TP-03.02、TP-04.01 |
| 4 | TP-04.02 |

# Runtime Workflow Contract
- No runtime worker required.
- No production credentials required.
- No business code execution allowed in this task.
- Evidence is file-based: `RESEARCH.md`, roadmap section, task docs, validator output.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| TP-04.01 | Finish roadmap/task-doc write. |
| TP-04.02 | Run task docs validator and placeholder checks. |

# Dependency Graph
```text
TP-01.01 -> TP-01.02
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-01.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01
TP-04.01 -> TP-04.02
```

# Future-Optimal Task Contract
| Field | Value |
| --- | --- |
| Target end state | FateCat 100% 由资源协议、执行控制面、质量评测、生产运维、安全审计和发布证明共同定义。 |
| Real constraints | 0098 本地 closeout 已通过；外部 live 依赖真实凭证和平台；已有主路线图不能分裂。 |
| Inertia constraints | 历史任务编号、已写路线图段落和局部 baseline 不应决定最终成熟模型。 |
| Wrong concept / wrong boundary | “模块越多越像基础设施”和“本地 dry-run 等同生产 live”都是错误边界。 |
| Kill list | 删除伪完成口径；拒绝把外部待验证项写成已通过；拒绝第二份平行路线图。 |
| Proof point | 主路线图新增 post-0098 delta，0099 任务包可由 validator 复核。 |
| Falsifier | 如果远端 CI 或外部 live 证据推翻本地 closeout 结论，本计划中 0098 完成口径需要刷新。 |
| Migration slice | 本轮只做计划，后续从 provider/license drift 与 certification aggregator dry-run 继续执行。 |
| Rejected short-term patches | 不为了“完整”新增空脚本、空 schema 或未验证任务。 |
| Future-optimal review owner | `auto-review` document-drift / future-optimal-drift。 |

# Ponytail Task Contract
| Field | Value |
| --- | --- |
| Existence check | 0096/0097/0098 本地切片已完成后，主路线图需要 post-0098 当前剩余路径。 |
| Selected ladder rung | Project-native roadmap + task docs; no new runtime abstraction. |
| Skipped scope | No code, no live credentials, no production deployment, no new capability module. |
| Ceiling / upgrade path | After version-control closeout, create concrete implementation tasks for next local Wave A items. |
| Do-not-simplify | Preserve external pending and anti-forgery requirements. |
| Minimal runnable check | `validate_task_docs.py --phase decompose` plus placeholder/reference checks. |
| Complexity review owner | `auto-review` ponytail-complexity。 |

# Document-Driven Task Contract
| Field | Value |
| --- | --- |
| Operating model update | Not needed: infrastructure positioning unchanged. |
| Toolchain model update | Not needed: no script/tool behavior changes. |
| Process update | Not needed: task planning only. |
| Source-of-truth updates | Main roadmap and 0099 task docs. |
| Local README/AGENTS impact | Not needed: no directory or command responsibility change. |
| Contract/catalog/schema impact | Not needed: no contract/schema edits. |
| ADR/Gate/module-context impact | Not needed this task; future implementation tasks may need gates. |
| Documentation exemption reason | Changes are limited to roadmap/task docs/research. |
| Validation evidence | Task docs validator and `rg` placeholder scan. |

# Rollback Protocol
- Revert the post-0098 section in `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
- Remove `governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan/`.
- Restore the 0099 row in `governance/tasks/INDEX.md`.
