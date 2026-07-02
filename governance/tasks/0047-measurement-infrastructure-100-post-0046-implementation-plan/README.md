# Task Overview

基于当前 `main` worktree、`0009-0046` 已完成任务、远端 CI 当前状态和外部基础设施一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划。

## In Scope

- 当前仓库事实、远端 CI 状态和 0046 closeout 后的剩余差距复核。
- 外部基础设施一手资料同构调研。
- 主路线图 post-0046 状态、剩余任务树和不可伪造证据口径刷新。
- 0047 任务包、任务索引和校验证据维护。

## Out of Scope

- Telegram live、registry attestation、OIDC/SIEM、OpenTelemetry collector、生产告警平台或新测算 provider 的真实实现。
- 业务源码、provider 计算逻辑、API 行为、Git 历史或远端状态修改。
- 把计划、contract、local baseline 或 pending evidence 写成生产完成。

## Task Package Tree

```text
TP-01 当前事实复核
  TP-01.01 git/workflow/release 状态复核
TP-02 外部资料调研
  TP-02.01 成熟基础设施同构矩阵
TP-03 路线图刷新
  TP-03.01 post-0046 剩余任务树和 100% 验收口径
TP-04 收口验证
  TP-04.01 任务文档、索引和 markdown 校验
```

## Requirement Alignment

| User Requirement | Task Response |
| --- | --- |
| 深度调研查询相关资料 | 使用官方/一手基础设施资料建立同构矩阵 |
| 制作 100% 基础设施完整实现计划 | 刷新主路线图和 `MI-NEXT-*` 剩余任务树 |
| 使用 auto-tasks | 新增 0047 任务包并接入任务索引 |
| 不伪造生产证据 | Acceptance/Bot/registry/OIDC/SIEM/monitoring 均按真实状态标注 |

## Task Package Overview

本任务是计划刷新任务，不是实现任务。它的完成标准是：路线图能直接指导下一批基础设施实现任务创建；审计人员能看出哪些已完成、哪些本地 baseline、哪些仍需外部连通或人工权限。

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `TODO.md`
5. `ACCEPTANCE.md`
6. `ACCEPTANCE_CHECKLIST.md`
7. `STATUS.md`

## Current Facts

- 当前分支：`main`
- 当前提交：`2b3f4c8`
- 当前 worktree：clean at task start
- 0046 状态：release clean/commit/push 已完成
- 远端 Container workflow：current commit `2b3f4c8` 已通过
- 远端 Acceptance workflow：baseline commit `2b3f4c8` 已通过，run `28575852876`

## External Research Basis

本任务以成熟基础设施同构为方法，不按“继续堆测算模块”规划：

- OpenAPI：机器可读 API contract、schema、示例、版本。
- Stripe：幂等请求和 webhook 事件交付。
- Temporal：durable execution、retry policy、长流程恢复。
- Kubernetes controller：desired/current state reconciliation。
- Terraform provider：provider source、version、plugin lifecycle。
- Backstage catalog：Component/API/Resource/System 可发现模型。
- OpenTelemetry：traces、metrics、logs 三信号。
- Google SRE：SLO 和 error budget。
- DORA：部署频率、变更前置时间、失败率、恢复时间。
- SLSA/CycloneDX：provenance、attestation、SBOM。
- OWASP API Security / NIST SSDF：API 安全、软件供应链和安全开发生命周期。
- CloudEvents：事件 envelope 标准化。

## Completion Definition

- 主路线图反映 post-0046 真实状态。
- 未来任务不再绑定过期编号，而用 `MI-NEXT-*` 表达可按顺序创建的实现切片。
- 任务包记录外部资料、当前事实、剩余风险和不可伪造证据口径。
- 文档校验、Markdown whitespace 和 git 状态可复核。
