# Execution Checklist
[x] TP-01.01 | P0 | 读取 provider drift scanner、contract、provider schema、local-ci 和路线图 | Verify: repo evidence recorded | Gate: no runtime rewrite | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 trend gate 与 baseline 边界 | Verify: PLAN/CONTEXT record boundary | Gate: no external live overclaim | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 provider drift baseline 与 trend contract | Verify: JSON parse + focused tests | Gate: tracked baseline includes fingerprints | Parallelizable: Yes
[x] TP-02.02 | P0 | 新增 provider drift trend gate script | Verify: script passes current baseline | Gate: status passed/findingCount 0 | Parallelizable: No
[x] TP-02.03 | P0 | 接入 local-ci、AGENTS、provider schema、docs | Verify: wiring regression assertions | Gate: quick CI invokes gate after scanner | Parallelizable: Yes
[x] TP-03.01 | P0 | 增加 trend gate positive/negative tests | Verify: focused pytest | Gate: missing provider/license/vendor/scanner failures rejected | Parallelizable: Yes
[x] TP-03.02 | P0 | 运行 focused tests、ruff、format、task validator | Verify: command output recorded | Gate: all pass | Parallelizable: No
[x] TP-04.01 | P0 | 回填 closeout 状态 | Verify: STATUS/ACCEPTANCE updated | Gate: no placeholders | Parallelizable: No
[x] TP-04.02 | P0 | 提交并推送 | Verify: git status clean and origin/main aligned | Gate: remote CI not overclaimed | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
