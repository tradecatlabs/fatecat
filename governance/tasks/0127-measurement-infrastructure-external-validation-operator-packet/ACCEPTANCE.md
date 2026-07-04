# Task-Level Acceptance

| Requirement | Acceptance |
| --- | --- |
| All-category operator packet exists | Contract, Python generator and shell wrapper are tracked |
| Current 22 category runbooks are covered | Regression builds packet from actual `CATEGORY_PROFILES` and compares category set |
| Output is safe for repo artifacts | Raw URL and sensitive-looking assignments are rejected |
| Packet does not claim live success | `packetGate.status` remains `blocked`; non-claims state no live checks are executed |
| local-ci exposes artifact | quick CI writes `external-validation-operator-execution-packet.json` and summary artifact key |

# Validation Plan

| Validation | Command |
| --- | --- |
| Python syntax | `.venv/bin/python -m py_compile scripts/external-validation-operator-execution-packet.py scripts/production-live-operator-execution-packet.py scripts/external-validation-category-runbooks.py` |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_operator_execution_packet.py tests/regression/test_external_validation_category_runbooks.py tests/regression/test_production_live_operator_execution_packet.py` |
| Lint | `.venv/bin/python -m ruff check scripts/external-validation-operator-execution-packet.py scripts/external-validation-category-runbooks.py scripts/production-live-operator-execution-packet.py tests/regression/test_external_validation_operator_execution_packet.py tests/regression/test_external_validation_category_runbooks.py tests/regression/test_production_live_operator_execution_packet.py` |
| Format check | `.venv/bin/python -m ruff format --check scripts/external-validation-operator-execution-packet.py scripts/external-validation-category-runbooks.py scripts/production-live-operator-execution-packet.py tests/regression/test_external_validation_operator_execution_packet.py tests/regression/test_external_validation_category_runbooks.py tests/regression/test_production_live_operator_execution_packet.py` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0127-measurement-infrastructure-external-validation-operator-packet --phase closeout` |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-operator-packet-0127.json` |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-operator-packet-0127-postcommit` |

# Review Gate

- Future-optimal drift: packet must move toward unified external validation execution, not duplicate 0126 production-only scope.
- Ponytail complexity: new contract/script must justify existence by covering all categories; no new abstraction beyond generator + wrapper.
- Document drift: roadmap, AGENTS, task index and task package must match actual wiring.
- Security/privacy: no secret values, raw URLs or fake proof text in generated output.

# Runtime Verification Gate

- No runtime service is introduced.
- No external endpoint is contacted.
- No credential is read.
- Generated artifacts remain local JSON files under explicit output paths.

# Ship Readiness

Task-local ship readiness requires:

- Targeted tests pass.
- Lint and format checks pass.
- Task docs validation passes.
- Secret scan passes.
- Quick CI passes after commit for the final HEAD.
- Remote GitHub Actions acceptance/container runs for the pushed commit are observed by the outer delivery flow.

Task-local readiness does not mean production 100% readiness. Real external live validation and third-party audit remain pending.

# Task Package Acceptance

- `TODO.md` leaves are all checked.
- `STATUS.md` overall status is `Done`.
- `STATUS.md` records validation evidence and remaining external blockers.
- `INDEX.md` contains 0127.

# Anti-Goals

- Do not execute live production requests.
- Do not create real proof refs.
- Do not store secrets, URLs, DSNs or webhook payloads.
- Do not mutate provider algorithms, report generation or user-facing outputs.
- Do not declare external validation, production readiness or 100% infrastructure complete.
