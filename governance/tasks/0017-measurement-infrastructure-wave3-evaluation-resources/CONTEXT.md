# Repo Evidence
- 当前工作目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`，工作树已有 0009-0016 未提交基础设施切片；本任务必须叠加增量，不得回滚旧改动。
- 现有数据产品：
  - `domains/fate-analysis/data-products/calendar/solar_terms/golden/solar_terms_1900_2030.json`
  - `domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json`
  - `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json`
  - `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json`
  - `domains/fate-analysis/data-products/bazi/golden/statement_cases.json`
  - `domains/fate-analysis/data-products/ziwei/golden/cases.json`
  - `domains/fate-analysis/data-products/ziwei/golden/rule_depth_cases.json`
- 现有评测入口：
  - `scripts/run-mingli-bench.sh`
  - `scripts/generate-mingli-predictions.sh`
  - `domains/fate-analysis/services/fate-core/src/fate_core/evaluation/mingli_baseline.py`
- 现有测试入口：
  - `tests/regression/test_solar_terms_golden.py`
  - `tests/regression/test_bazi_golden_coverage_matrix.py`
  - `tests/regression/test_bazi_statement_golden.py`
  - `tests/regression/test_bazi_ziwei_rule_depth.py`
  - `tests/regression/test_bazi_ziwei_benchmark_hardening.py`
  - `tests/regression/test_mingli_bench_gate.py`
- 当前契约缺口：`contracts/fate/capabilities/schemas/resource.schema.json` 已列出 `Dataset` 与 `EvaluationRun`，但没有字段契约、registry 和 `/evaluations` API。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不改生产算法 | 本任务只新增契约、registry、发现 API、文档和测试。 |
| 不混入 benchmark 答案 | registry 只登记数据集和 runner，不让 production provider 读取标准答案。 |
| 不联网执行模型 | MingLi-Bench 条目标记为 offline/evaluation_only，外部模型评测继续是人工或可选流程。 |
| 不移动大数据文件 | 使用现有 data-products 与 tools/reference-repos 路径，只做资源化索引。 |
| 文档驱动 | 更新 `contracts/fate/AGENTS.md`、API 接入文档和 100% 路线图。 |
| 架构变更 | 新增 `contracts/fate/evaluations/` 时必须补局部 `AGENTS.md`。 |

# Change Boundary
允许修改：
- `contracts/fate/AGENTS.md`
- `contracts/fate/capabilities/schemas/resource.schema.json`
- `contracts/fate/evaluations/**`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `tests/regression/test_capability_protocol.py`
- `tests/regression/test_api_contracts.py`
- `docs/reference-materials/**`
- `governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources/**`

禁止修改：
- 八字、紫微、黄历、梅花 calculation usecase。
- `scripts/run-mingli-bench.sh` 与 `generate-mingli-predictions.sh` 的评测逻辑，除非测试证明资源发现必须修正。
- raw 私有资料、vendor/reference repo 内容。
- Git 历史、分支、远端。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把评测数据误写成生产依赖 | 污染真实测算链路 | registry 明确 `usageRole=evaluation_only`，API 只读发现。 |
| 对 1900-2030 golden 说法过满 | 审计口径不一致 | 文档写清“fixture/容差/样本覆盖”，不宣称外部全量证明。 |
| MingLi-Bench 路径依赖 runtime reference repo | 干净仓库不可完整跑 benchmark | 标记 `localAvailability=requires_reference_repo`，不写成必过门禁。 |
| 新 API 与文档漂移 | 开发者接入失败 | API contract、OpenAPI、metadata、文档同步测试。 |
| 工作树已有大量未提交变更 | diff 审计复杂 | 只新增 0017 范围，最终 STATUS 记录验证命令。 |

# Assumptions and Falsification
Target end state:
FateCat 的评测、golden、benchmark 与 release gate 都是可发现资源；开发者和审计人员不需要翻源码就能知道有哪些数据集、如何运行、是否本地可验证、哪些需要外部权限。

Real constraints:
现有 API 路径、已有 data-products 路径、MingLi-Bench 本地 reference repo、隐私规则、不开外部 live smoke。

Inertia constraints:
已有脚本名字、旧 benchmark 目录位置、当前任务编号和未提交切片不能决定长期终态；它们只影响本轮最小切片。

Wrong concept / wrong boundary:
把“测试文件存在”当成“基础设施评测能力存在”是错误边界；评测能力必须有资源、schema、入口和门禁口径。

Kill list:
删除“Dataset/EvaluationRun 只有 resourceTypes 枚举、没有实际契约”的半成品状态。

Proof point:
`/evaluations` 能列出 Dataset 和 EvaluationRun；schema 测试与 API 测试能验证字段、链接、用途边界和 OpenAPI。

Falsifier:
如果新增 registry 需要生产 provider 读取 benchmark 标准答案，或 API 无法区分 evaluation_only 与 production_input，则本方向错误。

Migration slice:
本轮只做只读资源发现层；后续再做评测 run 持久化、diff dashboard、CI badge 和外部 eval runner。

Rejected short-term patches:
不把 `/reports` 塞入评测字段；不在 `/metadata` 写一串静态说明替代资源 API；不把大 JSON 内容复制进 API 响应。

Existence check:
`Dataset` 与 `EvaluationRun` 已在资源模型中列出，且路线图 IMP-08 需要它们；补真实契约和 API 是把半成品闭环的最低成本。

Selected ladder rung:
项目原生能力 + 直接实现。使用现有 FastAPI 和 JSON registry，不引入数据库或新框架。

Skipped scope:
评测结果数据库、远端 CI 状态同步、可视化 dashboard、外部 LLM API benchmark、Webhook。

Ceiling / upgrade path:
当需要保存多次 run、对比 commit、展示 trend 或并发评测时，升级为持久化 EvaluationRun store 和异步 runner。

Do-not-simplify:
不能省略 usageRole、本地可验证性、外部连通待执行、隐私/版权/数据用途边界。

Minimal runnable check:
契约/API focused pytest、ruff、mypy、quick CI、task docs closeout 校验。

# Critical Ambiguities
- 是否要把每个测试文件都登记为独立 EvaluationRun：本轮不做，避免 registry 噪声；只登记代表性门禁和关键数据集。
- 是否要暴露数据集内容：本轮不做，只暴露路径、用途、命令和风险边界，避免大响应和版权/隐私误用。
- 是否要把 MingLi-Bench 设为发布必跑：本轮不做；它依赖 reference repo，本地 quick CI 不应强制。

# Debug Evidence Contract
- 调试模式: Optional

本任务不是 bugfix；若发现 API/schema 回归，必须在 `STATUS.md` 记录失败命令、失败摘要、修复点和复跑证据。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | 读取现有 data-products、scripts、tests、resource schema 和 API 元数据。 |
| TP-02 | 新增 `contracts/fate/evaluations/schemas/*.json`，扩展 resource schema。 |
| TP-03 | 新增 `contracts/fate/evaluations/registry.json`，登记关键 Dataset/EvaluationRun。 |
| TP-04 | 修改 FastAPI 只读发现入口和 metadata 链接。 |
| TP-05 | 补 tests 和 docs，确保机器契约与人类文档一致。 |
| TP-06 | 跑本地门禁并 closeout。 |
