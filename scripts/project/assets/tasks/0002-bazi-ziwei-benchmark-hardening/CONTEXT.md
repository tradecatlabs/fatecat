# Repo Evidence
- `assets/fate/capabilities/registry.json` 显示 `bazi` 与 `ziwei` 均为 production，其中 `bazi` 是唯一 default。
- `assets/fate/capabilities/profiles/bazi.json` 与 `ziwei.json` 定义两个体系的报告 profile。
- `modules/fate_core/usecases/calculate_ziwei.py` 已存在紫微独立 usecase 与 `ziweiInterpretation`。
- `modules/telegram/src/bazi_calculator.py` 已包含综合八字计算、evidence、真太阳时、格局用神、动态运势等遗留生产链路。
- `assets/data/bazi/golden/statement_cases.json` 已存在第一批八字命例 golden。
- `assets/data/calendar/solar_terms/golden/solar_terms_1900_2030.json` 已存在节气 golden。
- 最新 `git status --short --branch` 在任务创建前显示 main 与 origin/main 同步，但已有路线图文档未提交。

# Constraints Matrix
- 胶水原则优先：优先复用 lunar-python、bazi-1、iztro、现有 vendor 和成熟开源库。
- 自研只允许做连接、编排、规则索引、evidence 映射、报告组织和 UI。
- 八字仍是唯一默认 Markdown 生产报告；紫微必须 standalone。
- 所有核心断语必须有 evidence 或规则索引，不允许只靠自然语言脑补。
- 架构或目录职责变化必须同步更新对应 AGENTS.md。

# Change Boundary
- 允许修改 `scripts/project/assets/tasks/0002-bazi-ziwei-benchmark-hardening/` 与 `scripts/project/assets/tasks/INDEX.md` 落盘任务树。
- 本轮允许保留已新增路线图文档与索引修改。
- 业务实现阶段允许修改 `modules/fate_core/`、`modules/telegram/`、`assets/fate/`、`assets/data/`、`tests/` 和相关文档。
- 禁止修改 vendor 快照来承载业务逻辑。
- 禁止引入未复核版权文本作为生产规则库。

# Risk Matrix
- 市面商业产品功能无法完全通过公开资料复核，需要把公开证据与人工复核项分开。
- 八字格局、用神、强弱有多流派冲突，必须先定义流派口径和冲突优先级。
- 紫微不同派别对星曜、四化、飞星和限运解释差异大，必须记录配置口径。
- 规则库扩张容易造成报告膨胀，必须保持结构化输出与 Markdown 输出边界。
- 命例 golden 若来源不清会污染准确性评估，必须记录来源和授权。

# Assumptions and Falsification
- 当前第一阶段以 FateCat 已接入的 lunar-python、bazi-1 和 iztro 为底座，不先替换核心库。
- 对标目标是功能结构和验证方法，不是复制商业产品文案。
- Web 工作台可以分阶段实现，先结构化数据和点击展开，再做视觉增强。
- MingLi-Bench 与外部 Drive 资料后续只作为评测/资料候选，进入生产前必须做版权和可复核性分级。

# Critical Ambiguities
- 不同标杆产品的私有功能无法完全公开验证；解决方式是只落公开可复核功能结构，把人工复核列为后续任务。
- 八字与紫微多流派差异会影响最终断语；解决方式是先把流派配置写入输出和 evidence。
- 是否做完整前端工作台取决于后续执行资源；任务树先把数据契约作为前置。

# Debug Evidence Contract
- 调试模式: Optional
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: 若后续出现计算结果与 golden 冲突，必须新增 DEBUG.md 记录数据来源、口径差异、根因和回归证据。
- 调试关注点: 若 Web/API/Bot 输出不一致，必须以能力 usecase 与 report profile 为单一真相源排查。

# Task Package Context Map
## TP-01
- Step Key: `benchmark_governance`
- 标题: 标杆证据与能力边界治理
- 类型: `Governance`
- 目标: 把八字/紫微对标范围、公开来源、不可复制边界和当前能力基线固定下来。
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `benchmark_source_registry`
- 标题: 建立标杆来源登记表
- 类型: `Audit`
- 目标: 把问真、从真版、Bazilabs、NCC、文墨天机、紫微 Palace、iztro 等公开来源登记为可复核资料。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.02
- Step Key: `current_capability_baseline`
- 标题: 固化当前 bazi/ziwei 能力基线
- 类型: `Audit`
- 目标: 输出当前字段、报告块、API/Web/Bot 入口和测试覆盖的基线快照。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.03
- Step Key: `feature_gap_matrix`
- 标题: 建立 P0/P1/P2 缺口矩阵
- 类型: `Plan`
- 目标: 把八字和紫微缺口拆成准确性、规则库、解释层、动态运势、Web 工作台、命例验证六类。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: benchmark_source_registry, current_capability_baseline
- 依赖节点 ID: TP-01.01, TP-01.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `bazi_accuracy_p0`
- 标题: 八字准确性 P0 加固
- 类型: `Build`
- 目标: 锁定八字排盘、边界、强弱、干支关系和动态运势的准确性地基。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05
- 依赖步骤 Key: benchmark_governance
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.01
- Step Key: `bazi_time_boundary_golden`
- 标题: 补早晚子时与真太阳时边界 golden
- 类型: `Test`
- 目标: 建立早晚子时、真太阳时入参、立春年界、月令切换的组合边界测试。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.02
- Step Key: `bazi_renyuan_siling`
- 标题: 补人元司令与月令权重
- 类型: `Build`
- 目标: 结构化输出人元司令、月令权重和旺相休囚死相关依据。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.03
- Step Key: `bazi_strength_score_golden`
- 标题: 补强弱评分 golden
- 类型: `Test`
- 目标: 锁定日主强弱评分的月令、通根、透干、藏干、五行分数权重。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.04
- Step Key: `bazi_ganzhi_priority`
- 标题: 补干支关系优先级
- 类型: `Build`
- 目标: 明确合化、三会、三合、冲刑害破、入库、拱合、伏吟反吟的判定和展示优先级。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.05
- Step Key: `bazi_fortune_trigger_golden`
- 标题: 补大运流年流月触发 golden
- 类型: `Test`
- 目标: 锁定岁运并临、天克地冲、伏吟反吟、流月触发等动态运势边界。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `bazi_rule_library`
- 标题: 八字规则库与解释层
- 类型: `Build`
- 目标: 把格局、用神、十神、调候、专题解释做成可追溯规则层。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05
- 依赖步骤 Key: bazi_accuracy_p0
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.01
- Step Key: `bazi_pattern_registry`
- 标题: 建立格局规则 registry
- 类型: `Build`
- 目标: 覆盖正格、变格、从格、专旺、化气的第一批规则和典型命例。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.02
- Step Key: `bazi_yongshen_strategy`
- 标题: 拆分用神策略口径
- 类型: `Build`
- 目标: 把调候、扶抑、通关、病药拆成独立依据，处理口径冲突。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.03
- Step Key: `bazi_tengod_interpretation`
- 标题: 建立十神组合解释库
- 类型: `Build`
- 目标: 为透干、藏干、十神数量、十神组合和十神成局建立结构化解释。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.04
- Step Key: `bazi_classics_rule_index`
- 标题: 扩展八字典籍规则索引
- 类型: `Research`
- 目标: 从已整理典籍资料中提炼规则 ID，不直接复制大段原文。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.05
- Step Key: `bazi_topic_reports`
- 标题: 设计八字专题报告
- 类型: `Design`
- 目标: 建立事业、财运、婚姻、健康、学业、迁移等专题结构，但保持默认报告克制。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `ziwei_chart_p0`
- 标题: 紫微完整盘面 P0 加固
- 类型: `Build`
- 目标: 吃透 iztro 输出，补齐星曜分类、宫位关系、四化飞入和紫微 golden。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05
- 依赖步骤 Key: benchmark_governance
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `ziwei_iztro_contract`
- 标题: 审计 iztro 输出契约
- 类型: `Audit`
- 目标: 确认 iztro 当前可用字段、配置插件、运限和四化能力，形成适配清单。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.02
- Step Key: `ziwei_star_taxonomy`
- 标题: 补星曜分类与亮度字段
- 类型: `Build`
- 目标: 结构化主星、辅星、杂曜、煞曜、吉曜与庙旺利陷字段。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: ziwei_iztro_contract
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.03
- Step Key: `ziwei_palace_relations`
- 标题: 补宫位关系结构
- 类型: `Build`
- 目标: 结构化对宫、夹宫、借宫、三方四正和宫位组合。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: ziwei_iztro_contract
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.04
- Step Key: `ziwei_mutagen_flow`
- 标题: 补四化飞入与冲照会照
- 类型: `Build`
- 目标: 在生年、大限、流年、流月、流日、流时四化基础上补飞入、冲照、会照解释字段。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: ziwei_iztro_contract
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.05
- Step Key: `ziwei_golden_cases`
- 标题: 建立紫微命例 golden
- 类型: `Test`
- 目标: 建立紫微命盘、命身宫、主星、四化、运限的第一批 fixture。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: ziwei_star_taxonomy, ziwei_palace_relations, ziwei_mutagen_flow
- 依赖节点 ID: TP-04.02, TP-04.03, TP-04.04
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `ziwei_interpretation_library`
- 标题: 紫微解释库与运限联动
- 类型: `Build`
- 目标: 建立星曜百科、主星组合、十二宫专题、格局识别和本命/大限/流年三层联动。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02, TP-05.03, TP-05.04
- 依赖步骤 Key: ziwei_chart_p0
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `ziwei_star_encyclopedia`
- 标题: 建立星曜百科索引
- 类型: `Build`
- 目标: 为主要星曜建立宫位、亮度、四化条件下的基础解释索引。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.02
- Step Key: `ziwei_main_star_combos`
- 标题: 扩展主星组合规则
- 类型: `Build`
- 目标: 补紫府、机月同梁、杀破狼等第一批主星组合解释。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.03
- Step Key: `ziwei_palace_topics`
- 标题: 建立十二宫专题解释
- 类型: `Build`
- 目标: 每宫输出主星、辅星、四化、三方四正、限运触发的结构化专题。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.04
- Step Key: `ziwei_fortune_linkage`
- 标题: 深化本命大限流年联动
- 类型: `Build`
- 目标: 输出本命为体、大限成形、流年触发的三层因果链。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: ziwei_star_encyclopedia, ziwei_main_star_combos, ziwei_palace_topics
- 依赖节点 ID: TP-05.01, TP-05.02, TP-05.03
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `web_workbench`
- 标题: 八字紫微 Web 专业工作台
- 类型: `Frontend`
- 目标: 把 Web 从报告复制页升级为八字/紫微结构化查看和点击展开工作台。
- 父节点: `ROOT`
- 子节点: TP-06.01, TP-06.02, TP-06.03, TP-06.04
- 依赖步骤 Key: bazi_rule_library, ziwei_interpretation_library
- 依赖节点 ID: TP-03, TP-05
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.01
- Step Key: `web_shared_data_contract`
- 标题: 统一 Web 数据契约
- 类型: `Contract`
- 目标: 定义 Web 只消费 capability/usecase 结构化结果，不自行拼命理结论。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.02
- Step Key: `web_bazi_workbench`
- 标题: 实现八字工作台
- 类型: `Frontend`
- 目标: 四柱、十神、藏干、五行、格局、用神、大运流年可点击展开。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: web_shared_data_contract
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.03
- Step Key: `web_ziwei_workbench`
- 标题: 实现紫微工作台
- 类型: `Frontend`
- 目标: 十二宫、星曜、四化、运限可点击展开解释。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: web_shared_data_contract
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.04
- Step Key: `web_privacy_regression`
- 标题: 补 Web 隐私回归
- 类型: `Test`
- 目标: 保证示例数据仍为北京/测试用户，不显示真实非北京地区样例。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: web_shared_data_contract
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-07
- Step Key: `quality_ship`
- 标题: 质量门禁、文档同步与交付
- 类型: `Ship`
- 目标: 把所有新增能力纳入测试、文档、acceptance、版本控制和远端 CI。
- 父节点: `ROOT`
- 子节点: TP-07.01, TP-07.02, TP-07.03, TP-07.04
- 依赖步骤 Key: web_workbench
- 依赖节点 ID: TP-06
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.01
- Step Key: `acceptance_gate_update`
- 标题: 更新 acceptance 门禁
- 类型: `Test`
- 目标: 确保新增八字/紫微 golden、Web 工作台和隐私回归进入发布门禁。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.02
- Step Key: `docs_sync`
- 标题: 同步 README、功能状态与路线文档
- 类型: `Docs`
- 目标: 更新当前能力、未实现能力、对标路线和使用边界。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.03
- Step Key: `self_review_audit`
- 标题: 执行自审和审计清单
- 类型: `Review`
- 目标: 检查准确性、evidence、隐私、输出边界、导出包、CI 和残留问题。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: acceptance_gate_update, docs_sync
- 依赖节点 ID: TP-07.01, TP-07.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.04
- Step Key: `git_delivery_closeout`
- 标题: 提交推送与 closeout
- 类型: `Ship`
- 目标: 提交、推送、检查 GitHub Actions，更新任务 closeout 证据。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: self_review_audit
- 依赖节点 ID: TP-07.03
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无
