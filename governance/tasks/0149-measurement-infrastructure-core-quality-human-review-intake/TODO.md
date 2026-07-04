# Execution Checklist
[x] TP-01.01 | P0 | Inspect existing core quality gates and identify missing intake | Verify: source files read | Gate: missing human review/external benchmark intake documented | Parallelizable: No
[x] TP-02.01 | P0 | Add human review contract, Python gate and shell wrapper | Verify: JSON syntax and CLI default pending | Gate: no evidence outputs blocked-as-expected | Parallelizable: Yes
[x] TP-02.02 | P0 | Add privacy and anti-forgery validation | Verify: negative regression tests | Gate: raw URL, secret, commit mismatch and missing dimensions rejected | Parallelizable: Yes
[x] TP-03.01 | P0 | Wire evaluation registry, local-ci and AGENTS | Verify: wiring regression test | Gate: local-ci artifact path and registry run exist | Parallelizable: Yes
[x] TP-03.02 | P0 | Wire certification core_quality domain | Verify: certification regression test | Gate: core_quality cannot pass without human review gate accepted | Parallelizable: Yes
[ ] TP-04.01 | P0 | Collect real expert rubric disposition bundle | Verify: future accepted gate summary | Gate: all rubric dimensions accepted with redacted refs | Parallelizable: No
[ ] TP-04.02 | P0 | Collect external benchmark aggregate and no-leak signoff | Verify: future accepted gate summary | Gate: benchmark/no-leak gates passed without detail leakage | Parallelizable: No
[x] TP-05.01 | P0 | Run validation commands | Verify: json/tool/pytest/local-ci/task-doc outputs | Gate: all local checks passed | Parallelizable: No
[ ] TP-05.02 | P0 | Commit, push and remote Acceptance | Verify: git status and GitHub Actions URL | Gate: current commit remote Acceptance success | Parallelizable: No

说明：
- TP-04.01 和 TP-04.02 是真实外部/人工证据，不得用 synthetic fixture 替代。
