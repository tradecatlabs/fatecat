# Acceptance Checklist

# Global Standards
- [x] 默认 Markdown 仍只有 `bazi`
- [x] production capability 必须 passing testGate
- [x] planned capability 必须 blocked 且不可执行
- [x] API developer discovery 可复核
- [x] API 接入文档已落入 operations 分区
- [x] quick CI 通过
- [x] governance strict 通过
- [x] task docs validator 通过
- [x] git diff hygiene 通过

# Task Package Checklists
## TP-01.01 metadata developer discovery

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k metadata`

Gate: `/metadata` 包含 developer、privacy、productionGate。

- [x] 新增 developer 字段。
- [x] 新增 privacy 字段。
- [x] 新增 productionGate 字段。

## TP-01.02 API 接入文档

Verify: `test -f docs/reference-materials/operations/测算基础设施\ API\ 接入.md`

Gate: 文档覆盖开发者接入最小路径。

- [x] 新增 API 接入文档。
- [x] 更新 docs/reference-materials 索引。

## TP-02.01 registry admission rules

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k admission`

Gate: production/planned 不变量由代码强制。

- [x] 新增 `_validate_capability_admission()`。
- [x] schema invariants 同步。

## TP-02.02 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi'`

Gate: 定向回归通过。

- [x] capability 准入测试通过。
- [x] OpenAPI discovery 测试通过。

## TP-03.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: quick CI、governance、task docs、git hygiene 通过。

- [x] quick CI 通过。
- [x] governance strict 通过。
- [x] task docs validator 通过。
- [x] git diff --check 通过。

## TP-03.02 git control

Verify: `git status --short --branch && git log -1 --oneline`

Gate: 提交推送后远端同步。

- [x] 本地提交。
- [x] 推送远端。
