# Execution Checklist

[x] TP-01.01 | P0 | 复核 0065 contract/gate、policy 与 roadmap 缺口 | Verify: inspected files | Gate: target is existing gate hardening | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 proof-ref/raw URL/production deletion non-claim 边界 | Verify: task docs | Gate: no live overclaim | Parallelizable: Yes
[x] TP-02.01 | P0 | 定义 proofRefPrefixes 和 live evidence 输入约束 | Verify: contract file | Gate: no raw URL/secret evidence | Parallelizable: No
[x] TP-02.02 | P0 | 定义 raw URL、retention production marker 和敏感值负例 | Verify: tests/contract | Gate: fake evidence rejected | Parallelizable: No
[x] TP-03.01 | P0 | 更新 contract 与 gate validation | Verify: JSON + gate smoke | Gate: non-allowlisted proof refs rejected | Parallelizable: No
[x] TP-03.02 | P0 | 更新 schema invariant、AGENTS、roadmap 和 task index | Verify: grep + docs | Gate: docs keep pending boundary | Parallelizable: No
[x] TP-04.01 | P0 | 更新 focused regression tests | Verify: pytest | Gate: positive/negative paths covered | Parallelizable: No
[x] TP-04.02 | P0 | 运行 JSON、gate、pytest、ruff、secret scan、quick CI 和任务校验 | Verify: command outputs | Gate: required checks pass | Parallelizable: No
[x] TP-05.01 | P0 | 回填 closeout 与剩余外部验证项 | Verify: task docs validate | Gate: no placeholder | Parallelizable: No
[x] TP-05.02 | P0 | 明确 git/CI 交付证据外置边界 | Verify: task snapshot does not pre-claim post-commit CI | Gate: no pre-claim | Parallelizable: No
