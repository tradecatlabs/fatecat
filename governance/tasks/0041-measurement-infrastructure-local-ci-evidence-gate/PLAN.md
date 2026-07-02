# Planning Summary
目标不是新增发布能力，而是修正发布证据链：`local-ci quick` 的真实通过结果必须变成 `live-release-gate` 可验证输入。

# Lifecycle Gates
- SPEC：确认现有参数和缺口。
- PLAN：拆成 summary 生成、summary 校验、public-release 接线、验证收口。
- BUILD：只改脚本和测试。
- TEST：覆盖成功、错误 profile、错误 commit、public-release 默认路径。
- REVIEW：确认剩余外部证据仍 pending，不被误报 pass。
- SHIP：任务文档 closeout，任务树校验通过。

禁止跳过任何 gate；不得用文件存在替代内容校验，不得把本地 quick CI 证据扩展解释为远端 CI 或生产发布通过。

# Simplest Path
复用已有 `--local-ci-summary` 参数，不新增 release gate evidence ID；只把 summary 从文本升级为 JSON，并在 live gate 里严格校验。

# Split Strategy
按证据链方向拆分：生产证据 -> 校验证据 -> 上游门禁传递 -> 验收。

# Execution Waves
- Wave 1：TP-01.01
- Wave 2：TP-02.01、TP-03.01
- Wave 3：TP-04.01
- Wave 4：TP-05.01

# Runtime Workflow Contract
- risk_level: medium
- affected_flows: local quick CI, public release gate, live release gate
- external_contracts: `contracts/fate/delivery/release-gate.json`
- data_flow: local-ci writes summary JSON; public-release/live-release consume it
- state_changes: filesystem artifacts only under configured output directories
- side_effects: no external network beyond existing optional release gate behavior
- rollback: revert script/test/doc changes; remove 0041 task row if needed
- required_tests: targeted pytest, shell syntax, release gate smoke, task docs validation

# Next Executable Leaves
TP-02.01、TP-03.01

# Dependency Graph
- TP-01.01 -> TP-02.01
- TP-01.01 -> TP-03.01
- TP-02.01 + TP-03.01 -> TP-04.01
- TP-04.01 -> TP-05.01

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
