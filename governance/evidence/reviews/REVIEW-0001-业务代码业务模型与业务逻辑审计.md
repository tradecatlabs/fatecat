---
id: REVIEW-0001
type: record
status: current
owner: engineering
created: 2026-06-17
last_reviewed: 2026-06-17
source: user-requested internal business code/model/logic audit
related_gates: []
---

# REVIEW-0001 业务代码业务模型与业务逻辑审计

## 背景

本记录沉淀一次针对 FateCat 项目内部业务代码、业务模型与业务逻辑的审计。

审计对象聚焦生产候选业务路径：

- `domains/fate-analysis/services/fate-core/src/fate_core/`：命理领域内核、能力执行、八字/紫微/纯分析用例。
- `domains/experience-delivery/services/fatecat-delivery/src/`：FastAPI、Web 报告、Telegram Bot、报告生成与记录持久化。
- `contracts/fate/`、`governance/`、`tests/regression/`：公开能力契约、治理约束与回归验证入口。

审计目标不是判断“能不能运行”，而是判断业务语义是否被统一模型真实承载，业务入口是否共享同一真相源，以及高风险计算路径在正确性、性能、资源成本、稳定性和可验证性上是否可交付。

## 决策或结论

**结论：原 BLOCK 已关闭，当前状态为 PASS WITH RESIDUAL RISKS。**

2026-06-17 修复任务 `governance/tasks/0006-business-logic-audit-remediation/` 已关闭原审计中的 F-001 到 F-005：

1. `fate-core` 不再反向依赖 `fatecat-delivery` 源码目录，旧 integration 已迁入 `fate_core.adapters.legacy_integrations`。
2. 未真实实现的 `calendarType=lunar`、`midnightMode=late`、`daylightSaving=on/off` 已显式返回 `422`，不再静默保存为已应用。
3. `useTrueSolarTime=false` 的响应回显已与 `inputTrace` 一致。
4. Web/API/Bot 计算编排已收敛到 `calculation_service.py`，并新增入口一致性回归。
5. `location.get()` 已拒绝越界经纬度，Web 路径复用同一错误。

剩余风险不是原 BLOCK，而是后续专业化与生产优化项：真实农历输入、DST、晚子时语义仍未实现；legacy integration 仍是迁移区；完整 benchmark/profiling 仍应在后续任务中继续推进。

## 证据

### F-001：`fate-core` 反向依赖交付层，领域边界被打穿

- 严重级别：BLOCK
- 置信度：高
- 修复状态：CLOSED，2026-06-17。
- 修复证据：
  - 新增 `domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_integrations/`，承载旧 integration glue。
  - `fate_core.support.paths` 删除 `TELEGRAM_SRC_DIR` / delivery 源码路径常量。
  - `ziwei_iztro.py` 与 `bazi_calculator.py` 改为包内显式导入，不再修改 `sys.path` 指向交付服务。
  - 新增 `tests/regression/test_architecture_boundaries.py`。
  - 验证：`rg "TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery" domains/fate-analysis/services/fate-core/src` 返回空；`tests/regression/test_architecture_boundaries.py` PASS。
- 证据：
  - `domains/fate-analysis/services/fate-core/src/fate_core/support/paths.py:25` 定义 `TELEGRAM_SERVICE_ROOT` 指向 `domains/experience-delivery/services/fatecat-delivery`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/support/paths.py:26` 定义 `TELEGRAM_SRC_DIR` 指向交付服务 `src`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:56` 从 `fate_core.support.paths` 导入 `TELEGRAM_SRC_DIR`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:64` 将 `SRC_DIR` 绑定到 `TELEGRAM_SRC_DIR`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:552`、`:580`、`:591`、`:650`、`:670`、`:678`、`:695`、`:702`、`:708`、`:715`、`:729`、`:742` 在领域计算过程中直接导入交付层旧模块。
  - `domains/fate-analysis/services/fate-core/src/fate_core/adapters/ziwei_iztro.py:10` 导入 `TELEGRAM_SRC_DIR`，`:14` 到 `:17` 修改 `sys.path` 后导入 `fortel_ziwei_integration`。
- 影响：
  - `fate-core` 不再是纯领域内核，部署、测试和算法行为依赖 delivery 目录形状。
  - delivery 层文件名、导入顺序或 `sys.path` 变化可能改变核心命理计算。
  - 违反根 `AGENTS.md` 中 `domains/experience-delivery -> domains/fate-analysis` 的依赖方向。
- 最小修复：
  - 将被核心算法使用的 integration 模块迁入 `fate_core/adapters/`、`fate_core/providers/` 或明确的 reference adapter。
  - delivery 只保留 API/Web/Bot/报告适配，不再承载底层命理算法模块。
  - 新增结构回归测试，禁止 `fate_core` 出现 `TELEGRAM_SRC_DIR`、`fatecat-delivery`、delivery `src` 动态加载。
- 验证方式：
  - `rg "TELEGRAM_SRC_DIR|fatecat-delivery|domains/experience-delivery" domains/fate-analysis/services/fate-core/src` 返回空。
  - `python -m pytest domains/fate-analysis/services/fate-core/tests tests/regression/test_capability_protocol.py tests/regression/test_bazi_ziwei_rule_depth.py`。

### F-002：公开业务选项未真实参与计算，记录却保存为已应用

- 严重级别：BLOCK
- 置信度：高
- 修复状态：CLOSED，2026-06-17。
- 修复证据：
  - `main._validate_supported_bazi_options()` 对未实现业务选项返回 `422`。
  - 持久化 `biz_data` 同时保留 `input` 原始请求与 `normalizedOptions` 实际计算口径。
  - 新增 `test_calculate_api_rejects_unsupported_business_options` 和 `test_calculate_record_keeps_raw_and_normalized_options`。
  - 验证：`tests/regression/test_api_contracts.py` PASS。
- 证据：
  - `domains/experience-delivery/services/fatecat-delivery/src/models.py:31` 到 `:36` 暴露 `useTrueSolarTime`、`daylightSaving`、`midnightMode`、`calendarType`、`reportSystem`。
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py:910` 到 `:923` 只按公历字符串解析 `birthDate` 和 `birthTime`，没有处理 `calendarType`、DST 或早晚子时。
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py:956` 到 `:970` 构造 `BaziCalculator` 时只传入 `use_true_solar_time`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:301` 到 `:310` 的构造参数没有 `calendarType`、`daylightSaving`、`midnightMode`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:316` 注释明确“原始公历输入”。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:348` 强制使用 `Solar.fromYmdHms(...)`。
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py:1074` 保存 `calendar_type=req.options.calendarType`。
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py:1082` 保存 `early_zi=1 if req.options.midnightMode == "early" else 0`。
- 影响：
  - `calendarType=lunar`、`midnightMode=late`、`daylightSaving=on/off` 可能产出与默认值相同的排盘。
  - 持久化记录会把未应用的业务选项保存为已应用，破坏审计、回放和用户信任。
  - 这是业务正确性问题，不是前端展示或性能问题。
- 最小修复：
  - 短期：对未支持的非默认选项返回 `422`，避免静默忽略。
  - 中期：在 `fate-core` 建立统一 canonical input，明确历法转换、DST、早晚子时的领域语义。
  - 持久化层只保存真实参与计算的 normalized options 和原始用户输入。
- 验证方式：
  - 添加 golden test：`calendarType=lunar` 要么 422，要么产出经人工校验的转换结果。
  - 添加边界 test：子时前后、`midnightMode=early/late` 必须有明确差异或明确拒绝。
  - 添加记录回放 test：保存的 options 必须与计算实际使用的 normalized options 一致。

### F-003：响应契约自相矛盾，`useTrueSolarTime=false` 时回显仍硬编码 true

- 严重级别：WARN
- 置信度：高
- 修复状态：CLOSED，2026-06-17。
- 修复证据：
  - `BaziCalculator` 的 `input.options.useTrueSolarTime` 改为 `self.use_true_solar_time`。
  - 新增 `test_simple_api_echoes_false_true_solar_option_consistently`。
  - 验证：`useTrueSolarTime=false` 时 `input.options.useTrueSolarTime` 与 `inputTrace.useTrueSolarTime` 均为 `false`。
- 证据：
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:826` 在结果 `input.options` 中硬编码 `{"useTrueSolarTime": True, "calendarType": "solar"}`。
  - `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py:831` 又在 `inputTrace.useTrueSolarTime` 使用 `self.use_true_solar_time`。
- 影响：
  - 同一响应里输入回显与追踪字段可能冲突。
  - 报告、前端、记录回放和审计证据可能引用不同真相。
- 最小修复：
  - `input.options.useTrueSolarTime` 使用 `self.use_true_solar_time`。
  - 未实现非 solar 时，不要在业务语义层把 `calendarType` 硬编码成用户选项；应区分 internal normalized calendar 与 raw user calendar。
- 验证方式：
  - `useTrueSolarTime=false` 的 API 响应中 `input.options.useTrueSolarTime` 和 `inputTrace.useTrueSolarTime` 均为 `false`。

### F-004：Web/API/Bot 没有完全共享同一业务真相源

- 严重级别：WARN
- 置信度：中高
- 修复状态：CLOSED，2026-06-17。
- 修复证据：
  - 新增 `domains/experience-delivery/services/fatecat-delivery/src/calculation_service.py`，统一交付层计算编排。
  - `main.py`、`web_report_service.py`、`bot.py` 均改为调用 `calculate_delivery_result()`。
  - `scripts/serve-api.sh` / `scripts/serve-bot.sh` 改为直接启动 delivery `start.py`，不再经 core CLI 启动交付服务。
  - 新增 `tests/regression/test_entrypoint_consistency.py`。
  - 验证：entrypoint consistency 2 passed；delivery API/Bot smoke PASS。
- 证据：
  - `domains/experience-delivery/services/fatecat-delivery/src/web_report_service.py:65` 到 `:87` 的 Web 报告通过 `CapabilityExecutor` 执行业务能力。
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py:1100` 到 `:1109` 的 API Markdown 路径中，紫微走 capability，八字仍走 `_calculate_bazi_raw`。
  - `domains/experience-delivery/services/fatecat-delivery/src/bot.py:927` 到 `:946` 的 Bot 报告直接调用 `BaziCalculator(...).calculate(...)`。
  - `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py:1290` 到 `:1300` 中 `reportSystem=ziwei` 会打开 `extensions`。
- 影响：
  - 同一出生信息在 Web、API、Bot 三条入口可能经过不同业务计算路径。
  - 后续修复 capability 规则不一定覆盖 Bot 和 legacy report。
  - Bot 的紫微报告可能触发旧扩展链，带来额外耗时与故障面。
- 最小修复：
  - 将 `CapabilityExecutor` 或 `calculate_pure_analysis` 定为唯一业务计算入口。
  - API/Web/Bot 只做输入适配、鉴权、报告格式化和交付。
  - `_calculate_bazi_raw` 若必须保留，应标注为 legacy/deprecated，并有字段一致性回归测试。
- 验证方式：
  - 同一输入在 Web/API/Bot 生成的 canonical calculation 字段一致。
  - Bot `reportSystem=ziwei` 不再触发八字 legacy extensions 链路。

### F-005：Web/Bot 直接坐标输入缺少范围校验

- 严重级别：WARN
- 置信度：高
- 修复状态：CLOSED，2026-06-17。
- 修复证据：
  - `location._validate_coordinates()` 校验经度 `[-180, 180]`、纬度 `[-90, 90]`。
  - 直接坐标、常用城市和离线库返回值都经过同一范围校验。
  - 新增 `tests/regression/test_location.py` 和 Web 越界坐标回归。
  - 验证：location/Web coordinate tests PASS。
- 证据：
  - `domains/experience-delivery/services/fatecat-delivery/src/location.py:175` 到 `:178` 允许 `lng,lat` 字符串并直接返回 float。
- 影响：
  - `999,999` 这类无效坐标可以绕过 API Pydantic `BirthPlace` 边界校验进入 Web/Bot 路径。
  - 真太阳时、风水、占星和地理相关计算可能产生伪结果或异常。
- 最小修复：
  - 在 `location.get` 中校验 `-180 <= longitude <= 180`、`-90 <= latitude <= 90`。
  - Web/Bot 输入层复用同一坐标验证函数。
- 验证方式：
  - `location.get("999,999")` 抛出明确错误。
  - Web/Bot 表单或会话输入无效坐标时返回可理解的校验错误。

### 治理与验证缺口

- `governance/tools/governance_context_bundle.py --task-type performance` 可生成性能任务上下文。
- `governance/tools/governance_context_bundle.py --task-type review` 当前因缺失 `processes/代码评审标准.md` 阻塞完整 review context bundle。
- 该缺口不改变本次修复后的 `PASS WITH RESIDUAL RISKS` 结论，但会影响后续审查流程的可重复性。

## 影响范围

- 领域边界：`fate-core` 与 `fatecat-delivery` 的依赖方向需要收敛。
- 公开 API：`BaziOptions` 中未实现的业务选项必须拒绝或真实实现。
- 持久化记录：记录中的 options 必须区分 raw input 和 normalized calculation input。
- Web/API/Bot：三条入口应共享同一个业务计算真相源。
- 测试：需要补业务语义 golden test、结构依赖测试、入口一致性测试、坐标边界测试。
- 性能：旧 extensions 链路应在业务入口收敛后再做 profiling 和优化。

## 后续动作

- [x] P0：移除 `fate-core` 对 `fatecat-delivery` 的反向依赖，迁移旧 integration 模块到领域 adapter/provider。
- [x] P0：对 `calendarType`、`midnightMode`、`daylightSaving` 未支持语义返回 `422`，或在 `fate-core` 实现真实领域语义。
- [x] P0：修复 `input.options.useTrueSolarTime` 硬编码 true 的响应契约错误。
- [x] P1：统一 Web/API/Bot 的业务计算入口，减少 legacy raw calculator 旁路。
- [x] P1：为无效经纬度补 Web/Bot 入口验证。
- [x] P1：新增结构测试，禁止 `fate-core` 导入 delivery 源码。
- [x] P1：新增业务 golden tests 覆盖真太阳时关闭、入口一致性和坐标边界；农历、DST、晚子时真实语义仍作为后续专业化任务。
- [ ] P2：对报告生成和 extensions 链路做 benchmark/profiling，记录 p95/p99、单模块耗时、失败率和内存峰值。
- [ ] P2：补齐 `governance/processes/代码评审标准.md`，恢复 review context bundle 的完整治理闭环。

## 效率与优化检查

### 1. 复杂度分析

- 时间复杂度：核心单次命理排盘输入规模固定，算法大体是常数级；风险主要来自串行外部模块调用，而不是 n 规模增长。
- 空间复杂度：单次结果对象固定但字段较深；extensions 打开时会构造大量中间结构。
- 输入规模扩大 10 倍/100 倍后的影响：用户请求量扩大时，瓶颈会集中在 CPU/外部库计算、报告生成和队列容量，而不是数据库查询。
- 是否存在明显退化风险：Bot 的 `reportSystem=ziwei` 旧扩展链存在明显耗时和故障面放大风险。

### 2. 主要性能风险

- Hot path：`BaziCalculator.calculate()` 的 extensions 分支。
- 重复 I/O：未发现明显 N+1 数据库路径；主要风险是外部模块串行计算和动态导入。
- 大数据量风险：当前不是大数据批处理问题。
- 并发风险：计算任务是 CPU/外部库混合型，不能通过无界并发解决。
- 成本风险：若后续接入模型解释或远程 API，必须先统一业务输入和缓存键，否则会缓存错误语义。

### 3. 数据结构与算法审查

- 当前主要问题不是 list/hash map 选择，而是 canonical business input 缺失。
- 在业务模型未统一前，不建议引入缓存；缓存会把错误语义固化。
- 地点 CSV 线性搜索当前可接受，只有地点库显著增大或成为 hot path 后才需要索引化。

### 4. I/O、数据库与外部调用审查

- 未发现记录读取路径的明显 N+1 问题。
- 报告任务队列有界，单进程天花板已在代码中体现。
- extensions 链路缺少统一超时、失败隔离和结构化耗时指标。

### 5. 内存与资源审查

- 标准八字报告默认隐藏 extensions，资源压力相对可控。
- 紫微/扩展报告可能加载多个中间结果，建议在 capability 收敛后再做内存峰值 profiling。

### 6. 并发与稳定性审查

- 当前任务属于 CPU-bound 与外部库-bound 混合型。
- 适合有限 worker、排队、超时和 backpressure，不适合无界并发。
- 需要避免重试风暴；命理计算失败应记录结构化错误并明确降级边界。

### 7. 可验证的优化方式

- benchmark：固定 20 个 birth cases，对 API/Web/Bot 三入口分别测平均值、p95、p99。
- profiling：对 `BaziCalculator.calculate()` 和 capability executor 分别采样，定位 extensions 模块耗时。
- 日志指标：记录 `capability_id`、`report_system`、`calc_ms`、`extension_ms`、`queue_wait_ms`、`error_type`。
- 内存峰值：对 ziwei/extensions 报告测 peak RSS。
- API 调用次数：若后续接入外部 API 或 LLM，记录 request count、token count、cache hit rate。

### 8. 优化建议优先级

- P0：先修业务正确性和领域边界；这是性能优化前置条件。
- P1：收敛入口和补结构测试，减少旧路径旁路。
- P2：对 extensions 链路 profiling 后再决定是否拆 worker、加缓存或做懒加载。
- P3：暂不优化地点线性搜索；当前收益小，可能引入不必要维护成本。

### 9. 权衡说明

先做缓存、并发或微优化会掩盖业务语义错误。推荐平衡方案是：先让业务模型真实、边界清楚、入口统一，再用 benchmark/profiling 决定是否优化 extensions 链路。这样牺牲一点短期速度，但换来可验证、可维护、可回滚的长期结构。
