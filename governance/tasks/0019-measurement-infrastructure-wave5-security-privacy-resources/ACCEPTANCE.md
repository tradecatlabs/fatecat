# Task-Level Acceptance
- `contracts/fate/security/registry.json` 可加载，所有 control 都是 `SecurityControl`。
- `contracts/fate/security/schemas/security-control.schema.json` 声明必填字段、控制类型、状态和外部连通枚举。
- `contracts/fate/capabilities/schemas/resource.schema.json` 包含 `SecurityControl` 和 `securityControlResourceFields`。
- `/security`、`/api/v1/security`、`/security/{control_id}`、`/api/v1/security/{control_id}` 可返回一致资源。
- `/metadata` 和 `/openapi.json` 暴露 security 入口。
- API 文档和 100% 路线图同步说明：资源发现不等于真实生产验证。
- 本地 focused tests、ruff、format、mypy、quick CI 和 task validators 通过。

# Validation Plan
| Item | Command | Expected |
| --- | --- | --- |
| task decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0019-measurement-infrastructure-wave5-security-privacy-resources --phase decompose` | PASS |
| focused contract | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'security or resource'` | PASS |
| focused API | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'security or metadata or openapi'` | PASS |
| combined focused | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'security or resource or metadata or openapi'` | PASS |
| lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` | PASS |
| format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` | PASS |
| type | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` | PASS |
| quick CI | `bash scripts/local-ci.sh --profile quick` | PASS |
| whitespace | `git diff --check` | PASS |
| task closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | PASS |

# Review Gate
- SecurityControl registry 不得包含真实 secret 值。
- `control.production_readiness_external` 不得写成已生产验证通过。
- `control.source_hygiene_gate` 不得被描述成完整 secret scanner。
- 任务文档必须明确 OAuth/OIDC、RBAC、retention、审计日志和专用 secret scanner 仍是后续项。

# Runtime Verification Gate
- 本任务只执行本地验证。
- 真实 API 域名、CORS、token、Bot live smoke、云端权限统一标注：外部连通验证待执行。

# Ship Readiness
- 本地 contract/API/quick CI 通过。
- 任务 closeout 和全任务树校验通过。
- 未提交改动需后续由 `auto-github` 或用户指令处理。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现有控制、脚本和边界已列入 CONTEXT。 |
| TP-02 | schema/registry/resource schema 完成并被测试覆盖。 |
| TP-03 | API、metadata、OpenAPI 完成并被测试覆盖。 |
| TP-04 | 文档和路线图同步，不夸大生产验证。 |
| TP-05 | 验证命令真实执行，证据写入 STATUS。 |

# Anti-Goals
- 不得修改 records 鉴权语义。
- 不得泄露真实凭证。
- 不得伪造外部生产验证结果。
