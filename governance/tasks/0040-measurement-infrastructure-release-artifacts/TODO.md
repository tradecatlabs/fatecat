# Execution Checklist

[x] TP-01.01 | P0 | 盘点 SBOM/provenance 现状和 0039 gate 接口 | Verify: `rg -n "SBOM|provenance|release artifact"` | Gate: 缺口来自真实文件 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 release artifact 生成脚本 | Verify: `rg -n "release-artifacts" scripts` | Gate: shell/Python 入口存在 | Parallelizable: No
[x] TP-02.02 | P0 | 生成并校验 SBOM/provenance/manifest | Verify: `bash scripts/release-artifacts.sh --output-dir /tmp/fatecat-release-artifacts-0040` | Gate: 3 个 JSON artifact 存在且 verify 通过 | Parallelizable: No
[x] TP-03.01 | P0 | 接入 public-release/local-ci | Verify: `rg -n "release-artifacts" scripts/public-release-gate.sh scripts/local-ci.sh` | Gate: release gate 消费生成路径 | Parallelizable: No
[x] TP-03.02 | P0 | 验证 live release gate 消费 artifact | Verify: `bash scripts/live-release-gate.sh --sbom-path ... --provenance-path ...` | Gate: SBOM/provenance checks 为 pass | Parallelizable: No
[x] TP-04.01 | P0 | 新增回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_release_artifacts.py` | Gate: 生成、verify、gate 消费都覆盖 | Parallelizable: No
[x] TP-04.02 | P0 | 同步合同、AGENTS、API 文档和 roadmap | Verify: `rg -n "release-artifacts|SBOM/provenance" contracts/fate/delivery scripts/AGENTS.md docs/reference-materials` | Gate: 文档明确不是远端 attestation | Parallelizable: No
[x] TP-05.01 | P0 | 运行验证并生成 closeout | Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py` | Gate: 任务文档无占位符，closeout ready | Parallelizable: No
