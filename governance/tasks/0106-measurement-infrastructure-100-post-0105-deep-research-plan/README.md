# Task Overview
- Task ID: `0106`
- Slug: `measurement-infrastructure-100-post-0105-deep-research-plan`
- Objective: `基于当前 main worktree、0104/0105 evaluation trend gate 与 current audit bundle 已完成事实、当前 HEAD 无可见远端 GitHub Actions run 的事实，以及 OpenAPI 3.2.0、AsyncAPI 3.1.0、CloudEvents、Kubernetes Controller、Backstage、Temporal、OpenTelemetry、DORA、SLSA 1.2、CycloneDX、GitHub Artifact Attestations 等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、执行波次、远端证据缺口和不可伪造验收口径；本任务只落盘调研与计划，不实现业务代码、不伪造远端 CI 或生产 live。`
- Status: `Done`

## In Scope
- 查询并整理基础设施官方或事实标准资料，更新 0105 之后的同构映射。
- 复核当前 `main`、0104/0105 任务事实、远端 Actions 可见性和主路线图。
- 输出 post-0105 资源成熟度矩阵、剩余差距、执行波次和下一批任务建议。
- 更新主路线图，明确当前 HEAD 无可见远端 CI run 是 release proof 缺口。
- 回填本任务任务包并通过 `auto-tasks` 文档校验。

## Out of Scope
- 不实现新的业务代码、capability provider、workflow、脚本或生产部署。
- 不触发真实生产 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS。
- 不把本地 local-ci、planning 文档或 blocked bundle 写成 100% 完成。
- 不修改 0104/0105 已完成实现，只引用其验证事实。

## Task Package Tree
```text
TP-01 调研基础设施同构资料
  TP-01.01 复核官方资料版本和适用性
  TP-01.02 提炼 FateCat post-0105 映射原则
TP-02 复核仓库当前状态
  TP-02.01 读取主路线图和 0104/0105 任务事实
  TP-02.02 识别当前 HEAD 的远端证据缺口
TP-03 制作 100% 完整实现计划刷新
  TP-03.01 定义资源成熟度矩阵
  TP-03.02 定义执行波次、下一任务树和不可伪造证据
TP-04 落盘与验证
  TP-04.01 更新 RESEARCH、任务包和主路线图
  TP-04.02 运行文档校验、占位符检查和引用检查
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 深度调研查询资料 | `RESEARCH.md` 记录官方资料、版本事实和 FateCat 映射。 |
| 制作 100% 基础设施完整实现计划 | 主路线图新增 post-0105 计划，任务包沉淀执行波次和验收口径。 |
| 基于当前 worktree | 记录 `main` 当前 HEAD、0105 Done、远端 Actions 对当前 HEAD 不可见。 |
| 不伪造生产完成 | 所有外部 live、第三方审计、远端 CI current commit 均按证据状态标注。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | Source matrix written in `RESEARCH.md`. |
| TP-01.02 | Done | Mapping rules written. |
| TP-02.01 | Done | Roadmap and 0104/0105 docs inspected. |
| TP-02.02 | Done | `gh run list --commit HEAD` returned no visible runs and was recorded as missing/pending. |
| TP-03.01 | Done | Resource maturity matrix written. |
| TP-03.02 | Done | Waves, next tasks and falsifiers written. |
| TP-04.01 | Done | Roadmap/task docs patched. |
| TP-04.02 | Done | Validator and scans passed. |

## Reading Order
1. README.md
2. RESEARCH.md
3. CONTEXT.md
4. PLAN.md
5. ACCEPTANCE.md
6. ACCEPTANCE_CHECKLIST.md
7. TODO.md
8. STATUS.md
