# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] scanner 输出不包含疑似密钥原文。
- [x] allowlist 只包含占位符、示例片段和排除边界。
- [x] focused tests、ruff、format、quick CI、diff check 全部通过。
- [x] task validators、全任务树验证和 closeout packet 通过。

# Task Package Checklists

## TP-01.01 盘点 secret scan 缺口
- [x] Verify: `rg -n "secret scanner|secret scan|source hygiene|public release|token|DSN|webhook" docs contracts scripts tests governance/tasks/0019-measurement-infrastructure-wave5-security-privacy-resources`
- [x] Gate: scanner 与 source hygiene/release gate 边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0025-measurement-infrastructure-wave5-secret-scan-gate --phase decompose`
- [x] Gate: 任务文档无占位符且任务树可解析。

## TP-02.01 新增 secret-scan 脚本
- [x] Verify: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan.json && python3 -m json.tool /tmp/fatecat-secret-scan.json >/dev/null`
- [x] Gate: 当前 worktree findingCount=0，输出不含疑似密钥原文。

## TP-02.02 新增 allowlist 与误报治理
- [x] Verify: `python3 -m json.tool contracts/fate/security/secret-scan-allowlist.json >/dev/null`
- [x] Gate: allowlist 不包含真实 secret，只记录占位符、示例片段和排除边界。

## TP-03.01 登记 SecurityControl
- [x] Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "control.secret_scan_gate|secret_scan|secretScanCommand" contracts/fate/security`
- [x] Gate: registry/schema/API 均可发现 secret scan gate。

## TP-03.02 新增 scanner 回归测试并接入 quick CI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'secret or security' && rg -n "test_secret_scan.py|secret scan" scripts/local-ci.sh`
- [x] Gate: scanner 命中、占位符忽略、CLI summary、API/contract tests 全覆盖。

## TP-03.03 更新 AGENTS、API 文档和路线图
- [x] Verify: `rg -n "secret-scan|secret scan|secret scanner|secretScanCommand" scripts/AGENTS.md contracts/fate/security/AGENTS.md docs/reference-materials`
- [x] Gate: 文档区分本地 scanner 与未完成生产安全能力。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0025-measurement-infrastructure-wave5-secret-scan-gate --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0025 closeout 和全任务树校验通过。
