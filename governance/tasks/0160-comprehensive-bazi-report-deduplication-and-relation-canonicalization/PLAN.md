# Planning Summary
先用动态样本和 red tests 锁定缺陷，再并行收敛关系计算与报告字段所有权；随后审计并迁移机器契约，建立全报告防复发门禁，最后执行多端、性能、治理和交付审查。

# Lifecycle Gates
- SPEC：缺陷分类、目标终态、真实约束和兼容边界已落盘。
- PLAN：十二个叶子节点、依赖波次、验证命令和回滚边界明确。
- BUILD：先 red tests，再分别修改 core 关系模型与 delivery 渲染；禁止跨范围重写。
- TEST：关系边界、报告唯一性、结构契约、多端 parity、紫微和性能验证通过。
- REVIEW：correctness、architecture、performance、test-quality、future-optimal-drift、document-drift 无 BLOCK。
- SHIP：closeout、审计案例采样和 Git 交付证据完整后才允许提交推送。
- 执行纪律：不得跳过 gate；任一 gate 未闭合时不得进入下一阶段。

# Simplest Path
复用现有 bazi-1 关系数据、BaziCalculator、report_generator 和 pytest 门禁；删除独立硬编码关系判断及重复 renderer，不新增新的规则库、报告框架或运行时服务。

# Split Strategy
按故障边界拆分为基线契约、关系计算、报告渲染、兼容契约、质量门禁和交付收口六个包；关系与报告实现可在共同契约确定后并行，契约同步和最终验证必须等待两者完成。

# Execution Waves
- Wave 1: TP-01.01
- Wave 2: TP-01.02
- Wave 3: TP-02.01, TP-03.01, TP-04.01
- Wave 4: TP-02.02, TP-03.02
- Wave 5: TP-04.02
- Wave 6: TP-05.01
- Wave 7: TP-05.02
- Wave 8: TP-06.01
- Wave 9: TP-06.02

# Runtime Workflow Contract
- 本任务需要语义 DAG，但不需要原子执行图：节点均为本地、确定性、可重试的代码与测试工作。
- TP-01 至 TP-06 已按依赖顺序完成，TP-02 与 TP-03 的写集保持 core/delivery 隔离。
- 最终隔离副本只应用 0160 文件，quick CI、治理 strict、任务 strict 和 closeout 均通过。
- 任务不需要原子执行图；所有节点已完成，不存在待恢复子图。

# Next Executable Leaves
- 无；12 个叶子节点全部完成。

# Dependency Graph
TP-01.01 -> TP-01.02
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.01
TP-01.01 -> TP-02.02
TP-01.02 -> TP-02.02
TP-02.01 -> TP-02.02
TP-01.01 -> TP-03.01
TP-01.02 -> TP-03.01
TP-01.01 -> TP-03.02
TP-01.02 -> TP-03.02
TP-03.01 -> TP-03.02
TP-01.01 -> TP-04.01
TP-01.02 -> TP-04.01
TP-01.01 -> TP-04.02
TP-01.02 -> TP-04.02
TP-02.01 -> TP-04.02
TP-02.02 -> TP-04.02
TP-03.01 -> TP-04.02
TP-03.02 -> TP-04.02
TP-04.01 -> TP-04.02
TP-02.01 -> TP-05.01
TP-02.02 -> TP-05.01
TP-03.01 -> TP-05.01
TP-03.02 -> TP-05.01
TP-04.01 -> TP-05.01
TP-04.02 -> TP-05.01
TP-02.01 -> TP-05.02
TP-02.02 -> TP-05.02
TP-03.01 -> TP-05.02
TP-03.02 -> TP-05.02
TP-04.01 -> TP-05.02
TP-04.02 -> TP-05.02
TP-05.01 -> TP-05.02
TP-05.01 -> TP-06.01
TP-05.02 -> TP-06.01
TP-05.01 -> TP-06.02
TP-05.02 -> TP-06.02
TP-06.01 -> TP-06.02

# Rollback Protocol
- 关系修复回滚必须整体恢复 canonical 模型、兼容投影、消费者与契约，禁止只恢复第二套硬编码算法。
- 报告修复可按 owner renderer 回滚，但不得恢复同一字段多章节消费。
- 回滚只触及 0160 文件清单，不得覆盖 0159 或其他并发任务。
