# Task-Level Acceptance

## Acceptance Criteria

- `sandbox-access-gateway.json` 存在并明确 `livePublicTokenServiceStatus=not_implemented`。
- `sandbox-token-contract.json` 链接本地 gateway contract，但仍保持 `liveServiceStatus=not_implemented`。
- `src/main.py` 提供 sandbox endpoint，缺 token 和错 scope 均拒绝。
- 成功 sandbox 请求通过 `CapabilityExecutor` 返回 capability response。
- gate 证明限流可拒绝第二个请求。
- gate 证明 audit event 已发出且不包含 token 或 raw subject。
- OpenAPI 暴露 sandbox gateway path。
- local-ci quick 接入新 gate 和 regression。
- 文档和 AGENTS 同步，不宣称公网 token service。

## Validation Commands

```bash
bash scripts/sandbox-access-gateway-gate.sh --output-json /tmp/fatecat-sandbox-access-gateway-gate-0087.json
bash scripts/developer-platform-gate.sh --output-json /tmp/fatecat-developer-platform-gate-0087.json
bash scripts/developer-portal-gate.sh --output-json /tmp/fatecat-developer-portal-gate-0087.json
.venv/bin/python -m pytest -q tests/regression/test_sandbox_access_gateway_gate.py tests/regression/test_developer_platform_gate.py tests/regression/test_developer_portal_gate.py
env RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache .venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/sandbox-access-gateway-gate.py scripts/developer-platform-gate.py scripts/developer-portal-gate.py tests/regression/test_sandbox_access_gateway_gate.py tests/regression/test_developer_platform_gate.py tests/regression/test_developer_portal_gate.py
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0087
```

## Current Evidence

- Gate smoke: `bash scripts/sandbox-access-gateway-gate.sh --output-json /tmp/fatecat-sandbox-access-gateway-gate-0087.json` passed with `checks=20`, `localGatewayExecutable=true`, `livePublicTokenService=false`.
- Developer platform gate: `bash scripts/developer-platform-gate.sh --output-json /tmp/fatecat-developer-platform-gate-0087.json` passed with `checks=92`, `localSandboxGateway=true`.
- Developer portal gate: `bash scripts/developer-portal-gate.sh --output-json /tmp/fatecat-developer-portal-gate-0087.json` passed with `checks=63`.
- Focused pytest: `.venv/bin/python -m pytest -q tests/regression/test_sandbox_access_gateway_gate.py tests/regression/test_developer_platform_gate.py tests/regression/test_developer_portal_gate.py` passed, `7 passed`.
- Ruff: `ruff check` and `ruff format --check` passed for touched Python files.
- Secret scan: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0087.json` passed with `findingCount=0`.
- Quick CI: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0087` passed, `249 passed in 115.44s`.
- Remote CI: pending commit/push; do not claim before GitHub Actions run exists.

# Validation Plan

- Run the new sandbox gateway gate directly.
- Run developer platform and portal gates to catch contract drift.
- Run focused regression covering new and updated tests.
- Run secret scan and quick CI before commit.

# Review Gate

- No token, subject, request body, report body or production URL appears in gate summary.
- Existing public capability endpoint remains compatible.
- Docs explicitly keep public token issuer/revocation/external gateway as future work.

# Runtime Verification Gate

- Missing token returns 403.
- Wrong scope returns 403.
- Allowed scope returns 200 through `CapabilityExecutor`.
- Forced `RATE_LIMIT_PER_MINUTE=1` rejects second request with 429.
- Audit event action `sandbox.capability.calculate` is captured without raw token or subject.

# Ship Readiness

- Local gate and quick CI passed.
- Task docs validate in closeout phase.
- Remote acceptance must be triggered after commit/push and reported separately.

# Task Package Acceptance

## TP-01 SPEC

Accepted: existing gap identified.

## TP-02 PLAN

Accepted: local gateway baseline defined.

## TP-03 BUILD

Accepted: code, contracts, docs, tests and wiring implemented.

## TP-04 TEST

Accepted: local validation passed.

## TP-05 SHIP

Accepted locally: closeout ready for commit/push.

# Anti-Goals

- Do not issue real sandbox tokens.
- Do not claim external gateway live evidence.
- Do not publish SDK packages.
- Do not change bazi/ziwei report semantics.
