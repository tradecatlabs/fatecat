# Execution Checklist

[x] TP-01.01 | P0 | 复核 provider lifecycle/dependency gate、registry、vendor manifest 和 roadmap | Verify: inspected files | Gate: target is drift scanner | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 dependency/source/license/trace drift 边界 | Verify: task docs | Gate: no external live overclaim | Parallelizable: Yes
[x] TP-02.01 | P0 | 定义 drift report contract 和 required provider fields | Verify: contract file | Gate: report kind and required fields present | Parallelizable: No
[x] TP-02.02 | P0 | 定义 provider span、dependency smoke、vendor license/source 校验 | Verify: scanner checks | Gate: missing evidence creates finding | Parallelizable: No
[x] TP-03.01 | P0 | 新增 scanner Python 和 shell wrapper | Verify: syntax + CLI smoke | Gate: wrapper executable | Parallelizable: No
[x] TP-03.02 | P0 | 更新 provider schema、local-ci、AGENTS、operations docs、roadmap 和 task index | Verify: grep + tests | Gate: docs keep pending boundary | Parallelizable: No
[x] TP-04.01 | P0 | 新增 focused regression tests | Verify: pytest | Gate: report/CLI/contract paths covered | Parallelizable: No
[x] TP-04.02 | P0 | 运行 JSON、scanner、pytest、ruff、secret scan、quick CI 和任务校验 | Verify: command outputs | Gate: required checks pass | Parallelizable: No
[x] TP-05.01 | P0 | 回填 closeout 与剩余外部验证项 | Verify: task docs validate | Gate: no placeholder | Parallelizable: No
[x] TP-05.02 | P0 | 明确 git/CI 交付证据外置边界 | Verify: task snapshot does not pre-claim post-commit CI | Gate: no pre-claim | Parallelizable: No
