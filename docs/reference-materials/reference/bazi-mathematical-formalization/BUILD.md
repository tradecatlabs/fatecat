# 八字数学形式化构建指南

> 状态：工作草案 v0.1
> 目标：规定如何把一个传统规则或历法事实构建成 FateCat 可执行、可验证、可维护的能力切片。

## 1. 构建原则

每个切片必须遵循：

```text
SOURCE
  -> SPEC
  -> PROFILE
  -> CONTRACT
  -> IMPLEMENTATION
  -> FIXTURES
  -> PROPERTY/GOLDEN GATES
  -> EVIDENCE
  -> DELIVERY
```

禁止从报告文案、UI 字段或单个样例反向生成规则。

“构建完成”不是指写出公式，而是指定义、机器契约、实现、正反例、边界例、证据和维护责任同时闭环。

## 2. 产物分层

| 产物 | 路径 | 职责 |
| --- | --- | --- |
| 人类形式规范 | 本目录 | 解释对象、术语、性质和边界 |
| 机器契约 | `contracts/fate/` | schema、Profile、枚举、规则和版本真相源 |
| 领域实现 | `domains/fate-analysis/services/fate-core/` | 执行已登记算法和规则 |
| Golden 数据 | `domains/fate-analysis/data-products/bazi/golden/` | 匿名正例、反例和边界例 |
| 服务级测试 | `domains/fate-analysis/services/fate-core/tests/` | 单元、性质和算法测试 |
| 仓库级门禁 | `tests/regression/` | 契约、跨端、导出和防回潮测试 |
| 本地 CI | `scripts/local-ci.sh` | 统一调度，不复制业务规则 |
| 交付层 | `domains/experience-delivery/` | 只呈现 capability 输出 |

在机器契约落地前，文档必须明确标记 `draft`；不得让生产代码解析 Markdown 作为规则来源。

## 3. 构建波次

### B0：范围、术语和来源

输入：

- 待形式化主题。
- 当前实现位置。
- 现有规则 ID、测试和来源。

动作：

1. 定义主题边界和非目标。
2. 列出所有同义词和歧义词。
3. 登记来源、版本、适用范围和许可证状态。
4. 区分基础事实、传统规则、解释策略和报告文案。
5. 建立当前实现与目标模型的差异清单。

输出：

- 术语表。
- source ledger。
- gap ledger。
- 不支持声明。

门禁：来源不明、定义冲突或无法区分事实与文案时停止。

### B1：输入和 Profile

输入：B0 产物。

动作：

1. 定义原始输入和 canonical 输入。
2. 明确地点、坐标、时区、UTC、DST fold 和时间误差。
3. 枚举会改变结果的所有 Profile 选项。
4. 定义无效、无定义和多候选状态。
5. 固定 provider 和依赖版本。

输出：

- 输入 schema 增量。
- Profile 增量。
- 输入规范化规则。
- 歧义案例矩阵。

门禁：任何隐式默认值都必须删除或变成显式 Profile。

### B2：历法和四柱

动作顺序：

1. 六十甲子有限代数。
2. 年柱映射及年界。
3. 月柱映射及节气月界。
4. 日柱映射及参考纪元。
5. 时柱映射及早晚子时。
6. 真太阳时和历史时区对边界的影响。
7. 起运只在四柱本体稳定后另建模型。

每个映射必须给出：

- 定义域和值域。
- Profile 参数。
- 无定义条件。
- 不变量。
- 边界前、边界点、边界后样本。
- 与 production provider 的对照结果。
- 与 oracle 不一致时的归因。

门禁：四柱基础值不稳定时，不进入强弱、格局或用神构建。

### B3：有限派生结构

推荐顺序：

1. 干支阴阳。
2. 干支五行。
3. 十神。
4. 藏干。
5. 地支本气、中气、余气 Profile。
6. 十二长生。
7. 空亡。
8. 干支静态关系。
9. 纳音和神煞等辅助层。

有限映射优先使用枚举表和穷举性质测试。任何权重都必须与基础映射分离，并进入版本化 Profile。

门禁：

- 映射必须闭合。
- 不得出现未登记输出值。
- 同一概念不得维护两套表。
- 辅助层不得修改核心四柱事实。

### B4：规则语义

推荐顺序：

1. 月令与日主结构。
2. 常规强弱证据。
3. 常规格局候选。
4. 合冲刑害破的结构关系。
5. 合化状态链。
6. 调候、扶抑、通关、病药策略。
7. 特殊格局和从化保护。
8. 岁运触发。
9. 专题 Profile。

每条规则必须包含：

```text
ruleId
system
layer
topic
predicate
exceptions
evidenceFields
sourceRuleIds
priority/weight
conflictPolicy
riskBoundary
lifecycle
```

规则实现不得只返回自然语言。自然语言必须从结构化命题和 evidence 渲染。

门禁：没有反例、例外或风险边界的规则不得晋升 production。

### B5：不确定性、冲突和证据图

动作：

1. 对候选 canonical 输入执行集合值计算。
2. 对每个字段计算候选值集合和稳定性。
3. 将 `unknown` 与 `false` 分离。
4. 将未解决冲突作为一等输出。
5. 建立 Evidence DAG。
6. 验证上游不确定性不会在下游无依据消失。

门禁：任何最终命题无法回溯到输入、Profile、算法或规则时停止。

### B6：集成和交付

动作：

1. 接入 `calculate_pure_analysis` 的单一生产链。
2. Capability schema 暴露结构化结果和 evidence。
3. Web/API/Bot/CLI/Agent 只消费同一输出。
4. Markdown 只负责呈现，不重算规则。
5. 对同一固定样本执行多端 semantic hash 对比。

门禁：任何交付端出现独立排盘、独立规则或独立权重实现时阻断。

## 4. 单切片构建模板

每个最小切片应填写：

```text
ID:
标题:
所属波次:
对象定义:
定义域:
值域:
Profile 依赖:
来源:
当前实现:
目标实现:
无定义条件:
不变量:
正例:
反例:
边界例:
性质测试:
Golden:
Evidence 节点:
风险边界:
兼容影响:
回滚方式:
Owner:
```

示例切片应足够小，例如“十神天干到天干映射”，而不是“完成所有用神系统”。

## 5. 测试结构

### 5.1 穷举测试

适用于有限映射：

- 10 天干。
- 12 地支。
- 60 干支。
- 100 个日干/目标干十神组合。
- 固定关系表的所有合法输入。

### 5.2 性质测试

优先验证：

- 闭合性。
- 双射或单射性质。
- 周期性。
- Profile 固定下的确定性。
- 输入候选缩小时的单调性。
- 上游不稳定时的非确定性传播。
- Evidence 图无环和引用完整。

### 5.3 边界矩阵

每个时间边界至少覆盖：

```text
boundary - epsilon
boundary
boundary + epsilon
```

并记录：

- 输入时区。
- UTC 时刻。
- 经纬度。
- Profile。
- provider 版本。
- 预期发生变化的字段。
- 预期保持稳定的字段。

### 5.4 Golden

Golden 只锁定已审查行为，不自动证明行为正确。每个 Golden 必须注明：

- 来源或构造方式。
- 是否匿名合成样本。
- 规则/Profile 版本。
- 预期字段。
- 禁止字段。
- 变更时的人工复核要求。

### 5.5 Oracle

Oracle 只用于差异发现。发生差异时必须分类：

- Profile 不同。
- provider 精度不同。
- 历史时区数据不同。
- 实现 bug。
- Oracle bug。
- 传统流派差异。
- 尚无法归因。

禁止采用“多数库一致即真”的投票策略。

## 6. 现有验证入口

当前相关入口包括：

```bash
.venv/bin/python -m pytest -q tests/regression/test_location.py
.venv/bin/python -m pytest -q tests/regression/test_calendar_oracle_contract.py
.venv/bin/python -m pytest -q tests/regression/test_fate_policy_assets.py
.venv/bin/python -m pytest -q tests/regression/test_bazi_ziwei_rule_depth.py
.venv/bin/python -m pytest -q tests/regression/test_evidence_coverage_trend_gate.py
bash scripts/provider-dependency-smoke.sh
bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick
bash scripts/local-ci.sh --profile quick
```

这些入口目前验证现有工程，不代表数学形式化已经完成。新增机器契约后必须增加专用 gate，而不是只扩充文档。

## 7. 构建审查清单

### 定义

- [ ] 对象有明确 ID。
- [ ] 定义域和值域明确。
- [ ] 全函数、偏函数或关系类型明确。
- [ ] Profile 参数完整。
- [ ] 无定义状态明确。

### 来源

- [ ] 来源可追踪。
- [ ] 来源用途和许可证边界明确。
- [ ] 流派差异未被隐藏。
- [ ] 文案没有被冒充为基础事实。

### 实现

- [ ] 只有一个生产事实源。
- [ ] 没有隐式 fallback。
- [ ] 没有 delivery 端重复算法。
- [ ] 版本和 hash 可记录。

### 测试

- [ ] 正例。
- [ ] 反例。
- [ ] 边界例。
- [ ] 性质测试。
- [ ] Golden 或差异报告。
- [ ] 跨端一致性。

### 输出

- [ ] Evidence 完整。
- [ ] 不确定性可见。
- [ ] 冲突可见。
- [ ] 风险边界可见。
- [ ] 没有科学效力越权声明。

## 8. 停止条件

遇到以下任一情况，停止晋升：

- 规则来源无法确定。
- 同一术语存在未解决的互斥定义。
- Profile 不完整却要求唯一输出。
- 边界样本无法解释。
- 实现依赖未登记或不可复现资源。
- 只能通过修改报告文案掩盖结构错误。
- Golden 变更没有明确原因。
- 测试只能证明当前实现自洽，不能独立发现错误。
- 输出包含无证据的确定性健康、财富、灾祸或法律结论。
