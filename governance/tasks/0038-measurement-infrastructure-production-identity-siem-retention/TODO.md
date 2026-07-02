# Execution Checklist
[x] TP-01.01 | P0 | 盘点 D8 安全/隐私现状、security registry、production readiness 和 roadmap 缺口 | Verify: `rg -n "OIDC|SIEM|retention|OWASP|production" contracts/fate/security scripts docs/reference-materials/roadmap` | Gate: D8 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 production security policy | Verify: `python3 -m json.tool contracts/fate/security/production-security-policy.json` | Gate: policy JSON 可解析且覆盖 identity/SIEM/retention/OWASP | Parallelizable: No
[x] TP-02.02 | P0 | 扩展 SecurityControl schema 和 registry 控制项 | Verify: `python3 -m json.tool contracts/fate/security/registry.json contracts/fate/security/schemas/security-control.schema.json` | Gate: registry 包含 4 个新控制项 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 production-security-gate | Verify: `bash scripts/production-security-gate.sh --output-json /tmp/fatecat-production-security-gate-0038.json` | Gate: gate passed | Parallelizable: No
[x] TP-03.02 | P0 | 扩展 production-readiness 静态准入检查 | Verify: `env FATE_CORS_ALLOW_ORIGINS=https://fatecat.tradecatlabs.example FATE_RECORDS_ENABLED=0 FATE_DEPLOYMENT_REPLICAS=1 FATE_RATE_LIMIT_BACKEND=gateway FATE_EDGE_BODY_LIMIT_ENABLED=1 FATE_TRUST_PROXY_HEADERS=1 FATE_ENABLE_HSTS=1 bash scripts/production-readiness.sh --skip-bootstrap` | Gate: 默认 public-service 静态门禁通过且外部项 warning | Parallelizable: No
[x] TP-04.01 | P0 | 新增/更新 regression tests 并接入 quick CI | Verify: `.venv/bin/python -m pytest -q tests/regression/test_production_security_gate.py tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Gate: focused pytest passed | Parallelizable: No
[x] TP-04.02 | P0 | 同步 env 示例、AGENTS、API 文档和 roadmap | Verify: `rg -n "production-security-gate|OIDC|SIEM|OWASP" infra/environments contracts/fate/security docs/reference-materials scripts/AGENTS.md` | Gate: 文档明确 contract baseline 和外部 pending | Parallelizable: Yes
[x] TP-05.01 | P0 | 运行 focused validation 和 local quick CI | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0038` | Gate: quick CI passed | Parallelizable: No
[x] TP-05.02 | P0 | 回填任务包并生成 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0038-measurement-infrastructure-production-identity-siem-retention --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
