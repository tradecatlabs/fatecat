# Task-Level Acceptance
- `scripts/evaluation-dashboard.py/.sh` 存在，可从 EvaluationRun summary 与可选 diff 生成静态 HTML dashboard。
- Dashboard 不渲染 stdout/stderr tail、benchmark 标准答案、报告正文、真实 token、secret、DSN 或真实用户输入。
- `scripts/evaluation-dashboard-smoke.sh` 使用 dry-run summary 验证 dashboard artifact，并进入 quick CI。
- `scripts/evaluation-nightly.sh` 执行 releaseRequired EvaluationRun、history/latest、可选 diff 和 dashboard artifact。
- `.github/workflows/evaluation-nightly.yml` 存在，只调用仓库脚本并上传 artifact，不保存 secret、不自动部署。
- `contracts/fate/evaluations/registry.json` 登记 `run.evaluation_dashboard_smoke`、`dashboardCommand` 和 `nightlyCommand`。
- `contracts/fate/data-supply-chain/registry.json` 中 evaluation registry sha 与当前文件一致。
- API/protocol/runner/dashboard 回归测试通过。
- docs/AGENTS/roadmap 明确本轮是本地 dashboard/nightly baseline，远端 CI/current diff 和生产 live smoke 待 push 后执行。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| registry JSON syntax | `python3 -m json.tool contracts/fate/evaluations/registry.json >/tmp/fatecat-evaluations-registry.json` | Passed |
| shell syntax | `bash -n scripts/evaluation-dashboard.sh scripts/evaluation-dashboard-smoke.sh scripts/evaluation-nightly.sh scripts/local-ci.sh` | Passed |
| ruff check | `.venv/bin/python -m ruff check scripts/evaluation-dashboard.py tests/regression/test_evaluation_dashboard.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check scripts/evaluation-dashboard.py tests/regression/test_evaluation_dashboard.py` | Passed |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_evaluation_dashboard.py tests/regression/test_evaluation_runner.py tests/regression/test_evaluation_history_diff.py` | Passed; 11 passed |
| data supply chain gate | `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate-0036.json` | Passed; assets=8, classics=14, checks=162 |
| data supply chain pytest | `.venv/bin/python -m pytest -q tests/regression/test_data_supply_chain_gate.py` | Passed; 2 passed |
| dashboard smoke | `bash scripts/evaluation-dashboard-smoke.sh --output-dir /tmp/fatecat-evaluation-dashboard-smoke` | Passed; runCount=3 |
| nightly wrapper | `bash scripts/evaluation-nightly.sh --output-dir /tmp/fatecat-evaluation-nightly-2 --history-dir /tmp/fatecat-evaluation-history-2 --timeout-seconds 900` | Passed; 3/3 EvaluationRun passed |

# Review Gate
- Dashboard renderer uses HTML escaping for all dynamic fields.
- Dashboard renderer intentionally omits command output tails.
- Nightly wrapper still renders dashboard when evaluation/diff fails and exits non-zero after artifact generation.
- EvaluationRun command stays inside runner whitelist: `bash scripts/evaluation-dashboard-smoke.sh`.
- GitHub workflow uses checkout/setup-python/bootstrap, then repository script, then artifact upload with `if: always()`.
- Data supply chain manifest hash was updated after evaluation registry change and gate passed.

# Runtime Verification Gate
- Focused tests、dashboard smoke、data supply chain gate 和 nightly wrapper 已通过。
- `run.local_ci_quick` 在 nightly wrapper 中通过，durationMs=116687。
- `run.solar_terms_golden` 在 nightly wrapper 中通过，durationMs=127356。
- `run.evaluation_dashboard_smoke` 在 nightly wrapper 中通过，durationMs=80。
- 外部连通验证待执行：push 后 GitHub Actions run、真实生产 API/Bot live smoke、外部长期结果库和监控平台。

# Ship Readiness
- 当前本地 0036 切片可进入审计：脚本、registry、workflow、quick CI hook、文档和任务 closeout 均有本地证据。
- 不能声称生产 100%：缺远端当前 diff CI 证据、长期结果库、趋势 dashboard、告警和生产 live smoke。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | dashboard renderer、回归测试和 dry-run smoke 落地。 |
| TP-03 | nightly wrapper 和 GitHub scheduled workflow artifact 落地。 |
| TP-04 | registry、quick CI、AGENTS、API docs 和 roadmap 同步。 |
| TP-05 | focused validation、dashboard smoke、data supply chain gate、nightly wrapper 和 closeout 完成。 |

# Anti-Goals
- 不接外部监控平台。
- 不调用外部模型 API。
- 不把 benchmark 标准答案注入 production provider。
- 不展示 stdout/stderr tail、报告正文或真实凭证。
- 不声明远端 CI 或生产 live smoke 已完成。
