# Planning Summary
先修复抓取入口与规范 URL，再建立实体和事实底座，最后用同一 HTTP 审计覆盖本地、CI 和线上部署；不通过内容数量制造虚假 GEO 成果。

# Lifecycle Gates
以下 gate 不得跳过：
- SPEC：基线、事实源、边界和不可测指标明确
- PLAN：四个任务包、回滚与验收命令明确
- BUILD：发现模块、llms、文档和门禁落地
- TEST：专项回归、quick CI、GEO live audit 通过
- REVIEW：correctness/security/reliability/performance/document drift 无 BLOCK
- SHIP：GitHub、HF Space、远端 CI 和线上端点一致

# Simplest Path
复用 FastAPI、Schema.org JSON-LD、robots/sitemap 标准、OpenAPI、现有 capability registry 和 Python 标准库；不引入 CMS、数据库、分析 SDK 或第三方 GEO SaaS。

# Split Strategy
- TP-01 只读审计 `/home/lenovo/.projects/geo` 与线上基线。
- TP-02 修改公开发现与事实内容。
- TP-03 修改测试和门禁。
- TP-04 同步文档、审查、部署和证据。

# Execution Waves
TP-01 -> TP-02 -> TP-03 -> TP-04

# Runtime Workflow Contract
- 机器发现内容不参与命理计算热路径。
- 所有动态公开 URL 从一个 canonical 基址生成。
- 线上审计输出 summary 和检查证据，不保存用户数据或页面正文。

# Next Executable Leaves
- TP-04 等待本地门禁。

# Dependency Graph
TP-01 -> TP-02 -> TP-03 -> TP-04

# Rollback Protocol
- 可单独回滚 `public_discovery.py` 路由与 Web head 元数据。
- 可恢复旧 `llms.txt`，但不得保留指向不存在端点的 robots/sitemap 链接。
- 发布失败时保持上一 HF commit，不改写 Git 历史。
