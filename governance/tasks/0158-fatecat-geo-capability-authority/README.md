# Task Overview
- Task ID: `0158`
- Slug: `fatecat-geo-capability-authority`
- Objective: 为综合八字与紫微斗数建立独立可引用权威页，并建立可重复的 AI 问答采样基线。
- Status: `Done`

## In Scope
- 新增 `/guides/bazi` 与 `/guides/ziwei` 服务端语义 HTML 页面。
- 页面事实来自 capability registry 与项目维护的有限解释内容，正文与 JSON-LD 共用事实源。
- 新增 GEO query set 契约和机械校验。
- 更新 sitemap、内链、`llms.txt`、README、HF README、GEO 审计与回归测试。
- 完成本地、GitHub、HF Space 和线上 HTTP 验证。

## Out of Scope
- 不建立内容农场、CMS、博客系统或 planned capability 页面。
- 不修改测算算法、报告结构、输入契约或 Web 视觉规范。
- 不伪造 AI 平台索引、引用、推荐、流量或转化数据。

## Task Package Tree
- `TP-01`：第三阶段差距、来源和边界基线。
- `TP-02`：八字与紫微独立权威页。
- `TP-03`：GEO 采样题集与机械门禁。
- `TP-04`：发现链、文档、测试与审计。
- `TP-05`：审查、提交、部署和线上复测。

## Requirement Alignment
- 使用 `/home/lenovo/.projects/geo` 的 page audit、article friendly、brand graph 与 effect monitor 方法。
- Google Search 与 Schema.org 官方文档只用于技术结构核验；项目事实只来自仓库契约、源码、测试和公开端点。

## Task Package Overview
| ID | Parent | Depth | Depends On | Priority | Objective |
|---|---|---:|---|---|---|
| TP-01 | ROOT | 1 | - | P1 | 建立最小充分方案与证据边界 |
| TP-02 | ROOT | 1 | TP-01 | P1 | 实现两个旗舰能力权威页 |
| TP-03 | ROOT | 1 | TP-01 | P1 | 建立稳定 GEO 采样题集 |
| TP-04 | ROOT | 1 | TP-02,TP-03 | P1 | 接入发现链、文档与门禁 |
| TP-05 | ROOT | 1 | TP-04 | P1 | 完成交付和线上证据 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
