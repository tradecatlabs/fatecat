# Task-Level Acceptance
- 14 本 canonical TXT 原文件哈希保持不变。
- 清洗器相同输入重复运行生成相同内容哈希和记录 ID。
- 每个 passage 可回指 document、source path、source hash 和 paragraph range。
- 输出明确标记 `review_required`、`distributionAllowed=false`、`productionUseAllowed=false`、`trainingUseAllowed=false`。
- 不自动删除原本/评注、重复命例或短干支行。

# Validation Plan
```bash
.venv/bin/python -m pytest -q tests/regression/test_classics_dataset_clean.py
.venv/bin/python scripts/classics-dataset-clean.py --input domains/fate-analysis/data-products/classics --output infra/runtime/local-state/exports/datasets/classics-clean-v1
.venv/bin/python scripts/classics-dataset-clean.py --validate-only --output infra/runtime/local-state/exports/datasets/classics-clean-v1
bash scripts/data-supply-chain-gate.sh
bash scripts/local-ci.sh --profile quick
```

# Review Gate
- Correctness：无内容丢失、ID 漂移、排序不稳定或坏 UTF-8 静默跳过。
- Privacy/license：无公开训练、生产或分发 overclaim。
- Architecture：数据正文留在 runtime，仓库只保存工具、契约、测试和治理证据。
- Performance：14 本处理为线性扫描；不把全文两两字符串比较做成 `O(total_chars²)`。

# Runtime Verification Gate
- `manifest.status=passed`。
- `documentCount=14`、`lineageErrorCount=0`、`invalidUtf8Count=0`。
- 每个输出文件出现在 `files.sha256`。

# Ship Readiness
- 本期可提交：工具、契约、测试、文档和任务证据。
- 本期不可提交：清洗正文、算准网正文、raw PDF/TXT 和私有案例。
- 本期不可声明：可公开训练、专业正确性已验证或版权已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | contract 与版权边界通过 JSON/文档检查 |
| TP-02 | fixture 两次运行输出哈希一致 |
| TP-03 | focused regression 通过，AGENTS/README 同步 |
| TP-04 | 14 本真实生成和 validate-only 通过 |
| TP-05 | review、quick CI、任务文档和 Git 边界通过 |

# Anti-Goals
- 不得覆盖 canonical TXT 或更改其 hash
- 不得虚构证据
- 不得把清洗结果直接写成训练集、公开数据集或专家答案
- 不得处理算准网、raw、Gem 合并包和用户报告
