# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不把本地 contract gate 等同于真实 live release。
- [x] `contracts/fate/delivery/release-gate.json` 已新增。
- [x] `contracts/fate/delivery/schemas/release-gate.schema.json` 已新增。
- [x] `contracts/fate/delivery/registry.json` 已引用 releaseGate。
- [x] `contracts/fate/capabilities/schemas/resource.schema.json` 已声明 `ReleaseGate`。
- [x] `scripts/live-release-gate.py` / `scripts/live-release-gate.sh` 已新增。
- [x] `scripts/public-release-gate.sh` 已输出 `live-release-gate.json`。
- [x] `scripts/local-ci.sh --profile quick` 已包含 live release gate contract step 与回归测试。
- [x] `/surfaces` API payload 已暴露 `releaseGate`。
- [x] `tests/regression/test_live_release_gate.py` 覆盖 local mode 和 require-live failure。
- [x] 文档同步 `contracts/fate/delivery/AGENTS.md`、`scripts/AGENTS.md`、API 接入文档、100% roadmap。
- [x] 外部证据缺失明确标注：真实 API、HF Space、Bot、CI、container digest、SBOM/provenance、rollback drill。
- [x] 不输出真实密钥，不伪造 live 通过。

# Task Package Checklists

## TP-01.01
- [x] 现有发布、HF、Bot、container、CI 入口已盘点。
- Verify: `sed -n` / `rg -n` 检查相关脚本和 workflow。
- Gate: 真实外部证据缺口明确。

## TP-02.01
- [x] ReleaseGate schema 与 contract 已新增。
- Verify: `python3 -m json.tool contracts/fate/delivery/release-gate.json`。
- Gate: requiredEvidence 覆盖 local CI、remote CI、API、HF、Bot、container、SBOM、provenance、rollback、git。

## TP-02.02
- [x] delivery registry 与 resource schema 已接入。
- Verify: `rg -n "ReleaseGate|releaseGate" contracts/fate`。
- Gate: `/surfaces` registry 有 releaseGate 元信息。

## TP-03.01
- [x] `live-release-gate` 执行器已新增并可输出 JSON。
- Verify: `bash scripts/live-release-gate.sh --output-json /tmp/fatecat-live-release-gate-0039.json`。
- Gate: local mode exit 0 且 `shipGate=blocked`。

## TP-03.02
- [x] public-release/local-ci 已接入。
- Verify: `rg -n "live-release-gate" scripts/public-release-gate.sh scripts/local-ci.sh`。
- Gate: public release 产出 JSON，quick CI 覆盖合同检查。

## TP-04.01
- [x] release gate 回归测试已新增。
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py`。
- Gate: local pass、require-live fail、敏感输出边界均覆盖。

## TP-04.02
- [x] `/surfaces` releaseGate 元信息已暴露。
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py::test_delivery_surfaces_are_discoverable_and_linked`。
- Gate: API payload 包含 releaseGate。

## TP-05.01
- [x] AGENTS、API 文档和 roadmap 已同步。
- Verify: `rg -n "live-release-gate|ReleaseGate|releaseGate" contracts/fate/delivery/AGENTS.md scripts/AGENTS.md docs/reference-materials`。
- Gate: 文档明确外部连通验证待执行。

## TP-05.02
- [x] 验证命令与 closeout 已执行或待本文件校验后生成。
- Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py`。
- Gate: 任务文档无占位符，closeout ready。
