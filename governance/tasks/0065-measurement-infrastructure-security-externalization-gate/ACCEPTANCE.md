# Task-Level Acceptance

0065 只有在以下证据同时成立时才能 closeout：

- `contracts/fate/security/externalization-evidence-contract.json` 存在，覆盖 OIDC/IdP、SIEM/不可变审计和 retention cleaner 三类外部证据，且不包含真实 endpoint、token、secret、DSN 或用户数据。
- Security registry/schema/AGENTS、API 文档、roadmap 和 scripts AGENTS 已同步。
- `bash scripts/security-externalization-gate.sh --output-json <path>` 通过。
- Gate 能拒绝伪造 live evidence：本地 scoped token 不能作为 OIDC proof，placeholder SIEM 不能作为 immutable audit proof，无 smoke 不能作为 retention cleaner proof。
- Focused regression tests、task validators、ruff/format、secret scan、quick local CI 通过。

# Task Package Acceptance

| Node ID | Verify | Gate |
| --- | --- | --- |
| TP-01.01 | `git status` / `rg` / `sed` | 当前事实和 0065 边界明确 |
| TP-02.01 | JSON syntax + gate | evidence contract 可机器读取 |
| TP-02.02 | focused tests / docs diff | registry/schema/AGENTS 链接一致 |
| TP-03.01 | gate CLI | dry-run gate 无外部账号依赖 |
| TP-03.02 | focused pytest | negative fake evidence 断言通过 |
| TP-03.03 | local-ci summary artifact | quick CI 运行新 gate |
| TP-04.01 | docs diff + rg | 文档不夸大安全外部化 live 状态 |
| TP-04.02 | validation evidence | 全部本地门禁通过并收口 |

# Edge Cases

- 如果 evidence contract 无法解析，gate 必须失败。
- 如果 identity live evidence 使用 `scoped_token_rbac`、`local_token` 或 `FATE_API_TOKEN`，gate 必须失败。
- 如果 SIEM live evidence 缺少外部 proof ref、不可变模式或把 endpoint/payload 写入证据，gate 必须失败。
- 如果 retention cleaner live evidence 缺少 smoke summary、delete mode 或 audit action，gate 必须失败。

# Validation Plan

| 验证项 | 命令 | 预期 |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/security/externalization-evidence-contract.json` | passed |
| Gate CLI | `bash scripts/security-externalization-gate.sh --output-json <path>` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_production_security_gate.py -k 'security_externalization or production_security'` | passed |
| Lint/format | `.venv/bin/python -m ruff check ...` / `.venv/bin/python -m ruff format --check ...` | passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json <path>` | 0 findings |
| Task validators | `validate_task_docs.py --phase closeout` + `validate_tasks_tree.py` | passed |
| Quick local CI | `bash scripts/local-ci.sh --profile quick --output <dir>` | passed |

# Review Gate

- Review must confirm no OAuth/OIDC, SIEM, immutable storage, retention cleaner live, production deletion or incident/security audit is claimed.
- Review must confirm no real endpoint, token, secret, DSN, request body, user input, report body, audit payload or production log is committed.
- Review must confirm docs and contracts use the same external pending wording.

# Runtime Verification Gate

- Runtime verification is limited to local contract checks and fake evidence negative tests.
- Any claim requiring real IdP, SIEM, immutable storage, production database or retention cleaner live remains `外部连通验证待执行`.

# Ship Readiness

- 0065 can ship after local validation, quick local CI, commit/push and current-commit remote Acceptance pass.
- 0065 cannot be used as proof that production identity, SIEM or retention cleaner is complete.

# Anti-Goals

- 不接入真实 OIDC/JWKS/IdP。
- 不接入真实 SIEM、云日志、WORM 存储或不可变审计平台。
- 不删除真实记录、报告任务、审计日志或生产数据。
- 不读取真实 `.env` 或生产凭证。
