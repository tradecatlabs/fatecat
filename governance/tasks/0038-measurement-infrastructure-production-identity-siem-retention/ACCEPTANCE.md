# Task-Level Acceptance
- `production-security-policy.json` 存在，覆盖 identity、SIEM、retention 和 OWASP API Security Top 10 2023。
- SecurityControl schema 支持 `identity`、`siem`、`owasp_api_regression`。
- Security registry 登记 `control.production_identity_oidc`、`control.external_siem_immutable_audit`、`control.retention_cleanup_plan` 和 `control.owasp_api_security_regression`。
- Manual controls 必须标记外部连通待验证，不得宣称真实 OIDC/SIEM/cleanup 已完成。
- `production-security-gate` 可执行并输出机器可读 JSON。
- `production-readiness.sh` 在显式启用公网多租户、SIEM export 或 record retention days 时检查必需配置；默认 public-service 静态验收不被破坏。
- API/protocol tests、security smoke 和 quick CI 通过。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/security/registry.json contracts/fate/security/schemas/security-control.schema.json contracts/fate/security/production-security-policy.json` | Passed |
| shell syntax | `bash -n scripts/production-security-gate.sh scripts/security-smoke.sh scripts/production-readiness.sh scripts/local-ci.sh` | Passed |
| production security gate | `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-gate-0038.json` | Passed; controls=4, owaspCoverageCount=10, checks=49 |
| ruff check/format | `ruff check/format` on production security gate and changed tests | Passed |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_production_security_gate.py tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Passed; 90 passed |
| production readiness static | `env FATE_CORS_ALLOW_ORIGINS=https://fatecat.tradecatlabs.example FATE_RECORDS_ENABLED=0 FATE_DEPLOYMENT_REPLICAS=1 FATE_RATE_LIMIT_BACKEND=gateway FATE_EDGE_BODY_LIMIT_ENABLED=1 FATE_TRUST_PROXY_HEADERS=1 FATE_ENABLE_HSTS=1 bash scripts/production-readiness.sh --skip-bootstrap` | Passed with external warnings |
| security smoke | `bash scripts/security-smoke.sh --skip-file-gates --output-json /tmp/fatecat-security-smoke-0038.json` | Passed; checks=16 |
| local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0038` | Passed; 118 regression passed |

# Review Gate
- Correctness: gate validates required controls, required env var names, OWASP 10/10 coverage and policy blockers.
- Security: output does not print real env values; registry/manual controls keep external validation pending.
- Privacy: policy/registry/gate do not store real token、secret、DSN、endpoint、payload or report body.
- Architecture: reuses existing SecurityControl registry and API endpoints; no new parallel security API.
- Performance: gate is local JSON validation, no network calls; negligible CI cost.

# Runtime Verification Gate
- `/security` API exposes new controls via existing registry path.
- `production-security-gate` verifies policy/registry/schema locally.
- `production-readiness` verifies static admission defaults still pass without real external services.
- 外部连通验证待执行：真实 OIDC/IdP、SIEM、immutable audit storage、record cleanup scheduler、live API/Bot。

# Ship Readiness
- 当前 0038 本地切片可进入审计：contracts、scripts、tests、quick CI、docs 和 task closeout 均有本地证据。
- 不能声明生产安全 100%：缺真实 OIDC/SIEM/retention cleanup/live smoke/third-party security audit。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | production security policy、schema 和 registry 控制项落地。 |
| TP-03 | production-security gate 和 production-readiness 静态准入落地。 |
| TP-04 | regression tests、quick CI、docs、AGENTS 和 env examples 同步。 |
| TP-05 | focused validation、local quick CI 和 closeout 完成。 |

# Anti-Goals
- 不接真实 OIDC/IdP、SIEM、WORM 或云日志平台。
- 不删除真实用户数据。
- 不输出真实 token、secret、DSN、endpoint、请求体、用户输入或报告正文。
- 不声明真实生产身份、不可变审计存储、自动清理或 live smoke 已完成。
