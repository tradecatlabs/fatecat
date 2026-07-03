# Task-Level Acceptance

- `provider-drift-scanner` exists and outputs `kind=fatecat.provider_drift_report`.
- Report covers 4 production providers and 4 production capabilities.
- Report includes local `provider.validate` and `provider.calculate` spans for each production provider/capability.
- Report compares dependency smoke refs、source refs、license evidence and vendor supply-chain metadata.
- Report has `findingCount=0` on current baseline and fails if blocking drift is found.
- local-ci writes `provider-drift-scanner.json` without claiming external live passed.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| JSON/syntax | `python3 -m json.tool contracts/fate/capabilities/provider-drift-contract.json`; `bash -n scripts/provider-drift-scanner.sh scripts/local-ci.sh`; `python3 -m py_compile scripts/provider-drift-scanner.py` | exit 0 |
| Scanner | `bash scripts/provider-drift-scanner.sh --output-json /tmp/fatecat-provider-drift-scanner-0084.json` | status `passed`, `providers=4`, `findings=0`, `spans=12` |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_provider_drift_scanner.py tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema'` | exit 0 |
| Ruff | focused `ruff check` and `ruff format --check` | exit 0 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0084.json` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0084` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| JSON/syntax | passed: provider drift contract、provider schema、shell syntax and Python compile |
| Scanner | passed: `{"status": "passed", "providers": 4, "findings": 0, "spans": 12}` |
| Focused pytest | passed: `17 passed, 14 deselected` |
| Ruff | passed after formatting scanner and test files |
| Secret scan | passed after 0084 changes; finding count recorded in `/tmp/fatecat-secret-scan-0084.json` |
| Quick CI | passed after 0084 changes; artifact directory `/tmp/fatecat-local-ci-0084` |
| Task validators | passed: `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` |

# Review Gate

- evidence-integrity: drift report must include trace、dependency、source、license、vendor evidence.
- security/privacy: no sample payload, real user input, report body, token, secret, DSN or production account in report.
- future-optimal-drift: scanner must lead toward provider drift evidence, not become another static docs table.
- ponytail-complexity: no new provider abstraction and no external OTel client dependency in this slice.
- document-drift: roadmap/docs/AGENTS/local-ci must agree on local scanner and external live pending boundary.

# Runtime Verification Gate

- Default mode must not require credentials or external services.
- Missing `provider.validate` or `provider.calculate` span must produce a drift finding.
- Missing source/license/vendor evidence must produce a drift finding.
- `provider-drift-contract.json` and provider schema invariant must remain linked by tests.

# Ship Readiness

- All TODO leaves complete.
- Worktree cleanliness is verified by the outer git delivery flow after commit.
- Remote CI evidence is reported from the actual post-push GitHub Actions run, not pre-claimed by this task snapshot.
- No document states real external provider live smoke、external trace backend or legal license review passed.

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | lifecycle/dependency gate、registry、vendor manifest and roadmap inspected. |
| TP-01.02 | dependency/source/license/trace drift boundary documented. |
| TP-02.01 | provider drift contract and required fields defined. |
| TP-02.02 | trace、dependency、source、license、vendor checks defined. |
| TP-03.01 | Python scanner and shell wrapper added. |
| TP-03.02 | provider schema、local-ci、AGENTS、operations docs、roadmap and task index linked. |
| TP-04.01 | regression tests cover report、CLI and contract. |
| TP-04.02 | focused gates, secret scan, quick CI and task validators complete. |
| TP-05.01 | closeout docs complete without overclaim. |
| TP-05.02 | task snapshot records that git push and remote CI evidence belong to the outer delivery flow after commit exists. |

# Anti-Goals

- 不接真实公网外部依赖。
- 不接外部 trace backend、collector、dashboard 或 alert platform。
- 不输出真实 secret、token、DSN、URL、报告正文、出生地区或用户输入。
- 不把 SPDX/license manifest 检查写成法务许可意见。

# Live Evidence

外部连通验证待执行。真实公网外部依赖 live smoke、外部 trace backend、法律许可复核和跨版本升级策略仍需后续外部证据。
