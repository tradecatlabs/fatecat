# Repo Evidence

- 调试模式: Optional
- 0128 已生成外部验证关闭证据摘要：`contracts/fate/audit/external-validation-closure-evidence-summary.json`、`scripts/external-validation-closure-evidence-summary.py`。
- certification 聚合器仍保持 blocked 语义：`scripts/measurement-infrastructure-certification.py`。
- audit handoff / dry-run / current bundle 已存在：`scripts/audit-handoff.py`、`scripts/audit-handoff-dry-run.py`、`scripts/current-audit-bundle.py`。
- roadmap 第 7/8 节仍要求外部连通验证待执行，真实第三方审计未完成。

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| 无真实外部凭证 | 只生成本地预演包，不连接外部系统。 |
| 不替代第三方审计 | `nonClaims` 和 `rehearsalGate` 明确 blocked 条件。 |
| 不泄露敏感值 | forbidden fragments 覆盖 token/secret/DSN/raw URL。 |
| 不引入新平台 | 复用现有 JSON artifact 和 local-ci。 |

# Change Boundary

Allowed:

- `contracts/fate/audit/third-party-audit-rehearsal.json`
- `scripts/third-party-audit-rehearsal.py`
- `scripts/third-party-audit-rehearsal.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_third_party_audit_rehearsal.py`
- `contracts/fate/audit/AGENTS.md`
- `scripts/AGENTS.md`
- `tests/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/INDEX.md`
- `governance/tasks/0129-measurement-infrastructure-third-party-audit-rehearsal/`

Not allowed:

- 真实 production API/HF/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS/developer portal/sandbox live 调用。
- 真实 token、secret、DSN、webhook secret、URL、chat id、生产日志、报告正文或用户输入。
- 关闭 third-party audit、production live 或 100% certification 阻断。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 rehearsal passed 误读成第三方审计通过 | 审计和发布结论失真 | `status=passed` 与 `rehearsalGate=blocked` 分离。 |
| 复制输入 JSON 中的 raw URL 或 secret | 隐私和安全事故 | 输出只做摘要，并有 raw URL / sensitive marker 拒绝。 |
| 与 certification 形成循环依赖 | local-ci 依赖错乱 | rehearsal 在 certification 后执行，只消费 certification 结果，不反向要求 certification 消费 rehearsal。 |
| quick CI 产物过大或重复 | 交付噪音 | 只新增一个 JSON 和一个 Markdown。 |

# Assumptions and Falsification

- Assumption: 当前阶段没有真实外部凭证。Falsifier: 用户提供真实生产 URL/token/DSN/Bot/外部平台权限，则应进入 live 执行任务，而非继续只做 rehearsal。
- Assumption: 正确推进方式是继续补齐不可伪造证据链。Falsifier: 任一输出把 external pending 或 third-party audit missing 写成 passed。
- Assumption: 独立审计结果未来应作为外部 proof-ref/live evidence 或新的 signed review artifact 接入。Falsifier: 审计方要求完全不同的 evidence schema，则后续新增适配器。

# Critical Ambiguities

- 外部审计人员、签名格式、审计系统和 review storage 尚未指定；本任务只生成本地预演包。
- 真实外部 live evidence 的采集顺序已由 operator packet 定义；本任务不重新设计执行命令。

# Debug Evidence Contract

- 调试模式: Optional
- 本任务不是 bugfix；若 JSON、gate、pytest、local-ci 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01 | roadmap 6.23/7/8、0128 任务包、audit/certification scripts。 |
| TP-02 | `third-party-audit-rehearsal.json` contract 与 Python generator。 |
| TP-03 | `scripts/local-ci.sh` artifact 和 regression test。 |
| TP-04 | AGENTS、roadmap 和 task index 文档同步。 |
| TP-05 | focused pytest、ruff、format、secret scan、task docs、quick CI。 |
| TP-06 | git commit/push 与远端 Acceptance/Container CI。 |
