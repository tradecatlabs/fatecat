# Task-Level Acceptance

## Acceptance Criteria

- `contracts/fate/audit/current-bundle.json` exists and defines required outputs, evidence sources, gate policy and privacy boundary.
- `scripts/current-audit-bundle.py/.sh` exists and writes:
  - `current-audit-bundle.json`
  - `CURRENT_AUDIT_BUNDLE.md`
  - `evidence-index.json`
  - `risk-register.json`
  - `pending-external-validations.json`
- Local mode can generate a structurally valid blocked bundle from local-contract evidence.
- Required mode fails when passed local-contract current release proof.
- Required mode passes only when supplied local-ci summary/current release proof/evidence artifacts match current HEAD and pass.
- `scripts/local-ci.sh --profile quick` generates rollback drill, current release proof local contract and current audit bundle, and records them in `summary.json`.
- Regression verifies contract behavior, wiring and sensitive marker protection.
- Final delivery closeout includes remote current commit acceptance/container evidence, required current release proof and required current audit bundle JSON/Markdown paths.

## Validation Commands

```bash
env RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache .venv/bin/python -m ruff format --check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py
env RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache .venv/bin/python -m ruff check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py
.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py tests/regression/test_audit_handoff.py tests/regression/test_audit_handoff_dry_run.py tests/regression/test_current_release_proof.py tests/regression/test_release_artifacts.py tests/regression/test_rollback_drill.py
bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0089.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0089
```

## Current Evidence

- Focused pytest: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py` passed, `4 passed`.
- Audit/release focused pytest: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py tests/regression/test_audit_handoff.py tests/regression/test_audit_handoff_dry_run.py tests/regression/test_current_release_proof.py tests/regression/test_release_artifacts.py tests/regression/test_rollback_drill.py` passed, `18 passed`.
- Ruff: `ruff check` and `ruff format --check` passed for `scripts/current-audit-bundle.py` and `tests/regression/test_current_audit_bundle.py`.
- Secret scan: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0089.json` passed with `findingCount=0`.
- Quick CI: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0089-precommit` passed, `258 passed`.
- Local current audit bundle: `/tmp/fatecat-local-ci-0089-precommit/current-audit-bundle/current-audit-bundle.json` generated with `auditGate=blocked`, `blockingItems=["git.clean"]`, `pendingExternalValidationCount=291`, as expected before final commit.
- Final required current audit bundle: handled by delivery flow after commit/push against final HEAD.

# Validation Plan

- Run focused tests first to catch contract/script mistakes.
- Run ruff and format check for new Python files.
- Run secret scan to ensure no sensitive markers.
- Run quick CI to prove local-ci wiring.
- After push, run required current release proof and required current audit bundle on final HEAD.

# Review Gate

- current audit bundle must not accept old commit evidence.
- current audit bundle must not hide `外部连通验证待执行` records.
- current audit bundle required mode must not accept local-contract proof.
- current audit bundle output must not include token/secret/password/private key marker assignments.

# Runtime Verification Gate

- Local quick CI gate proves local current audit bundle generation only.
- Required current audit bundle gate proves final HEAD audit bundle only after current release proof has passed.
- Third-party audit remains separate human/external verification.

# Ship Readiness

- Local focused tests passed.
- Local quick CI passed.
- Remote acceptance/container for final commit passed.
- Required current release proof for final commit passed.
- Required current audit bundle for final commit passed.

# Task Package Acceptance

## TP-01 SPEC

Accepted when 0089 audit aggregation gap is proven from current roadmap/state.

## TP-02 PLAN

Accepted when evidence boundary, local/required modes and anti-overclaim rules are documented.

## TP-03 BUILD

Accepted when scripts, contract, docs, local-ci wiring and regression exist.

## TP-04 TEST

Accepted when local validation passes.

## TP-05 SHIP

Accepted when repository contains current audit bundle gate and final commit delivery flow can generate required current audit bundle without follow-up source commit.

# Anti-Goals

- Do not claim production API/HF/Bot live.
- Do not execute production rollback.
- Do not store or print GitHub/registry credentials.
- Do not accept historical release or audit proof.
- Do not replace third-party audit with self-generated bundle.
