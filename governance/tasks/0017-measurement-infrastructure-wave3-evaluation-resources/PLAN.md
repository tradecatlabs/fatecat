# Planning Summary
本轮执行 IMP-08 的首个真实切片：把已经存在的节气 golden、八字/紫微 golden、MingLi-Bench 离线 runner 与 quick CI 评测门禁登记为 Dataset / EvaluationRun 资源。实现不引入数据库，不改生产算法，只让审计人员和开发者能通过 schema、registry、API 和文档发现评测资产。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确 Dataset / EvaluationRun 的只读资源边界，区分 production input 与 evaluation_only。 |
| PLAN | 任务拆成 schema、registry、API、测试、文档、验证。 |
| BUILD | 新增 `contracts/fate/evaluations/` 和 `/evaluations`，不复制大数据内容。 |
| TEST | contract/API focused tests 通过，OpenAPI 暴露新入口。 |
| REVIEW | 资源字段不夸大，MingLi-Bench 不被宣称为强制本地发布门禁。 |
| SHIP | quick CI、task docs closeout、task tree validation 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `contracts/fate/evaluations/AGENTS.md`、`registry.json`、Dataset/EvaluationRun schema。
2. 扩展 `resource.schema.json` 的 Dataset/EvaluationRun 字段清单和 invariant。
3. 在 `main.py` 增加 `_evaluation_registry_payload()` 与 `/evaluations` API。
4. 在 `/metadata` 挂载 evaluation 入口。
5. 补 `test_capability_protocol.py` 和 `test_api_contracts.py`。
6. 更新 API 文档、路线图和任务 closeout。

# Split Strategy
- TP-01：确认资源边界，避免把评测和生产混成一个概念。
- TP-02：先落 schema，保证后续 registry/API 有契约。
- TP-03：registry 只登记少量代表性资产，优先覆盖 golden、benchmark、release gate。
- TP-04：API 只做发现，不做运行和持久化。
- TP-05：测试文档同步。
- TP-06：验证收口。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| Wave 1 | TP-01.01、TP-01.02 |
| Wave 2 | TP-02.01、TP-02.02、TP-02.03 |
| Wave 3 | TP-03.01、TP-03.02、TP-03.03 |
| Wave 4 | TP-04.01、TP-04.02 |
| Wave 5 | TP-05.01、TP-05.02 |
| Wave 6 | TP-06.01、TP-06.02 |

# Runtime Workflow Contract
- 不访问外部 API。
- 不启动长期服务。
- 不提交、不推送。
- 不修改 production provider 计算逻辑。
- 所有验证结果写回 `STATUS.md`。

# Next Executable Leaves
- TP-01.01 资产盘点与资源映射
- TP-01.02 任务契约与文档字段

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02 -> TP-02.03
TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03
TP-03.03 -> TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01 -> TP-05.02
TP-05.02 -> TP-06.01 -> TP-06.02
```

# Rollback Protocol
- 删除 `contracts/fate/evaluations/`。
- 恢复 `resource.schema.json` 中 Dataset/EvaluationRun 字段扩展。
- 移除 `main.py` 的 `/evaluations` API 和 metadata 链接。
- 移除 API/contract tests 与 docs 中 0017 新增内容。
- 保留 0009-0016 已完成切片，不回滚旧基础设施能力。
