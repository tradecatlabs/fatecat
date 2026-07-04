# Execution Checklist
[x] TP-01 | P0 | Current rehearsal gap: inspect third-party audit rehearsal hard-coded independent result item. | Verify: gap documented | Gate: current script/test inspection | Parallelizable: No
[x] TP-02 | P0 | Independent audit result intake gate: add contract, script and wrapper. | Verify: focused regression | Gate: independent-audit-result-gate tests | Parallelizable: No
[x] TP-03 | P0 | Rehearsal/local-ci wiring: pass independent gate into rehearsal and local-ci summary. | Verify: focused regression and quick local-ci | Gate: third-party rehearsal tests | Parallelizable: No
[x] TP-04 | P0 | Regression and docs: update tests, AGENTS and roadmap. | Verify: wiring tests | Gate: local-ci quick | Parallelizable: Yes
[x] TP-05 | P0 | Task evidence closeout: copy key local-ci artifacts into task package. | Verify: task docs validation | Gate: auto-tasks closeout validation | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO

# TODO

## Done
- [x] Inspect third-party audit rehearsal independent result gap.
- [x] Implement independent audit result contract and gate.
- [x] Wire gate into third-party audit rehearsal.
- [x] Wire gate into local-ci summary artifacts.
- [x] Add regression tests.
- [x] Update AGENTS and roadmap.
- [x] Run focused regression and quick local-ci.
- [x] Copy key evidence artifacts into task package.

## Future
- [ ] Execute real independent third-party audit with authorized auditor.
- [ ] Submit a redacted `fatecat.independent_audit_result_bundle`.
- [ ] Rerun `independent-audit-result-gate.sh` with the real bundle.
- [ ] Rerun release proof, current audit bundle, certification and third-party rehearsal after external proof/live gates are accepted.
