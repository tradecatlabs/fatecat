# Task Overview
- Task ID: `0083`
- Slug: `measurement-infrastructure-oidc-siem-retention-staged-gate`
- Objective: `把 0065 的 OIDC/SIEM/retention cleaner externalization baseline 推进为更硬的本地 staged evidence gate：强制 proof-ref 白名单、raw URL 禁入、production deletion marker 拒绝和 5 类反伪造负例；无真实 IdP/SIEM/retention cleaner 权限时只输出外部连通验证待执行，不声明 external live passed。`
- Status: `Done`

## In Scope
- 加固 `contracts/fate/security/externalization-evidence-contract.json` 的 live evidence proof-ref 白名单。
- 加固 `scripts/security-externalization-gate.py`，拒绝 raw URL、敏感片段和不合规 proof refs。
- 增加 OIDC raw URL 与 retention production deletion marker 反伪造负例。
- 更新 security schema invariant、目录 AGENTS、roadmap、任务索引和回归测试。

## Out of Scope
- 不接入真实 OIDC/IdP、JWKS、外部 IAM 或组织级多租户身份系统。
- 不连接真实 SIEM、WORM 存储、云日志或不可变审计平台。
- 不实现真实记录按年龄清理器，不删除任何生产或用户数据。
- 不保存真实 issuer URL、JWKS URL、SIEM endpoint、token、secret、DSN、日志 payload、报告正文或用户输入。

## Task Package Tree
```text
TP-01 SPEC: 复核 0065 与 0082 后的 security externalization 缺口
  TP-01.01 读取 security registry、externalization contract、production security policy 和 roadmap
  TP-01.02 定义 proof-ref/raw URL/production deletion non-claim 边界
TP-02 PLAN: 设计 0083 staged hardening
  TP-02.01 定义 proofRefPrefixes 和 live evidence 输入约束
  TP-02.02 定义 raw URL、retention production marker 和敏感值负例
TP-03 BUILD: 加固 contract/gate/docs
  TP-03.01 更新 contract 与 gate validation
  TP-03.02 更新 schema invariant、AGENTS、roadmap 和 task index
TP-04 TEST: 回归和门禁
  TP-04.01 更新 focused regression tests
  TP-04.02 运行 JSON、gate、pytest、ruff、secret scan、quick CI 和任务校验
TP-05 REVIEW/SHIP: 收口
  TP-05.01 回填 closeout 与剩余外部验证项
  TP-05.02 明确 git/CI 交付证据外置边界
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| 100% infra 要安全外部化证据可复核 | 复用并加固现有 security externalization evidence contract/gate |
| 不伪造 OIDC/SIEM/retention live | 默认 pending；live evidence 必须字段完整且 proof refs 脱敏 |
| 不泄露真实外部端点 | gate 拒绝 raw URL、endpoint、issuer、JWKS、payload、token/secret 等片段 |
| 不重复建安全系统 | 不新建第二套 gate；只收紧 0065 已存在的安全外部化门禁 |
| 任务树推进 | 本任务按 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 执行 |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 缺口来自 repo evidence，不靠猜测 |
| TP-01.01 | 复核 0065/0082 状态 | Done | security registry、externalization contract、policy、roadmap 已读取 |
| TP-01.02 | 定义边界 | Done | proof-ref、raw URL、production deletion non-claim 明确 |
| TP-02 | PLAN | Done | hardening 范围和反伪造策略明确 |
| TP-02.01 | proofRefPrefixes | Done | identity/SIEM/retention live schema 均定义 proof-ref 白名单 |
| TP-02.02 | 反伪造 | Done | raw URL 与 production_deleted marker 会失败 |
| TP-03 | BUILD | Done | contract、gate、schema、docs 接线完成 |
| TP-03.01 | gate 加固 | Done | proof refs、raw URL、敏感片段校验完成 |
| TP-03.02 | docs 接线 | Done | AGENTS、roadmap、task index 更新 |
| TP-04 | TEST | Done | regression、focused checks、secret scan 和 quick CI 完成 |
| TP-04.01 | regression tests | Done | 覆盖 pending、negative cases 和 contract invariants |
| TP-04.02 | validation gates | Done | JSON、gate、pytest、ruff、secret scan、quick CI 和 task validators 完成 |
| TP-05 | REVIEW/SHIP | Done | closeout 完成；git/CI 由外层交付流记录 |
| TP-05.01 | closeout | Done | 文档无 overclaim，外部验证项保留 |
| TP-05.02 | git/CI boundary | Done | 任务包不预声明 commit/push/remote CI；真实证据由外层交付汇报记录 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
