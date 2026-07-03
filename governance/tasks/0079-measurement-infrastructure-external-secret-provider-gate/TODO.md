# Execution Checklist

[x] TP-01.01 | P0 | 复核 0059/0078 本地 vault 与 runtime 缺口 | Verify: docs/code read | Gate: 不把 local Fernet 视为 external Vault/KMS | Parallelizable: No
[x] TP-01.02 | P0 | 复核 security registry/schema/gate 接线点 | Verify: schema/registry/gate/local-ci read | Gate: 不新增孤立 contract | Parallelizable: No
[x] TP-02.01 | P0 | 新增 external-secret-provider evidence contract | Verify: JSON contract parse | Gate: 不保存真实 secret | Parallelizable: No
[x] TP-02.02 | P0 | 新增 negative evidence cases 与 live schema | Verify: gate negative cases | Gate: fake local evidence must fail | Parallelizable: No
[x] TP-03.01 | P0 | 更新 SecurityControl schema/registry/policy | Verify: production-security gate | Gate: registry status manual/external pending | Parallelizable: No
[x] TP-03.02 | P0 | 新增 external-secret-provider-gate.py/.sh | Verify: gate output JSON | Gate: summary 脱敏 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci artifact | Verify: local-ci summary artifact path | Gate: quick CI must run gate | Parallelizable: No
[x] TP-04.01 | P0 | 增加 regression tests | Verify: pytest focused | Gate: coverage includes contract/negative/privacy | Parallelizable: No
[x] TP-04.02 | P0 | 更新 roadmap、operations docs 和 AGENTS | Verify: rg docs | Gate: no live overclaim | Parallelizable: No
[x] TP-05.01 | P0 | 运行 focused gates、ruff/format 和 quick CI | Verify: commands pass | Gate: failures fixed or recorded | Parallelizable: No
[x] TP-05.02 | P0 | 回填任务 closeout、提交、推送并记录 CI | Verify: git/CI evidence | Gate: clean pushed worktree | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
