# Acceptance Checklist

# Global Standards

- [x] 不保存真实 token、secret、DSN、raw URL、private key 或生产日志 payload。
- [x] 不把 stale alert 写成 production live passed。
- [x] 不发送真实通知或创建外部 issue。
- [x] 新入口有 contract、test、AGENTS、local-ci 和 certification 接线。

# Task Package Checklists

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.04|closure trend dashboard|stale owner alert" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 不扩大到真实外部通知或 live validation。

- [x] 确认 0122 只覆盖 dashboard/alert 控制面。
- [x] 确认上游真相源为 closure plan/work queue/proof-ref gate/category runbooks。

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-closure-trend-dashboard" contracts scripts`

Gate: alert ready 仍保持 blocked。

- [x] Contract 定义 required output fields。
- [x] Script 校验 input kind 与 category runbook 覆盖。
- [x] Script 计算 owner/category/status dashboard。
- [x] Script 计算 proof-ref missing、manual triage、policy guardrail、category live pending 与 stale owner alert。
- [x] Script 拒绝 raw URL、token/secret/DSN/private-key marker。

## TP-03 Wiring

Verify: `rg -n "externalValidationClosureTrendDashboard|external-validation-closure-trend-dashboard" scripts tests contracts governance`

Gate: local-ci 与 certification 都消费新 artifact。

- [x] local-ci quick 运行 dashboard gate。
- [x] local-ci summary 记录 `externalValidationClosureTrendDashboard`。
- [x] Certification audit domain 要求 dashboard artifact。
- [x] AGENTS 与 task index 已更新。

## TP-04 Validation

Verify: targeted pytest、real gate chain、quick CI。

Gate: quick CI passed 且 certification 仍 blocked。

- [x] Ruff check passed.
- [x] Ruff format check passed.
- [x] Targeted pytest passed.
- [x] Secret scan passed.
- [x] Real gate chain passed.
- [x] local quick CI passed.
- [x] Task docs closeout validation passed.

## TP-05 Delivery Package

Verify: `git status --short --branch` and post-commit quick CI summary.

Gate: 远端 CI 结果不写回仓库，推送后单独观察并在交付汇报报告。

- [x] Commit created.
- [x] Post-commit quick CI passed on clean HEAD.
- [x] Remote CI observation kept out of repository evidence before push.
