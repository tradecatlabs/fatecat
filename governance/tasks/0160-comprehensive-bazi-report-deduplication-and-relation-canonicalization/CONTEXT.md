# Repo Evidence
- 匿名 1990-01-01 08:00 北京男命样本实测：`### 五行分数` 与 `### 天干分数` 各出现 2 次。
- 同一样本检测到完全相同表格位置 `[64, 258]`、`[74, 268]`、`[89, 283]`。
- `branchRelations.conflictsDetail` 输出 10 条，其中包含单个辰支的 `时支辰刑时支辰`、`时支辰被刑时支辰` 以及合/刑/害反向重复。
- `ganzhiRelations.diZhi` 对同一命盘另行输出 3 条规范不同的关系结论。
- `spirits == spiritsFull`，且 `spiritsExplain == spiritsFull.descriptions`。
- `tests/regression/test_branding_support.py` 当前结构契约明确期待两组五行/天干分数标题，只对神煞建立了唯一性断言。
- 紫微标准报告实测 249 行，未发现重复标题或完全重复表格。

# Constraints Matrix
- 保持当前 `main` 分支，不切换分支、不改写历史。
- 当前 worktree 存在 0159 及其依赖、脚本、测试和治理文档并发改动；本任务不得覆盖、回滚或混入这些文件。
- 核心关系规则优先复用已登记的成熟 bazi-1 数据，不新增第二套硬编码命理规则。
- 报告去重必须保留全部唯一信息，不得以删除章节掩盖数据缺失。
- 公开字段变更必须先审计 profile、contract、文档和消费者，再决定兼容投影或版本迁移。
- Web/API/Bot/CLI 必须继续调用同一 report profile，不允许各交付面自行去重。

# Change Boundary
- 实际业务修改覆盖 fate-core canonical 关系装配与消费者、delivery 报告 renderer/formatter、profile/规则 registry、golden 与既有回归测试。
- 长期事实同步到 fate-core/delivery 局部 `AGENTS.md`、架构/OI/能力文档和项目审计案例 overlay；catalog、运行入口与工具链不变。
- 未新增生产脚本、报告框架、规则引擎、运行时服务或外部依赖。
- 0160 交付清单显式排除 0159 的依赖、抓取脚本、测试和治理改动。

# Risk Matrix
- P0 正确性：单支错误自刑、关系双向重复或两套算法结论不一致。
- P0 兼容性：直接删除旧字段可能破坏 API/Agent 调用方。
- P1 完整性：去重时误删只在某一章节出现的唯一依据。
- P1 测试质量：快照继续把重复输出固化为正确行为。
- P2 性能：规范化或兼容投影若重复遍历，可能抵消报告去重收益。
- P2 文档漂移：代码改成 canonical/compat 后，profile 与说明仍宣称多套独立能力。

# Assumptions and Falsification
- 假设 A：`ganzhiExtra` 与 `branchRelations` 的成熟规则数据足以构建 canonical 关系模型；若匿名边界样本证明缺失必要关系，则重新评估 provider，而不是恢复独立硬编码算法。
- 假设 B：重复表格没有独占信息；若字段级 diff 发现唯一内容，则先迁移到所属章节再删除旧渲染。
- 假设 C：旧字段可能存在外部消费者；在没有版本化迁移证据前保留为纯投影，不直接删除。
- 假设 D：紫微当前无同类完全重复；若更大 fixture 扫描发现反例，则另建独立任务，不把紫微改动混入本任务。

# Critical Ambiguities
- `ganzhiRelations` 当前既是公开字段又是独立硬编码算法；计划采用“canonical 内部模型 + 旧字段纯投影”，最终删除时间取决于消费者审计。
- 刑关系是否方向化必须以成熟规则源和既有证据契约为准；不得用简单无序去重误删真实方向信息。
- 原标准结构曾明确包含两组五行分数标题；修复需要同步结构契约，而不是只修改生成器。

# Debug Evidence Contract
- 调试模式: Required
- 当前任务目录必须持续维护 `DEBUG.md`。
- BUILD 前必须完成 observe/hypothesize 校验；修复完成后必须通过 conclude 校验。
- 每个关系和报告修复必须记录 red/green 或等价回归证据。
- closeout 的 Recent Evidence 必须回指 DEBUG、测试和 review。

# Future-Optimal Task Contract

- Target end state: 综合八字内部每个业务概念只有一个计算事实源，每个报告字段只有一个 canonical 展示章节；公开旧字段只能由 canonical 结果投影。
- Real constraints: 保持成熟规则源、公开 API 兼容性、证据可追溯、多端同源输出和唯一信息完整。
- Inertia constraints: 旧标题顺序、旧 renderer 边界、历史结构快照和内部字段别名不得决定终态。
- Wrong concept / wrong boundary: 把兼容字段当事实源、把章节拼装函数当字段 owner、把独立硬编码关系表当第二生产引擎。
- Kill list: 独立 `_calc_ganzhi_relations` 规则判断、重复五行/调候 renderer、兼容字段独立渲染和锁定重复行为的测试期望。
- Proof point: 单辰无自刑、对称关系唯一、标准报告无重复业务块、唯一信息 diff 完整、多端 parity 通过。
- Falsifier: 成熟关系源无法覆盖现有必要关系，或去重导致唯一证据/公开兼容数据无法恢复。
- Migration slice: 先 red tests 和所有权契约，再分别迁移关系计算与报告渲染，最后同步兼容契约和门禁。
- Rejected short-term patches: 不在渲染末尾做字符串去重，不只过滤当前样本的辰自刑，不保留两套算法后比较选一，不靠扩张 allowlist 放过重复。
- Future-optimal review owner: `auto-review: future-optimal-drift`。

# Ponytail Task Contract

- Existence check: P0 正确性缺陷和已复现报告冗余证明任务与回归门禁现在必须存在。
- Selected ladder rung: 复用成熟规则源与项目现有 renderer/test 能力；仅编写 canonical 适配、投影和业务所有权代码。
- Skipped scope: 不新增报告框架、规则引擎、命理规则、运行时服务或通用去重平台。
- Ceiling / upgrade path: 只有新增更多生产 capability 且出现跨体系复用需求时，才评估抽取通用 report ownership contract。
- Do-not-simplify: 不得删除唯一信息、证据、公开兼容边界、方向关系语义或多端一致性验证。
- Minimal runnable check: 关系边界 pytest、标准报告唯一性 pytest 和 multi-surface parity。
- Complexity review owner: `auto-review: ponytail-complexity`。

# Engineering Change Safety

- Impact surface: fate-core 八字结构化结果、delivery Markdown、pure_analysis/profile/evidence 契约和现有回归测试。
- Data/control/state: 仅处理请求内确定性字典与 Markdown，不增加持久状态、数据库迁移或后台任务。
- Side effects: 无外部网络和持久化副作用；测试不得写 vendor、日志或真实用户报告。
- Concurrency/idempotency: 纯函数式关系规范化和 renderer 必须可重复调用且不修改共享全局对象。
- Failure recovery: 每个实现切片可通过对应 red/green commit 回退；兼容投影可在不恢复第二算法的前提下单独保留。
- Compatibility: 先审计消费者；公开旧字段在当前版本只能保留为 canonical 投影或走明确版本迁移。
- Observability: 不新增生产日志；失败由确定性测试、报告 diff 和 API contract gate 暴露。
- Release/rollback: 本地 quick 与 review 无 BLOCK 后才交给 auto-github；回滚不得恢复双真相源。

# Document-Driven Task Contract

- Operating model update: `not needed`；项目定位与操作模型不变。
- Toolchain model update: `not needed`；复用现有 pytest、local-ci、auto-review 和 governance 校验。
- Process update: `completed`；项目特有复发模式进入 `governance/evidence/audit-cases/`，未新增平行流程。
- Source-of-truth updates: `completed`；报告结构测试、pure_analysis profile、rule registry 与 evidence 映射已同步。
- Local README/AGENTS impact: `completed`；fate-core kernel/providers/evaluators 与 delivery 局部 `AGENTS.md` 已同步职责边界。
- Contract/catalog/schema impact: `completed`；profile/规则契约已更新，catalog 与持久化 schema 不受影响。
- ADR/Gate/module-context impact: `completed with exemption`；CASE-9001 记录项目复发模式，现有局部 `AGENTS.md` 足以承载模块边界，无需新 ADR 或 module context。
- Documentation exemption reason: 项目定位、操作模型、工具链和 catalog 未变化，不创建平行文档体系。
- Validation evidence: 隔离 quick CI 468 passed；governance strict、principle gate、案例 strict、DEBUG conclude 与任务 closeout strict 通过。

# Task Package Context Map
## TP-01
- 标题: 确认缺陷基线与目标契约
- 目标: 把重复渲染、关系自关联、双向重复和结构化别名固化为可重复验证的缺陷基线，并确定章节字段所有权与 canonical 关系模型。
- 有效叶子依赖: -
- 当前状态: Done

### TP-01.01
- 标题: 建立动态复现与影响矩阵
- 目标: 使用匿名八字样本复现重复标题、重复表格、单辰自刑、对称关系双向输出和 API 别名重叠，并记录精确输出与调用链。
- 有效叶子依赖: -
- 当前状态: Done

### TP-01.02
- 标题: 定义章节所有权与 canonical 关系契约
- 目标: 确定每类八字数据的唯一展示章节，并定义由成熟规则源生成、可规范化和可投影的唯一干支关系内部模型。
- 有效叶子依赖: TP-01.01
- 当前状态: Done

## TP-02
- 标题: 收敛干支关系计算真相源
- 目标: 消除独立硬编码关系算法与成熟规则源并行计算，修复自关联和对称重复，同时保留可审计依据。
- 有效叶子依赖: -
- 当前状态: Done

### TP-02.01
- 标题: 先写关系正确性失败测试
- 目标: 用单辰、辰辰、巳寅、子辰及无关系样本建立 red tests，锁定自刑基数、对称去重、方向关系和半合边界。
- 有效叶子依赖: TP-01.01, TP-01.02
- 当前状态: Done

### TP-02.02
- 标题: 实现 canonical 关系模型与兼容投影
- 目标: 以现有成熟 bazi-1 关系数据为事实来源，规范化柱位、关系类型、方向、完整度和五行，并由 canonical 模型生成必要的旧字段投影。
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01
- 当前状态: Done

## TP-03
- 标题: 收敛报告章节字段所有权
- 目标: 消除完全重复和无价值语义重叠，同时保留全部唯一业务信息与现有输出体系边界。
- 有效叶子依赖: -
- 当前状态: Done

### TP-03.01
- 标题: 先写全报告唯一性失败测试
- 目标: 建立标题、表格、静态字段所有权和神煞唯一性 red tests，并保留紫微独立报告的非回归扫描。
- 有效叶子依赖: TP-01.01, TP-01.02
- 当前状态: Done

### TP-03.02
- 标题: 按所有权重构报告渲染
- 目标: 将四柱、日主、五行、调候、格局、节气、关系和运势数据分别收敛到唯一章节，删除重复渲染分支。
- 有效叶子依赖: TP-01.01, TP-01.02, TP-03.01
- 当前状态: Done

## TP-04
- 标题: 治理兼容字段与机器契约
- 目标: 在不静默破坏公开调用方的前提下，把重复结构字段从内部事实源降为显式兼容投影并同步契约。
- 有效叶子依赖: -
- 当前状态: Done

### TP-04.01
- 标题: 审计公开字段依赖与迁移边界
- 目标: 盘点 spirits、spiritsFull、spiritsExplain、ganzhiExtra、branchRelations 和 ganzhiRelations 在 profile、文档、测试及交付面的真实依赖。
- 有效叶子依赖: TP-01.01, TP-01.02
- 当前状态: Done

### TP-04.02
- 标题: 同步 profile、证据与文档契约
- 目标: 将 canonical 字段和兼容投影的关系写入 profile、证据索引、开发文档与回归测试，消除机器契约继续鼓励双真相源的可能。
- 有效叶子依赖: TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01
- 当前状态: Done

## TP-05
- 标题: 建立防复发质量门禁
- 目标: 把本次灯下黑问题转化为稳定的全报告唯一性、关系正确性、多端一致性和性能门禁。
- 有效叶子依赖: -
- 当前状态: Done

### TP-05.01
- 标题: 补齐唯一性与关系门禁
- 目标: 将标题唯一、表格唯一、章节字段所有权、关系规范化和无单支自刑加入现有回归测试，不新增无必要生产抽象。
- 有效叶子依赖: TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01, TP-04.02
- 当前状态: Done

### TP-05.02
- 标题: 执行多端回归与性能验证
- 目标: 验证 Web、API、Bot、CLI 继续同源输出，八字与紫微报告结构正确，并量化去重后的体积与耗时变化。
- 有效叶子依赖: TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01, TP-04.02, TP-05.01
- 当前状态: Done

## TP-06
- 标题: 审查、治理与交付收口
- 目标: 完成 correctness、architecture、performance、test-quality 与 document-drift 审查，并形成可提交交接包。
- 有效叶子依赖: -
- 当前状态: Done

### TP-06.01
- 标题: 执行修复后专项审查与案例采样
- 目标: 复核是否仍有双真相源、重复字段、错误自关联、兼容壳扩散或测试灯下黑，并完成审计案例采样决定。
- 有效叶子依赖: TP-05.01, TP-05.02
- 当前状态: Done

### TP-06.02
- 标题: 生成 closeout 与 Git 交付交接
- 目标: 收口 DEBUG、测试、审查、文档同步和回滚证据，生成任务 closeout，并交给 auto-github 执行后续版本控制。
- 有效叶子依赖: TP-05.01, TP-05.02, TP-06.01
- 当前状态: Done
