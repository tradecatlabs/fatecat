# Task-Level Acceptance
- `report.schema.json` 存在并被 schema refs 暴露。
- `output.schema.json` requiredFields 包含 `report`。
- `evidence.schema.json` 声明 `evidenceRefs`。
- capability calculate 响应包含 `report.resourceType=Report`。
- report envelope 包含 profile、formats、sections、evidenceRefs、links、metadata、risk。
- 原始 `data/evidence/risk/metadata` 字段保持不变。
- 文档明确完整 snapshot gate 后续实现。

# Validation Plan
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'report or capability or metadata or openapi'`
- `.venv/bin/ruff check ...`
- `.venv/bin/ruff format --check ...`
- `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core`
- `bash scripts/local-ci.sh --profile quick`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`
- `git diff --check`

# Review Gate
- 不得重写 Markdown 结构。
- 不得删除旧 API 字段。
- evidenceRefs 不得替代原始 evidence。
- 不得声明 forbidden claims scanner 或 snapshot gate 已完成。

# Runtime Verification Gate
- 本轮只验证本地 API response contract。
- 外部连通验证待执行：真实域名、token、Bot、webhook、远程服务。

# Ship Readiness
- schema、API、tests、docs、task closeout 和本地门禁均通过后可 closeout。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | Report schema 可被测试读取。 |
| TP-01.02 | output/evidence/resource schema 同步。 |
| TP-02.01 | capability response 带 report envelope。 |
| TP-02.02 | schema refs 和 `/reports` 暴露 report schema。 |
| TP-03.01 | API regression 覆盖 report envelope。 |
| TP-03.02 | docs/roadmap 同步。 |
| TP-04.01 | 本地门禁通过。 |
| TP-04.02 | 任务树 closeout 通过。 |

# Anti-Goals
- 不得修改报告内容生成算法。
- 不得虚构证据
- 不得越权补全未确认信息
