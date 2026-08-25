# 八字数学形式化维护指南

> 状态：工作草案 v0.1
> 适用对象：形式规范、Profile、机器契约、规则、算法、Golden、Evidence 和交付映射。

## 1. 维护目标

维护工作的目标不是保持输出永远不变，而是保证每次变化：

- 有明确原因。
- 有可识别版本。
- 有影响分析。
- 有正反例和边界证据。
- 有兼容或迁移策略。
- 可以回滚。
- 不会把不确定性或争议隐藏起来。

## 2. 版本对象

下列版本必须分开管理：

| 版本 | 说明 |
| --- | --- |
| `formalSpecVersion` | 数学定义和证明义务版本 |
| `inputSchemaVersion` | 原始与 canonical 输入结构版本 |
| `profileVersion` | 边界约定和算法选择版本 |
| `calendarEngineVersion` | 历法与四柱实现版本 |
| `ruleSetVersion` | 规则集合和条件版本 |
| `weightPolicyVersion` | 权重和冲突排序版本 |
| `evidenceSchemaVersion` | Evidence 图和字段版本 |
| `capabilityEngineVersion` | 对外 capability 引擎版本 |
| `dependencyLockVersion` | 时区、历法、地点和 vendor 依赖锁定版本 |

禁止只增加一个总版本号而无法判断哪一层发生变化。

## 3. 语义版本规则

每个版本对象采用语义版本思想，但是否增加 major/minor/patch 必须按行为影响判断。

### Patch

允许：

- 不改变机器语义的文字澄清。
- 修复断链引用。
- 增加不改变既有结果的测试。
- 补充已有规则的来源元数据。

不得用于：任何会改变 canonical 输出、规则状态或 Evidence 结构的变更。

### Minor

适用于向后兼容扩展：

- 新增可选字段。
- 新增不影响旧 Profile 的规则。
- 新增明确 opt-in 的 Profile。
- 新增 Evidence 节点但保留既有字段语义。

### Major

适用于：

- 年、月、日、时柱边界语义变化。
- canonical 输入含义变化。
- 同一 Profile 下既有样本输出变化。
- 删除或重定义规则。
- 权重或冲突策略导致既有结论反转。
- Evidence 字段改变含义或删除。
- 历史结果无法按旧语义重放。

## 4. 变更分类

| 类别 | 典型变更 | 最低门禁 |
| --- | --- | --- |
| M0 文档澄清 | 术语、链接、非语义说明 | 文档复核、链接检查 |
| M1 输入/Profile | DST、地点解析、子时、真太阳时选项 | schema、边界矩阵、兼容测试 |
| M2 基础算法 | 四柱、五行、十神、藏干映射 | 穷举、性质测试、Golden、oracle 差异 |
| M3 规则语义 | 强弱、格局、调候、用神、合化 | 正反例、冲突、来源、risk gate |
| M4 权重裁决 | 优先级、置信度、冲突策略 | 前后 diff、反转清单、人工复核 |
| M5 Evidence | 节点、字段、引用和图结构 | schema、DAG、coverage、跨端测试 |
| M6 交付 | Markdown、Web、Bot、API 映射 | semantic diff、可见性、无重复算法 |

一个变更可能属于多个类别，必须执行最高等级及所有相关门禁。

## 5. 不可变 Profile

已经被生产结果引用的 Profile 视为不可变。

维护规则：

1. 不得原地改变边界约定。
2. 不得让相同 Profile ID 指向新 provider 版本。
3. 不得覆盖旧 hash。
4. 修复错误时创建新 Profile 或新引擎版本。
5. 历史 Profile 可以 deprecated，但在保留期内必须可解析。
6. 无法重放的 Profile 必须记录原因和缺失依赖。

推荐结果元数据：

```text
formalSpecVersion
profileId
profileVersion
profileHash
engineVersion
ruleSetVersion
weightPolicyVersion
evidenceSchemaVersion
dependencyVersions
canonicalInputHash
canonicalOutputHash
```

## 6. 规则维护

### 6.1 新增规则

必须：

- 分配稳定 `ruleId`。
- 声明来源和来源用途。
- 声明 `appliesWhen`。
- 声明 `doesNotApplyWhen` 或 exceptions。
- 声明 evidence 字段。
- 声明冲突策略。
- 声明风险边界。
- 添加正例、反例和边界例。
- 默认从非 production 生命周期开始。

### 6.2 修改规则

必须提供前后差异：

- 哪些条件改变。
- 哪些样本由 true 变 false。
- 哪些样本由 false 变 true。
- 哪些样本进入 unknown 或 conflict。
- 哪些报告命题发生变化。
- 是否改变权重或优先级。

禁止仅更新自然语言摘要而不更新机器契约。

### 6.3 删除规则

删除流程：

1. 标记 deprecated。
2. 记录替代规则或删除原因。
3. 保留兼容窗口。
4. 验证旧结果仍能解释其历史规则 ID。
5. major 版本中才能移除机器定义。

规则 ID 不得复用。

## 7. 来源维护

来源发生变化时必须区分：

- 许可证或分发状态变化。
- 上游版本变化。
- 文本版本变化。
- 传统流派差异。
- 项目对来源的解释变化。

来源更新不得自动修改生产规则。正确顺序是：

```text
来源变更
-> source diff
-> 规则影响分析
-> 新规则/Profile 候选
-> fixture 与 gate
-> 人工复核
-> 版本化晋升
```

Oracle、benchmark 和 reference-only 资源只能用于发现差异，不能静默改变生产结果。

## 8. Golden 维护

Golden 失败时不得直接更新期望值。必须先归因：

1. 规范预期变化。
2. Profile 变化。
3. provider 升级。
4. 时区或地点数据升级。
5. 实现 bug。
6. fixture bug。
7. 未解释差异。

只有前六类且证据闭合后才允许更新。未解释差异必须保持 gate 失败或进入显式隔离队列。

Golden 更新记录至少包含：

- 旧输出 hash。
- 新输出 hash。
- 变化字段。
- 对应规范或 Profile 版本。
- 变更原因。
- 审查人或 owner。
- 回滚提交。

## 9. 不确定性维护

新增输入精度、候选来源或边界模型时必须验证：

- 候选集合没有被静默截断。
- 更精确输入满足候选收缩单调性。
- 不受影响字段仍保持稳定。
- 受影响规则变为条件结论、unknown 或 conflict。
- 报告不把多候选压成一个无条件结论。
- Evidence 图保留候选来源和消歧过程。

禁止把“不知道”转换为低分，也禁止用平均命盘或平均柱表示多个离散候选。

## 10. 依赖升级

升级以下依赖视为形式语义变更候选：

- 历法 provider。
- IANA tzdata。
- 地点目录。
- 天文或节气数据。
- vendor 快照。
- 规则数据和典籍索引。

升级流程：

1. 固定新版本和 hash。
2. 运行边界矩阵。
3. 运行全量 Golden。
4. 生成旧版/新版字段级 diff。
5. 对差异分类。
6. 决定 patch、minor 或 major。
7. 更新 Profile 和 Evidence 元数据。
8. 保留回滚版本。

不得使用浮动依赖结果作为长期证明证据。

## 11. 实现与文档同步

变更顺序：

```text
形式规范
-> 机器契约
-> 实现
-> 测试和 fixture
-> Evidence
-> 人类文档
-> 交付说明
```

紧急 bug 可以先修复实现，但必须在同一发布窗口补齐规范差异、测试、版本和回滚证据。不得长期让文档、机器契约和生产实现互相矛盾。

## 12. 争议和流派差异

遇到不同流派定义时，不采用无依据的“唯一正确”表述。处理方式：

- 如果差异可配置：建立不同 Profile。
- 如果差异只影响解释：建立不同 rule set。
- 如果来源不足：保持 unknown 或 research 状态。
- 如果实现只支持一种：明确支持范围，不冒充全流派。
- 如果差异无法兼容：使用 major 版本和迁移说明。

默认生产 Profile 必须有明确选择依据和 owner，不能因为“当前代码这样写”而成为事实标准。

## 13. 故障处理

发现形式化或实现错误时：

1. 记录受影响对象和版本。
2. 确定是否影响四柱基础事实。
3. 确定受影响时间范围、Profile 和结果。
4. 冻结相关规则晋升。
5. 增加最小复现和反例。
6. 修复规范、契约或实现中的真实错误层。
7. 生成前后 diff。
8. 发布新版本。
9. 记录历史结果是否需要重新计算。
10. 不删除能解释事故的旧版本证据。

不得只通过修改 Markdown 文案掩盖底层错误。

## 14. 定期维护节奏

### 每次变更

- 运行相关 focused tests。
- 运行契约和 source hygiene。
- 更新版本、hash 和变更说明。

### 每个发布候选

- 运行 quick gate。
- 运行边界代表集。
- 运行多端 semantic diff。
- 检查未解决 unknown/conflict 数量是否异常变化。

### 每次依赖升级

- 运行全量边界矩阵和 Golden diff。
- 复核 provider/source/license drift。

### 定期审查

- 检查 deprecated Profile 和规则。
- 检查断链 evidence refs。
- 检查来源状态变化。
- 检查文档与机器契约漂移。
- 检查是否存在 delivery 端重复算法。

## 15. 变更审查模板

```text
变更 ID:
变更类别:
涉及版本:
对象/规则/Profile:
原因:
来源:
旧语义:
新语义:
受影响字段:
受影响 fixtures:
边界影响:
不确定性影响:
Evidence 影响:
兼容级别:
迁移方案:
验证命令:
回滚方案:
Owner:
审查结论:
```

## 16. 发布前维护清单

- [ ] 工作区干净，提交可追踪。
- [ ] 规范版本与实现版本一致。
- [ ] Profile 不可变规则未被破坏。
- [ ] 依赖和数据 hash 已锁定。
- [ ] 来源和许可证状态未被伪造。
- [ ] 正例、反例和边界例通过。
- [ ] Golden 变化已归因。
- [ ] unknown/conflict 没有被静默消除。
- [ ] Evidence 引用完整且无环。
- [ ] Web/API/Bot/CLI/Agent 同源。
- [ ] 报告层没有新增规则。
- [ ] 风险边界和免责声明保留。
- [ ] 没有宣称数学化证明了现实预测效力。
- [ ] 回滚版本和证据可用。
