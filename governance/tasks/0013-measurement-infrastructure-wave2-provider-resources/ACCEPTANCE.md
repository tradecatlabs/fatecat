# Task-Level Acceptance
- `provider.schema.json` 存在并被 schema refs 暴露。
- `/providers` 返回 production provider 集合。
- `/providers/{provider_id}` 返回单个 Provider resource，包含 metadata、health、links。
- capability detail links 包含对应 provider 资源入口。
- OpenAPI 暴露 provider endpoints。
- 文档明确 provider health 只是本地进程内 adapter health。

# Validation Plan
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'provider or capability or metadata or openapi'`
- `.venv/bin/ruff check ...`
- `.venv/bin/ruff format --check ...`
- `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core`
- `bash scripts/local-ci.sh --profile quick`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`
- `git diff --check`

# Review Gate
- Provider endpoints 必须只读。
- planned capability 不得出现在 `/providers` production 集合。
- 不得把本地 health 夸大成外部连通。
- 文档不得声明生产实测已完成。

# Runtime Verification Gate
- 本轮只验证本地 API 和 OpenAPI。
- 外部连通验证待执行：真实域名、token、Bot、webhook、远程服务。

# Ship Readiness
- 代码、契约、文档、任务容器和本地门禁均通过后可 closeout。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | Provider schema 可被测试读取。 |
| TP-01.02 | schema refs 包含 provider。 |
| TP-02.01 | provider list/detail API 可用。 |
| TP-02.02 | capability resource links.provider 可用。 |
| TP-03.01 | API regression 覆盖 provider resource。 |
| TP-03.02 | API docs/roadmap 同步。 |
| TP-04.01 | 本地门禁通过。 |
| TP-04.02 | 任务树 closeout 通过。 |

# Anti-Goals
- 不得修改 provider 计算逻辑。
- 不得虚构证据
- 不得越权补全未确认信息
