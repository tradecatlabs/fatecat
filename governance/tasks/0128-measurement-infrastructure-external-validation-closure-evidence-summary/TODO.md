# Execution Checklist

[x] TP-01 | P0 | Scope and upstream evidence chain confirmation | Verify: summary source chain matches work queue/proof-ref/runbook/operator/live/trend artifacts | Gate: no real credential dependency | Parallelizable: No
[x] TP-02 | P0 | Closure evidence summary contract, script and wrapper | Verify: contract/script/wrapper files exist | Gate: blocked summary and rejection paths covered | Parallelizable: No
[x] TP-03 | P0 | local-ci and certification wiring | Verify: certification requires new artifacts and local-ci summary exposes them | Gate: no certification passed claim | Parallelizable: No
[x] TP-04 | P0 | AGENTS/roadmap/task index sync | Verify: tests assert local-ci, AGENTS, certification and roadmap wiring | Gate: no live passed claim | Parallelizable: No
[x] TP-05 | P0 | Validation gates | Verify: targeted pytest, ruff, task docs validation, secret scan and quick CI pass | Gate: no URL/secret output and no over-claim | Parallelizable: No
[x] TP-06 | P0 | Delivery and remote CI observation | Verify: commit pushed and Actions observed | Gate: current remote CI result recorded | Parallelizable: No

说明：
- 每一行绑定 `TP-XX`。
- `TP-05/TP-06` 完成后才能 closeout。
