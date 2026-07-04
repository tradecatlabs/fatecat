# Acceptance Checklist

# Global Standards
- [x] 默认无外部证据时 blocked。
- [x] 不保存专家身份。
- [x] 不保存真实命例或真实出生地区。
- [x] 不保存题目、选项、答案、逐题预测或完整报告正文。
- [x] accepted bundle 必须绑定 commit。
- [x] accepted bundle 必须覆盖全部 professional rubric dimensions。
- [x] certification 不能在缺 human review / benchmark / no-leak evidence 时通过。

# Task Package Checklists
## Quality gap identification

### TP-01.01 Existing quality gate gap
- [x] core quality corpus gate inspected.
- [x] professional quality rubric inspected.
- [x] MingLi-Bench aggregate gate inspected.
- [x] certification core_quality domain inspected.
Verify: source files are listed in CONTEXT.
Gate: missing external review intake was identified.

## Intake implementation

### TP-02.01 Contract and gate
- [x] `core-quality-human-review-gate.json` added.
- [x] `core-quality-human-review-gate.py` added.
- [x] `core-quality-human-review-gate.sh` added.
Verify: JSON/tool syntax and CLI smoke.
Gate: default pending output is valid and exits 0.

### TP-02.02 Privacy and anti-forgery
- [x] raw URL rejected.
- [x] secret-like assignment rejected.
- [x] commit mismatch rejected.
- [x] missing rubric dimension rejected.
- [x] accepted synthetic bundle stores only refs/hash/aggregate stats.
Verify: `test_core_quality_human_review_gate.py`.
Gate: negative tests pass.

## Wiring

### TP-03.01 Registry local-ci AGENTS
- [x] evaluation registry has `run.core_quality_human_review_gate`.
- [x] local-ci runs gate and records artifact path.
- [x] scripts/tests/evaluations AGENTS mention the gate.
Verify: wiring regression test.
Gate: focused tests pass.

### TP-03.02 Certification core quality
- [x] certification contract lists `core-quality-human-review-gate.json`.
- [x] certification aggregator consumes it in `core_quality`.
- [x] synthetic full pass fixture includes accepted state.
Verify: `test_measurement_infrastructure_certification.py`.
Gate: certification tests pass.

## External closure

### TP-04.01 Expert rubric disposition
- [ ] Real redacted expert bundle supplied.
- [ ] All rubric dimensions accepted.
- [ ] Reviewer identity remains redacted.
Verify: future `bash scripts/core-quality-human-review-gate.sh --review-evidence-json <bundle>`.
Gate: `humanReviewGate.status=passed`.

### TP-04.02 External benchmark and no-leak
- [ ] External benchmark aggregate supplied.
- [ ] No per-question leak confirmed.
- [ ] noLeakReview passed with forbiddenFragmentsFound=0.
Verify: future accepted bundle and gate summary.
Gate: `externalBenchmarkGate.status=passed` and `noLeakGate.status=passed`.

## Validation and delivery

### TP-05.01 Local validation
- [x] JSON validation passed.
- [x] Focused tests passed.
- [x] quick local CI passed.
- [x] task docs validation passed.
Verify: terminal evidence.
Gate: no failed local check remains.

### TP-05.02 GitHub delivery
- [ ] Commit created and pushed.
- [ ] Remote Acceptance triggered for current commit.
- [ ] Remote Acceptance completed successfully.
Verify: Git status and GitHub Actions run URL.
Gate: current commit remote Acceptance success.
