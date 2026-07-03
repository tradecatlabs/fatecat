# Repo Evidence
- `scripts/run-evaluations.py` 已支持 `--record-history`、history summary 和 `latest.json`。
- `scripts/compare-evaluations.py` 已支持两个 summary 的 diff，但不做长期窗口趋势判断。
- `scripts/evaluation-dashboard.py` / `scripts/evaluation-nightly.sh` 已提供 dashboard/nightly baseline。
- `contracts/fate/evaluations/registry.json` 已登记 Dataset/EvaluationRun 和 runner/diff/dashboard/nightly metadata。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 在 Post-0098 里仍把 EvaluationRun 的缺口写成 “current commit nightly artifact、外部 benchmark aggregate、趋势库”。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造外部生产证据 | Trend gate 只读本地 history summary；生产 live、外部 benchmark、远端 CI 仍保持 pending。 |
| 不能泄露敏感信息 | Trend report 只保留 status/runId/exitCode/generatedAt/gitCommit，不复制 tails、答案、报告正文或凭证。 |
| 必须复用现有模式 | 复用 `run-evaluations` history/latest、`local-ci.sh` artifact summary、registry metadata 和 regression tests。 |
| 不扩大业务算法面 | 不触碰 production provider 算法或报告生成器。 |
| 任务包必须可校验 | README/CONTEXT/PLAN/TODO/STATUS/ACCEPTANCE/ACCEPTANCE_CHECKLIST 均回填并跑 validator。 |

# Change Boundary
Allowed paths:
- `contracts/fate/evaluations/*`
- `contracts/fate/data-supply-chain/registry.json`
- `scripts/evaluation-trend-gate*`
- `scripts/local-ci.sh`
- `scripts/AGENTS.md`
- `tests/regression/test_evaluation_trend_gate.py`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0104-measurement-infrastructure-evaluation-trend-store/*`
- `governance/tasks/INDEX.md`

Not allowed:
- 改生产 provider 算法。
- 改真实 secret、`.env` 或生产连接配置。
- 把外部 pending 写成 passed。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Trend gate 复制命令输出 tail | 泄露测试输出、标准答案或报告正文 | Regression assert serialized report 不包含 synthetic tail marker。 |
| Trend gate 只证明自洽，误写成生产通过 | 审计结论失真 | `productionBoundary` 明确限制，路线图保留外部 pending。 |
| local-ci artifact 漏接 | 门禁不能长期执行 | Focused test 检查 `evaluation-trend-gate-smoke` 已进入 local-ci。 |
| registry metadata 断链 | Agent/API 发现层看不到趋势策略 | Regression 检查 `trendPolicy` 与 `trendCommand`。 |

# Assumptions and Falsification
- Assumption: EvaluationRun summary JSON 的 `summary.status`、`runs[*].status`、`commands[*].exitCode` 足够支持本地趋势门禁。
- Falsifier: 历史 summary 中没有 releaseRequired run 或字段缺失导致 trend gate 无法判断；此时脚本应失败或输出 finding，而不是通过。
- Assumption: latest summary 必须通过，且 required run 集合不能从历史中消失。
- Falsifier: 最新 summary 失败、失败命令非零、或 required run 缺失时 trend gate 仍返回 passed。

# Critical Ambiguities
- 外部 benchmark 和远端 CI 是否纳入趋势库：本切片不纳入；后续必须通过真实 artifact 或 CI URL 接入。
- 趋势窗口大小：本切片固定 policy `defaultWindow=10`，后续可按证据量调整。
- 失败阈值：本切片对 releaseRequired 本地趋势采用零容忍；非必跑/外部 optional benchmark 后续可另建 policy。

# Debug Evidence Contract
- 调试模式: Optional

本任务是新增基础设施门禁，不是已知 bugfix。若 focused regression 或 smoke 失败，需要在 `STATUS.md` 记录根因、最小复现和回归命令；无需创建单独 `DEBUG.md`，除非出现重复失败或 CI-only 故障。

# Task Package Context Map
| Context | Path |
| --- | --- |
| Evaluation registry | `contracts/fate/evaluations/registry.json` |
| Evaluation diff policy | `contracts/fate/evaluations/diff-policy.json` |
| Evaluation runner | `scripts/run-evaluations.py` |
| Evaluation dashboard/nightly | `scripts/evaluation-dashboard.py`, `scripts/evaluation-nightly.sh` |
| Local CI truth | `scripts/local-ci.sh` |
| 100% infra plan | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
