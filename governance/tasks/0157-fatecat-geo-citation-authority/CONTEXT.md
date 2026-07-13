# Repo Evidence
- 第一阶段线上 GEO audit 为 33/33，但公开内容主要集中在 `/web`、Swagger、JSON registry 与 `llms.txt`。
- GitHub 改造前 `description=null`、`homepage=null`、`topics=[]`。
- 当前没有独立的答案前置产品事实页、可见 FAQ 或 `TechArticle`/`FAQPage`。

# Constraints Matrix
| Constraint | Decision |
|---|---|
| 零美化语义界面 | `/about` 只使用原生 HTML，无 CSS、class 或前端框架 |
| 事实准确性 | capability 表由实时注册表生成 |
| Schema 一致性 | FAQ 正文与 JSON-LD 共用 `PUBLIC_FAQS` |
| 外部指标 | 无平台采样、日志和站长权限时保持待验证 |
| 性能 | 页面服务端生成，无网络调用、数据库写入或算法计算 |

# Change Boundary
- 修改 delivery 的公开发现模块、路由和 Web 内链。
- 修改 GEO 审计、专项测试、README、`llms.txt`、HF 文档与目录 AGENTS。
- 通过 GitHub 官方 API 修改仓库元数据。

# Risk Matrix
| Risk | Impact | Control |
|---|---|---|
| capability 文案漂移 | AI 误引能力状态 | 实时生成并审计 production/planned 集合 |
| FAQ schema 与正文不一致 | 结构化数据失真 | 单一事实源与数量/答案回归 |
| 页面影响 Web 视觉 | 违反设计规则 | 独立语义页，无 CSS，Web 仅增加链接 |
| GitHub 权限不足 | 元数据无法更新 | 使用已认证组织身份并回读 API |

# Assumptions and Falsification
- 假设：独立、答案前置、可追溯的初始 HTML 比继续扩写单一 `llms.txt` 更利于引用。
- 证伪：页面无法被公开 GET、正文与 schema 不一致、能力状态漂移或线上 audit 失败。

# Critical Ambiguities
- 外部 AI 平台是否收录和引用无法由仓库内证明，因此不作为技术发布完成声明。

# Debug Evidence Contract
- 本任务不是既有 bug 修复；若部署或 HTTP 审计失败，记录首个失败端点、提交 SHA 和最小重现命令。
- 调试模式: `Optional`

# Task Package Context Map

## TP-01 差距基线
- 消费公开 HTTP、GitHub API 与 GEO 固定方法。

## TP-02 权威说明页
- 只写公开内容生成层和路由。

## TP-03 发现链与门禁
- 只写发现链、审计、测试与元数据。

## TP-04 交付闭环
- 负责门禁、版本控制和线上证据。
