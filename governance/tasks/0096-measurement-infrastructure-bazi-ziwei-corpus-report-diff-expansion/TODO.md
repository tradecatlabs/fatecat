# Execution Checklist
[x] TP-01.01 | P0 | 读取现有 corpus/report diff/gate/test | Verify: `sed` and `python3` fixture count inspection | Gate: weak spots identified without changing provider algorithm | Parallelizable: Yes
[x] TP-02.01 | P0 | 扩容紫微 basic fixture | Verify: `domains/fate-analysis/data-products/ziwei/golden/cases.json` caseCount=8 and coverageRequirements present | Gate: all samples 北京/测试样本 | Parallelizable: No
[x] TP-02.02 | P0 | 更新 core-quality manifest 与 report diff policy | Verify: JSON parse and contract diff | Gate: minZiweiGoldenCases=8 and structuralDiff.summaryOnly=true | Parallelizable: No
[x] TP-03.01 | P0 | 更新 core-quality gate | Verify: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-0096.json` | Gate: passed and totalCaseCount=329 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 regression tests | Verify: `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Gate: 5 passed | Parallelizable: No
[x] TP-04.01 | P0 | 更新 registry/AGENTS/roadmap/task docs | Verify: `rg` checks and task validator | Gate: docs reflect 0096 scope and no overclaim | Parallelizable: No
[x] TP-05.01 | P0 | 运行最终验证 | Verify: task closeout validator, diff check, focused tests | Gate: no placeholders, no whitespace errors | Parallelizable: No
