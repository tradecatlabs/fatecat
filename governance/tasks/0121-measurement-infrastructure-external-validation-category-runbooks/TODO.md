# Execution Checklist

[x] TP-01 | P0 | 复核 MI-100.A.03 与当前 22 个 category 边界 | Verify: `rg -n "MI-100.A.03 external validation runbook per category" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 不扩大到 stale alert 或 live validation | Parallelizable: No
[x] TP-02 | P0 | 新增 category runbooks contract/script/wrapper/certification wiring | Verify: `rg -n "external-validation-category-runbooks" contracts scripts` | Gate: runbook ready 仍 shipGate blocked | Parallelizable: No
[x] TP-03 | P0 | 新增回归测试与 local-ci artifact | Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py` | Gate: 22 category、未知 category、privacy、wiring 覆盖 | Parallelizable: No
[x] TP-04 | P0 | 运行 quick CI 与 secret scan | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-category-runbooks-0121` | Gate: 本地总门禁通过 | Parallelizable: No
[x] TP-05 | P0 | 准备提交推送交付包 | Verify: `git status --short --branch` | Gate: 远端 CI 结果不预写入仓库，推送后单独观察 | Parallelizable: No
