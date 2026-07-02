# Acceptance Checklist

# Global Standards
- [x] 不提交敏感信息、运行态 DB、缓存、大型 raw/vendor 产物。
- [x] 本地门禁真实执行并记录。
- [ ] Git 操作非破坏性。
- [ ] 远端 CI 只基于当前 commit 证据判断。

# Task Package Checklists
## TP-01.01
- [x] 工作树审计完成。
- Verify: `git status --short --branch`、`git diff --stat`、untracked 分类。
- Gate: 未发现明显不应提交项。

## TP-02.01
- [x] 本地发布门禁完成。
- Verify: task tree、diff check、local-ci quick、live-release-gate。
- Gate: 命令结果真实记录。

## TP-03.01
- [ ] 提交推送完成。
- Verify: `git log -1 --oneline`、`git push origin main`。
- Gate: 远端 `origin/main` 指向新 commit。

## TP-04.01
- [ ] 远端 CI 证据完成。
- Verify: `gh run list --limit 10` 或 GitHub Actions URL。
- Gate: run head SHA equals current commit。

## TP-05.01
- [ ] closeout 完成。
- Verify: `TASK_CLOSEOUT_PACKET.json`。
- Gate: closeout ready。
