# Audit Case Sampling Decision

- Source: governance/tasks/0165-classics-title-and-duplicate-curation
- Fixed Problem: 典籍清洗器曾将同一文档内重复出现的书名全部标为 document_title，并把同书重复、同家族共享文本和跨家族共享文本压成无关系语义的统一 duplicate evidence；现已实现标题唯一性、三类关系、可重算摘要和 tamper rejection。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: document_identity_boundary_and_duplicate_relation_collapse
- Trigger Signals: 单文档多个 document_title；重复书名出现在卷或分片边界；duplicate records 只有 action 而无 relationship；人工复核统计只能扫描明细获得。
- Evidence: 3 个 red failures；20 项 focused/data-gate 回归；真实 14 本重建；title 29 -> 11；duplicate relationship 407/46/31；data gate 355 checks；Quick CI 532 passed。
- No-Case Reason: 该问题属于 FateCat v3 典籍派生模型的项目内语义，现有 schema、owner validator、tamper 负例、真实数据回归和 data-supply-chain gate 已形成机械防回归；项目 CASE-9001 已覆盖 canonical 与派生消费者双轨风险，新增案例会重复现有保护。

## Reusable Audit Questions

- 文档身份记录是否在每个 document 内唯一，重复标题是否作为结构边界保留而不是删除？
- duplicate evidence 是否只陈述可重算的结构关系，而没有推断版本传承、引用方向或删除资格？
- quality summary 是否从明细重算并能拒绝自洽篡改？
- canonical、人工 review 状态和权限边界是否保持不变？

## Evidence Required

- 重复标题边界测试、三类 duplicate relationship 测试、validator tamper 负例、真实语料确定性重建、canonical hash、数据门禁和全量 CI。
