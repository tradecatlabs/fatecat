# Execution Checklist

[x] TP-01 | P0 | 复核 MI-100.A.02 与 0119 work queue 边界 | Verify: `rg -n "MI-100.A.02 proof-ref" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 不扩大到 category live runbook | Parallelizable: No
[x] TP-02 | P0 | 新增 proof-ref contract/schema/script/wrapper/certification wiring | Verify: `rg -n "external-validation-proof-ref" contracts scripts` | Gate: schema accepted 仍 shipGate blocked | Parallelizable: No
[x] TP-03 | P0 | 新增回归测试与 local-ci artifact | Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py` | Gate: pending、accepted bundle、raw URL、wiring 覆盖 | Parallelizable: No
[x] TP-04 | P0 | 运行 quick CI 与 secret scan | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-proof-ref-0120` | Gate: 本地总门禁通过 | Parallelizable: No
[x] TP-05 | P0 | 准备提交推送交付包 | Verify: `git status --short --branch` | Gate: 远端 CI 结果不预写入仓库，推送后单独观察 | Parallelizable: No
