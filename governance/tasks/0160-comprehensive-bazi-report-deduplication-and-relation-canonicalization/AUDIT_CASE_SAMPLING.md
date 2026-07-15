# Audit Case Sampling Decision

- Source: governance/tasks/0160-comprehensive-bazi-report-deduplication-and-relation-canonicalization
- Fixed Problem: 综合八字报告的重复章节与重复神煞释义已删除；地支关系已收敛到 canonical 单一真相源，修复自关联、反向重复、遗漏消费者和跨进程顺序漂移。
- Decision: project-overlay
- Case ID: CASE-9001
- Case Path: governance/evidence/audit-cases/cases/CASE-9001-canonical-field-and-compatibility-projection-double-consumption/CASE.md
- Root Cause Class: canonical_field_and_compatibility_projection_double_consumption
- Trigger Signals: 同一字段由多个 renderer 消费；兼容字段参与独立渲染；同一规则由成熟数据源和硬编码算法并行计算；结构测试期待重复标题。
- Evidence: DEBUG.md E1-E10、FIELD_OWNERSHIP.md、CONSUMER_AUDIT.md、关系与报告 red/green 回归、多端语义 diff、跨哈希种子测试和干净补丁 quick CI。
- No-Case Reason: 不适用；该模式已进入项目 overlay，因其依赖 FateCat 私有字段和报告契约而不进入全局案例库。

## Reusable Audit Questions

- 同一业务概念是否存在多个计算真相源或兼容字段参与独立计算？
- 同一报告字段是否由多个章节 renderer 同时负责？
- 结构快照是否只验证“存在”，却把重复输出固化成正确契约？
- 对称关系是否使用 canonical 键去重，自关系是否验证了实例基数？

## Evidence Required

- 最小复现、字段所有权矩阵、关系边界 red/green、报告唯一性回归、多端 parity、专项 review 和最终 CI。
