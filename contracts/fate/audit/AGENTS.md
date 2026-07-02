# AGENTS.md - audit contracts

## 目录用途

`contracts/fate/audit/` 是第三方审计交接资源的机器真相源。这里登记审计 handoff 契约、输出结构、证据来源和外部待验证项策略，不保存真实凭证、生产日志、用户报告正文或外部账号数据。

## 目录结构

```text
audit/
├── AGENTS.md
└── handoff.json
```

## 职责边界

- `handoff.json`：定义 audit handoff generator 的必备输出、Markdown 区块、JSON 字段和 pending external validation 策略。
- 审计包生成器位于 `scripts/audit-handoff.py`，只聚合仓库内证据、Git 状态、任务索引和明确标记的外部待验证项。
- 这里不声明真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal 或 sandbox token 已完成 live 验证。
