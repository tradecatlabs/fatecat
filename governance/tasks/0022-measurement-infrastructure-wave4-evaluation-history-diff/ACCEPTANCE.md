# Task-Level Acceptance
- `run-evaluations.sh --record-history` 可写 history 文件和 `latest.json`。
- `compare-evaluations.sh` 可比较两个 summary JSON，并按 `diff-policy.json` 输出机器可读 diff。
- diff policy 对新增失败、缺失 run、失败命令保持 0 容忍。
- quick CI 覆盖 `test_evaluation_history_diff.py`。
- API 文档和 roadmap 区分“本地 history/diff 已完成”和“dashboard/nightly 未完成”。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/diff-policy.json >/dev/null` |
| CLI smoke | `rm -rf /tmp/fatecat-evaluation-history && bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --record-history --history-dir /tmp/fatecat-evaluation-history --output-json /tmp/fatecat-evaluation-current.json && bash scripts/compare-evaluations.sh --baseline-json /tmp/fatecat-evaluation-history/latest.json --current-json /tmp/fatecat-evaluation-current.json --output-json /tmp/fatecat-evaluation-diff.json` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_evaluation_history_diff.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or history or diff or runner'` |
| ruff | `.venv/bin/ruff check scripts/run-evaluations.py scripts/compare-evaluations.py tests/regression/test_evaluation_history_diff.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| format | `.venv/bin/ruff format --check scripts/run-evaluations.py scripts/compare-evaluations.py tests/regression/test_evaluation_history_diff.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- 检查 history 输出路径默认在 `.gitignore` 覆盖范围内。
- 检查 diff 不解析 stdout/stderr 正文，不保存标准答案或用户隐私。
- 检查 `diff-policy.json` 阈值为 0 容忍。
- 检查文档不宣称 dashboard/nightly/远端 CI 已完成。

# Runtime Verification Gate
- CLI smoke 必须生成 `/tmp/fatecat-evaluation-history/latest.json` 与 `/tmp/fatecat-evaluation-diff.json`。
- focused tests 与 quick CI 必须通过。
- 任务树 validator 必须 22/22 valid。

# Ship Readiness
- 当前任务完成后可声明：EvaluationRun 具备本地 history/latest 与 summary diff policy。
- 不可声明：长期结果数据库、dashboard、nightly、远端 CI 状态同步或外部模型 eval 已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口和边界已落盘。 |
| TP-02 | history、latest、diff tool、diff policy 已实现。 |
| TP-03 | tests/docs/quick CI 已同步。 |
| TP-04 | INDEX 与任务目录状态一致。 |
| TP-05 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不得把运行态 history 提交进 Git。
- 不得把 dry-run diff 伪装成真实评测通过。
- 不得执行外部 live token、Bot、公网 API 或生产数据库验证。
