# Execution Checklist

[x] TP-01 | P0 | 核对当前 release/audit/certification/rehearsal 证据基线 | Verify: JSON inspection of `/tmp/fatecat-current-release-audit-chain-refresh-4710659` | Gate: passed/blocked 状态不混写 | Parallelizable: Yes
[x] TP-02 | P0 | 调研成熟基础设施官方资料 | Verify: `RESEARCH.md` source matrix | Gate: 每个来源映射到 FateCat 域 | Parallelizable: Yes
[x] TP-03 | P0 | 制作 100% 资源成熟度矩阵 | Verify: `RESEARCH.md` maturity matrix | Gate: 本地基线、生产缺口和外部 blocker 分开 | Parallelizable: No
[x] TP-04 | P0 | 制作完整实现任务树和执行波次 | Verify: `PLAN.md` next executable sequence | Gate: 后续任务有依赖和验收口径 | Parallelizable: No
[x] TP-05 | P0 | 落盘任务包和路线图 | Verify: task docs + roadmap diff | Gate: 没有改业务代码 | Parallelizable: No
[x] TP-06 | P0 | 执行验证和 no-overclaim 自审 | Verify: validator/rg checks | Gate: 无占位符、无伪完成声明 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
