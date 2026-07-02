# Task-Level Acceptance
- `scripts/export-openapi.sh` 可导出 OpenAPI JSON。
- OpenAPI 导出校验基础设施必备路径和 operationId 唯一性。
- `contracts/fate/developer/sandbox.json` 只包含北京/测试样本，不含真实 token、生产 URL 或报告正文。
- `scripts/developer-docs-smoke.sh` 可执行 sandbox fixture，并验证 curl/Python/Node/Agent 示例。
- quick CI 默认执行 developer docs smoke。
- focused regression 覆盖 OpenAPI 导出和 developer docs smoke。
- 文档明确本轮不是公网 sandbox token 服务、发布版 SDK 或开发者门户。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| sandbox JSON | `python3 -m json.tool contracts/fate/developer/sandbox.json >/dev/null` |
| shell syntax | `bash -n scripts/export-openapi.sh scripts/developer-docs-smoke.sh docs/reference-materials/developer/examples/curl-sandbox.sh` |
| Python compile | `python3 -m py_compile scripts/export-openapi.py scripts/developer-docs-smoke.py docs/reference-materials/developer/examples/python-client.py` |
| OpenAPI export | `bash scripts/export-openapi.sh --output /tmp/fatecat-openapi-0029.json && python3 -m json.tool /tmp/fatecat-openapi-0029.json >/dev/null` |
| developer docs smoke | `bash scripts/developer-docs-smoke.sh --output-json /tmp/fatecat-developer-docs-smoke-0029.json --openapi-json /tmp/fatecat-openapi-smoke-0029.json` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_developer_docs_smoke.py tests/regression/test_api_contracts.py -k 'developer_docs or openapi'` |
| ruff | `.venv/bin/python -m ruff check scripts/export-openapi.py scripts/developer-docs-smoke.py tests/regression/test_developer_docs_smoke.py docs/reference-materials/developer/examples/python-client.py` |
| format | `.venv/bin/python -m ruff format --check scripts/export-openapi.py scripts/developer-docs-smoke.py tests/regression/test_developer_docs_smoke.py docs/reference-materials/developer/examples/python-client.py` |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0029.json && python3 -m json.tool /tmp/fatecat-secret-scan-0029.json >/dev/null` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py` |

# Review Gate
- 示例不得包含真实 token、真实用户、生产域名或非北京真实地区。
- docs smoke 不得保存报告正文。
- 文档不得把本地 fixture 说成真实 sandbox token 服务。
- quick CI 失败时不得 closeout。
- OpenAPI 导出失败时不得只保留 `/openapi.json` 手动访问口径。

# Runtime Verification Gate
- `test_export_openapi_writes_required_schema` 必须通过。
- `test_developer_docs_smoke_executes_sandbox_and_examples` 必须通过。
- `developer-docs-smoke.sh` 必须返回 `status=passed`。

# Ship Readiness
- 当前任务完成后可声明：开发者接入具备本地 OpenAPI、sandbox fixture、示例和 docs smoke baseline。
- 不可声明：发布版 SDK、公网 sandbox token、开发者门户、生产开发者账号或固定输出 snapshot 已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现状、范围和风险已落盘。 |
| TP-02 | sandbox fixture 和四类示例已新增。 |
| TP-03 | OpenAPI 导出、docs smoke、回归测试和 quick CI 接入完成。 |
| TP-04 | 文档同步、quick CI、validators 和 closeout packet 通过。 |

# Anti-Goals
- 不发布 SDK 包。
- 不伪造真实 sandbox token。
- 不保存真实报告正文 fixture。
- 不接真实生产环境。
