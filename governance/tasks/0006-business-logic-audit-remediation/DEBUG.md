# Debug Record

## Bug

- 标题：REVIEW-0001 业务代码业务模型与业务逻辑审计修复计划
- 症状：审计指出 fate-core 反向依赖 delivery、业务选项被暴露但未真实执行、useTrueSolarTime 回显可能与请求冲突、Web/API/Bot 入口真相源不一致、经纬度输入缺范围校验。
- 首次发现位置 / 时间：governance/evidence/reviews/REVIEW-0001-业务代码业务模型与业务逻辑审计.md，2026-06-17。

## Environment

- 仓库 / 模块：/home/lenovo/.projects/fatecat；domains/fate-analysis、domains/experience-delivery、tests/regression、governance/evidence/reviews。
- 运行环境：WSL Ubuntu，本地 .venv，当前任务只设计修复计划，尚未修改业务源码。
- 依赖 / 版本：以当前仓库 pyproject.toml、.venv 与本地测试脚本为准。
- 配置差异：当前工作树已有未提交 governance 资产变更，本任务必须先冻结边界，避免把既有治理 churn 误算为业务修复。

## Reproduction

1. 用 `git status --short --branch`、`git diff --name-status`、`git ls-files --others --exclude-standard` 固定开始修复前的 dirty diff。
2. 用 `rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true` 复现 F-001 或证明该 finding 已被其他变更关闭。
3. 用 focused pytest 覆盖 API options、Web HTML、location 坐标与 entrypoint consistency，复现 F-002 到 F-005 的当前行为。

## Observations

- O1：任务包已生成 24 个节点、18 个叶子执行项和 11 个执行波次。
- O2：当前 ready leaves 是 TP-01.01 和 TP-01.02，说明必须先做 dirty diff 盘点和 REVIEW-0001 证据复现。
- O3：CONTEXT.md 将调试模式声明为 Required，因此后续每个 BLOCK 关闭都必须有命令、测试或 scan 证据。
- O4：`git status --short --branch`、`git diff --name-status` 和 `git ls-files --others --exclude-standard` 显示当前 dirty diff 全部位于 governance 下，没有业务源码 dirty diff。
- O5：`rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src` 命中 `support/paths.py`、`support/__init__.py`、`adapters/ziwei_iztro.py` 和 `kernel/bazi_calculator.py`。
- O6：`calendarType=lunar`、`midnightMode=late`、`daylightSaving=on` 的 `/api/v1/bazi/calculate` 请求返回 200 success，并在 record write 路径保存 `calendar_type=lunar`、`early_zi=0`、`dst=0`。
- O7：直接调用 `BaziCalculator(..., use_true_solar_time=False)` 时，结果 `input.options.useTrueSolarTime` 为 true，但 `inputTrace.useTrueSolarTime` 为 false。
- O8：`location.get("999,999")`、`location.get("181,0")`、`location.get("0,91")` 均返回坐标 tuple，没有拒绝越界输入。

## Hypotheses

### H1: 审计问题来自领域边界与入口契约漂移（ROOT HYPOTHESIS）
- Supports：REVIEW-0001 同时指向 fate-core 反向引用 delivery、入口不共享业务真相源、选项响应与计算事实不一致。
- Conflicts：如果 F-001 到 F-005 在当前代码中已经无法复现，则问题可能只是过期审计记录。
- Test：先执行 TP-01.02 的 rg 和 focused regression，确认每个 finding 的当前可复现状态。

### H2: 业务选项问题主要来自 API schema 过度承诺
- Supports：calendarType、midnightMode、daylightSaving 属于用户可见业务选项，但当前计划要求非默认未实现语义返回 422。
- Conflicts：如果已有实现真实支持这些选项，则 422 会错误降级能力。
- Test：为非默认选项添加失败测试，检查计算路径、响应回显和持久化记录是否真正使用这些值。

### H3: 入口不一致来自 delivery 层重复编排领域计算
- Supports：Web/API/Bot 同时存在报告交付、Markdown 输出和 pure-analysis 路径，容易各自拼装不同字段。
- Conflicts：如果现有入口已经全部调用同一个 canonical usecase，则只需补一致性测试。
- Test：绘制 Web/API/Bot 当前业务流，比较同一输入的 canonical calculation 字段。

## Experiments

### E1: 复现审计 finding
- Hypothesis: H1
- Change: 无生产代码改动；只运行 static rg、TestClient 请求、BaziCalculator 直接调用和 location.get 边界调用。
- Expected: 如果 H1 成立，则 F-001 到 F-005 至少各有一个当前可复现证据。
- Result: confirmed；F-001 命中 delivery 反向依赖，F-002 非默认选项返回 200 并可保存为已应用记录，F-003 `useTrueSolarTime` 回显冲突，F-004 Web/API/Bot 入口仍分别出现 CapabilityExecutor、_calculate_bazi_raw 和直接 BaziCalculator，F-005 越界坐标被接受。
- Verdict: confirmed
- Revert: 无代码变更，无需回滚。

### E2: 建立 API/Web 基线
- Hypothesis: H1
- Change: 无生产代码改动；运行 API/Web 目标基线测试。
- Expected: 当前公开 API/Web 既有回归应保持通过，后续新增失败用例才能清楚区分本轮修复影响。
- Result: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py` 通过，45 passed in 10.57s。
- Verdict: confirmed
- Revert: 无代码变更，无需回滚。

### E3: 补业务选项失败测试
- Hypothesis: H2
- Change: 添加 API 失败测试，不改业务实现。
- Expected: 当前实现会因为静默接受未实现选项和 true solar 回显冲突而失败。
- Result: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'unsupported_business_options or false_true_solar'` 失败 2 个：`calendarType=lunar` 当前返回 200，`input.options.useTrueSolarTime` 当前为 true。
- Verdict: confirmed
- Revert: 保留失败测试，下一步用实现修复。

### E4: 补坐标边界失败测试
- Hypothesis: H1
- Change: 添加直接坐标和 Web 坐标失败测试，不改业务实现。
- Expected: 当前实现会接受越界直接坐标，Web 不显示错误。
- Result: focused coordinate 测试失败 6 个：5 个 location 越界输入未抛错，Web `999,999` 未进入错误态。
- Verdict: confirmed
- Revert: 保留失败测试，下一步用实现修复。

### E5: 实现核心修复切片
- Hypothesis: H1
- Change: 迁移核心 legacy integrations 到 `fate_core.adapters.legacy_integrations`；真太阳时与 Dantalion bridge 脚本迁入 fate-core scripts；API 增加未实现业务选项 422；BaziCalculator 回显真实 `use_true_solar_time`；location 增加经纬度范围校验。
- Expected: 旧路径边界扫描为空；新增 API 和 location/Web 失败测试转绿；核心服务契约与 API/Web 回归不破坏。
- Result: `rg 'TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery' domains/fate-analysis/services/fate-core/src || true` 返回空；focused API 测试 2 passed；focused location/Web coordinate 测试 9 passed；fate-core tests 3 passed；API/Web 48 passed；compileall 通过。
- Verdict: confirmed
- Revert: 回滚本轮 adapter 迁移、API options 校验、true solar 回显和 location 校验补丁即可恢复旧行为；不涉及数据迁移。

### E6: 补边界与记录回归
- Hypothesis: H1
- Change: 新增领域边界防回潮测试；保存记录新增 `normalizedOptions`，同时保留 `input.options` 原始请求。
- Expected: 架构边界测试通过；record focused 测试证明 raw options 和 normalized options 同时存在且计算口径一致。
- Result: `tests/regression/test_architecture_boundaries.py` 1 passed；`tests/regression/test_api_contracts.py -k 'record_keeps_raw_and_normalized_options or unsupported_business_options or false_true_solar'` 3 passed；旧路径 marker rg 返回空。
- Verdict: confirmed
- Revert: 删除新增边界测试和 record normalizedOptions 字段，回滚对应断言。

### E7: 绘制入口业务流
- Hypothesis: H3
- Change: 扫描 Web/API/Bot 当前业务流并写入 `CONTEXT.md` 的 Entrypoint Business Flow Map。
- Expected: 每个入口都有当前调用链、迁移目标和兼容策略，为 canonical service 实现提供边界。
- Result: Web GET/async 当前走 `web_report_service -> CapabilityExecutor`；API simple/calculate 和 bazi Markdown 走 `_calculate_bazi_raw -> BaziCalculator`；Bot 走 `_calc_and_save_report -> BaziCalculator`；已记录迁移策略。
- Verdict: confirmed
- Revert: 删除 CONTEXT.md 新增 flow map 段落。

### E8: 收敛交付计算入口
- Hypothesis: H3
- Change: 新增 `calculation_service.py`，将 main、web_report_service、bot 接入同一交付层计算编排；serve-api/serve-bot 改为直接启动 delivery `start.py`。
- Expected: Web/API/Bot 不再各自拼装领域计算；公开 API/Web/Bot smoke 仍通过。
- Result: API/Web 回归 49 passed；architecture boundary 1 passed；delivery targeted 13 passed；`bash scripts/health.sh --mode delivery --json --pretty` PASS；`bash scripts/delivery-smoke.sh --target bot` PASS；`bash scripts/delivery-smoke.sh --target api` PASS。
- Verdict: confirmed
- Revert: 回滚 calculation_service 接入和 serve 脚本改动。

### E9: 补入口一致性回归
- Hypothesis: H3
- Change: 新增 `tests/regression/test_entrypoint_consistency.py`，验证 API、Bot 共享 service 和 Web 工作台 canonical 字段一致，并防止入口绕过 `calculation_service`。
- Expected: 同一输入的四柱、真太阳时开关等事实字段一致；入口源码不再直接导入 `BaziCalculator`。
- Result: entrypoint consistency focused 测试 2 passed；API/Web/architecture 组合回归 50 passed。
- Verdict: confirmed
- Revert: 删除新增一致性测试。

## Gate Evidence

### G1: 运行本地门禁
- Hypothesis: H1
- Change: 运行本地回归门禁与治理 strict 校验。
- Expected: 修复后的代码、测试和治理包能通过 quick release gate。
- Result: `bash scripts/local-ci.sh --profile quick` PASS；`validate_governance_package.py --strict` PASS；`validate_task_docs.py` PASS；`validate_debug_note.py` PASS。
- Verdict: confirmed
- Revert: 无代码变更；若后续门禁失败，回到对应 finding 修复。

### G2: 更新 REVIEW 状态
- Hypothesis: H1
- Change: 更新 `REVIEW-0001-业务代码业务模型与业务逻辑审计.md` 修复状态。
- Expected: REVIEW 不再停留在未解释的 BLOCK，F-001 到 F-005 都有关闭证据。
- Result: REVIEW 结论为 `PASS WITH RESIDUAL RISKS`；F-001 到 F-005 均标记 `CLOSED`；`validate_governance_package.py --strict` PASS。
- Verdict: confirmed
- Revert: 回滚 REVIEW 文档更新。

## Root Cause

- REVIEW-0001 的阻塞问题不是单点 bug，而是领域核心、交付入口和 API 选项契约长期漂移：fate-core 依赖 delivery 目录形状，Web/API/Bot 各自编排计算，部分公开选项被保存或回显成已应用状态但底层并未真实执行。
- 坐标输入缺少共享边界校验，导致 Web/Bot/API 可接受越界经纬度，错误会被推迟到下游计算或报告阶段。
- 治理状态没有随真实修复同步 closeout，导致任务包能执行但文档仍显示未完成或保留活动 blocker 字段。

## Fix

- 将领域运行所需 legacy integrations 和脚本迁入 `fate_core.adapters.legacy_integrations` 与 fate-core scripts，删除 fate-core 对 delivery 路径、`TELEGRAM_SRC_DIR` 和动态 src 加载的反向依赖。
- 新增 delivery `calculation_service.py`，让 Web/API/Bot 通过同一交付层计算编排输出 canonical 字段；入口层只做适配和报告交付。
- 对未实现的 `calendarType=lunar`、`daylightSaving` 非默认值、`midnightMode=late` 返回 422；修正 `useTrueSolarTime=false` 的响应回显；记录同时保存 raw input 与 normalized options。
- 在 `location.get` 入口统一校验经纬度范围，并补 Web 坐标错误态回归。
- 更新 REVIEW-0001、任务 TODO/STATUS/INDEX、执行波次包和 closeout 文档，使任务状态与验证证据一致。

## Regression Evidence

- `bash scripts/local-ci.sh --profile quick`：PASS。
- `bash scripts/health.sh --mode delivery --json --pretty`：PASS。
- `bash scripts/delivery-smoke.sh --target bot`：PASS。
- `bash scripts/delivery-smoke.sh --target api --startup-timeout 20`：PASS。
- `pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py tests/regression/test_architecture_boundaries.py`：50 passed。
- `pytest -q tests/regression/test_entrypoint_consistency.py`：2 passed。
- `cd domains/experience-delivery/services/fatecat-delivery && ../../../../.venv/bin/python -m pytest -q tests/test_bot_send_queue.py tests/test_service_contract.py tests/test_rate_limiter.py`：13 passed。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_runtime_contracts.py --task-package-set governance/tasks/0006-business-logic-audit-remediation/TASK_PACKAGE_SET.json --execution-wave governance/tasks/0006-business-logic-audit-remediation/TASK_EXECUTION_WAVE_PACKET.json`：PASS。
- `git diff --check`：PASS。
