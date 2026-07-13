# Planning Summary
目标终态是“发现入口 -> 可引用正文 -> 实时契约 -> 源码与 CI 证据”的单向事实链。现实约束是 HF 单进程、零美化 Web、外部平台数据不可见；旧页面数量少不是硬约束。

# Lifecycle Gates
以下 gate 不得跳过：
- SPEC：范围、事实来源、外部边界明确。
- PLAN：选择一个权威说明页，不建立内容农场。
- BUILD：正文、FAQ、Schema、内链、sitemap、GitHub 元数据落地。
- TEST：专项回归、GEO HTTP audit、quick CI。
- REVIEW：correctness、performance、security、document drift。
- SHIP：GitHub push、HF deploy、线上复测。

# Simplest Path
复用 FastAPI、标准库 HTML/JSON/XML 与现有 capability payload；不增加 CMS、SEO 框架、Markdown 渲染器、分析 SDK 或数据库。

# Split Strategy
- TP-01 先证明对象应存在。
- TP-02 建立最小权威页。
- TP-03 把现有发现入口全部接入。
- TP-04 只在门禁通过后发布。

# Execution Waves
1. TP-01
2. TP-02
3. TP-03
4. TP-04

# Runtime Workflow Contract
- 所有公开事实先在 TestClient 验证，再在 HF 真实 HTTP 验证。
- 线上 audit 失败不得用文档声明替代。

# Next Executable Leaves
- TP-04：完整门禁、review、GitHub/HF 交付与线上复测。

# Dependency Graph
`TP-01 -> TP-02 -> TP-03 -> TP-04`

# Rollback Protocol
- 回滚新增 `/about` 路由、Web 内链和 sitemap 条目。
- 恢复 GitHub description、homepage 和 topics 前状态。
- 不触碰测算算法、报告和数据资产。
