# Acceptance Checklist

# Global Standards
- [x] 无真实 token、secret、DSN、私钥、证书或 webhook 值进入 registry、docs 或 tests。
- [x] 需要真实域名、真实 token、Bot live smoke 或云端权限的内容均标注外部连通验证待执行。
- [x] 新增 API 是只读发现层，不改变现有鉴权/限流/发布脚本行为。
- [x] API 文档、100% 路线图、contracts AGENTS 与 schema 保持同一口径。

# Task Package Checklists

## TP-01.01 盘点现有控制
- [x] Verify: `rg -n "FATE_API|FATE_RATE|FATE_MAX|CORS|HSTS|nosniff|privacy|source hygiene|production" domains scripts tests`
- [x] Gate: 已确认现有 main.py、service_config.py 与 scripts 门禁入口。

## TP-01.02 回填任务契约
- [x] Verify: `validate_task_docs.py --phase decompose`
- [x] Gate: 任务文档无占位符且依赖图可解析。

## TP-02.01 新增 SecurityControl schema
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'security or resource'`
- [x] Gate: 必填字段、controlType、status、externalConnectivity 和 invariants 有断言。

## TP-02.02 新增 security registry
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k security`
- [x] Gate: registry 覆盖 auth、cors、rate_limit、request_limit、headers、privacy、source_hygiene、release_gate、production_readiness。

## TP-02.03 扩展 resource schema 与 AGENTS
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource`
- [x] Gate: resource schema 包含 `SecurityControl` 和 `securityControlResourceFields`。

## TP-03.01 新增 `/security` list/detail API
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k security`
- [x] Gate: canonical 与 alias 返回一致，detail 可按 id 查询。

## TP-03.02 更新 `/metadata` 与 OpenAPI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or security'`
- [x] Gate: metadata developer links 和 OpenAPI paths 包含 security。

## TP-04.01 补 contract/API 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'security or resource or metadata or openapi'`
- [x] Gate: focused tests 全部通过。

## TP-04.02 更新文档和路线图
- [x] Verify: `rg -n "SecurityControl|/security|production_readiness|外部连通验证待执行" docs contracts governance/tasks/0019-measurement-infrastructure-wave5-security-privacy-resources`
- [x] Gate: 人类文档与 API/契约一致。

## TP-05.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-05.02 回填 closeout 状态和验证证据
- [x] Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto`
- [x] Gate: 0019 closeout 和全任务树校验通过。
