# Task-Level Acceptance

0142 完成条件：

- 八字/紫微核心质量 corpus 最小样本线提升，并由门禁强制校验。
- `professional-quality-rubric.json` 成为 evaluation registry 可发现的一等契约。
- report diff policy 与 core-quality gate 同步校验 rubric、匿名样本、覆盖标签、隐私边界和禁止保存完整报告正文。
- regression tests 覆盖新增 rubric、样本阈值、隐私边界和 L4 smoke 阈值。
- 文档明确该质量证据只用于 evaluation/release gate，不进入 production provider，不宣称 100% 专业能力。

# Validation Plan

| Check | Command | Result |
| --- | --- | --- |
| JSON parse | `python3 -m json.tool ...` on modified JSON contracts/fixtures | passed |
| Core quality gate | `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json` | passed, `totalCaseCount=340` |
| Data supply chain gate | `bash scripts/data-supply-chain-gate.sh` | passed, `assets=8`, `checks=162` |
| L4 golden smoke | `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4-0142.json` | passed, `checks=71` |
| Regression pytest | `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | passed, `53 passed` |
| Whitespace diff | `git diff --check` | passed |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0142-measurement-infrastructure-bazi-ziwei-professional-quality-corpus-expansion --phase decompose` | passed |
| Quick local CI | `bash scripts/local-ci.sh --profile quick` | passed, evidence `/tmp/fatecat-local-ci-20260704233925`, focused regression `389 passed` |

# Review Gate

- Future-optimal: core quality is represented as explicit corpus/rubric/gate contracts, not ad hoc Markdown claims.
- Ponytail: no new runtime framework, dependency or provider introduced; reused existing golden fixture and gate structure.
- Glue: production calculation remains on existing mature provider chain; this task only adds evaluation glue and test assertions.
- Privacy: all new samples are synthetic anonymous Beijing/测试样本; no real user data or secret material.
- No-overclaim: rubric explicitly forbids `预测准确率 100%`、`专业能力 100% 已证明`、`确定未来`。

# Runtime Verification Gate

Not applicable for production runtime. This task intentionally does not change production provider behavior.

Evaluation runtime is verified through:

- `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json`
- `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4-0142.json`

# Ship Readiness

This local quality slice is ship-ready after task docs validation and commit.

It does not establish public production readiness, external live readiness, real expert certification or third-party audit completion.

# Task Package Acceptance

| TP | Acceptance |
| --- | --- |
| TP-01 | Rubric file exists, registry metadata links it, manifest requires it, policy threshold includes it. |
| TP-02 | Core-quality gate reports 5 corpora and at least 340 total cases. |
| TP-03 | Regression pytest, data supply chain gate and L4 smoke pass with new thresholds and hashes. |
| TP-04 | Evaluations AGENTS and 0142 task docs contain no template placeholders. |
| TP-05 | Final validation evidence recorded before commit. |

## TP-01 evaluation contract and rubric

Verify: JSON parse and `test_professional_quality_rubric_enforces_review_boundary_and_forbidden_claims`.

Gate: dimensionCount >= 8, required capabilities include bazi/ziwei, forbidden claims present, human review boundary present.

## TP-02 bazi/ziwei anonymous corpus expansion

Verify: `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-0142.json`.

Gate: `totalCaseCount=340`, bazi statement cases >= 8, ziwei basic/depth >= 12, all samples use 北京/测试样本.

## TP-03 gate and regression hardening

Verify: targeted pytest regression suite and L4 golden smoke.

Gate: all selected tests pass, selected supply-chain sha values match, and report-diff policy remains summary-only.

## TP-04 documentation closeout

Verify: placeholder scan and task docs validator.

Gate: docs describe evaluation-only/no-production/no-100%-claim boundaries.

## TP-05 validation and release handoff

Verify: git diff review and final commit/push.

Gate: no untracked runtime artifacts, no failed local validation.

# Anti-Goals

- 不改 production provider 算法。
- 不保存真实用户资料、真实非北京地区示例、完整报告正文、secret、DSN 或生产路径。
- 不把本地 gate 写成真实专家评审、真实命例准确率或专业能力 100%。
- 不伪造外部生产 live、CI、Bot、HF、OIDC、SIEM、OTel、Vault/KMS 或第三方审计结果。
