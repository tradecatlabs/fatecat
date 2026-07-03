# Task Overview
- Task ID: `0105`
- Slug: `measurement-infrastructure-current-audit-bundle-evaluation-trend`
- Objective: `执行 0104 后续审计证据收口切片：让 current audit bundle 显式纳入 EvaluationRun evaluation trend gate artifact，把 local-ci 中的 evaluation-trend-gate-smoke/trend-gate.json 写入 evidence index；确保第三方审计能追踪 0104 质量趋势门禁，不保存命令输出、benchmark 标准答案、完整报告正文或真实凭证。`
- Status: `Done`

## In Scope
- 让 `scripts/current-audit-bundle.py` 从 `--local-ci-output-dir` 读取 `evaluation-trend-gate-smoke/trend-gate.json`。
- 将 EvaluationRun trend gate 作为 `evidence.evaluation_trend_gate` 写入 current audit bundle evidence index。
- 更新 current bundle contract、audit AGENTS、regression tests、路线图和任务索引。
- 修复 0104 INDEX 状态漂移，使任务目录、closeout validator 和索引口径一致。

## Out of Scope
- 不修改 EvaluationRun trend gate 判定逻辑。
- 不连接远端 CI、外部 benchmark、真实 Bot/API/HF、OIDC/SIEM/OTel/Vault/KMS 或第三方审计平台。
- 不保存 stdout/stderr tail、benchmark 标准答案、完整报告正文、真实用户输入、token、secret 或 DSN。

## Task Package Tree
```text
TP-01 Audit evidence gap analysis
  TP-01.01 Confirm 0104 task status and current audit bundle coverage gap
  TP-01.02 Define evaluation trend evidence mapping
TP-02 Current audit bundle implementation
  TP-02.01 Add evaluation trend artifact spec to current audit bundle
  TP-02.02 Extend current audit bundle regression fixture and assertions
  TP-02.03 Sync contract, AGENTS and roadmap
TP-03 Validation and closeout
  TP-03.01 Run focused tests, bundle generation and static gates
  TP-03.02 Close task docs, fix task index status and prepare delivery
```

## Requirement Alignment
| Requirement | Implementation Mapping |
| --- | --- |
| 继续按任务树推进 100% 基础设施 | 新增 0105 任务包，作为 0104 后续审计证据收口切片。 |
| 证据包必须可审计 | current audit bundle evidence index 新增 `evidence.evaluation_trend_gate`。 |
| 不伪造外部 live | 仍只读取本地 local-ci artifact；外部 live 留作 pending。 |
| 隐私边界不回退 | 只读取 trend summary 字段，不复制命令输出、答案、报告正文或凭证。 |
| 文档口径统一 | contract、AGENTS、roadmap、task index 同步。 |

## Task Package Overview
| Node | Status | Deliverable |
| --- | --- | --- |
| TP-01 | Done | Gap analysis and evidence mapping |
| TP-02 | Done | current audit bundle evidence and tests |
| TP-03 | Done | validation, closeout and delivery handoff |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
