# Task Overview

0133 执行 `MI-100.G.08 external validation tracker issue evidence template`：在 0131 tracker import package 与 0132 tracker issue evidence gate 之间，新增 operator 可填写的脱敏 evidence bundle 模板。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不执行 `gh`，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成本地 evidence bundle skeleton，供 operator 在真实创建 issue 后填写 sanitized issue ref 和 artifact hash。

## In Scope

- 新增 external validation tracker issue evidence template contract。
- 新增 Python template generator 与 shell wrapper。
- 消费 0131 `external-validation-tracker-import-package.json`。
- 输出 JSON template、Markdown 操作说明和 `bundleSkeleton`。
- 接入 `scripts/local-ci.sh --profile quick`。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不创建真实 issue 或调用 GitHub API。
- 不执行 `gh`。
- 不上传 proof-ref/live proof。
- 不把模板当成 accepted issue evidence。
- 不关闭 production live、third-party audit 或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and evidence template boundary confirmation
TP-02 tracker issue evidence template contract/script/wrapper
TP-03 local-ci artifact and regression wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 0132 gate 需要 operator 正确填写 evidence bundle | `external-validation-tracker-issue-evidence-template.py` 预填 source binding、workItemId、issueTemplateId、bodySha256 和 labels |
| 模板不能伪装成已创建 issue | `templateGate.status=operator_action_required` 且 `readyToSubmitToGate=false` |
| 证据必须绑定 0131 package | template source 绑定 package sha256 与 commit |
| 输出不得泄露 URL/token/DSN | generator 对输入、输出和 Markdown 执行 raw URL / sensitive assignment / placeholder 拒绝 |
| local-ci 必须可复核 | quick profile 生成 JSON/Markdown artifact 并写入 summary |

## Task Package Overview

本任务把“可验证 evidence gate”前置成“可填写 evidence skeleton”，减少 operator 后续手工补证时的字段错配风险。它不是外部执行结果。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
