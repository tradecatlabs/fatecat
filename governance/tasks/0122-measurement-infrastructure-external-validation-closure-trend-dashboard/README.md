# Task Overview

0122 执行 `MI-100.A.04 closure trend dashboard and stale owner alert`：把 0119 work queue、0120 proof-ref gate 和 0121 category runbooks 继续提升为可本地复核的 owner/category/status 趋势 dashboard 与 stale owner alert summary。

该任务只做本地控制面。stale alert ready 不等于 production live passed；真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、外部 issue tracker 和第三方审计仍必须由后续 live gate 或人工审计提供外部证据。

## In Scope

- 新增 closure trend dashboard contract。
- 新增 closure trend dashboard Python generator 与 shell wrapper。
- 聚合 closure plan、work queue、proof-ref gate 和 category runbooks。
- 输出 owner/category/status dashboard、stale alert、trend delta 和 blocked ship gate。
- 接入 local-ci quick artifact。
- 接入 measurement infrastructure certification 的 audit domain。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live validation。
- 不发送真实通知、不连接外部 issue tracker。
- 不保存真实 token、secret、DSN、raw URL、生产日志 payload 或用户报告正文。
- 不把 alert acknowledgement 写成 live evidence closure。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and source confirmation
TP-02 contract/script/dashboard gate
TP-03 local-ci/certification/docs wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 聚合 closure plan/work queue/proof-ref/runbooks | `external-validation-closure-trend-dashboard.py` 必须消费四个上游 artifact |
| 按 owner/category/status 输出趋势 | `ownerDashboard`、`categoryDashboard`、`statusDashboard` |
| stale owner alert | `staleAlerts`、`alertStatus`、`alertGate` |
| 不能发送真实通知 | `alertGate.deliveryMode=local_dry_run_only`、`deliveryStatus=not_sent` |
| 不伪造 live | `shipGate.status=blocked` 和 certification blocked 保持不变 |

## Task Package Overview

本任务补齐 “work queue -> proof-ref -> category runbook -> stale alert/trend -> category live gate” 中的本地运营视图。它让 operator 和审计人员看到每个 owner/category 的未闭合状态、age、proof-ref missing、manual triage、policy guardrail 和 category live pending 分布。

## Reading Order

1. `PLAN.md`
2. `CONTEXT.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
