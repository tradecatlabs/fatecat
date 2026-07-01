# Repo Evidence
- governance/evidence/reviews/REVIEW-0001-业务代码业务模型与业务逻辑审计.md 结论为 BLOCK。
- F-001 指出 fate-core 通过 TELEGRAM_SRC_DIR 和 sys.path 反向依赖 fatecat-delivery。
- F-002 指出 calendarType、midnightMode、daylightSaving 暴露但未真实参与计算。
- F-003 指出 useTrueSolarTime=false 时 input.options 仍硬编码 true。
- F-004 指出 Web/API/Bot 没有完全共享同一业务真相源。
- F-005 指出 location.get 对 lng,lat 直接 float 返回但缺少范围校验。
- 当前 git status 显示仅 governance/ 下存在未提交变更和未跟踪治理文档，没有业务源码改动。

# Constraints Matrix
- 不得回滚或覆盖当前未提交治理资产，除非用户明确要求。
- 不得用文档关闭业务 BLOCK；必须有代码、测试和运行命令证据。
- 不得把未实现业务选项继续作为已应用配置保存。
- 不得为了快速消除 scan 结果而删除仍被运行链路需要的 adapter，必须先迁移再收口。
- 不得把 evaluation/oracle/reference 资源接入生产请求链路。

# Change Boundary
- 任务设计阶段只写 governance/tasks/0006-business-logic-audit-remediation 和 governance/tasks/INDEX.md。
- 修复执行阶段预计会改 domains/fate-analysis、domains/experience-delivery、tests/regression、contracts/fate 和 governance/evidence/reviews。
- 不修改 HF Space 发布配置、GitHub workflow 或前端视觉样式，除非测试发现与本任务直接相关。

# Risk Matrix
- high：迁移 delivery integration 模块可能影响八字、紫微、报告生成和 Bot 入口。
- high：业务选项从静默忽略改为 422 可能影响已有调用方，需要明确契约和测试。
- medium：统一入口可能触发 schema drift、import cycle 或性能变化。
- medium：坐标校验会拒绝历史上可输入但无意义的坐标，需要 Web/Bot 错误提示一致。
- medium：治理资产当前已有未提交变更，继续写入必须保持提交边界清晰。

# Integration Ownership Map
- `fate_core.support.paths.TELEGRAM_SRC_DIR`：当前提供 delivery `src` 路径；目标删除对 delivery `src` 的核心依赖，仅保留仓库根、contracts、vendor、runtime 等领域支撑路径。
- `fate_core.adapters.ziwei_iztro`：当前通过 `TELEGRAM_SRC_DIR` 修改 `sys.path` 后导入 `fortel_ziwei_integration`；目标改为从 `fate_core.adapters` 内部兼容模块导入。
- `fate_core.kernel.bazi_calculator` 扩展直导：`fortel_ziwei_integration`、`sxwnl_integration`；目标改为从 `fate_core.adapters.legacy_integrations` 之类的领域适配边界导入。
- `fate_core.kernel.bazi_calculator.calculate_complete` 动态加载：`sxwnl_integration.py`、`fortel_ziwei_integration.py`、`mikaboshi_fengshui_integration.py`、`astro_integration.py`、`dantalion_integration.py`、`bazi1_integration.py`、`true_solar_time.py`、`qimen.py`、`ziwei.py`、`liuren.py`；目标是迁入 `fate_core.adapters` 下的兼容模块目录，保持算法行为不变，后续再按 provider/usecase 拆分。
- `delivery/src` 保留职责：FastAPI、Web、Bot、报告渲染、运行队列和对外交付；不得再作为 fate-core 领域算法模块来源。

# Entrypoint Business Flow Map
- Web GET `/web`：`main.render_web_report_page -> web_ui.render_web_report_page -> web_report_service.build_web_report_result -> CapabilityExecutor(capability_id=bazi|ziwei) -> report_generator.generate_full_report`。迁移目标：继续保留 Web 只做表单、任务和 HTML 呈现，计算统一委托 canonical calculation service。
- Web async POST `/api/v1/report/jobs/web`：`main.create_web_report_job -> _web_form_from_payload -> web_report_service.build_web_report_result`。迁移目标：与 GET `/web` 共用同一 service，保留异步队列和轮询 UI。
- API `/api/v1/bazi/simple` 与 `/api/v1/bazi/calculate`：`main._calculate_bazi_raw -> BaziCalculator.calculate`。迁移目标：改为调用 canonical calculation service 的 bazi 分支；`calculate` 仍负责鉴权、BaziResponse DTO 和记录写入。
- API `/api/v1/bazi/pure-analysis`：`main.calculate_bazi_pure_analysis -> fate_core.usecases.calculate_pure_analysis`。迁移目标：保持纯分析链路不受 Markdown/report 交付影响；只复用统一输入解析和选项校验。
- API Markdown `/api/v1/report/jobs` 与 `/api/v1/report/markdown`：`main._build_markdown_report_payload -> ziwei 用 CapabilityExecutor；bazi 用 _calculate_bazi_raw -> generate_full_report`。迁移目标：改为 canonical calculation service 按 report_system 选择 bazi/ziwei。
- Bot：`bot._calc_and_save_report -> BaziCalculator.calculate(hide=build_report_hide(report_system)) -> generate_full_report -> TXT_DIR`。迁移目标：改为 canonical calculation service；保留 Telegram 文案、补发队列和 TXT 产物路径；ziwei 不再靠八字扩展链拼装。
- 兼容策略：对外路由、命令、Markdown 文案和 Web HTML 结构不改；只收敛内部计算入口。若入口差异属于交付层格式差异，允许保留；canonical `inputTrace/fourPillars/ziweiChart/workbench` 字段必须一致。

# Assumptions and Falsification
- 短期最安全策略是先拒绝未实现业务选项，而不是一次性实现 lunar/DST/late midnight 全部语义。
- fate-core 应拥有领域计算、provider、adapter 和 reference integration；delivery 只做入口、鉴权、报告、Bot/Web/API 交付。
- 统一入口应优先收敛到已有 CapabilityExecutor 或 calculate_pure_analysis，而不是新增平行业务服务。
- 当前任务的完成定义是关闭 REVIEW-0001 的工程 BLOCK，不是提高命理预测准确率。

# Critical Ambiguities
- 未支持业务选项的短期策略需要确认：拒绝非默认值，还是本轮实现部分真实语义。
- Bot 入口统一需要确认保留哪些用户可见文本和历史命令格式。
- 迁移 delivery integration 模块时，部分旧模块的 license/source 边界需要重新核查。

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: import boundary regression
- 调试关注点: unsupported option silent drift
- 调试关注点: canonical output mismatch across Web/API/Bot
- 调试关注点: coordinate validation false positive
- 调试关注点: governance index churn
- 强制调试叶子节点: TP-01.02, TP-01.03, TP-03.03, TP-04.03, TP-06.01, TP-06.02

# Task Package Context Map
## TP-01
- Step Key: `precheck-baseline`
- 标题: PRECHECK：冻结审计基线与治理资产边界
- 类型: `package`
- 目标: 确认当前未提交治理资产、REVIEW-0001 finding、现有测试基线和执行边界，避免修复过程混入无关变更。
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `dirty-governance-inventory`
- 标题: 盘点当前治理资产 dirty diff
- 类型: `action`
- 目标: 列出当前 governance 变更、未跟踪文件和它们是否属于本任务前置资产。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: dirty diff inventory；本任务可写/禁写边界
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.02
- Step Key: `baseline-repro`
- 标题: 复现 REVIEW-0001 关键证据
- 类型: `action`
- 目标: 用 rg 和最小测试复现 F-001 到 F-005 的当前状态，建立修复前证据。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: baseline evidence block；DEBUG.md 或任务 STATUS evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.03
- Step Key: `test-baseline`
- 标题: 建立当前测试基线
- 类型: `action`
- 目标: 运行目标回归，确认开始修复前哪些测试已经通过，哪些测试需要先补失败用例。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: dirty-governance-inventory, baseline-repro
- 依赖节点 ID: TP-01.01, TP-01.02
- 输入: 无
- 输出: baseline test evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `fix-domain-boundary`
- 标题: F-001：修复 fate-core 反向依赖 delivery
- 类型: `package`
- 目标: 迁移被领域内核使用的 delivery integration 到 fate-core adapter/provider，删除 TELEGRAM_SRC_DIR/sys.path 反向依赖。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02, TP-02.03
- 依赖步骤 Key: test-baseline
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.01
- Step Key: `integration-ownership-map`
- 标题: 绘制 integration ownership map
- 类型: `action`
- 目标: 列出 bazi_calculator.py 和 ziwei_iztro.py 通过 delivery src 动态导入的模块、调用点和迁移目标。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: integration ownership map
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.02
- Step Key: `migrate-core-adapters`
- 标题: 迁移核心 adapter/provider
- 类型: `action`
- 目标: 把核心计算需要的旧 integration 移入 fate_core.adapters/providers 或 reference adapter，delivery 只保留交付入口。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: integration-ownership-map
- 依赖节点 ID: TP-02.01
- 输入: 无
- 输出: fate-core adapter/provider modules；compatibility ledger update if needed
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.03
- Step Key: `boundary-guard-test`
- 标题: 新增领域边界防回潮测试
- 类型: `action`
- 目标: 新增结构测试，禁止 fate-core 源码再次引用 delivery 路径或 TELEGRAM_SRC_DIR。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: migrate-core-adapters
- 依赖节点 ID: TP-02.02
- 输入: 无
- 输出: architecture boundary regression
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `fix-option-semantics`
- 标题: F-002/F-003：修复业务选项语义和响应回显
- 类型: `package`
- 目标: 建立 canonical options，未实现语义显式 422，useTrueSolarTime 回显与真实计算一致。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02, TP-03.03, TP-03.04
- 依赖步骤 Key: test-baseline
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.01
- Step Key: `option-contract-tests`
- 标题: 先补业务选项失败测试
- 类型: `action`
- 目标: 为 calendarType=lunar、midnightMode=late、daylightSaving 非默认、useTrueSolarTime=false 写失败用例。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: option contract regression tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.02
- Step Key: `reject-unsupported-options`
- 标题: 未实现业务选项显式拒绝
- 类型: `action`
- 目标: 对未支持的 lunar/DST/late-midnight 语义返回 422，避免保存成已应用状态。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: option-contract-tests
- 依赖节点 ID: TP-03.01
- 输入: 无
- 输出: canonical option validator；API/Web/Bot error contract
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.03
- Step Key: `fix-true-solar-echo`
- 标题: 修复 useTrueSolarTime 响应回显
- 类型: `action`
- 目标: 让 input.options.useTrueSolarTime 与 inputTrace.useTrueSolarTime 和真实计算配置一致。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: option-contract-tests
- 依赖节点 ID: TP-03.01
- 输入: 无
- 输出: response contract fix
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.04
- Step Key: `record-normalized-options`
- 标题: 记录 raw options 与 normalized options
- 类型: `action`
- 目标: 持久化只保存实际参与计算的 normalized options，同时保留 raw input 供审计。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: reject-unsupported-options, fix-true-solar-echo
- 依赖节点 ID: TP-03.02, TP-03.03
- 输入: 无
- 输出: record replay regression
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `unify-entrypoints`
- 标题: F-004：统一 Web/API/Bot 业务真相源
- 类型: `package`
- 目标: 将 Web/API/Bot 的八字/紫微业务计算收敛到同一 canonical calculation usecase，delivery 仅负责适配和交付。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02, TP-04.03
- 依赖步骤 Key: fix-domain-boundary, fix-option-semantics
- 依赖节点 ID: TP-02, TP-03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `entrypoint-flow-map`
- 标题: 绘制 Web/API/Bot 当前业务流
- 类型: `action`
- 目标: 列出 Web、API markdown、API pure-analysis、Bot report 的当前计算入口、输出字段和差异。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: entrypoint flow map
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.02
- Step Key: `canonical-calculation-service`
- 标题: 建立 canonical calculation service
- 类型: `action`
- 目标: 优先复用 CapabilityExecutor/calculate_pure_analysis，形成 Web/API/Bot 可共享的薄服务层。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: entrypoint-flow-map
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: shared delivery calculation service
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.03
- Step Key: `entrypoint-consistency-tests`
- 标题: 入口一致性回归
- 类型: `action`
- 目标: 同一输入经 Web/API/Bot 或其服务层生成的 canonical calculation 字段一致。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: canonical-calculation-service
- 依赖节点 ID: TP-04.02
- 输入: 无
- 输出: entrypoint consistency regression
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `fix-coordinate-validation`
- 标题: F-005：补坐标输入边界校验
- 类型: `package`
- 目标: 让 Web/Bot 直接 lng,lat 输入复用经纬度范围验证，无效坐标返回明确错误。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02
- 依赖步骤 Key: test-baseline
- 依赖节点 ID: TP-01.03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `location-boundary-tests`
- 标题: 补 location 坐标边界测试
- 类型: `action`
- 目标: 覆盖 999,999、181,0、0,91、-181,0、0,-91 和合法边界坐标。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: location coordinate regression tests
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.02
- Step Key: `location-range-validator`
- 标题: 实现坐标范围校验
- 类型: `action`
- 目标: 在 location.get 或共享 validator 中校验经纬度范围，并让 Web/Bot 得到清晰错误。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: location-boundary-tests
- 依赖节点 ID: TP-05.01
- 输入: 无
- 输出: coordinate validator
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `review-closeout`
- 标题: REVIEW/CLOSEOUT：回归、审查和治理收口
- 类型: `package`
- 目标: 运行完整本地门禁，更新 REVIEW-0001 修复状态，整理治理资产和提交边界。
- 父节点: `ROOT`
- 子节点: TP-06.01, TP-06.02, TP-06.03
- 依赖步骤 Key: fix-domain-boundary, fix-option-semantics, unify-entrypoints, fix-coordinate-validation
- 依赖节点 ID: TP-02, TP-03, TP-04, TP-05
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.01
- Step Key: `full-regression-gate`
- 标题: 运行本地回归门禁
- 类型: `action`
- 目标: 运行 focused regression、ruff、format、mypy、local-ci quick 和治理 strict。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: gate evidence directory；STATUS Recent Evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.02
- Step Key: `review-status-update`
- 标题: 更新 REVIEW-0001 修复状态
- 类型: `action`
- 目标: 把 F-001 到 F-005 的状态、证据命令、剩余 WARN 和 owner 写回审计记录或 follow-up review。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: full-regression-gate
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: review closeout evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-06.03
- Step Key: `ship-package`
- 标题: 提交前交付包
- 类型: `action`
- 目标: 整理 git diff、任务 closeout、提交说明和回滚路径。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: review-status-update
- 依赖节点 ID: TP-06.02
- 输入: 无
- 输出: commit plan；rollback notes；task closeout packet
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
