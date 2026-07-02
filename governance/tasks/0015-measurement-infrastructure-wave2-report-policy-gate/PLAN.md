# Planning Summary
本轮把 0014 留下的 `forbidden claims scanner` 从 schema 后续项落成 capability report envelope 的最小政策门禁。实现只扫描生成报告摘要字段，明确排除 `risk.forbiddenClaims`，避免清单自检导致假阳性。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确 policyGate 是 Report resource 子字段，不是完整合规系统。 |
| PLAN | 任务拆成 schema、helper、API envelope、tests/docs、validation。 |
| BUILD | 不删除旧字段，不改变算法输出，只新增 policyGate。 |
| TEST | scanner fail/pass、schema、API response 和 quick CI 通过。 |
| REVIEW | 确认扫描范围、排除字段和后续升级路径透明。 |
| SHIP | closeout validators 通过，STATUS 有真实证据。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 在 `fate_core.capabilities` 增加 `report_policy.py`，提供 `build_report_policy_gate()`。
2. 更新 `fate_core/capabilities/AGENTS.md` 和可选 `__init__.py`。
3. 更新 `report.schema.json`，把 `policyGate` 纳入 required report fields。
4. 在 `_capability_report_payload()` 接入 helper。
5. 增加 scanner 与 API response 回归测试。
6. 更新 API 文档、100% 路线图和任务文档。
7. 跑 targeted tests、ruff、mypy、quick CI、governance、task validators、diff check。

# Split Strategy
- TP-01 契约与 schema。
- TP-02 helper 与 API envelope。
- TP-03 测试与文档。
- TP-04 验证与 closeout。

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
- 不新增数据库、缓存、队列或外部依赖。
- 不提交、不推送。
- 所有验证证据写回 STATUS。

# Next Executable Leaves
- TP-01.01 define-report-policy-scope
- TP-01.02 update-report-schema

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
- 移除本任务新增的 `report_policy.py` 和相关导入。
- 恢复 `report.schema.json`、`main.py`、测试和文档中的 `policyGate` 变更。
- 保留 0009-0014 已有工作树改动，不做跨任务回滚。
