# 综合八字报告去重与关系规范化审查

## Verdict

- Decision: PASS（0160 任务范围）
- Depth: deep
- Scope: correctness, architecture, contract, concurrency, performance, test-quality, future-optimal-drift, ponytail-complexity, document-drift
- Blocking findings in scope: 0
- Active warnings in scope: 0
- Delivery boundary: 本结论只覆盖 0160 文件清单；0159 语料任务及其依赖、脚本、测试和治理改动不属于本次审查。

## Findings

### RESOLVED-01：辅助评测消费者仍读取旧关系路径

- Severity: BLOCK（已修复）
- Evidence: `DEBUG.md` H4/E4；`fate_core/evaluation/mingli_baseline.py::_relation_pressure()`。
- Impact: 主报告已经迁移到 `branchRelations.canonical`，但 MingLi 评测会静默返回零关系压力，形成“生产输出正确、评测证据失真”的灯下黑。
- Fix: 直接读取顶层 `branchRelations.canonical`，不再把旧 evidence conclusion 当成关系事实源。
- Validation: 只提供 canonical 四条冲刑害破关系的定向回归得到 `4/12`。

### RESOLVED-02：刑关系集合迭代导致跨进程顺序不稳定

- Severity: BLOCK（已修复）
- Evidence: `DEBUG.md` H5/E5；`bazi_calculator.py` 中 `punishment_edges` 进入 canonical 聚合前的柱位排序。
- Impact: 相同命盘可能因 `PYTHONHASHSEED` 不同而产生不同关系顺序，破坏 golden、缓存键、证据 hash 和多端可复现性。
- Fix: 按来源柱位和目标柱位稳定排序后再生成 canonical 关系。
- Validation: 多个独立进程、不同哈希种子输出完全相同的 canonical key 序列。

### RESOLVED-03：容器级弃用标记错误覆盖仍有效的天干事实

- Severity: WARN（已修复）
- Evidence: `DEBUG.md` H6/E6；`ganzhiRelations.deprecatedAsSourceFields=["diZhi"]`；profile、rule registry 与 evaluator 文档同步。
- Impact: 原布尔标记无法表达 `tianGan` 仍是当前事实、只有 `diZhi` 是兼容投影，且文档曾引用不存在的 `tianGanExtra`。
- Fix: 改为字段级弃用，明确 `diZhi -> branchRelations.canonical`；保留 `tianGan` 当前语义并修正文档。
- Validation: profile、结构化结果和消费者审计断言一致。

## Correctness And Contract

- `branchRelations.canonical` 是地支关系唯一事实源；每条记录具有稳定 `key`、柱位实例、地支、方向、完整度、五行和来源。
- 单个辰、午、酉、亥不会产生需要两个实例才成立的自刑；两个不同柱位实例只生成一条自刑关系。
- 对称关系按 canonical key 唯一；方向关系保留方向语义；`ganzhiRelations.diZhi` 只由 canonical 投影。
- `ganzhiRelations.tianGan` 继续承载天干关系事实，不被地支兼容迁移错误弃用。
- 20,736 个四支组合的穷举探针共检查 99,360 条关系，未发现重复 key、同柱自关联、柱位/地支数量错配或兼容投影重复；单盘最大关系数为 12。

## Report Ownership

- 神煞章节只消费 `spiritsFull`；不再同时渲染 `spirits`、`spiritsExplain` 或“简表神煞”。
- 五行、天干、调候、格局、节气、运势和干支关系各自只有一个章节 owner。
- 干支关系只渲染一次 canonical 章节，兼容字段不再单独输出。
- 唯一性测试同时检查重复标题、完全重复业务表格和故障注入负例；紫微报告使用同一扫描器验证无误报。

## Architecture And Complexity

- Target end state 已满足：一个业务概念只有一个内部事实源，旧公开字段仅作为显式兼容投影。
- 未引入新生产框架、服务、依赖或通用去重平台；复用 bazi-1 关系数据、现有 calculator、renderer 和 pytest。
- `_calc_zhi_relations` 时间复杂度为 `O(P^2 + C)`，其中四柱 `P <= 4`，成熟规则组合 `C` 为固定小集合；空间复杂度为 `O(R)`，穷举观测单盘 `R <= 12`。
- 报告唯一性扫描只存在于测试，按报告行数线性执行，不进入生产热路径。
- renderer 同进程 25 次 benchmark：旧版 `95085 bytes / 1771 lines / median 1.939 ms`，当前 `93689 bytes / 1666 lines / median 1.940 ms`；体积下降 1.47%，减少 105 行，耗时变化 0.05%，无显著退化。
- 暂不继续微优化：四柱关系规模有硬上限，进一步缓存或抽象会增加维护成本而无可测收益。

## Concurrency, Security And Reliability

- 新关系装配和报告渲染只处理请求内局部对象，不修改共享全局状态。
- 本任务不新增数据库、文件写入、网络调用、重试、token、权限或生产配置；CASE-0002、CASE-0005、CASE-0006 不适用。
- 输出顺序通过跨哈希种子测试固定，多次调用具有确定性和幂等性。

## Test Quality

- red/green 契约覆盖单支自刑、双实例自刑、对称关系、方向关系、错误记录注入和旧消费者路径。
- 报告门禁验证语义唯一性，不使用整份易变 Markdown 快照替代关键断言。
- 多端 normalized Markdown hash 一致；八字和紫微标准报告均通过重复标题/表格扫描。
- 目标回归最近结果为 `40 passed in 33.71s`；fate-core mypy 为 `Success: no issues found in 71 source files`。

## Audit Case Consumption

- `CASE-9001`：已消费并通过；字段所有权、消费者审计、canonical/compat 契约和防复发测试均有证据。
- `CASE-0003`：审查时命中任务状态漂移；TP-06 closeout 只在最终验证后关闭，避免完成声明先于证据。
- `CASE-0002`：无新增外部调用，不适用。
- `CASE-0005`：未替换专业工具链或算法 provider，不适用。
- `CASE-0006`：未修改交互回调或同步冷查询，不适用。
- 采样结论见 `AUDIT_CASE_SAMPLING.md`；项目私有模式进入 `governance/evidence/audit-cases/` overlay。

## Document Drift

- 已同步 pure-analysis profile、规则深度 registry、能力/架构/OI 文档、fate-core 与 delivery 的局部 `AGENTS.md`。
- `FIELD_OWNERSHIP.md` 是本任务的章节所有权证据，`CONSUMER_AUDIT.md` 记录 canonical 与兼容字段的真实消费者。
- 项目定位、运行入口、工具链和 catalog 未变化，不新增平行操作模型或 ADR。

## Evidence

- 目标关系、报告、profile、八字/紫微回归：104 passed。
- 多端与体系回归：15 passed。
- 最新审查修复定向回归：40 passed。
- fate-core mypy：71 个源文件无问题。
- 关系组合穷举：12^4=20,736 个输入组合、99,360 条关系、0 项结构违规。
- 最终 0160 隔离副本 quick CI：468 passed，并通过 ruff、format、mypy、L4 golden、多端 semantic diff、性能、供应链和 whitespace gate。
- governance strict exit 0（仅运行态空目录建议 WARN）、principle gate 0 finding、项目审计案例 strict、采样 strict 和 DEBUG conclude 均通过。
- 当前完整工作树 governance strict 与 health 均 PASS；全局案例库测试、项目 overlay closeout 均 PASS。
- 任务文档 closeout strict 与 `TASK_CLOSEOUT_PACKET.json` 由 TP-06.02 生成并验证。

## Unknowns And Release Boundary

- 外部数据库、真实 Bot、线上 API 和远端 CI 不属于本任务验证范围；外部连通验证待执行。
- 本地 PASS 不等同于已经 commit、push 或通过当前提交的远端 CI；版本控制交付由后续 `auto-github` 使用真实 Git 证据执行。
