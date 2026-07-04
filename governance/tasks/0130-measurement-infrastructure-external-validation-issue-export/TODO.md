# Execution Checklist

[x] TP-01 | P0 | 确认 issue export 范围和证据链 | Verify: roadmap 6.24/6.25 与 existing scripts | Gate: 不依赖真实外部凭证 | Parallelizable: No
[x] TP-02 | P0 | 新增 contract/script/wrapper | Verify: py_compile + direct CLI smoke | Gate: 输出 no raw URL / no sensitive assignment | Parallelizable: No
[x] TP-03 | P0 | 接入 local-ci 和 regression | Verify: local-ci contains issue export step and focused pytest includes test | Gate: summary artifact path exposed | Parallelizable: No
[x] TP-04 | P0 | 同步 AGENTS/roadmap/task index | Verify: rg issue export docs | Gate: 文档不声明 live passed | Parallelizable: No
[x] TP-05 | P0 | 跑聚焦验证和 quick CI | Verify: pytest/ruff/secret-scan/task-docs/local-ci | Gate: dirty worktree evidence not used as final ship evidence | Parallelizable: No
[x] TP-06 | P0 | 提交、推送、观察远端 CI | Verify: git status clean, gh run URLs | Gate: current commit remote CI success or explicit evidence pending | Parallelizable: No
