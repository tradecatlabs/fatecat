# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None.

# Task Package Status Table
| Node | Parent | Depth | Depends On | Parallelizable | Status | Evidence | Blocker | Notes |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 评测资源边界已明确。 | - | scope |
| TP-01.01 | TP-01 | 2 | - | No | Done | 已盘点 data-products、golden tests、MingLi runner。 | - | inventory |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | `validate_task_docs.py --phase decompose` 通过。 | - | docs |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 资源契约已落地。 | - | schema |
| TP-02.01 | TP-02 | 2 | TP-01.02 | No | Done | Dataset schema 已新增并由 protocol tests 覆盖。 | - | dataset |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | EvaluationRun schema 已新增并由 protocol tests 覆盖。 | - | eval |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | resource schema 已补 dataset/evaluation fields。 | - | resource |
| TP-03 | ROOT | 1 | TP-02 | No | Done | Evaluation registry 已落地。 | - | registry |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | 已登记 solar/bazi/ziwei golden Dataset。 | - | golden |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | 已登记 MingLi-Bench offline benchmark Dataset。 | - | benchmark |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | 已登记 local-ci、solar-terms、MingLi EvaluationRun。 | - | run |
| TP-04 | ROOT | 1 | TP-03 | No | Done | API 发现层已落地。 | - | api |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | `/evaluations` list/detail API focused tests 3 passed。 | - | endpoints |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | metadata/OpenAPI focused tests 3 passed。 | - | metadata |
| TP-05 | ROOT | 1 | TP-04 | No | Done | tests/docs 已同步。 | - | qa |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Done | protocol 2 passed；API 3 passed。 | - | tests |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | docs/contracts 评测资源检索覆盖已确认。 | - | docs |
| TP-06 | ROOT | 1 | TP-05 | No | Done | 验证收口完成。 | - | closeout |
| TP-06.01 | TP-06 | 2 | TP-05.02 | No | Done | quick CI 69 passed；ruff/mypy/diff check 通过。 | - | gates |
| TP-06.02 | TP-06 | 2 | TP-06.01 | No | Done | closeout validator PASS；全任务树 17/17 PASS。 | - | ship |

# Blockers
- 无当前阻塞。
- 外部连通验证待执行：真实外部模型评测、线上 CI、生产域名、真实 token、Bot live smoke。

# Runtime State
## 2026-07-02
- 已确认现有 `resource.schema.json` 只枚举 Dataset/EvaluationRun，缺字段契约和 API 资源。
- 已确认数据产品存在节气 1900-2030 golden、八字/紫微 golden、MingLi-Bench 离线 runner 与 quick CI 测试。
- 已新增 `contracts/fate/evaluations/`、Dataset/EvaluationRun schema、evaluation registry、`/evaluations` API、metadata links、API 文档和路线图。
- 本地 focused tests、ruff、format、mypy、quick CI 已通过。

# Evidence Log
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase decompose`：通过。
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset or resource'`：2 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'evaluation or metadata or openapi'`：3 passed。
- `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py`：All checks passed。
- `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py`：3 files already formatted。
- `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core`：Success, 69 source files。
- `git diff --check`：PASS，无输出。
- `rg -n "EvaluationRun|Dataset|/evaluations|评测资源" docs contracts governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources`：覆盖 API 文档、roadmap、contracts 和任务文档。
- `bash scripts/local-ci.sh --profile quick`：PASS，focused regression 69 passed，evidence=/tmp/fatecat-local-ci-20260702080000。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase closeout`：PASS。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`：17/17 PASS。
