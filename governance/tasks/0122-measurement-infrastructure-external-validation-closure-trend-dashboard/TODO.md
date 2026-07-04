# Execution Checklist

[x] TP-01 | P0 | 复核 MI-100.A.04 与上游 artifact 边界 | Verify: `rg -n "MI-100.A.04 closure trend dashboard and stale owner alert" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 不扩大到真实通知或 live validation | Parallelizable: No
[x] TP-02 | P0 | 新增 closure trend dashboard contract/script/wrapper | Verify: `rg -n "external-validation-closure-trend-dashboard" contracts scripts` | Gate: dashboard ready 仍 shipGate blocked | Parallelizable: No
[x] TP-03 | P0 | 新增回归测试、local-ci、certification 与 AGENTS 接线 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py` | Gate: owner/category/status、privacy、wiring 覆盖 | Parallelizable: No
[x] TP-04 | P0 | 运行 targeted tests、secret scan、real gate chain、quick CI | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-trend-dashboard-0122` | Gate: 本地总门禁通过 | Parallelizable: No
[x] TP-05 | P0 | 准备提交推送交付包 | Verify: `git status --short --branch` | Gate: 远端 CI 结果不预写入仓库，推送后单独观察 | Parallelizable: No
