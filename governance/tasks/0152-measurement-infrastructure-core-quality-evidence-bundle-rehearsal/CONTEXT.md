# Repo Evidence
- git status --short --branch: ## main...origin/main，开始任务前工作树 clean。
- HEAD: 6e07615 feat: add external evidence readiness audit。
- docs/reference-materials/roadmap/测算基础设施100%实现计划.md 6.41 记录 0151 已完成 readiness audit。
- contracts/fate/evaluations/core-quality-human-review-gate.json 和 scripts/core-quality-human-review-gate.py 已存在。
- contracts/fate/evaluations/professional-quality-rubric.json 已作为 core quality 人审维度来源。

# Constraints Matrix
- 只允许分析和修改当前分支/current worktree。
- 真实外部证据仍必须标记为外部连通验证待执行。
- 模板不得包含 raw URL、secret、token、DSN、专家身份、真实用户资料、benchmark 逐题信息或报告正文。
- 任务文档必须通过 auto-tasks decompose 校验。

# Change Boundary
- contracts/fate/evaluations/*
- scripts/core-quality-human-review-bundle-template.*
- tests/regression/test_core_quality_human_review_bundle_template.py
- scripts/local-ci.sh
- docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal/*
- 相关 AGENTS.md 目录说明

# Risk Matrix
- 模板如果过于像真实 bundle，可能被误用为 accepted evidence。
- hash 说明如果缺少 no-leak 检查，人工提交材料可能污染仓库。
- 路线图如果只写计划不写阻断，会让 100% 结论被夸大。

# Assumptions and Falsification
- 当前没有真实专家评审、外部 benchmark aggregate 或 no-leak signoff 可写入仓库。
- 模板可以使用占位符和 operator commands，但不能使用虚构证据。
- 后续真实提交材料应在仓库外脱敏生成，只把合规 bundle 句柄和 hash 写入 gate 输入。

# Critical Ambiguities
- 真实专家评审、外部 benchmark 和 no-leak signoff 的执行者与时间未知；本任务只生成提交前演练资产。
- 100% 基础设施最终认证仍依赖外部 live/release/audit evidence；本任务不能解除这些阻断。

# Debug Evidence Contract
- 调试模式: Optional
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据

# Task Package Context Map
## TP-01
- Step Key: `source_alignment`
- 标题: 资料与仓库事实对齐
- 类型: `package`
- 目标: 读取 0151、core quality gate、professional rubric、local-ci 和官方基础设施资料，形成 0152 的事实边界。
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02
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
- Step Key: `repo_state_review`
- 标题: 盘点当前仓库证据链
- 类型: `action`
- 目标: 确认 HEAD、0151 readiness audit、core-quality-human-review-gate、rubric 和 local-ci 接线。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 0152 CONTEXT/STATUS 事实基线。
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.02
- Step Key: `infra_research_mapping`
- 标题: 基础设施同构资料映射
- 类型: `action`
- 目标: 把官方 infra 范式映射到 FateCat 100% 剩余证据链。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 路线图 Post-0151 同构矩阵。
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `template_contract_design`
- 标题: Core quality bundle 模板契约设计
- 类型: `package`
- 目标: 定义 template-only 输出、artifact hash 指南、rubric checklist、benchmark aggregate skeleton、no-leak checklist 和 gate expectation。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02
- 依赖步骤 Key: source_alignment
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.01
- Step Key: `contract_template`
- 标题: 新增模板契约
- 类型: `action`
- 目标: 新增 machine-readable template contract，明确 non-claim 和 forbidden leak policy。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: contracts/fate/evaluations/core-quality-human-review-bundle-template.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-02.02
- Step Key: `template_generator_design`
- 标题: 设计模板生成器输出
- 类型: `action`
- 目标: 生成 JSON/Markdown 模板，包含 operator checklist、hash commands、no-leak commands 和 gate run command。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: scripts/core-quality-human-review-bundle-template.py；scripts/core-quality-human-review-bundle-template.sh
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `implementation_and_tests`
- 标题: 实现、测试与 local-ci 接线
- 类型: `package`
- 目标: 落地模板生成器、回归测试和 quick local-ci artifact，证明模板不会解除 blocked gate。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02
- 依赖步骤 Key: template_contract_design
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.01
- Step Key: `regression_tests`
- 标题: 新增回归测试
- 类型: `action`
- 目标: 覆盖模板字段、敏感信息防护、CLI 输出和 gate 拒绝模板。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: tests/regression/test_core_quality_human_review_bundle_template.py
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-03.02
- Step Key: `local_ci_wiring`
- 标题: 接入 local-ci artifact
- 类型: `action`
- 目标: 让 quick local-ci 生成模板 JSON/Markdown 并继续运行 core quality gate blocked-as-expected。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: regression_tests
- 依赖节点 ID: TP-03.01
- 输入: 无
- 输出: scripts/local-ci.sh
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `docs_and_roadmap`
- 标题: 文档和路线图同步
- 类型: `package`
- 目标: 刷新 100% 基础设施实现计划、AGENTS 目录说明和 0152 任务文档。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02
- 依赖步骤 Key: implementation_and_tests
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `roadmap_refresh`
- 标题: 刷新 100% 路线图
- 类型: `action`
- 目标: 新增 Post-0151/0152 实现计划，列出下一批任务和不可伪造证据口径。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-04.02
- Step Key: `agents_task_docs`
- 标题: 同步 AGENTS 与任务文档
- 类型: `action`
- 目标: 更新相关 AGENTS 和 0152 TODO/STATUS/ACCEPTANCE。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal/*；contracts/fate/evaluations/AGENTS.md；scripts/AGENTS.md；tests/AGENTS.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `validation_and_delivery`
- 标题: 验证、审查与版本控制
- 类型: `package`
- 目标: 执行 targeted tests、lint、local-ci、diff check、提交推送并观察远端 CI。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02
- 依赖步骤 Key: docs_and_roadmap
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: 无
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `local_validation`
- 标题: 执行本地验证
- 类型: `action`
- 目标: 运行任务文档校验、测试、lint、format、local-ci 和 diff check。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: STATUS.md validation evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-05.02
- Step Key: `git_delivery`
- 标题: 提交推送并观察远端 Acceptance
- 类型: `action`
- 目标: 完成版本控制交付并记录当前 commit 的远端 CI 证据。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: local_validation
- 依赖节点 ID: TP-05.01
- 输入: 无
- 输出: Git commit and remote Acceptance evidence
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
