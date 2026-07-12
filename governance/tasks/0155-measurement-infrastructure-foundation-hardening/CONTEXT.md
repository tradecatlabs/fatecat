# Repo Evidence
- HF /health=200 而 /ready=503，Telegram webhook enabled 但 not_ready
- 当前 wheel 安装后在仓库外执行 CLI 无法定位企业仓库根
- 当前 skill RC ZIP 约 218 MiB，导出脚本为整仓 denylist rsync
- 综合八字 legacy 与 capability 顶层字段集合不一致
- Acceptance 与 Container workflow 当前仅 workflow_dispatch
- core quality human review/external benchmark/no-leak gate 仍 blocked

# Constraints Matrix
- 保持当前 main，不切分支、不改写历史
- 优先复用 importlib.resources、GitHub Actions、现有 CapabilityExecutor 和现有门禁脚本
- Web 零美化语义 HTML 与现有字段契约保持不变
- 架构变化同步 AGENTS.md、contracts、catalog 或治理 context

# Change Boundary
- 只修改 packaging/export、bazi delivery orchestration、Telegram lifecycle、CI、vendor hygiene、governance/docs 和相应测试
- 不改变八字/紫微规则结论，不新增术数体系

# Risk Matrix
- 移除 legacy 可能影响未登记调用方，需兼容性测试和弃用记录
- 分发白名单遗漏资源会造成安装后运行失败，必须通过 clean-room smoke 证明闭包
- Telegram readiness 拆分不能掩盖渠道故障，必须保留独立状态和告警
- 自动 CI 可能增加 GitHub Actions 使用量，quick 与 release gate 必须分层

# Assumptions and Falsification
- 公开 Web/API 核心服务可以在 Telegram 渠道暂时故障时继续服务
- capability bazi 是唯一目标生产引擎；legacy 只允许迁移期兼容
- 真实专家/外部 live 证据只能由具备凭证和权限的 operator 提交

# Critical Ambiguities
- 外部是否仍有调用 /api/v1/bazi/simple 或 /calculate 不可从仓库完全确认；采用明确弃用兼容层并统一底层引擎
- Telegram 当前失败的具体外部错误值不可从公开指标获得；先补脱敏错误类型和退避，再用现有 HF secret 复验

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: wheel repo-root discovery failure
- 调试关注点: Telegram fixed retry and global readiness coupling
- 调试关注点: legacy/capability semantic divergence
- 调试关注点: export recursion and vendor pycache pollution

# Task Package Context Map
## TP-01
- Step Key: `distribution`
- 标题: 建立可独立分发闭包
- 类型: `Packaging`
- 目标: 让 core wheel 和 lite skill 在仓库外独立运行，并阻止运行态、嵌套导出和无关大资产进入发布包。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 包内资源闭包；allowlist/明确分发清单；分发回归测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `bazi-engine`
- 标题: 统一综合八字生产引擎
- 类型: `Architecture`
- 目标: 所有公开交付面通过 CapabilityExecutor 执行综合八字，旧接口只保留明确兼容契约。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: distribution
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 单引擎编排；弃用契约；语义一致性测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `telegram-readiness`
- 标题: 隔离 Telegram 渠道就绪状态
- 类型: `Reliability`
- 目标: 核心 readiness 与渠道 readiness 分层，Telegram 使用有界指数退避并输出脱敏失败类型。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: bazi-engine
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 分层 readiness；指数退避；错误观测与回归测试
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `ci-release`
- 标题: 补齐自动 CI 与发布证明
- 类型: `CI`
- 目标: quick gate 自动覆盖 PR/main push，重型容器发布保持受控并可生成当前提交证明。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: telegram-readiness
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: 自动 quick workflow；受控 release workflow；当前提交证据
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `supply-chain`
- 标题: 加固供应链与 vendor 卫生
- 类型: `Supply Chain`
- 目标: 阻止测试污染 reference repo，并让分发许可、revision 与分发允许状态可机械复核。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: ci-release
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: pycache 防污染；分发策略门禁；供应链证据
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `governance-truth`
- 标题: 恢复治理真相源
- 类型: `Governance`
- 目标: 补齐 review standard/module contexts，刷新过期事实文档并收敛任务索引。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: supply-chain
- 依赖节点 ID: TP-05
- 输入: 无
- 输出: 评审标准；module contexts；事实文档和任务状态同步
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-07
- Step Key: `quality-closeout`
- 标题: 性能、质量与交付收口
- 类型: `Verification`
- 目标: 建立八字性能预算、执行完整门禁与审查，提交并推送所有已验证本地改动。
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: governance-truth
- 依赖节点 ID: TP-06
- 输入: 无
- 输出: 性能基线；审查结论；提交推送与远端证据
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
