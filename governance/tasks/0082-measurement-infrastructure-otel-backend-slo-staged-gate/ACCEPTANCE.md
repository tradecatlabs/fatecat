# Task-Level Acceptance

- `otel-backend-slo-gate` exists and passes without external credentials in pending mode.
- Contract defines required live evidence for collector runtime, trace backend, metrics backend, SLO dashboard, alert route, production traffic window, error budget and incident drill.
- Fake/local/placeholder/sensitive/overclaim evidence is rejected.
- Optional redacted live fixture is accepted only when schema is complete.
- local-ci writes an `otel-backend-slo-gate.json` artifact without claiming live passed.
- Docs and task closeout keep real backend/SLO live evidence as `外部连通验证待执行`.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Shell/Python syntax | `python3 -m py_compile scripts/otel-backend-slo-gate.py` and `bash -n scripts/otel-backend-slo-gate.sh scripts/local-ci.sh` | exit 0 |
| Pending gate | `bash scripts/otel-backend-slo-gate.sh --output-json /tmp/fatecat-otel-backend-slo-gate-recheck.json` | status `passed`, `liveEvidenceStatus=外部连通验证待执行` |
| Live fixture | regression fixture with complete redacted proof refs | accepted with `external_live_passed` |
| Negative evidence | fake/local/placeholder/sensitive evidence fixtures | rejected |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_otel_backend_slo_gate.py tests/regression/test_observability_trace_slo.py tests/regression/test_observability_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'observability or metadata'` | exit 0 |
| Ruff | focused `ruff check` and `ruff format --check` | exit 0 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0082.json` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0082` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| Syntax | passed: `python3 -m py_compile scripts/otel-backend-slo-gate.py`; `bash -n scripts/otel-backend-slo-gate.sh scripts/local-ci.sh` |
| Pending gate | passed: `{"checks": 25, "liveEvidenceStatus": "外部连通验证待执行", "negativeEvidenceRejected": 4, "status": "passed"}` |
| Live fixture | passed through regression tests |
| Negative evidence | passed through regression tests and built-in negative checks |
| Focused pytest | passed: `12 passed, 104 deselected` for observability/API focused set; direct `test_otel_backend_slo_gate.py` passed `6 passed` |
| Ruff | passed after formatting `scripts/otel-backend-slo-gate.py` and `tests/regression/test_otel_backend_slo_gate.py` |
| Secret scan | passed: `findingCount=0` |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0082`; summary `status=passed`, focused regression `237 passed`, artifact `otelBackendSloGate=/tmp/fatecat-local-ci-0082/otel-backend-slo-gate.json` |
| Task validators | passed: `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` with `valid=82`, `invalid=0` |

# Review Gate

- evidence-integrity: external live evidence must include required backend/SLO proof refs.
- security/privacy: no sensitive values, raw URL, production trace, metrics snapshot, log body or user input in evidence.
- future-optimal-drift: staged gate must lead toward real backend live verification, not become another static plan.
- ponytail-complexity: no OTel SDK/exporter dependency and no runtime rewrite in this slice.
- document-drift: roadmap/docs/AGENTS/local-ci must agree on pending/live non-claim boundary.

# Runtime Verification Gate

- Default mode must not require credentials or external services.
- External evidence mode must require complete `observabilityBackend` fields.
- Any forbidden proof fragment, sensitive assignment, raw URL, localhost/debug/sample backend, or missing error budget/alert/incident proof must fail.
- `signal.otel_backend_slo_evidence` and `otel-backend-slo-evidence-contract.json` must remain linked in observability registry.

# Ship Readiness

- All TODO leaves complete.
- Worktree cleanliness is verified by the outer git delivery flow after commit.
- Remote CI evidence is reported from the actual post-push GitHub Actions run, not pre-claimed by this task snapshot.
- No document states real OTel backend, production SLO, alert live or incident drill has passed.

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | observability registry、0064 gate、roadmap and local-ci inspected. |
| TP-01.02 | pending/live/non-claim boundary documented. |
| TP-02.01 | live evidence schema and proof ref allowlist defined. |
| TP-02.02 | fake/local/sensitive/overclaim cases rejected. |
| TP-03.01 | Python gate and shell wrapper added. |
| TP-03.02 | observability registry/schema、local-ci、AGENTS and docs linked. |
| TP-04.01 | regression tests cover pending, live fixture and negative cases. |
| TP-04.02 | focused gates, secret scan, quick CI and task validators complete. |
| TP-05.01 | closeout docs complete without overclaim. |
| TP-05.02 | task snapshot records that git push and remote CI evidence belong to the outer delivery flow after commit exists. |

# Anti-Goals

- 不启动真实 OTel collector。
- 不连接真实 trace backend、metrics backend、SLO dashboard 或 alert platform。
- 不声明 production SLO computed、alert live、incident drill completed。
- 不输出真实 secret、token、DSN、URL、生产日志、metrics snapshot、trace payload、报告正文或用户输入。

# Live Evidence

外部连通验证待执行。需要真实 OTel collector runtime、trace backend、metrics backend、SLO dashboard、alert platform、生产流量窗口、error budget 和 incident drill proof refs 后，才允许用 external live evidence 通过 gate。
