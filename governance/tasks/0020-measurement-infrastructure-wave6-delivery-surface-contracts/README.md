# Task Overview
- Task ID: `0020`
- Slug: `measurement-infrastructure-wave6-delivery-surface-contracts`
- Objective: `把 Web、FastAPI、Telegram Bot、CLI、Agent Skill 等交付面资源化为 DeliverySurface 发现层，明确每个入口的同源计算链路、输出契约、验证命令、隐私边界和外部连通状态，补 schema、registry、API、文档和回归测试。`
- Status: `In Progress`

## In Scope
- 新增 `contracts/fate/delivery/` 作为多端交付面资源真相源。
- 新增 `DeliverySurface` schema 与 registry。
- 扩展 `resource.schema.json`，把 `DeliverySurface` 纳入统一资源模型。
- 在 delivery API 增加 `/surfaces` 和 `/surfaces/{surface_id}` 只读发现入口。
- 在 `/metadata` 暴露 delivery surface registry links。
- 补 contract/API 回归测试、API 接入文档、100% 路线图和任务 closeout。

## Out of Scope
- 不重写 Web/API/Bot/CLI/Skill 交付实现。
- 不接入真实 Telegram live、真实 HF Space、真实公网 API 或浏览器自动化 live 验证。
- 不承诺 CLI/Skill 直接生成标准 Markdown；它们只能标记为 partial。
- 不保存用户输入、报告正文、运行时任务状态、token 或生产日志。

## Task Package Tree
```text
TP-01 多端交付面盘点
  TP-01.01 盘点 Web/API/Bot/CLI/Skill 输出链路和一致性测试
  TP-01.02 回填任务契约与文档字段
TP-02 DeliverySurface 契约
  TP-02.01 新增 DeliverySurface schema
  TP-02.02 新增 delivery registry
  TP-02.03 扩展 resource schema 与 contracts AGENTS
TP-03 API 发现层
  TP-03.01 新增 /surfaces list/detail API
  TP-03.02 更新 /metadata 与 OpenAPI 断言
TP-04 测试与文档
  TP-04.01 补 contract/API 回归测试
  TP-04.02 更新 API 文档、100% 路线图和任务文档
TP-05 验证收口
  TP-05.01 执行本地门禁
  TP-05.02 回填 closeout 状态和验证证据
```

## Requirement Alignment
- 用户目标：按任务树持续推进“测算基础设施 100%”。
- 本任务切片：落实 IMP-11 多端交付一致性的资源发现和本地一致性门禁。
- 基础设施同构依据：Backstage catalog、OpenAPI 和 Kubernetes resource model 的组件/API/资源可发现性。
- 完成口径：本地可发现、可测试、可审计；真实 Bot/托管 Web/公网 API live 验证仍标注待执行。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 确认已有交付面与本轮边界 | 不遗漏现有 entrypoint，不夸大 partial/manual |
| TP-02 | BUILD | 建立 DeliverySurface 契约和 registry | JSON 可加载，字段被测试锁定 |
| TP-03 | BUILD | 暴露 API 发现入口 | list/detail、metadata、OpenAPI 可复核 |
| TP-04 | TEST/DOC | 同步测试和人类文档 | 文档不夸大 live 验证 |
| TP-05 | SHIP | 执行门禁并回填证据 | quick CI 与任务校验通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
