# Repo Evidence
- `scripts/project/modules/telegram/src/bazi_calculator.py` 当前通过 `lunar-python` 执行四柱、节气、起运计算。
- `scripts/project/assets/data/calendar/solar_terms/raw/` 已保存 1900-2030 交节时间原始表，当前被 Git 与导出包排除。
- `scripts/project/assets/data/calendar/solar_terms/README.md` 明确 raw 表格当前只做交叉校验资料，不直接替换生产算法。
- `scripts/project/assets/fate/` 维护报告边界、profile 与未来功能登记。
- `scripts/acceptance.sh` 已覆盖 preflight、vendor health、source/privacy hygiene、pytest、ruff、mypy、delivery smoke、导出包 hygiene。

# Constraints Matrix
- 遵循胶水原则：继续复用 `lunar-python` 等成熟库，自研只做 fixture、adapter、provider、evidence 与报告编排。
- 默认综合八字报告必须和独立体系隔离。
- 业务代码不得直接依赖 raw 目录。
- 任何高风险断语必须受免责声明约束，不得替代医疗、法律、金融、心理诊断。
- 架构或目录职责变化必须同步更新对应 AGENTS.md。

# Change Boundary
- 允许修改 `scripts/project/modules/*`、`scripts/project/tests*`、`scripts/project/assets/fate/`、`scripts/project/assets/data/calendar/solar_terms/`、`scripts/project/assets/docs/`、`scripts/*.sh` 与任务文档。
- 不允许直接修改 vendor 快照以实现业务逻辑。
- 不允许把 raw 大文件加入 Git 或导出包。
- 当前任务树落地阶段只修改 `scripts/project/assets/tasks/`，业务实现另按执行波次推进。

# Risk Matrix
- 节气表字段格式、时区、精度可能不统一，需要先规范 schema 与容差。
- 报告结构快照可能暴露既有隐含耦合，需要分阶段收敛。
- evidence 契约如果过度设计会拖慢落地，必须先覆盖核心结论再扩展。
- 典籍引用层存在版权与原文引用边界，先做规则索引和短引用，不复制大段原文。

# Assumptions and Falsification
- 1900-2030 交节时间表默认以北京时间或中国常用历法时间表达，实际实现前必须验证时区。
- 综合八字默认报告继续保留袁天罡称骨为民俗附录，但不参与核心权重。
- Web、API、Bot 当前可以统一到同一 report profile，而不需要重写三端入口。

# Critical Ambiguities
- 交节时间表是否包含秒级精度、是否为北京时间、是否存在重复文件冲突，需要 TP-01 实测确认。
- 证据化字段最终是否进入公开 API 返回，需要在 TP-03 schema gate 决定默认可见性。
- 典籍引用是否允许显示原文短句，需要在 TP-08 版权复核后决定。

# Debug Evidence Contract
- 调试模式: Optional
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据
- 调试关注点: 若后续节气、起运、报告结构测试失败，必须补 DEBUG.md 记录根因、最小复现和回归证据。

# Task Package Context Map
## TP-01
- Step Key: `solar_terms_golden`
- 标题: 节气 golden 回归
- 类型: `Foundation`
- 目标: 解析 1900-2030 交节时间表，建立节气、月令、立春年界和起运边界回归。
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `solar_terms_inventory`
- 标题: 盘点交节时间 raw 表
- 类型: `Audit`
- 目标: 读取 CSV/XLS/XLSX 字段、年份覆盖、时区和精度，产出 normalized schema 设计。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.02
- Step Key: `solar_terms_fixture_builder`
- 标题: 构建节气 golden fixture
- 类型: `Build`
- 目标: 从 raw 表抽取可提交的小型标准化 fixture 或可复现生成脚本。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: solar_terms_inventory
- 依赖节点 ID: TP-01.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.03
- Step Key: `solar_terms_boundary_tests`
- 标题: 节气与月令边界测试
- 类型: `Test`
- 目标: 用 golden fixture 锁定节气时刻、月令切换、立春年界和真太阳时入参边界。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: solar_terms_fixture_builder
- 依赖节点 ID: TP-01.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-01.04
- Step Key: `yun_boundary_tests`
- 标题: 起运边界回归
- 类型: `Test`
- 目标: 建立 `yun.getStartSolar()` 样本回归，锁定起运年月日时分秒。
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: solar_terms_fixture_builder
- 依赖节点 ID: TP-01.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `report_structure_lock`
- 标题: 综合八字输出结构锁定
- 类型: `Contract`
- 目标: 固定默认 Markdown 块，确保非综合八字体系不混入默认报告。
- 父节点: `ROOT`
- 子节点: TP-02.01, TP-02.02, TP-02.03
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.01
- Step Key: `report_profile_audit`
- 标题: 审计当前 report profile
- 类型: `Audit`
- 目标: 定位 Web/API/Bot 当前使用的报告 profile 和 Markdown 拼装入口。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.02
- Step Key: `default_bazi_blocks`
- 标题: 锁定综合八字默认块
- 类型: `Build`
- 目标: 将默认块限定为综合八字核心、动态运势、辅助解释、称骨民俗附录。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: report_profile_audit
- 依赖节点 ID: TP-02.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-02.03
- Step Key: `report_snapshot_tests`
- 标题: 报告结构快照测试
- 类型: `Test`
- 目标: 新增 Markdown 结构快照和块可见性测试。
- 父节点: `TP-02`
- 子节点: 无
- 依赖步骤 Key: default_bazi_blocks
- 依赖节点 ID: TP-02.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `bazi_evidence_contract`
- 标题: 八字核心证据化
- 类型: `Contract`
- 目标: 为日主、旺衰、调候、格局、用神、干支关系等核心结论补 evidence 字段。
- 父节点: `ROOT`
- 子节点: TP-03.01, TP-03.02, TP-03.03
- 依赖步骤 Key: report_structure_lock
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.01
- Step Key: `evidence_schema`
- 标题: 定义 evidence schema
- 类型: `Design`
- 目标: 定义 source、basis、weight、visibility、risk、rule_id 等字段。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.02
- Step Key: `evidence_mappers`
- 标题: 核心结论 evidence mapper
- 类型: `Build`
- 目标: 把月令、藏干、透干、五行、合冲刑害、调候、神煞、称骨映射为证据来源。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: evidence_schema
- 依赖节点 ID: TP-03.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-03.03
- Step Key: `evidence_rendering`
- 标题: 证据渲染与可见性
- 类型: `Build`
- 目标: 确定 evidence 在 API、Markdown、Web 中的默认显示/隐藏策略。
- 父节点: `TP-03`
- 子节点: 无
- 依赖步骤 Key: evidence_mappers
- 依赖节点 ID: TP-03.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `weight_boundary_governance`
- 标题: 权重与边界治理
- 类型: `Governance`
- 目标: 固定八字核心、动态运势、辅助体系、民俗附录的权重层级。
- 父节点: `ROOT`
- 子节点: TP-04.01, TP-04.02
- 依赖步骤 Key: report_structure_lock
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.01
- Step Key: `capability_registry_boundary`
- 标题: 独立体系 capability 边界
- 类型: `Governance`
- 目标: 把紫微、黄历择日、占事、西方体系、铁板神数等声明为独立或未来 capability。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-04.02
- Step Key: `weight_policy_tests`
- 标题: 权重策略测试
- 类型: `Test`
- 目标: 为核心/辅助/民俗权重边界添加测试和文档说明。
- 父节点: `TP-04`
- 子节点: 无
- 依赖步骤 Key: capability_registry_boundary
- 依赖节点 ID: TP-04.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `input_contract_privacy`
- 标题: 输入契约与隐私治理
- 类型: `Contract`
- 目标: 加固姓名、性别、出生日期、时间、地区的必填/可选规则和隐私示例治理。
- 父节点: `ROOT`
- 子节点: TP-05.01, TP-05.02
- 依赖步骤 Key: report_structure_lock
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.01
- Step Key: `input_schema_validation`
- 标题: 输入 schema 与错误响应
- 类型: `Build`
- 目标: 明确缺字段、格式错误、地区解析失败的服务响应，不生成半残报告。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-05.02
- Step Key: `privacy_fixture_tests`
- 标题: 隐私与示例脱敏回归
- 类型: `Test`
- 目标: 统一北京/测试用户示例，禁止真实非北京地区进入前端样例和报告 fixture。
- 父节点: `TP-05`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-06
- Step Key: `channel_parity`
- 标题: Web/API/Bot 同源输出
- 类型: `Integration`
- 目标: 确保三端调用同一 report profile，Markdown 复制内容与 API 返回一致。
- 父节点: `ROOT`
- 子节点: TP-06.01, TP-06.02
- 依赖步骤 Key: report_structure_lock, input_contract_privacy
- 依赖节点 ID: TP-02, TP-05
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.01
- Step Key: `report_profile_single_source`
- 标题: 报告 profile 单一真相源
- 类型: `Build`
- 目标: 收敛 Web、API、Bot 调用链路到同一 report profile 或同一 renderer。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-06.02
- Step Key: `markdown_copy_parity`
- 标题: Markdown 复制一致性
- 类型: `Test`
- 目标: 保证 Web 复制 Markdown 与 API/Bot 产物结构一致。
- 父节点: `TP-06`
- 子节点: 无
- 依赖步骤 Key: report_profile_single_source
- 依赖节点 ID: TP-06.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-07
- Step Key: `classics_reference_layer`
- 标题: 八字典籍引用层
- 类型: `Knowledge`
- 目标: 从已整理典籍中提炼格局、调候、用神规则索引，支持结论可追溯。
- 父节点: `ROOT`
- 子节点: TP-07.01, TP-07.02, TP-07.03
- 依赖步骤 Key: bazi_evidence_contract
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.01
- Step Key: `classics_source_audit`
- 标题: 典籍来源与版权边界审计
- 类型: `Audit`
- 目标: 盘点《渊海子平》《三命通会》《子平真诠》《滴天髓》《穷通宝鉴》可用文本与来源状态。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.02
- Step Key: `rule_index_seed`
- 标题: 小型规则索引种子
- 类型: `Build`
- 目标: 先提炼格局、调候、用神的结构化规则索引种子。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: classics_source_audit
- 依赖节点 ID: TP-07.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-07.03
- Step Key: `rule_reference_integration`
- 标题: 规则引用接入 evidence
- 类型: `Integration`
- 目标: 把可用规则索引接入 evidence，不改变核心算法判断。
- 父节点: `TP-07`
- 子节点: 无
- 依赖步骤 Key: rule_index_seed
- 依赖节点 ID: TP-07.02
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-08
- Step Key: `quality_gates`
- 标题: 质量门禁加固
- 类型: `Quality`
- 目标: 把新增回归测试、隐私测试、结构测试和导出包卫生纳入 acceptance。
- 父节点: `ROOT`
- 子节点: TP-08.01, TP-08.02
- 依赖步骤 Key: solar_terms_golden, report_structure_lock, input_contract_privacy, channel_parity
- 依赖节点 ID: TP-01, TP-02, TP-05, TP-06
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-08.01
- Step Key: `pytest_gate_expansion`
- 标题: pytest 门禁扩展
- 类型: `Test`
- 目标: 把节气、起运、报告结构、隐私、同源输出测试纳入现有 pytest 目录。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-08.02
- Step Key: `acceptance_script_update`
- 标题: acceptance 脚本更新
- 类型: `CI`
- 目标: 必要时更新 acceptance/preflight，确保新增门禁在本地和 CI 运行。
- 父节点: `TP-08`
- 子节点: 无
- 依赖步骤 Key: pytest_gate_expansion
- 依赖节点 ID: TP-08.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-09
- Step Key: `service_docs`
- 标题: 服务化文档同步
- 类型: `Docs`
- 目标: 更新 README、SKILL、execution playbook 和架构文档，明确当前生产边界。
- 父节点: `ROOT`
- 子节点: TP-09.01, TP-09.02
- 依赖步骤 Key: report_structure_lock, weight_boundary_governance
- 依赖节点 ID: TP-02, TP-04
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-09.01
- Step Key: `readme_skill_update`
- 标题: README/SKILL 生产边界更新
- 类型: `Docs`
- 目标: 明确当前生产服务只支持综合八字默认报告，其他体系为独立或未来 capability。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-09.02
- Step Key: `playbook_architecture_update`
- 标题: playbook 与架构文档更新
- 类型: `Docs`
- 目标: 同步 execution playbook、AGENTS.md 和相关架构文档。
- 父节点: `TP-09`
- 子节点: 无
- 依赖步骤 Key: readme_skill_update
- 依赖节点 ID: TP-09.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

## TP-10
- Step Key: `ship_control`
- 标题: 交付控制与 closeout
- 类型: `Ship`
- 目标: 完成版本控制、推送、CI、任务 closeout 和交付证据归档。
- 父节点: `ROOT`
- 子节点: TP-10.01, TP-10.02
- 依赖步骤 Key: quality_gates, service_docs, classics_reference_layer, bazi_evidence_contract, weight_boundary_governance
- 依赖节点 ID: TP-08, TP-09, TP-07, TP-03, TP-04
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-10.01
- Step Key: `delivery_evidence`
- 标题: 生成交付证据
- 类型: `Ship`
- 目标: 捕获 git delivery evidence、验证命令结果和剩余风险。
- 父节点: `TP-10`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无

### TP-10.02
- Step Key: `task_closeout`
- 标题: 任务 closeout
- 类型: `Ship`
- 目标: 完成 TODO/STATUS，生成 Task Closeout Packet 并沉淀后续事项。
- 父节点: `TP-10`
- 子节点: 无
- 依赖步骤 Key: delivery_evidence
- 依赖节点 ID: TP-10.01
- 输入: 无
- 输出: 无
- 风险: 无
- 备注: 无
