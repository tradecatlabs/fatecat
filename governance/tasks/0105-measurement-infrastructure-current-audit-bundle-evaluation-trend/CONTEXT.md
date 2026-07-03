# Repo Evidence
- 0104 已新增 `contracts/fate/evaluations/trend-policy.json`、`scripts/evaluation-trend-gate.py`、`scripts/evaluation-trend-gate-smoke.sh` 和 local-ci wiring。
- `scripts/local-ci.sh` 会生成 `evaluation-trend-gate-smoke/trend-gate.json`，并在 summary artifacts 中记录 `evaluationTrendGateSmoke` 路径。
- `scripts/current-audit-bundle.py` 现有 `LOCAL_CI_GATE_ARTIFACTS` 只覆盖 `evidence-coverage-trend-gate.json`。
- `tests/regression/test_current_audit_bundle.py` 只断言 `evidence.evidence_coverage_trend_gate`，未覆盖 `evidence.evaluation_trend_gate`。
- `governance/tasks/0104.../STATUS.md` 已为 Done，但 `governance/tasks/INDEX.md` 当前需要同步为 Done。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不扩大审计包语义 | 仍使用 current audit bundle local-ci gate artifact 摘要机制。 |
| 不伪造外部证据 | 0105 只聚合本地 local-ci artifact，不声称远端 CI 或生产 live。 |
| 不泄露敏感信息 | 只输出 `summaryCount`、`latestStatus`、`consecutiveFailedSummaries` 和 digest。 |
| 不重写趋势门禁 | 复用 0104 trend gate 输出，不复制判定逻辑。 |
| 任务文档必须可校验 | 任务包 closeout 前跑 `validate_task_docs.py --phase closeout`。 |

# Change Boundary
Allowed paths:
- `scripts/current-audit-bundle.py`
- `tests/regression/test_current_audit_bundle.py`
- `contracts/fate/audit/current-bundle.json`
- `contracts/fate/audit/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/INDEX.md`
- `governance/tasks/0105-measurement-infrastructure-current-audit-bundle-evaluation-trend/*`

Not allowed:
- 修改 production provider 算法。
- 修改真实凭证、`.env` 或生产连接配置。
- 把外部 live/pending 项写成 passed。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 审计包漏掉 0104 trend gate | 第三方审计看不到最新质量趋势门禁 | 添加 `evidence.evaluation_trend_gate` 并补 regression。 |
| 输出复制 trend history 过多内容 | 可能泄露日志或评测数据 | 只使用 detailFields 和 digest，不内联 history。 |
| 任务索引状态漂移 | 审计时任务状态不可信 | 同步 0104 INDEX 为 Done，并校验 0104 closeout。 |
| 将本地 artifact 误解成外部 live | 交付结论失真 | roadmap 和 contract 保留 non-claim/pending。 |

# Assumptions and Falsification
- Assumption: `evaluation-trend-gate-smoke/trend-gate.json` 是 current audit bundle 可以消费的 summary-only evidence artifact。
- Falsifier: current audit bundle 生成后 evidence index 不含 `evidence.evaluation_trend_gate`，或该 item status 不是 `pass`。
- Assumption: `trendFindings=[]` 足以证明本地趋势门禁未触发 policy violation。
- Falsifier: artifact `status=passed` 但 `trendFindings` 非空仍被接受。

# Critical Ambiguities
- 是否把远端 CI evaluation artifact 也纳入 0105：不纳入；当前 GitHub Actions 对最新 commit 还无可见 run，且远端 artifact 是后续任务。
- 是否把 evaluation dashboard smoke 也作为 evidence item：不纳入；0105 只补 0104 trend gate 审计可追踪性。
- 是否要求 `--require-current-release`：不要求；本地 current audit bundle 仍可生成 blocked bundle。

# Debug Evidence Contract
- 调试模式: Optional

本任务是审计证据聚合增强，不是已知 bugfix。若 regression 失败，需要在 `STATUS.md` 记录最小失败证据、根因和回归命令；无需单独创建 `DEBUG.md`。

# Task Package Context Map
| Context | Path |
| --- | --- |
| Current audit bundle generator | `scripts/current-audit-bundle.py` |
| Current audit bundle tests | `tests/regression/test_current_audit_bundle.py` |
| Audit contract | `contracts/fate/audit/current-bundle.json` |
| Evaluation trend gate output | `evaluation-trend-gate-smoke/trend-gate.json` under local-ci output dir |
| 100% infra roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
