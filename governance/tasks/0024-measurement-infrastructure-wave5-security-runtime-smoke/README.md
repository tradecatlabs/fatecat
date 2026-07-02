# Task Overview
- Task ID: `0024`
- Slug: `measurement-infrastructure-wave5-security-runtime-smoke`
- Objective: `把 SecurityControl 从资源发现推进到本地可执行安全 smoke：用 TestClient 验证记录接口 token/owner 边界、响应安全头、请求体限制、限流，并串联 privacy/source/public-release 本地门禁，输出机器可读 summary JSON；不伪造真实生产域名、真实 token 或 Bot live smoke。`
- Status: `Done`

## In Scope
- 新增 `scripts/security-smoke.py` / `.sh`。
- smoke 使用 FastAPI `TestClient` 验证响应安全头、请求体大小限制、限流、记录接口禁用开关、user token owner 边界和 `/security` registry metadata。
- smoke 默认串联 privacy fixtures、source hygiene、public release policy 三类本地文件门禁。
- smoke 输出机器可读 JSON 到本地运行态目录或指定路径。
- 在 `contracts/fate/security/registry.json` metadata 中登记 smoke command/scope/output。
- 补回归测试、quick CI 接入、API 文档、roadmap 和任务 closeout。

## Out of Scope
- 不伪造真实生产域名、真实 API token、真实 Bot token、Webhook 或线上账号权限。
- 不实现专用 secret scanner、审计日志、retention、OAuth/OIDC、RBAC 或云端 WAF。
- 不修改鉴权业务模型之外的算法、报告结构、provider protocol 或交付面 UI。

## Task Package Tree
```text
TP-01 Security runtime 缺口盘点
  TP-01.01 盘点 registry、API、权限、header、限流、隐私门禁和 roadmap 缺口
  TP-01.02 回填任务契约与任务树
TP-02 本地 smoke 实现
  TP-02.01 新增 security smoke 脚本
  TP-02.02 将 smoke 登记到 registry/AGENTS
TP-03 测试与文档
  TP-03.01 新增 security smoke 回归测试
  TP-03.02 更新 contract/API tests 与 quick CI
  TP-03.03 更新 API 文档与 100% 路线图
TP-04 验证收口
  TP-04.01 执行 smoke、focused tests、ruff/format、quick CI 和 diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 用户目标：持续把 FateCat 推进为测算基础设施。
- 本任务切片：把安全资源从“可发现”推进到“本地可执行 smoke 可证明”，覆盖当前已落地的 token/owner、header、body limit、rate limit 和本地隐私/发布文件门禁。
- 完成口径：本地安全 smoke 可执行、可测试、可导出 JSON；真实生产域名、真实 token、Bot live、OAuth/OIDC、RBAC、审计日志和专用 secret scanner 仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确本地安全 smoke 范围 | 不夸大为生产安全体系完成 |
| TP-02 | BUILD | 新增 smoke 脚本与 registry metadata | JSON 输出可复核 |
| TP-03 | TEST/DOC | tests/docs/quick CI 同步 | focused tests 通过 |
| TP-04 | SHIP | 执行门禁并 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
