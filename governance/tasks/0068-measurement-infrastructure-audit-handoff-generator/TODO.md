# Execution Checklist

[x] TP-01.01 | P0 | 复核现有 closeout、release gate、local-ci、roadmap 和 pending external validation 事实 | Verify: rg/sed/git status | Gate: 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 audit handoff contract | Verify: json tool | Gate: pending policy 明确 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 audit handoff generator | Verify: generator CLI | Gate: writes Markdown/JSON | Parallelizable: No
[x] TP-03.01 | P0 | 新增 audit handoff 回归测试 | Verify: focused pytest | Gate: pending count equals git grep | Parallelizable: Yes
[x] TP-03.02 | P0 | 接入 local-ci artifact 和目录级 AGENTS | Verify: local-ci grep + docs | Gate: auditHandoff artifact 可发现 | Parallelizable: Yes
[x] TP-03.03 | P0 | 同步 roadmap 与任务索引 | Verify: roadmap diff | Gate: 不夸大 live evidence | Parallelizable: Yes
[x] TP-04.01 | P0 | 运行 focused validation 和 secret scan | Verify: pytest/ruff/secret scan | Gate: no sensitive assignment output | Parallelizable: No
[x] TP-04.02 | P0 | 运行 quick local-ci、任务校验并收口证据 | Verify: quick local-ci + validators | Gate: 本地 quick CI 通过 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
