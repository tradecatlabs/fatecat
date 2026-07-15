---
id: DOC-AUDIT-CASES-AGENTS
type: architecture
status: current
owner: engineering
last_reviewed: 2026-07-15
---

# AGENTS.md - FateCat 项目审计案例

## 目录用途

`audit-cases/` 是 FateCat 项目特有的审计案例 overlay。它补充全局 `auto-review` 案例库，只保存依赖本仓库契约、字段或模块边界的复发模式。

## 目录结构

```text
audit-cases/
├── AGENTS.md
├── README.md
├── INDEX.md
├── CASE.template.md
├── case-registry.yaml
└── cases/
    └── CASE-9001-canonical-field-and-compatibility-projection-double-consumption/
        ├── CASE.md
        └── artifacts/
            └── README.md
```

## 职责边界

- `case-registry.yaml`：机器可读的项目案例注册表。
- `cases/*/CASE.md`：问题模式、审计问题、证据和 Gate 建议的真相源。
- `cases/*/artifacts/`：案例的脱敏复现或验证证据，不保存运行态日志和用户数据。
- 跨项目通用模式必须进入全局案例库，不在此复制。
- 可机械阻断的高频问题应晋升到 `governance/architecture-gates/`，案例本身不替代 Gate。

## 验证

```bash
python3 /home/lenovo/.codex/skills/auto-review/scripts/validate_audit_cases.py \
  --project-overlay governance/evidence/audit-cases \
  --strict
```
