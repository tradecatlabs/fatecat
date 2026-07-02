# Execution Checklist
[x] TP-01.01 | P0 | 审计工作树、untracked 和敏感/运行态风险 | Verify: `git status --short --branch`、`git diff --stat`、untracked 分类 | Gate: 无明显误提交 | Parallelizable: No
[x] TP-02.01 | P0 | 运行本地发布门禁 | Verify: task tree、`git diff --check`、`bash scripts/local-ci.sh --profile quick` | Gate: 本地门禁真实结果 | Parallelizable: No
[ ] TP-03.01 | P0 | 提交并推送当前 main | Verify: `git commit`、`git push origin main` | Gate: origin/main 更新 | Parallelizable: No
[ ] TP-04.01 | P0 | 获取远端 CI 当前 commit 证据 | Verify: `gh run list --limit 10` | Gate: run head SHA equals current commit | Parallelizable: No
[ ] TP-05.01 | P0 | 回填 closeout 和剩余 pending | Verify: `build_task_closeout.py --strict` | Gate: closeout ready | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
