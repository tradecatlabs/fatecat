# Execution Checklist

[x] TP-01 | P0 | 复核 closure plan 与 MI-100.A.01 边界 | Verify: `rg -n "MI-100.A.01 closure owner work queue" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 不扩大到 proof verifier/live | Parallelizable: No
[x] TP-02 | P0 | 新增 work queue contract/script/wrapper/local-ci wiring | Verify: `rg -n "external-validation-closure-work-queue" contracts scripts` | Gate: `proofRef` 初始为空且 shipGate blocked | Parallelizable: No
[x] TP-03 | P0 | 新增回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py tests/regression/test_external_validation_closure_work_queue.py` | Gate: contract/grouping/privacy/invalid/wiring 覆盖 | Parallelizable: No
[x] TP-04 | P0 | 运行 quick CI 与 secret scan | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-work-queue-0119-final` | Gate: 本地总门禁通过 | Parallelizable: No
[x] TP-05 | P0 | 准备提交推送交付包 | Verify: `git status --short --branch` | Gate: 远端 CI 结果不预写入仓库，推送后单独观察 | Parallelizable: No
