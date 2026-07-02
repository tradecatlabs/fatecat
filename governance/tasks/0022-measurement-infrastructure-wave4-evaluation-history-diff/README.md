# Task Overview
- Task ID: `0022`
- Slug: `measurement-infrastructure-wave4-evaluation-history-diff`
- Objective: `把本地 EvaluationRun runner 进一步推进为可审计质量闭环：支持本地结果历史留痕、latest 指针、summary diff、diff policy 阈值判定和回归测试；不实现 dashboard/nightly/远端 CI。`
- Status: `In Progress`

## In Scope
- 扩展 `scripts/run-evaluations.py`，支持 `--record-history`、`--history-dir` 和 `history/latest.json`。
- 新增 `scripts/compare-evaluations.py` / `.sh`，比较两个 Evaluation summary JSON。
- 新增 `contracts/fate/evaluations/diff-policy.json`，定义本地 diff 阈值和隐私边界。
- 更新 Evaluation registry metadata、AGENTS、API 文档、100% 路线图和 quick CI focused tests。
- 补充 `tests/regression/test_evaluation_history_diff.py`，覆盖 history、latest、diff pass/fail 和 CLI 输出。
- 修正 `governance/tasks/INDEX.md` 中 0017-0020 的状态漂移。

## Out of Scope
- 不建立长期结果数据库。
- 不实现 dashboard、nightly 调度、远端 CI 状态同步或外部模型 eval。
- 不把评测 summary 写入 Git；默认写入 `infra/runtime/local-state/exports/`，该路径被 `.gitignore` 排除。
- 不解析或保存 benchmark 标准答案、用户输入、token、secret、DSN 或生产日志。

## Task Package Tree
```text
TP-01 评测质量闭环缺口盘点
  TP-01.01 盘点 runner、registry、roadmap 和 runtime ignore 边界
  TP-01.02 回填任务契约与任务树
TP-02 History 与 Diff 能力
  TP-02.01 扩展 runner 结果历史留痕
  TP-02.02 新增 Evaluation summary diff 工具
  TP-02.03 新增 diff-policy 并登记到 registry/AGENTS
TP-03 测试与文档
  TP-03.01 新增 history/diff 回归测试
  TP-03.02 更新 contract/API tests 与 quick CI
  TP-03.03 更新 API 文档与 100% 路线图
TP-04 治理一致性
  TP-04.01 修正任务 INDEX 状态漂移
TP-05 验证收口
  TP-05.01 执行 CLI、focused tests、ruff/format、quick CI 和 diff check
  TP-05.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 用户目标：持续按任务树推进 FateCat 成为测算基础设施。
- 本任务切片：把 0021 的 runner 继续推进为“可留痕、可比较、可按 policy 判定回归”的本地质量闭环。
- 基础设施同构依据：CI/eval 系统必须有当前结果、历史指针和回归判定，而不是只跑一次命令。
- 完成口径：本地 summary history 和 diff policy 可用；dashboard/nightly/远端 CI 作为后续切片。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确本轮只做本地 history/diff | 不把 dashboard/nightly 混入 |
| TP-02 | BUILD | 落地 history、latest、diff tool 和 policy | CLI 可生成可读 JSON |
| TP-03 | TEST/DOC | 测试和文档同步 | quick CI 覆盖 history/diff |
| TP-04 | GOVERN | 修正任务索引漂移 | INDEX 与 STATUS 一致 |
| TP-05 | SHIP | 验证并收口 | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
