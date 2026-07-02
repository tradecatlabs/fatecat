# Task-Level Acceptance
- `audit_event` helper 存在，输出 JSON 结构化日志。
- 记录创建、读取、列表、删除，以及报告 job 提交/取消均有 audit_event 调用点。
- audit_event 不输出 token、请求体、报告正文、姓名、出生地区、recordId、jobId 或 userId 原文。
- `control.audit_event_log` 与 `control.retention_policy` 登记到 SecurityControl registry。
- API/contract tests 覆盖 audit/retention registry 和 runtime event 脱敏。
- 文档和 roadmap 区分本地 baseline 与未完成外部 SIEM/不可变审计存储/自动记录清理。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/security/schemas/security-control.schema.json >/dev/null && python3 -m json.tool contracts/fate/security/registry.json >/dev/null` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'audit_event or retention or security'` |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0026.json && python3 -m json.tool /tmp/fatecat-secret-scan-0026.json >/dev/null` |
| ruff | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- audit_event 输出不得包含真实 token、请求体、报告正文、姓名、出生地区、recordId、jobId 或 userId 原文。
- registry/docs 不得把本地 audit_event 写成外部 SIEM、不可变审计存储或生产日志平台已接入。
- retention policy 不得把显式删除模式写成自动记录清理已完成。

# Runtime Verification Gate
- caplog tests 必须证明 `record.read`、`report_job.submit`、`report_job.cancel` 有 audit_event 且敏感原文未出现。
- quick CI 必须通过。

# Ship Readiness
- 当前任务完成后可声明：FateCat 具备本地结构化 audit_event 与 retention policy baseline。
- 不可声明：外部 SIEM、不可变审计存储、生产日志 retention、自动记录清理、OAuth/OIDC、RBAC 或 live smoke 已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口和边界已落盘。 |
| TP-02 | runtime audit_event 已接入关键动作。 |
| TP-03 | registry/schema/tests/docs 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不得输出真实请求体、报告正文、token、姓名、出生地区或 ID 原文。
- 不得接入外部 SIEM 或伪造生产审计平台。
- 不得声称记录自动清理或 OAuth/RBAC 已完成。
