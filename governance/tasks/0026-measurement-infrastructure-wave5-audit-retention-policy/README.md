# Task Overview
- Task ID: `0026`
- Slug: `measurement-infrastructure-wave5-audit-retention-policy`
- Objective: `把 SecurityControl 的审计日志与 retention policy 从后续缺口推进到本地可验证基线：为记录读写/删除、报告 job 提交/取消等关键动作输出脱敏结构化 audit_event，登记 retention policy 和 audit log SecurityControl，补回归测试、quick CI、文档和任务 closeout；不接入外部 SIEM、不保存真实请求体、不伪造生产审计平台。`
- Status: `Done`

## In Scope
- 新增本地结构化 `audit_event` 日志 helper。
- 对记录创建、读取、列表、删除，以及报告 job 提交、取消输出脱敏 audit event。
- 资源 ID、用户 ID 和 job ID 不输出原文，只输出短哈希；不记录 token、请求体、报告正文、姓名或出生地区。
- 在 `contracts/fate/security/registry.json` 登记 `control.audit_event_log` 与 `control.retention_policy`。
- 在 `security-control.schema.json` 增加 `audit_log` 与 `retention` 控制类型。
- 补 API/contract 回归测试、API 文档、100% roadmap、任务 closeout。

## Out of Scope
- 不接入外部 SIEM、云端日志平台、不可变审计存储或生产日志 retention 后端。
- 不实现记录按年龄自动清理；当前记录默认仍是显式删除模式。
- 不保存真实请求体、报告正文、token、secret、姓名、出生地区或生产日志。
- 不实现 OAuth/OIDC、RBAC 或真实生产域名/Bot live 验证。

## Task Package Tree
```text
TP-01 Audit/retention 缺口盘点
  TP-01.01 盘点记录接口、报告 job、security registry 和 roadmap 缺口
  TP-01.02 回填任务契约与任务树
TP-02 Runtime audit event 实现
  TP-02.01 新增脱敏 audit_event helper
  TP-02.02 接入记录接口和报告 job 生命周期
TP-03 契约、测试与文档
  TP-03.01 登记 audit_log / retention SecurityControl
  TP-03.02 新增 audit/retention 回归测试
  TP-03.03 更新 AGENTS、API 文档和 100% 路线图
TP-04 验证收口
  TP-04.01 执行 focused tests、secret scan、ruff/format、quick CI 和 diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 用户目标：持续把 FateCat 推进为测算基础设施。
- 本任务切片：补齐 IMP-10 中可本地实现的 audit log 与 retention policy baseline。
- 完成口径：关键动作可输出脱敏 audit_event，SecurityControl 可发现，retention 口径可复核；外部 SIEM、不可变审计存储、生产日志 retention、自动记录清理和 OAuth/RBAC 仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确 audit/retention 范围 | 不夸大为生产审计平台 |
| TP-02 | BUILD | 新增 runtime audit event | 不输出敏感原文 |
| TP-03 | TEST/DOC | registry/schema/tests/docs 同步 | focused tests 通过 |
| TP-04 | SHIP | 执行门禁并 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
