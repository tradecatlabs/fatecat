# Execution Checklist

[x] TP-01 | P0 | 核查当前 worktree、0140 和主路线图状态 | Verify: `git status --short --branch` + task/roadmap inspection | Gate: 当前状态来自真实文件/命令 | Parallelizable: Yes
[x] TP-02 | P0 | 调研成熟基础设施官方资料 | Verify: `RESEARCH.md` source matrix | Gate: 每类资料映射到 FateCat 资源 | Parallelizable: Yes
[x] TP-03 | P0 | 制作 100% 准入模型和资源成熟度矩阵 | Verify: `RESEARCH.md` admission/resource sections | Gate: local/external/audit 边界清楚 | Parallelizable: No
[x] TP-04 | P0 | 制作完整任务树、执行波次和后续任务 | Verify: `RESEARCH.md` implementation tree | Gate: 后续任务有 blocker 与证据口径 | Parallelizable: No
[x] TP-05 | P0 | 落盘任务包和主路线图 post-0140 摘要 | Verify: `git diff --name-only` | Gate: docs-only 变更 | Parallelizable: No
[x] TP-06 | P0 | 执行验证和 no-overclaim 自审 | Verify: validator + scans | Gate: pass | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
