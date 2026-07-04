# Acceptance Checklist

# Global Standards

- [x] 任务包不包含模板占位符。
- [x] 所有新增样本使用 synthetic anonymous fixture，不包含真实用户资料。
- [x] 生产 provider 不读取本任务新增 golden fixture 或 professional rubric。
- [x] 不输出或保存完整报告正文作为 diff artifact。
- [x] 不声明八字/紫微专业能力 100%、预测准确率 100% 或确定未来。
- [x] 本地验证命令有真实执行证据。

# Task Package Checklists

## TP-01 evaluation contract and rubric

Verify: JSON parse, core-quality gate and rubric regression test.

Gate: rubric dimensionCount >= 8, required evidence kinds present, registry/manifest/policy links intact.

- [x] `contracts/fate/evaluations/professional-quality-rubric.json` 存在并可 JSON parse。
- [x] `core-quality-corpus.json` 登记 `professionalQualityRubric`。
- [x] `report-diff-policy.json` 登记 `minProfessionalRubricDimensions >= 8`。
- [x] `registry.json` metadata 和 dataset paths 登记 rubric。
- [x] rubric 包含 bazi/ziwei、golden fixture、report diff、evidence、privacy、human review 要求。
- [x] rubric 包含禁止宣称：预测准确率 100%、专业能力 100% 已证明、确定未来。

## TP-02 bazi/ziwei anonymous corpus expansion

Verify: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json`.

Gate: `totalCaseCount=340`, bazi statement >= 8, ziwei basic/depth >= 12, birthPlace/name privacy boundary intact.

- [x] 八字 statement cases 最小线为 8。
- [x] 紫微基础 cases 最小线为 12。
- [x] 紫微 rule depth cases 最小线为 12。
- [x] 紫微基础覆盖标签包含夏季/秋季、身宫福德、天机/贪狼/武曲/武曲天相等新增结构。
- [x] 新增样本输入使用北京、测试样本、经纬度和性别/出生时间结构化字段。

## TP-03 gate and regression hardening

Verify: targeted regression pytest and L4 golden smoke.

Gate: `53 passed`, L4 smoke passed, data supply chain gate passed, report diff remains summary-only.

- [x] `scripts/core-quality-corpus-gate.py` 接受 `--professional-rubric` 参数。
- [x] core-quality gate 校验 registry、policy、rubric、corpus 数量、coverage tags 和隐私边界。
- [x] `test_core_quality_corpus_gate.py` 覆盖新阈值和 rubric。
- [x] `test_bazi_ziwei_l4_golden_smoke.py` 覆盖紫微 12 例阈值。
- [x] 紫微 rule depth 新增样本 expected 与当前 executor 输出一致。
- [x] 数据供应链 registry selected sha 与更新后的紫微/evaluation fixture 一致。

## TP-04 documentation closeout

Verify: task docs validator, placeholder scan and docs review.

Gate: 0142 task docs and evaluations AGENTS reflect current scope/status.

- [x] `contracts/fate/evaluations/AGENTS.md` 说明 professional rubric 职责。
- [x] 0142 README/PLAN/TODO/STATUS/ACCEPTANCE/ACCEPTANCE_CHECKLIST/CONTEXT 已回填。
- [x] `governance/tasks/INDEX.md` 与任务状态一致。

## TP-05 validation and release handoff

Verify: final validation commands and git diff review.

Gate: all local validations pass before commit/push.

- [x] JSON parse 通过。
- [x] `git diff --check` 通过。
- [x] `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json` 通过。
- [x] `bash scripts/data-supply-chain-gate.sh` 通过。
- [x] `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4-0142.json` 通过。
- [x] 相关 regression pytest 通过：`53 passed`。
- [x] `bash scripts/local-ci.sh --profile quick` 通过：evidence `/tmp/fatecat-local-ci-20260704233925`，focused regression `389 passed`。
