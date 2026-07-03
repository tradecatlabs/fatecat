# Execution Checklist

[x] TP-01 | P0 | 扫描 W2 runtime 现有子 gate 和证据缺口 | Verify: file scans | Gate: reuse path identified | Parallelizable: Yes
[x] TP-02 | P0 | 新增 runtime proof pack contract/schema | Verify: JSON parse + required components | Gate: contract present | Parallelizable: No
[x] TP-03 | P0 | 新增 runtime-proof-gate 并接入 local-ci/certification/audit | Verify: gate command | Gate: status passed with pending externals | Parallelizable: No
[x] TP-04 | P0 | 增加回归测试并同步 AGENTS/roadmap | Verify: targeted pytest + docs validator | Gate: tests pass | Parallelizable: Yes
[x] TP-05 | P0 | 运行验证、提交推送、收集证据 | Verify: local-ci quick | Gate: quick CI passed | Parallelizable: No
