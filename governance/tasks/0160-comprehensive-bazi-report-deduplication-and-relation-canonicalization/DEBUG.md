# Debug Record

## Bug

- 标题：综合八字报告重复渲染与地支关系双真相源
- 症状：综合八字标准 Markdown 重复输出五行、天干、长生和调候内容；地支关系同时出现反向重复、单支自关联和另一套不同格式的关系结论；结构化结果保留内容相同的神煞别名。
- 首次发现位置 / 时间：2026-07-15 对已修复神煞重复问题开展同类灯下黑审查时发现。

## Environment

- 仓库 / 模块：FateCat `main`；`fate-core` 八字计算与 `fatecat-delivery` Markdown 渲染。
- 运行环境：Ubuntu / Python 3；项目当前本地依赖环境。
- 依赖 / 版本：以当前 `pyproject.toml` 和 lock 文件为准；关系成熟规则源为项目已登记的 bazi-1 资产。
- 配置差异：使用匿名北京样本，不依赖外部网络、token、数据库或生产配置。

## Reproduction

1. 对匿名 `1990-01-01 08:00`、北京、男命生成默认综合八字报告。
2. 统计 Markdown 标题和连续表格块，比较完全相同内容的位置。
3. 查看 `branchRelations.conflictsDetail` 与 `ganzhiRelations.diZhi`，检查自关联、反向重复和跨字段重复。
4. 比较 `spirits`、`spiritsFull` 与 `spiritsExplain` 的结构化值。

## Observations

- O1：`### 五行分数` 和 `### 天干分数` 各出现两次；完全重复表格位于 `[64, 258]`、`[74, 268]`、`[89, 283]`。
- O2：同一样本的 `branchRelations.conflictsDetail` 有 10 条，包含 `时支辰刑时支辰`、`时支辰被刑时支辰`，但四柱只有一个辰。
- O3：巳寅刑害、子辰合等关系同时输出正向和反向文本；`ganzhiRelations.diZhi` 又以第二套格式输出 3 条关系。
- O4：`spirits == spiritsFull`，`spiritsExplain == spiritsFull.descriptions`；当前报告已只渲染 canonical 神煞块，但 API 数据别名仍在。
- O5：结构测试明确期待两组五行/天干标题，说明测试把重复行为固化为正确契约。
- O6：同一匿名样本的紫微报告为 249 行，未发现重复标题或完全重复表格。

## Hypotheses

### H1: （ROOT HYPOTHESIS）缺少字段与规则的单一所有权
- Supports：`generate_bazi_standard_report` 顺序拼接多个各自读取重叠 root fields 的 renderer；核心同时返回三套关系结构和三套神煞别名。
- Conflicts：不同章节展示同一字段有时可能是有意摘要，不能仅凭字段复用判定为缺陷。
- Test：建立字段到章节和字段到计算源矩阵；完全相同块、无独占语义的重复以及冲突关系应全部落在无唯一 owner 的字段上。

### H2: `_calc_zhi_relations` 未按柱位实例建立关系键
- Supports：函数先把目标降为 `branch_set`，再把所有同支位置展开；未排除来源柱位，最终只按文本去重。
- Conflicts：辰辰、午午等自刑在存在两个同支实例时确实需要保留，不能一律排除同字关系。
- Test：对单辰与辰辰样本分别断言 0 条和 1 条自刑，并检查两个不同柱位。

### H3: 独立硬编码 `_calc_ganzhi_relations` 是关系结果不一致的来源
- Supports：该函数自行维护合冲刑害破表，与 `_calc_zhi_relations` 和 `_calc_ganzhi_extra` 并行返回，报告同时消费。
- Conflicts：它可能包含其他成熟源暂未投影的天干或半合展示信息。
- Test：以成熟规则结果构建 canonical 模型并生成兼容投影；若所有 golden 和边界关系均能覆盖，则确认第二套算法没有存在必要。

### H4: 消费者清单遗漏会让旧事实源在辅助评测中继续生效
- Supports：主报告与主要 evaluator 已迁移，但独立 benchmark evaluator 可能按旧 evidence 路径读取关系数据并静默得到默认值。
- Conflicts：全仓字段扫描已覆盖多数生产目录，遗漏未必存在。
- Test：只提供 `branchRelations.canonical` 调用 MingLi 关系压力函数，断言四条冲刑害破得到 `4/12`。

### H5: 无序集合会破坏 canonical 证据的跨进程确定性
- Supports：刑关系先聚合到 `set`，随后直接迭代进入有序输出列表。
- Conflicts：单进程测试和部分输入可能恰好保持相同顺序。
- Test：用多个 `PYTHONHASHSEED` 在独立进程计算同一命盘并比较 canonical 键序列。

### H6: 对容器级兼容标记会错误弃用仍有效的字段
- Supports：`ganzhiRelations` 同时承载当前天干事实和地支兼容投影，布尔弃用标记无法表达字段级边界。
- Conflicts：若所有内部消费者都迁出整个容器，容器级弃用可以成立。
- Test：对照 profile、rule registry、evaluator 和 renderer 的实际字段读取，确认 `tianGan` 与 `diZhi` 的事实源资格不同。

## Experiments

### E1
- Hypothesis: H1
- Change: 不修改代码，仅对一个匿名八字结果执行标题、表格和关系探针。
- Expected: 若假设成立，应同时发现 renderer 重叠、单支自关联和跨关系字段重复。
- Result: 检测到 2 个重复标题、3 张完全重复表格、2 条单辰自关联、多个反向关系以及 3 条第二格式关系。
- Verdict: confirmed
- Revert: 只读实验，无需回滚。

### E2
- Hypothesis: H3
- Change: 使用当前工作树和匿名北京样本运行可复制探针，统计 Markdown 标题、连续表格、关系明细、兼容地支视图和神煞别名。
- Command: `PYTHONPATH=domains/fate-analysis/services/fate-core/src:domains/experience-delivery/services/fatecat-delivery/src .venv/bin/python - <<'PY' ... BaziCalculator(datetime(1990,1,1,8), 'male', 116.4074, latitude=39.9042) ... PY`
- Expected: 当前旧实现应稳定暴露重复所有权、单辰自刑和第二套地支格式。
- Result: `duplicate_headings={'### 五行分数': 2, '### 天干分数': 2}`；重复表格起始行分别为 `[64,258]`、`[74,268]`、`[89,283]`；`conflictsDetail=10`，含两条单辰自关联；`ganzhiRelations.diZhi=3`；两个神煞别名比较均为 `True`；报告为 `95837 bytes / 1804 lines`。
- Verdict: confirmed
- Revert: 只读实验，无需回滚。

### E3
- Hypothesis: H2
- Change: 对照 bazi-1 自身关系展示逻辑与项目实现的实例匹配方式。
- Expected: 成熟实现应从候选列表中排除当前柱位实例，而项目实现没有排除。
- Result: bazi-1 使用 `others = zhis[:seq] + zhis[seq + 1:]`；项目旧实现先降为 `branch_set`，再从全量 `zhi_pos_map` 展开目标，因此会把来源柱位自身重新匹配回来。
- Verdict: confirmed
- Revert: 只读对照，无需回滚。

### E4
- Hypothesis: H4
- Change: 用只含 `branchRelations.canonical` 的结果调用 `mingli_baseline._relation_pressure()`。
- Expected: 四条冲刑害破关系应得到 `4/12` 的压力值。
- Result: 修复前返回 `0.0` 并触发 `AssertionError`；根因是函数仍把 `analysisEvidence.items.ganzhiRelations.conclusion.diZhi` 当成旧字典读取。
- Verdict: confirmed
- Revert: 已迁移为直接读取 `branchRelations.canonical`，并补定向回归。

### E5
- Hypothesis: H5
- Change: 分别以 `PYTHONHASHSEED=1..5` 在独立进程计算 `丑戌未辰` 的 canonical 关系键序列。
- Expected: 相同命盘在不同进程中必须输出完全相同的关系顺序。
- Result: 修复前至少出现两种刑关系顺序；根因是 `punishment_edges` 的集合迭代顺序未按柱位排序。
- Verdict: confirmed
- Revert: 已在进入关系对聚合前按来源柱位和目标柱位排序，并补跨哈希种子回归。

### E6
- Hypothesis: H6
- Change: 对照 `projectionOf`、profile、rule registry、evaluator 与报告消费者的字段级读取路径。
- Expected: 只有 `diZhi` 被标记为兼容投影和不可作为事实源，`tianGan` 保持当前天干事实语义。
- Result: 修复前布尔标记作用域过宽，且 evaluator 目录文档误写不存在的 `tianGanExtra`；代码实际读取 `ganzhiRelations.tianGan`。
- Verdict: confirmed
- Revert: 已改为 `deprecatedAsSourceFields=[diZhi]`，并同步 profile、文档、消费者审计和回归断言。

## Root Cause

- 当前确认的共同根因是：计算结果与报告章节没有 canonical ownership；兼容字段被当成事实源，成熟规则结果与独立硬编码算法并行存在，测试又只锁结构存在而未锁唯一性。

## Fix

- 已完成目标契约：`FIELD_OWNERSHIP.md` 固定章节所有权、canonical 关系键、方向语义和兼容投影边界。
- 已建立关系和报告 red tests，将地支关系收敛为 bazi-1 数据驱动的 `branchRelations.canonical`，并由它生成 `ganzhiRelations.diZhi` 兼容投影。
- 已按字段所有权删除重复 renderer；五行分数、天干分数、调候、日主、格局、运势和干支关系分别只有一个展示 owner。
- 已增加全报告唯一性、关系键、自刑基数、故障注入、紫微非误报和多端同源门禁。

## Regression Evidence

- E4 定向回归：`104 passed in 58.03s`，覆盖 statement golden、报告结构、profile 契约、八字/紫微规则深度和 capability 协议。
- E5 多端与体系回归：`15 passed in 6.60s`；六个本地交付面 normalized Markdown hash 一致，八字和紫微标准报告均无重复标题或完全重复业务表格。
- E6 renderer benchmark：同一结构化结果、同一进程、各 25 次；旧 renderer `95085 bytes / 1771 lines / median 1.939ms`，当前 `93689 bytes / 1666 lines / median 1.940ms`；体积 `-1.47%`、行数 `-105`、耗时 `+0.05%`，无显著退化。
- E7 当前并发工作树第一次 quick CI 在 secret scan 被 0159 的 `DEBUG.md` 误报阻断；临时排除该未跟踪目录后第二次运行又只被 0159 的两份未格式化 Python 文件阻断。本任务未修改这些文件。
- E8 在 `/tmp/fatecat-0160-clean` 从当前 HEAD 建立干净副本，仅应用 0160 明确文件清单后执行 `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0160-clean`：完整通过，包含 `467 passed in 87.00s`、ruff、format、mypy、八字/紫微 L4 golden、多端 semantic diff、核心性能、供应链和 whitespace gate。
- E9 在最终隔离副本 `/tmp/fatecat-0160-final-PhEZGQ` 重新应用 0160 文件并执行 quick CI：`468 passed in 79.78s`，ruff、format、71 个 fate-core 源文件 mypy、八字/紫微 L4 golden、多端 semantic diff、性能、供应链和 whitespace gate 全部通过；随后 governance strict、health、principle gate、案例库与任务 closeout strict 均通过。
- 备注：外部数据库、真实 Bot 和线上服务仍按仓库既有契约标记为“外部连通验证待执行”；它们不属于本任务范围。

## Failed Nodes

- 当前无 0160 失败节点；TP-06 审查与 closeout 尚在执行。

## First Invalid Node

- 无；原首个无效节点 TP-02.01 已通过 red/green 回归闭合。

## Upstream Lineage

- `BaziCalculator.calculate` 顶层结果装配、关系计算函数和 `generate_bazi_standard_report` 章节编排。

## Downstream Blast Radius

- 综合八字结构化 API、标准 Markdown、Web/API/Bot/CLI 同源输出、证据字段和报告结构测试。

## Lowest Common Refinement Ancestor

- 综合八字计算结果与报告字段所有权边界。

## Repair Boundary

- `bazi_calculator.py`、`report_generator.py`、相关 profile/证据契约和回归测试；不扩展其他体系。

## Frozen Nodes

- 紫微算法与报告内容、新能力开发、Web 视觉、地点时区、生产部署、0159 语料任务。

## Invalidated Nodes

- 当前“无重复、关系正确、单一事实源”的综合八字交付声明需要重新验证。

## Reverification Required

- 动态复现、关系边界 red/green、报告唯一性 red/green、多端 parity、紫微非回归、性能、quick CI、review 与 governance strict。
