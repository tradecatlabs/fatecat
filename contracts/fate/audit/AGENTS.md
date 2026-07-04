# AGENTS.md - audit contracts

## 目录用途

`contracts/fate/audit/` 是第三方审计交接资源的机器真相源。这里登记审计 handoff 契约、输出结构、证据来源和外部待验证项策略，不保存真实凭证、生产日志、用户报告正文或外部账号数据。

## 目录结构

```text
audit/
├── AGENTS.md
├── current-bundle.json
├── dry-run.json
├── external-validation-category-runbooks.json
├── external-validation-closure.json
├── external-validation-closure-trend-dashboard.json
├── external-validation-closure-work-queue.json
├── external-validation-live-proof-gate.json
├── external-validation-proof-ref.json
├── handoff.json
├── measurement-infrastructure-certification.json
├── production-live-delivery-evidence-bundle.json
├── production-live-operator-execution-packet.json
└── schemas/
    ├── external-validation-live-evidence.schema.json
    └── external-validation-proof-ref.schema.json
```

## 职责边界

- `handoff.json`：定义 audit handoff generator 的必备输出、Markdown 区块、JSON 字段和 pending external validation 策略。
- `dry-run.json`：定义 audit handoff dry-run verifier 的输入、输出、检查项、ship gate 与 non-claim 策略。
- `current-bundle.json`：定义 current audit bundle 的输入证据、必备输出、required/local 模式和隐私边界。
- `external-validation-category-runbooks.json`：定义外部验证 category runbook 契约，为每个 work queue category 固化 required credential、operator command、proof-ref artifact pattern、redaction rule、expiry policy、failure rollback 和 closure condition。
- `external-validation-closure.json`：定义外部待验证项关闭计划门禁的输入、输出字段、owner/凭证/关闭条件要求和隐私边界。
- `external-validation-closure-trend-dashboard.json`：定义外部验证关闭趋势 dashboard 契约，聚合 closure plan、work queue、proof-ref gate、category runbooks 和可选 live proof gate，输出 owner/category/status 趋势与 stale alert；不发送真实通知，不关闭 live evidence。
- `external-validation-closure-work-queue.json`：定义外部待验证项 owner/category 工作队列契约，把 closure plan 聚合成可派发、可跟踪、但仍 pending 的 work item。
- `external-validation-live-proof-gate.json`：定义外部验证 live proof gate 契约，校验 operator 脱敏 live evidence 与 work item、proof-ref、category runbook 和当前 commit 的绑定；不执行真实生产请求，不替代第三方审计。
- `external-validation-proof-ref.json`：定义外部验证 proof-ref 与 evidence upload 契约，只校验证据句柄、hash、时间窗、redaction、current commit 与 work item 绑定，不证明外部 live 已通过。
- `schemas/external-validation-live-evidence.schema.json`：定义 operator 提供的脱敏 live evidence bundle 结构。
- `schemas/external-validation-proof-ref.schema.json`：定义 operator 提供的脱敏 proof-ref bundle 结构。
- `measurement-infrastructure-certification.json`：定义 100% 测算基础设施 certification aggregator dry-run 的输入证据、分域状态、blocked/pending 语义和禁止 100% 伪声明策略。
- `production-live-delivery-evidence-bundle.json`：定义生产交付 live evidence bundle 装配契约，把 production API、HF Space、Telegram Bot、公网 webhook 和多端 live parity 的脱敏 summary 转成 live proof gate 可校验的 evidence bundle。
- `production-live-operator-execution-packet.json`：定义生产 live operator execution packet 契约，把 work queue、proof-ref gate、category runbooks、live proof gate 和 delivery evidence bundle 串成可执行但不含敏感值的操作包。
- 审计包生成器位于 `scripts/audit-handoff.py`，只聚合仓库内证据、Git 状态、任务索引和明确标记的外部待验证项。
- dry-run verifier 位于 `scripts/audit-handoff-dry-run.py`，只做本地审计前置检查，不替代真实第三方审计。
- current audit bundle generator 位于 `scripts/current-audit-bundle.py`，只聚合当前 commit 的 release proof、audit handoff、dry-run、SBOM/provenance、rollback dry-run、local-ci gate artifact 摘要、evidence index、risk register 和外部待验证项；local-ci gate artifact 当前覆盖 evidence coverage trend gate 与 evaluation trend gate；`auditGate=passed` 只代表当前提交审计包证据齐备，不代表第三方审计已通过。
- external validation closure gate 位于 `scripts/external-validation-closure-gate.py`，只把外部待验证 occurrence 转成可分派的关闭计划，不连接真实 API、Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 或第三方审计系统。
- external validation closure work queue 位于 `scripts/external-validation-closure-work-queue.py`，只把 closure plan 按 owner/category 聚合成 work item，补齐 assignee、proofRef、lastCheckedAt、staleReason 和 closeConditionResult；空 proofRef 必须保持 blocked，不连接真实外部系统。
- external validation proof-ref gate 位于 `scripts/external-validation-proof-ref-gate.py`，消费 work queue 和可选 operator 脱敏 evidence bundle；接受结构不等于生产放行，`shipGate` 必须继续 blocked，直到 category live gate 和第三方审计另行闭合。
- external validation category runbooks gate 位于 `scripts/external-validation-category-runbooks.py`，消费 work queue，为每个 category 生成 operator runbook；runbook ready 只代表可执行指引齐备，不证明 live evidence 已完成。
- external validation closure trend dashboard 位于 `scripts/external-validation-closure-trend-dashboard.py`，消费 closure plan、work queue、proof-ref gate、category runbooks 和可选 live proof gate，输出本地 owner/category/status dashboard 与 stale alert；alert 只是待办提醒，不发送外部通知，不关闭 proof-ref/category live/第三方审计阻断。
- external validation live proof gate 位于 `scripts/external-validation-live-proof-gate.py`，消费 work queue、proof-ref gate、category runbooks 和可选 operator 脱敏 live evidence bundle；只接受已 schema-accepted proof-ref 对应的 live proof，并继续保持第三方审计/认证阻断。
- production live delivery evidence bundle assembler 位于 `scripts/production-live-delivery-evidence-bundle.py`，消费 delivery live summary JSON 和外部验证三件套，默认无真实 summary 时只输出 pending bundle；有真实脱敏 summary 时仅输出 proof id、artifact hash 和 source binding，不复制 URL/token/DSN/webhook secret。
- production live operator execution packet generator 位于 `scripts/production-live-operator-execution-packet.py`，消费外部验证三件套，输出 operator 步骤、必需环境变量名、proof-ref bundle 模板和最终 gate 命令；它不执行真实外部请求，不保存 URL/token/DSN/webhook secret，不证明 live passed。
- measurement infrastructure certification aggregator 位于 `scripts/measurement-infrastructure-certification.py`，默认消费 local-ci 产物目录中已有 gate summary，也可显式接收 `live-release-gate.json`、`current-release-proof.json` 和 `current-audit-bundle.json` sidecar；sidecar 只覆盖对应逻辑证据文件，不跨文件覆盖 release proof、audit bundle 或外部 live 证据。当前 release/audit/live evidence 未闭合时必须输出 `status=blocked`，不得支持 100% 完成声明。
- 这里不声明真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal 或 sandbox token 已完成 live 验证。
