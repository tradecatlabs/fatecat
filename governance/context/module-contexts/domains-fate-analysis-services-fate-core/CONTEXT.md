---
id: CTX-DOMAINS-FATE-ANALYSIS-SERVICES-FATE-CORE
type: module-context
status: current
owner: fate-core
created: 2026-07-13
last_reviewed: 2026-07-13
code_path: domains/fate-analysis/services/fate-core
---

# Fate Core Context

## 模块职责

- 拥有 capability 执行协议、八字/紫微计算用例、规则证据和确定性结果。
- 通过 provider 适配成熟历法/排盘引擎；不拥有 HTTP、Web、Bot 或持久化交付逻辑。
- wheel 中只嵌入运行所需契约快照；不可分发引擎资产不得伪装成包依赖。

## 上下游

- 上游：`contracts/fate/`、已登记供应链和项目规则 registry。
- 下游：`fatecat-delivery`、CLI、评测与报告渲染。
- 禁止反向导入 delivery、apps 或运行环境配置。

## 关键门禁

- `tests/regression/test_capability_protocol.py`
- `bash scripts/provider-lifecycle-gate.sh`
- `bash scripts/core-quality-corpus-gate.sh`
- `bash scripts/package-distribution-smoke.sh`

## 禁止事项

- 禁止 planned capability 执行。
- 禁止新增第二套八字生产引擎或无证据规则。
- 禁止用同一引擎生成的 fixture 声称独立正确性证明。
