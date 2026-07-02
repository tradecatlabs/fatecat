# Task-Level Acceptance
- `ApiPrincipal` 显式携带 record scopes。
- `FATE_API_USER_TOKENS` 旧值形态 `用户ID:占位令牌` 保持兼容，仍可写自己记录。
- `FATE_API_USER_TOKENS` 新值形态 `用户ID:占位令牌:record.read|record.list` 只授予声明 scope。
- 缺 `record.write` 写入返回 403 `权限不足`。
- 缺 `record.delete` 删除返回 403 `权限不足`。
- owner 边界仍有效，跨用户访问返回 403 `无权访问该记录`。
- `control.rbac_policy` 可通过 `/security` 发现。
- 文档明确本任务不是 OAuth/OIDC、外部 IdP 或生产 IAM。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && python3 -m json.tool contracts/fate/security/schemas/security-control.schema.json >/dev/null` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'scoped_user_token or rbac or token or record or security'` |
| shell syntax | `bash -n scripts/production-readiness.sh` |
| ruff | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0028.json && python3 -m json.tool /tmp/fatecat-secret-scan-0028.json >/dev/null` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- 旧 token 兼容必须保留。
- scoped token 不能越过 scope gate。
- scope 通过后仍必须执行 owner gate。
- registry/docs 不得把本地 RBAC 写成 OAuth/OIDC 或外部 IdP 已完成。
- audit/log 不得输出 token、userId 原文、请求体或报告正文。

# Runtime Verification Gate
- `test_scoped_user_token_can_read_and_list_but_cannot_write_record` 必须通过。
- `test_scoped_user_token_requires_delete_scope` 必须通过。
- `test_user_token_can_write_only_own_record` 必须继续通过。

# Ship Readiness
- 当前任务完成后可声明：records API 具备本地 scoped RBAC baseline。
- 不可声明：OAuth/OIDC、外部 IdP、生产 IAM、多租户组织权限或真实生产 token live 验证已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现状、范围和风险已落盘。 |
| TP-02 | runtime scope gate 和 production-readiness 格式校验已实现。 |
| TP-03 | registry/schema/tests/docs 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不实现 OAuth/OIDC。
- 不新增数据库权限表。
- 不把 scoped token 说成生产 IAM。
- 不输出真实 token 或用户 ID 原文。
