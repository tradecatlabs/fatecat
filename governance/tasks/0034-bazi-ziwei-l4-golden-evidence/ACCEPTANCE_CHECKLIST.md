# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不混入新体系或生产 live smoke。
- [x] 隐私边界明确，只使用北京/测试样本。
- [x] 不伪造专业能力 100%、全文 diff 或远端 CI。
- [x] quick CI 通过。
- [x] closeout validator 已通过，closeout packet 已生成。

# Task Package Checklists

## TP-01.01 现状审计
Verify: `rg -n "MI-05|bazi-ziwei|snapshotGate|coverage_matrix_cases|rule_depth_cases" docs domains tests scripts`

Gate: L4 baseline 缺口明确。

- [x] 已盘点 MI-05、bazi/ziwei fixture 和 Markdown gate。

## TP-02.01 smoke 脚本
Verify: `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4.json`

Gate: status passed。

- [x] `scripts/bazi-ziwei-l4-golden-smoke.py/.sh` 已新增。

## TP-02.02 quick/full profile
Verify: `python3 -m json.tool /tmp/fatecat-bazi-ziwei-l4.json`

Gate: summary 有 profile、availableCaseCount、executedCaseCount 和 privacyBoundary。

- [x] quick summary 已输出 profile 与执行/可用样本计数。

## TP-02.03 local-ci hook
Verify: `rg -n "bazi ziwei L4 golden smoke|test_bazi_ziwei_l4_golden_smoke" scripts/local-ci.sh`

Gate: quick CI 包含脚本和测试。

- [x] `scripts/local-ci.sh` 已加入 L4 smoke 和 focused regression test。

## TP-03.01 pytest
Verify: `.venv/bin/python -m pytest -q tests/regression/test_bazi_ziwei_l4_golden_smoke.py`

Gate: focused pytest passes。

- [x] focused pytest 已通过，2 passed。

## TP-03.02 verification
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-bazi-ziwei-l4`

Gate: quick CI passes。

- [x] quick CI 已通过，108 passed。

## TP-04.01 docs sync
Verify: `rg -n "bazi-ziwei-l4-golden-smoke|MI-05|0034" docs/reference-materials scripts/AGENTS.md governance/tasks/INDEX.md`

Gate: 不夸大专业能力 100%。

- [x] API 文档、roadmap、专项基线、AGENTS 已同步。

## TP-04.02 closeout
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0034-bazi-ziwei-l4-golden-evidence --phase closeout`

Gate: closeout packet 写入任务目录。

- [x] closeout validator 已通过，`TASK_CLOSEOUT_PACKET.json` 已生成。
