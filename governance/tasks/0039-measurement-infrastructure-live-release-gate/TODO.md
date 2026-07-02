# Execution Checklist

[x] TP-01.01 | P0 | 盘点现有发布、HF、Bot、container、CI 入口 | Verify: `sed -n` / `rg -n` 检查相关脚本和 workflow | Gate: 真实外部证据缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 ReleaseGate schema 与 contract | Verify: `python3 -m json.tool contracts/fate/delivery/release-gate.json` | Gate: requiredEvidence 覆盖 local CI、remote CI、API、HF、Bot、container、SBOM、provenance、rollback、git | Parallelizable: No
[x] TP-02.02 | P0 | 接入 delivery registry 和 resource schema | Verify: `rg -n "ReleaseGate|releaseGate" contracts/fate` | Gate: `/surfaces` registry 有 releaseGate 元信息 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 `live-release-gate` 执行器 | Verify: `bash scripts/live-release-gate.sh --output-json /tmp/fatecat-live-release-gate-0039.json` | Gate: local mode exit 0 且 `shipGate=blocked` | Parallelizable: No
[x] TP-03.02 | P0 | 接入 public-release/local-ci | Verify: `rg -n "live-release-gate" scripts/public-release-gate.sh scripts/local-ci.sh` | Gate: public release 产出 JSON，quick CI 覆盖合同检查 | Parallelizable: No
[x] TP-04.01 | P0 | 增加 release gate 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py` | Gate: local pass、require-live fail、敏感输出边界均覆盖 | Parallelizable: No
[x] TP-04.02 | P0 | 暴露 `/surfaces` releaseGate 元信息 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py::test_delivery_surfaces_are_discoverable_and_linked` | Gate: API payload 包含 releaseGate | Parallelizable: No
[x] TP-05.01 | P0 | 同步 AGENTS、API 文档和 roadmap | Verify: `rg -n "live-release-gate|ReleaseGate|releaseGate" contracts/fate/delivery/AGENTS.md scripts/AGENTS.md docs/reference-materials` | Gate: 文档明确外部连通验证待执行 | Parallelizable: No
[x] TP-05.02 | P0 | 运行验证并生成 closeout | Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py` | Gate: 任务文档无占位符，closeout ready | Parallelizable: No
