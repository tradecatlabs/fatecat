# Task-Level Acceptance

- Multi-replica runtime evidence contract exists and defines local baseline, external target, live evidence schema, negative evidence cases, privacy boundary and release boundary.
- `multi-replica-runtime-gate` passes local contract validation without external credentials and outputs `外部连通验证待执行`.
- Gate rejects single-replica、short-run、SQLite and exactly-once overclaim evidence.
- Runtime backend registry keeps `backend.postgres` planned and marks multi-replica as evidence-contract pending.
- Quick local-ci generates `multi-replica-runtime-gate.json`.
- Docs and AGENTS state this is not real multi-replica live evidence.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/delivery/multi-replica-runtime-contract.json` | exit 0 |
| Shell syntax | `bash -n scripts/multi-replica-runtime-gate.sh scripts/local-ci.sh` | exit 0 |
| Multi-replica runtime gate | `bash scripts/multi-replica-runtime-gate.sh --output-json /tmp/fatecat-multi-replica-runtime-gate.json` | status passed, liveEvidenceStatus pending |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate-0080.json` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_multi_replica_runtime_gate.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | exit 0 |
| Formatting/lint | focused `ruff check` and `ruff format --check` | exit 0 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0080.json` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0080` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| JSON syntax | passed: `python3 -m json.tool contracts/fate/delivery/multi-replica-runtime-contract.json` |
| Shell/Python syntax | passed: `python3 -m py_compile scripts/multi-replica-runtime-gate.py scripts/runtime-backend-gate.py` and `bash -n scripts/multi-replica-runtime-gate.sh scripts/local-ci.sh` |
| Multi-replica runtime gate | passed: `checks=27`, `negativeEvidenceRejected=4`, `liveEvidenceStatus=外部连通验证待执行` |
| Runtime backend gate | passed: `checks=100`, `externalCandidate=backend.postgres` |
| Focused pytest | passed: `33 passed` |
| Ruff | passed: focused `ruff check`; format check passed after formatting two files |
| Secret scan | passed: `findingCount=0` |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0080`, focused regression `224 passed` |

# Review Gate

- reliability-drift: Postgres remains planned; multi-replica live evidence remains external pending.
- document-drift: runtime registry、delivery registry、roadmap、operations docs、AGENTS and task docs agree.
- future-optimal-drift: evidence protocol leads to real multi-replica live validation instead of text-only blocked claim.
- ponytail-complexity: no external runner/dependency added before real platform exists.
- evidence-integrity: gate rejects fake single-replica/short-run/local/exactly-once evidence.

# Runtime Verification Gate

- No external runtime: gate must pass only as contract validation and mark `外部连通验证待执行`.
- With evidence JSON: gate must validate replica count、duration、completed jobs、proof refs、public webhook proof、external secret provider proof、metrics proof and redaction boundary.
- Any raw secret/token/DSN/URL/private key marker in evidence must fail.

# Ship Readiness

- All TODO leaves complete.
- Code, scripts, tests, docs, contract and task docs pass validation.
- Git diff contains no real secret、DSN、webhook URL、报告正文或真实用户数据。
- commit/push 后记录远端 CI 或明确 CI 待执行。

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 0078/0079 后 runtime 缺口已记录。 |
| TP-01.02 | runtime registry/local-ci/tests 接线点已确认。 |
| TP-02.01 | multi-replica runtime contract exists and parses. |
| TP-02.02 | fake single-replica、short-run、SQLite、exactly-once overclaim evidence is rejected. |
| TP-03.01 | Runtime backend registry and delivery registry link contract/gate. |
| TP-03.02 | multi-replica-runtime gate writes redacted summary. |
| TP-03.03 | local-ci runs gate and records artifact path. |
| TP-04.01 | regression tests cover contract, negative cases, redacted live evidence and summary privacy. |
| TP-04.02 | roadmap、operations docs and AGENTS updated without live overclaim. |
| TP-05.01 | focused gates and quick CI pass. |
| TP-05.02 | closeout docs complete; commit/push/CI evidence is recorded by delivery closeout after the commit exists. |

# Anti-Goals

- 不启动真实多副本 runtime。
- 不声明 multi-replica live passed。
- 不声明 production ready 或 exactly-once。
- 不输出真实 secret、token、DSN、webhook URL、报告正文或用户隐私样例。

# Live Evidence

外部连通验证待执行。需要真实多副本环境、公网 webhook receiver、external secret provider 和 metrics proof 后，才允许传入 `--evidence-json` 并推进 live status。
