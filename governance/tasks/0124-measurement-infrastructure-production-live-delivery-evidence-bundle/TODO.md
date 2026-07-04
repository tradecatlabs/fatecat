# Execution Checklist

[x] TP-01 | P0 | Scope and upstream category confirmation | Verify: supported categories match roadmap/runbooks | Gate: no real credential dependency | Parallelizable: No
[x] TP-02 | P0 | Contract, script and wrapper | Verify: contract/script/wrapper files exist | Gate: pending and live fixture paths covered | Parallelizable: No
[x] TP-03 | P0 | local-ci/live-proof/docs wiring | Verify: tests assert local-ci and AGENTS wiring | Gate: live proof gate consumes generated bundle | Parallelizable: No
[x] TP-04 | P0 | Validation gates | Verify: targeted pytest, ruff, local artifact chain and quick CI pass | Gate: no URL/secret output and no over-claim | Parallelizable: No
[ ] TP-05 | P0 | Delivery and remote CI observation | Verify: commit pushed and Actions observed | Gate: current remote CI result recorded | Parallelizable: No

说明：
- 每一行绑定 `TP-XX`。
- `TP-04/TP-05` 完成后才能 closeout。
