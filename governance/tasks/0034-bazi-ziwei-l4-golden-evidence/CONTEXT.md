# Repo Evidence
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 将八字/紫微 L4 样板列为 `MI-05`。
- `domains/fate-analysis/data-products/bazi/golden/coverage_matrix_cases.json` 当前有 300 个匿名北京/测试矩阵样本。
- `domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json` 当前有 8 个八字规则深度样本。
- `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` 当前有 5 个八字断语 golden 样本。
- `domains/fate-analysis/data-products/ziwei/golden/cases.json` 当前有 1 个紫微基础 golden 样本。
- `domains/fate-analysis/data-products/ziwei/golden/rule_depth_cases.json` 当前有 8 个紫微规则深度样本。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py` 是 capability provider 执行真相源。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 暴露 Markdown API 和 `policyGate` / `snapshotGate`。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不能伪造专业能力 100% | summary 和文档明确本轮只做本地 L4 baseline。 |
| 不能泄露真实地区 | fixture 和 Markdown payload 固定北京/测试样本。 |
| quick CI 不能过重 | smoke 支持 `--profile quick`，只执行代表样本；`full` 留给发布前加严。 |
| 不旁路统一能力协议 | bazi/ziwei 计算走 `CapabilityExecutor`。 |
| 不让前端拼命理规则 | Markdown profile gate 通过后端 API 验证。 |

# Change Boundary
- 新增：`scripts/bazi-ziwei-l4-golden-smoke.py`
- 新增：`scripts/bazi-ziwei-l4-golden-smoke.sh`
- 新增：`tests/regression/test_bazi_ziwei_l4_golden_smoke.py`
- 修改：`scripts/local-ci.sh`
- 修改：`scripts/AGENTS.md`
- 修改：`docs/reference-materials/operations/测算基础设施 API 接入.md`
- 修改：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- 修改：`docs/reference-materials/reference/八字紫微能力基线与缺口矩阵.md`
- 修改：`docs/reference-materials/roadmap/八字紫微标杆对标路线图.md`
- 修改：`governance/tasks/INDEX.md`
- 修改：本任务目录任务文档

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| smoke 太慢拖垮 quick CI | Medium | `quick` 只跑代表样本，`full` 手动执行。 |
| 证据字段存在但规则断链 | High | 检查 required rule IDs、组合主题、冲突解释和反证字段。 |
| Markdown API payload 漂移 | Medium | 通过 TestClient 真实调用 `/api/v1/report/markdown`。 |
| 文档夸大完成度 | High | 明确“不锁全文断语、不新增真实命例、不声明专业能力 100%”。 |

# Assumptions and Falsification
- 假设：现有 fixture 足以作为本地 L4 baseline 的代表样本。反证：新增规则或字段无法被 quick/full smoke 检出，需要扩 fixture。
- 假设：`CapabilityExecutor` 是 production capability 执行的统一入口。反证：任何生产入口绕过 executor，则本 smoke 不足以证明同源。
- 假设：Markdown API 的 `policyGate` / `snapshotGate` 是报告交付最低门禁。反证：报告 profile 新增后未进入 snapshot gate。

# Critical Ambiguities
- “专业能力 100%”仍依赖真实匿名命例 corpus、人工命师复核、全文断语 golden 和长期评测平台；本轮不解决。
- “外部 golden”仍需后续数据供应链和版权/来源复核；本轮只复用已入库 fixture。

# Debug Evidence Contract
- 调试模式: `Optional`

本任务不是 bugfix，不维护独立 `DEBUG.md`。如 smoke 失败，必须记录失败命令、fixture id、字段差异和最小复现输入，再修脚本或业务代码。

# Task Package Context Map
| Package | 主要上下文 |
| --- | --- |
| TP-01 | MI-05 roadmap、现有 bazi/ziwei golden fixtures、Markdown gate。 |
| TP-02 | `CapabilityExecutor`、FastAPI TestClient、summary JSON。 |
| TP-03 | pytest、ruff、format、quick local-ci。 |
| TP-04 | API 文档、roadmap、专项基线、AGENTS、任务 closeout。 |
