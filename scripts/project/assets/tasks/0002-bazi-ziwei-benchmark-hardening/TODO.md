# Execution Checklist
[x] TP-01.01 | P0 | 建立标杆来源登记表 | Verify: 文档列出来源、体系、可对标点、复核 URL 和版权边界。 | Gate: 不得复制商业产品文案或私有算法。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 固化当前 bazi/ziwei 能力基线 | Verify: 生成当前能力矩阵并链接到 registry/profile/tests。 | Gate: 基线必须来自仓库文件和命令输出。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 建立 P0/P1/P2 缺口矩阵 | Verify: 缺口矩阵与本任务树 TP 节点互相可追溯。 | Gate: 不得把 planned 缺口写成 production。 | Parallelizable: No
[x] TP-02.01 | P0 | 补早晚子时与真太阳时边界 golden | Verify: pytest 覆盖边界样本并进入 acceptance。 | Gate: 每个样本记录来源、时区、预期柱变化。 | Parallelizable: No
[x] TP-02.02 | P0 | 补人元司令与月令权重 | Verify: 新增字段、规则 ID 和 fixture 断言。 | Gate: 字段不得破坏现有 Markdown 默认结构。 | Parallelizable: No
[x] TP-02.03 | P0 | 补强弱评分 golden | Verify: 典型强、弱、中和、从格边界命例测试通过。 | Gate: 评分口径写入 evidence 与文档。 | Parallelizable: No
[x] TP-02.04 | P0 | 补干支关系优先级 | Verify: 干支关系 golden 和规则 ID 覆盖主要组合。 | Gate: 合化是否成化必须有依据字段。 | Parallelizable: No
[x] TP-02.05 | P0 | 补大运流年流月触发 golden | Verify: 新增动态运势 fixture 与 pytest。 | Gate: 动态触发只作为趋势依据，不输出确定未来。 | Parallelizable: No
[x] TP-03.01 | P0 | 建立格局规则 registry | Verify: 规则索引、evidence 和 golden 互相可追溯。 | Gate: 无法稳定判定的格局必须输出不确定原因。 | Parallelizable: No
[x] TP-03.02 | P0 | 拆分用神策略口径 | Verify: 用神输出包含 strategy、basis、conflicts、ruleIds。 | Gate: 不得把单一调候结论包装成全部用神结论。 | Parallelizable: No
[x] TP-03.03 | P1 | 建立十神组合解释库 | Verify: 十神解释字段和 Markdown 摘要测试通过。 | Gate: 十神解释必须引用盘面证据。 | Parallelizable: Yes
[x] TP-03.04 | P1 | 扩展八字典籍规则索引 | Verify: 规则索引包含来源、短依据、适用条件和版权边界。 | Gate: 版权未复核内容不得进入生产文案。 | Parallelizable: Yes
[x] TP-03.05 | P1 | 设计八字专题报告 | Verify: 专题 profile 与默认 Markdown 隔离测试通过。 | Gate: 健康等高风险专题必须有更强免责声明。 | Parallelizable: Yes
[x] TP-04.01 | P0 | 审计 iztro 输出契约 | Verify: 输出字段矩阵和未用字段清单。 | Gate: 只读 vendor，不魔改 iztro。 | Parallelizable: No
[x] TP-04.02 | P0 | 补星曜分类与亮度字段 | Verify: 十二宫星曜分类和亮度测试通过。 | Gate: 不得丢失 iztro 原始 palaces。 | Parallelizable: No
[x] TP-04.03 | P0 | 补宫位关系结构 | Verify: 命宫、身宫、事业、财帛、夫妻等宫位关系测试通过。 | Gate: 关系字段必须能追到宫位和地支。 | Parallelizable: No
[x] TP-04.04 | P0 | 补四化飞入与冲照会照 | Verify: 四化落宫、飞入、冲照、会照字段测试通过。 | Gate: 四化解释不得覆盖原始四化事实。 | Parallelizable: No
[x] TP-04.05 | P0 | 建立紫微命例 golden | Verify: pytest 锁定紫微 P0 字段和解释层结构。 | Gate: 命例来源必须可追溯或使用合成匿名样本。 | Parallelizable: No
[x] TP-05.01 | P1 | 建立星曜百科索引 | Verify: 星曜索引 schema 和抽样解释测试通过。 | Gate: 解释必须标注适用条件。 | Parallelizable: Yes
[x] TP-05.02 | P1 | 扩展主星组合规则 | Verify: 组合识别和 evidence rule ID 测试通过。 | Gate: 组合缺条件时输出不成立原因。 | Parallelizable: Yes
[x] TP-05.03 | P1 | 建立十二宫专题解释 | Verify: 十二宫专题快照测试通过。 | Gate: 专题解释不得输出恐吓式断语。 | Parallelizable: Yes
[x] TP-05.04 | P1 | 深化本命大限流年联动 | Verify: 联动解释包含本命宫位、大限宫位、流年四化和风险边界。 | Gate: 不得把趋势解释写成确定未来。 | Parallelizable: No
[x] TP-06.01 | P0 | 统一 Web 数据契约 | Verify: API 与 Web 测试断言同源字段。 | Gate: 前端不得重复实现命理规则。 | Parallelizable: No
[x] TP-06.02 | P1 | 实现八字工作台 | Verify: Web 测试覆盖八字工作台结构和复制 Markdown。 | Gate: 默认 Markdown 结构不被前端改写。 | Parallelizable: Yes
[x] TP-06.03 | P1 | 实现紫微工作台 | Verify: Web 测试覆盖紫微工作台结构和 standalone 输出。 | Gate: 紫微不得混入八字默认报告。 | Parallelizable: Yes
[x] TP-06.04 | P0 | 补 Web 隐私回归 | Verify: privacy fixtures gate 和 Web 测试通过。 | Gate: 真实地区只用于后端计算，不进前端示例。 | Parallelizable: Yes
[x] TP-07.01 | P0 | 更新 acceptance 门禁 | Verify: `bash scripts/acceptance.sh` 覆盖新增测试并通过。 | Gate: 导出包卫生继续通过。 | Parallelizable: No
[x] TP-07.02 | P0 | 同步 README、功能状态与路线文档 | Verify: 文档无 planned/production 口径冲突。 | Gate: 不把未来能力写成已生产。 | Parallelizable: Yes
[x] TP-07.03 | P0 | 执行自审和审计清单 | Verify: 输出审计摘要并记录剩余风险。 | Gate: 阻断项必须修复或明确标为 blocker。 | Parallelizable: No
[x] TP-07.04 | P0 | 提交推送与 closeout | Verify: git clean、远端 CI 成功、closeout 文档完整。 | Gate: 不得在 CI 未覆盖最新提交时宣称完成。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
