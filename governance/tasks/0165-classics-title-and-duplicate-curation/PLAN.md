# Planning Summary
目标终态是把“文档身份、章节边界、重复关系、人工复核”分开：标题记录唯一，重复文本完整保留但关系明确，所有摘要可从明细重算。

# Lifecycle Gates
所有阶段按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 执行，不得跳过 gate。

1. SPEC：锁定 29 titles、exact paragraph 404/46/28 duplicate split、21 review items 红证据。
2. PLAN：先定义兼容字段和关系枚举。
3. BUILD：只增强现有 cleaner 与 validator。
4. TEST：先合成 red/green，再跑真实 14 本。
5. REVIEW：知识资产边界、复杂度、性能和文档漂移审查。
6. SHIP：本地提交，不自动 push。

# Simplest Path
在段落状态机增加 `document_title_seen`；在现有 hash 分组阶段用 document map 一次分类；quality report 用 Counter 聚合。无需新脚本、NLP、数据库或删除策略。

# Split Strategy
- TP-01 锁契约和 red tests。
- TP-02 只修标题类型和 heading path。
- TP-03 只做关系和摘要。
- TP-04 锁真实数据与 validator。
- TP-05 完成交付证据。

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01 |
| 2 | TP-02 |
| 3 | TP-03 |
| 4 | TP-04 |
| 5 | TP-05 |

# Runtime Workflow Contract
- 输入：v3 contract、14 本 canonical、curation policy、source/copyright manifest。
- 输出：同一组 v3 文件，增加兼容字段和可重算摘要。
- 副作用：原子替换 ignored v3 目录；不写 canonical。
- 失败：多 title、关系漂移、摘要漂移、权限放宽或 fingerprint 不一致立即终止。

# Next Executable Leaves
- 无；TP-01 至 TP-05 已完成。

# Dependency Graph
`TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05`

# Rollback Protocol
- 回退本任务提交即可恢复 0164 的 v3 输出语义。
- ignored v3 可由上一 commit 的 cleaner 重建。
- canonical 和人工 review 状态从不参与回滚写入。
