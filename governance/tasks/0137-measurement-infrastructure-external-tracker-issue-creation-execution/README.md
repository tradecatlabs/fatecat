# Task Overview
- Task ID: `0137`
- Slug: `measurement-infrastructure-external-tracker-issue-creation-execution`
- Objective: `执行 0136 后续 0137：基于当前 HEAD 的 external validation tracker import package，在授权 GitHub tracker 会话中创建真实外部验证 issue，生成脱敏 tracker issue evidence bundle，并通过 tracker issue evidence gate；不执行 production live、不上传 proof-ref、不关闭 certification 或 third-party audit。`
- Status: `Done`

## In Scope
- 使用当前 HEAD `2a2da45eb787efd5ab316fa19367cd9440007f0b` 的 `external-validation-tracker-import-package.json`。
- 在授权 GitHub tracker 会话中创建 22 个 `[External Validation]` issue。
- 为每个 issue 生成脱敏 evidence artifact，绑定 `workItemId`、`issueTemplateId`、`trackerIssueRef`、`bodySha256` 与 `artifactSha256`。
- 执行 `scripts/external-validation-tracker-issue-evidence-gate.sh`，验证 22 个 issue evidence 全部 accepted。
- 将脱敏 evidence bundle、gate 输出与人工可读 issue ref 清单落盘到本任务包。

## Out of Scope
- 不执行 production API、Bot、Webhook、HF Space、Postgres 或 SIEM live 验证。
- 不上传 proof-ref，不关闭 `external-validation-proof-ref-gate`。
- 不声明 measurement infrastructure certification 已完成。
- 不声明第三方审计已完成。
- 不在仓库中保存 GitHub 原始 URL、token、secret、DSN、webhook secret、外部账号、生产日志、trace payload、报告正文或用户输入。

## Task Package Tree
```text
0137-measurement-infrastructure-external-tracker-issue-creation-execution/
├── README.md
├── CONTEXT.md
├── PLAN.md
├── ACCEPTANCE.md
├── ACCEPTANCE_CHECKLIST.md
├── TODO.md
├── STATUS.md
└── evidence/
    ├── TRACKER_ISSUE_CREATION_SUMMARY.json
    ├── TRACKER_ISSUE_EVIDENCE_BUNDLE.json
    ├── TRACKER_ISSUE_EVIDENCE_GATE.json
    └── TRACKER_ISSUE_REFS.md
```

## Requirement Alignment
- 对齐 0136 后续 0137：从“生成 tracker import package”推进到“真实 tracker issue 已创建并有 gate 证据”。
- 对齐 100% 测算基础设施路线图：外部验证闭环必须有真实外部工单载体，但工单载体不等于生产 live 通过。
- 对齐隐私边界：仓库只保存脱敏 tracker ref 和 hash 证据。

## Task Package Overview
| TP | 名称 | 状态 | 证据 |
| --- | --- | --- | --- |
| TP-01 | 当前 HEAD 与 import package 核查 | Done | `TRACKER_ISSUE_EVIDENCE_BUNDLE.json` source.commit |
| TP-02 | GitHub tracker 权限与重复项核查 | Done | issue 创建摘要记录 22 created issues |
| TP-03 | 真实 issue 创建 | Done | `TRACKER_ISSUE_REFS.md` |
| TP-04 | 脱敏 evidence bundle 生成 | Done | `TRACKER_ISSUE_EVIDENCE_BUNDLE.json` |
| TP-05 | issue evidence gate | Done | `TRACKER_ISSUE_EVIDENCE_GATE.json` status `accepted` |
| TP-06 | 任务文档与证据落盘 | Done | 本任务包 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
