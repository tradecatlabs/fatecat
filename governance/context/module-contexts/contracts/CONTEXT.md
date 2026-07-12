---
id: CTX-CONTRACTS
type: module-context
status: current
owner: architecture
created: 2026-07-13
last_reviewed: 2026-07-13
code_path: contracts
---

# Contracts Context

## 模块职责

- 机器可读定义 capability、provider、profile、delivery、evidence、security、observability 和数据供应链协议。
- 合同只描述可验证事实、生命周期和风险边界，不保存运行态结果、用户数据或凭证。
- wheel 构建可嵌入必要合同快照，但 canonical 真相源仍是本目录。

## 依赖边界

- `domains/` 和 `scripts/` 消费 contracts；contracts 不导入业务源码。
- 人类文档必须引用 contracts，不得在路线图中建立平行机器协议。

## 关键门禁

- `tests/regression/test_capability_protocol.py`
- `tests/regression/test_api_contracts.py`
- `bash scripts/check-structure.sh`
- `bash scripts/data-supply-chain-gate.sh`

## 禁止事项

- 禁止把未来功能登记为 production。
- 禁止把 pending/blocked 外部证据改写成 accepted。
- 禁止 schema 与实现字段无迁移计划地分叉。
