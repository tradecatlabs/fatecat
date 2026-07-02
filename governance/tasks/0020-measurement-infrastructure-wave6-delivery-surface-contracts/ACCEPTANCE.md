# Task-Level Acceptance
- `contracts/fate/delivery/registry.json` 可加载，所有 surface 都是 `DeliverySurface`。
- `contracts/fate/delivery/schemas/delivery-surface.schema.json` 声明必填字段、surface 类型、状态和外部连通枚举。
- `contracts/fate/capabilities/schemas/resource.schema.json` 包含 `DeliverySurface` 和 `deliverySurfaceResourceFields`。
- `/surfaces`、`/api/v1/surfaces`、`/surfaces/{surface_id}`、`/api/v1/surfaces/{surface_id}` 可返回一致资源。
- `/metadata` 和 `/openapi.json` 暴露 surfaces 入口。
- API 文档和 100% 路线图同步说明：DeliverySurface 发现不等于所有端 live 生产验证。
- 本地 focused tests、ruff、format、mypy、quick CI 和 task validators 通过。

# Validation Plan
| Item | Command | Expected |
| --- | --- | --- |
| task decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0020-measurement-infrastructure-wave6-delivery-surface-contracts --phase decompose` | PASS |
| focused contract | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'surface or resource'` | PASS |
| focused API | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'surface or metadata or openapi'` | PASS |
| entrypoint consistency | `.venv/bin/python -m pytest -q tests/regression/test_entrypoint_consistency.py` | PASS |
| combined focused | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py tests/regression/test_entrypoint_consistency.py -k 'surface or resource or metadata or openapi or entrypoint'` | PASS |
| lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py tests/regression/test_entrypoint_consistency.py` | PASS |
| format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py tests/regression/test_entrypoint_consistency.py` | PASS |
| type | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` | PASS |
| quick CI | `bash scripts/local-ci.sh --profile quick` | PASS |
| whitespace | `git diff --check` | PASS |
| task closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | PASS |

# Review Gate
- `surface.cli` 和 `surface.agent_skill` 必须保持 `partial`，不能宣称已提供标准 Markdown 全链路。
- `surface.telegram_bot` 必须标明真实 token/live smoke 待执行。
- `surface.huggingface_space` 必须标明真实托管平台验证待执行。
- Registry 不得保存用户输入、报告正文、真实 token 或生产日志。

# Runtime Verification Gate
- 本任务只执行本地验证。
- 真实 Bot live、真实 HF Space、公网 API、多浏览器和完整 Markdown byte-level diff 统一标注后续验证。

# Ship Readiness
- 本地 contract/API/entrypoint/quick CI 通过。
- 任务 closeout 和全任务树校验通过。
- 未提交改动需后续由 `auto-github` 或用户指令处理。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现有交付面、链路和边界已列入 CONTEXT。 |
| TP-02 | schema/registry/resource schema 完成并被测试覆盖。 |
| TP-03 | API、metadata、OpenAPI 完成并被测试覆盖。 |
| TP-04 | 文档和路线图同步，不夸大 live 验证。 |
| TP-05 | 验证命令真实执行，证据写入 STATUS。 |

# Anti-Goals
- 不得重写交付面实现。
- 不得泄露真实用户数据或凭证。
- 不得伪造外部 live 验证结果。
