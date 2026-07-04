# Execution Checklist
[x] TP-01 | P0 | Current HEAD package: run local quick CI and identify current import package. | Verify: package SHA recorded | Gate: current HEAD binding | Parallelizable: No
[x] TP-02 | P0 | Tracker preflight: confirm GitHub Issues enabled, authorized session, and no duplicate tracker issues. | Verify: preflight completed before creation | Gate: duplicate avoidance | Parallelizable: No
[x] TP-03 | P0 | Issue creation: create 22 tracker issues with required labels. | Verify: `TRACKER_ISSUE_REFS.md` has 22 refs | Gate: real tracker side effect | Parallelizable: No
[x] TP-04 | P0 | Evidence bundle: generate redacted tracker issue evidence bundle and per-issue artifacts. | Verify: bundle has 22 issues | Gate: privacy boundary | Parallelizable: No
[x] TP-05 | P0 | Evidence gate: run `scripts/external-validation-tracker-issue-evidence-gate.sh` and record accepted output. | Verify: gate accepted 22 issues | Gate: issue evidence gate | Parallelizable: No
[x] TP-06 | P0 | Closeout: store redacted evidence and update task package documentation. | Verify: no placeholders remain | Gate: task docs validation | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
