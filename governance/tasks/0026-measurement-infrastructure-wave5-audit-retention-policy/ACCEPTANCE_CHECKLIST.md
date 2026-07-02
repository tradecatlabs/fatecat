# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] audit_event 不输出 token、请求体、报告正文、姓名、出生地区或 ID 原文。
- [x] registry/docs 不伪造外部 SIEM、不可变审计存储或自动记录清理。
- [x] focused tests、secret scan、ruff、format、quick CI、diff check 全部通过。
- [x] task validators、全任务树验证和 closeout packet 通过。

# Task Package Checklists

## TP-01.01 盘点 audit/retention 缺口
- [x] Verify: `rg -n "record|records|audit|retention|ttl|report/jobs" domains/experience-delivery/services/fatecat-delivery/src contracts/fate/security docs/reference-materials/roadmap`
- [x] Gate: audit event、job TTL、record explicit delete 和外部生产缺口边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0026-measurement-infrastructure-wave5-audit-retention-policy --phase decompose`
- [x] Gate: 任务文档无占位符且任务树可解析。

## TP-02.01 新增脱敏 audit_event helper
- [x] Verify: `rg -n "_log_audit_event|_audit_hash|auditRetentionDays" domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: helper 只输出短哈希和安全 metadata。

## TP-02.02 接入记录接口和报告 job 生命周期
- [x] Verify: `rg -n "record\\.read|record\\.create|record\\.list|record\\.delete|report_job\\.submit|report_job\\.cancel" domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: 关键动作都有 audit_event 调用点。

## TP-03.01 登记 audit_log / retention SecurityControl
- [x] Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "control.audit_event_log|control.retention_policy|audit_log|retention" contracts/fate/security`
- [x] Gate: schema、registry 和 API 均可发现 audit/retention 控制。

## TP-03.02 新增 audit/retention 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'audit_event or retention or security'`
- [x] Gate: runtime audit_event 脱敏和 registry/API 断言通过。

## TP-03.03 更新 AGENTS、API 文档和路线图
- [x] Verify: `rg -n "audit_event|retention policy|SIEM|不可变审计|自动清理" contracts/fate/security/AGENTS.md docs/reference-materials`
- [x] Gate: 文档区分本地 baseline 与未完成生产审计能力。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0026-measurement-infrastructure-wave5-audit-retention-policy --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0026 closeout 和全任务树校验通过。
