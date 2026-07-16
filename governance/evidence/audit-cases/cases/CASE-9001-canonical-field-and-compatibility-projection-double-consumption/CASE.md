---
id: CASE-9001
slug: canonical-field-and-compatibility-projection-double-consumption
title: canonical 字段与兼容投影被双重消费
type: audit-case
status: active
owner: engineering
last_reviewed: 2026-07-15
severity: BLOCK
root_cause_class: canonical_field_and_compatibility_projection_double_consumption
review_profiles:
  - correctness
  - architecture
  - contract
  - test-quality
  - completion-verification
reviewer_prompts:
  - reviewers/compatibility-worship-audit-prompt.md
  - reviewers/wrong-concept-preservation-audit-prompt.md
  - reviewers/critical-review-audit-prompt.md
  - reviewers/test-quality-tdd-audit-prompt.md
trigger_signals:
  - canonical field
  - compatibility projection
  - duplicate report section
  - duplicate renderer
  - multiple truth sources
  - deprecated as source
  - consumer migration
  - report ownership
  - availability maturity migration
  - stale lifecycle consumer
audit_questions:
  - 每个业务概念是否只有一个 canonical 计算结果和一个报告章节 owner？
  - 兼容投影是否只由 canonical 结果生成，并被禁止参与新的计算、证据或独立渲染？
  - 所有消费者是否完成枚举与迁移，测试是否能发现遗漏消费者和重复输出？
  - 无序集合或映射是否会使 canonical 证据顺序在不同进程中漂移？
  - 生命周期迁移是否分别指定可执行资格与成熟度的 canonical 字段，并禁止内部门禁继续依赖旧顶层投影？
automation_candidate: 对 canonical、projectionOf、deprecatedAsSourceFields 和 renderer 消费点做静态扫描，并以唯一性、消费者清单、跨哈希种子和多端语义回归作为合并 Gate。
project_safe: false
---

# CASE-9001 canonical 字段与兼容投影被双重消费

## Problem Pattern

FateCat 为同一命理概念同时保留 canonical 字段和旧兼容字段，但计算器、evaluator、评测器或 Markdown renderer 把兼容投影继续当作独立事实源。结果表现为同一规则被计算两次、关系正反重复、报告章节或表格重复、证据链读取旧结构，甚至不同消费者得到不一致结论。兼容字段虽然标记了弃用，只要仍被新逻辑读取，就形成隐藏的第二真相源。

同一模式也适用于控制面生命周期：当 `availability` 已成为执行准入真相源、`maturity.status` 已成为成熟度真相源时，旧顶层 `status` 即使保留为兼容投影，也不得继续被 provider gate、control-plane、GEO audit 或 smoke 用来判断“能否执行”。否则 validated 且 available 的能力会被误拒绝，或被错误标记为 production。

## Why It Recurs

兼容字段与 canonical 字段通常具有相似名称和数据内容，局部开发者容易选择离当前代码最近的路径，而不是先确认字段所有权。结构测试如果只断言标题或字段“存在”，还会把重复输出固化为 golden。消费者清单不完整时，主报告修复后，benchmark、评测、Bot 或辅助 evaluator 仍可能静默读取旧结构。关系结果若先进入无序集合再输出，还会在跨进程时破坏可复现证据顺序。

## Audit Questions

- 当前变更涉及的每个业务概念，canonical 计算 owner、兼容投影 owner 和报告章节 owner 分别是谁？
- 兼容字段是否完全由 canonical 结果单向生成，是否存在任何 evaluator、评测器或 renderer 回读它进行新判断？
- `projectionOf`、`deprecatedAsSourceFields` 等机器边界是否与 profile、文档和实际消费者一致？
- `availability`、`maturity.status` 与兼容 `status` 的所有消费者是否已枚举；执行门禁是否只读取 `availability`，成熟度展示是否只读取 `maturity.status`？
- 是否用全仓符号与字段路径扫描建立了消费者清单，并对每个消费者记录迁移、保留或删除决定？
- 报告测试是否断言标题、业务表格、释义和关系键的语义唯一性，而非只断言它们出现？
- 对称关系、方向关系和自关系是否按柱位实例建模，并覆盖单实例、双实例和反向重复边界？
- canonical 数组是否有确定排序；同一输入在不同 `PYTHONHASHSEED` 和不同交付面是否逐项一致？

## Evidence To Request

- 字段所有权矩阵，明确 canonical 计算、兼容投影和报告章节的唯一 owner。
- 全仓消费者扫描结果，覆盖 API、Web、Bot、评测器、golden、profile、文档和导出脚本。
- 生命周期迁移还必须覆盖 control-plane、provider lifecycle/dependency/drift gates、公开发现页和 GEO audit，并提供旧字段零命中或明确兼容豁免证据。
- 修复前能失败、修复后能通过的关系基数、重复标题、重复表格和故障注入测试。
- 兼容投影由 canonical 单向生成的契约测试，以及禁止新消费者回读兼容字段的审查证据。
- 匿名固定输入在不同哈希种子、不同进程和多个交付面的 normalized 输出对比。
- 干净工作树或只包含当前任务补丁的 CI 证据，避免并行改动制造假失败或假通过。

## Finding Template

- Severity: BLOCK
- Category: canonical-ownership
- Evidence: 同一业务概念存在 canonical 与兼容字段双重计算或双重渲染；消费者清单显示旧投影仍被 evaluator、评测器、renderer 或生命周期门禁当作事实源；唯一性、生命周期一致性或跨进程确定性测试缺失或失败。
- Risk: 同一输入可能生成重复、矛盾或顺序漂移的结果，证据链和评测值与主报告不一致，多端交付无法可靠复现。
- Minimal Fix: 指定唯一 canonical owner，使兼容字段只由 canonical 单向投影；迁移全部内部消费者；删除重复 renderer；补消费者、唯一性、实例基数和确定性回归。
- Verification: 执行全仓消费者扫描、关系与报告定向回归、多端语义 diff、跨哈希种子测试，并在仅应用当前任务补丁的干净环境运行 quick CI。

## Gate Suggestion

发现兼容投影参与新计算、证据或独立渲染，或存在两个可独立变化的业务事实源时，合并必须 `BLOCK`。仅当兼容字段仍为公开契约、完全由 canonical 单向生成、没有内部事实消费者且有明确移除条件时，才允许保留并记录为 `WARN`。同类问题再次出现或可稳定扫描时，应晋升为项目 architecture Gate。

## Automation Candidate

- 扫描 `projectionOf` 与 `deprecatedAsSourceFields` 声明，对照内部字段读取点，发现新增回读即失败。
- 扫描 capability 注册表直接消费者，禁止内部执行门禁以兼容 `status` 代替 `availability`，并对 available/validated 与 available/production 组合建立回归。
- 建立报告章节 owner registry，对标准 Markdown 的标题和规范化业务表格执行唯一性检查。
- 对关系数组执行唯一键、同位置实例、方向语义和确定排序断言。
- 在 CI 中用多个 `PYTHONHASHSEED` 运行固定关系输入，并比较 canonical 键序列。
- 让 task closeout 强制附消费者清单、多端 parity 和干净补丁 CI 证据。

## Privacy Boundary

该案例依赖 FateCat 的 `branchRelations.canonical`、兼容投影、命理关系实例和报告章节所有权等项目契约，不适合进入跨项目全局案例库。正文只保存脱敏结构和审计方法，不保存用户出生信息、生产报告、密钥或外部账户数据。
