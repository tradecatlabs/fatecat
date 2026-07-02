# Task-Level Acceptance
- 当前 worktree 改动边界已审计，无明显敏感/运行态误提交。
- 本地发布门禁真实执行，结果写入任务证据。
- 当前 main 有语义清晰 commit 并推送到 origin。
- GitHub Actions 有当前 commit 的 run URL 和 head SHA 证据，最终以提交后 `gh run list` / `gh run view` 为准。
- live release gate 中 `remote_ci_current_commit`、`container_digest` 与 `clean_git_state` 的状态真实反映当前情况。
- live release gate 仍因缺真实 Telegram Bot token 保持 blocked，不得写成已发布。

# Validation Plan
- `git status --short --branch`
- `git diff --stat`
- `git ls-files --others --exclude-standard`
- `git diff --check`
- `bash scripts/local-ci.sh --profile quick --output <dir>`
- `bash scripts/live-release-gate.sh ... --output-json <path>`
- `git commit`
- `git push origin main`
- `gh run list --limit 10`

# Review Gate
- 提交前必须确认 `.env`、private key、token、runtime DB、cache、大型 raw/vendor 产物未混入。
- 提交信息必须说明基础设施收口，不使用 `update`/`wip`。
- 远端 CI 失败时不得写“已通过”。

# Runtime Verification Gate
- 本地 quick CI 必须有 summary JSON。
- live release gate 必须输出 JSON。
- GitHub Actions 证据必须包含 run URL 与当前 commit SHA；若 `gh` 不可用，记录不可用原因。

# Ship Readiness
只有 commit/push 成功、远端 CI 当前 commit 通过、git clean 且 0046 closeout 完成时，本任务才能 Done。真实 Telegram Bot live smoke、registry signature、OIDC/SIEM 仍作为后续外部任务 pending。

# Task Package Acceptance
- TP-01.01：改动边界审计完成。
- TP-02.01：本地门禁执行完成。
- TP-03.01：commit/push 完成。
- TP-04.01：远端 CI 证据完成。
- TP-05.01：closeout 完成。

# Anti-Goals
- 不得重写 Git 历史
- 不得虚构证据
- 不得越权补全未确认信息
