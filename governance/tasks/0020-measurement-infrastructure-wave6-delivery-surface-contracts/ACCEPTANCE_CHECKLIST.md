# Acceptance Checklist

# Global Standards
- [x] 无用户输入、报告正文、真实 token、secret、DSN、私钥、生产日志进入 registry、docs 或 tests。
- [x] Bot live、HF Space、公网 API 和浏览器 live 均标注外部连通验证待执行。
- [x] 新增 API 是只读发现层，不改变 Web/API/Bot/CLI/Skill 执行行为。
- [x] API 文档、100% 路线图、contracts AGENTS 与 schema 保持同一口径。

# Task Package Checklists

## TP-01.01 盘点现有交付面
- [x] Verify: `rg -n "reportSystem|generate_full_report|build_web_report_result|Telegram|Bot|CLI|Skill|/web|/api/v1/report" apps ai domains contracts docs references scripts tests`
- [x] Gate: 已确认现有 API/Web/Bot/CLI/Skill/HF 入口和缺失发现层。

## TP-01.02 回填任务契约
- [x] Verify: `validate_task_docs.py --phase decompose`
- [x] Gate: 任务文档无占位符且依赖图可解析。

## TP-02.01 新增 DeliverySurface schema
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'surface or resource'`
- [x] Gate: 必填字段、surfaceType、status、externalConnectivity 和 invariants 有断言。

## TP-02.02 新增 delivery registry
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k surface`
- [x] Gate: registry 覆盖 api、web、bot、cli、skill、hosted_web。

## TP-02.03 扩展 resource schema 与 AGENTS
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource`
- [x] Gate: resource schema 包含 `DeliverySurface` 和 `deliverySurfaceResourceFields`。

## TP-03.01 新增 `/surfaces` list/detail API
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k surface`
- [x] Gate: canonical 与 alias 返回一致，detail 可按 id 查询。

## TP-03.02 更新 `/metadata` 与 OpenAPI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or surface'`
- [x] Gate: metadata developer links 和 OpenAPI paths 包含 surfaces。

## TP-04.01 补 contract/API/entrypoint 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py tests/regression/test_entrypoint_consistency.py -k 'surface or resource or metadata or openapi or entrypoint'`
- [x] Gate: focused tests 全部通过。

## TP-04.02 更新文档和路线图
- [x] Verify: `rg -n "DeliverySurface|/surfaces|surface\\.telegram_bot|surface\\.cli|外部连通验证待执行" docs contracts governance/tasks/0020-measurement-infrastructure-wave6-delivery-surface-contracts`
- [x] Gate: 人类文档与 API/契约一致。

## TP-05.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-05.02 回填 closeout 状态和验证证据
- [x] Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto`
- [x] Gate: 0020 closeout 和全任务树校验通过。
