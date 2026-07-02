# Repo Evidence
- `contracts/fate/capabilities/schemas/evidence.schema.json` 目前只声明 common fields，没有 evidenceRefs 结构。
- `contracts/fate/capabilities/schemas/output.schema.json` 目前 required fields 不含 report。
- `resource.schema.json` 已声明 `Report` resource type，但未定义 reportResourceFields。
- `main.py` capability 执行响应目前返回 `capabilityId/status/reportProfile/data/evidence/risk/metadata`，没有统一 `report` resource envelope。
- `/reports` 当前只列 profile 和 job endpoints。
- IMP-05 明确需要 report profile schema、Markdown section schema、JSON report schema、evidence reference schema。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不改报告生成器 | 只加 API envelope，不重排 Markdown。 |
| 不改算法 data | `report.sections` 只引用 top-level data keys，不复制或改写结果。 |
| evidence 结构不统一 | 先从 `analysisEvidence.items.*.ruleIds` 提取 best-effort refs。 |
| 多端未来复用 | envelope 使用 `resourceType=Report` 和 schema refs。 |

# Change Boundary
- 可改：schemas、`main.py` response helper、API tests、API docs、100% 计划、0014 任务文档。
- 不改：report markdown renderer、provider registry、算法 usecases、job store。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| report envelope 过度承诺完整 section schema | 审计误判 | schema 标明当前是 resource envelope，完整 snapshot gate 后续做。 |
| evidenceRefs 抽取不完整 | 证据链误读 | 标明 best-effort refs，原始 evidence 仍完整返回。 |
| API 响应体变大 | 低 | envelope 只放摘要和引用，不复制完整 data。 |

# Assumptions and Falsification
- Target end state: 所有 capability 执行结果都能同时被人类报告层和机器审计层消费，Report 资源负责表达 profile、format、section 和 evidence refs。
- Real constraints: 现有 API response 不能破坏；旧客户端继续读 `data/evidence`。
- Inertia constraints: 不能因为已有 `reportProfile` 字段就放弃独立 report resource。
- Wrong concept / wrong boundary: report 只是一个字符串 profile，而不是可审计交付资源。
- Kill list: capability 执行响应缺少 `report` envelope。
- Proof point: API tests 证明 production capability response 包含 `report.resourceType=Report`、sections 和 evidenceRefs。
- Falsifier: 如果新增 envelope 改变 `data/evidence` 原始结构，或默认 Markdown 混入非 bazi，本切片失败。
- Migration slice: 先做 JSON execution envelope；后续再做 Markdown section snapshot 和 forbidden claims scanner。
- Rejected short-term patches: 不在文档里声明 report snapshot 已完成；不硬编码某一个体系的章节结构。

# Critical Ambiguities
- 无阻塞歧义。完整 report section schema 与 snapshot gate 后续单独实现。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；最小复现命令为 `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k report`.

# Task Package Context Map
| Node | Required Context |
| --- | --- |
| TP-01.01 | `resource.schema.json`、IMP-05 |
| TP-01.02 | `output.schema.json`、`evidence.schema.json` |
| TP-02.01 | capability API response in `main.py` |
| TP-02.02 | `_capability_schema_refs()` and `/reports` |
| TP-03.01 | API and capability protocol tests |
| TP-03.02 | API docs and 100% roadmap |
| TP-04.01 | pytest、ruff、mypy、quick CI、governance |
| TP-04.02 | 0014 task docs and INDEX |
