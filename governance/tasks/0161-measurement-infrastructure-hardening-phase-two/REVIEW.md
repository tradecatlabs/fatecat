# Review

## Result

- Scope: 审查用户要求的第 2 到 9 项；第 1 项专业断语明确不在本次改动范围。
- Decision: `PASS`
- BLOCK: 0
- Unresolved implementation findings: 0
- External pending: 人类命理专家评审、生产 API/数据库/Bot live、多副本指标后端和公共 package registry 发布。

## Findings Resolved During Review

1. `P1 correctness`：公开 Markdown 表格校验只识别 `| :--` 分隔线，标准 `| --- |` 可绕过未知表头 allowlist。已改为通用 Markdown 分隔单元识别，并增加无空格、居中对齐分隔符回归；7 tests passed。
2. `P1 contract drift`：生命周期迁移后，control-plane、provider dependency/drift/lifecycle gates、公开说明页和 GEO audit 仍存在旧 `status` 语义。已统一为 `availability` 决定执行、`maturity.status` 表示成熟度；控制面 219 checks 和 26 个专项回归通过。
3. `P1 supply-chain drift`：evaluation registry 更新后，data supply chain manifest 仍保存旧 SHA256。已刷新为真实 hash，门禁 8 assets、14 classics、172 checks 通过。
4. `P2 repository hygiene`：任务 0159 文档残留本机个人路径和易被 secret scanner 误判的赋值表达。已改为不含个人路径的描述，secret scan 2197 files、0 findings。

## Lens Review

- Correctness: 公开报告 allowlist、完整 98 年/1176 月输出、60 甲子乘 12 月等价、planned 拒绝执行和异步终态均有回归；未发现结果语义退化。
- Reliability/concurrency: job metrics 在 `ReportJobManager._lock` 内记录，终态按 job/status 去重；取消、失败、成功、过期路径均覆盖。进程重启后 Prometheus counter 重置属于当前进程级指标边界，不伪装为多副本持久指标。
- Performance: 流年父级干支从每月重复计算收敛为每年一次；最终本地 smoke 为 bazi first 412.921 ms、warm p95 358.638 ms，ziwei first 127.286 ms、warm p95 136.39 ms。结果大小和完整范围未缩减。
- Architecture: 公开投影、领域 evidence、执行资格、成熟度、指标和分发对象分别具有机器契约；兼容 `Capability.status` 仅保留成熟度投影，不作为内部执行准入。
- Future-optimal/ponytail: 未新增通用报告框架、队列服务或私有历法算法；新增对象均有直接消费者和回归。未保留永久双轨真相源。
- Security/privacy: metrics 只使用固定状态标签；公开客户端限制响应大小、标识符与站内路径；报告 allowlist 和 secret/source hygiene gates 通过。
- License/distribution: `fatecat-client` 为独立 MIT、零运行依赖远程客户端；wheel/sdist archive allowlist 和 clean-room HTTP smoke 通过。bazi-1、sxwnl 仍为 `NOASSERTION` 且禁止公共分发，完整服务端运行时继续 restricted。
- Document drift: capability、control-plane、developer、observability、distribution、scripts/tests AGENTS 和任务文档已同步；第 1 项与外部 live 均明确保留待执行。

## Verification

- `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0161-closeout`：PASS；513 passed，Ruff/format/mypy/vendor/structure/security/privacy/control-plane/provider/performance/package gates 全部通过。
- `.venv/bin/python -m pytest -q tests/regression/test_public_report_visibility.py`：7 passed。
- 生命周期专项测试：26 passed。
- `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-0161.json`：PASS。
- `git diff --check`：PASS。

## Residual Boundaries

- 第 1 项专业断语正确性由人类命理专家后续处理，本次没有修改或认证。
- 外部连通验证待执行：真实 API、PostgreSQL、多副本、Telegram Bot、OTel 后端和发布 registry。
- 本地性能数据是单机单进程 wall-clock，不代表生产 p95/p99；生产环境需用真实负载另行验收。
- 全任务树中 `0090`、`0091` 两个历史任务仍使用旧版任务文档模板；当前任务 `0161` 的 closeout 严格校验已通过，该历史治理债不改变本轮实现结论。
