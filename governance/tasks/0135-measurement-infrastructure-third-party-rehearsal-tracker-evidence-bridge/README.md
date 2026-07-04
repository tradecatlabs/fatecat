# Task Overview

0135 执行 `MI-100.G.10 third-party rehearsal tracker evidence bridge`：把 0131-0133 已生成的 tracker import package、tracker issue evidence template 和 tracker issue evidence gate 直接纳入 third-party audit rehearsal 的输入、证据索引和审计 checklist，防止独立审计人员只能通过 certification 间接发现 tracker issue 创建证据链阻断。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不执行 `gh`，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只让 third-party audit rehearsal 能直接看见本地 tracker issue evidence 链路。

## In Scope

- 更新 third-party audit rehearsal contract。
- 更新 third-party audit rehearsal generator 的 CLI 输入和 kind 校验。
- 把 tracker import package、tracker issue evidence template 和 tracker issue evidence gate 纳入 rehearsal `evidenceIndex`。
- 把 tracker issue 创建/模板填写/issue evidence gate 纳入 rehearsal `auditorChecklist`。
- 更新 local-ci 的 third-party audit rehearsal 调用。
- 增加 rehearsal regression coverage。
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
TP-01 rehearsal tracker blind spot confirmation
TP-02 contract and CLI input bridge
TP-03 rehearsal evidence/checklist bridge
TP-04 local-ci/AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| Third-party audit rehearsal 必须直接消费 tracker issue 链路 | contract/generator 增加 tracker import package、tracker issue evidence template、tracker issue evidence gate |
| 模板等待人工填写不能当 passed | checklist 对 `operator_action_required` 输出 blocked |
| Issue evidence gate 缺真实 evidence 不能当 passed | checklist 对 `issueEvidenceGate=blocked` 输出 blocked |
| 审计人员能直接复核 artifact | `evidenceIndex` 输出三项 tracker artifact 的 path、sha256、status 和 gate |
| 不泄露敏感值 | 继续使用 rehearsal 的 raw URL / secret fragment scanner |

## Task Package Overview

本任务修补第三方审计预演包的证据交接盲区。0134 已让 certification 看见 tracker issue 链路；0135 让独立审计预演包也直接消费这些 artifact，使“真实 issue 还没创建/证据还没提交”的阻断能出现在审计 checklist 和 evidence index 中。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
