# Planning Summary
把 D8 安全/隐私从“本地 token/RBAC/audit/retention baseline”推进到“生产身份、外部审计、retention 和 OWASP 回归有机器可读准入合同”。本轮不做真实外部集成，只做本地可验证 contract、gate、文档和 CI。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Requirement | Status |
| --- | --- | --- |
| SPEC | 明确本轮是 contract/gate baseline，不是生产 OIDC/SIEM 实接 | Passed |
| PLAN | 身份、SIEM、retention、OWASP、CI、docs 分包清楚 | Passed |
| BUILD | policy、registry、gate、readiness、tests、docs 落地 | Passed |
| TEST | focused validation 和 local quick CI 通过 | Passed |
| REVIEW | 外部连通、隐私、删除风险、兼容性已自审 | Passed |
| SHIP | 任务文档与 closeout packet 生成 | Pending closeout generation |

# Simplest Path
1. 复用现有 SecurityControl registry，不新增单独安全 API。
2. 用 JSON policy 描述 OIDC/SIEM/retention/OWASP 准入条件。
3. 用本地 gate 验证 policy、schema 和 registry 一致性。
4. production-readiness 只在显式启用相关生产能力时阻断，默认输出 warning。
5. tests 与 quick CI 保护 contract 不漂移。

# Split Strategy
- TP-01 先确认 D8 缺口。
- TP-02 落策略和资源合同。
- TP-03 把合同变成可执行 gate。
- TP-04 接入测试、CI 和文档。
- TP-05 做验证与 closeout。

# Execution Waves
| Wave | Packages | Result |
| --- | --- | --- |
| Wave 1 | TP-01 | 现状和边界确认完成。 |
| Wave 2 | TP-02, TP-03 | policy、registry、gate 和 readiness 完成。 |
| Wave 3 | TP-04 | tests、CI、docs 完成。 |
| Wave 4 | TP-05 | validation 和 closeout 完成。 |

# Runtime Workflow Contract
- Gate output must not include env values or sensitive payloads.
- Registry controls for real OIDC/SIEM/cleanup stay manual/external pending.
- `production-readiness.sh` may fail only when production features are explicitly enabled with incomplete static config.
- Quick CI must run `production-security-gate` before general pytest.

# Next Executable Leaves
无；任务实现完成，剩余动作为 closeout packet 生成与验证。

# Dependency Graph
```text
TP-01.01
  -> TP-02.01 -> TP-02.02
  -> TP-03.01 -> TP-03.02
  -> TP-04.01 -> TP-04.02
  -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
