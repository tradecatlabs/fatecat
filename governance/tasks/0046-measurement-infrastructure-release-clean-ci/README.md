# Task Overview
- Task ID: `0046`
- Slug: `measurement-infrastructure-release-clean-ci`
- Objective: `把当前本地测算基础设施改动收口为可发布交付状态：审计并归类未提交改动，运行本地发布门禁，按清晰边界提交并推送当前 main，获取远端 GitHub Actions 当前 commit 证据，最终让 clean git state 和 remote_ci_current_commit 进入 live release gate；不伪造 Bot token、registry signature 或外部生产平台证据。`
- Status: `Done`

## In Scope
- 审计当前 dirty worktree，确认改动属于测算基础设施批次。
- 生成 release clean state 的任务证据：diff 边界、敏感信息扫描、本地门禁、提交/推送、远端 CI。
- 只在当前 `main` 分支上推进，不切分支、不重写历史。
- 回填 0046 closeout，并更新 live release gate 中 remote CI 与 clean git 的真实状态。

## Out of Scope
- 不提供 Telegram Bot token，不执行 Bot live smoke。
- 不推送 registry，不声明 registry digest/signature 已完成。
- 不接真实 OIDC/SIEM/监控平台。
- 不删除或回滚当前已有改动，除非发现明确误提交风险并能安全隔离。

## Task Package Tree
```text
ROOT
├── TP-01 工作树与改动边界审计
│   └── TP-01.01 统计 tracked/untracked、关键目录、潜在敏感文件
├── TP-02 本地发布门禁
│   └── TP-02.01 运行任务树校验、diff whitespace、本地 quick CI/live gate
├── TP-03 提交与推送
│   └── TP-03.01 按基础设施批次提交并推送当前 main
├── TP-04 远端 CI 证据
│   └── TP-04.01 获取 GitHub Actions 当前 commit run URL 和状态
└── TP-05 closeout
    └── TP-05.01 回填 0046 文档、Git delivery evidence 和剩余 pending 项
```

## Requirement Alignment
- 对齐 0045 路线图：0046 是 100% 基础设施最短路径第一项。
- 对齐 live release gate：本任务只负责 `remote_ci_current_commit` 与 `clean_git_state`，不伪造 Bot、registry、OIDC/SIEM。
- 对齐 auto-github：默认留在当前 `main` 分支，非破坏性提交/推送，提交前必须检查 diff。

## Task Package Overview
| ID | Name | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | 工作树审计 | Done | `git status --short --branch`、`git diff --stat`、untracked 统计 |
| TP-02.01 | 本地发布门禁 | Done | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0046-followup-postcommit` |
| TP-03.01 | 提交推送 | Done | 发布收口 commit 已推送到 `origin/main` |
| TP-04.01 | 远端 CI 证据 | Done | 当前最终 commit 以 GitHub Actions Acceptance/Container success 为准 |
| TP-05.01 | closeout | Done | `TASK_CLOSEOUT_PACKET.json` ready |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
