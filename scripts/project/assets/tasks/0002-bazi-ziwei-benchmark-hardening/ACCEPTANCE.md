# Task-Level Acceptance
- 八字 P0 边界、格局、用神、强弱、干支关系和运势触发有可复现测试或 golden。
- 紫微 P0 命盘、星曜、宫位关系、四化、运限和解释层有可复现测试或 golden。
- Web/API/Bot 继续使用同一能力契约与报告 profile，前端不自行拼命理结论。
- 文档明确当前生产能力、未实现能力、标杆缺口和下一步执行波次。
- `bash scripts/acceptance.sh` 通过，远端 CI 覆盖最终提交。
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 30
- 当前可立即执行叶子节点: TP-01.01, TP-01.02

# Validation Plan
- 任务树阶段运行 auto-tasks 文档校验。
- 实现阶段新增或更新 pytest：八字 golden、紫微 golden、报告结构、API/Web 同源、隐私样例。
- 每批实现后运行 `cd scripts/project && .venv/bin/pytest ...` 的针对性测试。
- 出货前运行 `bash scripts/acceptance.sh`。
- 推送后检查 GitHub Actions 最新 run 成功。
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01.01 | Verify: 文档列出来源、体系、可对标点、复核 URL 和版权边界。 | Gate: 不得复制商业产品文案或私有算法。
- TP-01.02 | Verify: 生成当前能力矩阵并链接到 registry/profile/tests。 | Gate: 基线必须来自仓库文件和命令输出。
- TP-01.03 | Verify: 缺口矩阵与本任务树 TP 节点互相可追溯。 | Gate: 不得把 planned 缺口写成 production。
- TP-02.01 | Verify: pytest 覆盖边界样本并进入 acceptance。 | Gate: 每个样本记录来源、时区、预期柱变化。
- TP-02.02 | Verify: 新增字段、规则 ID 和 fixture 断言。 | Gate: 字段不得破坏现有 Markdown 默认结构。
- TP-02.03 | Verify: 典型强、弱、中和、从格边界命例测试通过。 | Gate: 评分口径写入 evidence 与文档。
- TP-02.04 | Verify: 干支关系 golden 和规则 ID 覆盖主要组合。 | Gate: 合化是否成化必须有依据字段。
- TP-02.05 | Verify: 新增动态运势 fixture 与 pytest。 | Gate: 动态触发只作为趋势依据，不输出确定未来。
- TP-03.01 | Verify: 规则索引、evidence 和 golden 互相可追溯。 | Gate: 无法稳定判定的格局必须输出不确定原因。
- TP-03.02 | Verify: 用神输出包含 strategy、basis、conflicts、ruleIds。 | Gate: 不得把单一调候结论包装成全部用神结论。
- TP-03.03 | Verify: 十神解释字段和 Markdown 摘要测试通过。 | Gate: 十神解释必须引用盘面证据。
- TP-03.04 | Verify: 规则索引包含来源、短依据、适用条件和版权边界。 | Gate: 版权未复核内容不得进入生产文案。
- TP-03.05 | Verify: 专题 profile 与默认 Markdown 隔离测试通过。 | Gate: 健康等高风险专题必须有更强免责声明。
- TP-04.01 | Verify: 输出字段矩阵和未用字段清单。 | Gate: 只读 vendor，不魔改 iztro。
- TP-04.02 | Verify: 十二宫星曜分类和亮度测试通过。 | Gate: 不得丢失 iztro 原始 palaces。
- TP-04.03 | Verify: 命宫、身宫、事业、财帛、夫妻等宫位关系测试通过。 | Gate: 关系字段必须能追到宫位和地支。
- TP-04.04 | Verify: 四化落宫、飞入、冲照、会照字段测试通过。 | Gate: 四化解释不得覆盖原始四化事实。
- TP-04.05 | Verify: pytest 锁定紫微 P0 字段和解释层结构。 | Gate: 命例来源必须可追溯或使用合成匿名样本。
- TP-05.01 | Verify: 星曜索引 schema 和抽样解释测试通过。 | Gate: 解释必须标注适用条件。
- TP-05.02 | Verify: 组合识别和 evidence rule ID 测试通过。 | Gate: 组合缺条件时输出不成立原因。
- TP-05.03 | Verify: 十二宫专题快照测试通过。 | Gate: 专题解释不得输出恐吓式断语。
- TP-05.04 | Verify: 联动解释包含本命宫位、大限宫位、流年四化和风险边界。 | Gate: 不得把趋势解释写成确定未来。
- TP-06.01 | Verify: API 与 Web 测试断言同源字段。 | Gate: 前端不得重复实现命理规则。
- TP-06.02 | Verify: Web 测试覆盖八字工作台结构和复制 Markdown。 | Gate: 默认 Markdown 结构不被前端改写。
- TP-06.03 | Verify: Web 测试覆盖紫微工作台结构和 standalone 输出。 | Gate: 紫微不得混入八字默认报告。
- TP-06.04 | Verify: privacy fixtures gate 和 Web 测试通过。 | Gate: 真实地区只用于后端计算，不进前端示例。
- TP-07.01 | Verify: `bash scripts/acceptance.sh` 覆盖新增测试并通过。 | Gate: 导出包卫生继续通过。
- TP-07.02 | Verify: 文档无 planned/production 口径冲突。 | Gate: 不把未来能力写成已生产。
- TP-07.03 | Verify: 输出审计摘要并记录剩余风险。 | Gate: 阻断项必须修复或明确标为 blocker。
- TP-07.04 | Verify: git clean、远端 CI 成功、closeout 文档完整。 | Gate: 不得在 CI 未覆盖最新提交时宣称完成。

# Review Gate
- 每个核心结论必须可追溯到底层计算、规则 ID、fixture 或公开来源。
- 八字和紫微输出必须保持体系隔离。
- Web 不允许自行拼装命理判断，只消费后端结构化结果。
- 新增资料不得违反版权和隐私边界。

# Ship Readiness
- `bash scripts/acceptance.sh` 通过。
- Git 工作树干净，当前分支推送远端。
- GitHub Actions 最新 run 成功。
- 任务 TODO 全部关闭，STATUS 无 blocker，closeout 证据完整。

# Task Package Acceptance
## TP-01
- 标题: 标杆证据与能力边界治理
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: 无

### TP-01.01
- 标题: 建立标杆来源登记表
- 验收标准:
  - 来源表进入 `assets/docs/vendor/` 或 roadmap 附录。
  - 不可验证项标记为人工复核。
- Verify: 文档列出来源、体系、可对标点、复核 URL 和版权边界。
- Gate: 不得复制商业产品文案或私有算法。
- 输出物: 无

### TP-01.02
- 标题: 固化当前 bazi/ziwei 能力基线
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 生成当前能力矩阵并链接到 registry/profile/tests。
- Gate: 基线必须来自仓库文件和命令输出。
- 输出物: 无

### TP-01.03
- 标题: 建立 P0/P1/P2 缺口矩阵
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 缺口矩阵与本任务树 TP 节点互相可追溯。
- Gate: 不得把 planned 缺口写成 production。
- 输出物: 无

## TP-02
- 标题: 八字准确性 P0 加固
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: benchmark_governance
- 输出物: 无

### TP-02.01
- 标题: 补早晚子时与真太阳时边界 golden
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 覆盖边界样本并进入 acceptance。
- Gate: 每个样本记录来源、时区、预期柱变化。
- 输出物: 无

### TP-02.02
- 标题: 补人元司令与月令权重
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 新增字段、规则 ID 和 fixture 断言。
- Gate: 字段不得破坏现有 Markdown 默认结构。
- 输出物: 无

### TP-02.03
- 标题: 补强弱评分 golden
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 典型强、弱、中和、从格边界命例测试通过。
- Gate: 评分口径写入 evidence 与文档。
- 输出物: 无

### TP-02.04
- 标题: 补干支关系优先级
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 干支关系 golden 和规则 ID 覆盖主要组合。
- Gate: 合化是否成化必须有依据字段。
- 输出物: 无

### TP-02.05
- 标题: 补大运流年流月触发 golden
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 新增动态运势 fixture 与 pytest。
- Gate: 动态触发只作为趋势依据，不输出确定未来。
- 输出物: 无

## TP-03
- 标题: 八字规则库与解释层
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: bazi_accuracy_p0
- 输出物: 无

### TP-03.01
- 标题: 建立格局规则 registry
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 规则索引、evidence 和 golden 互相可追溯。
- Gate: 无法稳定判定的格局必须输出不确定原因。
- 输出物: 无

### TP-03.02
- 标题: 拆分用神策略口径
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 用神输出包含 strategy、basis、conflicts、ruleIds。
- Gate: 不得把单一调候结论包装成全部用神结论。
- 输出物: 无

### TP-03.03
- 标题: 建立十神组合解释库
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 十神解释字段和 Markdown 摘要测试通过。
- Gate: 十神解释必须引用盘面证据。
- 输出物: 无

### TP-03.04
- 标题: 扩展八字典籍规则索引
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 规则索引包含来源、短依据、适用条件和版权边界。
- Gate: 版权未复核内容不得进入生产文案。
- 输出物: 无

### TP-03.05
- 标题: 设计八字专题报告
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 专题 profile 与默认 Markdown 隔离测试通过。
- Gate: 健康等高风险专题必须有更强免责声明。
- 输出物: 无

## TP-04
- 标题: 紫微完整盘面 P0 加固
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: benchmark_governance
- 输出物: 无

### TP-04.01
- 标题: 审计 iztro 输出契约
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 输出字段矩阵和未用字段清单。
- Gate: 只读 vendor，不魔改 iztro。
- 输出物: 无

### TP-04.02
- 标题: 补星曜分类与亮度字段
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 十二宫星曜分类和亮度测试通过。
- Gate: 不得丢失 iztro 原始 palaces。
- 输出物: 无

### TP-04.03
- 标题: 补宫位关系结构
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 命宫、身宫、事业、财帛、夫妻等宫位关系测试通过。
- Gate: 关系字段必须能追到宫位和地支。
- 输出物: 无

### TP-04.04
- 标题: 补四化飞入与冲照会照
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 四化落宫、飞入、冲照、会照字段测试通过。
- Gate: 四化解释不得覆盖原始四化事实。
- 输出物: 无

### TP-04.05
- 标题: 建立紫微命例 golden
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 锁定紫微 P0 字段和解释层结构。
- Gate: 命例来源必须可追溯或使用合成匿名样本。
- 输出物: 无

## TP-05
- 标题: 紫微解释库与运限联动
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: ziwei_chart_p0
- 输出物: 无

### TP-05.01
- 标题: 建立星曜百科索引
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 星曜索引 schema 和抽样解释测试通过。
- Gate: 解释必须标注适用条件。
- 输出物: 无

### TP-05.02
- 标题: 扩展主星组合规则
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 组合识别和 evidence rule ID 测试通过。
- Gate: 组合缺条件时输出不成立原因。
- 输出物: 无

### TP-05.03
- 标题: 建立十二宫专题解释
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 十二宫专题快照测试通过。
- Gate: 专题解释不得输出恐吓式断语。
- 输出物: 无

### TP-05.04
- 标题: 深化本命大限流年联动
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 联动解释包含本命宫位、大限宫位、流年四化和风险边界。
- Gate: 不得把趋势解释写成确定未来。
- 输出物: 无

## TP-06
- 标题: 八字紫微 Web 专业工作台
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: bazi_rule_library, ziwei_interpretation_library
- 输出物: 无

### TP-06.01
- 标题: 统一 Web 数据契约
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: API 与 Web 测试断言同源字段。
- Gate: 前端不得重复实现命理规则。
- 输出物: 无

### TP-06.02
- 标题: 实现八字工作台
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Web 测试覆盖八字工作台结构和复制 Markdown。
- Gate: 默认 Markdown 结构不被前端改写。
- 输出物: 无

### TP-06.03
- 标题: 实现紫微工作台
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Web 测试覆盖紫微工作台结构和 standalone 输出。
- Gate: 紫微不得混入八字默认报告。
- 输出物: 无

### TP-06.04
- 标题: 补 Web 隐私回归
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: privacy fixtures gate 和 Web 测试通过。
- Gate: 真实地区只用于后端计算，不进前端示例。
- 输出物: 无

## TP-07
- 标题: 质量门禁、文档同步与交付
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: web_workbench
- 输出物: 无

### TP-07.01
- 标题: 更新 acceptance 门禁
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: `bash scripts/acceptance.sh` 覆盖新增测试并通过。
- Gate: 导出包卫生继续通过。
- 输出物: 无

### TP-07.02
- 标题: 同步 README、功能状态与路线文档
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 文档无 planned/production 口径冲突。
- Gate: 不把未来能力写成已生产。
- 输出物: 无

### TP-07.03
- 标题: 执行自审和审计清单
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 输出审计摘要并记录剩余风险。
- Gate: 阻断项必须修复或明确标为 blocker。
- 输出物: 无

### TP-07.04
- 标题: 提交推送与 closeout
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: git clean、远端 CI 成功、closeout 文档完整。
- Gate: 不得在 CI 未覆盖最新提交时宣称完成。
- 输出物: 无

# Anti-Goals
- 不得修改 `assets/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
