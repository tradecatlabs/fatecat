# Execution Checklist
[x] TP-01.01 | P0 | Confirm clean current HEAD and workflow dispatch availability | Verify: git/workflow reads | Gate: clean before dispatch | Parallelizable: Yes
[x] TP-01.02 | P0 | Confirm current HEAD has no existing remote run evidence | Verify: `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha"` | Gate: empty means missing, not pass | Parallelizable: Yes
[x] TP-02.01 | P0 | Dispatch FateCat Acceptance for current HEAD | Verify: `gh workflow run acceptance.yml --ref main` | Gate: run appears for final headSha | Parallelizable: Yes
[x] TP-02.02 | P0 | Dispatch FateCat Container for current HEAD with push_image=false | Verify: `gh workflow run container.yml --ref main -f push_image=false` | Gate: run appears for final headSha | Parallelizable: Yes
[x] TP-03.01 | P0 | Poll GitHub Actions until terminal state or timeout | Verify: `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha"` | Gate: terminal state reached or timeout recorded | Parallelizable: No
[x] TP-03.02 | P0 | Verify headSha matches current HEAD and conclusions are success | Verify: `gh run view <run-id>` | Gate: success only for matching final headSha | Parallelizable: No
[x] TP-04.01 | P0 | Validate task docs and no placeholder drift | Verify: validator + rg placeholders | Gate: docs pass | Parallelizable: No
[x] TP-04.02 | P0 | Commit task package before dispatch, then keep final evidence in GitHub Actions external state | Verify: git clean after push | Gate: no post-evidence commit | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
