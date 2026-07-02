# Execution Checklist
[x] TP-01.01 | P0 | 盘点 runner、registry、roadmap 和 runtime ignore 边界 | Verify: `rg -n "EvaluationRun runner|summary history|diff policy|golden/eval|infra/runtime/local-state/exports" docs contracts scripts tests .gitignore governance/tasks/0022-measurement-infrastructure-wave4-evaluation-history-diff` | Gate: history/diff 与 dashboard/nightly 边界明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约与任务树 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 扩展 runner 结果历史留痕 | Verify: `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --record-history --history-dir /tmp/fatecat-evaluation-history --output-json /tmp/fatecat-evaluation-current.json` | Gate: history 文件和 latest.json 生成 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 Evaluation summary diff 工具 | Verify: `bash scripts/compare-evaluations.sh --baseline-json /tmp/fatecat-evaluation-history/latest.json --current-json /tmp/fatecat-evaluation-current.json --output-json /tmp/fatecat-evaluation-diff.json` | Gate: diff JSON 生成且 summary.status=passed | Parallelizable: No
[x] TP-02.03 | P0 | 新增 diff-policy 并登记到 registry/AGENTS | Verify: `python3 -m json.tool contracts/fate/evaluations/diff-policy.json >/dev/null && rg -n "diff-policy|compare-evaluations" contracts/fate/evaluations scripts/AGENTS.md` | Gate: policy、registry 和 AGENTS 同步 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 history/diff 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_history_diff.py` | Gate: history/latest、diff pass/fail 和 CLI 输出均覆盖 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 contract/API tests 与 quick CI | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation && rg -n "test_evaluation_history_diff.py" scripts/local-ci.sh` | Gate: diff policy metadata 和 quick CI 测试入口一致 | Parallelizable: No
[x] TP-03.03 | P0 | 更新文档与路线图 | Verify: `rg -n "record-history|compare-evaluations|diff-policy|summary history|golden/eval 具备本地 summary history" docs/reference-materials` | Gate: 文档区分已完成本地能力和未完成 dashboard/nightly | Parallelizable: No
[x] TP-04.01 | P0 | 修正任务 INDEX 状态漂移 | Verify: `rg -n "0017|0018|0019|0020|0021|0022" governance/tasks/INDEX.md` | Gate: 0017-0021 与各自 STATUS closeout 一致，0022 为当前任务 | Parallelizable: No
[x] TP-05.01 | P0 | 执行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过 | Parallelizable: No
[x] TP-05.02 | P0 | 回填 closeout 状态和验证证据 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0022 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
