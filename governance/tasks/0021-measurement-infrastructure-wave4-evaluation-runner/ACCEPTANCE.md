# Task-Level Acceptance
- `scripts/run-evaluations.sh --dry-run --all-local-required` 可生成 summary JSON。
- `scripts/run-evaluations.sh --run-id run.solar_terms_golden` 可真实执行节气 golden regression。
- runner 拒绝非白名单命令和 shell 拼接语法。
- `/evaluations` 文档明确 API 只发现资源，不启动评测。
- quick CI 覆盖 runner 测试，且任务 closeout validators 通过。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/schemas/evaluation-run.schema.json >/dev/null` |
| 任务文档 decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --phase decompose` |
| runner dry-run | `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-dry-run.json` |
| runner 实跑 | `bash scripts/run-evaluations.sh --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-solar-terms.json` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or runner'` |
| ruff | `.venv/bin/ruff check scripts/run-evaluations.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| format | `.venv/bin/ruff format --check scripts/run-evaluations.py tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- 检查 runner 没有 `shell=True`。
- 检查命令白名单只允许 `bash scripts/*.sh` 与 `python -m pytest`。
- 检查 summary JSON 不保存 benchmark answer、用户样例、token、secret、DSN 或生产路径。
- 检查 docs 没有把本地 runner 夸大成 dashboard/nightly/远端 CI。

# Runtime Verification Gate
- 本地 dry-run 与实际 `run.solar_terms_golden` 必须有真实输出文件。
- quick CI 必须通过，或者失败原因必须明确区分环境问题与代码问题。
- `requires_reference_repo` run 未显式授权时必须跳过。

# Ship Readiness
- 当前任务完成后可声明：EvaluationRun 具备本地最小集执行器。
- 不可声明：完整评测平台、历史趋势、跨 commit diff、nightly 扩展集、外部模型 eval 或远端 CI 已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现有 registry 与 scripts 被盘点，任务文档无占位符。 |
| TP-02 | runner 可选择、校验、执行并输出 summary JSON。 |
| TP-03 | 安全白名单、registry metadata、API payload 和 quick CI 断言完成。 |
| TP-04 | API 接入文档与 100% 路线图同步。 |
| TP-05 | 验证命令和任务 closeout 有真实证据。 |

# Anti-Goals
- 不得执行外部 live token、Bot、公网 API 或生产数据库验证。
- 不得把 optional benchmark 变成默认 release gate。
- 不得把 benchmark 标准答案或真实用户输入写入生产 provider。
