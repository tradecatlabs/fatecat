# Planning Summary
目标终态是 canonical 原文、结构策略、语义段落和检索 passage 四层分离：原文不可变，结构选择可重建，目录可查询但不污染检索，passage 永不跨章节。

# Lifecycle Gates
所有阶段按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 执行，不得跳过 gate。
1. SPEC：用 v2 指标和源文件行号确认问题。
2. PLAN：先升级契约和 source-hash 结构策略。
3. BUILD：只增强现有 cleaner，不建平行实现。
4. TEST：合成 red/green 与真实 14 本回归。
5. REVIEW：正确性、知识资产、复杂度、性能和文档漂移深审。
6. SHIP：本地提交，不自动 push。

# Simplest Path
使用标准库状态机将物理行组合为语义段落；目录范围由现有 policy 显式声明；passage builder 在 heading path 变化时 flush。无需分词、NLP 模型或向量数据库。

# Split Strategy
- TP-01 先锁 schema 和 policy，防止实现偷偷猜目录。
- TP-02 只负责语义段落与标题层级。
- TP-03 只负责检索切片和验证器。
- TP-04 用真实语料证明质量和无损。
- TP-05 在新鲜 Quick CI 后关闭任务。

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01 |
| 2 | TP-02 |
| 3 | TP-03 |
| 4 | TP-04 |
| 5 | TP-05 |

# Runtime Workflow Contract
- 输入：14 本 canonical TXT、source/copyright manifest、source-hash curation policy。
- 输出：v3 documents/paragraphs/passages/duplicates/exclusions/review queue/quality/manifest/checksums。
- 副作用：原子替换 ignored v3 输出目录。
- 失败：hash、结构范围、语义回放、heading 边界或权限不变量不满足即终止。

# Next Executable Leaves
- 无；全部节点已完成。

# Dependency Graph
`TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05`

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
