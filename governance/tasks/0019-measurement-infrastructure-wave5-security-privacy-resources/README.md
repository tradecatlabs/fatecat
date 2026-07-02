# Task Overview
- Task ID: `0019`
- Slug: `measurement-infrastructure-wave5-security-privacy-resources`
- Objective: `把现有 token 权限、CORS、限流、请求体限制、响应安全头、隐私示例、source hygiene、public release policy 和 production readiness 门禁资源化为 SecurityControl 发现层，提供 schema、registry、API 入口、文档和回归测试。`
- Status: `In Progress`

## In Scope
- 新增 `contracts/fate/security/` 作为安全、隐私与发布门禁资源真相源。
- 新增 `SecurityControl` schema 与 registry。
- 扩展 `resource.schema.json`，把 `SecurityControl` 纳入统一资源模型。
- 在 delivery API 增加 `/security` 和 `/security/{control_id}` 只读发现入口。
- 在 `/metadata` 暴露 security registry links。
- 补 contract/API 回归测试、API 接入文档、100% 路线图和任务 closeout。

## Out of Scope
- 不改现有 token 鉴权执行语义。
- 不接入 OAuth/OIDC、RBAC、WAF、SIEM、外部 secret scanner 或云端权限系统。
- 不伪造真实域名、真实 token、真实 Bot live smoke 或远端 CI 通过证据。
- 不把生产凭证、webhook、DSN、私钥或扫描命中值写入 registry。

## Task Package Tree
```text
TP-01 Security/Privacy/ReleaseGate 盘点
  TP-01.01 盘点现有 token、CORS、限流、请求体、响应头、隐私和发布门禁
  TP-01.02 回填任务契约与文档字段
TP-02 SecurityControl 契约
  TP-02.01 新增 SecurityControl schema
  TP-02.02 新增 security registry
  TP-02.03 扩展 resource schema 与 contracts AGENTS
TP-03 API 发现层
  TP-03.01 新增 /security list/detail API
  TP-03.02 更新 /metadata 与 OpenAPI 断言
TP-04 测试与文档
  TP-04.01 补 contract/API 回归测试
  TP-04.02 更新 API 文档、100% 路线图和任务文档
TP-05 验证收口
  TP-05.01 执行 focused tests、lint/type 和 quick CI
  TP-05.02 回填 closeout 状态和验证证据
```

## Requirement Alignment
- 用户目标：制作实现 100% 测算基础设施所需完整计划，并持续推进可落地切片。
- 本任务切片：落实 IMP-10 安全、隐私与权限的资源发现层。
- 基础设施同构依据：OWASP API Security、SLSA、Google SRE、OpenAPI、Backstage/Kubernetes 资源发现模型。
- 完成口径：本地可发现、可测试、可审计；真实外部生产验证仍明确标注待执行。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 确认已有控制与本轮边界 | 不遗漏现有门禁，不扩大生产承诺 |
| TP-02 | BUILD | 建立 SecurityControl 契约和 registry | JSON 可加载，字段被测试锁定 |
| TP-03 | BUILD | 暴露 API 发现入口 | list/detail、metadata、OpenAPI 可复核 |
| TP-04 | TEST/DOC | 同步测试和人类文档 | 文档不夸大外部验证 |
| TP-05 | SHIP | 执行门禁并回填证据 | quick CI 与任务校验通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
