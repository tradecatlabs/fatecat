# Task Overview
- Task ID: `0118`
- Slug: `measurement-infrastructure-100-post-0117-deep-research-plan`
- Objective: `基于当前 main worktree、0116/0117 外部验证 closure gate 事实和外部基础设施官方资料，制作 FateCat 达到 100% 测算基础设施所需的完整实现计划、执行任务树、验收门禁和不可伪造证据口径。`
- Status: `Done`

## In Scope
- 调研基础设施同构资料并更新 post-0117 口径。
- 复用 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 作为主路线图。
- 产出 `RESEARCH.md`，整理资源域、当前状态、100% 目标、下一步任务和外部阻断。
- 更新 `governance/tasks/INDEX.md`。

## Out of Scope
- 不实现生产 API、HF、Bot、OIDC、SIEM、OTel、Vault/KMS、Postgres webhook 或第三方审计 live。
- 不修改 capability/provider/runtime 业务代码。
- 不声明 FateCat 已经达到 100% 基础设施。
- 不新增平行路线图真相源。

## Task Package Tree
```text
TP-01 repo baseline and 0117 evidence review
TP-02 external infrastructure research mapping
TP-03 post-0117 100% implementation plan
TP-04 roadmap, task package and validation
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 深度调研资料 | `RESEARCH.md` 记录 OpenAPI、AsyncAPI、CloudEvents、Kubernetes、Backstage、Temporal、OpenTelemetry、SRE、DORA、OWASP、NIST、SLSA、CycloneDX、GitHub Attestations、Stripe 等同构资料。 |
| 制作完整实现计划 | 主路线图新增 post-0117 执行计划、波次、任务树和验收门禁。 |
| 100% 基础设施口径 | 100% 定义为资源化、可恢复、可观测、可审计、可证明发布、可外部复核，不是预测准确率或功能数量。 |
| 不伪造证据 | 外部 live 项继续标记 `外部连通验证待执行`。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | Current HEAD and dirty 0117 context reviewed. |
| TP-02 | Done | Official infrastructure sources mapped in `RESEARCH.md`. |
| TP-03 | Done | Post-0117 plan and MI-100 task tree added. |
| TP-04 | Done | Task package and roadmap updated; validators run in final gate. |

## Reading Order
1. README.md
2. CONTEXT.md
3. RESEARCH.md
4. PLAN.md
5. ACCEPTANCE.md
6. ACCEPTANCE_CHECKLIST.md
7. TODO.md
8. STATUS.md
