# TODO

# Execution Checklist

[x] TP-01 | P0 | 确认 certification tracker issue evidence blind spot | Verify: roadmap/local-ci/certification rg | Gate: 不依赖真实外部凭证或 tracker 权限 | Parallelizable: No
[x] TP-02 | P0 | 接入 certification contract 和 aggregator | Verify: contract + script diff | Gate: `operator_action_required` 不当 passed | Parallelizable: No
[x] TP-03 | P0 | 补 regression | Verify: focused pytest | Gate: current audit sidecar 不绕过 tracker 阻断 | Parallelizable: No
[x] TP-04 | P0 | 同步 roadmap/AGENTS/task index | Verify: rg certification tracker issue evidence bridge docs | Gate: 文档不声明 live passed | Parallelizable: No
[x] TP-05 | P0 | 验证本地 gates | Verify: focused gates + quick CI | Gate: 所有本地验证通过 | Parallelizable: No
[x] TP-06 | P0 | 交付与远端 CI | Verify: git delivery + remote CI | Gate: 当前 commit 远端 CI 通过 | Parallelizable: No

