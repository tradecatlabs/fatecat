---
id: DOC-AUDIT-CASES-README
type: documentation
status: current
owner: engineering
last_reviewed: 2026-07-15
---

# FateCat 项目审计案例

本目录承载仅对 FateCat 成立的复发问题模式，并作为全局 `auto-review` 案例库的项目 overlay。案例必须能转化为审计问题、证据要求、finding 模板或 Gate 建议，不能只记录一次故障故事。

## 使用方式

- 审查报告字段、兼容契约和消费者迁移时，同时加载全局案例库与本目录。
- 新案例必须登记到 `case-registry.yaml`，并通过 strict 校验。
- 用户数据、密钥、生产地址和未脱敏报告不得进入案例正文或 artifacts。
- 同类问题可稳定机械检测后，晋升为项目 architecture gate。

## 验证命令

```bash
python3 /home/lenovo/.codex/skills/auto-review/scripts/validate_audit_cases.py \
  --project-overlay governance/evidence/audit-cases \
  --strict
```
