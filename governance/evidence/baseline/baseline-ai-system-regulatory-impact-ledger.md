---
id: BASELINE-AI-SYSTEM-REGULATORY-IMPACT-LEDGER-FATECAT
type: baseline-ai-system-regulatory-impact-ledger
status: archived
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-13
review_cycle: P30D
---

# Baseline AI System Regulatory Impact Ledger

> 历史快照：记录 2026-06 企业迁移初期边界，不作为当前监管或生产准入结论。

## AI Boundary

FateCat 当前核心能力是确定性结构化排盘与民俗参考分析，不是自主决策 AI 系统。AI/Agent 只允许消费稳定 JSON 或 Markdown，不允许直接口算排盘或绕过 capability 契约。

## Systems

| System | Purpose | Deployment role | Risk classification | Human supervision | Logs | Technical docs | Supplier responsibility | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FateCat skill / Agent entry | 让 Agent 调用 CLI/API/Bot/报告生成入口 | Agent tool wrapper | low / folk-reference assistant | required for user-facing interpretation | CLI/API logs pending | `SKILL.md`, `references/*` | OpenAI/Codex runtime external | migration review |
| AI downstream interpretation | 基于 FateCat JSON/Markdown 做解释总结 | downstream consumer | depends on deployment | required | external | downstream-owned | downstream-owned | out of scope, must not be implied as deterministic |

## Blocking Rules

- 高风险 AI 用途无分类、无人工监督、无日志、无技术文档、无供应商责任映射时不得进入 baseline/frozen。
- FateCat 不得输出医疗、法律、金融替代判断或确定性未来断语。
