# Execution Checklist
[x] TP-01.01 | P0 | 盘点 source_manifest、copyright_review、vendor_sources、evaluation registry 和 data-products 目录 | Verify: `rg -n "source_manifest|copyright_review|vendor_sources|Dataset|MI-06" domains tools contracts docs` | Gate: 数据供应链现状和缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 data-supply-chain registry/schema/AGENTS | Verify: `test -f contracts/fate/data-supply-chain/registry.json && test -f contracts/fate/data-supply-chain/schemas/data-supply-chain.schema.json` | Gate: registry 和 schema 存在 | Parallelizable: No
[x] TP-02.02 | P0 | 补齐 canonical classics source/copyright manifest 覆盖 | Verify: `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate.json` | Gate: canonical classics coverage complete | Parallelizable: No
[x] TP-03.01 | P0 | 新增 data-supply-chain-gate 脚本和 shell wrapper | Verify: `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate.json` | Gate: status passed | Parallelizable: No
[x] TP-03.02 | P0 | 新增 gate pytest 并接入 quick local-ci | Verify: `.venv/bin/python -m pytest -q tests/regression/test_data_supply_chain_gate.py` | Gate: focused pytest passes and local-ci hook exists | Parallelizable: No
[x] TP-04.01 | P1 | 同步 API 文档、roadmap、contracts/data-products/scripts AGENTS | Verify: `rg -n "data-supply-chain|data supply chain|供应链门禁|0035" contracts docs domains scripts governance/tasks/INDEX.md` | Gate: 不夸大法律意见或 SBOM/provenance | Parallelizable: No
[x] TP-04.02 | P0 | 运行 gate、pytest、ruff、format、quick CI | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-data-supply-chain` | Gate: quick CI passes | Parallelizable: No
[x] TP-04.03 | P0 | 生成任务 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0035-measurement-infrastructure-data-supply-chain --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
