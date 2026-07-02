# Planning Summary
本轮执行 IMP-11 的首个真实切片：把 FastAPI、Web、Telegram Bot、CLI、Agent Skill 与 Hugging Face Space 登记为 DeliverySurface 资源，并通过 API 暴露发现层。实现不重写交付面，不执行外部 live，只把同源链路、输出契约、验证命令和外部连通边界机器化。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确 DeliverySurface 资源边界，区分 available、partial 与 manual。 |
| PLAN | 任务拆成 schema、registry、API、测试、文档、验证。 |
| BUILD | 新增 `contracts/fate/delivery/` 和 `/surfaces`，不保存运行时数据。 |
| TEST | contract/API focused tests 通过，OpenAPI 暴露新入口。 |
| REVIEW | 不把 CLI/Skill partial 和 Bot/HF manual 写成完整生产同源。 |
| SHIP | quick CI、task docs closeout、task tree validation 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `contracts/fate/delivery/AGENTS.md`、`registry.json`、`delivery-surface.schema.json`。
2. 扩展 `resource.schema.json` 的 DeliverySurface 资源字段。
3. 在 `main.py` 增加 `_delivery_surface_registry_payload()` 与 `/surfaces` API。
4. 在 `/metadata` 挂载 surfaces 入口。
5. 补 `test_capability_protocol.py` 和 `test_api_contracts.py`。
6. 更新 API 文档、路线图和任务 closeout。

# Split Strategy
- TP-01：确认现有交付面和本轮边界。
- TP-02：先落 schema/registry，确保 API 有契约。
- TP-03：API 只做发现，不做外部 live。
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
- 不输出真实用户输入、报告正文、token 或生产日志。
- 所有验证结果写回 `STATUS.md`。

# Next Executable Leaves
- TP-01.01 多端交付面盘点
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
- 删除 `contracts/fate/delivery/`。
- 恢复 `resource.schema.json` 中 DeliverySurface 字段扩展。
- 移除 `main.py` 的 `/surfaces` API 和 metadata 链接。
- 移除 tests/docs 中 0020 新增内容。
- 保留 0009-0019 已完成切片，不回滚旧基础设施能力。
