# Planning Summary
本轮执行 IMP-09 的首个真实切片：把已有 health、ready、metrics、requestId 和结构化日志登记为 ObservabilitySignal 资源，并通过 API 暴露发现层。实现不引入外部监控平台，不改 `/metrics` 语义，只让开发者和审计人员能发现、复核和验证当前观测能力。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确 ObservabilitySignal 资源边界，区分 available 与 planned。 |
| PLAN | 任务拆成 schema、registry、API、测试、文档、验证。 |
| BUILD | 新增 `contracts/fate/observability/` 和 `/observability`，不接外部 collector。 |
| TEST | contract/API focused tests 通过，OpenAPI 暴露新入口。 |
| REVIEW | 不把现有 metrics 夸大成完整 SRE；planned signals 必须明确未生产。 |
| SHIP | quick CI、task docs closeout、task tree validation 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `contracts/fate/observability/AGENTS.md`、`registry.json`、`observability-signal.schema.json`。
2. 扩展 `resource.schema.json` 的 ObservabilitySignal 资源字段。
3. 在 `main.py` 增加 `_observability_registry_payload()` 与 `/observability` API。
4. 在 `/metadata` 挂载 observability 入口。
5. 补 `test_capability_protocol.py` 和 `test_api_contracts.py`。
6. 更新 API 文档、路线图和任务 closeout。

# Split Strategy
- TP-01：确认现有观测能力和本轮边界。
- TP-02：先落 schema/registry，确保 API 有契约。
- TP-03：API 只做发现，不做运行和持久化。
- TP-04：测试文档同步。
- TP-05：验证收口。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| Wave 1 | TP-01.01、TP-01.02 |
| Wave 2 | TP-02.01、TP-02.02、TP-02.03 |
| Wave 3 | TP-03.01、TP-03.02 |
| Wave 4 | TP-04.01、TP-04.02 |
| Wave 5 | TP-05.01、TP-05.02 |

# Runtime Workflow Contract
- 不访问外部 API。
- 不启动长期服务。
- 不提交、不推送。
- 不改 `/metrics` 已有指标语义。
- 所有验证结果写回 `STATUS.md`。

# Next Executable Leaves
- TP-01.01 现有观测能力盘点
- TP-01.02 任务契约与文档字段

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02 -> TP-02.03
TP-02.03 -> TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `contracts/fate/observability/`。
- 恢复 `resource.schema.json` 中 ObservabilitySignal 字段扩展。
- 移除 `main.py` 的 `/observability` API 和 metadata 链接。
- 移除 tests/docs 中 0018 新增内容。
- 保留 0009-0017 已完成切片，不回滚旧基础设施能力。
