# Task Overview
- Task ID: `0104`
- Slug: `measurement-infrastructure-evaluation-trend-store`
- Objective: `执行 0099 后续本地可执行质量趋势库切片：新增 EvaluationRun history trend policy/gate/smoke，把 run-evaluations history/latest 从单次记录升级为可审计趋势门禁；拒绝最新失败、连续失败、缺失 required run 或失败命令；不保存命令输出、benchmark 标准答案、报告正文或真实凭证。`
- Status: `Done`

## In Scope
- 新增 EvaluationRun history trend policy，作为本地质量趋势库的机器可读策略。
- 新增 trend gate 脚本，读取 `run-evaluations` 的 history/latest summary，拒绝最新失败、连续失败、缺失 required run 和失败命令。
- 新增 synthetic smoke、focused regression、quick CI 接线、registry metadata 和目录级 AGENTS 文档。
- 刷新测算基础设施 100% 路线图，把质量趋势库纳入 Post-0103 最短路径。

## Out of Scope
- 不连接外部 benchmark、真实模型 API、生产 Bot、生产 API、真实监控或第三方审计平台。
- 不保存 stdout/stderr tail、benchmark 标准答案、完整报告正文、真实用户输入、token、secret、DSN。
- 不改变八字/紫微 provider 算法，不新增术数体系，不宣称预测准确率或基础设施 100% 已完成。

## Task Package Tree
```text
TP-01 Evaluation trend store specification
  TP-01.01 Inspect existing EvaluationRun runner/history/dashboard contracts
  TP-01.02 Define trend policy and privacy boundary
TP-02 Trend gate implementation
  TP-02.01 Add trend gate CLI and shell wrapper
  TP-02.02 Add synthetic smoke and quick CI wiring
  TP-02.03 Add registry and AGENTS documentation
TP-03 Regression and route-plan refresh
  TP-03.01 Add focused regression tests
  TP-03.02 Refresh 100% infrastructure plan with Post-0103 quality trend store path
TP-04 Closeout and version control
  TP-04.01 Run validators, focused tests, smoke, lint, secret/diff checks
  TP-04.02 Close task docs and prepare git delivery
```

## Requirement Alignment
| Requirement | Implementation Mapping |
| --- | --- |
| 深度调研并制作 100% 基础设施实现计划 | 更新 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 Post-0103 调研刷新、资源模型和任务树。 |
| 当前质量门禁要可长期复核 | `trend-policy.json` + `evaluation-trend-gate.py` 读取 history/latest，不只看单次 summary。 |
| 不伪造外部生产结论 | Trend gate `productionBoundary` 明确只证明本地趋势策略；外部 live 仍是 `外部连通验证待执行`。 |
| 隐私治理 | Trend gate 和 smoke 不复制命令输出、标准答案、报告正文或真实凭证。 |
| 进入本地门禁 | `scripts/local-ci.sh --profile quick` 接入 synthetic smoke 和 focused regression。 |

## Task Package Overview
| Node | Status | Deliverable |
| --- | --- | --- |
| TP-01 | Done | Trend policy and privacy boundary |
| TP-02 | Done | CLI, smoke, CI wiring, registry, AGENTS |
| TP-03 | Done | Regression tests and roadmap refresh |
| TP-04 | Done | Validation, closeout, version control handoff |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
