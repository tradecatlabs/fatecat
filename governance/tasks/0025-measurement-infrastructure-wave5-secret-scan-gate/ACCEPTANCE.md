# Task-Level Acceptance
- `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan.json` 通过并输出 JSON。
- summary 覆盖 scannedFiles、skippedFiles、findingCount、findings、privacyBoundary 和 scope。
- scanner 对高置信 secret 样例有回归测试，对占位符/函数调用误报有回归测试。
- `control.secret_scan_gate` 登记到 SecurityControl registry，API 和 schema tests 覆盖。
- quick CI 包含 secret scan 步骤和 `test_secret_scan.py`。
- 文档和 roadmap 区分本地 scanner 与未完成的审计日志、retention、OAuth/OIDC、RBAC、真实 live 验证。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && python3 -m json.tool contracts/fate/security/secret-scan-allowlist.json >/dev/null` |
| scanner CLI | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan.json && python3 -m json.tool /tmp/fatecat-secret-scan.json >/dev/null` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'secret or security'` |
| ruff | `.venv/bin/ruff check scripts/secret-scan.py tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| format | `.venv/bin/ruff format --check scripts/secret-scan.py tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- scanner 输出不得包含疑似密钥原文、真实 token、secret、DSN、私钥、证书或 webhook 值。
- 文档不得写成云端 secret scanning、生产凭证审计、OAuth/OIDC、RBAC 或 retention 已完成。
- allowlist 只能登记占位符、示例片段和排除边界，不得登记真实 secret。

# Runtime Verification Gate
- scanner CLI 当前 worktree findingCount 必须为 0。
- focused tests 和 quick CI 必须通过。

# Ship Readiness
- 当前任务完成后可声明：FateCat 具备本地专用 secret scanner gate。
- 不可声明：生产 secret 审计、云端 secret scanning、OAuth/OIDC、RBAC、审计日志、retention 或 live smoke 已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口和边界已落盘。 |
| TP-02 | scanner 与 allowlist 已实现。 |
| TP-03 | registry/schema/tests/docs/quick CI 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不得读取 ignored `.env` 或生产 secret store。
- 不得输出疑似密钥原文。
- 不得把本地启发式 scanner 写成生产安全 100%。
