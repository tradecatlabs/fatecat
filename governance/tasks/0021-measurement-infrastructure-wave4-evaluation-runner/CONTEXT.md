# Repo Evidence
- `contracts/fate/evaluations/registry.json` 已登记 `Dataset` 与 `EvaluationRun`，其中 `run.local_ci_quick` 与 `run.solar_terms_golden` 为 `releaseRequired=true` 且 `tracked_in_repo`。
- `scripts/local-ci.sh`、`scripts/run-mingli-bench.sh`、`scripts/generate-mingli-predictions.sh` 是现有评测/门禁入口。
- `tests/regression/test_solar_terms_golden.py`、`test_bazi_golden_coverage_matrix.py`、`test_bazi_ziwei_rule_depth.py`、`test_bazi_ziwei_benchmark_hardening.py` 是当前 golden/规则深度回归入口。
- `/evaluations` API 当前只读发现，不执行任务；这符合安全边界，但还缺少本地执行闭环。

# Constraints Matrix
| 约束 | 决策 |
| --- | --- |
| 安全 | runner 不使用 `shell=True`，只允许 `bash scripts/*.sh` 与 `python -m pytest`。 |
| 隐私 | summary 只写命令尾部输出和 exit code，不写用户输入、token、secret、DSN 或 benchmark 标准答案。 |
| 可复现 | 默认选择本地必跑集合；可按 `--run-id` 精确执行。 |
| 外部依赖 | `requires_reference_repo` 默认跳过，显式 `--allow-reference-repo` 才能执行。 |
| 文档口径 | 只声明本地最小集 runner 可用，不声明 dashboard、nightly、外部模型 eval 已完成。 |

# Change Boundary
- 允许修改：`scripts/`、`contracts/fate/evaluations/`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0021-*`。
- 不允许修改：八字/紫微领域算法、报告正文生成逻辑、外部服务凭证、生产部署配置。

# Risk Matrix
| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| registry command 被滥用为任意 shell | 高 | shlex 拆分、白名单、路径约束、测试覆盖。 |
| API 发现被误解为远端执行 | 中 | 文档明确 `/evaluations` 不启动任务。 |
| 可选 benchmark 被当成 release gate | 中 | `releaseRequired=false` 且默认跳过 `requires_reference_repo`。 |
| summary 输出过大或泄露敏感信息 | 中 | 仅截断 stdout/stderr tail，评测命令本身不应输出 secret。 |

# Assumptions and Falsification
- 假设：本地 `.venv/bin/python` 已由项目 bootstrap 管理。反证：runner wrapper 找不到 `.venv/bin/python` 时失败并提示 bootstrap。
- 假设：本地必跑集合只包含无外部凭证命令。反证：registry 中 `releaseRequired=true` 资源若需要外部连通，则 schema/contract tests 应失败或需人工复核。
- 假设：当前切片不需要结果历史数据库。反证：如果审计要求趋势对比或跨 commit diff，则进入后续 EvaluationRun persistence 任务。

# Critical Ambiguities
- 扩展评测的执行频率、历史保留期和 dashboard 形态未定；本任务不实现。
- 外部模型评测的 token、账号、成本和数据合规边界未定；本任务不执行。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix，不维护 `DEBUG.md`。
- 若 runner 执行失败，必须保留失败命令、exit code、stderrTail 和复现命令。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | registry 与现有评测脚本事实盘点 |
| TP-02 | runner 实现和协议登记 |
| TP-03 | tests 与 quick CI 接入 |
| TP-04 | docs/roadmap 口径同步 |
| TP-05 | 真实命令证据、closeout 与任务树验证 |
