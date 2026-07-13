# Planning Summary
目标终态是“项目权威页 -> 旗舰能力权威页 -> 实时 capability/API -> 源码、测试与 CI”的可引用层级，同时以固定 query set 为后续真实 AI 平台采样提供稳定输入。现实约束是 HF 单进程、零美化页面和外部平台不可观测；旧页面数量少只是惯性，不是保留单页的理由。

# Lifecycle Gates
以下 gate 不得跳过：
- SPEC：目标页、事实源、外部指标边界明确。
- PLAN：只建立两个旗舰页和一个题集契约，不创建内容平台。
- BUILD：页面、Schema、题集、内链和 sitemap 落地。
- TEST：专项回归、query set gate、GEO HTTP audit、quick CI。
- REVIEW：correctness、performance、security、document drift、ponytail complexity。
- SHIP：GitHub push、HF deploy、线上复测。

# Future-Optimal and Ponytail Decision
- Target end state：每个真正成熟且有用户入口的 capability 拥有独立、可追溯、可测量的权威说明。
- Real constraints：当前只有 `bazi`、`ziwei` 同时达到 L4 和 Web 可用。
- Inertia constraints：`/about` 已存在不代表所有能力事实必须继续挤在一个页面。
- Kill list：planned 页面、批量关键词页、CMS、营销数据库、自研爬虫平台。
- Existence check：两个旗舰能力页服务明确高意图问题；稳定 query set 是后续效果测量的必要输入。
- Selected ladder rung：复用 FastAPI、标准库 HTML/JSON、现有 registry 和测试框架。
- Proof point：两页初始 HTML、Schema、registry 字段、query set 和线上 audit 全部一致。
- Falsifier：非 L4/Web 能力可访问、页面依赖 provider health、题集缺来源或 audit 失败。
- Ceiling / upgrade path：新能力达到 L4 且有公开交付面后，才允许新增对应 guide。

# Simplest Path
复用 FastAPI、标准库 HTML/JSON、现有 capability registry 和 pytest；不增加 CMS、数据库、前端框架、SEO SDK 或平台采集服务。

# Split Strategy
- TP-02 只负责两页可引用正文和 Schema。
- TP-03 只负责稳定题集与离线 gate。
- TP-04 在前两者通过后接入发现链和文档。
- TP-05 只负责审查与交付证据。

# Execution Waves
1. TP-01
2. TP-02 与 TP-03
3. TP-04
4. TP-05

# Next Executable Leaves
- TP-02、TP-03：能力权威页与采样题集。

# Dependency Graph
`TP-01 -> (TP-02, TP-03) -> TP-04 -> TP-05`

# Runtime Workflow Contract
- 所有页面和题集先经 TestClient 与本地真实 HTTP 验证，再部署到 HF。
- 线上 audit 失败不得用本地结果或文档声明替代。
- query set 只提供采样输入，真实平台结果必须进入独立外部证据流程。

# Rollback Protocol
- 回滚 `/guides/*` 路由、页面生成、内链和 sitemap 条目。
- 删除 discovery query set 契约及其 gate。
- 不触碰测算算法、报告、运行数据或外部凭证。
