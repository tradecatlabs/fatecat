# 0096 Implementation Notes

## Scope

0096 执行 0095 `Wave A Next-01`：扩容八字/紫微核心质量 corpus 与 report diff gate。实现保持在 evaluation/contract/test 层，不修改 production provider 算法，不新增真实用户样本，不保存完整报告正文。

## Changes

| Area | Change |
| --- | --- |
| 紫微 basic corpus | `domains/fate-analysis/data-products/ziwei/golden/cases.json` 从 4 个匿名北京样本扩为 8 个，并新增 `coverageTags` 与 `coverageRequirements`。 |
| Core quality manifest | `corpus.ziwei.basic_cases.minCaseCount` 从 4 提升到 8，并登记必需 coverage tags 与 report diff summary-only 字段。 |
| Report diff policy | 增加 `structuralDiff.summaryOnly`、必需结构摘要字段、禁止保存完整报告正文字段和 profile minimums。 |
| Gate | `scripts/core-quality-corpus-gate.py` 校验 coverage tags、紫微最小样本数 8、summary-only 策略和 forbidden stored fields。 |
| Tests | `test_core_quality_corpus_gate.py` 校验 329+ 总样本、紫微 8+、coverageTagCount 和 report diff forbidden fields。 |
| Supply chain | `contracts/fate/data-supply-chain/registry.json` 同步更新紫微 golden fixture 与 evaluation registry sha，保持资产指纹可复核。 |
| Docs | 同步 registry metadata、AGENTS、主路线图和任务包。 |

## Evidence

- `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-0096.json`：passed，`totalCaseCount=329`。
- `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py`：5 passed。
- `bash scripts/check-privacy-fixtures.sh`：passed。
- `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0096-final.json`：passed，`findingCount=0`。
- `bash scripts/data-supply-chain-gate.sh`：passed，`assets=8`，`classics=14`，`checks=162`。
- `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0096-rerun`：passed，focused regression `267 passed`。

## Boundaries

- 不保存完整 Markdown/report body。
- 不加入真实用户、真实非北京地区、token、secret、DSN 或生产路径。
- 不把 synthetic corpus 写成真实命例库或专家准确率证明。
- 不改变 `CapabilityExecutor`、provider 算法或报告生成逻辑。
