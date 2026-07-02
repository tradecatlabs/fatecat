# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None.

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 评测入口边界已盘点。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 已确认 registry 与现有 scripts/tests。 | - | - |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | 任务文档已回填，validator 已通过。 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 本地 runner 已落地。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.02 | No | Done | `scripts/run-evaluations.py` 与 `.sh` 已新增。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | 选择器、白名单、dry-run、summary JSON 已实现。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | registry/schema/AGENTS 已同步 runner 边界。 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | runner 与 contract tests 已补。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | `test_evaluation_runner.py` 已新增并通过。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | capability/API contract tests 已更新并通过。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | `scripts/local-ci.sh` 已纳入 runner focused test。 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | docs/roadmap 已同步。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | API 接入文档已新增 runner 命令。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | 100% 路线图区分最小集与扩展集。 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | Done | 验证收口完成。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Done | runner 实跑通过；quick CI 77 passed。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | closeout validator、全任务树 validator 和 closeout packet 已通过。 | - | - |

# Blockers
- 无当前代码阻塞。
- 外部连通验证待执行：外部模型 eval、真实 Bot、真实公网 API、远端 CI 状态同步、nightly/dashboard。

# Runtime State
## 2026-07-02
- 已新增本地 EvaluationRun runner、测试、registry metadata、schema summary fields、文档和路线图更新。
- runner dry-run、focused tests、真实 `run.solar_terms_golden`、ruff、format、quick CI 均已通过。

# Evidence Log
- `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/schemas/evaluation-run.schema.json >/dev/null`：PASS。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --phase decompose`：PASS。
- `bash scripts/run-evaluations.sh --list`：PASS，列出 `run.local_ci_quick`、`run.solar_terms_golden`、`run.mingli_bench_offline`。
- `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-dry-run.json && python3 -m json.tool /tmp/fatecat-evaluation-dry-run.json >/dev/null`：PASS，summary.status=`planned`。
- `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py`：5 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation`：3 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or runner'`：8 passed。
- `.venv/bin/ruff check scripts/run-evaluations.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`：PASS。
- `.venv/bin/ruff format --check scripts/run-evaluations.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`：PASS，4 files already formatted。
- `bash scripts/run-evaluations.sh --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-solar-terms.json`：PASS，summary.status=`passed`，`test_solar_terms_golden.py` 7 passed，用时 125.18s。
- `rg -n "run-evaluations|all-local-required|shell=True|requires_reference_repo" docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md`：PASS。
- `rg -n "本地 EvaluationRun runner|golden/eval 能跑本地最小集|扩展集" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`：PASS。
- `bash scripts/local-ci.sh --profile quick`：PASS，77 passed，evidence=/tmp/fatecat-local-ci-20260702085438。
- `git diff --check`：PASS，无输出。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --phase closeout`：PASS。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`：PASS，21/21 valid。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/build_task_closeout.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --out governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner/TASK_CLOSEOUT_PACKET.json --strict`：PASS，closeout_gate.ready=true。
