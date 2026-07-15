# 综合八字字段所有权与关系契约

## 目标终态

计算层中每个关系事实只计算一次；结构化旧字段只做兼容投影；Markdown 中每个静态业务字段只由一个章节负责展示。禁止在报告末尾做字符串去重，因为那会掩盖字段所有权错误并可能误删合法内容。

## 报告章节所有权

| Canonical 章节 | 唯一拥有字段 | 不再拥有 |
| --- | --- | --- |
| 基本资料（含真太阳时、节气） | `input`、`meta`、基本历法信息 | 五行、格局、关系、运势 |
| 八字排盘详情 | `fourPillars`、`tenGods`、`hiddenStems`、`twelveGrowth`、四柱空亡与纳音 | `wuxingScores`、`climateScores`、`ganzhiExtra`、`branchRelations` |
| 日主概览 | `dayMaster` 的日干、五行、阴阳、强弱、自坐摘要 | 完整五行表、`geju`、`wuxingState` |
| 五行喜忌（调候与平衡） | `fiveElements`、`wuxingScores`、`wuxingState` | `climateScores`、完整格局、运势触发 |
| 五行停匀与寒湿燥热（调候依据） | `climateScores`、调候依据、拱神与空亡提示 | 五行分数、格局、运势 |
| 干支取象（原文） | `ganzhiImagery` | 关系计算结果 |
| 命造格局（格局用神） | `geju`、`yongShen` 的格局/取用依据 | 调候表的重复展开、动态运势 |
| 节气司令 | `jieqi`、`siling` | 运势章节中的静态重复 |
| 干支关系 | `ganzhiExtra`、`branchRelations` 及 `ganzhiRelations.tianGan` 当前事实 | 八字排盘详情中的关系副本、`ganzhiRelations.diZhi` 兼容投影 |
| 神煞断语 | `spiritsFull` | `spirits`、`spiritsExplain` 的重复渲染 |
| 运势分析 | `fortune`、`dayun`、`liunian`、`liuyue`、`xiaoyun` 的动态结果 | 静态空亡、司令、完整用神原文 |
| 袁天罡称骨 | `boneWeight` | 八字核心判断 |

## 关系字段分层

| 字段 | 终态角色 | 计算规则 |
| --- | --- | --- |
| `branchRelations` | 地支关系 canonical 结果 | 只从已登记的 bazi-1 `zhi_6hes`、`zhi_huis`、`zhi_3hes`、`zhi_atts` 生成；按柱位实例匹配 |
| `ganzhiExtra` | 同柱干支合、天干克、地支入库的 canonical 补充事实 | 保留现有成熟数据调用；不重复计算地支合冲刑害 |
| `ganzhiRelations` | 过渡容器 | `tianGan` 使用 bazi-1 `gan_hes`、`gan_chongs` 并作为当前天干事实；`diZhi` 必须从 `branchRelations` 投影且列入 `deprecatedAsSourceFields` |
| `spiritsFull` | 神煞 canonical 结果 | 报告和内部规则只消费此字段 |
| `spirits`、`spiritsExplain` | 公开兼容别名 | 当前版本保留，不独立计算、不独立渲染；未来主版本再评估移除 |

## Canonical 关系语义

每条 `branchRelations.canonical` 记录必须包含：

- `key`：稳定去重键。
- `relation`：`六合`、`三会`、`三合`、`合`、`会`、`冲`、`刑`、`害`、`破` 或 `暗合`。
- `positions`：参与关系的柱位，使用 `year/month/day/hour`。
- `branches`：与 `positions` 同序的地支。
- `directional`：是否具有方向。
- `full`：组合关系是否完整。
- `element`：规则源提供时记录五行。
- `source`：固定指向所用 bazi-1 表名。
- `text`：可读依据，不作为去重键。

### 去重键

| 关系类别 | 方向 | Canonical key |
| --- | --- | --- |
| 六合、冲、害、破、暗合 | 对称 | `branch:<relation>:<排序后的柱位对>` |
| 刑 / 被刑 | 有向；`被刑`先规范化为相反方向的`刑` | `branch:刑:<source-position>><target-position>` |
| 同支自刑 | 需要两个不同柱位实例，按无序柱位对唯一 | `branch:刑:<排序后的柱位对>` |
| 半合、半会 | 对称 | `branch:<合或会>:<排序后的柱位对>` |
| 完整三合、三会 | 组合 | `branch:<三合或三会>:<规则 pattern>:<排序后的柱位集合>` |

### 基数与方向约束

1. 来源柱位与目标柱位必须不同；单个辰、午、酉、亥不得产生自刑。
2. 辰辰、午午、酉酉、亥亥只有存在两个不同柱位实例时才成立，并且同一柱位对只输出一次。
3. `被刑`不是第二种关系；它只用于把成熟表中的反向描述归一为有向 `刑`。
4. 对称关系按无序柱位集合去重；可读文本方向不影响事实唯一性。
5. `ganzhiRelations.diZhi` 只能由 canonical 记录投影，因此其信息可恢复但不能成为新的事实来源。

## 兼容与回滚边界

- 当前版本不删除 `ganzhiRelations`、`spirits`、`spiritsExplain`，避免静默破坏公开消费者。
- 兼容投影必须有回归测试证明来自 canonical 结果；任何重新引入独立规则表的改动应失败。
- 回滚只允许回滚 renderer 编排或投影格式，不允许恢复单支自关联和第二套地支算法。
- 若未来移除兼容字段，必须通过主版本契约、弃用公告和消费者迁移完成，不在本任务内直接删除。
