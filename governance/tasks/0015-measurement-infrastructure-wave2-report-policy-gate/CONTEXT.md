# Repo Evidence
- `git status --short --branch` 显示当前分支 `main...origin/main`，0009-0014 相关文件仍未提交。
- `contracts/fate/capabilities/schemas/report.schema.json` 当前 invariants 写有 `完整 report snapshot gate 和 forbidden claims scanner 属后续发布门禁`。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已有 `_capability_report_payload(result)`，但只输出 `sections/evidenceRefs/risk/metadata`。
- `CapabilityExecutor._risk_payload()` 已从 capability registry 输出 `forbiddenClaims`，但执行结果尚未被 gate 消费。
- `tests/regression/test_api_contracts.py` 已覆盖 capability response 的 `report` envelope。
- `tests/regression/test_capability_protocol.py` 已覆盖 report/output/evidence/provider schema 基线。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 当前分支和工作树已有 0009-0014 未提交改动 | 继续叠加最小切片，不重置、不提交、不推送。 |
| 不能把风险词清单扫描成自身违规 | `policyGate` 只扫描生成报告摘要字段，显式排除 `risk.forbiddenClaims`。 |
| 不能改变命理算法 | 只改 capability helper、report envelope、schema、tests/docs。 |
| 不能宣称完整生产合规 | 本轮只做最小 forbidden claims gate；完整 snapshot、人工审核、线上策略仍是后续项。 |
| 文档驱动 | 更新 schema、API 文档、路线图和任务文档。 |

# Change Boundary
- May change:
  - `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/`
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py`
  - `contracts/fate/capabilities/schemas/report.schema.json`
  - `tests/regression/test_capability_protocol.py`
  - `tests/regression/test_api_contracts.py`
  - `docs/reference-materials/operations/测算基础设施 API 接入.md`
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
  - `governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate/`
- Must not change:
  - 八字/紫微/黄历/梅花计算核心行为。
  - 数据库 schema、记录写入、Bot live 行为。
  - 其他任务目录的历史证据，除非任务树 validator 需要更新 `INDEX.md`。

# Risk Matrix
| Risk | Level | Mitigation |
| --- | --- | --- |
| 误扫 `forbiddenClaims` 清单导致所有报告 fail | medium | `excludedFields` 明确排除清单字段，测试覆盖。 |
| 只扫描摘要而被误认为完整内容审查 | medium | `scope`/`contentCoverage` 明确写入 policyGate 和文档。 |
| API contract 变更破坏调用方 | medium | 只新增 `report.policyGate`，旧字段不删除。 |
| 过度设计成完整合规模块 | medium | 本轮不新增数据库、不新增远程策略服务、不做大规模规则引擎。 |

# Assumptions and Falsification
- Assumption: 当前 capability registry 的 `forbiddenClaims` 足以作为最小门禁输入。
- Assumption: `report.sections` 是 capability API 当前最稳定的生成报告摘要位置。
- Falsifier: 如果测试发现实际用户可见 Markdown 不经过 `policyGate`，则本轮不能宣称完整报告政策门禁，只能宣称 capability report envelope gate。
- Falsifier: 如果 `policyGate` 对正常 bazi/ziwei/almanac/meihua 响应误报，则必须缩小扫描范围或修复匹配规则。

# Critical Ambiguities
- 完整 Markdown snapshot gate 仍未定义，本任务不解决。
- 外部生产策略审核、人工审核、线上可观测告警不在本轮验证范围。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务是新增 infrastructure gate，不是已复现 bugfix；若出现回归失败，失败命令和根因写入 STATUS。

# Future-Optimal Contract
- Target end state: 所有测算报告都有统一 `Report` resource，生成内容、证据、风险、policy、snapshot、provider 可审计。
- Real constraints: 现有 capability API 已对外暴露；旧 `data/evidence/risk/metadata` 字段必须保持兼容。
- Inertia constraints: 0014 里 `metadata.snapshotGate` 的后续提示不能长期替代真实 gate。
- Wrong concept / wrong boundary: 把“有免责声明”误认为“有报告政策门禁”。
- Kill list: 删除 schema 中“forbidden claims scanner 属后续发布门禁”的过期表达。
- Proof point: API response 中存在 `report.policyGate.status=pass`，scanner 单测能对违规文本返回 fail。
- Falsifier: policy gate 只存在文档，没有被 capability API 实际调用。
- Migration slice: 本轮先接 capability report envelope；后续再接 Markdown job snapshot 和人工 release gate。
- Rejected short-term patches: 不用硬编码空 `policyGate`；不只更新文档；不在前端做字符串过滤。

# Ponytail Contract
- Existence check: 测算基础设施必须能机器检查高风险断语，`policyGate` 是 Report resource 的最小可审计对象。
- Selected ladder rung: 项目原生直接实现；不引入新依赖，使用简单字符串匹配作为第一阶段。
- Skipped scope: NLP 分类器、远程 policy service、完整 Markdown snapshot、人工审核后台。
- Ceiling / upgrade path: 当报告 Markdown、API JSON、Bot 消息都需要统一审查时，升级为中央 ReportPolicyExecutor。
- Do-not-simplify: 不得扫描风险清单自身；不得删除 disclaimer 和 forbiddenClaims 原始字段。
- Minimal runnable check: scanner fail/pass 单测 + capability API response 回归。
- Complexity review owner: `auto-review` future pass；本轮先以回归测试和 schema gate 自审。

# Document-Driven Contract
- Operating model update: not needed；项目定位未变。
- Toolchain model update: not needed；没有新增命令或外部工具。
- Process update: not needed；仍走现有 quick CI 与 governance validators。
- Source-of-truth updates: updated；`report.schema.json`、API 文档、路线图和任务文档同步。
- Local README/AGENTS impact: updated if new module is added under `fate_core/capabilities/AGENTS.md`。
- Contract/catalog/schema impact: updated；`report.schema.json` 增加 `policyGate`。
- ADR/Gate/module-context impact: not needed；本轮是已有 Report resource 的子字段落地。
- Documentation exemption reason: none。
- Validation evidence: STATUS 记录真实命令输出。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | 当前 schema 明确 scanner 后续，需改成已实现最小门禁。 |
| TP-02 | 执行路径在 `main.py::_capability_report_payload`，风险清单来自 `CapabilityExecutor`。 |
| TP-03 | 回归测试必须同时覆盖 schema、helper fail case、API pass case。 |
| TP-04 | local-ci/governance/task validators 是收口证据。 |
