# Repo Evidence
- 当前八字冷进程实测约 4.4 至 4.7 秒，热进程约 0.32 至 0.36 秒；主要热点在逐月 LiuYue.getGanZhi 调用
- report_generator.py 与 bazi_calculator.py 含超长函数，公开渲染与内部结果选择仍存在局部耦合
- capability registry 中 almanac/meihua 顶层 production 与 L3 validated 成熟度表达不一致
- HTTP request latency 不能代表异步 report job 的排队与计算时长
- bazi-1 与 sxwnl 许可证状态未知，完整运行时不满足无条件公开分发
- 任务 0159 已独立提交为 942b965，本任务从干净基线开始

# Constraints Matrix
- Target end state: 计算、证据、公开投影、执行状态、观测和分发边界各有单一机器真相源
- Real constraints: 公共 API、完整报告输出、未知许可证、人工专家证据、HF 生产环境和当前用户承诺
- Inertia constraints: 旧 status 命名、超长函数形状、内部字段直接拼接和全运行时打包习惯不能决定终态
- Wrong concept / wrong boundary: 可执行不等于生产成熟；内部结果不等于公开字段；HTTP 延迟不等于异步计算耗时
- Kill list: 隐式公开字段、重复逐月父级计算、成熟度双重语义、超长多职责函数、无任务级异步指标、受限资产混入公开包
- Proof point: 多样本泄露门禁、字节/语义等价性能回归、独立 fixture 来源校验、registry 一致性、metrics 测试与 clean-room 客户端 smoke 全部通过
- Falsifier: 优化改变任一柱/运/月结果，字段契约无法兼容，或客户端不能在无受限资产环境运行
- Migration slice: 先固化契约和测试，再逐项替换热路径与边界，最后统一验证和提交
- Rejected short-term patches: 不追加散落字符串 denylist、不用全局缓存掩盖重复计算、不把 unknown license 改成 allowed、不保留永久双 status
- Existence check: 八项均对应已复现风险或交付阻断，必须存在；通用报告框架、新队列服务和新预测体系不应存在
- Selected ladder rung: 现有项目契约、标准库、lunar-python、Prometheus 与打包工具优先；只增加薄投影、runner 和指标适配
- Skipped scope: 专业断语、人类评审、外部生产 live、新体系和视觉重构
- Ceiling / upgrade path: 当任务量跨进程或多副本时再把内存 job manager 升级为外部队列与共享 metrics
- Do-not-simplify: 隐私、完整输出、确定性、许可证阻断、错误状态和审计来源不可删除
- Minimal runnable check: quick CI 加各切片定向回归与 clean-room smoke
- Complexity review owner: auto-review ponytail-complexity 与 future-optimal-drift lenses

# Change Boundary
- 允许修改 fate-core、delivery、contracts、metrics、packaging、scripts、tests 与对应 AGENTS/governance 文档
- 禁止修改专业断语文本和第一项专家内容
- 禁止减少完整报告的数据范围或弱化许可证门禁

# Risk Matrix
- 热路径优化可能改变节气或流月边界，必须以现有输出和独立 golden 双重约束
- status 字段属于公开契约，迁移必须版本化且有明确弃用边界
- 报告 allowlist 过窄会误删用户需要字段，过宽会继续泄露内部元数据
- metrics 标签若包含用户输入会造成隐私泄露和高基数，标签只允许固定枚举
- 公开客户端若隐式 import 服务端模块会在 clean-room 中失效

# Assumptions and Falsification
- lunar-python 的公开对象可在不手写历法规则的情况下复用或缓存父级确定性结果
- 当前公开客户端以调用已部署 API 为主要能力，不需要携带受限计算 vendor
- 人类专家评审材料可以后续接入同一独立评测 schema

# Critical Ambiguities
- 公开 status 兼容边界需以现有 schema 和调用方扫描为准，若已对外暴露则保留单个有期限的 deprecated projection
- 独立准确性只证明 fixture 对照，不代表专业解释层已由专家认可

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: LiuYue.getGanZhi 冷启动重复父级计算
- 调试关注点: 公开 Markdown 与结构化证据字段边界
- 调试关注点: capability status/maturity 双重语义
- 调试关注点: 异步任务生命周期指标完整性
- 强制调试叶子节点: TP-03

# Task Package Context Map
## TP-01
- Step Key: `public-report-contract`
- 标题: 建立公开报告字段允许契约
- 类型: `Contract`
- 目标: 明确公开 Markdown 与机器证据的字段边界，并建立多样本防泄露门禁
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 公开字段契约；投影/验证薄层；泄露回归测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `cold-start-performance`
- 标题: 优化完整八字冷启动热路径
- 类型: `Performance`
- 目标: 消除逐月重复父级计算，保持完整输出和历法结果不变
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: public-report-contract
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 热路径优化；benchmark；等价回归
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `independent-accuracy`
- 标题: 建立独立准确性评测入口
- 类型: `Quality`
- 目标: 把外部 fixture、来源和容差与引擎自生成 golden 分离，并保留专家待审状态
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: public-report-contract
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 独立评测 runner；fixture manifest；可选 acceptance gate
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `capability-lifecycle`
- 标题: 统一 capability 生命周期语义
- 类型: `Contract`
- 目标: 让可执行状态、生命周期和成熟度在 registry/schema/executor/API 中含义一致
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: public-report-contract
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 统一 registry 字段；迁移契约；一致性测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `core-complexity`
- 标题: 收敛核心与报告职责复杂度
- 类型: `Refactor`
- 目标: 拆分超长计算与渲染职责，不改变结果和公共接口
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: cold-start-performance, capability-lifecycle
- 依赖节点 ID: TP-02, TP-04
- 输入: 无
- 输出: 小职责 helper/模块；行为保持测试；AGENTS/module context 同步
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `async-job-metrics`
- 标题: 补齐异步报告端到端指标
- 类型: `Observability`
- 目标: 记录排队、执行、结果大小、终态和过期，不采集用户输入标签
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: capability-lifecycle
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: job metrics；observability contract；回归测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-07
- Step Key: `public-distribution`
- 标题: 建立许可证安全的公开客户端闭包
- 类型: `Packaging`
- 目标: 公开包只含客户端、契约和文档，受限计算资产继续留在服务端并由门禁阻断
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: capability-lifecycle
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: 公开客户端包；distribution manifest；许可证门禁测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-08
- Step Key: `quality-closeout`
- 标题: 全量验证、审查与仓库卫生收口
- 类型: `Verification`
- 目标: 统一验证所有切片，更新治理真相源，形成语义提交并恢复干净工作树
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: core-complexity, independent-accuracy, async-job-metrics, public-distribution
- 依赖节点 ID: TP-05, TP-03, TP-06, TP-07
- 输入: 无
- 输出: REVIEW；closeout packet；语义提交；干净工作树
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
