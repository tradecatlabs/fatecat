# Execution Checklist

[x] TP-01.01 | P0 | 复核 0080 contract/gate 与 roadmap 剩余缺口 | Verify: repo evidence | Gate: missing controlled producer identified | Parallelizable: No
[x] TP-01.02 | P0 | 定义 assembler live/pending 边界 | Verify: task docs | Gate: pending cannot mean live passed | Parallelizable: No
[x] TP-02.01 | P0 | 设计 CLI 输入、输出 schema 和防敏感值策略 | Verify: PLAN | Gate: output is 0080-compatible evidence | Parallelizable: No
[x] TP-02.02 | P0 | 定义 0080 gate 复用路径和反伪造负例 | Verify: PLAN | Gate: no duplicated gate logic | Parallelizable: No
[x] TP-03.01 | P0 | 新增 assembler Python 与 shell wrapper | Verify: syntax + CLI smoke | Gate: output validates through 0080 gate | Parallelizable: No
[x] TP-03.02 | P0 | 接入 local-ci artifact、scripts AGENTS 和 docs | Verify: local-ci/docs grep | Gate: no live overclaim | Parallelizable: Yes
[x] TP-04.01 | P0 | 增加 assembler regression tests | Verify: focused pytest | Gate: positive/negative coverage | Parallelizable: Yes
[x] TP-04.02 | P0 | 运行 focused gates、ruff/format、secret scan、quick CI 和任务校验 | Verify: command outputs | Gate: all required checks pass | Parallelizable: No
[x] TP-05.01 | P0 | 回填 closeout 与剩余外部验证项 | Verify: task validators | Gate: no placeholders/no overclaim | Parallelizable: No
[x] TP-05.02 | P0 | 明确 git/CI 交付证据外置边界 | Verify: task snapshot does not pre-claim post-commit git/CI | Gate: no pre-claim | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
