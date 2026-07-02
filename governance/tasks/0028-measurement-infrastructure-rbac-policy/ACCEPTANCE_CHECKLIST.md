# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] 旧 `user_id:token` 格式保持兼容。
- [x] 新 scoped token 格式执行最小权限。
- [x] owner 边界不削弱。
- [x] registry/docs 不伪造 OAuth/OIDC 或生产 IAM。
- [x] focused tests、secret scan、ruff、format、quick CI、diff check 全部通过。
- [x] task validators、全任务树验证和 closeout packet 通过。

# Task Package Checklists

## TP-01.01 盘点现有权限边界
- [x] Verify: `rg -n "ApiPrincipal|_require_record_access|_require_owner_or_admin|FATE_API_USER_TOKENS|records" domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py contracts/fate/security`
- [x] Gate: token、owner 和缺失 scope 的现状已确认。

## TP-01.02 回填任务契约
- [x] Verify: `validate_task_docs.py --phase decompose`
- [x] Gate: 任务树、scope 边界、out-of-scope 和验证计划已落盘。

## TP-02.01 新增 Principal scopes 和 parser
- [x] Verify: `rg -n "RECORD_SCOPE_|ApiPrincipal|_user_token_principals|_parse_record_scope_list" domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: admin/user principal 可携带 record scopes。

## TP-02.02 接入 endpoint scope gate
- [x] Verify: `rg -n "_require_scope\\(principal, RECORD_SCOPE_(WRITE|READ|LIST|DELETE)" domains/experience-delivery/services/fatecat-delivery/src/main.py`
- [x] Gate: write/read/list/delete 均检查对应 scope。

## TP-02.03 更新 audit 和 production readiness
- [x] Verify: `rg -n "scopeCount|record.read\\|record.list|unknown record scope|allowed_record_scopes" domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/production-readiness.sh`
- [x] Gate: audit 不输出 scope 明细或 token；生产预检识别 scoped 格式和未知 scope。

## TP-03.01 登记 RBAC SecurityControl
- [x] Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "control.rbac_policy|\\\"rbac\\\"" contracts/fate/security`
- [x] Gate: `/security` 可发现 RBAC control。

## TP-03.02 新增 scoped token 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'scoped_user_token or rbac or token or record or security'`
- [x] Gate: scoped read/list/write/delete negative/positive cases 通过。

## TP-03.03 更新文档和 roadmap
- [x] Verify: `rg -n "scoped RBAC|record.read|OAuth/OIDC|control.rbac_policy" docs/reference-materials contracts/fate/security/AGENTS.md`
- [x] Gate: 文档明确本地 RBAC baseline 与外部身份系统边界。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py`
- [x] Gate: 0028 closeout 和全任务树校验通过。
