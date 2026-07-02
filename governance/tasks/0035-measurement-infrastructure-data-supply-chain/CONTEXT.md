# Repo Evidence
- `domains/fate-analysis/data-products/classics/source_manifest.tsv` 登记来源文件、bytes 与 sha256。
- `domains/fate-analysis/data-products/classics/copyright_review.tsv` 登记版权/用途/发布边界。
- `domains/fate-analysis/data-products/calendar/solar_terms/source_manifest.tsv` 登记交节时间 raw 来源 hash。
- `tools/reference-repos/vendor_sources.json` 登记 reference repo 快照、license、usageRole 和 production eligibility。
- `contracts/fate/evaluations/registry.json` 已登记 golden、benchmark 与 EvaluationRun。
- `scripts/vendor-health.sh` 已做 vendor 快照完整性和 license policy 校验。
- `scripts/local-ci.sh` 是 quick gate 编排入口。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不引入新外部资料 | 只登记与校验当前仓库已有 manifest 和 tracked files。 |
| 不做法律意见 | registry/gate 只做机器分级和待复核状态，不声明授权最终结论。 |
| 不读取 raw 私有资料 | 只校验 source manifest 中的 hash 字段和 derived fixture。 |
| 不改变算法 | gate 只读 metadata/hash，不进入 provider 计算路径。 |
| quick CI 可承受 | gate 只读小型 manifest 和 tracked file hash，运行时间毫秒级。 |

# Change Boundary
- 新增：`contracts/fate/data-supply-chain/AGENTS.md`
- 新增：`contracts/fate/data-supply-chain/registry.json`
- 新增：`contracts/fate/data-supply-chain/schemas/data-supply-chain.schema.json`
- 新增：`scripts/data-supply-chain-gate.py`
- 新增：`scripts/data-supply-chain-gate.sh`
- 新增：`tests/regression/test_data_supply_chain_gate.py`
- 修改：`domains/fate-analysis/data-products/classics/source_manifest.tsv`
- 修改：`domains/fate-analysis/data-products/classics/copyright_review.tsv`
- 修改：`scripts/local-ci.sh`
- 修改：`scripts/AGENTS.md`
- 修改：`contracts/fate/AGENTS.md`
- 修改：`domains/fate-analysis/data-products/AGENTS.md`
- 修改：`domains/fate-analysis/data-products/README.md`
- 修改：`docs/reference-materials/operations/测算基础设施 API 接入.md`
- 修改：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- 修改：`governance/tasks/INDEX.md`
- 修改：本任务目录任务文档

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| manifest 漏登记 canonical TXT | High | gate 要求所有 `classics/*.txt` 都有 source/copyright 行和 hash。 |
| review_required 被误宣称为 production | High | gate 检查 review_required 资产不能 productionEligibility=allowed。 |
| vendor 缺许可却被生产化 | High | gate 检查 production_dependency 必须 spdx 且 productionUseAllowed=true。 |
| registry hash 漂移 | Medium | required path sha256 变化会使 gate 失败，要求同步 manifest。 |
| 文档夸大法律状态 | Medium | 文档明确“不提供法律意见、不生成 SBOM/provenance”。 |

# Assumptions and Falsification
- 假设：当前 tracked manifest 足以形成本地供应链 baseline。反证：新增生产输入无法用 registry/source manifest/hash/license policy 描述。
- 假设：canonical classics 当前只能作规则索引种子。反证：后续有明确授权和人工法律复核，可升级 export/production policy。
- 假设：vendor production dependency 资格由 `vendor_sources.json` 表达。反证：构建系统引入未登记依赖或绕过 vendor manifest。

# Critical Ambiguities
- 人工法律复核、SBOM/provenance、外部 raw 授权不在本轮完成。
- `classics/*.txt` 是否可公开分发仍按 `review_required` 处理，不在本轮做最终判断。

# Debug Evidence Contract
- 调试模式: `Optional`

本任务不是 bugfix，不维护独立 `DEBUG.md`。如 gate 失败，必须记录失败 asset id、path、hash 或 policy 字段，再修 manifest 或 registry。

# Task Package Context Map
| Package | 主要上下文 |
| --- | --- |
| TP-01 | data-products manifest、vendor_sources、evaluations registry。 |
| TP-02 | data-supply-chain registry/schema、canonical classics coverage。 |
| TP-03 | gate script、pytest、quick local-ci hook。 |
| TP-04 | API 文档、roadmap、AGENTS、task closeout。 |
