# Debug Record

## Bug

- 标题：测算基础设施边界、性能、生命周期、观测与分发证据不闭合
- 症状：公开 Markdown 缺少统一允许字段契约；完整八字冷进程明显慢于热进程；capability 可执行状态与成熟度表达冲突；异步任务只有 HTTP 外层延迟；未知许可证运行时不能形成公开分发闭包。
- 首次发现位置 / 时间：2026-07-16 第二阶段基础设施审查。

## Environment

- 仓库 / 模块：FateCat `main`；fate-core、fatecat-delivery、contracts、packaging、observability。
- 运行环境：Ubuntu / Python 3.12；项目 `.venv`。
- 外部边界：人类命理专家评审、生产 live 与未知许可证授权不在本地伪造。

## Reproduction

1. 对多个匿名样本生成公开 Markdown，扫描机器规则 ID、provider/source 编码和内部调试字段。
2. 在独立 Python 进程和同一进程分别计算完整八字，比较耗时、月份数量和结构化结果。
3. 比较 capability registry 的顶层状态、maturity、executor 判定和 API 投影。
4. 提交异步报告任务并检查 `/metrics` 是否能区分排队和执行时长。
5. 检查公开发行物是否依赖 bazi-1、sxwnl 或其他未知许可证资产。

## Observations

- O1：冷进程完整八字约 4.4 至 4.7 秒，热进程约 0.32 至 0.36 秒；主要热点为逐月 `LiuYue.getGanZhi` 的父级重复计算。
- O2：报告渲染已局部隐藏内部字段，但缺少单一公开字段允许契约。
- O3：almanac/meihua 顶层 `production` 与 `L3 validated` 同时存在。
- O4：HTTP latency 只覆盖 job 创建/轮询请求，不能表示后台计算耗时。
- O5：受限运行时 release gate 能阻断，但尚需证明公开客户端在无受限资产环境可独立工作。

## Hypotheses

### H1: （ROOT HYPOTHESIS）领域结果、公开投影、运行状态和分发对象缺少各自单一契约

- Supports：同一对象存在隐式渲染字段、双状态语义、外层 HTTP 指标代替后台任务指标以及全运行时/公开客户端边界混合。
- Conflicts：近期修复已消除部分具体泄露和重复，不能把所有问题归为同一代码缺陷。
- Test：分别建立公开字段、lifecycle、job metrics 和 distribution manifest 契约，验证消费者只依赖对应真相源。

### H2: 冷启动退化来自 lunar-python 父级年结果在每个月被重复构造

- Supports：profile 显示 1152 次月干支调用伴随大量年干支和 Solar/Lunar 转换。
- Conflicts：天文历法初始化和模块导入也可能占据显著冷启动时间。
- Test：缓存同一 `LiuNian` 的稳定父级结果，比较调用次数、结果等价和冷进程耗时。

### H3: 未分级的 golden 会把引擎自洽误当作独立准确性

- Supports：部分节气边界由 lunar-python 自身生成后再由同一引擎验证。
- Conflicts：仓库已有外部交节表和 benchmark 资产，需先盘点实际来源。
- Test：runner 必须拒绝 `origin=self_generated` 的 fixture 进入 independent gate。

## Experiments

### E1
- Hypothesis: H1
- Change: 新增 profile 级 `publicMarkdown` allowlist 与 `report_visibility.py` 验证薄层，并补标准 Markdown 表格分隔符绕过测试。
- Command: `.venv/bin/python -m pytest -q tests/regression/test_public_report_visibility.py`
- Expected: 机器规则 ID、provider/source 编码和未知表头不得进入 Markdown，结构化 `analysisEvidence` 不被删除。
- Result: 7 个样本/契约回归通过，公开字段边界由机器契约约束。
- Verdict: confirmed
- Revert: 删除 validator 会使绕过用例失败；保留当前契约与回归。

### E2
- Hypothesis: H2
- Change: 复用 `lunar_python.eightchar.LiuYue`，同一流年干支只构造一次。
- Command: `.venv/bin/python -m pytest -q tests/regression/test_monthly_performance_equivalence.py && .venv/bin/python scripts/core-performance-smoke.py --output-json /tmp/fatecat-core-performance-0161.json`
- Expected: 60 甲子乘 12 月结果等价，完整范围保持不变且 first/warm 性能满足预算。
- Result: 完整样本保持 98 个流年、1176 个流月和 1176 个月度神煞；最终 Quick CI 中八字 first execution 412.921 ms、warm p95 358.638 ms。
- Verdict: confirmed
- Revert: 若未来 lunar-python 接口变化，回退为原生 `ln.getLiuYue()` 输出并由等价测试阻止语义漂移。

### E3
- Hypothesis: H3
- Change: Dataset/EvaluationRun schema 强制 `evidenceClass`，区分内部回归、独立参考、外部 benchmark 与专家签字。
- Expected: 自产 fixture 不能进入 independent gate，MingLi-Bench 只用于 evaluation，专家结论保持待执行。
- Result: 交节表登记为独立来源，MingLi-Bench 保持 evaluation-only，human attestation 未被本地测试伪造。
- Verdict: confirmed
- Revert: schema 和 registry 必须同步回退；不得仅删除分类字段。

### E4
- Hypothesis: H1
- Change: 以 `availability` 决定执行资格，以 `maturity.status` 表示成熟度，并全仓迁移直接消费者。
- Command: `.venv/bin/python -m pytest -q tests/regression/test_control_plane_gate.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_drift_scanner.py tests/regression/test_geo_discovery.py`
- Expected: available/validated 与 available/production 均可执行，planned 拒绝执行，控制面对账不读取旧顶层状态。
- Result: 初次 Quick CI 暴露旧消费者；修复后控制面 219 checks 与 26 个专项回归通过。
- Verdict: confirmed
- Revert: 保留公共 `Capability.status` 成熟度投影，但内部执行门禁不得回退读取它。

### E5
- Hypothesis: H1
- Change: ReportJobManager 记录 queue wait、execution duration、result size 与固定终态计数，并通过 `/metrics` 导出。
- Expected: 指标能区分后台排队/执行和 HTTP 外层延迟，且没有 PII 或高基数标签。
- Result: succeeded/failed/expired/cancelled 路径和三个 histogram 回归通过，输出不含姓名、地区或任务 ID 标签。
- Verdict: confirmed
- Revert: 若停用指标，必须同时移除观测契约和门禁，不得保留虚假指标声明。

### E6
- Hypothesis: H1
- Change: 新增独立 `fatecat-client` stdlib HTTP 客户端、分发 manifest 和 archive allowlist/clean-room smoke。
- Command: `.venv/bin/python scripts/public-client-package-smoke.py --output /tmp/fatecat-public-client-package-0161`
- Expected: wheel/sdist 不含服务端或未知许可证资产，可在无依赖 venv 中安装并调用 HTTP fixture。
- Result: wheel 7 members、sdist 8 members、runtime dependencies 为空；服务端运行时保持 restricted。
- Verdict: confirmed
- Revert: 若撤销客户端包，完整服务端仍不得改标为公共可分发。

### E7
- Hypothesis: H1
- Change: 对全部切片执行最终本地集成门禁。
- Command: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0161-final`
- Expected: 契约、性能、供应链、安全、隐私、格式、类型和重点回归全部通过。
- Result: Ruff、format、mypy、供应链、控制面、provider、L4 golden、性能、隐私、安全、打包与 513 个重点回归全部通过。
- Verdict: confirmed
- Revert: 只读验证，无需回滚；外部生产 live 和人工专家评审仍未执行。

## Root Cause

- 主根因：领域结构化结果、公开 Markdown、能力执行资格、成熟度、后台任务指标和公开分发对象此前依赖实现惯例，没有各自的单一机器契约。
- 性能根因：流月构造路径对同一流年的稳定干支结果重复计算，而不是 lunar-python 本身无法满足完整输出。
- 迁移根因：旧 `status` 同时承担“能否执行”和“成熟度”两种语义；即使注册表已迁移，控制面和 smoke 中仍存在旧消费者。
- 供应链门禁失败根因：评测 registry 合法更新后，其受控资产 SHA256 未同步刷新；门禁正确阻止了来源证据漂移。

## Fix

- 公开层：以 profile `publicMarkdown` 契约和单一 validator 约束 Markdown，不删除领域结构化 evidence。
- 计算层：复用成熟 `LiuYue` 类型并缓存单个流年稳定父级结果；未引入自研历法算法或无界全局缓存。
- 证据层：schema 强制 evidence class，并保持专家签字和外部 benchmark 的未完成状态。
- 生命周期：`availability` 是执行准入真相源，`maturity.status` 是成熟度真相源；旧 `Capability.status` 只保留为有边界的成熟度投影。
- 复杂度：把基本资料、神煞、基础命盘上下文和运势神煞映射提取为直接消费者 helper，未新增通用框架。
- 观测层：在 job manager 内记录固定低基数生命周期指标，并由 `/metrics` 导出。
- 分发层：完整服务端运行时继续 restricted；公开发行物改为独立 MIT 客户端，只通过远程 API 使用服务能力。
- 仓库层：清除任务 0159 文档中的本机个人路径和误触 secret scanner 的伪赋值文本，同步数据供应链 hash。

## Regression Evidence

- `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0161-closeout`：PASS；513 passed。
- `.venv/bin/python -m pytest -q tests/regression/test_control_plane_gate.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_drift_scanner.py tests/regression/test_geo_discovery.py`：26 passed。
- `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-0161.json`：PASS；8 assets、14 classics、172 checks。
- `scripts/public-client-package-smoke.py`（由 Quick CI 调用）：PASS；clean-room 安装、archive allowlist、本地 HTTP fixture 全部通过。
- `scripts/core-performance-smoke.py`（由 Quick CI 调用）：PASS；bazi first 412.921 ms、warm p95 358.638 ms；ziwei first 127.286 ms、warm p95 136.39 ms。
- `.venv/bin/ruff check .`、`.venv/bin/ruff format --check .`、mypy `fate_core`：均由最终 Quick CI 验证通过。

## Failed Nodes

- 已恢复：control-plane gate 因旧顶层 `status` 消费失败；迁移全部直接消费者后通过。
- 已恢复：data supply chain gate 因 evaluation registry 的旧 SHA256 失败；刷新真实 hash 后通过。
- 已恢复：Ruff format gate 要求格式化 `provider-dependency-smoke.py`；格式化后最终 Quick CI 通过。
- 未失败但仍外部待办：第 1 项专业断语、人类专家签字和生产 live 证据。

## First Invalid Node

- 初始首个无效节点为 TP-01（公开字段契约缺失）；实现后，集成验证首个失效节点为 TP-04 的旧控制面消费者，现已修复并复验。

## Upstream Lineage

- capability provider 结构化结果、报告 job manager、contracts registry 与 packaging manifest。

## Downstream Blast Radius

- Web/API/Bot/CLI Markdown、Agent API、Prometheus、公开 wheel/skill 和第三方审计。

## Lowest Common Refinement Ancestor

- 测算能力从领域结果到公开交付的契约边界。

## Repair Boundary

- 仅限任务计划登记模块；不改专业断语、不减少完整输出。

## Frozen Nodes

- 第 1 项专业内容、人类评审、外部生产 live、新预测体系和 Web 视觉。

## Invalidated Nodes

- 已恢复：公开字段受控、完整输出性能、capability 执行/成熟度语义、异步任务观测、公开客户端闭包。
- 仍无效：“专业断语已由专家认证”“生产公网/数据库/Bot live 已验证”“完整服务端运行时可发布公共 registry”。

## Reverification Required

- 本地变更后必须重跑 Quick CI、公开客户端 clean-room smoke、数据供应链 gate 与任务/governance strict。
- 人类专家评审和外部生产 live 必须由真实账号、凭证和环境另行执行，不能由本地 fixture 替代。
