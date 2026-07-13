# Repo Evidence
- 第二阶段线上 GEO audit 为 46/46，已覆盖根入口、Web、`/about`、robots、sitemap、`llms.txt`、OpenAPI 与 capability/provider registry。
- `/about` 能回答项目级事实，但综合八字和紫微尚无各自可独立引用的正文页面。
- 外部 GEO 指标保持 pending，但仓库内没有固定 Prompt 题集，后续平台采样不可稳定比较。
- `0157` 的 README 状态仍为 `In Progress`，与 STATUS 的 `Done` 不一致，需在文档漂移收口中修正。

# Constraints Matrix
| Constraint | Decision |
|---|---|
| 最小内容面 | 只发布 L4 且 Web 可用的 `bazi`、`ziwei` 两页 |
| 零美化语义界面 | 原生 HTML，无 CSS、class、前端框架或 JS 依赖 |
| 事实准确性 | 生命周期、输入、引擎、证据和风险来自 registry |
| Schema 一致性 | FAQ、实体和正文共用同一 guide 事实源 |
| 外部指标 | query set 只建立采样基线，不伪造平台结果 |
| 性能 | 页面无网络、数据库、provider health 或命理计算 |

# Change Boundary
- 修改 delivery 公开发现模块、路由和现有 Web 内链。
- 新增 `contracts/fate/discovery/` 的题集与目录说明。
- 修改 GEO audit、专项测试、README、`llms.txt`、HF README 和相关 AGENTS。
- 不触碰 fate-core 算法和报告生成器。

# Risk Matrix
| Risk | Impact | Control |
|---|---|---|
| 页面事实与 registry 漂移 | AI 引用错误 | 动态字段来自 registry；测试锁定状态与引擎 |
| 批量低质量页面 | 搜索信誉下降 | 只允许两个旗舰能力，其他路径 404 |
| Schema 超出正文 | 结构化数据失真 | FAQ 逐项一致回归 |
| Prompt 题集变成结果伪证 | 错误宣称 GEO 效果 | 契约明确 `expectedSourceUrls`，不保存虚构答案 |

# Assumptions and Falsification
- 假设：两个高意图能力页比继续扩写项目总览更容易被独立抽取和引用。
- 证伪：页面不可公开抓取、正文与 schema/registry 漂移、planned 页面被暴露或线上 audit 失败。

# Critical Ambiguities
- 外部 AI 平台何时收录、是否引用和推荐无法由代码证明，保持“外部连通验证待执行”。

# Debug Evidence Contract
- 本任务不是既有运行故障；若路由、部署或审计失败，记录首个失败端点、提交 SHA 和最小复现命令。
- 调试模式: `Optional`

# Task Package Context Map
- TP-01：消费公开 HTTP、registry 与固定 GEO 方法。
- TP-02：只写公开内容生成和路由。
- TP-03：只写 discovery 契约和校验。
- TP-04：只写发现链、文档、测试和 audit。
- TP-05：只负责门禁、Git/HF 与线上证据。
