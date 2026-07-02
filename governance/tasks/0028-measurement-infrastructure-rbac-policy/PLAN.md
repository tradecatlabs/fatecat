# Planning Summary
本轮把记录接口权限从隐含 token/owner 检查推进为本地可验证 scoped RBAC baseline：显式 record scopes、兼容旧 token、支持 scoped token、登记 SecurityControl、补回归测试和生产预检格式校验。

# Lifecycle Gates
- SPEC：确认范围只覆盖本地 records API scoped RBAC。
- PLAN：任务树、验收、风险、out-of-scope 落盘。
- BUILD：实现 `ApiPrincipal.scopes`、scope parser、`_require_scope()` 和 endpoint gates。
- TEST：JSON、focused tests、shell syntax、ruff、format、secret scan、quick CI、diff check。
- REVIEW：检查旧格式兼容、scope 缺失拒绝、owner 边界不削弱、文档不夸大 OIDC/IAM。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
在现有 token/owner 鉴权函数上加一层 scope，不新增 auth service、不新增依赖、不改数据库；生产身份系统保留为后续任务。

# Split Strategy
先 runtime scope gate，再 registry/schema/tests，最后 docs/roadmap/task closeout。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 现状和任务契约 |
| Wave 2 | TP-02 | runtime scoped RBAC |
| Wave 3 | TP-03 | registry/tests/docs |
| Wave 4 | TP-04 | 验证与 closeout |

# Runtime Workflow Contract
- 旧格式：`FATE_API_USER_TOKENS` 值形态为 `用户ID:占位令牌`，默认 `record.read/list/write/delete`。
- 新格式：`FATE_API_USER_TOKENS` 值形态为 `用户ID:占位令牌:record.read|record.list`，只授权声明 scope。
- 缺 scope 返回 403 `权限不足`。
- 跨 owner 返回 403 `无权访问该记录`。
- production-readiness 对未知 scope 直接失败。

# Next Executable Leaves
- TP-04.01：执行完整本地门禁。
- TP-04.02：回填 closeout 和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Future-Optimal Contract
Target end state: 记录接口权限进入测算基础设施安全控制面，身份、owner、operation scope 可审计、可测试、可发现。

Real constraints: 当前没有生产 OIDC/IdP；必须兼容现有 `FATE_API_USER_TOKENS=user_id:token`；不能泄露 token 和用户 ID 原文。

Inertia constraints: 原共享 token 模式和散落 owner 判断不能决定最终权限模型。

Kill list: “有 user token 就能做所有 record 操作”“记录接口 auth 只登记 token 不登记 scope”“本地 scoped token 等同 OAuth/OIDC”。

Proof point: focused tests 证明旧 token 兼容、新 scoped token 缺 scope 被拒绝、有 scope 可执行、registry 发现 RBAC control。

Falsifier: 如果旧 token 写入回归失败，或 scoped read token 能写/删记录，则本任务失败。

Migration slice: 本轮实现本地 scoped token baseline；后续迁移到 OIDC/IAM 时复用 role/scope/owner 语义。

Rejected short-term patches: 不只改文档登记 RBAC；不直接接 OIDC；不跳过 negative tests。

# Ponytail Contract
Existence check: RBAC 是 100% 基础设施计划中的本地安全缺口，直接保护 records API，必须存在。

Selected ladder rung: 项目内直接实现薄 scope gate，复用现有 FastAPI/header/env/auth helpers。

Skipped scope: OAuth/OIDC、外部 IdP、多租户组织、角色继承、DB 权限表、admin scoped token。

Ceiling / upgrade path: 当公网多租户、组织级权限或第三方开发者账号出现时，升级到 OIDC/IAM 和结构化 token claims。

Do-not-simplify: owner 边界、403 行为、token 脱敏、生产预检格式校验必须保留。

Minimal runnable check: focused tests、security contract tests、production-readiness shell syntax、quick CI。

Complexity review owner: auto-review/security/document-drift/ponytail-complexity。

# Documentation Impact
Operating model update: not needed；项目定位不变。

Toolchain model update: not needed；未新增工具。

Process update: not needed；沿用现有 local-ci、security smoke 和 task validators。

Source-of-truth updates: updated；security registry、schema、API 文档、100% roadmap 和 security AGENTS 已更新。

Local README/AGENTS impact: updated；`contracts/fate/security/AGENTS.md` 已补 scoped RBAC 边界。

Contract/catalog/schema impact: updated；`security-control.schema.json` 新增 `rbac`，`registry.json` 新增 `control.rbac_policy`。

ADR/Gate/module-context impact: not needed；本任务是局部安全 baseline，不改变架构边界。

Documentation exemption reason: 无需新增 ADR；若后续接 OIDC/IAM 再记录架构决策。

Validation evidence: 见 `STATUS.md`。

# Rollback Protocol
- 恢复 `main.py` 的 scope 常量、`ApiPrincipal.scopes`、`_require_scope()` 和 endpoint 调用点。
- 恢复 `scripts/production-readiness.sh` scoped token 校验改动。
- 恢复 security schema/registry、tests、docs、roadmap 和 0028 任务文档。
- 不得影响 0010-0027 已落地基础设施切片。
