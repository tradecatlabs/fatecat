# Repo Evidence

- `contracts/fate/audit/external-validation-closure-work-queue.json` 已定义 work queue。
- `contracts/fate/audit/external-validation-proof-ref.json` 已定义 proof-ref evidence upload。
- `contracts/fate/audit/external-validation-category-runbooks.json` 已定义 per-category operator runbooks。
- `scripts/external-validation-closure-work-queue.py` 已输出 owner/category work item。
- `scripts/external-validation-proof-ref-gate.py` 已输出 accepted/pending proof-ref 结构状态。
- `scripts/external-validation-category-runbooks.py` 已覆盖当前 22 个 category。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已列出 `MI-100.A.04 closure trend dashboard and stale owner alert`。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 无真实外部凭证 | 只做本地 dashboard 和 alert summary |
| 不泄露敏感信息 | 禁止 raw URL、token/secret/DSN/private-key marker |
| 不伪造 production live | `shipGate.status=blocked` 必须保持 |
| 不发送通知 | `alertGate.deliveryStatus=not_sent` |
| 不引入第二状态源 | dashboard 只消费 closure plan/work queue/proof-ref gate/category runbooks |

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
- 外部 issue tracker 或通知系统

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| alert 被误当 live evidence | non-claims、`alertGate.status=blocked`、`shipGate.status=blocked` |
| dashboard 状态源漂移 | 只消费四个上游 artifact，并校验 count/category 覆盖 |
| category runbook 漏项 | dashboard 缺 category runbook 时失败 |
| raw URL 或 secret marker 泄露 | gate 全量扫描并拒绝 |
| certification 绕过 stale alert | audit domain 追加 dashboard artifact、`alertGate` blocker |

# Assumptions and Falsification

- Assumption: 本任务只需要本地 dashboard JSON，不需要真实通知渠道。
- Falsifier: 如果用户提供外部 issue tracker/Slack/飞书/邮件凭证并要求发送通知，必须新开通知交付切片，不能在 0122 中伪造。
- Assumption: closure plan/work queue/proof-ref gate/category runbooks 是当前外部验证控制面的单一真相源。
- Falsifier: 如果出现独立外部工单系统状态源，必须先设计状态同步契约，不能让 dashboard 静默双写。

# Critical Ambiguities

- 真实 stale alert 的发送渠道尚未确定。
- owner 到真实账号的映射尚未确定。
- category live gate 的真实 proof-ref 存储位置尚未确定。
- 本任务仅输出 local JSON dashboard，不输出公网 dashboard。

# Debug Evidence Contract

- 调试模式: `Optional`

本任务不是 bug 修复；若验证失败，以 targeted pytest、ruff、secret scan、real gate chain 和 quick CI 输出作为定位证据。

# Task Package Context Map

## TP-01 Scope Confirmation

确认 0122 只覆盖 closure trend dashboard/stale owner alert，不进入 live validation 或真实通知。

## TP-02 Contract And Gate

新增 contract/script/wrapper，消费 closure plan、work queue、proof-ref gate、category runbooks，输出 dashboard 和 blocked alert gate。

## TP-03 Wiring

新增 regression，接入 local-ci quick artifact、summary、certification audit domain、AGENTS、roadmap、task index。

## TP-04 Validation

运行 targeted pytest、ruff、secret scan、real gate chain、quick CI 和任务文档校验。

## TP-05 Delivery

提交、推送并观察当前 commit 远端 CI；远端 CI 结果不写入仓库，只在交付汇报中报告。
