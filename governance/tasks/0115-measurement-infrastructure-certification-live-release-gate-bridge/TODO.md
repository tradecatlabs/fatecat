# Execution Checklist

[x] TP-01 | P0 | 确认 certification live gate 只能从 evidence dir 读取 | Verify: source scan + CLI help | Gate: blind spot defined | Parallelizable: Yes
[x] TP-02 | P0 | 实现 live release gate sidecar override | Verify: CLI smoke | Gate: release proof/audit not bypassed | Parallelizable: No
[x] TP-03 | P0 | 更新 regression tests、contract、AGENTS、roadmap 和 task index | Verify: targeted pytest + docs validator | Gate: tests pass | Parallelizable: Yes
[x] TP-04 | P0 | 运行验证、自审、提交推送 | Verify: ruff + secret scan + git status | Gate: remote updated | Parallelizable: No
