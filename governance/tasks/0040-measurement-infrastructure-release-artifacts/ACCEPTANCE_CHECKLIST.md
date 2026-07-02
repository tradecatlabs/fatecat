# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不把本地 SBOM/provenance baseline 等同于远端发布证明。
- [x] `scripts/release-artifacts.py` 已新增。
- [x] `scripts/release-artifacts.sh` 已新增。
- [x] `scripts/public-release-gate.sh` 已接入 release artifacts。
- [x] `scripts/local-ci.sh --profile quick` 已接入 release artifacts 和回归测试。
- [x] `contracts/fate/delivery/release-gate.json` 已登记 release-artifacts localVerification。
- [x] `contracts/fate/delivery/registry.json` 已登记 release-artifacts localVerification。
- [x] `tests/regression/test_release_artifacts.py` 已新增。
- [x] 文档同步 `contracts/fate/delivery/AGENTS.md`、`scripts/AGENTS.md`、API 接入文档、100% roadmap。
- [x] 不输出真实密钥，不伪造 registry/CI/container 证据。

# Task Package Checklists

## TP-01.01
- [x] 0039 gate 和供应链缺口已盘点。
- Verify: `rg -n "SBOM|provenance|release artifact"`。
- Gate: 缺口来自真实文件。

## TP-02.01
- [x] release artifact 生成脚本已新增。
- Verify: `rg -n "release-artifacts" scripts`。
- Gate: shell/Python 入口存在。

## TP-02.02
- [x] SBOM/provenance/manifest 可生成和校验。
- Verify: `bash scripts/release-artifacts.sh --output-dir /tmp/fatecat-release-artifacts-0040`。
- Gate: 3 个 JSON artifact 存在且 verify 通过。

## TP-03.01
- [x] public-release/local-ci 已接入。
- Verify: `rg -n "release-artifacts" scripts/public-release-gate.sh scripts/local-ci.sh`。
- Gate: release gate 消费生成路径。

## TP-03.02
- [x] live release gate 消费 artifact。
- Verify: `bash scripts/live-release-gate.sh --sbom-path ... --provenance-path ...`。
- Gate: SBOM/provenance checks 为 pass。

## TP-04.01
- [x] 回归测试已新增。
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_release_artifacts.py`。
- Gate: 生成、verify、gate 消费都覆盖。

## TP-04.02
- [x] 合同、AGENTS、API 文档和 roadmap 已同步。
- Verify: `rg -n "release-artifacts|SBOM/provenance" contracts/fate/delivery scripts/AGENTS.md docs/reference-materials`。
- Gate: 文档明确不是远端 attestation。

## TP-05.01
- [x] 验证和 closeout 已执行或待本文件校验后生成。
- Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py`。
- Gate: 任务文档无占位符，closeout ready。
