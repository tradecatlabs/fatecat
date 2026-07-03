# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean after 0082 push, then 0083 implementation creates tracked diff |
| `governance/tasks/INDEX.md` | 0065 已完成 security externalization baseline；0082 已完成 observability staged gate |
| `contracts/fate/security/externalization-evidence-contract.json` | 0065 已有 OIDC/SIEM/retention evidence contract，但缺统一 proof-ref prefix invariant 和 raw URL 泛化拒绝 |
| `scripts/security-externalization-gate.py` | 已验证 negative cases，但需要把 proof-ref allowlist 和 raw URL 禁入做成 gate 规则 |
| `contracts/fate/security/production-security-policy.json` | 声明 OIDC/SIEM/retention 是生产准入 contract，不保存真实外部配置 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0083 标记为 OIDC/SIEM/retention staged gate，真实 live 仍需 IdP/SIEM 权限 |
| `scripts/local-ci.sh` | quick profile 已运行 security externalization gate，可承载加固后的 artifact |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造 live | gate 默认 pending；无完整 live evidence 时保持 `外部连通验证待执行` |
| 不泄露 endpoint | 输入 evidence 中的 proof ref 必须是 `evidence://`、`artifact://` 或 `ci-artifact://` |
| 不重复建系统 | 复用 0065 的 contract/gate，只加固校验规则 |
| 不删除真实数据 | retention cleaner evidence 只接受 dry-run/smoke proof refs，不接受 production deletion marker |
| 不新增外部依赖 | 只用 Python 标准库和现有 regression/local-ci 模式 |

# Change Boundary
- Allowed: `contracts/fate/security/`、`scripts/security-externalization-gate.py`、`tests/regression/test_production_security_gate.py`、`tests/regression/test_capability_protocol.py`、`docs/reference-materials/roadmap/`、`governance/tasks/0083-*`、`scripts/AGENTS.md`。
- Read-only context: 0038/0065 security tasks、production security policy、security registry、0082 staged gate pattern。
- Forbidden: 真实 IdP/SIEM 连接、真实 URL/secret 入仓、生产清理器实现、生产数据删除、把 pending 写成 live passed。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| raw issuer/JWKS/SIEM URL 被当 proof ref 入仓 | gate 对 submitted evidence 启用 raw URL 禁入和 proof-ref prefix 白名单 |
| scoped token 被包装成 OIDC live | negative case 继续拒绝 scoped token 伪证 |
| retention cleaner proof 伪造成生产删除完成 | 新增 production_deleted/hard_delete/dryRun=false 负例 |
| 文档把 staged gate 写成真实外部接入 | roadmap、AGENTS 和 task docs 明确 external live 仍待执行 |

# Assumptions and Falsification
- Assumption: 下一个有价值切片是收紧 0065 security externalization staged gate，而不是新建一套 OIDC/SIEM runner。
- Falsifier: 如果已有 gate 能拒绝所有 raw URL、真实 endpoint、production deletion marker 和非白名单 proof refs，则本任务应收缩为文档校准。
- Assumption: live proof refs 只能保存脱敏句柄，不保存真实 issuer/JWKS/SIEM endpoint。
- Falsifier: 如果审计必须保存真实 URL，则必须放进受保护外部证据系统，不能写入本 repo。

# Critical Ambiguities
- 当前没有真实 OIDC/IdP、JWKS、外部 SIEM、不可变审计存储、生产数据库或 retention cleaner 权限。
- 本任务只能证明 staged evidence contract/gate 能识别伪证和泄密风险；真实 live 仍需外部 operator 后续执行。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务是 security evidence gate hardening，不是 bugfix；若 gate、CI 或 regression 失败，则记录失败命令、根因、修复和回归证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | security registry、externalization contract、production security policy、roadmap |
| TP-01.02 | proof-ref allowlist、raw URL rejection、retention non-claim boundary |
| TP-02.01 | identity/SIEM/retention live evidence schema |
| TP-02.02 | negative cases、sensitive scan、raw URL and production deletion rejection |
| TP-03.01 | `scripts/security-externalization-gate.py` and evidence contract |
| TP-03.02 | security schema、AGENTS、roadmap、task index |
| TP-04.01 | `tests/regression/test_production_security_gate.py` and `test_capability_protocol.py` |
| TP-04.02 | JSON validation、gate、pytest、ruff、secret scan、quick CI、task validators |
| TP-05.01 | closeout docs and external pending list |
| TP-05.02 | git/CI delivery evidence boundary |
