# Planning Summary
本轮把 EvaluationRun 的机器 JSON 证据提升为人类可审计 artifact。正确终态是长期评测结果库、趋势 dashboard、告警、nightly 远端证据和评测服务。本轮只做最低可交付切片：静态 dashboard renderer、dry-run smoke、nightly wrapper、GitHub scheduled artifact 和 quick CI 门禁。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义 scope、anti-goals、隐私边界和外部验证待执行项。 |
| PLAN | Done | 本文件拆出 dashboard、nightly、registry/CI/docs、validation/closeout。 |
| BUILD | Done | scripts、workflow、registry、tests、docs 已落地。 |
| TEST | Done | focused tests、dashboard smoke、data supply chain gate、nightly wrapper 已通过。 |
| REVIEW | Done | 供应链 hash 漂移已修复，dashboard 不渲染 stdout/stderr tail。 |
| SHIP | Done | closeout packet 生成后本任务本地完成；远端 CI/nightly artifact 需 push 后执行。 |

# Simplest Path
- 不新增服务端 dashboard API；静态 HTML artifact 足够作为 D6 baseline。
- 不新增数据库；history/latest 沿用 runner 本地文件。
- 不新增外部平台；GitHub Actions 只调用本地脚本并上传 artifact。
- 不改 runner 安全模型；EvaluationRun 继续只允许 `bash scripts/*.sh` 和 `python -m pytest`。

# Split Strategy
- TP-01：确认 D6 已有 runner/history/diff，缺 dashboard/nightly。
- TP-02：新增 dashboard renderer 与 dry-run smoke。
- TP-03：新增 nightly wrapper 与 GitHub workflow。
- TP-04：把 dashboard/nightly 接入 registry、quick CI 和文档。
- TP-05：运行验证、修复供应链 hash 漂移、生成 closeout。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02 | Done |
| Wave 3 | TP-03.01, TP-03.02 | Done |
| Wave 4 | TP-04.01, TP-04.02 | Done |
| Wave 5 | TP-05.01, TP-05.02 | Done |

# Runtime Workflow Contract
- Input: EvaluationRun summary JSON and optional diff JSON.
- Runner: `bash scripts/run-evaluations.sh --all-local-required`.
- Diff: `bash scripts/compare-evaluations.sh --baseline-json <baseline> --current-json <current>`.
- Dashboard: `bash scripts/evaluation-dashboard.sh --summary-json <summary> --output-html <dashboard>`.
- Nightly: `bash scripts/evaluation-nightly.sh --output-dir <dir> --history-dir <dir>`.
- Output: summary JSON、optional diff JSON、dashboard HTML、dashboard render summary JSON。
- Privacy: no stdout/stderr tail, no benchmark answers, no report body, no real token/secret/DSN/user input。
- Failure: runner failure exits non-zero after attempting dashboard render; diff regression exits non-zero.

# Next Executable Leaves
- 无；任务完成。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 移除 `scripts/evaluation-dashboard.*`、`scripts/evaluation-dashboard-smoke.sh`、`scripts/evaluation-nightly.sh`。
- 移除 `.github/workflows/evaluation-nightly.yml`。
- 从 `scripts/local-ci.sh` 移除 dashboard smoke 和 `test_evaluation_dashboard.py`。
- 从 evaluation registry 移除 `run.evaluation_dashboard_smoke`、`dashboardCommand`、`nightlyCommand`。
- 恢复 data supply chain registry 中 evaluation registry sha 到对应内容。
- 回滚相关 docs/AGENTS/任务文档。
