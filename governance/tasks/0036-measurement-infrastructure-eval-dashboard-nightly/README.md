# Task Overview
- Task ID: `0036`
- Slug: `measurement-infrastructure-eval-dashboard-nightly`
- Objective: `把 EvaluationRun runner/history/diff 从 JSON 证据推进为本地可读评测 dashboard 与 nightly baseline：新增 evaluation dashboard renderer、dry-run dashboard smoke、nightly wrapper 和 GitHub scheduled workflow artifact，接入 quick CI、文档、roadmap 与任务 closeout；不接外部监控平台、不调用外部模型 API、不把 benchmark 标准答案注入生产路径。`
- Status: `Done`

## In Scope
- 新增 `scripts/evaluation-dashboard.py/.sh`，把 EvaluationRun summary 与可选 diff 渲染为静态 HTML dashboard。
- 新增 `scripts/evaluation-dashboard-smoke.sh`，用 dry-run summary 验证 dashboard artifact 和隐私边界。
- 新增 `scripts/evaluation-nightly.sh`，执行 releaseRequired EvaluationRun、history/latest、diff 和 dashboard artifact。
- 新增 `.github/workflows/evaluation-nightly.yml`，提供手动和定时远端 artifact 入口。
- 更新 `contracts/fate/evaluations/registry.json`，登记 `run.evaluation_dashboard_smoke` 和 dashboard/nightly 命令。
- 新增 `tests/regression/test_evaluation_dashboard.py`，同步 runner/API/protocol 测试和 quick CI。
- 同步 `.github`、`scripts`、`contracts/fate/evaluations` AGENTS、API 接入文档、100% roadmap 和任务 closeout。

## Out of Scope
- 不接外部监控平台、Grafana、云对象存储或长期结果数据库。
- 不执行真实生产 API 域名、真实 CORS、真实 token、真实 Bot 或 webhook live smoke。
- 不默认执行 `requires_reference_repo` 的 MingLi-Bench 完整评测。
- 不调用外部模型 API，不把 benchmark 标准答案注入 production provider。
- 不展示 stdout/stderr tail、报告正文、真实用户输入、token、secret、DSN 或私有 raw 资料。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 EvaluationRun registry、runner、history、diff、workflow 和 roadmap 缺口
TP-02 dashboard artifact baseline
  TP-02.01 新增 evaluation dashboard renderer 和 shell wrapper
  TP-02.02 新增 dashboard 回归测试和 dry-run smoke
TP-03 nightly baseline
  TP-03.01 新增 evaluation-nightly wrapper，串联 runner/history/diff/dashboard
  TP-03.02 新增 GitHub scheduled workflow artifact 入口
TP-04 registry、CI 与文档
  TP-04.01 登记 dashboard smoke EvaluationRun 和 dashboard/nightly metadata
  TP-04.02 接入 quick CI、API/protocol 测试和文档
TP-05 验证与 closeout
  TP-05.01 运行 focused validation、dashboard smoke、data supply chain gate、nightly wrapper
  TP-05.02 回填任务包并生成 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 D6 评测与质量平台。
- 对齐基础设施同构：runner 负责执行，history/diff 负责回归判断，dashboard/nightly 负责可审计 artifact。
- 对齐胶水原则：复用现有 EvaluationRun registry、runner、diff policy 和 GitHub Actions artifact，不新增外部平台依赖。
- 对齐隐私边界：HTML dashboard 不渲染 stdout/stderr tail、benchmark 标准答案、报告正文或真实凭证。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 `scripts/run-evaluations.py`、`scripts/compare-evaluations.py`、`.github/workflows/*`、evaluation registry 和 D6 roadmap。 |
| TP-02 | Done | `scripts/evaluation-dashboard.py/.sh`、`scripts/evaluation-dashboard-smoke.sh` 和 `tests/regression/test_evaluation_dashboard.py` 已新增。 |
| TP-03 | Done | `scripts/evaluation-nightly.sh` 与 `.github/workflows/evaluation-nightly.yml` 已新增。 |
| TP-04 | Done | evaluation registry、quick CI、AGENTS、API 文档和 roadmap 已同步。 |
| TP-05 | Done | focused tests、dashboard smoke、data supply chain gate 和 nightly wrapper 已通过；closeout packet 待生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
