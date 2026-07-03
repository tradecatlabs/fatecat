# Execution Checklist
[x] TP-01.01 | P0 | 官方资料版本快照 | Verify: `RESEARCH.md` source matrix | Gate: 只使用官方/事实标准来源 | Parallelizable: Yes
[x] TP-01.02 | P0 | 当前仓库与远端状态快照 | Verify: `git status` + `gh run list` snapshot | Gate: `in_progress` 不写 passed | Parallelizable: Yes
[x] TP-02.01 | P0 | 资源模型和缺口矩阵 | Verify: matrix covers infra resources | Gate: 不隐藏 external live pending | Parallelizable: No
[x] TP-02.02 | P0 | 不可伪造验收口径 | Verify: anti-forgery section | Gate: dry-run/staged/local 不写 production | Parallelizable: No
[x] TP-03.01 | P0 | 执行波次和优先级 | Verify: W0-W9 waves | Gate: W0 release truth first | Parallelizable: No
[x] TP-03.02 | P0 | 最短下一步与阻断项 | Verify: shortest path section | Gate: 外部 blocker 明确 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 RESEARCH、任务包和主路线图 | Verify: git diff scoped | Gate: 不改业务代码 | Parallelizable: No
[x] TP-04.02 | P0 | 运行文档校验、占位符检查和状态检查 | Verify: validator + rg scans | Gate: 无占位符，task docs pass | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
