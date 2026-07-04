# Task Overview

0132 执行 `MI-100.G.07 external validation tracker issue evidence gate`：在 0131 tracker import package 之后，新增外部验证 tracker issue 创建证据门禁，把 operator 手工创建 issue 后提交的脱敏 evidence bundle 与 import package 逐项绑定。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不执行 `gh`，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只验证本地脱敏 tracker issue evidence bundle 的结构和 hash 绑定。

## In Scope

- 新增 external validation tracker issue evidence contract。
- 新增 Python gate 与 shell wrapper。
- 消费 0131 `external-validation-tracker-import-package.json`。
- 可选消费 operator 脱敏 `external_validation_tracker_issue_evidence_bundle`。
- 输出 accepted/rejected/pending issue evidence gate。
- 接入 `scripts/local-ci.sh --profile quick`。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不创建真实 issue 或调用 GitHub API。
- 不执行 `gh`。
- 不上传 proof-ref/live proof。
- 不关闭 production live、third-party audit 或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and tracker issue evidence boundary confirmation
TP-02 tracker issue evidence contract/script/wrapper
TP-03 local-ci artifact and regression wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| tracker import package 后需要验证真实 issue 创建证据 | `external-validation-tracker-issue-evidence-gate.py` 校验 issue ref、workItemId、issueTemplateId 和 body hash |
| 不伪造 issue 创建或 live passed | 无 evidence 时 `issueEvidenceGate.status=blocked`；即使 issue evidence accepted，`shipGate.status=blocked` |
| 证据必须绑定 0131 package | evidence bundle source 绑定 package sha256 与 commit |
| 输出不得泄露 URL/token/DSN | gate 对输入和输出执行 raw URL / sensitive assignment / placeholder 拒绝 |
| local-ci 必须可复核 | quick profile 生成 `external-validation-tracker-issue-evidence-gate.json` 并写入 summary |

## Task Package Overview

本任务把“可导入 tracker 的本地包”推进成“真实创建 issue 后可验证的脱敏证据入口”。它不是外部执行结果，而是外部验证执行前的 tracker 绑定证据门禁。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
