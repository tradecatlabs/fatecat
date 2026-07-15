# AGENTS.md - fate_core usecases evaluators

## 目录用途

`usecases/evaluators/` 承载 pure-analysis 中逐步抽离的纯 evaluator。它只把已经存在的盘面、registry 和运行时证据转换为结构化分析片段，不做交付、不渲染报告、不读取 benchmark 标准答案。

## 目录结构

```text
evaluators/
├── AGENTS.md
├── __init__.py
├── advanced_pattern.py
├── combine_transform.py
├── constants.py
├── fortune.py
├── regular_pattern.py
├── relation.py
├── strength.py
├── ten_god.py
├── topic_profile.py
└── yongshen.py
```

## 职责边界

- `advanced_pattern.py`：高级格局候选 evaluator，输出从格、化气、专旺、假从等候选成熟度与反证边界。
- `combine_transform.py`：合化条件链 evaluator，输出合象、候选、成化、破化、争合状态矩阵。
- `constants.py`：天干地支、五行、合化、冲克等 evaluator 共享常量；不承载业务流程。
- `fortune.py`：岁运触发矩阵 evaluator，输入 `raw` 与已识别 triggers，输出 `fortuneTriggerMatrix`。
- `relation.py`：消费 `branchRelations.canonical`、`ganzhiRelations.tianGan` 与 `ganzhiExtra` 的干支关系优先级和阻隔证据，输出 `ganzhiPriority` 所需排序结构；不得回读 `ganzhiRelations.diZhi` 兼容投影。
- `regular_pattern.py`：常规格局候选 evaluator，输出正格候选、uncertainty 与破格边界。
- `strength.py`：日主强弱评分 evaluator，输入 `raw` 与人元司令上下文，输出 `strengthScore`。
- `ten_god.py`：十神结构 evaluator，输入 `raw.tenGods` 与藏干，输出 `tenGodStructure` 与家族统计。
- `topic_profile.py`：事业、财运、婚姻、健康、学业、迁移、家庭 profile evaluator，输出结构评分、beta lifecycle 和报告风险边界。
- `yongshen.py`：用神策略排序 evaluator，输出调候、扶抑、通关、病药的 ranking、冲突矩阵和非绝对结论边界。
- `__init__.py`：只导出稳定 evaluator 函数，供 `calculate_pure_analysis.py` 编排使用。

## 依赖方向

- `calculate_pure_analysis.py -> usecases.evaluators`
- `usecases.evaluators -> usecases.rule_depth`
- 禁止依赖交付域、FastAPI、Bot、Web、Markdown 渲染或 benchmark evaluator。
- 禁止读取 MingLi/BaziQA 的 expected answer、question_id 或 scoring result。

## 重构纪律

- 每次只迁移一个 evaluator。
- 迁移必须保持输出 schema、字段名和风险边界不变。
- 新 evaluator 必须是纯函数；不得写文件、联网、读取环境变量或修改全局状态。
