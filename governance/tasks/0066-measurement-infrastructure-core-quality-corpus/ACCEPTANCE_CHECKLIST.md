# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 evaluation contracts、golden fixture、gate、tests、docs 和任务文档。
- [x] 不连接真实用户数据、真实非北京地区样例、公网 API、Bot 或外部专家评测系统。
- [x] 不保存真实 token、secret、DSN、私钥、证书、报告正文或生产路径。
- [x] focused tests、ruff、语料 gate 和 quick local-ci 已通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 复核现有 golden fixture、evaluation registry、local-ci 和 L4 smoke。
Verify: `rg` / `sed` / JSON summary。
Gate: 当前差距明确。

## TP-02.01

- [x] 新增核心质量语料 manifest。
Verify: JSON syntax + gate。
Gate: 5 个 corpus 分片可发现。

## TP-02.02

- [x] 新增完整报告 diff 策略。
Verify: JSON syntax + policy assertions。
Gate: 结构、隐私和体系隔离明确。

## TP-03.01

- [x] 扩容紫微匿名基础样本到 4 个。
Verify: L4 golden smoke。
Gate: 仅北京/测试样本。

## TP-03.02

- [x] 新增 `core-quality-corpus-gate`。
Verify: gate CLI。
Gate: output JSON status=passed。

## TP-03.03

- [x] 接入 evaluation registry、runner、local-ci 和 summary artifact。
Verify: focused API/runner tests。
Gate: required run 可发现。

## TP-04.01

- [x] 新增回归测试并同步 AGENTS/README/roadmap。
Verify: focused tests + diff review。
Gate: 文档不夸大。

## TP-04.02

- [x] 运行 quick local-ci 并记录本地交付证据。
Verify: local-ci summary。
Gate: 本地 quick CI 通过。

## Evidence Checklist

- [x] `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-gate.json`
- [x] `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py tests/regression/test_evaluation_runner.py`
- [x] `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py::test_evaluation_resources_are_discoverable_and_linked tests/regression/test_capability_protocol.py::test_evaluation_registry_resources_are_traceable_and_do_not_pollute_production_inputs`
- [x] `ruff check` / `ruff format --check` focused files
- [x] `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0066`
- [x] task validators
