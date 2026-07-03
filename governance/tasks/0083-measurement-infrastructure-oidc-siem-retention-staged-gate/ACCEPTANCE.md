# Task-Level Acceptance

- `security-externalization-gate` exists and passes without external credentials in pending mode.
- Contract defines proof-ref prefixes for identity、SIEM and retentionCleaner live evidence.
- Gate rejects raw OIDC/SIEM URL evidence, non-allowlisted proof refs, token/secret fragments and retention production deletion marker.
- Built-in negative evidence count is 5 and all negative fixtures are rejected.
- local-ci writes `security-externalization-gate.json` without claiming live passed.
- Docs and task closeout keep real OIDC/SIEM/retention live evidence as `外部连通验证待执行`.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/security/externalization-evidence-contract.json` and `python3 -m json.tool contracts/fate/security/schemas/security-control.schema.json` | exit 0 |
| Pending gate | `bash scripts/security-externalization-gate.sh --output-json /tmp/fatecat-security-externalization-0083.json` | status `passed`, `liveEvidenceStatus=外部连通验证待执行` |
| Production security gate | `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-0083.json` | exit 0 |
| Negative evidence | built-in fake scoped token, placeholder SIEM, missing retention smoke, raw OIDC URL, production deletion marker | rejected |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_production_security_gate.py tests/regression/test_capability_protocol.py -k 'security or externalization'` | exit 0 |
| Ruff | focused `ruff check` and `ruff format --check` | exit 0 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0083.json` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0083` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| JSON syntax | passed: security externalization contract and security-control schema parse with `python3 -m json.tool` |
| Pending gate | passed: `{"checks": 38, "liveEvidenceStatus": "外部连通验证待执行", "negativeEvidenceRejected": 5, "status": "passed"}` |
| Production security gate | passed in focused local gate run |
| Negative evidence | passed through built-in gate checks and regression tests |
| Focused pytest | passed: `11 passed, 23 deselected` for security/externalization focused set |
| Ruff | passed: `ruff check` and `ruff format --check` on modified Python test/gate files |
| Secret scan | passed after 0083 code/doc changes; finding count recorded in `/tmp/fatecat-secret-scan-0083.json` |
| Quick CI | passed after 0083 code/doc changes; artifact directory `/tmp/fatecat-local-ci-0083` |
| Task validators | passed: `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` |

# Review Gate

- evidence-integrity: external live evidence must include required OIDC/SIEM/retention proof refs.
- security/privacy: no sensitive values, raw URL, real endpoint, audit payload, report body or user input in evidence.
- future-optimal-drift: 0083 must harden the existing 0065 gate, not create a duplicate security workflow.
- ponytail-complexity: no OIDC/JWKS/SIEM client dependency and no runtime rewrite in this slice.
- document-drift: roadmap/docs/AGENTS/local-ci must agree on pending/live non-claim boundary.

# Runtime Verification Gate

- Default mode must not require credentials or external services.
- External evidence mode must require complete `identity`、`siem` and `retentionCleaner` fields.
- Any forbidden proof fragment, sensitive assignment, raw URL, non-allowlisted proof ref, placeholder SIEM, missing retention smoke or production deletion marker must fail.
- `externalization-evidence-contract.json` must remain linked from security controls and production security policy.

# Ship Readiness

- All TODO leaves complete.
- Worktree cleanliness is verified by the outer git delivery flow after commit.
- Remote CI evidence is reported from the actual post-push GitHub Actions run, not pre-claimed by this task snapshot.
- No document states real OIDC/IdP、external SIEM、immutable audit storage or retention cleaner live has passed.

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | security registry、externalization contract、production security policy and roadmap inspected. |
| TP-01.02 | proof-ref/raw URL/production deletion non-claim boundary documented. |
| TP-02.01 | proofRefPrefixes and live evidence input constraints defined. |
| TP-02.02 | raw URL and retention production marker negative cases rejected. |
| TP-03.01 | Contract and gate validation updated. |
| TP-03.02 | schema invariant、AGENTS、roadmap and task index linked. |
| TP-04.01 | regression tests cover pending, contract invariants and negative cases. |
| TP-04.02 | focused gates, secret scan, quick CI and task validators complete. |
| TP-05.01 | closeout docs complete without overclaim. |
| TP-05.02 | task snapshot records that git push and remote CI evidence belong to the outer delivery flow after commit exists. |

# Anti-Goals

- 不接入真实 OIDC/IdP 或 JWKS 校验。
- 不连接真实 SIEM、WORM 存储或云日志平台。
- 不实现真实 retention cleaner 或生产删除流程。
- 不声明 production identity、external SIEM、immutable audit storage 或 retention cleaner live completed。
- 不输出真实 secret、token、DSN、URL、日志 payload、报告正文、出生地区或用户输入。

# Live Evidence

外部连通验证待执行。需要真实 OIDC/IdP、JWKS、外部 SIEM、不可变审计存储、生产数据库、retention cleaner smoke 和脱敏 proof refs 后，才允许用 external live evidence 通过 gate。
