# Execution Checklist
[x] TP-01 | P0 | 审计污染、完整性、家族和书目异常 | Verify: path/line evidence | Gate: no unsupported fact | Parallelizable: No
[x] TP-02 | P0 | 建立 source-hash 绑定 curation policy 与 schema | Verify: 14/14 coverage | Gate: fail closed | Parallelizable: No
[x] TP-03 | P0 | 增强现有清洗器分离正文与来源元数据 | Verify: focused tests | Gate: semantic round-trip | Parallelizable: No
[x] TP-04 | P0 | 重建 14 本数据集并验证噪声零进入 | Verify: build/validate-only | Gate: source hash unchanged | Parallelizable: No
[x] TP-05 | P0 | 深审、Quick CI、任务和本地版本控制收口 | Verify: review/CI/task strict | Gate: PASS | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
