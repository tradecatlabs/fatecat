# Task Overview

0126 执行 `MI-100.B.00 operator live execution packet and evidence template`：在 0121 category runbooks、0123 live proof gate 和 0124 production live delivery evidence bundle 之后，新增一个生产 live operator execution packet，把真实凭证到位后的操作顺序、必需环境变量名、脱敏 proof-ref bundle 模板、最终 gate 命令和失败回滚统一落成机器可读包。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres webhook 或多端 live 请求，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成操作员执行包和证据模板。

## In Scope

- 新增 production live operator execution packet contract。
- 新增 Python generator 与 shell wrapper。
- 支持 `release.production_api_live`、`release.hf_space_live`、`release.telegram_bot_live`、`runtime.public_webhook_live`、`delivery.multi_surface_live` 五类交付 live category。
- 接入 `scripts/local-ci.sh --profile quick`，在 delivery evidence bundle 之前生成 operator packet artifact。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不上传或保存 operator 外部 artifact 原文。
- 不验证隐藏外部 artifact 的真实性。
- 不关闭第三方审计或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and upstream evidence chain confirmation
TP-02 operator packet contract/script/wrapper
TP-03 local-ci/AGENTS/roadmap wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 操作员不能靠聊天记录执行 live | `production-live-operator-execution-packet.py` 输出确定的 operator steps 和 final gate commands |
| 无真实凭证时不能伪造通过 | packet gate 固定 `blocked`，只声明 `operator_action_required` |
| 证据必须绑定 0121/0123/0124 | source 绑定 work queue、proof-ref gate、category runbooks、live proof gate contract、delivery bundle contract 和 commit |
| 输出不得泄露 URL/token/DSN | 输出只含环境变量名、占位路径和 artifact hash 指令；测试覆盖敏感赋值拒绝和 raw URL 禁入 |
| local-ci 必须覆盖新入口 | quick profile 生成 `production-live-operator-execution-packet.json` 并写入 summary artifacts |

## Task Package Overview

本任务把 `MI-100.B` 的执行前置层收束成一个可交接、可复核、可重复生成的 operator packet。它不是 live smoke，也不是 evidence accepted 结论；它是把真实外部凭证到位后的执行和交证流程固化成仓库内契约。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
