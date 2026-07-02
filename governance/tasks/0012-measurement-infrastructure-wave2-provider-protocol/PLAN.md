# Planning Summary
本轮执行 Wave 2 的第一个 provider 协议切片。长期正确终态是 capability executor 不关心具体术数算法，只调用统一 provider object；provider 负责输入归一、计算、metadata、health 和错误边界。当前最小路径是在 `fate_core/capabilities/` 内新增 provider 协议和 registry，把四个已生产 capability 包装进去，并用现有回归测试证明行为不变。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 0012 文档写清 scope、out-of-scope、proof point、falsifier。 |
| PLAN | 任务树只覆盖 provider 协议，不混入算法深化和生产实测。 |
| BUILD | executor 通过 provider registry 执行 production capability。 |
| TEST | targeted pytest、ruff、mypy、quick CI、task validators 通过。 |
| REVIEW | 自审 provider 边界、planned gate、metadata 和文档同步。 |
| SHIP | 任务文档 closeout，无非法占位符。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 新增 `fate_core/capabilities/providers.py`，定义协议和 registry。
2. 改造 `executor.py` 使用 provider object。
3. 补测试断言 provider metadata、health、registry 完整性和 planned 拒绝。
4. 更新 AGENTS 和 100% 计划状态。
5. 运行本地门禁并收口任务文档。

# Split Strategy
- TP-01 建运行时协议真相源。
- TP-02 迁移 executor 行为。
- TP-03 锁测试与文档口径。
- TP-04 做验证和 closeout。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| Wave 1 | TP-01.01、TP-01.02 |
| Wave 2 | TP-02.01、TP-02.02 |
| Wave 3 | TP-03.01、TP-03.02 |
| Wave 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract
- 不使用子进程 worker。
- 不启动长期服务。
- 不访问外部生产凭证。
- 所有验证命令输出写回 STATUS。

# Next Executable Leaves
- TP-01.01 define-provider-protocol
- TP-01.02 add-provider-registry

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.01
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
