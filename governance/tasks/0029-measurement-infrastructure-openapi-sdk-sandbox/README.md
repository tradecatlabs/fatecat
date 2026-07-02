# Task Overview
- Task ID: `0029`
- Slug: `measurement-infrastructure-openapi-sdk-sandbox`
- Objective: `把开发者接入面推进为本地可验证 baseline：提供 OpenAPI 导出脚本、developer docs smoke、sandbox fixture、curl/Python/Node/Agent 示例，接入 quick CI，并回填任务包与 closeout；不实现公网 SDK 发布、真实 sandbox token 服务或远端开发者门户。`
- Status: `Done`

## In Scope
- 新增开发者 sandbox fixture 契约：`contracts/fate/developer/sandbox.json`。
- 新增开发者示例文档和最小示例：curl、Python、Node、Agent tool call。
- 新增 OpenAPI 导出脚本并校验开发者必备路径。
- 新增 developer docs smoke，使用 FastAPI `TestClient` 执行 sandbox fixture 和示例静态检查。
- 将 developer docs smoke 和回归测试接入 quick CI。
- 更新 API 接入文档、100% roadmap、目录级 AGENTS 和任务 closeout。

## Out of Scope
- 不发布 pip/npm/HTTP SDK 包。
- 不实现公网 sandbox token 服务、开发者门户、API key 自助开通或真实生产租户。
- 不引入真实生产 URL、真实 token、真实用户输入、非北京真实地区或报告正文 fixture。
- 不重构 FastAPI 路由、不改变 capability 执行行为。
- 不实现固定输出 snapshot；本轮只锁定响应 shape 和基础字段。

## Task Package Tree
```text
TP-01 开发者接入现状确认
  TP-01.01 盘点 OpenAPI、API 文档、示例和 CI 入口
  TP-01.02 回填任务契约、范围和验证计划
TP-02 开发者契约与示例
  TP-02.01 新增 developer sandbox fixture
  TP-02.02 新增 curl/Python/Node/Agent 最小示例
TP-03 OpenAPI 与 docs smoke
  TP-03.01 新增 OpenAPI 导出脚本
  TP-03.02 新增 developer docs smoke 脚本
  TP-03.03 新增回归测试并接入 quick CI
TP-04 文档与收口
  TP-04.01 更新 API 文档、roadmap 和目录级 AGENTS
  TP-04.02 执行门禁、任务验证和 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中 `MI-01 开发者平台`。
- 对齐测算基础设施目标：外部开发者不读源码，也能看到机器契约、示例、sandbox 输入和本地验证命令。
- 本任务只完成本地可验证 baseline；公网开发者平台、发布版 SDK 和生产 sandbox 仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确开发者接入缺口 | 不把本地 baseline 写成生产门户 |
| TP-02 | BUILD | 增加 sandbox fixture 和示例 | 只使用北京/测试样本 |
| TP-03 | BUILD/TEST | OpenAPI 导出、docs smoke、quick CI | TestClient smoke 可重复执行 |
| TP-04 | DOC/SHIP | 文档同步和 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
