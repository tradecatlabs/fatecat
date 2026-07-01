# FateCat 专业八字体系资源地图

更新时间：2026-07-01

## 资源使用原则

- `production_dependency`：允许进入生产请求链路，必须有声明依赖、许可证、测试和升级门禁。
- `oracle_only`：只允许用于测试、对照、差异解释，不允许进入生产入口。
- `evaluation_only`：只允许用于离线 benchmark、分类准确率和失败归因，不允许参与生产排盘。
- `reference_only`：只允许做规则材料和结构参考，不复制大段源码/原文，不作为 runtime dependency。
- `future_candidate`：必须先完成 license、数据质量、adapter、验收和 release gate，才能升级。

## 核心资源表

| 资源 | usageRole | license boundary | productionUseAllowed | 可补能力 | 禁止用途 |
| --- | --- | --- | --- | --- | --- |
| `lunar-python` | `production_dependency` | MIT；项目依赖已声明在 `pyproject.toml`、`requirements.txt`、lock 文件 | true | 四柱、节气、干支、生肖、八字、五行、十神、大运、基础历法。 | 禁止绕过依赖直接绑定 vendor 快照；禁止把 oracle 差异无解释地改成生产真相。 |
| `sxtwl` | `oracle_only` | PyPI/本地依赖声明存在；只用于 oracle 测试 | false | 节气、历法、稳定四柱样本对照。 | 禁止进入 `fate_core.kernel/providers/usecases` 生产请求路径。 |
| `sxwnl` | `oracle_only` | 本地参考快照 license 风险未完全生产化 | false | 节气、历法、四柱离线对照。 | 禁止作为用户请求路径依赖；禁止绕过 license 风险。 |
| `paipan` | `oracle_only` | 本地参考快照，需保留 license/source 审查 | false | 真太阳时、早晚子时、排盘口径对照。 | 禁止直接替换生产时间管线；必须先有 adapter 测试和口径说明。 |
| `bazica` | `oracle_only` | MIT；跨语言 Go 实现 | false | 四柱/大运交叉校验、离线 oracle。 | 禁止为了参考引入 Go runtime 到 Python 请求链路。 |
| `MingLi-Bench` | `evaluation_only` | MIT；离线 benchmark 数据 | false | 160 题样本外评测、分类准确率、失败归因。 | 禁止进入请求链路；禁止答案泄漏；禁止把 sample 命中率当专业完成度。 |
| `BaziQA` | `future_candidate` | 待审查 license、dataset schema 和题型契约 | false | 可能补充八字问答样本外评测。 | 未完成准入审查前禁止纳入正式 release gate 或 runtime。 |
| `bazi-1` | `reference_only` | 本地快照缺明确上游 LICENSE，`distributionAllowed=false` | false | 金不换、调候、神煞、格局、干支关系、十神规则材料。 | 禁止作为生产依赖；禁止复制大段原文；禁止无 `sourceRuleId` 进入报告。 |
| `classics/ctext-bazi-corpus` | `reference_only` | ctext 可见文本整理；`copyright_review.tsv` 逐本标记 `review_required` | false | 五行精纪、滴天髓阐微、子平真诠评注、珞琭子三命消息赋注、兰台妙选、神峰通考等规则源语料。 | 禁止作为 runtime dependency；禁止把大段原文复制进报告；禁止未经人工复核直接升级为 production 断语。 |
| `bazi-calculator-by-alvamind` | `reference_only` | MIT 字段来自 package 元信息，仍需本地 license 审查 | false | TypeScript 基础分析结构和输入输出组织参考。 | 禁止作为生产依赖；禁止用它补高级专业断法。 |
| `rule-engine` | `future_candidate` | PyPI BSD；当前未纳入项目依赖 | false | 后期 registry 表达式膨胀时可能替代局部条件表达式。 | 当前阶段禁止引入；优先 Python evaluator 和现有 registry。 |
| `iztro` | `future_candidate` | MIT；紫微方向候选，不属于八字 100% 主线 | false | 紫微盘面和后续独立 capability。 | 禁止混入默认八字 Markdown；紫微需独立验收。 |

## 能力缺口到资源映射

| 能力缺口 | 主资源 | 辅助资源 | 交付形态 |
| --- | --- | --- | --- |
| 基础排盘 | `lunar-python` | `sxtwl`、`sxwnl`、`bazica` | production provider + oracle contract + golden。 |
| 节气/立春/起运 | `lunar-python` | `sxtwl`、`sxwnl`、`paipan` | calendar boundary golden + tolerance/failureExplanation。 |
| 真太阳时/早晚子时 | 本仓 adapter | `paipan` | adapter 测试 + boundary golden + 口径说明。 |
| 日主强弱 | 本仓 evaluator | `bazi-1` | rule_depth_registry + strength golden。 |
| 常规格局 | 本仓 evaluator | `bazi-1`、`bazi-calculator-by-alvamind` | classics_rule_index + rule_depth_registry + report evidence。 |
| 高级格局 | 本仓 evaluator | `bazi-1` | appliesWhen/doesNotApplyWhen + 正反例 golden。 |
| 合化成败 | 本仓 evaluator | `bazi-1`、`paipan` | condition chain + transform status + negative golden。 |
| 用神裁决 | 本仓 evaluator | `bazi-1` | 调候/扶抑/通关/病药 strategy matrix。 |
| 岁运专题 | `lunar-python` 运势字段 + 本仓 evaluator | `MingLi-Bench` | fortune trigger matrix + topic profile + benchmark feedback。 |
| 样本外评测 | `MingLi-Bench` | `BaziQA` | predictions JSONL + report JSON + failure taxonomy。 |

## 升级条件

| 资源 | 可升级条件 | 禁止升级条件 |
| --- | --- | --- |
| `lunar-python` | 通过 calendar oracle、solar terms golden、bazi golden、API contract 和 local-ci quick/full。 | 上游 API 变化未验证，或依赖锁与实际 import 口径不一致。 |
| `sxtwl` | 只增强 oracle；如需生产化必须先完成 license、adapter、性能、回归和替换策略。 | 生产入口 import，或对照差异无法解释仍标绿。 |
| `sxwnl` | 只增强离线 oracle 和差异审计。 | license/source 不清时进入 runtime。 |
| `paipan` | 真太阳时/早晚子时 adapter 有独立测试、口径文档和 golden 对照。 | 未说明口径差异就替换当前时间管线。 |
| `bazica` | 只扩展离线 oracle 样本。 | 为了快速补功能引入跨语言运行时所有权。 |
| `MingLi-Bench` | 用于评测门槛、分类失败队列和 regression policy。 | 用答案训练或硬编码预测；把 benchmark 数据当用户样例。 |
| `BaziQA` | 完成 `TP-09.03` license、schema、adapter 和 no-runtime gate。 | license/source 不清时纳入 release gate。 |
| `bazi-1` | 只能把短规则摘要、条件和来源转成本仓 registry。 | 复制大段原文或作为生产依赖。 |
| `classics/ctext-bazi-corpus` | 只允许先进入规则索引种子、人工复核、短摘要和 golden 依据。 | 未经版权/文本质量复核直接进入报告长文引用；OCR 质量差的《增补星平会海命学全书》不得入库。 |
| `rule-engine` | 只有当 JSON registry + Python evaluator 条件表达膨胀到不可维护，并有迁移测试时考虑。 | 为了“看起来专业”提前新增规则引擎依赖。 |

## TP-01.02 Gate 判定

- `production_dependency` 边界明确：`PASS`
- `oracle_only` 边界明确：`PASS`
- `evaluation_only` 边界明确：`PASS`
- `reference_only` 边界明确：`PASS`
- `future_candidate` 边界明确：`PASS`
- `production/oracle/evaluation/reference/future_candidate 边界不混写`：`PASS`
