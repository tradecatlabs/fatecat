# Execution Checklist

[x] TP-01.01 | P0 | 复核 core corpus、MingLi-Bench、vendor 和 evaluation registry | Verify: inspected files and upstream ls-remote | Gate: target is aggregate no-leak gate | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 MingLi-Bench aggregate gate contract | Verify: contract file | Gate: forbidden fragments declared | Parallelizable: No
[x] TP-03.01 | P0 | 实现 `mingli-bench-gate.py/.sh` | Verify: syntax + CLI smoke | Gate: no external API call | Parallelizable: No
[x] TP-04.01 | P0 | 接入 registry、docs、AGENTS 和 quick CI | Verify: grep + tests | Gate: MingLi remains optional/evaluation_only | Parallelizable: No
[x] TP-04.02 | P0 | 刷新 data supply chain registry hash | Verify: data supply chain gate | Gate: hash matches evaluation registry | Parallelizable: No
[x] TP-05.01 | P0 | 增加 focused regression tests | Verify: pytest | Gate: aggregate gate and legacy runner covered | Parallelizable: No
[x] TP-05.02 | P0 | 运行完整本地验证并明确 git/CI 交付证据外置边界 | Verify: quick CI + task validators | Gate: all local checks pass and no remote CI pre-claim | Parallelizable: No
