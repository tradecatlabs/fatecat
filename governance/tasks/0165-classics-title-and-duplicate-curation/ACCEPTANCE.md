# Task-Level Acceptance
- 同一 document 的 `document_title` 数量不超过 1；重复书名不丢失并形成 heading 边界。
- exact paragraph group 必须分类为 `same_document_repetition`、`same_family_shared_text` 或 `cross_family_shared_text`。
- exact passage group 与 document overlap 使用同一可重算关系语义。
- quality report 的 review/duplicate summaries 与明细完全一致。
- canonical bytes/hash、正文 fingerprint、权限边界和 21 项 pending review 不变。

# Validation Plan
```bash
.venv/bin/python -m pytest -q tests/regression/test_classics_dataset_clean.py tests/regression/test_data_supply_chain_gate.py
.venv/bin/python scripts/classics-dataset-clean.py
.venv/bin/python scripts/classics-dataset-clean.py --validate-only
bash scripts/data-supply-chain-gate.sh
bash scripts/local-ci.sh --profile quick
```

# Review Gate
- Correctness：标题转换不丢字；关系分类由源记录重算；tamper 必须失败。
- Knowledge assets：分类不升级为书目、作者、底本或删除结论。
- Performance：保持 O(total chars + records + document pairs)，不引入逐记录全表查找。
- Future optimal：clean dataset 继续作为唯一派生管线，不新增 review sidecar 或 v4 空壳。

# Runtime Verification Gate
- `multipleDocumentTitleDocumentCount=0`。
- `duplicateRelationshipCounts` 精确等于 duplicates 明细。
- `reviewIssueTypeCounts`、`reviewSeverityCounts`、`reviewBlockCounts` 精确等于 21 项 review queue。
- semantic replay、heading violation、navigation passage、lineage error 均为 0。
- 连续两次构建聚合 hash 一致，canonical hash 不变。

# Ship Readiness
- 可提交：兼容性 schema 增量、owner cleaner、门禁、测试、文档与任务证据。
- 不可提交：ignored 派生正文、raw、外部下载文件或人工未确认结论。
- 不可声明：重复已去除、底本已核验、版权已清或数据可公开训练。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | red tests 证明多 title 和无分类问题 |
| TP-02 | title <=1 且重复书名变 heading |
| TP-03 | 三类关系和三组 review summary 可重算 |
| TP-04 | 真实 build/validate/data gate/确定性通过 |
| TP-05 | deep review、Quick CI、task strict、Git 边界通过 |

# Anti-Goals
- 不修改 canonical TXT。
- 不自动删除、合并或覆盖重复正文。
- 不把 same-family shared text 包装为权威版本谱系或传承方向。
- 不把 pending review 改成 resolved。
- 不新增平行 cleaner、数据集版本或依赖。
