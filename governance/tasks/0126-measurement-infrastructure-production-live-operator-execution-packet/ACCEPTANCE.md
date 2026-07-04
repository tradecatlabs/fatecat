# Task-Level Acceptance

| Requirement | Evidence |
| --- | --- |
| Contract exists | `contracts/fate/audit/production-live-operator-execution-packet.json` |
| CLI generator exists | `scripts/production-live-operator-execution-packet.py` and `.sh` |
| Packet stays blocked | Output uses `status=operator_action_required` and `packetGate.status=blocked` |
| Five categories covered | Regression fixture covers API/HF/Bot/webhook/parity categories |
| Sensitive input rejected | Regression rejects `token=` marker in input queue |
| Output no raw URL | Regression confirms serialized packet contains no `https://` |
| local-ci wired | `scripts/local-ci.sh` generates packet and records summary artifact |
| Docs wired | AGENTS and roadmap reference the packet |

# Validation Plan

```bash
.venv/bin/python -m pytest -q tests/regression/test_production_live_operator_execution_packet.py tests/regression/test_production_live_delivery_evidence_bundle.py tests/regression/test_external_validation_category_runbooks.py
.venv/bin/python -m ruff check scripts/production-live-operator-execution-packet.py tests/regression/test_production_live_operator_execution_packet.py
.venv/bin/python -m ruff format --check scripts/production-live-operator-execution-packet.py tests/regression/test_production_live_operator_execution_packet.py
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0126-measurement-infrastructure-production-live-operator-execution-packet --phase closeout
bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-production-live-operator-packet-0126.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-production-live-operator-packet-0126
```

# Review Gate

- No output JSON may contain raw `http://` / `https://` URL.
- No output JSON may contain token/secret/password/DSN/private key assignments.
- No local-contract, dry-run, pending summary or operator packet may become live proof.
- Operator packet must stay upstream of real live execution and downstream gates.

# Runtime Verification Gate

No long-running runtime is introduced. The shell wrapper must use repo `.venv/bin/python` or `python3` fallback and write deterministic JSON to explicit output paths.

# Ship Readiness

Ready only when targeted tests, ruff, format check, task docs validation, secret scan, quick local CI, commit, push and remote CI observation complete.

# Task Package Acceptance

## TP-01 Scope Confirmation

Accepted when `MI-100.B` categories and upstream/downstream evidence chain are recorded.

## TP-02 Contract Script Wrapper

Accepted when contract/script/wrapper exist and tests cover blocked packet generation and rejection paths.

## TP-03 Wiring

Accepted when local-ci, AGENTS and roadmap reference the operator packet.

## TP-04 Validation

Accepted when local gates pass and generated packet remains blocked without real summaries.

## TP-05 Delivery

Accepted when commit is pushed and remote CI result is recorded.

# Anti-Goals

- Do not execute real production API/HF/Bot/Postgres/webhook calls in this task.
- Do not save real endpoint URLs, credentials, DSNs, logs or report body.
- Do not claim third-party audit or 100% measurement infrastructure completion.
