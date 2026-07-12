# Task Overview
- Task ID: `0156`
- Slug: `fatecat-geo-discovery-optimization`
- Objective: 基于固定 GEO 方法与公开证据，提升 FateCat 在 AI 搜索、问答引擎和 Agent 生态中的可发现性、可解析性、可引用性与可信度。
- Status: `In Progress`

## In Scope
- HF Space 根入口、robots、sitemap、canonical 与 Schema.org 实体图
- `llms.txt` 事实底座、能力状态、来源、问答和引用边界
- GitHub/HF README 机器入口与 GEO 治理文档
- 可重复 HTTP 审计、量化技术分数、回归与公开发布门禁
- 无法从仓库获取的 crawler、索引、引用、流量和转化指标的外部证据口径

## Out of Scope
- 关键词堆砌、批量内容页、伪造案例、第三方背书或平台引用
- 承诺 AI 平台收录、排名、引用或推荐
- 新增命理体系或改变计算结果
- 未经同意接入用户级追踪、cookie 或个人画像

## Task Package Tree
- TP-01：建立公开 GEO 基线与方法映射
- TP-02：实现机器发现、实体结构和事实底座
- TP-03：建立审计脚本、回归测试与发布门禁
- TP-04：文档、治理、审查、部署和线上验证

## Requirement Alignment
- 直接覆盖用户要求的站点、GitHub、HF Space、llms、结构化数据、抓取策略、证据、作者、更新时间、内链与量化指标。
- 方法来源固定为 `/home/lenovo/.projects/geo`；只吸收可验证白帽方法，不执行外部仓库安装或发布逻辑。
- 公开能力以 `contracts/fate/capabilities/registry.json` 和线上 registry 为真相源。

## Task Package Overview
| ID | Parent | Depth | Depends On | Priority | Objective |
|---|---|---:|---|---|---|
| TP-01 | ROOT | 1 | - | P0 | 建立 GEO 方法和线上基线 |
| TP-02 | ROOT | 1 | TP-01 | P0 | 实现机器发现、实体结构和事实底座 |
| TP-03 | ROOT | 1 | TP-02 | P0 | 建立审计、回归与发布门禁 |
| TP-04 | ROOT | 1 | TP-03 | P0 | 文档、审查、部署和线上验证 |

## Reading Order
1. CONTEXT.md
2. PLAN.md
3. ACCEPTANCE.md
4. ACCEPTANCE_CHECKLIST.md
5. TODO.md
6. STATUS.md
