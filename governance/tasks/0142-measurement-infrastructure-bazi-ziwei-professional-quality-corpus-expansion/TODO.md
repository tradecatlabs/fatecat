# Execution Checklist

[x] TP-01 | P0 | 新增 professional quality rubric 并接入 core-quality manifest、report diff policy、evaluation registry | Verify: JSON parse + core-quality gate | Gate: rubric dimensionCount>=8 and forbidden claims present | Parallelizable: Yes
[x] TP-02 | P0 | 扩展八字/紫微匿名 golden corpus | Verify: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json` | Gate: totalCaseCount>=340, ziwei basic/depth>=12, bazi statement>=8 | Parallelizable: Yes
[x] TP-03 | P0 | 加固 core-quality gate 与 regression tests | Verify: `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Gate: 53 passed | Parallelizable: No
[x] TP-04 | P0 | 同步评测目录说明和任务包 closeout | Verify: placeholder scan + docs review | Gate: no template placeholders in 0142 task package | Parallelizable: No
[x] TP-05 | P0 | 执行最终验证并准备提交 | Verify: JSON parse, core-quality gate, L4 smoke, pytest, task docs validation | Gate: all pass before git commit | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
