# Execution Checklist
[x] TP-01.01 | P0 | 盘点当前治理资产 dirty diff | Verify: git status --short --branch && git diff --name-status && git ls-files --others --exclude-standard | Gate: 无业务源码 dirty diff；治理变更清单完整记录。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 复现 REVIEW-0001 关键证据 | Verify: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true | Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 建立当前测试基线 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py | Gate: 基线测试结果记录到 STATUS；新增失败测试前能区分既有失败和本轮回归。 | Parallelizable: No
[x] TP-02.01 | P0 | 绘制 integration ownership map | Verify: rg 'TELEGRAM_SRC_DIR|sys.path|importlib|fortel_|lunar_|bazi_' domains/fate-analysis/services/fate-core/src -n | Gate: 每个旧导入都有 fate-core 目标模块、测试和回滚说明。 | Parallelizable: No
[x] TP-02.02 | P0 | 迁移核心 adapter/provider | Verify: .venv/bin/python -m pytest -q domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py | Gate: 迁移后核心能力测试通过；旧 facade 有 owner/removal 条件。 | Parallelizable: No
[x] TP-02.03 | P0 | 新增领域边界防回潮测试 | Verify: .venv/bin/python -m pytest -q tests/regression/test_architecture_boundaries.py | Gate: rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src 返回空。 | Parallelizable: No
[x] TP-03.01 | P0 | 先补业务选项失败测试 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'calendarType or midnightMode or daylightSaving or trueSolar' | Gate: 测试能证明当前静默忽略或回显冲突。 | Parallelizable: No
[x] TP-03.02 | P0 | 未实现业务选项显式拒绝 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py | Gate: 非默认未实现选项返回 422；默认路径不回归。 | Parallelizable: No
[x] TP-03.03 | P0 | 修复 useTrueSolarTime 响应回显 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k trueSolar | Gate: useTrueSolarTime=false 响应中不出现硬编码 true。 | Parallelizable: Yes
[x] TP-03.04 | P1 | 记录 raw options 与 normalized options | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k record | Gate: 保存记录中的 options 与计算实际使用值一致。 | Parallelizable: No
[x] TP-04.01 | P1 | 绘制 Web/API/Bot 当前业务流 | Verify: rg 'CapabilityExecutor|calculate_pure_analysis|_calculate_bazi_raw|BaziCalculator' domains/experience-delivery/services/fatecat-delivery/src -n | Gate: 每个入口都有迁移目标和兼容策略。 | Parallelizable: Yes
[x] TP-04.02 | P1 | 建立 canonical calculation service | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py | Gate: delivery 不新增领域规则；共享服务输出稳定 canonical 字段。 | Parallelizable: No
[x] TP-04.03 | P1 | 入口一致性回归 | Verify: .venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py | Gate: Web/API/Bot canonical fields 一致；报告格式差异只允许在 delivery 层。 | Parallelizable: No
[x] TP-05.01 | P1 | 补 location 坐标边界测试 | Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py -k coordinate | Gate: 无效坐标当前能被测试捕获。 | Parallelizable: No
[x] TP-05.02 | P1 | 实现坐标范围校验 | Verify: .venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_web_html.py | Gate: 非法坐标明确拒绝；合法边界坐标通过。 | Parallelizable: No
[x] TP-06.01 | P0 | 运行本地回归门禁 | Verify: bash scripts/local-ci.sh --profile quick && .venv/bin/python governance/tools/validate_governance_package.py --project-root . --strict | Gate: 所有本地门禁通过；失败必须回到对应 finding 修复。 | Parallelizable: No
[x] TP-06.02 | P0 | 更新 REVIEW-0001 修复状态 | Verify: rg 'F-001|F-002|F-003|F-004|F-005|closed|remaining' governance/evidence/reviews -n | Gate: REVIEW-0001 不再停留在未解释的 BLOCK。 | Parallelizable: No
[x] TP-06.03 | P0 | 提交前交付包 | Verify: git diff --check && git status --short --branch | Gate: 无运行态、secret、无关格式化或未说明治理 churn。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
