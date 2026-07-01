# Task-Level Acceptance
- `/metadata` 暴露开发者入口、隐私策略和生产门禁。
- `/openapi.json` 可发现 `/metadata`、`/capabilities`、`/capabilities/{capability_id}/calculate`、`/reports`。
- registry 强制 production/planned 准入不变量。
- 文档说明 capability 调用、报告入口、错误、隐私和本地验证。
- 本地测试和治理门禁真实执行，不伪造外部生产验证。

# Validation Plan
| 验证 | 命令 |
| --- | --- |
| 定向回归 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi'` |
| Lint | `.venv/bin/ruff check ...` |
| Format | `.venv/bin/ruff format --check ...` |
| Type | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` |
| Quick CI | `bash scripts/local-ci.sh --profile quick` |
| Governance | `python3 governance/tools/validate_governance_package.py --project-root . --strict` |
| Task docs | `validate_task_docs.py`、`validate_tasks_tree.py` |
| Git hygiene | `git diff --check` |

# Review Gate
- 不新增业务模块。
- 不改变默认 Markdown 体系。
- 不引入真实 secret 或非北京真实地区公开示例。
- 不把外部生产连通说成已验证。

# Runtime Verification Gate
- `/ready` 通过 registry 加载校验。
- API contract test 覆盖 discovery 和 OpenAPI。
- 生产域名、真实 token、Bot live smoke：外部连通验证待执行。

# Ship Readiness
- quick CI、governance strict、task docs validator、git diff hygiene 全部通过后才提交。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | `/metadata` 和文档可作为开发者接入入口 |
| TP-02 | registry 对错误 capability 配置能 fail fast |
| TP-03 | 本地门禁通过，提交推送后任务关闭 |

# Anti-Goals
- 不得新增预测体系业务实现
- 不得虚构证据
- 不得越权补全未确认信息
