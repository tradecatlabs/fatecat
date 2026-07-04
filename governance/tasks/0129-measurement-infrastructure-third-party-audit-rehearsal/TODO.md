# Execution Checklist

[x] TP-01 | P0 | 确认 third-party audit rehearsal 范围和证据链 | Verify: roadmap 6.23/7/8 与现有 scripts | Gate: 不依赖真实外部凭证 | Parallelizable: No
[x] TP-02 | P0 | 新增 contract/script/wrapper | Verify: py_compile and contract test | Gate: no live calls, no secret output | Parallelizable: No
[x] TP-03 | P0 | 接入 local-ci 和 regression | Verify: local-ci contains third-party audit rehearsal step and focused pytest includes test | Gate: summary artifact path exposed | Parallelizable: No
[x] TP-04 | P0 | 同步 AGENTS、roadmap、task index | Verify: rg wiring and docs validation | Gate: 文档口径不声明第三方审计完成 | Parallelizable: Yes
[x] TP-05 | P0 | 运行验证门禁 | Verify: focused pytest, ruff, format, secret scan, task docs, quick CI | Gate: all pass | Parallelizable: No
[x] TP-06 | P0 | 提交推送并观察远端 CI | Verify: git status clean, remote Acceptance/Container success | Gate: current commit CI passed | Parallelizable: No
