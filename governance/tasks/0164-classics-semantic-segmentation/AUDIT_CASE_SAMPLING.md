# Audit Case Sampling Decision

- Source: governance/tasks/0164-classics-semantic-segmentation
- Fixed Problem: 典籍清洗器曾将物理源行直接视为语义段落，并允许检索切片跨越标题边界和消费目录记录；v3 已重建语义段落、分离 navigation，并把 passage 限制在单一 heading path 内。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: physical-line-semantic-model-and-boundary-agnostic-chunking
- Trigger Signals: 大量异常短段；单一 passage 包含多个 heading path；目录项进入正文切片；重复证据消费非正文记录。
- Evidence: DEBUG.md H1-H3；17 项专项/data-gate 回归；真实 14 本双重重建；semantic replay、heading violation、navigation passage、lineage error 均为零；Quick CI 529 passed。
- No-Case Reason: 该问题只影响 FateCat 当前典籍派生管线，v3 schema、validator、真实数据回归和 data-supply-chain gate 已提供机械防回归；重复消费者风险另由现有项目案例 CASE-9001 覆盖，无需新增重叠案例。

## Reusable Audit Questions

- 文档摄取是否错误地把物理换行等同于语义段落？
- 检索切片是否在标题路径变化时强制结束？
- 目录、标题和其他导航记录是否被正文消费者误用？
- 派生段落能否按精确源行无损回放？

## Evidence Required

- 源行到语义段落的回放校验、标题边界负例、目录分流负例、真实语料双重确定性构建、canonical hash 不变证据和全量 CI。
