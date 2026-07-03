# Task Overview
- Task ID: `0082`
- Slug: `measurement-infrastructure-otel-backend-slo-staged-gate`
- Objective: `把 0064 的 OTel collector/SLO dry-run contract baseline 推进为可审计的外部 backend/SLO staged evidence gate：默认输出 外部连通验证待执行，只有 operator 提供完整脱敏 proof refs 时才允许通过 live evidence schema；不得连接真实 backend，不得保存生产 trace、metrics、logs、dashboard URL、token、secret 或用户数据。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/observability/otel-backend-slo-evidence-contract.json`。
- 新增 `scripts/otel-backend-slo-gate.py/.sh`。
- 更新 observability registry/schema、API 文档、roadmap、local-ci artifact 和 regression tests。
- 建立反伪造负例：localhost backend、placeholder proof、raw URL、token/secret、生产指标快照、缺少 error budget 或 alert proof。

## Out of Scope
- 不启动真实 OpenTelemetry Collector。
- 不连接 trace backend、metrics backend、Grafana、Alertmanager、PagerDuty、云监控或 SIEM。
- 不声明真实 production SLO、error budget、alert live 或 incident drill 已完成。
- 不保存真实 URL、token、secret、生产 trace、metrics snapshot、日志正文、报告正文或用户输入。

## Task Package Tree
```text
TP-01 SPEC: 复核 0064 与 0081 后的 observability 缺口
  TP-01.01 读取 registry、SLO evidence contract、roadmap 和 local-ci
  TP-01.02 定义 staged gate 的 pending/live/non-claim 边界
TP-02 PLAN: 设计 OTel backend/SLO evidence contract
  TP-02.01 定义 live evidence schema 与 proof ref 白名单
  TP-02.02 定义反伪造负例和敏感值防护
TP-03 BUILD: 实现 gate 与接线
  TP-03.01 新增 Python gate 与 shell wrapper
  TP-03.02 更新 observability registry/schema、local-ci 和文档
TP-04 TEST: 回归和门禁
  TP-04.01 新增 focused regression tests
  TP-04.02 运行 syntax、pytest、ruff、secret scan、quick CI 和任务校验
TP-05 REVIEW/SHIP: 收口
  TP-05.01 回填 closeout 与剩余外部验证项
  TP-05.02 明确 git/CI 交付证据外置边界
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| 100% infra 要 observability live evidence 可复核 | 新增 staged evidence contract 和 gate |
| 不伪造外部 live | 默认 pending；live evidence 必须字段完整且 proof refs 脱敏 |
| 不泄露敏感信息 | gate 拒绝 token/secret/raw URL/生产 payload 等片段 |
| 不污染 0064 dry-run 边界 | 新 gate 独立存在，0064 仍只证明 collector/SLO dry-run contract |
| 任务树推进 | 本任务按 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 执行 |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 缺口来自 repo evidence，不靠猜测 |
| TP-01.01 | 复核 0064/roadmap | Done | observability registry、0064 gate、roadmap/local-ci 已读取 |
| TP-01.02 | 定义边界 | Done | pending/live/non-claim 明确 |
| TP-02 | PLAN | Done | contract、proof refs、negative cases 明确 |
| TP-02.01 | live schema | Done | required live fields 和 proof ref 白名单定义 |
| TP-02.02 | 反伪造 | Done | fake/local/sensitive/overclaim evidence 会失败 |
| TP-03 | BUILD | Done | gate、contract、registry、local-ci、docs 接线完成 |
| TP-03.01 | gate 脚本 | Done | wrapper + Python 可执行 |
| TP-03.02 | registry/docs 接线 | Done | observability schema、local-ci artifact、AGENTS 和 docs 更新 |
| TP-04 | TEST | Done | regression、focused checks、secret scan 和 quick CI 完成 |
| TP-04.01 | regression tests | Done | 覆盖 pending、live fixture、negative cases |
| TP-04.02 | validation gates | Done | syntax、pytest、ruff、format、secret scan、quick CI 和 task validators 完成 |
| TP-05 | REVIEW/SHIP | Done | closeout 完成；git/CI 由外层交付流记录 |
| TP-05.01 | closeout | Done | 文档无 overclaim，外部验证项保留 |
| TP-05.02 | git/CI boundary | Done | 任务包不预声明 commit/push/remote CI；真实证据由外层交付汇报记录 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
