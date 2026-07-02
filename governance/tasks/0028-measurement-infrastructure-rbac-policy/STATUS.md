# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None.

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 权限现状和任务边界已确认。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 已盘点 `main.py` auth helpers、records endpoints、security registry 和 tests。 | - | - |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | 任务文档已回填，待最终 validator。 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | runtime scoped RBAC 已实现。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.02 | No | Done | `ApiPrincipal.scopes`、scope 常量和 parser 已新增。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | write/read/list/delete 已接入 `_require_scope`。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | audit `scopeCount` 和 production-readiness scoped token 校验已新增。 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | registry/tests/docs 已同步。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.03 | No | Done | `rbac` schema 和 `control.rbac_policy` 已登记。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | focused tests 已通过。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | API 文档、security AGENTS 和 roadmap 已同步。 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | 验证收口完成。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.03 | No | Done | JSON、focused tests、shell syntax、ruff/format、secret scan、quick CI 和 diff check 已通过。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | closeout validator、全任务树验证和 closeout packet 已通过。 | - | - |

# Blockers
- 无当前本地阻塞。
- 外部连通验证待执行：OAuth/OIDC、外部 IdP、生产 IAM、真实生产 token/live smoke。

# Runtime State
## 2026-07-02
- 已实现本地 scoped token RBAC baseline。
- 已登记 `control.rbac_policy` 并更新 schema。
- 已补 scoped token 行为测试和 registry contract 测试。
- 已更新 production-readiness scoped token 格式校验。
- 已更新 API 文档、security AGENTS 和 100% roadmap。
- quick CI 已通过：90 passed，evidence=/tmp/fatecat-local-ci-20260702102027。

# Evidence Log
- `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && python3 -m json.tool contracts/fate/security/schemas/security-control.schema.json >/dev/null`：PASS。
- `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'scoped_user_token or rbac or token or record or security'`：PASS，15 passed。
- `bash -n scripts/production-readiness.sh`：PASS。
- `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py`：PASS。
- `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py`：PASS，3 files already formatted。
- `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0028.json && python3 -m json.tool /tmp/fatecat-secret-scan-0028.json >/dev/null`：PASS，findingCount=0。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0028-measurement-infrastructure-rbac-policy --phase decompose`：PASS。
- `bash scripts/local-ci.sh --profile quick`：PASS，90 passed，evidence=/tmp/fatecat-local-ci-20260702102027。
- `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py && git diff --check`：PASS。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0028-measurement-infrastructure-rbac-policy --phase closeout`：PASS。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto`：PASS，task_total=28，valid=28，invalid=0。
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/build_task_closeout.py --task-dir governance/tasks/0028-measurement-infrastructure-rbac-policy --out governance/tasks/0028-measurement-infrastructure-rbac-policy/TASK_CLOSEOUT_PACKET.json --strict`：PASS。
