# Task Overview
- Task ID: `0025`
- Slug: `measurement-infrastructure-wave5-secret-scan-gate`
- Objective: `把 SecurityControl 的专用 secret scanner 从后续缺口推进到本地可执行门禁：扫描 tracked first-party 文件中的真实密钥、高熵 token、私钥/证书、DSN 和 webhook 风险，输出机器可读 summary JSON，接入 security registry、quick CI、回归测试和文档；不读取真实 .env、不输出密钥原文、不替代真实生产凭证审计。`
- Status: `Done`

## In Scope
- 新增 `scripts/secret-scan.py` / `.sh`。
- 新增 `contracts/fate/security/secret-scan-allowlist.json`，只记录占位符、reference repo/archive 排除边界和允许示例片段。
- secret scanner 扫描 tracked 与未跟踪但未被 gitignore 排除的一线文本文件，排除 reference repos、archive 和二进制/大文件。
- 输出机器可读 JSON，包含路径、行号、规则、severity、短指纹和脱敏长度，不输出疑似密钥原文。
- 在 `contracts/fate/security/registry.json` 登记 `control.secret_scan_gate`，更新 schema、API/contract tests、quick CI、AGENTS 和路线图文档。

## Out of Scope
- 不读取 ignored `.env`、`.env.*`、生产 secret store 或云端凭证。
- 不替代 GitHub secret scanning、gitleaks/trufflehog 等云端/供应链扫描器。
- 不实现审计日志、retention、OAuth/OIDC、RBAC 或真实生产凭证审计。
- 不输出疑似密钥原文，不把本地启发式扫描写成生产安全 100%。

## Task Package Tree
```text
TP-01 Secret scan 缺口盘点
  TP-01.01 盘点 SecurityControl、source hygiene、release gate 和 secret scanner 缺口
  TP-01.02 回填任务契约与任务树
TP-02 Scanner 实现
  TP-02.01 新增 secret-scan 脚本与脱敏 summary
  TP-02.02 新增 allowlist 并处理占位符/函数调用误报
TP-03 契约、测试与文档
  TP-03.01 登记 SecurityControl 和 schema controlType
  TP-03.02 新增 scanner 回归测试并接入 quick CI
  TP-03.03 更新 AGENTS、API 文档和 100% 路线图
TP-04 验证收口
  TP-04.01 执行 scanner、focused tests、ruff/format、quick CI 和 diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 用户目标：持续把 FateCat 推进为测算基础设施。
- 本任务切片：补齐 IMP-10 中可本地实现的“专用 secret scanner”缺口。
- 完成口径：本地 secret scanner 有脚本、JSON summary、SecurityControl 登记、quick CI、回归测试和文档；审计日志、retention、OAuth/OIDC、RBAC、真实生产域名/CORS/token/Bot live 仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确 scanner 范围和边界 | 不伪造生产凭证审计 |
| TP-02 | BUILD | 新增 scanner 与 allowlist | 当前 worktree 0 finding |
| TP-03 | TEST/DOC | registry/schema/API/tests/docs/quick CI 同步 | focused tests 通过 |
| TP-04 | SHIP | 执行门禁并 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
