# Task-Level Acceptance
| 验收项 | 命令 / 证据 | 通过标准 |
| --- | --- | --- |
| JSON parse | `python3 -m json.tool` on changed event contracts/examples | exit 0 |
| event gate | `bash scripts/event-contract-gate.sh --output-json /tmp/fatecat-event-contract-0097.json` | passed，checks >= 240 |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_event_contract_gate.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_webhook_outbox_redelivery_smoke.py` | 11 passed |
| docs sync | AGENTS/API/roadmap/task docs diff | 不声明 broker/live/production replay 已完成 |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0097.json` | findingCount=0 |
| local-ci quick | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0097` | status passed |
| task docs | `validate_task_docs.py --phase closeout` | exit 0 |

# Validation Plan
1. Parse JSON contracts and examples.
2. Run event contract gate.
3. Run focused event/replay/webhook regression tests.
4. Run secret scan and privacy-sensitive grep if needed.
5. Run quick local-ci because `event-contract-gate.sh` is already in quick CI.
6. Run task closeout validator and `git diff --check`.

# Review Gate
- No external broker or live webhook claim.
- No runtime event processor rewrite.
- No complete payload, real webhook URL, user input, report body, secret, token, DSN or production log stored.
- Producer path, required consumer and replay/DLQ example links are machine checked.

# Runtime Verification Gate
- Required local gate: `bash scripts/event-contract-gate.sh --output-json /tmp/fatecat-event-contract-0097.json`。
- Required regression: focused pytest listed above.
- Required release slice proof: quick local-ci before commit.
- External live verification: not required for this task.

# Ship Readiness
- 0097 can ship: TP-05.01 is Done, local gates passed, and live external event delivery remains explicitly out of scope.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Existing event baseline and missing consumer/replay coverage identified. |
| TP-02.01 | Every event has `consumerContract` with at least one non-future required consumer. |
| TP-02.02 | Replay/DLQ policy and redacted examples exist. |
| TP-03.01 | Gate rejects missing required consumer, missing producer path and sensitive replay examples. |
| TP-03.02 | Regression tests prove new gate behavior. |
| TP-04.01 | Docs keep live/external claims out of scope. |
| TP-05.01 | Final validators pass. |

# Anti-Goals
- 不接外部 broker。
- 不实现生产 replay/DLQ worker。
- 不声明公网 webhook live delivery。
