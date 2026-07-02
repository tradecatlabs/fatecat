# Planning Summary

0065 的目标不是接入真实 OIDC、SIEM 或数据库清理器，而是把安全外部化缺口从“策略说明”推进为“机器可验证证据契约 + 反伪造门禁”。正确终态是：审计者能从仓库判断哪些安全能力仍是 external pending，且任何把本地 token、policy 文档或 placeholder 当作 live evidence 的尝试都会失败。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0065 不能标记 Done，也不能声明 OIDC/IdP、SIEM、不可变审计存储或 retention cleaner 已生产。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确只做 security externalization evidence contract 与 negative gate | Done |
| PLAN | 任务树、边界、验证计划落盘 | Done |
| BUILD | contract、gate、tests、local-ci、docs 接线完成 | Done |
| TEST | validators、gate CLI、focused tests、ruff、secret scan、quick local CI 通过 | Done |
| REVIEW | 不夸大 OIDC/SIEM/retention live 状态 | Done |
| SHIP | commit/push 后可进入下一切片 | Done |

# Simplest Path

复用 `contracts/fate/security/` 作为安全资源真相源；新增一个 evidence contract、一个 Python gate、一个 shell wrapper 和 focused tests。只验证契约结构和反伪造边界，不连接真实 IdP、SIEM 或生产数据库。

# Split Strategy

- TP-01：确认现有安全基线和 0065 标准。
- TP-02：实现机器契约。
- TP-03：实现 gate、测试和 local-ci 接线。
- TP-04：同步文档并完成验收。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核上下文和现状。 |
| 2 | TP-02.01, TP-02.02 | 新增 externalization evidence contract 并挂到安全资源模型。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate、测试、local-ci。 |
| 4 | TP-04.01, TP-04.02 | 文档与验收。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无；0065 security externalization evidence contract baseline 已通过本地验收。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`json.tool`、`pytest`、`ruff`、`secret-scan`、task validators、git |
| forbidden actions | 不切换分支、不连接真实 IdP/SIEM、不读取真实 `.env`、不删除真实数据、不输出 secret |
| expected output | security externalization evidence contract、gate/test/docs/task closeout |
| required evidence | gate CLI、pytest、task validators、ruff、secret scan、quick local CI |
| stop condition | 需要真实 OIDC/SIEM/retention cleaner live 时，标记外部连通验证待执行，不阻塞 contract baseline |

# Future-Optimal Contract

- Target end state: SecurityControl 资源能用统一证据契约证明外部身份、外部审计和 retention 自动清理，而不是靠自然语言承诺。
- Real constraints: 当前没有真实 IdP、SIEM、不可变审计平台或生产清理器。
- Inertia constraints: 旧 scoped token 和 production-security-gate 只能作为本地 baseline。
- Kill list: 删除“本地 token/RBAC 已等于 production IAM”的隐性口径。
- Proof point: `security-externalization-gate` 能验证 pending contract，并拒绝伪造 live evidence。
- Falsifier: gate 接受 `scoped_token_rbac`、placeholder SIEM 或无 smoke 的 retention cleaner 作为 live proof。
- Migration slice: 本轮先做 evidence contract，后续真实平台只需按同一 contract 提供 external evidence。
- Rejected short-term patches: 不把 README 文案当证据；不在 production-security-gate 中继续混入 live evidence 职责。

# Ponytail Contract

- Existence check: 0061 明确 0065 是 P0；现有安全门禁缺 live evidence 反伪造。
- Selected ladder rung: project-native contract + direct gate implementation；不新增外部服务依赖。
- Skipped scope: OAuth library integration、JWKS validation、SIEM exporter、WORM storage、record cleanup scheduler。
- Ceiling / upgrade path: 一旦有真实 IdP/SIEM/DB 环境，新增 live smoke 和 evidence JSON。
- Do-not-simplify: 隐私边界、external pending 状态、dry-run/live 区分不能删除。
- Minimal runnable check: `bash scripts/security-externalization-gate.sh --output-json <path>`。
- Complexity review owner: `auto-review` 的 document-drift、feature-change-safety、ponytail-complexity。

# Document-Driven Contract

- Operating model update: not needed；项目定位未变。
- Toolchain model update: not needed；只新增本地 shell/Python gate，接入现有 local-ci 模式。
- Process update: not needed；继续使用 task validators、local-ci、remote acceptance。
- Source-of-truth updates: planned；`contracts/fate/security`、API 文档和 roadmap。
- Local README/AGENTS impact: planned；`contracts/fate/security/AGENTS.md` 与 `scripts/AGENTS.md`。
- Contract/catalog/schema impact: planned；security schema/registry 新增 externalization evidence contract 链接。
- ADR/Gate/module-context impact: not needed；不改变架构边界，只补同目录 gate。
- Documentation exemption reason: 无；本任务会同步相关文档。
- Validation evidence: gate、focused tests、ruff、secret scan、quick local CI。

# Rollback Protocol

- 删除新增 externalization evidence contract、gate 脚本和 tests。
- 从 security registry/schema/local-ci/docs/AGENTS/roadmap 移除 security externalization 引用。
- 删除 0065 任务包和 INDEX 行。
