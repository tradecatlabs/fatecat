# Task Overview

0134 执行 `MI-100.G.09 certification tracker issue evidence bridge`：把 0131-0133 已生成的 tracker import package、tracker issue evidence template 和 tracker issue evidence gate 纳入 measurement infrastructure certification audit domain，防止 100% certification 聚合器遗漏真实 issue 创建证据链阻断。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不执行 `gh`，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只让 certification dry-run 能看见本地 tracker issue evidence 链路。

## In Scope

- 更新 measurement infrastructure certification contract。
- 更新 certification aggregator 的 audit domain evidence files。
- 把 `packageGate`、`templateGate`、`issueEvidenceGate` 纳入 blocked marker。
- 把 `operator_action_required` 识别为阻断型 gate 状态。
- 增加 certification regression coverage。
- 同步 AGENTS、roadmap 和任务索引。

## Out of Scope

- 不创建真实 issue 或调用 GitHub API。
- 不执行 `gh`。
- 不上传 tracker issue evidence bundle。
- 不执行 production live validation。
- 不关闭 proof-ref、live proof、third-party audit 或 100% certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 certification tracker issue evidence blind spot confirmation
TP-02 certification contract and aggregator bridge
TP-03 regression coverage
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| Certification 必须消费 tracker issue 链路 | audit domain 增加 tracker import package、tracker issue evidence template、tracker issue evidence gate |
| 模板等待人工填写不能当 passed | `_blocked_items` 将 `operator_action_required` 视为阻断型 gate 状态 |
| Current audit sidecar 不能绕过 tracker 阻断 | regression 断言 tracker import/template/gate 仍在 audit evidence 中并产生 blockingItems |
| 合成全绿仍可验收 | synthetic fixture 为三项 tracker evidence 输出 passed，保护 aggregator 不是永久 blocked |
| 不泄露敏感值 | 只记录 gate 状态和 artifact path，不复制外部 URL/token/DSN/报告正文 |

## Task Package Overview

本任务修补 certification 的审计聚合盲区。0131-0133 已经让 local-ci 生成 tracker issue 链路 artifact；0134 让 certification audit domain 正式消费这些 artifact，使“真实 issue 还没创建/证据还没提交”的阻断能进入 100% certification 总门禁。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`

