# Acceptance Checklist

# Global Standards
- [x] 只保存匿名 synthetic fixture。
- [x] 只使用北京/测试样本。
- [x] 不保存完整报告正文。
- [x] 不修改 production provider 算法。
- [x] 不宣称预测准确率或专业能力 100%。

# Task Package Checklists

## TP-01.01 读取现有 corpus/report diff/gate/test

Verify: `sed`/`python3` inspection of existing manifest, policy, gate and tests.

Gate: Existing weak point is concrete: ziwei basic min count was 4 and report diff lacked structuralDiff summary-only policy.

- [x] Existing state reviewed.

## TP-02.01 扩容紫微 basic fixture

Verify: `domains/fate-analysis/data-products/ziwei/golden/cases.json` has `caseCount=8` and `coverageRequirements`.

Gate: All cases use `birthPlace=北京` and `name=测试样本`.

- [x] Ziwei fixture expanded.

## TP-02.02 更新 core-quality manifest 与 report diff policy

Verify: JSON parse and diff.

Gate: `minZiweiGoldenCases=8`; `structuralDiff.summaryOnly=true`; forbidden stored fields include `fullReport` and `reportText`.

- [x] Contracts updated.

## TP-03.01 更新 core-quality gate

Verify: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-0096.json`.

Gate: Summary status passed and totalCaseCount is 329.

- [x] Gate updated and passed.

## TP-03.02 更新 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py`.

Gate: 5 passed.

- [x] Tests updated and passed.

## TP-04.01 更新 registry/AGENTS/roadmap/task docs

Verify: `rg -n "summary-only|coverage tags|0096|caseCount=8" ...`.

Gate: Docs describe the new scope without production or accuracy overclaim.

- [x] Docs updated.

## TP-05.01 最终验证

Verify: `validate_task_docs.py --phase closeout` and `git diff --check`.

Gate: exit 0.

- [x] Final validation passed.
