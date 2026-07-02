# Planning Summary
0012 已把 provider registry 放入运行时，但开发者仍只能通过 capability response 间接看到 provider。本轮把 provider 提升为只读资源：有 schema、集合入口、详情入口、OpenAPI 和文档。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确只做 provider resource，不做外部 health。 |
| PLAN | 任务拆成 schema、API、tests/docs、validation。 |
| BUILD | API 只读取 fate-core provider registry。 |
| TEST | provider API regression、OpenAPI、quick CI 通过。 |
| REVIEW | 确认没有把 planned provider 伪装为 production。 |
| SHIP | closeout validators 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `provider.schema.json`。
2. 在 `main.py` 新增 provider payload helper 和 endpoints。
3. 在 capability resource links 中增加 provider link。
4. 更新 tests/docs。
5. 跑本地门禁并 closeout。

# Split Strategy
- TP-01 契约。
- TP-02 API。
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
- TP-01.01 add-provider-schema
- TP-01.02 expose-provider-schema-ref

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
