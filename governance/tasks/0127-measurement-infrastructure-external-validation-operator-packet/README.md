# Task Overview

0127 执行 `MI-100.C/D/E/F/G operator execution packet preparation`：在 0119 work queue、0120 proof-ref gate 和 0121 category runbooks 之后，新增全 external validation category 的 operator execution packet，把 22 类外部验证的执行顺序、必需凭证名称、脱敏 proof-ref bundle 模板、最终 gate 命令和分域分组统一落成机器可读包。

该任务不执行真实 production API、HF Space、Telegram Bot、OIDC、SIEM、Vault/KMS、OTel、developer portal、SDK 发布或第三方审计请求，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成操作员执行包和证据模板。

## In Scope

- 新增 external validation operator execution packet contract。
- 新增 Python generator 与 shell wrapper。
- 覆盖当前 work queue / category runbooks 中 22 类 external validation category。
- 接入 `scripts/local-ci.sh --profile quick`，在 category runbooks 后生成 operator packet artifact。
- 修正 category runbook 中 Postgres live smoke 命令参数和 production live operator packet 的 webhook allowed-hosts 环境变量口径。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不上传或保存 operator 外部 artifact 原文。
- 不验证隐藏外部 artifact 的真实性。
- 不关闭 production live、第三方审计或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and upstream evidence chain confirmation
TP-02 all-category operator packet contract/script/wrapper
TP-03 runbook command and env var alignment
TP-04 local-ci/AGENTS/roadmap wiring
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 22 类外部验证不能靠聊天记录执行 | `external-validation-operator-execution-packet.py` 输出确定的 `domainGroups`、`operatorSteps`、required credentials 和 final gate commands |
| 无真实凭证时不能伪造通过 | packet gate 固定 `blocked`，状态只声明 `operator_action_required` |
| 证据必须绑定 0119/0120/0121 | source 绑定 work queue、proof-ref gate、category runbooks、proof-ref contract 和 commit |
| 输出不得泄露 URL/token/DSN | 输出只含环境变量名、占位路径和 artifact hash 指令；测试覆盖敏感赋值拒绝和 raw URL 禁入 |
| local-ci 必须覆盖新入口 | quick profile 生成 `external-validation-operator-execution-packet.json` 并写入 summary artifacts |

## Task Package Overview

本任务把 `MI-100.C/D/E/F/G` 的执行前置层收束成一个可交接、可复核、可重复生成的 operator packet。它不是 live smoke，也不是 evidence accepted 结论；它是把真实外部凭证到位后的执行和交证流程固化成仓库内契约。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
