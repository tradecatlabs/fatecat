# Task Overview
- Task ID: `0160`
- Slug: `comprehensive-bazi-report-deduplication-and-relation-canonicalization`
- Objective: `修复综合八字报告重复渲染、地支关系自关联与双向重复，并收敛结构化结果和报告章节的单一事实源，建立全报告唯一性与关系正确性回归门禁。`
- Status: `Done`

## In Scope
- 综合八字标准 Markdown 的重复标题、重复表格和语义字段所有权
- 干支/地支关系的单一计算真相源、自关联、对称重复与兼容投影
- spirits 与关系相关结构化别名的公开消费者审计和迁移边界
- 八字、紫微、多端语义一致性和性能回归
- DEBUG、review、审计案例采样、治理与 closeout 证据

## Out of Scope
- 新增或调整八字命理规则、格局、喜忌、神煞释义或称骨内容
- 新增紫微、黄历、六爻、梅花、奇门等能力
- 修改 Web 视觉、地区控件、生产部署或外部 live 配置
- 无关仓库卫生、依赖升级、语料抓取或 0159 并发任务
- 未经版本契约审计直接删除公开 API 字段

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 确认缺陷基线与目标契约
  │  ├─ TP-01.01 [leaf] [P0] 建立动态复现与影响矩阵
  │  └─ TP-01.02 [leaf] [P0] 定义章节所有权与 canonical 关系契约
  ├─ TP-02 [branch] [P0] 收敛干支关系计算真相源
  │  ├─ TP-02.01 [leaf] [P0] 先写关系正确性失败测试
  │  └─ TP-02.02 [leaf] [P0] 实现 canonical 关系模型与兼容投影
  ├─ TP-03 [branch] [P0] 收敛报告章节字段所有权
  │  ├─ TP-03.01 [leaf] [P0] 先写全报告唯一性失败测试
  │  └─ TP-03.02 [leaf] [P0] 按所有权重构报告渲染
  ├─ TP-04 [branch] [P1] 治理兼容字段与机器契约
  │  ├─ TP-04.01 [leaf] [P1] 审计公开字段依赖与迁移边界
  │  └─ TP-04.02 [leaf] [P1] 同步 profile、证据与文档契约
  ├─ TP-05 [branch] [P0] 建立防复发质量门禁
  │  ├─ TP-05.01 [leaf] [P0] 补齐唯一性与关系门禁
  │  └─ TP-05.02 [leaf] [P0] 执行多端回归与性能验证
  └─ TP-06 [branch] [P0] 审查、治理与交付收口
     ├─ TP-06.01 [leaf] [P0] 执行修复后专项审查与案例采样
     └─ TP-06.02 [leaf] [P0] 生成 closeout 与 Git 交付交接

## Requirement Alignment
- 用户要求把本次重复与相似问题落盘，并制定可执行修复计划。
- 已确认神煞重复是同一计算结果通过兼容字段被重复渲染；当前展示已修复，但结构化别名仍存在。
- 已确认综合八字还存在五行/天干/长生表格完全重复、调候语义重复和关系双真相源。
- TP-01 至 TP-06 全部闭合；深度审查修复三个隐藏问题，最终隔离 quick CI、治理 strict、任务 closeout 与交付边界验证均通过。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | Package | No | - | - | No | No | 把重复渲染、关系自关联、双向重复和结构化别名固化为可重复验证的缺陷基线，并确定章节字段所有权与 canonical 关系模型。 |
| TP-01.01 | TP-01 | 2 | P0 | Bugfix | Yes | - | 1 | No | No | 使用匿名八字样本复现重复标题、重复表格、单辰自刑、对称关系双向输出和 API 别名重叠，并记录精确输出与调用链。 |
| TP-01.02 | TP-01 | 2 | P0 | Architecture | Yes | TP-01.01 | 2 | No | No | 确定每类八字数据的唯一展示章节，并定义由成熟规则源生成、可规范化和可投影的唯一干支关系内部模型。 |
| TP-02 | ROOT | 1 | P0 | Package | No | TP-01.01, TP-01.02 | - | No | No | 消除独立硬编码关系算法与成熟规则源并行计算，修复自关联和对称重复，同时保留可审计依据。 |
| TP-02.01 | TP-02 | 2 | P0 | Testing | Yes | TP-01.01, TP-01.02 | 3 | No | No | 用单辰、辰辰、巳寅、子辰及无关系样本建立 red tests，锁定自刑基数、对称去重、方向关系和半合边界。 |
| TP-02.02 | TP-02 | 2 | P0 | Bugfix | Yes | TP-01.01, TP-01.02, TP-02.01 | 4 | No | No | 以现有成熟 bazi-1 关系数据为事实来源，规范化柱位、关系类型、方向、完整度和五行，并由 canonical 模型生成必要的旧字段投影。 |
| TP-03 | ROOT | 1 | P0 | Package | No | TP-01.01, TP-01.02 | - | No | Yes | 消除完全重复和无价值语义重叠，同时保留全部唯一业务信息与现有输出体系边界。 |
| TP-03.01 | TP-03 | 2 | P0 | Testing | Yes | TP-01.01, TP-01.02 | 3 | No | Yes | 建立标题、表格、静态字段所有权和神煞唯一性 red tests，并保留紫微独立报告的非回归扫描。 |
| TP-03.02 | TP-03 | 2 | P0 | Refactor | Yes | TP-01.01, TP-01.02, TP-03.01 | 4 | No | Yes | 将四柱、日主、五行、调候、格局、节气、关系和运势数据分别收敛到唯一章节，删除重复渲染分支。 |
| TP-04 | ROOT | 1 | P1 | Package | No | TP-01.01, TP-01.02 | - | No | Yes | 在不静默破坏公开调用方的前提下，把重复结构字段从内部事实源降为显式兼容投影并同步契约。 |
| TP-04.01 | TP-04 | 2 | P1 | Contract | Yes | TP-01.01, TP-01.02 | 3 | No | Yes | 盘点 spirits、spiritsFull、spiritsExplain、ganzhiExtra、branchRelations 和 ganzhiRelations 在 profile、文档、测试及交付面的真实依赖。 |
| TP-04.02 | TP-04 | 2 | P1 | Contract | Yes | TP-01.01, TP-01.02, TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01 | 5 | No | No | 将 canonical 字段和兼容投影的关系写入 profile、证据索引、开发文档与回归测试，消除机器契约继续鼓励双真相源的可能。 |
| TP-05 | ROOT | 1 | P0 | Package | No | TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01, TP-04.02 | - | No | No | 把本次灯下黑问题转化为稳定的全报告唯一性、关系正确性、多端一致性和性能门禁。 |
| TP-05.01 | TP-05 | 2 | P0 | Testing | Yes | TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01, TP-04.02 | 6 | No | No | 将标题唯一、表格唯一、章节字段所有权、关系规范化和无单支自刑加入现有回归测试，不新增无必要生产抽象。 |
| TP-05.02 | TP-05 | 2 | P0 | Verification | Yes | TP-02.01, TP-02.02, TP-03.01, TP-03.02, TP-04.01, TP-04.02, TP-05.01 | 7 | No | No | 验证 Web、API、Bot、CLI 继续同源输出，八字与紫微报告结构正确，并量化去重后的体积与耗时变化。 |
| TP-06 | ROOT | 1 | P0 | Package | No | TP-05.01, TP-05.02 | - | No | No | 完成 correctness、architecture、performance、test-quality 与 document-drift 审查，并形成可提交交接包。 |
| TP-06.01 | TP-06 | 2 | P0 | Review | Yes | TP-05.01, TP-05.02 | 8 | No | No | 复核是否仍有双真相源、重复字段、错误自关联、兼容投影扩散或测试灯下黑，并完成审计案例采样决定。 |
| TP-06.02 | TP-06 | 2 | P0 | Delivery | Yes | TP-05.01, TP-05.02, TP-06.01 | 9 | No | No | 收口 DEBUG、测试、审查、文档同步和回滚证据，生成任务 closeout，并交给 auto-github 执行后续版本控制。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
8. REVIEW.md
