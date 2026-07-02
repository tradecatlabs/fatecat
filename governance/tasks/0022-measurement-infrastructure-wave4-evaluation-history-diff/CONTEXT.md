# Repo Evidence
- `scripts/run-evaluations.py` 已能执行 registry 中的 EvaluationRun 并输出 summary JSON。
- `contracts/fate/evaluations/registry.json` 已登记 runner metadata，但缺少 diff policy 与 history 口径。
- `infra/runtime/local-state/exports/` 已在 `.gitignore` 中排除，适合作为本地运行态 summary/history 输出位置。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 仍标记 eval 的扩展集、nightly、跨 commit diff 和 dashboard 未完成。
- `governance/tasks/INDEX.md` 中 0017-0020 状态滞后于对应 `STATUS.md`。

# Constraints Matrix
| 约束 | 决策 |
| --- | --- |
| 运行态不入 Git | history 默认写 `infra/runtime/local-state/exports/evaluations/history/`。 |
| 不扩大范围 | 本轮只做本地 history/latest 和 summary diff，不做 dashboard/nightly。 |
| 隐私 | diff 只比较 runId、status、exitCode 和 summary，不解析用户输入或标准答案。 |
| 失败判定 | policy 阈值默认全部为 0：新增失败、缺失 run、失败命令均阻断。 |
| 可复现 | CLI 和测试均使用 JSON 文件，可在本地重复执行。 |

# Change Boundary
- 允许修改：`scripts/run-evaluations.py`、新增 `scripts/compare-evaluations.*`、`contracts/fate/evaluations/`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/`。
- 不允许修改：八字/紫微算法、报告生成、外部 live 配置、生产数据库、第三方 benchmark 标准答案。

# Risk Matrix
| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| history 误提交 | 中 | 默认输出到已忽略的 local-state exports。 |
| diff 过度解读 stdout | 中 | diff 不解析 stdout 内容，只看状态和 exitCode。 |
| policy 被误认为远端 CI 证据 | 中 | 文档明确只覆盖本地 summary。 |
| INDEX 与任务目录冲突 | 低 | 同步 0017-0020 为 Done，并跑任务树 validator。 |

# Assumptions and Falsification
- 假设：本地 history/latest 足以作为下一步 dashboard/nightly 的输入。反证：若后续需要趋势查询、聚合和 retention，就进入长期结果数据库任务。
- 假设：0 容忍失败适合当前 required local gate。反证：若引入 flaky 或允许性能阈值，需要扩展 `diff-policy.json`。

# Critical Ambiguities
- dashboard 形态、nightly 调度平台和远端 CI 同步方式未定；本任务不实现。
- 跨 commit baseline 的来源未定；本任务只提供两个 summary JSON 的比较能力。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix，不维护 `DEBUG.md`。
- 若 diff 失败，必须保留 baseline/current/diff JSON 路径和 policy violation 摘要。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | runner 与 roadmap 缺口 |
| TP-02 | history/diff/policy 实现 |
| TP-03 | tests/docs/quick CI |
| TP-04 | INDEX 状态一致性 |
| TP-05 | 本地门禁与 closeout |
