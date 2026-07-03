# Task-Level Acceptance
| 验收项 | 命令 / 证据 | 通过标准 |
| --- | --- | --- |
| 紫微 basic corpus 扩容 | `python3 -m json.tool domains/fate-analysis/data-products/ziwei/golden/cases.json` | `caseCount=8`，所有样本为北京/测试样本。 |
| manifest/policy 更新 | `python3 -m json.tool contracts/fate/evaluations/core-quality-corpus.json` and report policy | minZiwei=8，structuralDiff summary-only。 |
| core-quality gate | `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-0096.json` | passed，totalCaseCount=329。 |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | 5 passed。 |
| privacy gate | `bash scripts/check-privacy-fixtures.sh` | passed。 |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0096-final.json` | passed，findingCount=0。 |
| data supply chain | `bash scripts/data-supply-chain-gate.sh` | passed，assets=8，classics=14，checks=162。 |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0096-rerun` | passed，focused regression 267 passed。 |
| task docs | `validate_task_docs.py --phase closeout` | exit 0。 |

# Validation Plan
1. JSON parse changed contracts/fixtures.
2. Run core-quality corpus gate.
3. Run focused regression tests.
4. Run privacy fixture and secret scan gates.
5. Run data supply chain gate after fixture/registry hash changes.
6. Run quick local-ci before closeout.
7. Run task document validator.
8. Run `git diff --check`.

# Review Gate
- No provider algorithm change.
- No full report body stored.
- No real user sample or non-Beijing public fixture.
- No 100% professional accuracy claim.
- Existing L4 smoke still passes.

# Runtime Verification Gate
- Required local gate: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-0096.json`。
- Required regression: focused pytest listed above.
- External live verification: not required for this task.

# Ship Readiness
- 0096 can ship when focused gate/tests/docs validators pass.
- Quick local-ci has passed locally for this slice; live external gates remain outside scope.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Existing weak spots identified from real files. |
| TP-02.01 | Ziwei basic fixture has 8 anonymous Beijing cases and coverage requirements. |
| TP-02.02 | Core manifest and report diff policy enforce new threshold and summary-only policy. |
| TP-03.01 | Gate validates coverage tags and report diff structural policy. |
| TP-03.02 | Regression tests assert new gate behavior. |
| TP-04.01 | Registry, AGENTS, roadmap and task docs updated. |
| TP-05.01 | All required validators pass. |

# Anti-Goals
- 不改 production provider。
- 不保存完整报告正文。
- 不引入真实用户资料或 benchmark 标准答案。
