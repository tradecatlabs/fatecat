# Task Overview

0131 执行 `MI-100.G.06 external validation tracker import package`：在 0130 issue export 之后，新增外部验证 tracker import package，把 issue export 中的 pending work items 落成独立 issue body 文件、导入 manifest 和人工可复核的 tracker CLI 命令清单。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不创建真实 GitHub issue，不执行 `gh`，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成本地 tracker import dry-run package。

## In Scope

- 新增 external validation tracker import package contract。
- 新增 Python package builder 与 shell wrapper。
- 消费 0130 `external-validation-issue-export.json`。
- 输出 package manifest、Markdown README、独立 issue body 文件和 `gh issue create` 命令文本。
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
TP-01 scope and tracker import boundary confirmation
TP-02 tracker import package contract/script/wrapper
TP-03 local-ci artifact and regression wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| issue export 需要变成可导入包 | `external-validation-tracker-import-package.py` 输出 body files、manifest 和 command text |
| 不伪造 issue 创建或 live passed | `packageGate.status` 在真实 issue/live/proof 缺失时保持 `blocked` |
| 证据必须绑定 0130 export | 输入包含 issue export sha256、kind 和 commit |
| 输出不得泄露 URL/token/DSN | builder 对输入、body、命令和输出执行 raw URL / sensitive assignment 拒绝 |
| local-ci 必须可复核 | quick profile 生成 tracker import package artifact 并写入 summary |

## Task Package Overview

本任务把“可复制的 issue 模板”推进成“可交给 operator 审核后导入 tracker 的本地包”。它不是执行结果，而是外部验证 issue 创建前的最后一层本地可复核准备。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
