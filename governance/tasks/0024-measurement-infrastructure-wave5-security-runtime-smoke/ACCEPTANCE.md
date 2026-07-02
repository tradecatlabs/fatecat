# Task-Level Acceptance
- `bash scripts/security-smoke.sh --output-json /tmp/fatecat-security-smoke.json` 通过并输出 JSON。
- JSON 覆盖响应安全头、请求体限制、限流、records disabled、user token owner boundary、security registry metadata 和本地文件门禁。
- registry metadata 暴露 `smokeCommand`、`smokeOutput` 和 `smokeScope`。
- quick CI 包含 `test_security_smoke.py`。
- 文档和 roadmap 区分本地 smoke 与未完成的真实生产域名/CORS/token/Bot live、OAuth/OIDC、RBAC、审计日志、retention、专用 secret scanner。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/security/registry.json >/dev/null` |
| smoke CLI | `bash scripts/security-smoke.sh --output-json /tmp/fatecat-security-smoke.json && python3 -m json.tool /tmp/fatecat-security-smoke.json >/dev/null` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'security or smoke'` |
| ruff | `.venv/bin/ruff check scripts/security-smoke.py tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| format | `.venv/bin/ruff format --check scripts/security-smoke.py tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- smoke 输出不得包含真实日志正文、请求体、用户输入、token、secret、DSN 或报告正文。
- 文档不得写成真实生产域名、真实 token、Bot live、OAuth/OIDC、RBAC、审计日志或专用 secret scanner 已完成。
- planned security controls 仍保持 planned 或 pending，不得升格为 production。

# Runtime Verification Gate
- smoke CLI 至少返回 19 个 passed checks。
- focused tests 和 quick CI 必须通过。

# Ship Readiness
- 当前任务完成后可声明：available security controls 具备本地 smoke。
- 不可声明：真实生产安全、OAuth/OIDC、RBAC、审计日志、retention、专用 secret scanner、线上 CORS/token/Bot live 完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口和边界已落盘。 |
| TP-02 | smoke 和 registry metadata 已实现。 |
| TP-03 | tests/docs/quick CI 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不得伪造真实生产域名、真实 token、Webhook 或 Bot live smoke。
- 不得输出真实密钥、请求体、报告正文、用户输入或 DSN。
- 不得把 TestClient smoke 当成公网生产验证。
