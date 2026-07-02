# Execution Checklist
[x] TP-01.01 | P0 | 盘点记录接口、报告 job、security registry 和 roadmap 缺口 | Verify: `rg -n "record|records|audit|retention|ttl|report/jobs" domains/experience-delivery/services/fatecat-delivery/src contracts/fate/security docs/reference-materials/roadmap` | Gate: audit event、job TTL、record explicit delete 和外部生产缺口边界明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约与任务树 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增脱敏 audit_event helper | Verify: `rg -n "_log_audit_event|_audit_hash|auditRetentionDays" domains/experience-delivery/services/fatecat-delivery/src/main.py` | Gate: helper 只输出短哈希和安全 metadata | Parallelizable: No
[x] TP-02.02 | P0 | 接入记录接口和报告 job 生命周期 | Verify: `rg -n "record\\.read|record\\.create|record\\.list|record\\.delete|report_job\\.submit|report_job\\.cancel" domains/experience-delivery/services/fatecat-delivery/src/main.py` | Gate: 关键动作都有 audit_event 调用点 | Parallelizable: No
[x] TP-03.01 | P0 | 登记 audit_log / retention SecurityControl | Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "control.audit_event_log|control.retention_policy|audit_log|retention" contracts/fate/security` | Gate: schema、registry 和 API 均可发现 audit/retention 控制 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 audit/retention 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'audit_event or retention or security'` | Gate: runtime audit_event 脱敏和 registry/API 断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 更新 AGENTS、API 文档和 100% 路线图 | Verify: `rg -n "audit_event|retention policy|SIEM|不可变审计|自动清理" contracts/fate/security/AGENTS.md docs/reference-materials` | Gate: 文档区分本地 baseline 与未完成生产审计能力 | Parallelizable: No
[x] TP-04.01 | P0 | 执行 focused tests、secret scan、ruff/format、quick CI 和 diff check | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过 | Parallelizable: No
[x] TP-04.02 | P0 | 回填 closeout 状态、全任务树验证和 closeout packet | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0026 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
