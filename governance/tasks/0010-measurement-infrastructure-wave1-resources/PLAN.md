# Planning Summary
执行 0009 Wave 1 的首批低风险可验收切片：先把资源模型和错误码变成机器契约，再通过 API 暴露 capability detail 与 errors catalog，最后用回归测试和文档锁定。

# Lifecycle Gates
- SPEC：明确本轮只做 schema/API discovery/error catalog，不做 job/provider 后续切片。
- PLAN：拆成 resource contracts、developer API、tests/docs、validation。
- BUILD：新增契约文件、API helper 和端点、回归测试、文档同步。
- TEST：定向 pytest、ruff、mypy、quick CI、task validators、git diff check。
- REVIEW：确认无算法变更、无默认报告污染、无外部生产验证伪造。
- SHIP：本轮不自动提交；等待用户明确要求版本控制；不得跳过 gate。

# Simplest Path
复用现有 `contracts/fate/capabilities/`、FastAPI、pytest，不引入新框架、不新增顶层资源目录、不改执行器。

# Split Strategy
- TP-01 先补机器契约。
- TP-02 再暴露 API。
- TP-03 锁测试和文档。
- TP-04 统一验证收口。

# Execution Waves
- Wave A：TP-01.01、TP-01.02。
- Wave B：TP-02.01、TP-02.02。
- Wave C：TP-03.01、TP-03.02。
- Wave D：TP-04.01、TP-04.02。

# Runtime Workflow Contract
- 不切换分支。
- 不修改 secret。
- 不提交推送，除非用户明确要求。
- 每个 leaf 完成后必须有文件或命令证据。

# Next Executable Leaves
- TP-04.01

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01 -> TP-04.02
TP-01.02 -> TP-02.02 -> TP-03.01 -> TP-04.01 -> TP-04.02
TP-03.02 -> TP-04.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
