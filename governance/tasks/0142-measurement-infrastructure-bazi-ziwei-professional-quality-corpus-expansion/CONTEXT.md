# Repo Evidence

| Evidence | Path / Command |
| --- | --- |
| Core corpus manifest | `contracts/fate/evaluations/core-quality-corpus.json` |
| Report diff policy | `contracts/fate/evaluations/report-diff-policy.json` |
| Professional rubric | `contracts/fate/evaluations/professional-quality-rubric.json` |
| Evaluation registry | `contracts/fate/evaluations/registry.json` |
| Bazi statement fixture | `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` |
| Ziwei basic fixture | `domains/fate-analysis/data-products/ziwei/golden/cases.json` |
| Ziwei rule depth fixture | `domains/fate-analysis/data-products/ziwei/golden/rule_depth_cases.json` |
| Core-quality gate | `scripts/core-quality-corpus-gate.py` and `scripts/core-quality-corpus-gate.sh` |
| Regression tests | `tests/regression/test_core_quality_corpus_gate.py`, `tests/regression/test_bazi_statement_golden.py`, `tests/regression/test_bazi_ziwei_rule_depth.py`, `tests/regression/test_bazi_ziwei_l4_golden_smoke.py` |

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| 不改生产算法 | Only evaluation contracts, fixtures, gates, tests and docs changed. |
| 不保存真实资料 | All new cases use `birthPlace=北京` and `name=测试样本`. |
| 不保存完整报告正文 | report diff remains summary-only; forbidden fields include markdown/content/body/fullReport/reportText. |
| 不宣称 100% | rubric forbids 100% prediction/professional claims and keeps human review required. |
| 复用现有能力 | Existing `CapabilityExecutor`, golden fixtures and gate scripts reused. |
| 可本地复核 | JSON parse, core-quality gate, L4 smoke and pytest commands are reproducible locally. |

# Change Boundary

In boundary:

- `contracts/fate/evaluations/*`
- `domains/fate-analysis/data-products/bazi/golden/statement_cases.json`
- `domains/fate-analysis/data-products/ziwei/golden/cases.json`
- `domains/fate-analysis/data-products/ziwei/golden/rule_depth_cases.json`
- `scripts/core-quality-corpus-gate.py`
- selected regression tests
- `contracts/fate/evaluations/AGENTS.md`
- `governance/tasks/0142-*` and `governance/tasks/INDEX.md`

Out of boundary:

- production provider algorithms
- Web/API/Bot delivery behavior
- external live production validation
- real user corpus or expert identity records
- dependency/vendor/supply-chain changes

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fixture expected values drift from executor | Regression failures or false confidence | New samples are validated by `test_bazi_ziwei_rule_depth.py` and statement golden tests. |
| Rubric mistaken as completed expert review | Overclaim risk | `humanReview.status=required_before_external_claim`; limitations and forbidden claims are tested. |
| Evaluation fixture leaks into production | Incorrect runtime dependency | Manifest/rubric declare `evaluation_only`; task does not modify provider code. |
| Report diff stores full report | Privacy and artifact risk | report diff forbidden fields remain gated by core-quality tests. |
| Sample expansion still not enough for real accuracy | Professional quality overclaim | Task explicitly states it is not real case accuracy proof; future real corpus/expert review remains separate. |

# Assumptions and Falsification

| Assumption | Falsifier |
| --- | --- |
| Current executor output is the right source for new synthetic golden expected fields | Regression tests fail after executing `CapabilityExecutor` on the same inputs. |
| Existing core-quality gate is the right place to enforce rubric | Gate cannot validate rubric/policy/registry together or requires separate runtime state. |
| Synthetic Beijing/test samples satisfy current privacy boundary | Any new case contains non-Beijing real location, real name, secret, DSN or production path. |
| Local quality slice can close without production live | User requests live deployment proof or production credential validation in this task. |

# Critical Ambiguities

- Real professional quality still requires external human review; this task only defines and gates the rubric.
- Real-world accuracy needs a legally usable, anonymized and reviewed case corpus; current synthetic fixtures are engineering regression samples.
- External production readiness remains separate from local evaluation readiness.

# Debug Evidence Contract

- 调试模式: Optional

If a gate fails:

1. Capture the failing command and exact assertion.
2. Identify whether failure is contract drift, fixture drift, privacy violation or production-boundary violation.
3. Fix the smallest affected contract/fixture/test.
4. Rerun the failed command plus `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json`.

# Task Package Context Map

| TP | Context |
| --- | --- |
| TP-01 | Contract layer: rubric, manifest, policy, registry. |
| TP-02 | Data product layer: bazi/ziwei anonymous golden fixtures. |
| TP-03 | Quality gate layer: core-quality script and regression tests. |
| TP-04 | Documentation layer: AGENTS and task package. |
| TP-05 | Release handoff layer: validation evidence and git state. |
