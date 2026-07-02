# Context

## Current Facts

- 当前 0061 后续路线图把 0066 定义为 `core quality corpus expansion`。
- 八字已有 `coverage_matrix_cases.json` 300 个匿名样本、`rule_depth_cases.json` 8 个匿名样本、`statement_cases.json` 5 个轻量样本。
- 紫微已有 `rule_depth_cases.json` 8 个匿名样本，但基础 `cases.json` 原本只有 1 个样本。
- `scripts/bazi-ziwei-l4-golden-smoke.py` 已能执行八字/紫微代表样本和 Markdown profile gate。
- `contracts/fate/evaluations/registry.json` 是 Dataset/EvaluationRun 发现层真相源。

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不使用真实用户隐私样例 | 所有新增样本使用北京、测试样本、固定经纬度和合成日期。 |
| 不把 fixture 变成生产输入 | manifest 明确 `usageRole=evaluation_only`，gate 只做测试和发布门禁。 |
| 不夸大准确率 | 文档和 policy 明确不证明专家准确率或真实命例库覆盖。 |
| 不锁完整断语正文 | report diff policy 锁结构、门禁和隐私边界，不逐字锁自然语言段落。 |
| 复用现有能力 | 复用已有 CapabilityExecutor、L4 smoke、evaluation registry、local-ci。 |
| Change boundary | 只改 evaluation contracts、data-products golden、gate scripts、tests、local-ci、AGENTS/README、roadmap 和 0066 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。0066 是 contract/gate 新增，不是已复现 bug；若 gate/test 失败再补 DEBUG 证据。 |

## Change Boundary

- 允许修改：`contracts/fate/evaluations/`、`domains/fate-analysis/data-products/*/golden/`、`scripts/core-quality-corpus-gate.*`、`scripts/local-ci.sh`、`tests/regression/`、相关 AGENTS/README/roadmap 和 0066 任务文档。
- 禁止修改：production provider 算法、真实用户数据、真实 `.env`、公网 live smoke、外部专家评测结论。
- 本轮只落核心质量语料 contract/gate baseline；专业准确率、人审 benchmark 和外部 live 证据留到后续任务。

## Repo Evidence

- `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json`
- `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
- `domains/fate-analysis/data-products/bazi/golden/statement_cases.json`
- `domains/fate-analysis/data-products/ziwei/golden/cases.json`
- `domains/fate-analysis/data-products/ziwei/golden/rule_depth_cases.json`
- `contracts/fate/evaluations/registry.json`
- `scripts/bazi-ziwei-l4-golden-smoke.py`
- `scripts/local-ci.sh`

## Critical Ambiguities

- “full report diff policy” 不能理解为全文断语 snapshot；本轮定义为结构、门禁、体系隔离和隐私边界策略。
- “sample expansion” 不能理解为真实命例库；本轮只扩匿名工程回归样本。

## Debug Evidence Contract

- 调试模式: Optional
- 0066 是 contract/gate 新增，不是已复现 bug；如果 JSON、gate、pytest 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

## Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 把工程 fixture 当作真实命例库 | manifest 和 docs 明确 `evaluation_only` 与 limitations。 |
| 紫微样本仍过少 | 本轮提高基础 cases 到 4 个；后续继续扩展专家/benchmark 样本。 |
| 报告 diff 误锁自然语言 | policy 只锁结构、门禁和隐私，不逐字锁完整断语。 |
| quick CI 漏跑新 gate | `local-ci.sh --profile quick` 生成 `core-quality-corpus-gate.json` artifact。 |
| registry 与脚本事实漂移 | 新 Dataset/EvaluationRun 与 runner/API 回归测试覆盖。 |

## Assumptions and Falsification

- 假设：核心质量语料首先应该服务可复现工程门禁，而不是一次性追求专家评测全量覆盖。
- 证伪条件：如果 gate 允许真实非北京地区、真实姓名、生产路径或 production provider 读取 fixture，本任务失败。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 现有 bazi/ziwei golden fixture、evaluation registry、local-ci、L4 smoke。 |
| TP-02.01 | `contracts/fate/evaluations/core-quality-corpus.json` 是核心质量语料清单。 |
| TP-02.02 | `contracts/fate/evaluations/report-diff-policy.json` 是报告结构 diff 策略。 |
| TP-03.01 | `domains/fate-analysis/data-products/ziwei/golden/cases.json` 是紫微基础样本入口。 |
| TP-03.02 | `scripts/core-quality-corpus-gate.py` 复用本仓 gate 脚本风格。 |
| TP-03.03 | `scripts/local-ci.sh` 和 evaluation registry 是发布门禁入口。 |
| TP-04.01 | AGENTS/README/roadmap/tests 是文档和发现层同步点。 |
| TP-04.02 | quick local-ci、commit/push、remote CI 是 closeout 证据。 |
