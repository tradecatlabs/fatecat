# Planning Summary
目标终态是“原文不可变、派生数据可重建、每个切片可回源、版权状态不被清洗过程放宽”。本轮只完成最小可运行的 canonical 典籍清洗闭环。
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`。

# Lifecycle Gates
1. 所有阶段必须按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 顺序闭合，不得跳过 gate。
2. SPEC：输入范围、输出 schema、版权与隐私边界明确。
3. PLAN：稳定 ID、规范化、切片、重复和 manifest 算法可解释。
4. BUILD：实现清洗器，不引入第三方依赖。
5. TEST：fixture 单测、真实 14 本生成和数据门禁。
6. REVIEW：检查数据损失、血缘、版权 overclaim 和文档漂移。
7. SHIP：只提交工具、契约、测试和文档；本地正文不提交。

# Simplest Path
使用 Python 标准库完成 NFC、控制字符检查、空白规范化、段落和句界切片、SHA-256、NDJSON、重复统计和 manifest；不引入数据库、向量库、分词器或 RAG 框架。

# Split Strategy
- TP-01 先锁 contract，防止实现阶段改变边界。
- TP-02/TP-03 形成可独立测试的工具切片。
- TP-04 只生成本地派生资产。
- TP-05 统一审查和交付。

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01 |
| 2 | TP-02 |
| 3 | TP-03 |
| 4 | TP-04 |
| 5 | TP-05 |

# Runtime Workflow Contract
- 输入：canonical TXT、`source_manifest.tsv`、`copyright_review.tsv`。
- 输出：`documents.ndjson`、`paragraphs.ndjson`、`passages.ndjson`、`duplicates.ndjson`、`quality-report.json`、`manifest.json`、`files.sha256`。
- 副作用：仅写显式 `--output` 目录；拒绝把输出放入输入目录。
- 重试：输出写临时目录，验证完成后原子替换目标目录。

# Next Executable Leaves
- 无；全部节点已完成。

# Dependency Graph
`TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05`

# Rollback Protocol
- 删除新增工具、契约和测试即可回滚 tracked 变更。
- 本地派生数据集可直接删除后重建，canonical TXT 不受影响。
- 不使用 `git reset --hard`、`git checkout --` 或其他破坏性命令。
