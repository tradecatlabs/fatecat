# Repo Evidence
| Evidence | Result |
| --- | --- |
| Current base HEAD | `e34418ca01dbae2f01a81a0c9bf3fc32e5615ef5` |
| 0095 plan | `governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md` selects Wave A Next-01 as next local task. |
| Existing core manifest | `contracts/fate/evaluations/core-quality-corpus.json` had 5 corpora and ziwei basic min count 4. |
| Existing report policy | `contracts/fate/evaluations/report-diff-policy.json` had policy/snapshot gates but no structuralDiff summary-only section. |
| Existing gate | `scripts/core-quality-corpus-gate.py` checked counts, privacy and registry links. |
| Existing tests | `tests/regression/test_core_quality_corpus_gate.py` expected 5 corpora and total 325+ cases. |

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| Privacy | Use only 北京/测试样本; no real user data. |
| Production boundary | Evaluation fixtures must not be read by production providers. |
| Report body | Store only structural summary policy; full report body forbidden. |
| Scope | No provider algorithm changes. |
| Evidence | Gate and focused pytest must pass. |

# Change Boundary
Allowed:
- `domains/fate-analysis/data-products/ziwei/golden/cases.json`
- `contracts/fate/evaluations/core-quality-corpus.json`
- `contracts/fate/evaluations/report-diff-policy.json`
- `contracts/fate/evaluations/registry.json`
- `scripts/core-quality-corpus-gate.py`
- `tests/regression/test_core_quality_corpus_gate.py`
- `contracts/fate/evaluations/AGENTS.md`
- `domains/fate-analysis/data-products/AGENTS.md`
- `scripts/AGENTS.md`
- `tests/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0096-measurement-infrastructure-bazi-ziwei-corpus-report-diff-expansion/`

Not allowed:
- 修改 production provider 算法。
- 保存完整报告正文。
- 使用真实用户样本、真实非北京地区、token、secret、DSN、webhook 或生产路径。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| 自生成 fixture 误读为专家命例 | 文档和 manifest 明确 synthetic anonymous fixture，不证明专家准确率。 |
| report diff 名称让人以为逐字锁正文 | `structuralDiff.summaryOnly=true` 且 forbidden stored fields 包含 `fullReport`、`reportText`。 |
| coverageTags 写了不检 | gate 校验 fixture 和 manifest required tags。 |
| 路线图编号漂移 | 0.11 表更新 0095/0096 真实含义，后续用 Next 表示未建任务。 |

# Assumptions and Falsification
- Assumption: 紫微 basic 的最弱环节是样本数和覆盖标签，不是 provider 算法。
- Falsifier: 若 L4 smoke 或 core-quality gate 因新增样本失败，说明 fixture 与当前 provider 输出不一致，不能 closeout。
- Assumption: summary-only report diff 是本轮足够边界。
- Falsifier: 若 gate 输出包含完整 `markdown`、`fullReport` 或 `reportText` 字段，本任务失败。

# Critical Ambiguities
- “全文 report diff”长期目标仍需要人工审定如何在不保存完整正文的情况下做结构化 diff。本轮选择 summary-only 结构策略，避免隐私和报告正文漂移问题。
- 八字 corpus 当前已有 300 个矩阵样本，本轮优先补紫微短板；八字后续仍需要更多规则深度/人审抽样。

# Debug Evidence Contract
- 调试模式: Optional

本任务不是 bugfix；若 gate/test 失败，则按 focused failure 升级为 debug-required。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | Existing contracts, fixture, gate and tests. |
| TP-02.01 | `ziwei/golden/cases.json` current provider guard output for additional synthetic Beijing samples. |
| TP-02.02 | `core-quality-corpus.json` and `report-diff-policy.json` thresholds/policy. |
| TP-03.01 | `core-quality-corpus-gate.py` validation logic. |
| TP-03.02 | `test_core_quality_corpus_gate.py` and L4 smoke regression. |
| TP-04.01 | registry, AGENTS and roadmap. |
| TP-05.01 | `/tmp/fatecat-core-quality-0096.json` and pytest output. |
