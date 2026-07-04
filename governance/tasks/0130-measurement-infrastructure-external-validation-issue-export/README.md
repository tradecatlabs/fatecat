# Task Overview

0130 执行 `MI-100.G.05 external validation issue export`：在 0129 third-party audit rehearsal 之后，新增外部验证 issue export，把 work queue、category runbooks、operator execution packet 和 closure evidence summary 聚合成可导入 issue tracker 的脱敏执行卡片。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成本地 issue export 包。

## In Scope

- 新增 external validation issue export contract。
- 新增 Python generator 与 shell wrapper。
- 消费 closure work queue、category runbooks、operator packet 和 closure evidence summary。
- 输出 JSON/Markdown issue export。
- 接入 `scripts/local-ci.sh --profile quick`。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不创建真实 issue 或调用 GitHub API。
- 不上传 proof-ref/live proof。
- 不关闭 production live、third-party audit 或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and issue export evidence chain confirmation
TP-02 issue export contract/script/wrapper
TP-03 local-ci artifact and regression wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 外部验证需要可分派执行卡片 | `external-validation-issue-export.py` 输出 JSON/Markdown issue templates |
| 不伪造 issue 创建或 live passed | `issueGate.status` 在真实 tracker/live/proof 缺失时保持 `blocked` |
| 证据必须绑定当前执行链路 | 输入包含 work queue、category runbooks、operator packet、closure evidence summary |
| 输出不得泄露 URL/token/DSN | 只输出 owner/category/workItemId、credential 名称、命令模板、hash 指令和关闭条件 |
| local-ci 必须可复核 | quick profile 生成 issue export artifact 并写入 summary |

## Task Package Overview

本任务把“下一步由谁执行什么外部验证”从摘要文本变成 issue tracker 可消费的卡片集合。它不是执行结果，而是 operator 分派入口。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
