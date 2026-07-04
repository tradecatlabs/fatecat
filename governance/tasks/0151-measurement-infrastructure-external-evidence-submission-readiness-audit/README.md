# Task Overview
- Task ID: `0151`
- Slug: `measurement-infrastructure-external-evidence-submission-readiness-audit`
- Objective: `实现外部证据提交准备度审计：聚合 0144-0149 proof-ref、live proof、operator packet、human review、audit rehearsal 与 certification 产物，输出 current HEAD 可提交/待提交/阻断矩阵，不执行真实 live、不伪造外部证据。`
- Status: `In Progress`

## In Scope
- 新增外部证据提交准备度 audit contract、脚本、wrapper 和回归测试。
- 聚合 `external-validation-closure-work-queue`、`proof-ref gate`、`live proof gate`、`operator execution packet`、`core quality human review gate`、`third-party audit rehearsal` 和 `measurement infrastructure certification`。
- 输出 JSON/Markdown readiness matrix，明确哪些证据包可提交、哪些仍需 operator、人审或审计证据。
- 接入 `scripts/local-ci.sh` quick profile 和 summary artifacts。
- 更新 `scripts/AGENTS.md`、`contracts/fate/audit/AGENTS.md`、`tests/AGENTS.md` 与 roadmap。

## Out of Scope
- 不执行真实生产 API、HF Space、Telegram Bot、webhook、Postgres、OIDC、SIEM、OTel、Vault/KMS 或 developer portal live。
- 不上传 proof-ref、live proof、人审、benchmark、no-leak 或 independent audit result bundle。
- 不把 `operator_action_required`、模板、占位 artifact hash、pending gate 写成 passed。
- 不修改测算 provider、CapabilityExecutor、报告输出结构或新术数 capability。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree
```text
0151-measurement-infrastructure-external-evidence-submission-readiness-audit
├── TP-01 现有证据链复核
│   ├── TP-01.01 读取 external proof/live/operator/human review/certification 现有契约
│   └── TP-01.02 确认 local-ci 产物顺序和接入点
├── TP-02 任务容器与契约设计
│   ├── TP-02.01 创建 0151 任务包
│   └── TP-02.02 定义 readiness audit 输出口径和 non-claim
├── TP-03 代码落地
│   ├── TP-03.01 新增 contract/script/wrapper
│   ├── TP-03.02 新增 regression tests
│   └── TP-03.03 接入 local-ci 和 summary artifact
├── TP-04 文档同步
│   ├── TP-04.01 更新 AGENTS 和 roadmap
│   └── TP-04.02 回填任务文档
└── TP-05 验证与交付
    ├── TP-05.01 运行 targeted tests、script smoke、docs validation 和 diff check
    └── TP-05.02 提交、推送并等待远端 Acceptance
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 任务树为核心 | 使用 0151 任务包拆分 TP-01..TP-05，所有叶子有验收证据。 |
| 可验证、可落地 | 新增可执行脚本、contract、测试和 local-ci 接线。 |
| 不伪造外部证据 | 默认结果仍 blocked；审计器只聚合 readiness，不改变 proof/live/human/certification 事实。 |
| 100% 基础设施目标 | 把外部证据提交前检查从人工判断提升为机器产物，为后续 operator 提交和审计闭环降低错误率。 |

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | 现有证据链复核 | Done | 读取 proof-ref/live/operator/human review/local-ci 现有脚本与契约 |
| TP-02 | 任务容器与契约设计 | Done | 0151 任务包和 contract 口径 |
| TP-03 | 代码落地 | In Progress | contract/script/test/local-ci diff |
| TP-04 | 文档同步 | In Progress | AGENTS、roadmap、task docs |
| TP-05 | 验证与交付 | Pending | targeted tests、local-ci、commit/push/CI |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
