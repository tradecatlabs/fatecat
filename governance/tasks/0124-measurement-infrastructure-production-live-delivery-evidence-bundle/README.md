# Task Overview

0124 执行 `MI-100.B.01 production live delivery evidence bundle`：在 0123 live proof gate 之后，新增一层生产交付 live evidence bundle 装配器，把 production API、HF Space、Telegram Bot、公网 webhook 和多端 live parity 的脱敏真实执行摘要转换为 `fatecat.external_validation_live_evidence_bundle`，供 `external-validation-live-proof-gate.py` 统一校验。

该任务不执行真实生产请求，不读取或保存真实 token、secret、DSN、webhook secret、外部账号、生产日志、用户输入或报告正文。无真实 summary 时输出 `external_connectivity_pending`；有真实脱敏 summary 时只输出 proof id、artifact hash、source binding 和 operator attestation。

## In Scope

- 新增 production live delivery evidence bundle contract。
- 新增 production live delivery evidence bundle Python assembler 与 shell wrapper。
- 支持 `release.production_api_live`、`release.hf_space_live`、`release.telegram_bot_live`、`runtime.public_webhook_live`、`delivery.multi_surface_live` 五类交付 live category。
- 接入 local-ci，在 live proof gate 之前生成 pending/live bundle，并把 bundle 传给 live proof gate。
- 修正 Telegram Bot category runbook 中不可执行的 `live-bot-smoke.sh --require-live --output-json` 命令，统一改为 `live-release-gate.sh --run-live-bot --output-json`。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实 API/HF/Bot/Postgres/webhook 请求。
- 不上传或保存外部 evidence artifact 原文。
- 不验证隐藏外部 artifact 的真实性。
- 不关闭第三方审计或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and upstream category confirmation
TP-02 production live delivery contract/script/wrapper
TP-03 local-ci/live-proof/docs wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 生产 live 证据不能靠聊天或散落 JSON | `production-live-delivery-evidence-bundle.py` 统一装配为 `external_validation_live_evidence_bundle` |
| 无真实凭证时不能伪造通过 | 默认无 passing summaries 时 `status=external_connectivity_pending` 且 `liveProofs=[]` |
| API/HF/Bot/webhook/parity 证据要能绑定 0123 | 输出 `sourceBinding` 绑定 work queue sha、proof-ref gate sha、category runbooks sha、commit 和 occurrence ids |
| 输出不得泄露 URL/token/DSN | bundle 只输出 artifact hash 和脱敏命令；测试确认 raw URL 不进入输出，敏感赋值输入被拒绝 |
| local-ci 必须覆盖新入口 | quick profile 生成 `production-live-delivery-evidence-bundle.json` 并传给 live proof gate |

## Task Package Overview

本任务把 `MI-100.B` 的真实生产交付 evidence 接入口收束成一个机器契约。它不是 live smoke 本身，而是 live smoke 后的审计装配层：操作员在外部环境执行 live gate，仓库只消费脱敏 summary 的 hash/状态/绑定关系。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
