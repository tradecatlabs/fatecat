# Repo Evidence

- `git status --short --branch` 输出 `## main...origin/main`，0065 开始前 worktree 干净。
- `governance/tasks/INDEX.md` 最新已完成任务为 `0064 measurement-infrastructure-otel-collector-slo-adapter`。
- 0061 roadmap 推荐 0065：`security externalization`，要求 `OIDC/SIEM/retention cleaner implementation plan + negative tests`，不能用本地 token 代替 IdP。
- `contracts/fate/security/production-security-policy.json` 已有生产身份、SIEM、retention 和 OWASP API Security Top 10 策略。
- `scripts/production-security-gate.py` 已验证策略完整性，但未验证 live evidence 的反伪造结构。
- `scripts/local-ci.sh --profile quick` 已运行 `production-security-gate`，尚未运行单独的 security externalization gate。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Target end state | FateCat 的 SecurityControl 资源能区分本地 scoped token baseline、外部 OIDC/IdP live evidence、外部 SIEM/不可变审计 evidence 和 retention cleaner smoke evidence。 |
| Real constraints | 当前没有真实 IdP、SIEM、WORM 存储、生产数据库或 live retention cleaner；不能读取真实 `.env`。 |
| Inertia constraints | 现有 `production-security-gate` 是策略完整性 gate，不应被误当成外部生产平台验证。 |
| Wrong concept / wrong boundary | “本地 token/RBAC 可用”等于“生产 OIDC/IdP 可用”是错误边界，必须用负向 gate 拒绝。 |
| Change boundary | 只改 security contracts、gate scripts、tests、local-ci、docs、AGENTS、roadmap 和 0065 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。0065 是 contract/gate 新增，不是已复现 bug；若 gate/test 失败再补 DEBUG 证据。 |

# Change Boundary

- 允许修改：`contracts/fate/security/`、`scripts/security-externalization-gate.*`、`scripts/local-ci.sh`、`scripts/AGENTS.md`、`tests/regression/test_production_security_gate.py`、API 文档、roadmap、0065 任务文档和 `governance/tasks/INDEX.md`。
- 禁止修改：真实身份实现、真实 SIEM export、生产数据库清理、业务算法、真实 `.env`、外部部署凭证。
- 本轮只落 externalization contract/gate baseline；任何真实平台 live evidence 只能登记为 pending。

# Critical Ambiguities

- 真实 IdP/OIDC 供应商未知：不阻塞 evidence contract，但阻止声明 production IAM 已完成。
- 真实 SIEM/不可变审计平台未知：不阻塞 gate，但阻止声明 external SIEM live 已完成。
- 真实 retention cleaner 的数据存储和删除模式未知：不阻塞 contract，但阻止声明 record cleanup 已上线。

# Debug Evidence Contract

- 调试模式: Optional
- 0065 是 contract/gate 新增，不是已复现 bug；如果 JSON、gate、pytest 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 把 scoped token 当作 OIDC | Gate 必须负测拒绝 `scoped_token_rbac` / `local_token` 作为 identity live proof。 |
| 把 policy 登记当作 SIEM live | Evidence contract 明确 live SIEM 需要外部 proof ref、immutability mode 和 no-payload boundary。 |
| 把 retention plan 当作清理器实现 | Contract 明确 retention cleaner 需要 smoke evidence、dry-run summary 和 audit action。 |
| 泄露真实 endpoint/secret | Contract/gate output 只允许 proof refs 和脱敏摘要，不输出 endpoint、token、payload 或用户数据。 |
| quick CI 漏跑新 gate | `local-ci.sh --profile quick` 必须生成 `security-externalization-gate.json` artifact。 |

# Assumptions and Falsification

- Assumption: 0065 可复用现有 security registry 与 production-security-policy，不需要新增真实 IAM/SIEM 依赖。
- Falsifier: 如果现有 registry 未登记 OIDC/SIEM/retention controls，0065 不能 closeout，必须先补 SecurityControl。
- Assumption: 负向 evidence 可以用临时 JSON fixture 在测试中构造，不需要提交真实 live evidence。
- Falsifier: 如果 gate 不能区分 fake evidence 与 pending contract，0065 不可 closeout。

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0061/0064 任务、security registry、production-security-policy、production-security-gate、local-ci、API docs。 |
| TP-02.01 | `contracts/fate/security/` 是安全契约真相源。 |
| TP-02.02 | `contracts/fate/security/AGENTS.md` 和 schema 必须同步新增 contract 边界。 |
| TP-03.01 | 复用现有 gate 脚本风格，不新增外部服务依赖。 |
| TP-03.02 | `tests/regression/test_production_security_gate.py` 是现有安全 gate 测试落点。 |
| TP-03.03 | `scripts/local-ci.sh` quick profile 已运行 production security gate，可插入新 gate artifact。 |
| TP-04.01 | API docs 与 roadmap 是人类接入口径真相源。 |
| TP-04.02 | validators、focused tests、ruff、secret scan、quick local CI 是 closeout 证据。 |
