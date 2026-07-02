# Planning Summary
本轮把 capability 执行结果提升为同时包含原始 `data/evidence` 和机器可审计 `Report` resource envelope。它是 IMP-05 的第一刀，不处理完整 Markdown snapshot，也不改变任何算法结论。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确只做 report/evidence envelope，不做报告内容重构。 |
| PLAN | 任务拆成 schema、API envelope、tests/docs、validation。 |
| BUILD | `report` envelope 不复制完整 data，不改变旧字段。 |
| TEST | API/capability protocol regression 通过。 |
| REVIEW | 确认默认 Markdown 仍只有 bazi，非 bazi standalone。 |
| SHIP | closeout validators 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `report.schema.json`。
2. 更新 `output.schema.json`、`evidence.schema.json`、`resource.schema.json`。
3. 在 `main.py` 新增 `_capability_report_payload()`。
4. capability calculate response 增加 `report`。
5. 更新 tests/docs 并运行门禁。

# Split Strategy
- TP-01 契约。
- TP-02 API envelope。
- TP-03 测试与文档。
- TP-04 验证。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| Wave 1 | TP-01.01、TP-01.02 |
| Wave 2 | TP-02.01、TP-02.02 |
| Wave 3 | TP-03.01、TP-03.02 |
| Wave 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract
- 不访问外部服务。
- 不启动长期服务。
- 不新增数据库。
- 所有证据写回 STATUS。

# Next Executable Leaves
- TP-01.01 add-report-schema
- TP-01.02 update-output-and-evidence-schema

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01
TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
