# Repo Evidence
- 当前分支：`main`。
- 当前基准 commit：`d53dc06e7d06bfbacf99648001fbffd9c5aa6ccb`，commit message `test: expand bazi ziwei quality corpus`。
- 远端 CI：
  - FateCat Acceptance run `28711321429`，`success`，URL `https://github.com/tradecatlabs/fatecat/actions/runs/28711321429`。
  - FateCat Container run `28711321547`，`success`，URL `https://github.com/tradecatlabs/fatecat/actions/runs/28711321547`。
- 0142 本地证据：
  - `/tmp/fatecat-local-ci-20260704233925`，`status=passed`，`389 passed`。
  - `/tmp/fatecat-core-quality-corpus-0142.json`，`status=passed`，`totalCaseCount=340`。
  - `/tmp/fatecat-bazi-ziwei-l4-0142.json`，`status=passed`，`checks=71`。
- 外部验证阻断证据：
  - `/tmp/fatecat-local-ci-20260704233925/external-validation-closure-gate.json`：`status=passed`、`shipGate.status=blocked`、`summary.total=438`、`summary.categories=22`。
  - `/tmp/fatecat-local-ci-20260704233925/external-validation-closure-work-queue.json`：`workItems=22`、`owners=13`、`staleItems=22`。
  - `/tmp/fatecat-local-ci-20260704233925/external-validation-proof-ref-gate.json`：`acceptedProofRefs=0`、`pendingWorkItems=22`。
  - `/tmp/fatecat-local-ci-20260704233925/external-validation-live-proof-gate.json`：`acceptedLiveProofs=0`、`pendingWorkItems=22`。
  - `/tmp/fatecat-local-ci-20260704233925/external-validation-operator-execution-packet.json`：`status=operator_action_required`、`operatorSteps=22`、`domains=12`。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不伪造外部证据 | 所有 live、proof-ref、审计、token、OIDC、SIEM、OTel、Vault/KMS 继续标注待执行。 |
| 当前任务只做计划 | 不修改业务代码、不新增 gate、不执行生产 live。 |
| 任务包必须闭合 | 0143 必须清掉模板占位符并通过 `validate_task_docs.py`。 |
| 资料必须可追溯 | roadmap 中保留官方资料 URL，不把二手总结当事实来源。 |
| 当前 worktree 事实优先 | 0142 的成功证据和 0138/外部验证 pending 证据共同构成计划输入。 |

# Change Boundary
允许修改：
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan/*`
- `governance/tasks/INDEX.md`

禁止修改：
- 生产 provider、report builder、API、Web、Bot、脚本、测试和契约 schema。
- 任何真实密钥、运行态文件或外部 proof/live bundle。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 plan 写成完成 | 审计误判、100% 声明失真 | 所有结论都区分 local passed、remote CI passed、external pending。 |
| 路线图重复膨胀 | 后续执行顺序混乱 | 只新增 post-0142 增量刷新，并修正后续任务编号。 |
| 外部资料过时 | 计划依据弱 | 只引用官方资料，记录 URL 与范式，不引用不可复核摘要。 |
| 0143 占位符残留 | auto-tasks 文档门禁失败 | 执行占位符扫描和 task docs validator。 |
| 外部阻断被掩盖 | 生产门禁被绕过 | roadmap 明确 22 个 pending work items、0 accepted proof refs、0 accepted live proofs。 |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 100% 指基础设施成熟度，不是预测准确率 100%。 | 用户明确要求预测命中率 100%，则必须改写为不可承诺目标。 |
| 当前任务是 planning-only。 | 若用户提供真实外部凭证并要求 live 执行，应另起 external proof/live 执行任务。 |
| 0142 已完成本地核心质量扩容。 | 若远端 CI 或本地 quick CI 对 `d53dc06` 失败，则计划事实需改写。 |
| external closure 仍阻断。 | 只有 proof-ref gate 和 live-proof gate 对 22 个 work item 全部 accepted 才能解除该假设。 |

# Critical Ambiguities
- 是否拥有真实外部 operator 凭证：当前仓库无法确认。
- 是否已有第三方审计人员签署结果：当前仓库只有 intake gate，不存在 accepted result。
- 是否应把后续 0144 先做 external proof/live，还是先做 developer public platform：本计划建议先闭合 external proof/live 的 operator 执行，因为 certification 阻断依赖它。
- 真实生产 SLO、OIDC、SIEM、OTel backend 的平台选型仍需外部环境确认。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bug 修复，不生成 `DEBUG.md`。
- 若验证失败，记录失败命令、失败文件和下一步修复动作。

# Task Package Context Map
| TP | Context |
| --- | --- |
| TP-01 | 吸收 git、CI、0142 local artifacts 和 external validation artifacts。 |
| TP-02 | 对照成熟基础设施官方资料，把能力映射为 FateCat resource domain。 |
| TP-03 | 刷新 roadmap 末尾 post-0142/post-0143 增量计划。 |
| TP-04 | 校验任务包、占位符、索引和文档一致性。 |
