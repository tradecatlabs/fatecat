# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None.

# Task Package Status Table
| Node | Parent | Depth | Depends On | Parallelizable | Status | Evidence | Blocker | Notes |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | Markdown gate scope 和 schema 口径已更新。 | - | contract |
| TP-01.01 | TP-01 | 2 | - | No | Done | scope 覆盖同步、标准异步、Web 异步。 | - | scope |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | report schema 增加 requiredMarkdownResultFields 与 snapshotGate fields。 | - | schema |
| TP-02 | ROOT | 1 | TP-01 | No | Done | helper 已实现。 | - | helper |
| TP-02.01 | TP-02 | 2 | TP-01.02 | No | Done | Markdown policy helper 单测通过。 | - | policy |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | Markdown snapshot helper 单测通过。 | - | snapshot |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 三条路径已接入。 | - | integration |
| TP-03.01 | TP-03 | 2 | TP-02.02 | No | Done | 同步 Markdown API 返回 gate。 | - | sync api |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | 标准异步 job result 返回 gate。 | - | standard job |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | Web 异步 job result 返回 gate。 | - | web job |
| TP-04 | ROOT | 1 | TP-03 | No | Done | tests/docs updated。 | - | tests/docs |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | 组合回归 22 passed。 | - | tests |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | API 文档、100% 计划、report schema 同步。 | - | docs |
| TP-05 | ROOT | 1 | TP-04 | No | Done | local gates passed。 | - | validation |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Done | quick CI 68 passed；governance strict PASS；diff check PASS。 | - | gates |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | closeout validator 和全任务树 validator 均通过。 | - | closeout |

# Blockers
- None。

# Runtime State
- Phase: SPEC/PLAN
- External connectivity: 外部连通验证待执行。
- Git: 当前工作树已有 0009-0015 未提交改动；本任务不提交、不推送。

# Evidence Log
- `git status --short --branch`：`main...origin/main`，有 0009-0015 未提交和未跟踪文件。
- `materialize_task_docs.py --task-id 0016 ...`：骨架生成成功，INIT validation ok。
- `validate_task_docs.py --phase decompose`：首次失败，PLAN 缺少“不得跳过 gate”；已修复。
- `validate_task_docs.py --phase decompose`：通过。
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy or snapshot or report'`：4 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown or job or web'`：首次失败，紫微 Markdown 风险边界句“不输出确定未来”触发字面误报；已将 Markdown helper 加入否定上下文处理，generic scanner 保持严格。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown or job or web'`：13 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or snapshot or report or markdown or job or web'`：22 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown and gate'`：3 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'job and gate'`：2 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'web and gate'`：1 passed。
- `.venv/bin/ruff check ...`：All checks passed。
- `.venv/bin/ruff format --check ...`：11 files already formatted。
- `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core`：Success, 69 source files。
- `bash scripts/local-ci.sh --profile quick`：PASS，focused regression 68 passed。
- `rg -n "policyGate|snapshotGate|Markdown 正文" docs/reference-materials contracts/fate/capabilities governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates`：输出覆盖 schema、API 文档、roadmap 和 0016 文档。
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`：PASS，issue_count 0。
- `validate_task_docs.py --phase decompose`：通过。
- `git diff --check`：PASS，无输出。
- `validate_task_docs.py --phase closeout`：通过。
- `validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`：16/16 PASS。
- `git diff --check`：最终复跑 PASS，无输出。
