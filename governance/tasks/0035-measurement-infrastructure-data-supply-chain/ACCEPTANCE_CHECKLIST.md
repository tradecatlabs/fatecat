# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不混入法律意见、SBOM 或生产部署。
- [x] 隐私边界明确，不读取 raw 私有资料或真实用户数据。
- [x] review_required 不被宣称为 production allowed。
- [x] quick CI 通过。
- [x] task closeout packet 生成。

# Task Package Checklists

## TP-01.01 现状审计
Verify: `rg -n "source_manifest|copyright_review|vendor_sources|Dataset|MI-06" domains tools contracts docs`

Gate: 数据供应链现状和缺口明确。

- [x] 已盘点 source/copyright/vendor/evaluation registry。

## TP-02.01 data-supply-chain registry/schema
Verify: `test -f contracts/fate/data-supply-chain/registry.json && test -f contracts/fate/data-supply-chain/schemas/data-supply-chain.schema.json`

Gate: registry 和 schema 存在。

- [x] 已新增 registry/schema/AGENTS。

## TP-02.02 classics manifest coverage
Verify: `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate.json`

Gate: 14 个 canonical TXT 均有 source/copyright/hash coverage。

- [x] 已补齐 canonical classics manifest 与 copyright review。

## TP-03.01 gate runtime
Verify: `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate.json`

Gate: gate status passed。

- [x] data supply chain gate 已通过。

## TP-03.02 pytest/local-ci hook
Verify: `.venv/bin/python -m pytest -q tests/regression/test_data_supply_chain_gate.py`

Gate: focused pytest passes，local-ci hook 存在。

- [x] focused pytest 已通过，local-ci hook 已接入。

## TP-04.01 docs sync
Verify: `rg -n "data-supply-chain|data supply chain|供应链门禁|0035" contracts docs domains scripts governance/tasks/INDEX.md`

Gate: 文档不夸大法律意见或 SBOM/provenance。

- [x] contracts/data-products/scripts/API/roadmap 文档已同步。

## TP-04.02 quick CI
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-data-supply-chain`

Gate: quick CI passes。

- [x] quick CI 已通过，110 passed。

## TP-04.03 closeout
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0035-measurement-infrastructure-data-supply-chain --phase closeout`

Gate: closeout packet 写入任务目录。

- [x] closeout validator 已通过，`TASK_CLOSEOUT_PACKET.json` 已生成。
