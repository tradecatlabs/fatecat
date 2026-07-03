# Execution Checklist

[x] TP-01.01 | P0 | 读取 retention/security baseline | Verify: `sed`/`rg` evidence | Gate: 不重复实现 cleanup runtime | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 staged contract | Verify: `python3 -m json.tool contracts/fate/security/retention-production-cleanup-staged.json` | Gate: 三类 evidence area 与负例存在 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 gate script/wrapper | Verify: `bash scripts/retention-production-cleanup-gate.sh --output-json /tmp/fatecat-retention-production-cleanup-0098.json` | Gate: shipGate blocked/pending | Parallelizable: No
[x] TP-03.01 | P0 | 接入 registry/policy/local-ci/AGENTS/docs | Verify: regression wiring assertions | Gate: local-ci 包含 gate 和 test | Parallelizable: No
[x] TP-03.02 | P0 | 新增 regression | Verify: focused pytest | Gate: 反伪造负例被拒绝 | Parallelizable: No
[x] TP-04.01 | P0 | 运行最终验证并 closeout | Verify: secret scan, quick local-ci, task validator | Gate: no placeholders, quick pass | Parallelizable: No
