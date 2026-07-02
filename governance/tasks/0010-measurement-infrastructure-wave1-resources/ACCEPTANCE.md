# Task-Level Acceptance
- `contracts/fate/capabilities/schemas/resource.schema.json` 存在并定义核心资源类型。
- `contracts/fate/capabilities/schemas/error.schema.json` 和 `errors.json` 存在。
- `/capabilities/{capability_id}` 返回单个 capability 资源详情。
- `/errors` 返回标准错误码字典。
- OpenAPI 暴露新入口。
- API 接入文档同步。
- 本地门禁通过。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 定向回归 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error'` |
| Lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| Format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| Type | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` |
| Quick CI | `bash scripts/local-ci.sh --profile quick` |
| Governance | `python3 governance/tools/validate_governance_package.py --project-root . --strict` |
| Task docs | `validate_task_docs.py --phase closeout`、`validate_tasks_tree.py --phase auto` |
| Whitespace | `git diff --check` |

# Review Gate
- 确认没有改命理算法。
- 确认没有改变默认 Markdown 结构。
- 确认 planned capability 仍只可发现不可执行。
- 确认错误码不包含 secret 或外部敏感值。

# Runtime Verification Gate
- `/capabilities/bazi`、`/api/v1/capabilities/liuyao`、`/errors` 由 API contract tests 覆盖。
- `/openapi.json` 由 API contract tests 覆盖。

# Ship Readiness
- quick CI、governance strict、task validators、git diff check 通过后，任务可进入 closeout。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 机器契约存在并由协议测试覆盖 |
| TP-02 | API discovery 入口存在并由 API tests 覆盖 |
| TP-03 | 文档与回归同步 |
| TP-04 | 本地门禁和任务校验通过 |

# Anti-Goals
- 不实现 job 幂等与 provider protocol
- 不得虚构证据
- 不得越权补全未确认信息
