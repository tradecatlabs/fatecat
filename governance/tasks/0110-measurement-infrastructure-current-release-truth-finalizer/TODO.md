# Execution Checklist

[x] TP-01 | P0 | 删除 0108 重复 INDEX 行并新增 0110 任务包 | Verify: index row count + task docs validator | Gate: 0108 一行且 docs pass | Parallelizable: No
[x] TP-02 | P0 | 提交推送最终文档状态并确认 clean HEAD | Verify: git status | Gate: origin/main matches HEAD | Parallelizable: No
[x] TP-03 | P0 | 触发并等待 Acceptance 与 Container workflow | Verify: gh run view | Gate: both success and headSha matches | Parallelizable: No
[x] TP-04 | P0 | 生成 rollback dry-run 并运行 current-release-proof | Verify: proof JSON status passed | Gate: pending 0, failed 0 | Parallelizable: No
