# Repo Evidence
- 调试模式: Optional
- `main.py` 原有 `ApiPrincipal(role,user_id)`、`_require_record_access()`、`_require_owner_or_admin()`，能验证 token 和 owner，但没有显式 operation scope。
- `FATE_API_USER_TOKENS` 原格式为 `user_id:token`，一个用户 token 可读、列、写、删全部记录接口操作。
- 记录接口包括 `calculate_bazi?user_id=...`、`get_record`、`get_user_records`、`delete_record`。
- `contracts/fate/security/registry.json` 原有 `control.record_token_access`，但没有独立 RBAC control。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 将 `MI-09.01 scoped RBAC baseline` 登记为下一步任务。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 向后兼容 | `user_id:token` 保留，默认拥有全部 record scopes。 |
| 最小实现 | 不引入 OAuth/OIDC、不改 DB、不加依赖。 |
| 权限最小化 | 新格式只授予显式 scope，缺 scope 返回 403 `权限不足`。 |
| owner 边界不削弱 | 即使 scope 足够，用户 token 仍只能访问自己的记录。 |
| 不泄露凭证 | 日志、registry、文档只写变量名和 scope 名，不输出 token 值。 |

# Change Boundary
- 可改：`main.py`、`scripts/production-readiness.sh`、security schema/registry、API/contract tests、API 文档、security AGENTS、100% roadmap、0028 任务文档。
- 不改：数据库 schema、计算逻辑、报告结构、Web UI、Bot、provider、真实生产配置。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 旧 user token 行为被破坏 | 现有接入失败 | 旧格式默认全部 record scopes，回归测试覆盖写入。 |
| scoped token 解析歧义 | 权限误授予 | token 格式限定 `user_id:token:scope1|scope2`，未知 scope 不授权，生产预检失败。 |
| RBAC 被误读为生产 IAM | 审计夸大 | registry/docs 明确不是 OAuth/OIDC、外部 IdP 或多租户 IAM。 |
| 审计日志泄露 scope 外信息 | 隐私风险 | audit principal 只加 `scopeCount`，不输出 token 和 userId 原文。 |

# Assumptions and Falsification
- 假设：记录接口本地 RBAC baseline 只需要 admin/user/owner/scopes 四层。反证：若需要组织、租户、角色继承或外部 claims，则进入 OIDC/IAM 后续任务。
- 假设：scope 只覆盖 records API，不覆盖公开测算计算。反证：如未来用户记录以外的敏感资源出现，应新增资源 scope。
- 假设：旧 `user_id:token` 兼容必须保留。反证：若用户决定破坏性收紧生产 token，需另起迁移任务。

# Critical Ambiguities
- 生产身份系统供应商未定；本任务不选择 OIDC provider。
- 是否要对 admin token 加可配置 scope 未定；本任务中 admin token 默认拥有全部 record scopes。
- scoped token 的 token 字符串不支持冒号；后续若需要更复杂凭证格式，应迁移到结构化 secret/IdP。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 若 scoped token 测试失败，必须记录失败命令和修复结果到 `STATUS.md`。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 盘点 auth/runtime/registry/doc 缺口。 |
| TP-02 | 修改 runtime scope 模型、endpoint gates 和 production-readiness。 |
| TP-03 | 补 SecurityControl、tests、docs、roadmap。 |
| TP-04 | 执行 validators、quick CI 和 closeout packet。 |

# Blockers
- 无当前本地阻塞。
- 外部连通验证待执行：OAuth/OIDC、外部 IdP、生产 IAM、真实 token/live smoke。
