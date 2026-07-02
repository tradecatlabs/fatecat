# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不混入真实 OIDC/SIEM/live smoke 或数据删除。
- [x] production security policy、registry、gate 三者一致。
- [x] OWASP API Security Top 10 2023 映射覆盖 10/10。
- [x] gate output 不泄露真实 secret、endpoint、请求体或报告正文。
- [x] quick CI hook 已接入并通过。
- [x] task closeout packet 生成。

# Task Package Checklists
## TP-01.01 现状审计
Verify: `rg -n "OIDC|SIEM|retention|OWASP|production" contracts/fate/security scripts docs/reference-materials/roadmap`

Gate: D8 缺口明确。

- [x] 已盘点 security registry、security smoke、production readiness 和 D8 roadmap。

## TP-02.01 production security policy
Verify: `python3 -m json.tool contracts/fate/security/production-security-policy.json`

Gate: policy JSON 可解析且覆盖 identity/SIEM/retention/OWASP。

- [x] `production-security-policy.json` 已新增。

## TP-02.02 security schema/registry
Verify: `python3 -m json.tool contracts/fate/security/registry.json contracts/fate/security/schemas/security-control.schema.json`

Gate: registry 包含 4 个新控制项。

- [x] schema 支持 `identity`、`siem`、`owasp_api_regression`。
- [x] registry 新增 production identity、external SIEM、retention cleanup 和 OWASP regression controls。

## TP-03.01 production-security-gate
Verify: `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-gate-0038.json`

Gate: gate passed。

- [x] production security gate passed，controls=4，owaspCoverageCount=10，checks=49。

## TP-03.02 production-readiness static checks
Verify: `env FATE_CORS_ALLOW_ORIGINS=https://fatecat.tradecatlabs.example FATE_RECORDS_ENABLED=0 FATE_DEPLOYMENT_REPLICAS=1 FATE_RATE_LIMIT_BACKEND=gateway FATE_EDGE_BODY_LIMIT_ENABLED=1 FATE_TRUST_PROXY_HEADERS=1 FATE_ENABLE_HSTS=1 bash scripts/production-readiness.sh --skip-bootstrap`

Gate: 默认 public-service 静态门禁通过且外部项 warning。

- [x] production-readiness static check passed。

## TP-04.01 tests/CI
Verify: `.venv/bin/python -m pytest -q tests/regression/test_production_security_gate.py tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`

Gate: focused pytest passed。

- [x] focused pytest passed，90 passed。
- [x] `local-ci.sh --profile quick` includes production-security-gate and test file。

## TP-04.02 docs/env/AGENTS
Verify: `rg -n "production-security-gate|OIDC|SIEM|OWASP" infra/environments contracts/fate/security docs/reference-materials scripts/AGENTS.md`

Gate: 文档明确 contract baseline 和外部 pending。

- [x] env examples、AGENTS、API docs、roadmap 已同步。

## TP-05.01 validation
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0038`

Gate: quick CI passed。

- [x] local quick CI passed；118 regression passed。

## TP-05.02 closeout
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0038-measurement-infrastructure-production-identity-siem-retention --phase closeout`

Gate: closeout packet 写入任务目录。

- [x] closeout validator 通过，`TASK_CLOSEOUT_PACKET.json` 已生成。
