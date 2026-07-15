# Audit Case Sampling Decision

- Source: governance/tasks/0159-suanzhun-content-corpus-crawl
- Fixed Problem: 详情 URL 分类器静默拒绝 `_N.html` 续页，完整性验证器又只检查同一分类器已接受的 frontier，导致 756 个可访问页面缺失时仍报告 PASS；元数据扫描同时越过正文边界污染 3 条作者字段。
- Decision: promoted-to-gate
- Case ID: CASE-0001
- Case Path:
- Gate Path: governance/architecture-gates/rules/GATE-0002-抓取完整性不得与发现规则共因失明.md
- Root Cause Class: shared_discovery_validation_blindness
- Trigger Signals: crawler completeness pass, pagination suffix, raw href rejected by classifier, frontier-only validation, false completion claim
- Evidence: `DEBUG.md` 的 E1/E2；修复前 5 项预期 RED；修复后 15 passed；756/756 续页 done；4100 个物理详情页、3344 篇逻辑文章、分页缺口、原始 href 漏入 frontier 和 pending resources 均为 0；`files.sha256` 11046 项通过。
- No-Case Reason: 不适用；全局 `CASE-0001/0003/0008` 提供完成声明与证据漂移审查问题，本项目另以可机械检测的 GATE-0002 固化站点采集共因失明条件，避免重复创建全局案例。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
