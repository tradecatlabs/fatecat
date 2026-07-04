# Repo Evidence

- `contracts/fate/audit/external-validation-closure-work-queue.json` 已定义 work queue。
- `contracts/fate/audit/external-validation-proof-ref.json` 已定义 proof-ref evidence upload。
- `scripts/external-validation-closure-work-queue.py` 已输出 22 个当前 category work items。
- `scripts/external-validation-proof-ref-gate.py` 已验证 proof-ref bundle 结构。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已列出 `MI-100.A.03 external validation runbook per category`。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 无真实外部凭证 | 只做本地 runbook contract/generator |
| 不泄露敏感信息 | 禁止 raw URL、token/secret/DSN/private-key marker |
| 不伪造 production live | `shipGate.status=blocked` 必须保持 |
| 不引入服务端上传系统 | 继续使用 JSON artifact 和 local-ci |
| category 不可漏 | 未知 category 必须失败 |

# Change Boundary

允许改动：

- audit contract
- scripts gate/wrapper/local-ci/certification aggregator
- regression tests
- AGENTS/roadmap/task docs/index

禁止改动：

- 业务排盘核心
- 生产部署凭证
- GitHub secret
- 真实外部服务配置

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 新 category 没 runbook | unknown category fail |
| runbook ready 被误写成 live passed | `shipGate` blocked 和 non-claims |
| runbook 输出 raw URL 或 secret marker | gate 全量扫描并拒绝 |
| audit sidecar 绕过 runbook | certification audit domain 追加 category runbooks |
| 文档漂移 | auto-tasks 文档校验和 AGENTS/roadmap 同步 |

# Assumptions and Falsification

- Assumption: 本任务只需要本地 category runbook，不需要运行外部 live。
- Falsifier: 如果用户提供真实外部凭证并要求 live 验证，则必须新开 category live gate 切片，不能在 0121 中伪造。
- Assumption: 22 个当前 category 是 closure work queue 的完整现状。
- Falsifier: 如果 work queue 出现未知 category，runbook gate 必须失败并要求新增 profile。

# Critical Ambiguities

- 各外部系统的真实账号和 endpoint 尚未提供；runbook 只能保留脱敏命令模板。
- runbook 的 proof-ref artifact 真实存储位置尚未确定；本任务只规定 pattern。
- stale alert 的发送渠道尚未确定；下一任务只先做本地趋势 artifact。

# Debug Evidence Contract

- 调试模式: `Optional`

本任务不是 bug 修复；若验证失败，以 targeted pytest、ruff、secret scan 和 quick CI 输出作为定位证据。

# Task Package Context Map

## TP-01 Scope Confirmation

确认 0121 只覆盖 per-category runbook，不进入 live validation 或 stale alert。

## TP-02 Contract And Gate

新增 contract/script/wrapper，并让 certification audit domain 消费 category runbooks。

## TP-03 Regression And Local-CI

新增 category runbooks regression，覆盖 22 个 category、未知 category、脱敏和 wiring。

## TP-04 Validation

运行 targeted pytest、ruff、secret scan、real gate chain、quick CI 和任务文档校验。

## TP-05 Delivery

提交、推送并观察当前 commit 远端 CI；远端 CI 结果不写入仓库，只在交付汇报中报告。
