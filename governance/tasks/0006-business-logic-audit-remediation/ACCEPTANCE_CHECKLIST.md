# Acceptance Checklist

# Global Standards
- [x] 所有 P0 BLOCK finding 有测试先行或同步测试。
- [x] 所有代码迁移保持行为兼容，旧 facade 只允许作为明确注册的 adapter。
- [x] 任何未实现业务选项必须显式拒绝，不能保存成已应用状态。
- [x] 每个修复都要能指回 REVIEW-0001 finding id。
- [x] 最终 REVIEW-0001 可从 BLOCK 降为 PASS 或 PASS with tracked WARN。

# Task Package Checklists
## TP-01
- 标题: PRECHECK：冻结审计基线与治理资产边界
- 验收项:
  - [x] 达成 `PRECHECK：冻结审计基线与治理资产边界` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 确认当前未提交治理资产、REVIEW-0001 finding、现有测试基线和执行边界，避免修复过程混入无关变更。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 盘点当前治理资产 dirty diff
- 验收项:
  - [x] 不回滚现有治理资产；不把旧 dirty diff 误算成本任务修复。
- Verify: git status --short --branch && git diff --name-status && git ls-files --others --exclude-standard
- Gate: 无业务源码 dirty diff；治理变更清单完整记录。
- 输出物:
  - [x] dirty diff inventory
  - [x] 本任务可写/禁写边界
- 标准清单:
  - [x] Verify: git status --short --branch && git diff --name-status && git ls-files --others --exclude-standard
  - [x] Gate: 无业务源码 dirty diff；治理变更清单完整记录。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 复现 REVIEW-0001 关键证据
- 验收项:
  - [x] 后续修复能对比前后状态，不靠人工印象关闭 BLOCK。
- Verify: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true
- Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。
- 输出物:
  - [x] baseline evidence block
  - [x] DEBUG.md 或任务 STATUS evidence
- 标准清单:
  - [x] Verify: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true
  - [x] Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-01.03
- 标题: 建立当前测试基线
- 验收项:
  - [x] 没有未解释的基线失败。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- Gate: 基线测试结果记录到 STATUS；新增失败测试前能区分既有失败和本轮回归。
- 输出物:
  - [x] baseline test evidence
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
  - [x] Gate: 基线测试结果记录到 STATUS；新增失败测试前能区分既有失败和本轮回归。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-02
- 标题: F-001：修复 fate-core 反向依赖 delivery
- 验收项:
  - [x] 达成 `F-001：修复 fate-core 反向依赖 delivery` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物:
  - [x] 迁移被领域内核使用的 delivery integration 到 fate-core adapter/provider，删除 TELEGRAM_SRC_DIR/sys.path 反向依赖。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: test-baseline
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 绘制 integration ownership map
- 验收项:
  - [x] 未识别清楚前不移动文件。
- Verify: rg 'TELEGRAM_SRC_DIR|sys.path|importlib|fortel_|lunar_|bazi_' domains/fate-analysis/services/fate-core/src -n
- Gate: 每个旧导入都有 fate-core 目标模块、测试和回滚说明。
- 输出物:
  - [x] integration ownership map
- 标准清单:
  - [x] Verify: rg 'TELEGRAM_SRC_DIR|sys.path|importlib|fortel_|lunar_|bazi_' domains/fate-analysis/services/fate-core/src -n
  - [x] Gate: 每个旧导入都有 fate-core 目标模块、测试和回滚说明。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 迁移核心 adapter/provider
- 验收项:
  - [x] 领域算法不再依赖 delivery 目录形状。
- Verify: .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py
- Gate: 迁移后核心能力测试通过；旧 facade 有 owner/removal 条件。
- 输出物:
  - [x] fate-core adapter/provider modules
  - [x] compatibility ledger update if needed
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py
  - [x] Gate: 迁移后核心能力测试通过；旧 facade 有 owner/removal 条件。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 新增领域边界防回潮测试
- 验收项:
  - [x] F-001 可由机器 gate 防回潮。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_architecture_boundaries.py
- Gate: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src 返回空。
- 输出物:
  - [x] architecture boundary regression
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_architecture_boundaries.py
  - [x] Gate: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src 返回空。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: F-002/F-003：修复业务选项语义和响应回显
- 验收项:
  - [x] 达成 `F-002/F-003：修复业务选项语义和响应回显` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物:
  - [x] 建立 canonical options，未实现语义显式 422，useTrueSolarTime 回显与真实计算一致。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: test-baseline
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 先补业务选项失败测试
- 验收项:
  - [x] 失败测试先于实现或与实现同提交清晰可审。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'calendarType or midnightMode or daylightSaving or trueSolar'
- Gate: 测试能证明当前静默忽略或回显冲突。
- 输出物:
  - [x] option contract regression tests
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'calendarType or midnightMode or daylightSaving or trueSolar'
  - [x] Gate: 测试能证明当前静默忽略或回显冲突。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 未实现业务选项显式拒绝
- 验收项:
  - [x] 不再有未应用选项被持久化为已应用。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py
- Gate: 非默认未实现选项返回 422；默认路径不回归。
- 输出物:
  - [x] canonical option validator
  - [x] API/Web/Bot error contract
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py
  - [x] Gate: 非默认未实现选项返回 422；默认路径不回归。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 修复 useTrueSolarTime 响应回显
- 验收项:
  - [x] F-003 关闭。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k trueSolar
- Gate: useTrueSolarTime=false 响应中不出现硬编码 true。
- 输出物:
  - [x] response contract fix
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k trueSolar
  - [x] Gate: useTrueSolarTime=false 响应中不出现硬编码 true。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-03.04
- 标题: 记录 raw options 与 normalized options
- 验收项:
  - [x] 记录回放不会假称未实现选项已应用。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k record
- Gate: 保存记录中的 options 与计算实际使用值一致。
- 输出物:
  - [x] record replay regression
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k record
  - [x] Gate: 保存记录中的 options 与计算实际使用值一致。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: F-004：统一 Web/API/Bot 业务真相源
- 验收项:
  - [x] 达成 `F-004：统一 Web/API/Bot 业务真相源` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics
- 输出物:
  - [x] 将 Web/API/Bot 的八字/紫微业务计算收敛到同一 canonical calculation usecase，delivery 仅负责适配和交付。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 绘制 Web/API/Bot 当前业务流
- 验收项:
  - [x] 没有遗漏 Bot 路径。
- Verify: rg 'CapabilityExecutor|calculate_pure_analysis|_calculate_bazi_raw|BaziCalculator' domains/experience-delivery/services/fatecat-delivery/src -n
- Gate: 每个入口都有迁移目标和兼容策略。
- 输出物:
  - [x] entrypoint flow map
- 标准清单:
  - [x] Verify: rg 'CapabilityExecutor|calculate_pure_analysis|_calculate_bazi_raw|BaziCalculator' domains/experience-delivery/services/fatecat-delivery/src -n
  - [x] Gate: 每个入口都有迁移目标和兼容策略。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 建立 canonical calculation service
- 验收项:
  - [x] 同一输入不因入口不同走不同业务逻辑。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
- Gate: delivery 不新增领域规则；共享服务输出稳定 canonical 字段。
- 输出物:
  - [x] shared delivery calculation service
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py
  - [x] Gate: delivery 不新增领域规则；共享服务输出稳定 canonical 字段。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 入口一致性回归
- 验收项:
  - [x] F-004 关闭或降为有 owner 的兼容 WARN。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py
- Gate: Web/API/Bot canonical fields 一致；报告格式差异只允许在 delivery 层。
- 输出物:
  - [x] entrypoint consistency regression
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py
  - [x] Gate: Web/API/Bot canonical fields 一致；报告格式差异只允许在 delivery 层。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-05
- 标题: F-005：补坐标输入边界校验
- 验收项:
  - [x] 达成 `F-005：补坐标输入边界校验` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: test-baseline
- 输出物:
  - [x] 让 Web/Bot 直接 lng,lat 输入复用经纬度范围验证，无效坐标返回明确错误。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: test-baseline
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 补 location 坐标边界测试
- 验收项:
  - [x] 失败用例先建立。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py -k coordinate
- Gate: 无效坐标当前能被测试捕获。
- 输出物:
  - [x] location coordinate regression tests
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py -k coordinate
  - [x] Gate: 无效坐标当前能被测试捕获。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 实现坐标范围校验
- 验收项:
  - [x] F-005 关闭。
- Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py
- Gate: 非法坐标明确拒绝；合法边界坐标通过。
- 输出物:
  - [x] coordinate validator
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py
  - [x] Gate: 非法坐标明确拒绝；合法边界坐标通过。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: REVIEW/CLOSEOUT：回归、审查和治理收口
- 验收项:
  - [x] 达成 `REVIEW/CLOSEOUT：回归、审查和治理收口` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics, unify-entrypoints, fix-coordinate-validation
- 输出物:
  - [x] 运行完整本地门禁，更新 REVIEW-0001 修复状态，整理治理资产和提交边界。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: fix-domain-boundary, fix-option-semantics, unify-entrypoints, fix-coordinate-validation
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 运行本地回归门禁
- 验收项:
  - [x] 没有跳过关键失败。
- Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict
- Gate: 所有本地门禁通过；失败必须回到对应 finding 修复。
- 输出物:
  - [x] gate evidence directory
  - [x] STATUS Recent Evidence
- 标准清单:
  - [x] Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict
  - [x] Gate: 所有本地门禁通过；失败必须回到对应 finding 修复。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-06.02
- 标题: 更新 REVIEW-0001 修复状态
- 验收项:
  - [x] 每个 finding 都有关闭证据或剩余风险 owner。
- Verify: rg 'F-001|F-002|F-003|F-004|F-005|closed|remaining' governance/evidence/reviews -n
- Gate: REVIEW-0001 不再停留在未解释的 BLOCK。
- 输出物:
  - [x] review closeout evidence
- 标准清单:
  - [x] Verify: rg 'F-001|F-002|F-003|F-004|F-005|closed|remaining' governance/evidence/reviews -n
  - [x] Gate: REVIEW-0001 不再停留在未解释的 BLOCK。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-06.03
- 标题: 提交前交付包
- 验收项:
  - [x] 可交给 auto-github 进行 commit/push。
- Verify: git diff --check && git status --short --branch
- Gate: 无运行态、secret、无关格式化或未说明治理 churn。
- 输出物:
  - [x] commit plan
  - [x] rollback notes
  - [x] task closeout packet
- 标准清单:
  - [x] Verify: git diff --check && git status --short --branch
  - [x] Gate: 无运行态、secret、无关格式化或未说明治理 churn。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
