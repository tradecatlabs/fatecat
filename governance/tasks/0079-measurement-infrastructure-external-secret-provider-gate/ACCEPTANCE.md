# Task-Level Acceptance

- External secret provider evidence contract exists and defines local baseline, external target, live evidence schema, negative evidence cases, privacy boundary and release boundary.
- `external-secret-provider-gate` passes local contract validation without external credentials and outputs `外部连通验证待执行`.
- Gate rejects local Fernet/env var/placeholder evidence pretending to be external Vault/KMS.
- Security registry/schema/policy register `control.external_secret_provider_kms` as `secret_provider`, `manual`, `external_connectivity_pending`.
- Production security gate includes secret provider control.
- Quick local-ci generates `external-secret-provider-gate.json`.
- Docs and AGENTS state this is not real external Vault/KMS live evidence.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/security/external-secret-provider-contract.json` | exit 0 |
| Shell syntax | `bash -n scripts/external-secret-provider-gate.sh scripts/local-ci.sh scripts/production-security-gate.sh` | exit 0 |
| External secret provider gate | `bash scripts/external-secret-provider-gate.sh --output-json /tmp/fatecat-external-secret-provider-gate.json` | status passed, liveEvidenceStatus pending |
| Production security gate | `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-gate.json` | controls includes secret provider |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate.json` | exit 0 |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_secret_provider_gate.py tests/regression/test_production_security_gate.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py tests/regression/test_runtime_backend_gate.py` | exit 0 |
| Formatting/lint | focused `ruff check` and `ruff format --check` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| JSON syntax | passed: `python3 -m json.tool contracts/fate/security/external-secret-provider-contract.json` |
| Shell syntax | passed: `bash -n scripts/external-secret-provider-gate.sh scripts/local-ci.sh scripts/production-security-gate.sh` |
| External secret provider gate | passed: `bash scripts/external-secret-provider-gate.sh --output-json /tmp/fatecat-external-secret-provider-gate.json` |
| Production security gate | passed: `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-gate.json` |
| Runtime backend gate | passed: `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate.json` |
| Focused pytest | passed: 120 tests |
| Formatting/lint | passed: focused `ruff check`; format passed after formatting new test |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick`, evidence `/tmp/fatecat-local-ci-20260703105055`, focused regression `219 passed` |

# Review Gate

- security-drift: local Fernet remains local baseline; external Vault/KMS remains external pending.
- document-drift: security registry/schema/policy、runtime backend note、operations docs、AGENTS and task docs agree.
- future-optimal-drift: evidence protocol leads to real secret provider live validation instead of text-only blocked claim.
- ponytail-complexity: no external SDK/dependency added before real provider is selected.
- evidence-integrity: gate rejects fake local/placeholder evidence.

# Runtime Verification Gate

- No external provider: gate must pass only as contract validation and mark `外部连通验证待执行`.
- With evidence JSON: gate must validate provider type, key reference, rotation proof, access audit proof, application injection proof and redaction boundary.
- Any raw secret/token/DSN/URL/private key marker in evidence must fail.

# Ship Readiness

- All TODO leaves complete.
- Code, scripts, tests, docs, contract and task docs pass validation.
- Git diff contains no real secret、DSN、webhook URL、KMS key、provider endpoint、报告正文或真实非北京地区示例。
- commit/push 后记录远端 CI 或明确 CI 待执行。

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 0059/0078 缺口已记录，不把 local Fernet 写成 external Vault/KMS。 |
| TP-01.02 | security gate 接线点已确认。 |
| TP-02.01 | external secret provider contract exists and parses. |
| TP-02.02 | fake local/placeholder/missing audit evidence is rejected. |
| TP-03.01 | SecurityControl schema/registry/policy include secret_provider. |
| TP-03.02 | external-secret-provider gate writes redacted summary. |
| TP-03.03 | local-ci runs gate and records artifact path. |
| TP-04.01 | regression tests cover contract, negative cases, redacted live evidence and summary privacy. |
| TP-04.02 | roadmap、operations docs and AGENTS updated without live overclaim. |
| TP-05.01 | focused gates and quick CI pass. |
| TP-05.02 | closeout、commit、push、CI evidence complete. |

# Anti-Goals

- 不接入真实 Vault/KMS/secret manager。
- 不声明 external Vault/KMS live passed。
- 不声明生产密钥生命周期已完成。
- 不声明 public webhook live passed、exactly-once 或长期多副本 production ready。
- 不输出真实 secret、token、DSN、webhook URL、provider endpoint、KMS key、审计日志 payload、报告正文或用户隐私样例。
