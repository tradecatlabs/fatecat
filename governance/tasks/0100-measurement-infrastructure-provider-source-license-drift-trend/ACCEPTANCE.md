# Task-Level Acceptance
- [x] `provider-drift-trend-gate.sh` passes on current tracked baseline.
- [x] Trend report records baseline id, current provider count, scanner finding count, provider fingerprints and privacy/release boundary.
- [x] Missing provider baseline is rejected.
- [x] License production-use regression is rejected.
- [x] Vendor snapshot hash drift is rejected.
- [x] Failed scanner report is rejected.
- [x] quick local-ci invokes provider drift trend gate after scanner.
- [x] No output stores real user input、报告正文、出生地区、token、secret、DSN 或生产外部账号。

# Validation Plan
| Validation | Command |
| --- | --- |
| Gate smoke | `bash scripts/provider-drift-trend-gate.sh --output-json /tmp/fatecat-provider-drift-trend-0100.json` |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_provider_drift_trend_gate.py tests/regression/test_provider_drift_scanner.py tests/regression/test_capability_protocol.py` |
| Lint | `.venv/bin/ruff check scripts/provider-drift-trend-gate.py tests/regression/test_provider_drift_trend_gate.py` |
| Format | `.venv/bin/ruff format --check scripts/provider-drift-trend-gate.py tests/regression/test_provider_drift_trend_gate.py` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0100-measurement-infrastructure-provider-source-license-drift-trend --phase decompose` |
| Local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0100-final` |

# Review Gate
- Diff contains only provider drift trend baseline/gate, tests, local-ci wiring, docs and task package.
- No production provider algorithm changes.
- No external live evidence is claimed.

# Runtime Verification Gate
- Gate output must be `kind=fatecat.provider_drift_trend_report`.
- `status=passed` requires `findingCount=0`.
- External evidence remains `外部连通验证待执行`.

# Ship Readiness
- Focused validation, quick local-ci, secret scan inside quick CI, diff checks and task docs validator passed. Commit/push is the final delivery action and must be verified after push; remote CI must not be overclaimed unless a current-commit run is observed.

# Task Package Acceptance
## TP-01 SPEC
Verify: existing scanner and roadmap inspected.
Gate: do not duplicate provider runtime.

## TP-02 BUILD
Verify: new contract/baseline/script/wiring exist.
Gate: baseline and report JSON parse and initial gate passes.

## TP-03 TEST
Verify: focused tests and lint/format pass.
Gate: negative cases fail as intended.

## TP-04 SHIP
Verify: task docs closeout and git delivery evidence.
Gate: remote CI not overclaimed if current commit run is not observed.

# Anti-Goals
- 不得修改 production provider 算法。
- 不得虚构外部 provider live、外部 trace backend 或法律许可复核结果。
- 不得保存真实用户输入、报告正文、出生地区、token、secret、DSN 或生产外部账号。
