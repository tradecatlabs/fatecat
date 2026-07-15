# 公开字段消费者与迁移边界

## 审计范围

扫描命令：

```bash
rg -n --no-ignore 'ganzhiRelations|branchRelations|ganzhiExtra|spiritsExplain|spiritsFull' \
  contracts catalog docs domains/fate-analysis/services/fate-core/src \
  domains/experience-delivery/services/fatecat-delivery/src tests
```

归档审计样本只作为历史证据，不作为当前生产消费者。

## 消费者清单

| 字段 | 当前生产消费者 | 契约 / 测试消费者 | 决策 |
| --- | --- | --- | --- |
| `branchRelations` | `relation.py`、`regular_pattern.py`、`topic_profile.py`、`yongshen.py`、`calculate_pure_analysis.py`、`report_generator.py`、`mingli_baseline.py` | `pure_analysis.json`、`classics_rule_index.json`、`rule_depth_registry.json`、statement golden | 保留并升级为地支关系 canonical；新增稳定 `canonical` 记录，旧 detail/list 由其投影 |
| `ganzhiExtra` | `relation.py`、`report_generator.py` | `pure_analysis.json`、`rule_depth_registry.json` | 保留为同柱合、天干克、地支入库的独占事实；不拥有地支合冲刑害 |
| `ganzhiRelations` | `calculate_pure_analysis.py`（仅取天干）、`relation.py`（仅取天干）、`output_formatter.py`（公开结构化输出） | `pure_analysis.json`、evidence baseline、rule registries、statement golden、文档 | 当前版本保留为过渡容器；`tianGan` 是当前天干事实，`diZhi` 必须从 `branchRelations.canonical` 投影且不得独立维护规则 |
| `spiritsFull` | `calculate_pure_analysis.py`、`report_generator.py` | `pure_analysis.json`、rule registry、报告测试 | 神煞 canonical；所有新消费者只读该字段 |
| `spirits` | 未发现当前生产逻辑读取；由 calculator/base provider 输出 | `pure_analysis.json`、历史 OI 文档 | 保留兼容别名，不渲染、不新增消费者；主版本迁移后再移除 |
| `spiritsExplain` | 未发现当前生产逻辑读取；由 calculator/base provider 输出 | `pure_analysis.json`、历史 OI 文档 | 保留 `spiritsFull.descriptions` 兼容投影，不渲染、不新增消费者 |

## 兼容策略

1. 本任务不删除 profile 中现有顶层字段，避免无版本升级的 API 破坏。
2. `ganzhiRelations` 增加 `projectionOf.diZhi=branchRelations.canonical` 和 `deprecatedAsSourceFields=[diZhi]`，只弃用地支兼容投影的事实源资格，不错误弃用天干事实。
3. 现有 evidence 字段名按当前公开版本契约保留；规则文档说明 `branchRelations.canonical` 是地支依据，`ganzhiRelations.tianGan` 是当前天干事实。
4. `spirits` 与 `spiritsExplain` 保留同对象/派生值语义，不重复计算；报告继续只读 `spiritsFull`。
5. 未来删除旧字段的触发条件：主版本契约、公开弃用周期、仓库内消费者归零、API fixture 迁移和回滚版本同时具备。

## 回滚边界

- 可以回滚 Markdown 章节排序和兼容字符串格式。
- 不可回滚单柱自关联修复、canonical 柱位键或“地支只算一次”的架构约束。
- 若外部调用方依赖旧字符串，恢复投影格式即可，不得恢复独立规则计算。
