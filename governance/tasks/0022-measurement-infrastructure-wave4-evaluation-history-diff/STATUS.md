# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None.

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | history/diff 缺口已确认。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 已盘点 roadmap、runner、registry 与 ignore 边界。 | - | - |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | 任务文档已回填，待 validator 复核。 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | history/diff 能力已落地。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.02 | No | Done | `--record-history` 与 `history/latest.json` 已实现。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | `scripts/compare-evaluations.py` 与 `.sh` 已新增。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | `diff-policy.json` 与 registry/AGENTS 已同步。 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | tests/docs 已同步。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | `test_evaluation_history_diff.py` 已新增并通过。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | capability/API tests 与 quick CI 已更新。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | API 文档与 100% 路线图已同步。 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | 治理一致性修复已完成。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | 0017-0020 INDEX 状态已按 STATUS 修正。 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | Done | 验证收口完成。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-04.01 | No | Done | quick CI 81 passed；diff check 通过。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | closeout 状态已回填，待 validator 复核。 | - | - |

# Blockers
- 无当前代码阻塞。
- 外部连通验证待执行：dashboard、nightly、远端 CI 同步、外部模型 eval、生产 Bot/API live。

# Runtime State
## 2026-07-02
- 已新增本地 Evaluation summary history/latest、diff 工具、diff policy、回归测试、文档和路线图更新。
- quick CI、任务 validators 和 closeout packet 已通过。

# Evidence Log
- `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/diff-policy.json >/dev/null`：PASS。
- `.venv/bin/python -m pytest -q tests/regression/test_evaluation_history_diff.py`：4 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation`：3 passed。
- `rm -rf /tmp/fatecat-evaluation-history && bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --record-history --history-dir /tmp/fatecat-evaluation-history --output-json /tmp/fatecat-evaluation-current.json && bash scripts/compare-evaluations.sh --baseline-json /tmp/fatecat-evaluation-history/latest.json --current-json /tmp/fatecat-evaluation-current.json --output-json /tmp/fatecat-evaluation-diff.json`：PASS，diff summary.status=`passed`。
- `.venv/bin/python -m pytest -q tests/regression/test_evaluation_history_diff.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or history or diff or runner'`：12 passed。
- `.venv/bin/ruff check scripts/run-evaluations.py scripts/compare-evaluations.py tests/regression/test_evaluation_history_diff.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`：PASS。
- `.venv/bin/ruff format --check scripts/run-evaluations.py scripts/compare-evaluations.py tests/regression/test_evaluation_history_diff.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`：PASS。
- `bash scripts/local-ci.sh --profile quick`：PASS，81 passed，evidence=/tmp/fatecat-local-ci-20260702090721。
- `git diff --check`：PASS，无输出。
