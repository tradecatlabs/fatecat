# Task Overview
- Task ID: `0028`
- Slug: `measurement-infrastructure-rbac-policy`
- Objective: `把记录接口的隐含 admin/user/owner 权限边界推进为本地可验证 RBAC baseline：显式 record scopes、兼容旧 user token、支持 scoped FATE_API_USER_TOKENS、登记 control.rbac_policy，补回归测试、生产预检兼容、文档和 closeout；不实现 OAuth/OIDC、外部 IdP 或多租户身份系统。`
- Status: `Done`

## In Scope
- 在记录接口建立显式 record scopes：`record.read`、`record.list`、`record.write`、`record.delete`。
- 兼容旧 `FATE_API_USER_TOKENS` 值形态 `用户ID:占位令牌`，默认拥有全部 record scopes，仍受 owner 边界约束。
- 新增 scoped token 值形态：`用户ID:占位令牌:record.read|record.list`。
- 在记录创建、读取、列表、删除入口执行 scope 检查。
- 登记 `control.rbac_policy` SecurityControl，并更新 schema、文档、生产预检脚本和回归测试。

## Out of Scope
- 不实现 OAuth/OIDC、外部 IdP、组织级多租户 IAM 或生产身份系统。
- 不修改数据库 schema。
- 不引入新依赖。
- 不改变报告计算、Web UI、Bot 或 provider 行为。
- 不输出真实 token、用户 ID 原文、请求体或报告正文。

## Task Package Tree
```text
TP-01 RBAC 现状和边界确认
  TP-01.01 盘点现有 token、owner、record 接口和 security registry
  TP-01.02 回填任务契约、范围和验证计划
TP-02 scoped RBAC runtime 实现
  TP-02.01 新增 ApiPrincipal scopes、record scope 常量和 user token parser
  TP-02.02 在 record write/read/list/delete 入口接入 scope gate
  TP-02.03 更新 audit principal metadata 和 production-readiness scoped token 格式校验
TP-03 契约、测试和文档
  TP-03.01 登记 rbac SecurityControl 和 schema controlType
  TP-03.02 新增 scoped token 行为回归和 registry contract 断言
  TP-03.03 更新 API 接入文档、security AGENTS 和 100% roadmap
TP-04 验证收口
  TP-04.01 执行 JSON、focused tests、shell syntax、ruff/format、secret scan、quick CI、diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中 `MI-09.01 scoped RBAC baseline`。
- 对齐 OWASP API 的 BOLA/BFLA 风险治理方向：记录接口必须同时检查身份、owner 和操作 scope。
- 本任务只把本地记录接口从共享 token/owner 检查升级为 scoped RBAC baseline；生产 OIDC/IAM 是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确本地 RBAC 范围 | 不扩成 OIDC/IAM |
| TP-02 | BUILD | 实现 scoped record permissions | 旧 token 兼容，新 scope 生效 |
| TP-03 | TEST/DOC | registry/tests/docs 同步 | contract tests 通过 |
| TP-04 | SHIP | 执行门禁并 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
