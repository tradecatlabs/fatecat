# Acceptance Checklist

# Global Standards
- [x] 单个地支不会与自身发生需要两个实例才成立的关系
- [x] 同一对称关系按 canonical 键只出现一次
- [x] 报告不存在重复标题、完全重复业务表格或同字段多章节所有权
- [x] 所有唯一业务信息和证据仍然存在
- [x] 兼容字段仅由 canonical 结果投影，不独立计算
- [x] Web/API/Bot/CLI 同源，紫微无回归
- [x] DEBUG、测试、review、文档同步和回滚证据完整
- [x] 不混入 0159 或其他并发任务改动

# Task Package Checklists
## TP-01
- 标题: 确认缺陷基线与目标契约
- 验收项:
  - [x] `确认缺陷基线与目标契约` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把重复渲染、关系自关联、双向重复和结构化别名固化为可重复验证的缺陷基线，并确定章节字段所有权与 canonical 关系模型。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 建立动态复现与影响矩阵
- 验收项:
  - [x] 动态样本稳定复现两组重复标题和三张完全重复表格
  - [x] 稳定复现单个辰支错误自刑与对称关系双向重复
  - [x] 区分展示冗余、API 兼容别名和计算正确性缺陷
- Verify: 运行匿名八字报告重复扫描和关系输出探针，并把命令与摘要写入 DEBUG.md
- Gate: 所有已报告症状都有可重复输入、输出和源码调用链
- 输出物:
  - [x] DEBUG.md 中的最小复现证据
  - [x] 字段到章节与字段到计算源的影响矩阵
  - [x] 关系错误样本集合
- 标准清单:
  - [x] Verify: 运行匿名八字报告重复扫描和关系输出探针，并把命令与摘要写入 DEBUG.md
  - [x] Gate: 所有已报告症状都有可重复输入、输出和源码调用链
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 定义章节所有权与 canonical 关系契约
- 验收项:
  - [x] 每个静态字段只有一个 canonical 展示章节
  - [x] 对称、方向、组合和自刑关系拥有明确去重键
  - [x] ganzhiExtra、branchRelations、ganzhiRelations 不再被视为三套独立事实源
- Verify: 人工审查所有权表与现有 pure_analysis/profile/evidence 契约的字段映射
- Gate: 后续实现不需要自行猜测字段归属或关系语义
- 输出物:
  - [x] 章节字段所有权表
  - [x] canonical 关系键与方向语义
  - [x] 旧字段兼容投影边界
- 标准清单:
  - [x] Verify: 人工审查所有权表与现有 pure_analysis/profile/evidence 契约的字段映射
  - [x] Gate: 后续实现不需要自行猜测字段归属或关系语义
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 收敛干支关系计算真相源
- 验收项:
  - [x] `收敛干支关系计算真相源` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 消除独立硬编码关系算法与成熟规则源并行计算，修复自关联和对称重复，同时保留可审计依据。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 先写关系正确性失败测试
- 验收项:
  - [x] 单个辰支不得产生辰辰自刑
  - [x] 两个辰支的自刑结果只出现一次且带两个柱位
  - [x] 对称关系按无序柱位对只输出一次
  - [x] 关系依据仍可追溯到规则源
- Verify: 定向 pytest 在旧实现上按预期失败，失败原因与 DEBUG.md 一致
- Gate: 测试能区分真正自刑、方向关系和错误自关联
- 输出物:
  - [x] 关系正确性 red tests
  - [x] 匿名边界 fixture
- 标准清单:
  - [x] Verify: 定向 pytest 在旧实现上按预期失败，失败原因与 DEBUG.md 一致
  - [x] Gate: 测试能区分真正自刑、方向关系和错误自关联
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 实现 canonical 关系模型与兼容投影
- 验收项:
  - [x] 删除或停用独立硬编码的第二套关系判断
  - [x] 同一关系在 canonical 结果中只出现一次
  - [x] 兼容字段不得再次独立计算
  - [x] 现有证据字段能够映射到 canonical 关系结果
- Verify: 关系定向测试、八字 statement golden 与 evidence 回归通过
- Gate: 计算结果不存在双真相源、自关联或无依据关系
- 输出物:
  - [x] 单一关系计算路径
  - [x] 规范化关系键
  - [x] 兼容字段投影
- 标准清单:
  - [x] Verify: 关系定向测试、八字 statement golden 与 evidence 回归通过
  - [x] Gate: 计算结果不存在双真相源、自关联或无依据关系
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 收敛报告章节字段所有权
- 验收项:
  - [x] `收敛报告章节字段所有权` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 消除完全重复和无价值语义重叠，同时保留全部唯一业务信息与现有输出体系边界。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 先写全报告唯一性失败测试
- 验收项:
  - [x] 能够检测五行分数、天干分数和长生概要的完全重复
  - [x] 能够检测温湿度与拱神的重复所有权
  - [x] 能够检测同一神煞释义被渲染多次
  - [x] 不会把紫微不同运限的合法同名字段误报为重复
- Verify: 定向 pytest 在旧报告实现上按预期失败，并对紫微基线通过
- Gate: 测试检查语义所有权而非绑定整份易变长文本快照
- 输出物:
  - [x] 八字报告唯一性 red tests
  - [x] 紫微报告无重复基线
- 标准清单:
  - [x] Verify: 定向 pytest 在旧报告实现上按预期失败，并对紫微基线通过
  - [x] Gate: 测试检查语义所有权而非绑定整份易变长文本快照
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 按所有权重构报告渲染
- 验收项:
  - [x] 五行和天干分数只在五行喜忌章节展示一次
  - [x] 温湿度、拱神和调候只在寒湿燥热章节展示一次
  - [x] 日主概览不重复格局和完整五行分析
  - [x] 运势章节不重复静态空亡、司令和完整用神原文
  - [x] 所有原有唯一信息仍可在报告中找到
- Verify: 标准报告结构测试、唯一性测试和匿名报告语义 diff 通过
- Gate: 默认综合八字 Markdown 不含完全重复块或无所有权字段
- 输出物:
  - [x] 唯一章节渲染路径
  - [x] 更新后的标准 Markdown 结构
- 标准清单:
  - [x] Verify: 标准报告结构测试、唯一性测试和匿名报告语义 diff 通过
  - [x] Gate: 默认综合八字 Markdown 不含完全重复块或无所有权字段
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 治理兼容字段与机器契约
- 验收项:
  - [x] `治理兼容字段与机器契约` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 在不静默破坏公开调用方的前提下，把重复结构字段从内部事实源降为显式兼容投影并同步契约。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 审计公开字段依赖与迁移边界
- 验收项:
  - [x] 每个重复字段都有真实消费者证据或明确无消费者结论
  - [x] 不得仅因内部方便直接删除公开字段
  - [x] 不得继续把兼容字段描述成独立计算能力
- Verify: rg/contract/profile/catalog 扫描结果与 API 回归契约对齐
- Gate: 兼容决策有证据、版本策略和移除条件
- 输出物:
  - [x] 公开字段消费者清单
  - [x] 保留、弃用或迁移决策
  - [x] 版本与回滚边界
- 标准清单:
  - [x] Verify: rg/contract/profile/catalog 扫描结果与 API 回归契约对齐
  - [x] Gate: 兼容决策有证据、版本策略和移除条件
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 同步 profile、证据与文档契约
- 验收项:
  - [x] 机器契约只声明一个内部事实源
  - [x] 兼容字段的来源和弃用状态明确
  - [x] README、SKILL 或操作文档只在长期事实发生变化时同步
- Verify: contract/profile/evidence/文档回归与多端语义测试通过
- Gate: 代码、契约、测试和文档对 canonical/compat 的表述一致
- 输出物:
  - [x] 更新后的 pure_analysis/profile 契约
  - [x] 兼容投影说明
  - [x] 证据映射回归
- 标准清单:
  - [x] Verify: contract/profile/evidence/文档回归与多端语义测试通过
  - [x] Gate: 代码、契约、测试和文档对 canonical/compat 的表述一致
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 建立防复发质量门禁
- 验收项:
  - [x] `建立防复发质量门禁` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把本次灯下黑问题转化为稳定的全报告唯一性、关系正确性、多端一致性和性能门禁。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 补齐唯一性与关系门禁
- 验收项:
  - [x] 重复标题和完全重复业务表格默认失败
  - [x] 允许项必须有明确业务原因和最小 allowlist
  - [x] 关系键、柱位与自刑基数可机械验证
- Verify: pytest 运行新增门禁并通过故障注入负例
- Gate: 原问题的任一旧实现回潮都会使测试失败
- 输出物:
  - [x] 唯一性回归门禁
  - [x] 关系规范化回归门禁
  - [x] 误报边界说明
- 标准清单:
  - [x] Verify: pytest 运行新增门禁并通过故障注入负例
  - [x] Gate: 原问题的任一旧实现回潮都会使测试失败
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 执行多端回归与性能验证
- 验收项:
  - [x] Web/API/Bot/CLI normalized Markdown 一致
  - [x] 紫微报告无结构回归
  - [x] 报告生成耗时不得出现无解释的显著退化
  - [x] 输出体积下降但不丢失唯一字段
- Verify: 定向回归、bash scripts/local-ci.sh --profile quick 与最小 benchmark
- Gate: 正确性、兼容性、性能和多端一致性全部通过
- 输出物:
  - [x] 定向 pytest 结果
  - [x] quick CI 结果
  - [x] 报告大小与生成耗时前后对比
- 标准清单:
  - [x] Verify: 定向回归、bash scripts/local-ci.sh --profile quick 与最小 benchmark
  - [x] Gate: 正确性、兼容性、性能和多端一致性全部通过
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 审查、治理与交付收口
- 验收项:
  - [x] `审查、治理与交付收口` 达到其 objective，且依赖关系保持一致
- Verify: 核对目标完成并补充执行证据
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 完成 correctness、architecture、performance、test-quality 与 document-drift 审查，并形成可提交交接包。
- 标准清单:
  - [x] Verify: 核对目标完成并补充执行证据
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 执行修复后专项审查与案例采样
- 验收项:
  - [x] correctness 与 architecture 无 BLOCK
  - [x] 测试没有再次把重复行为写成正确契约
  - [x] 可复发模式完成项目级案例入库或记录明确 no-case reason
- Verify: auto-review 专项路由、审计采样 strict 校验与 governance strict
- Gate: 修复没有以新的兼容双轨或过度抽象替代旧问题
- 输出物:
  - [x] REVIEW.md
  - [x] AUDIT_CASE_SAMPLING.md
  - [x] 文档漂移结论
- 标准清单:
  - [x] Verify: auto-review 专项路由、审计采样 strict 校验与 governance strict
  - [x] Gate: 修复没有以新的兼容双轨或过度抽象替代旧问题
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 生成 closeout 与 Git 交付交接
- 验收项:
  - [x] 所有叶子任务和 checklist 已真实关闭
  - [x] DEBUG.md 通过 conclude 校验
  - [x] closeout 不混入 0159 或其他并发任务改动
  - [x] 提交、推送和远端 CI 由 auto-github 单独执行并保留真实证据
- Verify: validate_task_docs --phase closeout 与 build_task_closeout --audit-case-sampling-required
- Gate: 任务证据完整、工作树边界清晰且可安全交付
- 输出物:
  - [x] TASK_CLOSEOUT_PACKET.json
  - [x] Git 交付边界与验证摘要
- 标准清单:
  - [x] Verify: validate_task_docs --phase closeout 与 build_task_closeout --audit-case-sampling-required
  - [x] Gate: 任务证据完整、工作树边界清晰且可安全交付
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
