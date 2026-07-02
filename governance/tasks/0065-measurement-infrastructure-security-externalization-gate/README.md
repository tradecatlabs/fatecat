# Task Overview

- Task ID: `0065`
- Slug: `measurement-infrastructure-security-externalization-gate`
- Objective: `执行 0061 后续任务树的 Security externalization P0 切片：新增 OIDC/SIEM/retention cleaner 外部化证据契约、反伪造 gate、回归测试、quick CI 接线和文档 closeout；本任务不接入真实 IdP、SIEM、不可变审计平台或真实数据清理器，不把本地 scoped token 写成生产身份。`
- Status: `Done`

## In Scope

- 新增 Security externalization evidence contract。
- 新增 `security-externalization-gate` Python/sh wrapper。
- 覆盖 OIDC、SIEM、retention cleaner 的 dry-run contract、external pending、live evidence 必备字段和负向伪造检查。
- 更新 security registry/schema/AGENTS、scripts AGENTS、local-ci quick、API 文档、100% roadmap 和任务索引。
- 运行 gate、focused regression、syntax/lint、secret scan、task validators 和 quick local CI。

## Out of Scope

- 不连接真实 OIDC/IdP、JWKS、SIEM、WORM 存储、云日志或生产数据库。
- 不读取真实 `.env`、token、secret、DSN、私钥、证书或 webhook secret。
- 不删除真实记录、审计日志、报告任务或生产数据。
- 不声明生产身份、外部 SIEM、不可变审计或 retention cleaner live 已完成。

## Requirement Alignment

- 对齐 0061 推荐任务：`0065 security externalization`，最小交付物为 OIDC/SIEM/retention cleaner implementation plan + negative tests，且不能用本地 token 代替 IdP。
- 对齐当前安全事实：已有 scoped RBAC、production-security-policy、production-security-gate 和 OWASP mapping；仍缺外部平台 live 证据契约和反伪造验证。
- 对齐基础设施定位：安全能力必须是可发现、可验证、可审计的 SecurityControl，不是 README 中的生产承诺。

## Task Package Tree

```text
TP-01 Security context
  TP-01.01 复核 0061/0064、security registry、production security gate、local-ci 和 API 文档
TP-02 Evidence contract baseline
  TP-02.01 新增 security externalization evidence contract
  TP-02.02 更新 security registry、schema 和 AGENTS
TP-03 Gate、测试和 CI
  TP-03.01 新增 security-externalization-gate Python/sh wrapper
  TP-03.02 新增 regression tests 覆盖 contract、CLI、negative fake evidence
  TP-03.03 接入 local-ci quick artifact
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、scripts AGENTS 和 INDEX
  TP-04.02 运行 validators、focused tests、lint/hygiene、quick local CI 并收口
```

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核安全外部化现状和 0065 边界。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 读取 0061/0064、security registry、production-security-gate、local-ci 和 API 文档。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 新增外部化证据契约 baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 OIDC/SIEM/retention cleaner evidence contract。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 更新 security registry、schema 和 AGENTS。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | Gate、测试和 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 security-externalization-gate。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 新增 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并收口。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
