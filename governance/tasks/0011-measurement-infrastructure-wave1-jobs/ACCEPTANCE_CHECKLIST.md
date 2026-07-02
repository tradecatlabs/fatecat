# Acceptance Checklist

# Global Standards
- [x] Idempotency-Key 支持
- [x] cancelled 状态支持
- [x] cancel API 支持
- [x] job payload resource links 支持
- [x] 文档记录单进程/TTL 边界
- [x] 定向测试通过
- [x] quick CI 通过
- [x] governance strict 通过
- [x] task closeout 通过

# Task Package Checklists
## TP-01.01 Idempotency-Key

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k idempotency`

Gate: 同一 key 返回同一 jobId。

- [x] 已通过。

## TP-01.02 cancelled status

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k cancelled`

Gate: cancel 后状态保持 cancelled。

- [x] 已通过。

## TP-02.01 job resource links

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k report_job`

Gate: payload 包含 resourceType、links、cancelUrl。

- [x] 已通过。

## TP-02.02 cancel API

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k cancel`

Gate: cancel endpoint 可用。

- [x] 已通过。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error or report_job'`

Gate: 综合定向回归通过。

- [x] 29 passed。

## TP-03.02 docs

Verify: `rg -n "Idempotency-Key|cancelled|cancel" docs/reference-materials/operations/测算基础设施\ API\ 接入.md contracts/fate/capabilities/schemas/resource.schema.json`

Gate: 文档和 schema 同步。

- [x] 已同步。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: 本地门禁通过。

- [x] quick CI 通过。
- [x] governance strict 通过。
- [x] git diff --check 通过。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0011-measurement-infrastructure-wave1-jobs --phase closeout`

Gate: 任务 closeout 通过。

- [x] closeout 通过。
