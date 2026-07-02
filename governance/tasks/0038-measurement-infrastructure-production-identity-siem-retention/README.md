# Task Overview
- Task ID: `0038`
- Slug: `measurement-infrastructure-production-identity-siem-retention`
- Objective: `把 D8 安全/隐私从 scoped RBAC、secret scan、audit_event 和 retention baseline 推进为本地可验证的生产身份/SIEM/retention 准入基线：新增生产身份外部化策略、OIDC/IdP 准入 contract、SIEM/不可变审计存储 contract、retention 自动清理计划 contract、OWASP API security regression pack gate，并接入 security registry、production-readiness、quick CI、API 文档、roadmap 与任务 closeout；不接真实 OIDC/外部 SIEM、不删除真实数据、不伪造生产 live 证据。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/security/production-security-policy.json`，定义生产身份、OIDC/IdP、SIEM、不可变审计、retention 自动清理和 OWASP API Top 10 回归策略。
- 扩展 `contracts/fate/security/schemas/security-control.schema.json` 与 `registry.json`，登记 identity、siem、retention cleanup、OWASP API regression 控制项。
- 新增 `scripts/production-security-gate.py/.sh`，验证策略、registry、schema、OWASP 映射和隐私边界。
- 扩展 `scripts/production-readiness.sh`，在启用公网多租户、SIEM export 或 record retention days 时执行静态准入检查。
- 接入 `scripts/local-ci.sh --profile quick`、API/protocol tests、API 文档、roadmap、AGENTS 和任务 closeout。

## Out of Scope
- 不接真实 OIDC/IdP、JWKS、外部 IAM、外部 SIEM、WORM 存储、云日志平台或生产账号。
- 不实现记录按年龄自动清理器，不删除真实数据，不改变当前显式删除 baseline。
- 不做第三方渗透测试、WAF/网关真实策略验证、生产 live smoke 或远端 CI 当前 diff 验证。
- 不输出真实 token、secret、DSN、SIEM endpoint、请求体、用户输入或报告正文。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 D8 安全/隐私现状、security registry、production readiness 和 roadmap 缺口
TP-02 生产安全 contract baseline
  TP-02.01 新增 production security policy
  TP-02.02 扩展 SecurityControl schema 和 registry 控制项
TP-03 gate 与 production readiness
  TP-03.01 新增 production-security-gate
  TP-03.02 扩展 production-readiness 静态准入检查
TP-04 tests、CI 与文档
  TP-04.01 新增/更新 regression tests 并接入 quick CI
  TP-04.02 同步 env 示例、AGENTS、API 文档和 roadmap
TP-05 验证与 closeout
  TP-05.01 运行 focused validation 和 local quick CI
  TP-05.02 回填任务包并生成 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 D8 安全、隐私与合规边界。
- 对齐 OWASP API Security Top 10 2023：把 10 个风险项映射到本地检查或明确外部待验证。
- 对齐生产诚实口径：本轮是本地 contract/gate baseline；真实 OIDC、SIEM、自动清理器和 live smoke 仍待外部环境。
- 对齐隐私边界：contract、registry、gate output 和 API 响应只输出变量名、控制项和摘要，不输出真实凭证或用户数据。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 security registry、security smoke、production readiness、D8 roadmap 和现有 tests。 |
| TP-02 | Done | `production-security-policy.json`、schema 扩展和 4 个 SecurityControl 已新增。 |
| TP-03 | Done | `production-security-gate` 与 `production-readiness` 静态准入检查已落地。 |
| TP-04 | Done | tests、quick CI、env examples、AGENTS、API docs 和 roadmap 已同步。 |
| TP-05 | Done | focused validation 与 local quick CI 已通过；closeout packet 待生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
