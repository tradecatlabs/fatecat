# Execution Checklist
[x] TP-01.01 | P0 | 盘点现有 token、owner、record 接口和 security registry | Verify: `rg -n "ApiPrincipal|_require_record_access|_require_owner_or_admin|FATE_API_USER_TOKENS|records" domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py contracts/fate/security` | Gate: 现有 token/owner 边界和 scope 缺口明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约、范围和验证计划 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 ApiPrincipal scopes、record scope 常量和 user token parser | Verify: `rg -n "RECORD_SCOPE_|ApiPrincipal|_user_token_principals|_parse_record_scope_list" domains/experience-delivery/services/fatecat-delivery/src/main.py` | Gate: principal 可携带 scopes，旧 token 默认全部 record scopes | Parallelizable: No
[x] TP-02.02 | P0 | 在 record write/read/list/delete 入口接入 scope gate | Verify: `rg -n "_require_scope\\(principal, RECORD_SCOPE_(WRITE|READ|LIST|DELETE)" domains/experience-delivery/services/fatecat-delivery/src/main.py` | Gate: 每个敏感 record 操作都有对应 scope 检查 | Parallelizable: No
[x] TP-02.03 | P0 | 更新 audit principal metadata 和 production-readiness scoped token 格式校验 | Verify: `bash -n scripts/production-readiness.sh && rg -n "scopeCount|allowed_record_scopes" domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/production-readiness.sh` | Gate: 生产预检可识别 scoped token 且未知 scope 失败 | Parallelizable: No
[x] TP-03.01 | P0 | 登记 rbac SecurityControl 和 schema controlType | Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && python3 -m json.tool contracts/fate/security/schemas/security-control.schema.json >/dev/null` | Gate: `control.rbac_policy` 和 `rbac` controlType 可解析 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 scoped token 行为回归和 registry contract 断言 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'scoped_user_token or rbac or token or record or security'` | Gate: scoped token 行为和 registry 断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 更新 API 接入文档、security AGENTS 和 100% roadmap | Verify: `rg -n "scoped RBAC|record.read|OAuth/OIDC|control.rbac_policy" docs/reference-materials contracts/fate/security/AGENTS.md` | Gate: 文档边界和路线图同步 | Parallelizable: No
[x] TP-04.01 | P0 | 执行 JSON、focused tests、shell syntax、ruff/format、secret scan、quick CI 和 diff check | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: 本地门禁全部通过 | Parallelizable: No
[x] TP-04.02 | P0 | 回填 closeout 状态、全任务树验证和 closeout packet | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py` | Gate: 0028 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
