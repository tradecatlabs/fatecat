# Execution Checklist

[x] TP-01.01 | P0 | 复核 0064 contract/gate 与 roadmap 缺口 | Verify: inspected files | Gate: target is staged backend evidence gate | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 pending/live/non-claim 边界 | Verify: task docs | Gate: no live overclaim | Parallelizable: Yes
[x] TP-02.01 | P0 | 定义 live evidence schema 与 proof ref 白名单 | Verify: contract file | Gate: no raw URL/secret evidence | Parallelizable: No
[x] TP-02.02 | P0 | 定义反伪造负例和敏感值防护 | Verify: tests/contract | Gate: fake evidence rejected | Parallelizable: No
[x] TP-03.01 | P0 | 新增 Python gate 与 shell wrapper | Verify: syntax + smoke | Gate: wrapper executable | Parallelizable: No
[x] TP-03.02 | P0 | 更新 registry/schema、local-ci 和文档 | Verify: grep + tests | Gate: docs keep pending boundary | Parallelizable: No
[x] TP-04.01 | P0 | 新增 focused regression tests | Verify: pytest | Gate: positive/negative paths covered | Parallelizable: No
[x] TP-04.02 | P0 | 运行 syntax、pytest、ruff、secret scan、quick CI 和任务校验 | Verify: command outputs | Gate: required checks pass | Parallelizable: No
[x] TP-05.01 | P0 | 回填 closeout 与剩余外部验证项 | Verify: task docs validate | Gate: no placeholder | Parallelizable: No
[x] TP-05.02 | P0 | 明确 git/CI 交付证据外置边界 | Verify: task snapshot does not pre-claim post-commit CI | Gate: no pre-claim | Parallelizable: No
