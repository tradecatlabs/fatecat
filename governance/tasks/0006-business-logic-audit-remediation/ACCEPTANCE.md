# Task-Level Acceptance
- fate-core 源码中不再出现 TELEGRAM_SRC_DIR、fatecat-delivery、domains/experience-delivery 或 delivery src 动态加载。
- calendarType、midnightMode、daylightSaving 的非默认未实现语义不会被静默忽略；要么真实实现，要么返回 422。
- useTrueSolarTime=false 的响应回显与 inputTrace 一致，不再硬编码 true。
- Web/API/Bot 同一输入的 canonical calculation 字段一致，delivery 不新增领域算法。
- location.get("999,999") 等无效坐标明确失败，Web/Bot 输入返回可理解错误。
- 治理 strict validate 与 health report 通过，review closeout 明确哪些 BLOCK 已关闭、哪些 WARN 留有 owner。
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 18
- 当前可立即执行叶子节点: TP-01.01, TP-01.02

# Validation Plan
- 结构扫描：rg "TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery" domains/fate-analysis/services/fate-core/src 应返回空。
- API 契约测试：pytest 覆盖 unsupported options、useTrueSolarTime=false 回显、记录回放一致性。
- 入口一致性测试：同一输入经 Web/API/Bot 或其服务层得到相同 canonical calculation 字段。
- 坐标边界测试：location.get 和 Web 表单对无效经纬度返回明确错误。
- 回归门禁：ruff、format、mypy、focused regression、local-ci quick。
- 治理门禁：validate_governance_package.py --strict 与 governance_health_report.py --strict。
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01.01 | Verify: git status --short --branch && git diff --name-status && git ls-files --others --exclude-standard | Gate: 无业务源码 dirty diff；治理变更清单完整记录。
- TP-01.02 | Verify: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true | Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。
- TP-01.03 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py | Gate: 基线测试结果记录到 STATUS；新增失败测试前能区分既有失败和本轮回归。
- TP-02.01 | Verify: rg 'TELEGRAM_SRC_DIR|sys.path|importlib|fortel_|lunar_|bazi_' domains/fate-analysis/services/fate-core/src -n | Gate: 每个旧导入都有 fate-core 目标模块、测试和回滚说明。
- TP-02.02 | Verify: .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py | Gate: 迁移后核心能力测试通过；旧 facade 有 owner/removal 条件。
- TP-02.03 | Verify: .venv/bin/python -m pytest -q tests/regression/test_architecture_boundaries.py | Gate: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src 返回空。
- TP-03.01 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'calendarType or midnightMode or daylightSaving or trueSolar' | Gate: 测试能证明当前静默忽略或回显冲突。
- TP-03.02 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py | Gate: 非默认未实现选项返回 422；默认路径不回归。
- TP-03.03 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k trueSolar | Gate: useTrueSolarTime=false 响应中不出现硬编码 true。
- TP-03.04 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k record | Gate: 保存记录中的 options 与计算实际使用值一致。
- TP-04.01 | Verify: rg 'CapabilityExecutor|calculate_pure_analysis|_calculate_bazi_raw|BaziCalculator' domains/experience-delivery/services/fatecat-delivery/src -n | Gate: 每个入口都有迁移目标和兼容策略。
- TP-04.02 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py | Gate: delivery 不新增领域规则；共享服务输出稳定 canonical 字段。
- TP-04.03 | Verify: .venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py | Gate: Web/API/Bot canonical fields 一致；报告格式差异只允许在 delivery 层。
- TP-05.01 | Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py -k coordinate | Gate: 无效坐标当前能被测试捕获。
- TP-05.02 | Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py | Gate: 非法坐标明确拒绝；合法边界坐标通过。
- TP-06.01 | Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict | Gate: 所有本地门禁通过；失败必须回到对应 finding 修复。
- TP-06.02 | Verify: rg 'F-001|F-002|F-003|F-004|F-005|closed|remaining' governance/evidence/reviews -n | Gate: REVIEW-0001 不再停留在未解释的 BLOCK。
- TP-06.03 | Verify: git diff --check && git status --short --branch | Gate: 无运行态、secret、无关格式化或未说明治理 churn。

# Review Gate
- 确认 fate-core 不再反向依赖 delivery。
- 确认未实现业务选项不再静默参与记录或响应。
- 确认 API/Web/Bot 未产生新平行业务计算链。
- 确认测试覆盖正例、反例和边界例。
- 确认治理变更清单完整，不再漏报新增标准或索引变更。

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-01.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-01.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03.04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-05.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-05.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-06.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-06.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-06.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py
- bash scripts/local-ci.sh --profile quick
- .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict
- .venv/bin/python governance/tools/governance_health_report.py --project-root . --strict
- git diff --check

# Task Package Acceptance
## TP-01
- 标题: PRECHECK：冻结审计基线与治理资产边界
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: 无

### TP-01.01
- 标题: 盘点当前治理资产 dirty diff
- 验收标准:
  - 不回滚现有治理资产；不把旧 dirty diff 误算成本任务修复。
- Verify: git status --short --branch && git diff --name-status && git ls-files --others --exclude-standard
- Gate: 无业务源码 dirty diff；治理变更清单完整记录。
- 输出物: dirty diff inventory；本任务可写/禁写边界

### TP-01.02
- 标题: 复现 REVIEW-0001 关键证据
- 验收标准:
  - 后续修复能对比前后状态，不靠人工印象关闭 BLOCK。
- Verify: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true
- Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。
- 输出物: baseline evidence block；DEBUG.md 或任务 STATUS evidence

### TP-01.03
- 标题: 建立当前测试基线
- 验收标准:
  - 没有未解释的基线失败。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- Gate: 基线测试结果记录到 STATUS；新增失败测试前能区分既有失败和本轮回归。
- 输出物: baseline test evidence

## TP-02
- 标题: F-001：修复 fate-core 反向依赖 delivery
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物: 无

### TP-02.01
- 标题: 绘制 integration ownership map
- 验收标准:
  - 未识别清楚前不移动文件。
- Verify: rg 'TELEGRAM_SRC_DIR|sys.path|importlib|fortel_|lunar_|bazi_' domains/fate-analysis/services/fate-core/src -n
- Gate: 每个旧导入都有 fate-core 目标模块、测试和回滚说明。
- 输出物: integration ownership map

### TP-02.02
- 标题: 迁移核心 adapter/provider
- 验收标准:
  - 领域算法不再依赖 delivery 目录形状。
- Verify: .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py
- Gate: 迁移后核心能力测试通过；旧 facade 有 owner/removal 条件。
- 输出物: fate-core adapter/provider modules；compatibility ledger update if needed

### TP-02.03
- 标题: 新增领域边界防回潮测试
- 验收标准:
  - F-001 可由机器 gate 防回潮。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_architecture_boundaries.py
- Gate: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src 返回空。
- 输出物: architecture boundary regression

## TP-03
- 标题: F-002/F-003：修复业务选项语义和响应回显
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物: 无

### TP-03.01
- 标题: 先补业务选项失败测试
- 验收标准:
  - 失败测试先于实现或与实现同提交清晰可审。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'calendarType or midnightMode or daylightSaving or trueSolar'
- Gate: 测试能证明当前静默忽略或回显冲突。
- 输出物: option contract regression tests

### TP-03.02
- 标题: 未实现业务选项显式拒绝
- 验收标准:
  - 不再有未应用选项被持久化为已应用。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py
- Gate: 非默认未实现选项返回 422；默认路径不回归。
- 输出物: canonical option validator；API/Web/Bot error contract

### TP-03.03
- 标题: 修复 useTrueSolarTime 响应回显
- 验收标准:
  - F-003 关闭。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k trueSolar
- Gate: useTrueSolarTime=false 响应中不出现硬编码 true。
- 输出物: response contract fix

### TP-03.04
- 标题: 记录 raw options 与 normalized options
- 验收标准:
  - 记录回放不会假称未实现选项已应用。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k record
- Gate: 保存记录中的 options 与计算实际使用值一致。
- 输出物: record replay regression

## TP-04
- 标题: F-004：统一 Web/API/Bot 业务真相源
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics
- 输出物: 无

### TP-04.01
- 标题: 绘制 Web/API/Bot 当前业务流
- 验收标准:
  - 没有遗漏 Bot 路径。
- Verify: rg 'CapabilityExecutor|calculate_pure_analysis|_calculate_bazi_raw|BaziCalculator' domains/experience-delivery/services/fatecat-delivery/src -n
- Gate: 每个入口都有迁移目标和兼容策略。
- 输出物: entrypoint flow map

### TP-04.02
- 标题: 建立 canonical calculation service
- 验收标准:
  - 同一输入不因入口不同走不同业务逻辑。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- Gate: delivery 不新增领域规则；共享服务输出稳定 canonical 字段。
- 输出物: shared delivery calculation service

### TP-04.03
- 标题: 入口一致性回归
- 验收标准:
  - F-004 关闭或降为有 owner 的兼容 WARN。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py
- Gate: Web/API/Bot canonical fields 一致；报告格式差异只允许在 delivery 层。
- 输出物: entrypoint consistency regression

## TP-05
- 标题: F-005：补坐标输入边界校验
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物: 无

### TP-05.01
- 标题: 补 location 坐标边界测试
- 验收标准:
  - 失败用例先建立。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py -k coordinate
- Gate: 无效坐标当前能被测试捕获。
- 输出物: location coordinate regression tests

### TP-05.02
- 标题: 实现坐标范围校验
- 验收标准:
  - F-005 关闭。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py
- Gate: 非法坐标明确拒绝；合法边界坐标通过。
- 输出物: coordinate validator

## TP-06
- 标题: REVIEW/CLOSEOUT：回归、审查和治理收口
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics, unify-entrypoints, fix-coordinate-validation
- 输出物: 无

### TP-06.01
- 标题: 运行本地回归门禁
- 验收标准:
  - 没有跳过关键失败。
- Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict
- Gate: 所有本地门禁通过；失败必须回到对应 finding 修复。
- 输出物: gate evidence directory；STATUS Recent Evidence

### TP-06.02
- 标题: 更新 REVIEW-0001 修复状态
- 验收标准:
  - 每个 finding 都有关闭证据或剩余风险 owner。
- Verify: rg 'F-001|F-002|F-003|F-004|F-005|closed|remaining' governance/evidence/reviews -n
- Gate: REVIEW-0001 不再停留在未解释的 BLOCK。
- 输出物: review closeout evidence

### TP-06.03
- 标题: 提交前交付包
- 验收标准:
  - 可交给 auto-github 进行 commit/push。
- Verify: git diff --check && git status --short --branch
- Gate: 无运行态、secret、无关格式化或未说明治理 churn。
- 输出物: commit plan；rollback notes；task closeout packet

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
