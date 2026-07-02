# Repo Evidence
- 当前仓库根：`/home/lenovo/.projects/fatecat`。
- 当前任务上游：`0010-measurement-infrastructure-wave1-resources` 已完成 capability resource / error catalog；`0011-measurement-infrastructure-wave1-jobs` 已完成 report job 幂等和取消切片。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py` 当前通过 provider 字符串映射到 usecase 函数，仍不是 provider object 协议。
- `contracts/fate/capabilities/registry.json` 已登记 `bazi`、`ziwei`、`almanac`、`meihua` 为 production，其他新体系为 planned。
- `tests/regression/test_capability_protocol.py` 已覆盖 registry、planned 拒绝、bazi/ziwei/almanac/meihua 执行。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 明确 IMP-03 需要 provider protocol、provider registry、provider health、error normalization 和 bazi/ziwei adapter。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 默认 Markdown 只能是 `bazi` | 本轮不改报告 profile 和默认输出。 |
| planned 能力不得执行 | `CapabilityExecutor` 先做 capability admission，再找 provider。 |
| 胶水原则 | 不引入新依赖；provider 只包装现有成熟 usecase。 |
| 最少改动 | 不迁移具体算法；只改能力执行边界。 |
| 文档驱动 | 同步任务容器、局部 AGENTS、API/路线图文档和回归测试。 |

# Change Boundary
- 允许修改：`fate_core/capabilities/*`、相关 regression tests、capability docs、100% 计划、0012 任务文档。
- 禁止修改：八字/紫微/黄历/梅花具体计算逻辑、Web UI 视觉、Bot 生产配置、外部部署配置。
- 如果需要新增文件，只允许新增 provider 协议运行时文件，不新增无主抽象。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| monkeypatch 测试失效 | 既有 delegate 测试会失败 | provider registry 动态读取模块函数，保持 monkeypatch 可见。 |
| provider 协议过度抽象 | 增加维护负担 | 只保留 validate/calculate/metadata/health 四个本轮需要的方法。 |
| 异常包装破坏错误信息 | API contract 退化 | 只补统一前缀和 provider 元信息，不吞掉原始异常语义。 |
| planned 绕过执行门禁 | 未完成能力被执行 | executor 先校验 `status == production`。 |

# Assumptions and Falsification
- Target end state: 所有 production capability 经统一 provider object 执行，每个 provider 可被发现、健康检查和版本审计。
- Real constraints: 现有 public API 和测试依赖 `CapabilityExecutor().execute(CapabilityInput(...))`；registry provider 字符串已经是契约。
- Inertia constraints: 旧函数路由和 monkeypatch 习惯不能决定最终结构，只能作为迁移约束处理。
- Wrong concept / wrong boundary: executor 内部维护散落函数路由表。
- Kill list: 删除 executor 内私有 `_provider_handlers()` 作为唯一 provider 真相源。
- Proof point: capability/API targeted tests、quick CI、mypy 和 task validators 全部通过。
- Falsifier: 如果 provider object 不能保持现有 bazi/ziwei/almanac/meihua 行为，或 planned capability 可执行，则本切片失败。
- Migration slice: 先在 fate-core 内建 provider registry；后续再补 provider schema、health endpoint 和跨进程执行。
- Rejected short-term patches: 不继续往 executor 里追加 if/else；不为未实现体系写假 provider。

# Critical Ambiguities
- 无阻塞歧义。跨进程 provider health、外部依赖探测和 webhook callback 属后续任务。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；若出现回归，最小复现命令为 `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error or report_job'`。

# Task Package Context Map
| Node | Required Context |
| --- | --- |
| TP-01.01 | `contracts.py`、`executor.py`、registry provider 字段 |
| TP-01.02 | production capabilities: `bazi`、`ziwei`、`almanac`、`meihua` |
| TP-02.01 | `CapabilityExecutor.execute` 当前行为和 API response contract |
| TP-02.02 | `errors.json`、API error behavior、metadata payload |
| TP-03.01 | `test_capability_protocol.py`、`test_api_contracts.py` |
| TP-03.02 | `capabilities/AGENTS.md`、100% 实现计划 |
| TP-04.01 | pytest、ruff、mypy、local-ci、governance validators |
| TP-04.02 | 0012 task docs 和 `governance/tasks/INDEX.md` |
