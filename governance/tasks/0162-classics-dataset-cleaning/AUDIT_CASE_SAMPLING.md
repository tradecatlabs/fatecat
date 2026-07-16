# Audit Case Sampling Decision

- Source: governance/tasks/0162-classics-dataset-cleaning
- Fixed Problem: 初版验证器只校验 artifact hash 和记录字段，无法拒绝“篡改 passage 后同步重算所有 hash”的语义血缘错误；现已增加 passage/paragraph 文档归属、序号、范围和全文无损等价校验及负向回归。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: semantic_lineage_not_covered_by_integrity_hash
- Trigger Signals: checksum passed; manifest passed; derived dataset; passage lineage; self-consistent tampering
- Evidence: `tests/regression/test_classics_dataset_clean.py::test_validator_rejects_self_consistent_hashes_when_passage_content_breaks_lineage`；focused pytest 9 passed；真实 14 本 build/validate-only passed。
- No-Case Reason: 这是新数据管线首轮实现中的局部校验缺口，已由数据契约、专用负向测试和现有 completion-verification/test-quality 审查面完整覆盖；当前没有跨任务复发证据，新增全局或项目案例会重复现有门禁。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
