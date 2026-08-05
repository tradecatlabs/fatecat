---
id: SOP-REL-EXTERNAL-VALIDATION-CLOSE
type: process
status: current
execution_status: blocked
owner: governance
route_key: close_external_validation
route_aliases: ["关闭外部验证项", "生成 operator packet", "提交 proof ref"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P14D
---

# 关闭外部验证事项

## 任务定义
把 audit bundle 中的 pending external validations 转成 owner 工作队列、category runbook、operator packet、proof-ref/live-proof evidence 和关闭结论。

## 当前状态
本地计划、模板和 gate 全部可用；真实 proof 依赖外部 token、账号、服务、权限和人工操作，当前可能 blocked。

## 适用场景
生产 API/Bot/Postgres/OIDC/SIEM/OTel/Vault、developer portal、第三方审计等外部事项补证。

## 输入要求
`pending-external-validations.json`、当前 commit、owner、credential 名称、脱敏 proof refs、artifact hash 和 live evidence。

## 前置条件
current audit bundle 最新；每项 owner/权限明确；operator 获得授权；证据 schema 和时效已确认。

## 默认工具链
closure gate -> work queue -> proof-ref gate -> category runbooks -> operator packet -> live-proof gate -> closure evidence summary。

## 固定路径
`scripts/external-validation-*`、对应 contracts、`infra/runtime/local-state/exports/external-validation/<short-sha>/`。

## 成熟参数
所有 `--expected-commit` 固定 HEAD；proof 只接受脱敏 handle/hash；缺输入时 gate 保持 blocked而非默认通过。

## 分步执行流程
1. 从 pending JSON 生成 closure plan。
2. 生成 owner/category work queue 和 runbooks。
3. 生成 operator execution packet。
4. Operator 在外部系统执行并提交 proof-ref/live bundle。
5. 运行 proof/live gates和 closure summary，确认每个 occurrence关闭。

## 幂等与增量策略
work item ID 稳定；已验证且输入未变的项可复用；commit、runbook、artifact或时效变化使证据 stale。

## 限速与并发规则
不同外部系统可由不同 owner 并行；同一 work item 只允许一个 active operator；API 调用遵守各服务限速。

## 输出目录
`infra/runtime/local-state/exports/external-validation/<short-sha>/`；真实凭证留外部 secret store。

## 命名规范
artifact 由 workItemId/category/commit 组成；proof ref 不使用 raw URL/token。

## 质量验收门禁
work queue 无空 owner、proof/live/current commit/hash/redaction/expiry/runbook 全通过，closure summary 无 required pending。

## 失败处理
proof 缺失、stale、hash/commit 不匹配、redaction失败或 live 未通过时保留 blocked。

## 恢复与重试策略
只重做失败 work item；冻结其他 verified 节点；外部瞬时失败按 runbook 有界重试。

## 安全边界
不保存 token/DSN/private URL/个人信息；本地工具不自动连接真实系统，operator 才执行授权副作用。

## 临时文件清理
删除 operator 本地 secret/env和原始响应；保留脱敏 proof bundle与 gate summary。

## 运行记录登记
记录 workItemId、owner、category、commit、proof refs/hash、时间、gate、staleReason和关闭状态。

## 明确禁止事项
- 禁止伪造 proof/live。
- 禁止空 proofRef 关闭事项。
- 禁止将 schema accepted 等同生产 live passed。
