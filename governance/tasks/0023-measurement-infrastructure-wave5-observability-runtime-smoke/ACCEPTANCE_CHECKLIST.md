# Acceptance Checklist

# Global Standards
- [x] smoke 输出不包含真实日志正文、请求体、用户输入、token、secret、DSN 或报告正文。
- [x] planned trace/SLO/alert 不被标记为 available。
- [x] 文档不宣称 OpenTelemetry、collector、dashboard、SLO 或生产监控平台已完成。

# Task Package Checklists

## TP-01.01 盘点观测缺口
- [x] Verify: `rg -n "observability|metrics|request-id|logs|SLO|ready" contracts docs scripts tests domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: available signals 与 planned signals 边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0023-measurement-infrastructure-wave5-observability-runtime-smoke --phase decompose`
- [x] Gate: 任务文档无占位符且任务树可解析。

## TP-02.01 新增 observability smoke 脚本
- [x] Verify: `bash scripts/observability-smoke.sh --output-json /tmp/fatecat-observability-smoke.json && python3 -m json.tool /tmp/fatecat-observability-smoke.json >/dev/null`
- [x] Gate: smoke 返回 passed 并覆盖 15 个 checks。

## TP-02.02 登记 smoke 到 registry/AGENTS
- [x] Verify: `python3 -m json.tool contracts/fate/observability/registry.json >/dev/null && rg -n "observability-smoke|smokeCommand|smokeScope" contracts/fate/observability scripts/AGENTS.md`
- [x] Gate: registry metadata 与 AGENTS 均可定位 smoke 入口。

## TP-03.01 新增 smoke 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_observability_smoke.py`
- [x] Gate: script 函数和 CLI 输出均被覆盖。

## TP-03.02 更新 contract/API tests 与 quick CI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k observability && rg -n "test_observability_smoke.py" scripts/local-ci.sh`
- [x] Gate: registry metadata、API payload 和 quick CI 测试入口一致。

## TP-03.03 更新文档与路线图
- [x] Verify: `rg -n "observability-smoke|health/ready/metrics/request-id|OpenTelemetry|生产监控平台" docs/reference-materials`
- [x] Gate: 文档区分本地 smoke 与未完成生产监控。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0023-measurement-infrastructure-wave5-observability-runtime-smoke --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0023 closeout 和全任务树校验通过。
