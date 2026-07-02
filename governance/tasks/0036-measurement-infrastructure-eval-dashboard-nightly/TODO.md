# Execution Checklist
[x] TP-01.01 | P0 | 盘点 EvaluationRun registry、runner、history、diff、workflow 和 roadmap 缺口 | Verify: `sed -n '1,260p' scripts/run-evaluations.py && sed -n '1,260p' scripts/compare-evaluations.py` | Gate: D6 缺 dashboard/nightly 明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 evaluation dashboard renderer 和 shell wrapper | Verify: `test -f scripts/evaluation-dashboard.py && test -f scripts/evaluation-dashboard.sh` | Gate: renderer 可从 summary/diff 生成 HTML | Parallelizable: No
[x] TP-02.02 | P0 | 新增 dashboard 回归测试和 dry-run smoke | Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_dashboard.py` | Gate: HTML escape、隐私边界和 CLI 输出通过 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 evaluation-nightly wrapper，串联 runner/history/diff/dashboard | Verify: `bash scripts/evaluation-nightly.sh --output-dir /tmp/fatecat-evaluation-nightly-2 --history-dir /tmp/fatecat-evaluation-history-2 --timeout-seconds 900` | Gate: 3 个 run 全部 passed | Parallelizable: No
[x] TP-03.02 | P1 | 新增 GitHub scheduled workflow artifact 入口 | Verify: `test -f .github/workflows/evaluation-nightly.yml` | Gate: workflow 只调用仓库脚本并上传 artifact | Parallelizable: No
[x] TP-04.01 | P0 | 登记 dashboard smoke EvaluationRun 和 dashboard/nightly metadata | Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py` | Gate: registry/API/protocol 可发现 | Parallelizable: No
[x] TP-04.02 | P0 | 接入 quick CI、API/protocol 测试和文档 | Verify: `jq '.summary' /tmp/fatecat-evaluation-nightly-2/summary.json` | Gate: `run.local_ci_quick` passed | Parallelizable: No
[x] TP-05.01 | P0 | 运行 focused validation、dashboard smoke、data supply chain gate、nightly wrapper | Verify: `bash scripts/evaluation-dashboard-smoke.sh --output-dir /tmp/fatecat-evaluation-dashboard-smoke` and `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate-0036.json` | Gate: smoke/gate/nightly all pass | Parallelizable: No
[x] TP-05.02 | P0 | 回填任务包并生成 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0036-measurement-infrastructure-eval-dashboard-nightly --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
