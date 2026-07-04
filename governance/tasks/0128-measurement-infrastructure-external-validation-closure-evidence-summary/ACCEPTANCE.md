# Task-Level Acceptance

| Requirement | Acceptance |
| --- | --- |
| Closure evidence summary exists | Contract, Python generator and shell wrapper are tracked |
| Current 22 category runbooks are covered | Regression builds summary from actual `CATEGORY_PROFILES` and compares category set |
| Output is safe for repo artifacts | Raw URL and sensitive-looking assignments are rejected |
| Summary does not claim live success | `closureGate.status` remains `blocked` when proof-ref/live evidence is missing |
| local-ci exposes artifact | quick CI writes `external-validation-closure-evidence-summary.json` and summary artifact key |
| certification consumes it | audit domain requires operator packet and closure evidence summary |

# Validation Plan

| Validation | Command |
| --- | --- |
| Python syntax | `.venv/bin/python -m py_compile scripts/external-validation-closure-evidence-summary.py scripts/measurement-infrastructure-certification.py` |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_evidence_summary.py tests/regression/test_measurement_infrastructure_certification.py` |
| Lint | `.venv/bin/python -m ruff check scripts/external-validation-closure-evidence-summary.py scripts/measurement-infrastructure-certification.py tests/regression/test_external_validation_closure_evidence_summary.py tests/regression/test_measurement_infrastructure_certification.py` |
| Format check | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-evidence-summary.py scripts/measurement-infrastructure-certification.py tests/regression/test_external_validation_closure_evidence_summary.py tests/regression/test_measurement_infrastructure_certification.py` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0128-measurement-infrastructure-external-validation-closure-evidence-summary --phase closeout` |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-closure-evidence-summary-0128.json` |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-closure-evidence-summary-0128-postcommit` |

# Review Gate

- Future-optimal drift: summary must improve audit/certification closure evidence, not duplicate trend dashboard.
- Ponytail complexity: new contract/script must justify existence by adding audit-ready rollup; no new framework.
- Document drift: roadmap, AGENTS, task index and certification contract must match actual wiring.
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
- `INDEX.md` contains 0128.

# Anti-Goals

- Do not execute live production requests.
- Do not create real proof refs or live proofs.
- Do not store secrets, URLs, DSNs or webhook payloads.
- Do not mutate provider algorithms, report generation or user-facing outputs.
- Do not declare external validation, production readiness or 100% infrastructure complete.
