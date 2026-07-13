# Audit Case Sampling Decision

- Source: governance/tasks/0157-fatecat-geo-citation-authority
- Fixed Problem: FateCat 已可被机器发现，但缺少答案前置、正文与 Schema 一致的公开权威说明页，GitHub 仓库元数据为空。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: first-time-citation-authority-capability-gap
- Trigger Signals: 缺独立可引用主题页；缺可见 FAQ；GitHub description、homepage、topics 为空。
- Evidence: `public_discovery.py`、`tests/regression/test_geo_discovery.py`、`scripts/geo-audit.py`、GitHub API 回读。
- No-Case Reason: 本轮是首次建立引用权威层，不是 bug、重复失败或明确 debug 根因；现有 GEO 回归与 document drift 门禁可直接防回归。

## Reusable Audit Questions
- 结构化 FAQ 是否与用户可见正文逐项一致？
- capability 状态是否来自实时真相源而不是营销文案？
- GitHub 元数据是否只描述可验证的当前能力？

## Evidence Required
- 专项测试、quick CI、GitHub API 回读、HF runtime SHA 与线上 GEO audit。
