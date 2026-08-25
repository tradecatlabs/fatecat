# 八字数学形式化文档集

> 状态：工作草案 v0.1
> Owner：`tradecatlabs/fate-core`
> 范围：八字输入、历法排盘、有限结构推导、规则求值、证据链与不确定性传播
> 最近评审：2026-08-25

## 目的

本目录为 FateCat 八字数学形式化工作的长期人类入口。目标是把现有八字能力拆成可定义、可实现、可验证、可追踪和可维护的数学对象，而不是用数学符号包装传统断语。

本体系只试图证明：

1. 给定输入、规则 Profile、引擎版本和依赖版本后，程序是否确定地执行了声明的规则。
2. 四柱和派生结构是否满足已声明的不变量。
3. 每条规则是否具有明确条件、例外、证据和冲突处理。
4. 输入歧义和上游不确定性是否被完整传播到下游。
5. Web、API、Bot、CLI 和 Agent 是否消费同一事实源。

本体系不试图证明：

- 命理预测具备现代科学意义上的因果性或预测效力。
- 传统规则可以通过任意分数变成客观自然定律。
- 测试通过等于现实人生事件预测正确。
- 数学形式化可以替代来源审查、专家复核或风险治理。

## 文档地图

| 文档 | 职责 | 当前状态 |
| --- | --- | --- |
| [`AGENTS.md`](AGENTS.md) | 约束后续代理和维护者的修改边界与同步要求 | current |
| [`FORMAL_SPEC.md`](FORMAL_SPEC.md) | 定义集合、函数、关系、稳定性、规则逻辑、证据图和证明义务 | v0.1 工作草案 |
| [`BUILD.md`](BUILD.md) | 规定从自然语言规则到机器契约、实现和测试的构建顺序 | v0.1 工作草案 |
| [`MAINTENANCE.md`](MAINTENANCE.md) | 规定版本、变更分类、Profile、兼容、回归和争议处理 | v0.1 工作草案 |

后续计划文档：

| 计划文档 | 内容 |
| --- | --- |
| `CALENDAR_AND_PILLARS.md` | 年柱、月柱、日柱、时柱映射与节气、子时、DST、真太阳时边界 |
| `DERIVED_STRUCTURES.md` | 五行、阴阳、十神、藏干、十二长生、干支关系等有限映射 |
| `RULE_SEMANTICS.md` | 格局、强弱、调候、用神、合化和岁运规则的形式语义 |
| `UNCERTAINTY_AND_EVIDENCE.md` | 候选命盘、字段稳定性、条件结论、证据 DAG 和冲突传播 |
| `PROOF_OBLIGATIONS.md` | 每层不变量、性质测试、golden、oracle 和跨端一致性门禁 |

计划文档只有在定义、来源、实现映射和验证方法都明确后才能从本表晋升为当前文档。

## 真相源边界

本目录是人类可读设计说明，不是运行时机器事实源。

| 层级 | 真相源 |
| --- | --- |
| Capability 状态和引擎入口 | `contracts/fate/capabilities/registry.json` |
| 八字 Profile | `contracts/fate/capabilities/profiles/bazi.json`、`contracts/fate/profiles/pure_analysis.json` |
| 规则和来源索引 | `contracts/fate/rule_depth_registry.json`、`contracts/fate/classics_rule_index.json` |
| Evidence 字段 | `contracts/fate/evidence_schema.json` |
| 权重边界 | `contracts/fate/weight_policy.json` |
| 位置和时间契约 | `contracts/fate/locations/` |
| 生产计算入口 | `fate_core.usecases.calculate_pure_analysis` |
| 生产历法底座 | `lunar-python` 的已登记版本与 adapter |
| Golden 和边界样本 | `domains/fate-analysis/data-products/bazi/golden/` |
| 仓库级回归 | `tests/regression/` 与 `scripts/local-ci.sh` |

未来如果建立 `contracts/fate/formalization/`，其中的 schema、Profile、有限映射表和版本 manifest 才是可执行形式化契约。本目录负责解释这些契约，不复制第二份机器数据。

## 分层模型

八字形式化采用以下依赖方向：

```text
原始输入空间
  -> 输入规范化关系
  -> canonical 时间与地点候选集
  -> 历法与四柱偏函数
  -> 有限派生结构
  -> 规则谓词和例外
  -> 冲突裁决与不确定性传播
  -> Evidence DAG
  -> Capability 输出
  -> Web/API/Bot/CLI/Agent 交付
```

禁止反向依赖：

- 报告文案不得反向决定规则结果。
- Web/Bot 不得重新计算四柱或专业结论。
- Oracle 和 evaluation-only 资源不得成为未登记的生产事实源。
- 权重不得覆盖基础排盘事实。
- 下游确定性不得高于上游输入和证据的确定性。

## 初始建模原则

1. **有限代数优先**：天干、地支、六十甲子、五行、阴阳和十神优先建成有限集合与总映射。
2. **偏函数优先于猜测**：缺输入、超范围或约定不完整时返回无定义或标准错误，不静默回退。
3. **集合值优先于伪精度**：DST、时间误差或边界歧义产生候选集合，不使用无依据百分比掩盖。
4. **Profile 显式化**：立春年界、节气月界、子时换日、真太阳时和依赖版本必须进入 Profile。
5. **规则与文案分离**：规则输出结构化命题和证据，Markdown 只负责呈现。
6. **来源和适用边界并列**：每条规则同时声明来源、适用条件、不适用条件和风险边界。
7. **可反驳性**：每个阶段必须列出能证明实现错误的 falsifier。
8. **不做科学效力越权声明**：形式正确性、软件正确性和现实预测效力必须分开。

## 当前里程碑

| 里程碑 | 目标 | 状态 |
| --- | --- | --- |
| M0 | 锁定范围、术语、文档结构和维护规则 | 本文档集已建立 |
| M1 | 形式化输入空间和规范化关系 | 草案已写入 `FORMAL_SPEC.md` |
| M2 | 形式化干支、六十甲子和四柱输出空间 | 草案已写入 `FORMAL_SPEC.md` |
| M3 | 形式化年/月/日/时柱映射和边界 | 待构建 |
| M4 | 形式化五行、阴阳、十神等有限派生 | 十神族草案已建立，其余待构建 |
| M5 | 形式化规则、冲突和不确定性 | 基础语义草案已建立 |
| M6 | 建立机器契约、性质测试和证据图 | 待构建 |
| M7 | 与 `calculate_pure_analysis` 和多端输出闭环 | 待构建 |

## 阅读顺序

首次参与者按以下顺序阅读：

1. 本文档。
2. `FORMAL_SPEC.md`。
3. `BUILD.md`。
4. `MAINTENANCE.md`。
5. `contracts/fate/capabilities/profiles/bazi.json`。
6. `contracts/fate/evidence_schema.json`。
7. `contracts/fate/rule_depth_registry.json`。
8. `fate_core.usecases.calculate_pure_analysis` 及其测试。

## 完成定义

一项形式化能力只有同时满足以下条件才算完成：

- 数学对象、定义域和值域明确。
- Profile 依赖明确。
- 无定义和歧义状态明确。
- 来源、条件、例外和风险边界明确。
- 对应机器契约存在且版本化。
- 实现只消费机器契约或已登记算法。
- 正例、反例、边界例和性质测试齐全。
- Evidence 可以回溯到输入、版本、规则和依赖。
- 多端输出不产生第二事实源。
- 文档没有把软件验证写成现实预测效力证明。
