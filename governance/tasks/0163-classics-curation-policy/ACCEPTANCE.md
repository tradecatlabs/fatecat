# Task-Level Acceptance
- 14 本 policy 覆盖且每项 source hash 与 manifest 一致。
- 渊海推广包装、ctext 整理说明和章节 URL 不进入 paragraph/passage。
- 被排除行保留行号、原因和 hash，可审计但不复制全文到 review queue。
- 原本/评注不去重，家族关系和 completeness issues 可查询。
- reviewed bibliography 默认为未核实，不把候选作者/底本写成事实。
- canonical TXT hash 不变，三项权限继续为 false。

# Validation Plan
```bash
.venv/bin/python -m pytest -q tests/regression/test_classics_dataset_clean.py
.venv/bin/python scripts/classics-dataset-clean.py
.venv/bin/python scripts/classics-dataset-clean.py --validate-only
bash scripts/data-supply-chain-gate.sh
bash scripts/local-ci.sh --profile quick
```

# Review Gate
- Correctness：正文选择无越界、无误删、无 source hash 漂移。
- Knowledge assets：canonical 原文和 review-required metadata 不被覆盖。
- Contract：observed/reviewed、role/family/completeness 和权限语义一致。
- Performance：仍为正文线性扫描；不引入模糊全文比对。

# Runtime Verification Gate
- 14/14、lineageErrorCount=0、invalidUtf8Count=0。
- 已确认 envelope/promotional markers 在 passages 中零命中。
- `excludedSourceLineCount` 与 policy 命中数一致。
- 连续重建 hash 稳定。

# Ship Readiness
- 可提交：policy/schema、清洗器、测试、文档、任务证据。
- 不可提交：ignored 派生正文、raw、外部抓取正文。
- 不可声明：版权已清、底本已校、书目已权威核验、训练/生产可用。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 所有问题有本地路径/行或 manifest 证据 |
| TP-02 | 14/14 hash-bound policy，schema/registry 通过 |
| TP-03 | policy fail closed，正文与元数据分离 |
| TP-04 | focused/real build/data gate 通过 |
| TP-05 | deep review、Quick CI、task strict 通过 |

# Anti-Goals
- 不修改 canonical TXT 或 source manifest hash。
- 不用关键词模型自动决定古文正文。
- 不虚构作者、年代、底本、版权和完整性结论。
- 不把被排除文本静默丢弃；必须留元数据证据。
