# Planning Summary
本轮从“基础设施骨架”继续向“开发者可接入、能力准入可拒绝、生产/隐私门禁可审计”推进。切片保持小而硬：先补 discoverability 和 admission gates，再用 regression/quick/governance 验证。

# Lifecycle Gates
- SPEC：明确本轮只做基础设施硬化，不新增预测业务体系。
- PLAN：任务树拆为 developer-entrypoints、capability-admission、verification-and-ship。
- BUILD：只修改 registry 准入、API metadata、API 接入文档和回归测试。
- TEST：定向 pytest、ruff、mypy、quick CI、governance、task validator、git diff hygiene 必须真实执行。
- REVIEW：检查默认 Markdown 不被污染、planned 能力不被生产执行、外部连通不被伪造成已验证。
- SHIP：本地门禁通过后提交推送；不得跳过 gate。

# Simplest Path
复用现有 FastAPI OpenAPI、现有 capability registry、现有 pytest 回归和现有 docs/reference-materials 分区；不新建第二套 API gateway 或文档站。

# Split Strategy
- TP-01 先补开发者入口和文档。
- TP-02 再补 capability registry 准入规则和回归。
- TP-03 最后统一验证、提交和推送。

# Execution Waves
- Wave 1：改 registry、metadata、docs、tests。
- Wave 2：定向测试、格式、类型检查。
- Wave 3：quick CI、governance/task docs、git diff hygiene、提交推送。

# Runtime Workflow Contract
- 不切换分支。
- 不执行破坏性 git 命令。
- 不伪造外部生产验证。
- 所有新增字段必须有回归测试或文档证据。

# Next Executable Leaves
- TP-03.01 跑 quick CI、governance strict 和 task validators。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-03.01
TP-02.01 -> TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
