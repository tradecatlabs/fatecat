# Task Overview
- Task ID: `0157`
- Slug: `fatecat-geo-citation-authority`
- Objective: 建立 FateCat 可引用权威页、GitHub 实体元数据与第二阶段 GEO 机械门禁。
- Status: `Done`

## In Scope
- 新增服务端直出的 `/about` 权威说明页与正文一致的 Schema.org 实体。
- 接入 Web 内链、sitemap、`llms.txt`、README、HF README 和 GEO 审计。
- 补齐 GitHub description、homepage 与真实 topics。
- 执行本地、GitHub、HF Space 与线上 HTTP 验证。

## Out of Scope
- 不制造关键词页、伪造案例、评价、引用率或平台排名。
- 不修改测算算法、报告结构、输入契约和 Web 视觉规范。
- 不在缺少平台权限时宣称索引、引用、推荐或转化指标已改善。

## Task Package Tree
- `TP-01`：第二阶段 GEO 差距与证据基线。
- `TP-02`：公开权威说明页与实体图。
- `TP-03`：内链、机器文档、GitHub 元数据与机械门禁。
- `TP-04`：审查、提交、部署和线上复测。

## Requirement Alignment
- 以 `/home/lenovo/.projects/geo` 的 page audit、brand graph、article friendly 与 effect monitor 方法为依据。
- 事实必须回指实时 capability、OpenAPI、仓库契约、CI 或公开运行端点。

## Task Package Overview
| ID | Parent | Depth | Depends On | Priority | Objective |
|---|---|---:|---|---|---|
| TP-01 | ROOT | 1 | - | P1 | 建立差距结论与边界 |
| TP-02 | ROOT | 1 | TP-01 | P1 | 实现 `/about` 与 JSON-LD |
| TP-03 | ROOT | 1 | TP-02 | P1 | 接入内链、文档、元数据和 audit |
| TP-04 | ROOT | 1 | TP-03 | P1 | 完成 GitHub/HF/线上交付证据 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
