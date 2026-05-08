# Acceptance Checklist

# Global Standards
- [x] 不得把 planned 功能描述成 production。
- [x] 不得让神煞、称骨、民俗附录影响八字核心格局和喜忌。
- [x] 不得让紫微解释覆盖或篡改 iztro 原始星盘事实。
- [x] 不得在前端示例显示真实非北京地区。
- [x] 所有外部资料来源必须可追溯。

# Task Package Checklists
## TP-01
- 标题: 标杆证据与能力边界治理
- 验收项:
  - [x] 达成 `标杆证据与能力边界治理` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 把八字/紫微对标范围、公开来源、不可复制边界和当前能力基线固定下来。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 建立标杆来源登记表
- 验收项:
  - [x] 来源表进入 `assets/docs/vendor/` 或 roadmap 附录。
  - [x] 不可验证项标记为人工复核。
- Verify: 文档列出来源、体系、可对标点、复核 URL 和版权边界。
- Gate: 不得复制商业产品文案或私有算法。
- 输出物:
  - [x] 把问真、从真版、Bazilabs、NCC、文墨天机、紫微 Palace、iztro 等公开来源登记为可复核资料。
- 标准清单:
  - [x] Verify: 文档列出来源、体系、可对标点、复核 URL 和版权边界。
  - [x] Gate: 不得复制商业产品文案或私有算法。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 固化当前 bazi/ziwei 能力基线
- 验收项:
  - [x] 达成 `固化当前 bazi/ziwei 能力基线` 的 objective，且输出物可复核
- Verify: 生成当前能力矩阵并链接到 registry/profile/tests。
- Gate: 基线必须来自仓库文件和命令输出。
- 输出物:
  - [x] 输出当前字段、报告块、API/Web/Bot 入口和测试覆盖的基线快照。
- 标准清单:
  - [x] Verify: 生成当前能力矩阵并链接到 registry/profile/tests。
  - [x] Gate: 基线必须来自仓库文件和命令输出。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.03
- 标题: 建立 P0/P1/P2 缺口矩阵
- 验收项:
  - [x] 达成 `建立 P0/P1/P2 缺口矩阵` 的 objective，且输出物可复核
- Verify: 缺口矩阵与本任务树 TP 节点互相可追溯。
- Gate: 不得把 planned 缺口写成 production。
- 输出物:
  - [x] 把八字和紫微缺口拆成准确性、规则库、解释层、动态运势、Web 工作台、命例验证六类。
- 标准清单:
  - [x] Verify: 缺口矩阵与本任务树 TP 节点互相可追溯。
  - [x] Gate: 不得把 planned 缺口写成 production。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 八字准确性 P0 加固
- 验收项:
  - [x] 达成 `八字准确性 P0 加固` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: benchmark_governance
- 输出物:
  - [x] 锁定八字排盘、边界、强弱、干支关系和动态运势的准确性地基。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: benchmark_governance
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 补早晚子时与真太阳时边界 golden
- 验收项:
  - [x] 达成 `补早晚子时与真太阳时边界 golden` 的 objective，且输出物可复核
- Verify: pytest 覆盖边界样本并进入 acceptance。
- Gate: 每个样本记录来源、时区、预期柱变化。
- 输出物:
  - [x] 建立早晚子时、真太阳时入参、立春年界、月令切换的组合边界测试。
- 标准清单:
  - [x] Verify: pytest 覆盖边界样本并进入 acceptance。
  - [x] Gate: 每个样本记录来源、时区、预期柱变化。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 补人元司令与月令权重
- 验收项:
  - [x] 达成 `补人元司令与月令权重` 的 objective，且输出物可复核
- Verify: 新增字段、规则 ID 和 fixture 断言。
- Gate: 字段不得破坏现有 Markdown 默认结构。
- 输出物:
  - [x] 结构化输出人元司令、月令权重和旺相休囚死相关依据。
- 标准清单:
  - [x] Verify: 新增字段、规则 ID 和 fixture 断言。
  - [x] Gate: 字段不得破坏现有 Markdown 默认结构。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 补强弱评分 golden
- 验收项:
  - [x] 达成 `补强弱评分 golden` 的 objective，且输出物可复核
- Verify: 典型强、弱、中和、从格边界命例测试通过。
- Gate: 评分口径写入 evidence 与文档。
- 输出物:
  - [x] 锁定日主强弱评分的月令、通根、透干、藏干、五行分数权重。
- 标准清单:
  - [x] Verify: 典型强、弱、中和、从格边界命例测试通过。
  - [x] Gate: 评分口径写入 evidence 与文档。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.04
- 标题: 补干支关系优先级
- 验收项:
  - [x] 达成 `补干支关系优先级` 的 objective，且输出物可复核
- Verify: 干支关系 golden 和规则 ID 覆盖主要组合。
- Gate: 合化是否成化必须有依据字段。
- 输出物:
  - [x] 明确合化、三会、三合、冲刑害破、入库、拱合、伏吟反吟的判定和展示优先级。
- 标准清单:
  - [x] Verify: 干支关系 golden 和规则 ID 覆盖主要组合。
  - [x] Gate: 合化是否成化必须有依据字段。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.05
- 标题: 补大运流年流月触发 golden
- 验收项:
  - [x] 达成 `补大运流年流月触发 golden` 的 objective，且输出物可复核
- Verify: 新增动态运势 fixture 与 pytest。
- Gate: 动态触发只作为趋势依据，不输出确定未来。
- 输出物:
  - [x] 锁定岁运并临、天克地冲、伏吟反吟、流月触发等动态运势边界。
- 标准清单:
  - [x] Verify: 新增动态运势 fixture 与 pytest。
  - [x] Gate: 动态触发只作为趋势依据，不输出确定未来。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 八字规则库与解释层
- 验收项:
  - [x] 达成 `八字规则库与解释层` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: bazi_accuracy_p0
- 输出物:
  - [x] 把格局、用神、十神、调候、专题解释做成可追溯规则层。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: bazi_accuracy_p0
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 建立格局规则 registry
- 验收项:
  - [x] 达成 `建立格局规则 registry` 的 objective，且输出物可复核
- Verify: 规则索引、evidence 和 golden 互相可追溯。
- Gate: 无法稳定判定的格局必须输出不确定原因。
- 输出物:
  - [x] 覆盖正格、变格、从格、专旺、化气的第一批规则和典型命例。
- 标准清单:
  - [x] Verify: 规则索引、evidence 和 golden 互相可追溯。
  - [x] Gate: 无法稳定判定的格局必须输出不确定原因。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 拆分用神策略口径
- 验收项:
  - [x] 达成 `拆分用神策略口径` 的 objective，且输出物可复核
- Verify: 用神输出包含 strategy、basis、conflicts、ruleIds。
- Gate: 不得把单一调候结论包装成全部用神结论。
- 输出物:
  - [x] 把调候、扶抑、通关、病药拆成独立依据，处理口径冲突。
- 标准清单:
  - [x] Verify: 用神输出包含 strategy、basis、conflicts、ruleIds。
  - [x] Gate: 不得把单一调候结论包装成全部用神结论。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 建立十神组合解释库
- 验收项:
  - [x] 达成 `建立十神组合解释库` 的 objective，且输出物可复核
- Verify: 十神解释字段和 Markdown 摘要测试通过。
- Gate: 十神解释必须引用盘面证据。
- 输出物:
  - [x] 为透干、藏干、十神数量、十神组合和十神成局建立结构化解释。
- 标准清单:
  - [x] Verify: 十神解释字段和 Markdown 摘要测试通过。
  - [x] Gate: 十神解释必须引用盘面证据。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.04
- 标题: 扩展八字典籍规则索引
- 验收项:
  - [x] 达成 `扩展八字典籍规则索引` 的 objective，且输出物可复核
- Verify: 规则索引包含来源、短依据、适用条件和版权边界。
- Gate: 版权未复核内容不得进入生产文案。
- 输出物:
  - [x] 从已整理典籍资料中提炼规则 ID，不直接复制大段原文。
- 标准清单:
  - [x] Verify: 规则索引包含来源、短依据、适用条件和版权边界。
  - [x] Gate: 版权未复核内容不得进入生产文案。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.05
- 标题: 设计八字专题报告
- 验收项:
  - [x] 达成 `设计八字专题报告` 的 objective，且输出物可复核
- Verify: 专题 profile 与默认 Markdown 隔离测试通过。
- Gate: 健康等高风险专题必须有更强免责声明。
- 输出物:
  - [x] 建立事业、财运、婚姻、健康、学业、迁移等专题结构，但保持默认报告克制。
- 标准清单:
  - [x] Verify: 专题 profile 与默认 Markdown 隔离测试通过。
  - [x] Gate: 健康等高风险专题必须有更强免责声明。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 紫微完整盘面 P0 加固
- 验收项:
  - [x] 达成 `紫微完整盘面 P0 加固` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: benchmark_governance
- 输出物:
  - [x] 吃透 iztro 输出，补齐星曜分类、宫位关系、四化飞入和紫微 golden。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: benchmark_governance
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 审计 iztro 输出契约
- 验收项:
  - [x] 达成 `审计 iztro 输出契约` 的 objective，且输出物可复核
- Verify: 输出字段矩阵和未用字段清单。
- Gate: 只读 vendor，不魔改 iztro。
- 输出物:
  - [x] 确认 iztro 当前可用字段、配置插件、运限和四化能力，形成适配清单。
- 标准清单:
  - [x] Verify: 输出字段矩阵和未用字段清单。
  - [x] Gate: 只读 vendor，不魔改 iztro。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 补星曜分类与亮度字段
- 验收项:
  - [x] 达成 `补星曜分类与亮度字段` 的 objective，且输出物可复核
- Verify: 十二宫星曜分类和亮度测试通过。
- Gate: 不得丢失 iztro 原始 palaces。
- 输出物:
  - [x] 结构化主星、辅星、杂曜、煞曜、吉曜与庙旺利陷字段。
- 标准清单:
  - [x] Verify: 十二宫星曜分类和亮度测试通过。
  - [x] Gate: 不得丢失 iztro 原始 palaces。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.03
- 标题: 补宫位关系结构
- 验收项:
  - [x] 达成 `补宫位关系结构` 的 objective，且输出物可复核
- Verify: 命宫、身宫、事业、财帛、夫妻等宫位关系测试通过。
- Gate: 关系字段必须能追到宫位和地支。
- 输出物:
  - [x] 结构化对宫、夹宫、借宫、三方四正和宫位组合。
- 标准清单:
  - [x] Verify: 命宫、身宫、事业、财帛、夫妻等宫位关系测试通过。
  - [x] Gate: 关系字段必须能追到宫位和地支。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.04
- 标题: 补四化飞入与冲照会照
- 验收项:
  - [x] 达成 `补四化飞入与冲照会照` 的 objective，且输出物可复核
- Verify: 四化落宫、飞入、冲照、会照字段测试通过。
- Gate: 四化解释不得覆盖原始四化事实。
- 输出物:
  - [x] 在生年、大限、流年、流月、流日、流时四化基础上补飞入、冲照、会照解释字段。
- 标准清单:
  - [x] Verify: 四化落宫、飞入、冲照、会照字段测试通过。
  - [x] Gate: 四化解释不得覆盖原始四化事实。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.05
- 标题: 建立紫微命例 golden
- 验收项:
  - [x] 达成 `建立紫微命例 golden` 的 objective，且输出物可复核
- Verify: pytest 锁定紫微 P0 字段和解释层结构。
- Gate: 命例来源必须可追溯或使用合成匿名样本。
- 输出物:
  - [x] 建立紫微命盘、命身宫、主星、四化、运限的第一批 fixture。
- 标准清单:
  - [x] Verify: pytest 锁定紫微 P0 字段和解释层结构。
  - [x] Gate: 命例来源必须可追溯或使用合成匿名样本。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-05
- 标题: 紫微解释库与运限联动
- 验收项:
  - [x] 达成 `紫微解释库与运限联动` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: ziwei_chart_p0
- 输出物:
  - [x] 建立星曜百科、主星组合、十二宫专题、格局识别和本命/大限/流年三层联动。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: ziwei_chart_p0
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 建立星曜百科索引
- 验收项:
  - [x] 达成 `建立星曜百科索引` 的 objective，且输出物可复核
- Verify: 星曜索引 schema 和抽样解释测试通过。
- Gate: 解释必须标注适用条件。
- 输出物:
  - [x] 为主要星曜建立宫位、亮度、四化条件下的基础解释索引。
- 标准清单:
  - [x] Verify: 星曜索引 schema 和抽样解释测试通过。
  - [x] Gate: 解释必须标注适用条件。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 扩展主星组合规则
- 验收项:
  - [x] 达成 `扩展主星组合规则` 的 objective，且输出物可复核
- Verify: 组合识别和 evidence rule ID 测试通过。
- Gate: 组合缺条件时输出不成立原因。
- 输出物:
  - [x] 补紫府、机月同梁、杀破狼等第一批主星组合解释。
- 标准清单:
  - [x] Verify: 组合识别和 evidence rule ID 测试通过。
  - [x] Gate: 组合缺条件时输出不成立原因。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.03
- 标题: 建立十二宫专题解释
- 验收项:
  - [x] 达成 `建立十二宫专题解释` 的 objective，且输出物可复核
- Verify: 十二宫专题快照测试通过。
- Gate: 专题解释不得输出恐吓式断语。
- 输出物:
  - [x] 每宫输出主星、辅星、四化、三方四正、限运触发的结构化专题。
- 标准清单:
  - [x] Verify: 十二宫专题快照测试通过。
  - [x] Gate: 专题解释不得输出恐吓式断语。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.04
- 标题: 深化本命大限流年联动
- 验收项:
  - [x] 达成 `深化本命大限流年联动` 的 objective，且输出物可复核
- Verify: 联动解释包含本命宫位、大限宫位、流年四化和风险边界。
- Gate: 不得把趋势解释写成确定未来。
- 输出物:
  - [x] 输出本命为体、大限成形、流年触发的三层因果链。
- 标准清单:
  - [x] Verify: 联动解释包含本命宫位、大限宫位、流年四化和风险边界。
  - [x] Gate: 不得把趋势解释写成确定未来。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 八字紫微 Web 专业工作台
- 验收项:
  - [x] 达成 `八字紫微 Web 专业工作台` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: bazi_rule_library, ziwei_interpretation_library
- 输出物:
  - [x] 把 Web 从报告复制页升级为八字/紫微结构化查看和点击展开工作台。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: bazi_rule_library, ziwei_interpretation_library
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 统一 Web 数据契约
- 验收项:
  - [x] 达成 `统一 Web 数据契约` 的 objective，且输出物可复核
- Verify: API 与 Web 测试断言同源字段。
- Gate: 前端不得重复实现命理规则。
- 输出物:
  - [x] 定义 Web 只消费 capability/usecase 结构化结果，不自行拼命理结论。
- 标准清单:
  - [x] Verify: API 与 Web 测试断言同源字段。
  - [x] Gate: 前端不得重复实现命理规则。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: 实现八字工作台
- 验收项:
  - [x] 达成 `实现八字工作台` 的 objective，且输出物可复核
- Verify: Web 测试覆盖八字工作台结构和复制 Markdown。
- Gate: 默认 Markdown 结构不被前端改写。
- 输出物:
  - [x] 四柱、十神、藏干、五行、格局、用神、大运流年可点击展开。
- 标准清单:
  - [x] Verify: Web 测试覆盖八字工作台结构和复制 Markdown。
  - [x] Gate: 默认 Markdown 结构不被前端改写。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.03
- 标题: 实现紫微工作台
- 验收项:
  - [x] 达成 `实现紫微工作台` 的 objective，且输出物可复核
- Verify: Web 测试覆盖紫微工作台结构和 standalone 输出。
- Gate: 紫微不得混入八字默认报告。
- 输出物:
  - [x] 十二宫、星曜、四化、运限可点击展开解释。
- 标准清单:
  - [x] Verify: Web 测试覆盖紫微工作台结构和 standalone 输出。
  - [x] Gate: 紫微不得混入八字默认报告。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-06.04
- 标题: 补 Web 隐私回归
- 验收项:
  - [x] 达成 `补 Web 隐私回归` 的 objective，且输出物可复核
- Verify: privacy fixtures gate 和 Web 测试通过。
- Gate: 真实地区只用于后端计算，不进前端示例。
- 输出物:
  - [x] 保证示例数据仍为北京/测试用户，不显示真实非北京地区样例。
- 标准清单:
  - [x] Verify: privacy fixtures gate 和 Web 测试通过。
  - [x] Gate: 真实地区只用于后端计算，不进前端示例。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-07
- 标题: 质量门禁、文档同步与交付
- 验收项:
  - [x] 达成 `质量门禁、文档同步与交付` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: web_workbench
- 输出物:
  - [x] 把所有新增能力纳入测试、文档、acceptance、版本控制和远端 CI。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: web_workbench
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: 更新 acceptance 门禁
- 验收项:
  - [x] 达成 `更新 acceptance 门禁` 的 objective，且输出物可复核
- Verify: `bash scripts/acceptance.sh` 覆盖新增测试并通过。
- Gate: 导出包卫生继续通过。
- 输出物:
  - [x] 确保新增八字/紫微 golden、Web 工作台和隐私回归进入发布门禁。
- 标准清单:
  - [x] Verify: `bash scripts/acceptance.sh` 覆盖新增测试并通过。
  - [x] Gate: 导出包卫生继续通过。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-07.02
- 标题: 同步 README、功能状态与路线文档
- 验收项:
  - [x] 达成 `同步 README、功能状态与路线文档` 的 objective，且输出物可复核
- Verify: 文档无 planned/production 口径冲突。
- Gate: 不把未来能力写成已生产。
- 输出物:
  - [x] 更新当前能力、未实现能力、对标路线和使用边界。
- 标准清单:
  - [x] Verify: 文档无 planned/production 口径冲突。
  - [x] Gate: 不把未来能力写成已生产。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: 执行自审和审计清单
- 验收项:
  - [x] 达成 `执行自审和审计清单` 的 objective，且输出物可复核
- Verify: 输出审计摘要并记录剩余风险。
- Gate: 阻断项必须修复或明确标为 blocker。
- 输出物:
  - [x] 检查准确性、evidence、隐私、输出边界、导出包、CI 和残留问题。
- 标准清单:
  - [x] Verify: 输出审计摘要并记录剩余风险。
  - [x] Gate: 阻断项必须修复或明确标为 blocker。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-07.04
- 标题: 提交推送与 closeout
- 验收项:
  - [x] 达成 `提交推送与 closeout` 的 objective，且输出物可复核
- Verify: git clean、远端 CI 成功、closeout 文档完整。
- Gate: 不得在 CI 未覆盖最新提交时宣称完成。
- 输出物:
  - [x] 提交、推送、检查 GitHub Actions，更新任务 closeout 证据。
- 标准清单:
  - [x] Verify: git clean、远端 CI 成功、closeout 文档完整。
  - [x] Gate: 不得在 CI 未覆盖最新提交时宣称完成。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
