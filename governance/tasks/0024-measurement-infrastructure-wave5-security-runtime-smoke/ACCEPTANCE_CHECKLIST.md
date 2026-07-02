# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] 新增执行入口只做本地 smoke，不伪造外部生产验证。
- [x] 输出 JSON 不包含真实 token、secret、DSN、用户输入、请求体或报告正文。
- [x] focused tests、ruff、format、quick CI、diff check 全部通过。
- [x] task validators、全任务树验证和 closeout packet 通过。

# Task Package Checklists

## TP-01.01 盘点安全缺口
- [x] Verify: `rg -n "security|token|rate|privacy|public release|records" contracts docs scripts tests domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: available controls 与 planned controls 边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0024-measurement-infrastructure-wave5-security-runtime-smoke --phase decompose`
- [x] Gate: 任务文档无占位符且任务树可解析。

## TP-02.01 新增 security smoke 脚本
- [x] Verify: `bash scripts/security-smoke.sh --output-json /tmp/fatecat-security-smoke.json && python3 -m json.tool /tmp/fatecat-security-smoke.json >/dev/null`
- [x] Gate: smoke 返回 passed 并覆盖 19 个 checks。

## TP-02.02 登记 smoke 到 registry/AGENTS
- [x] Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "security-smoke|smokeCommand|smokeScope" contracts/fate/security scripts/AGENTS.md`
- [x] Gate: registry metadata 与 AGENTS 均可定位 smoke 入口。

## TP-03.01 新增 smoke 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_security_smoke.py`
- [x] Gate: script 函数和 CLI 输出均被覆盖。

## TP-03.02 更新 contract/API tests 与 quick CI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k security && rg -n "test_security_smoke.py" scripts/local-ci.sh`
- [x] Gate: registry metadata、API payload 和 quick CI 测试入口一致。

## TP-03.03 更新文档与路线图
- [x] Verify: `rg -n "security-smoke|token/owner|OAuth|RBAC|Bot live" docs/reference-materials`
- [x] Gate: 文档区分本地 smoke 与未完成生产安全能力。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0024-measurement-infrastructure-wave5-security-runtime-smoke --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0024 closeout 和全任务树校验通过。
