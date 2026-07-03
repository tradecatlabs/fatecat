# Execution Checklist

[x] TP-01.01 | P0 | 复核 0078/0079 后 runtime 缺口 | Verify: roadmap/runtime registry | Gate: 不把外部 live 写成完成 | Parallelizable: Yes
[x] TP-01.02 | P0 | 复核 runtime registry/local-ci/test 接线点 | Verify: file reads | Gate: 接线点明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 multi-replica runtime evidence contract | Verify: json.tool | Gate: no secrets | Parallelizable: No
[x] TP-02.02 | P0 | 新增反伪造负例 | Verify: pytest negative cases | Gate: fake evidence rejected | Parallelizable: No
[x] TP-03.01 | P0 | 更新 runtime backend registry 与 delivery registry | Verify: runtime-backend-gate | Gate: postgres still planned | Parallelizable: No
[x] TP-03.02 | P0 | 新增 gate scripts | Verify: py_compile + shell syntax | Gate: no external calls by default | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci artifact | Verify: local-ci quick | Gate: summary records artifact | Parallelizable: No
[x] TP-04.01 | P0 | 增加 regression tests | Verify: focused pytest | Gate: pass | Parallelizable: Yes
[x] TP-04.02 | P0 | 更新 docs/AGENTS | Verify: rg + tests | Gate: no overclaim | Parallelizable: Yes
[x] TP-05.01 | P0 | 运行验证 | Verify: focused gates + quick CI | Gate: pass | Parallelizable: No
[x] TP-05.02 | P0 | closeout/git/CI | Verify: task closeout; delivery closeout records post-commit git/CI | Gate: no pre-claim | Parallelizable: No
