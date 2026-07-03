# Task Plan

## Phase 1 - SPEC

- 复核 `contracts/fate/security/registry.json`、`production-security-policy.json`、`externalization-evidence-contract.json` 中 retention 现状。
- 确认已有计划未落本地清理器，生产 live 仍外部 pending。

## Phase 2 - PLAN

- 选择本地 SQLite records/report jobs 作为最小可执行 baseline。
- 规定 audit/SIEM retention 只输出 `external_connectivity_pending`。
- 规定 summary 脱敏边界和 `dry-run` 默认行为。

## Phase 3 - BUILD

- 新增 delivery 层 `retention_cleanup.py`。
- 新增 root scripts runner 和 smoke。
- 新增 security contract，更新 registry/policy/externalization contract。
- 接入 production-security gate、local-ci、回归测试和 AGENTS。

## Phase 4 - TEST

- `bash scripts/retention-cleanup-smoke.sh --output-json <path> --pretty`
- `python3 -m pytest -q tests/regression/test_retention_cleanup.py`
- `python3 -m pytest -q tests/regression/test_production_security_gate.py`
- `ruff check` / `ruff format --check` changed Python files
- `bash scripts/secret-scan.sh --output-json <path>`
- `bash scripts/local-ci.sh --profile quick --output <dir>`

## Phase 5 - SHIP

- 提交并推送当前切片。
- 触发远端 Acceptance 和 Container workflows。
- 当前 release proof / audit bundle 必须在 commit 后刷新。
