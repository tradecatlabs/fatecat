# Execution Checklist

[x] TP-01 | P0 | 扫描现有 capability/provider/release/evaluation 契约和 gate | Verify: file scans | Gate: reuse path identified | Parallelizable: Yes
[x] TP-02 | P0 | 新增 control-plane registry/schema/AGENTS | Verify: JSON parse + schema fields | Gate: 4 core resources present | Parallelizable: No
[x] TP-03 | P0 | 新增 control-plane gate 并接入 local-ci quick | Verify: `bash scripts/control-plane-gate.sh` | Gate: status passed | Parallelizable: No
[x] TP-04 | P0 | 新增回归测试与文档同步 | Verify: targeted pytest + docs validator | Gate: tests pass | Parallelizable: Yes
[x] TP-05 | P0 | 提交推送并汇报证据 | Verify: git status / remote CI if run | Gate: worktree clean | Parallelizable: No
