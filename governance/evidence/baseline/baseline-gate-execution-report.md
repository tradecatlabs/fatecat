---
id: BASELINE-GATE-EXECUTION-REPORT-FATECAT
type: baseline-gate-execution-report
status: archived
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-13
review_cycle: P30D
---

# Baseline Gate Execution Report

> 历史快照：以下结果对应 2026-06 迁移阶段，不得引用为当前提交证据。

## Current Evidence

| Gate | Command | Status |
| --- | --- | --- |
| Git status | `git status --short --branch` | WARN: user dirty worktree exists and must be preserved |
| Ahead/behind | `git rev-list --left-right --count @{u}...HEAD` | PASS: `0 0` |
| Governance init dry run | `init_governance_package.py --dry-run` | PASS |
| Governance init | `init_governance_package.py --mode minimal` | PASS |
| Shell syntax | `bash -n scripts/*.sh` | PASS |
| Structure gate | `bash scripts/check-structure.sh` | PASS with expected `scripts/project` migration warning |
| Source hygiene | `bash scripts/check-source-hygiene.sh` | PASS |
| Privacy fixtures | `bash scripts/check-privacy-fixtures.sh` | PASS |
| Governance strict validate | `python3 governance/tools/validate_governance_package.py --project-root . --strict` | PASS |
| Pure preflight | `bash scripts/preflight.sh --mode pure --bootstrap --pretty` | PASS; runtime root remains transitional `scripts/project` |
| Diff whitespace | `git diff --check` | PASS |
| Root service contract tests | `python3 -m pytest -q` | PASS: 4 service contract tests |
| Legacy behavior regression | `cd scripts/project && .venv/bin/python -m pytest -q tests modules/telegram/tests` | PASS: 108 tests |
| Full acceptance | `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-enterprise` | PASS |
| Explicit lite export | `bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite` | PASS |
| Explicit export hygiene | `bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat` | PASS |
| Enterprise root acceptance | `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-enterprise-root-2` | PASS: root runtime, 112 tests, ruff, mypy, API/Bot smoke, export smoke |
| Enterprise root pytest | `.venv/bin/python -m pytest -q` | PASS: 112 tests |
| Enterprise vendor health | `bash scripts/vendor-health.sh` | PASS: required=5 optionalFutureFeatures=10 hashed=15 |

## Required Before Completion

- Continue retiring compatibility-only references to `scripts/project`.
- Confirm `rg -n 'scripts/project'` only returns compatibility fields, migration ledger, historical evidence, negative tests or guard patterns.

## Latest Migration Delta

- Canonical service source roots contain copied source for `fate-core` and `fatecat-delivery`.
- Canonical contract/data/config/schema/runtime/vendor roots are populated; raw private data, real `.env`, real database files and `node_modules` remain excluded.
- Runtime root resolution has been switched to enterprise root when canonical assets are ready.
- Root `pyproject.toml` is active: pytest collects service tests and `tests/regression`, ruff/mypy run from enterprise root.
- `iztro` Node dependencies build under `infra/runtime/local-state/vendor-build/` instead of mutating `tools/reference-repos`.
- Full enterprise root acceptance is green; remaining risk is compatibility box retirement, not runtime-root readiness.
