# AGENTS.md - audit contracts

## 目录用途

`contracts/fate/audit/` 是第三方审计交接资源的机器真相源。这里登记审计 handoff 契约、输出结构、证据来源和外部待验证项策略，不保存真实凭证、生产日志、用户报告正文或外部账号数据。

## 目录结构

```text
audit/
├── AGENTS.md
├── current-bundle.json
├── dry-run.json
├── handoff.json
└── measurement-infrastructure-certification.json
```

## 职责边界

- `handoff.json`：定义 audit handoff generator 的必备输出、Markdown 区块、JSON 字段和 pending external validation 策略。
- `dry-run.json`：定义 audit handoff dry-run verifier 的输入、输出、检查项、ship gate 与 non-claim 策略。
- `current-bundle.json`：定义 current audit bundle 的输入证据、必备输出、required/local 模式和隐私边界。
- `measurement-infrastructure-certification.json`：定义 100% 测算基础设施 certification aggregator dry-run 的输入证据、分域状态、blocked/pending 语义和禁止 100% 伪声明策略。
- 审计包生成器位于 `scripts/audit-handoff.py`，只聚合仓库内证据、Git 状态、任务索引和明确标记的外部待验证项。
- dry-run verifier 位于 `scripts/audit-handoff-dry-run.py`，只做本地审计前置检查，不替代真实第三方审计。
- current audit bundle generator 位于 `scripts/current-audit-bundle.py`，只聚合当前 commit 的 release proof、audit handoff、dry-run、SBOM/provenance、rollback dry-run、local-ci gate artifact 摘要、evidence index、risk register 和外部待验证项；`auditGate=passed` 只代表当前提交审计包证据齐备，不代表第三方审计已通过。
- measurement infrastructure certification aggregator 位于 `scripts/measurement-infrastructure-certification.py`，只消费 local-ci 产物目录中已有 gate summary；当前 release/audit/live evidence 未闭合时必须输出 `status=blocked`，不得支持 100% 完成声明。
- 这里不声明真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal 或 sandbox token 已完成 live 验证。
