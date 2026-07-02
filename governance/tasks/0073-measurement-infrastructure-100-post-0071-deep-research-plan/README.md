# Task Overview

- Task ID: `0073`
- Slug: `measurement-infrastructure-100-post-0071-deep-research-plan`
- Objective: 基于当前 `main` worktree、0071 Postgres live smoke 已完成事实、0072 worker lease smoke 已完成事实，以及 OpenAPI、AsyncAPI、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、OWASP、NIST、SLSA、CycloneDX、CNCF 平台工程等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、任务树、执行顺序、验收门禁和不可伪造证据口径。
- Status: `Done`

## In Scope

- 复核当前仓库事实、任务索引和 0071/0072 后的 durable runtime 状态。
- 用外部基础设施一手资料重新定义 FateCat 100% 基础设施终态。
- 把调研结论落盘到 `RESEARCH.md` 和主路线图 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 明确 100% 任务树、优先顺序、完成门禁、不可伪造证据和失败判定。

## Out of Scope

- 不实现业务代码。
- 不提交或推送 Git。
- 不把 0072 outbox worker lease smoke 写成 job execution worker lease 或生产完成。
- 不伪造 Bot live、真实公网 webhook、OIDC/IdP、SIEM、OTel backend、Vault/KMS、第三方审计或生产 exactly-once。

## Task Package Tree

```text
TP-01 现状复核
  TP-01.01 读取 Git 状态、任务索引和 100% 路线图
  TP-01.02 标记 0071 与 0072 已交付，但仍非生产完成
TP-02 外部同构调研
  TP-02.01 采集基础设施一手资料
  TP-02.02 提炼 API、事件、控制面、运行时、SRE、安全、供应链、审计的共同能力
TP-03 FateCat 100% 计划
  TP-03.01 形成资源成熟度矩阵
  TP-03.02 形成完整任务树和执行顺序
  TP-03.03 形成不可伪造验收口径和失败判定
TP-04 文档落盘与验证
  TP-04.01 写入 RESEARCH.md
  TP-04.02 更新主路线图 0.9 章节
  TP-04.03 运行任务文档校验
```

## Requirement Alignment

- 用户要求：深度调研查询相关资料，制作实现 100% 基础设施所需的完整实现计划。
- 项目定位：FateCat 是面向 Agent 与应用开发者的测算基础设施。
- auto-tasks 契约：本任务是 planning-only 任务包，不越界实现、不伪造证据。

## Task Package Overview

| Node | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | `git status --short --branch`、`governance/tasks/INDEX.md`、主路线图读取 |
| TP-02 | Done | `RESEARCH.md` 外部资料矩阵 |
| TP-03 | Done | `RESEARCH.md` 资源矩阵、任务树、执行顺序、验收口径 |
| TP-04 | Done | 主路线图 `0.9` 章节与任务文档校验 |

## Reading Order

1. `README.md`
2. `RESEARCH.md`
3. `CONTEXT.md`
4. `PLAN.md`
5. `ACCEPTANCE.md`
6. `ACCEPTANCE_CHECKLIST.md`
7. `TODO.md`
8. `STATUS.md`
