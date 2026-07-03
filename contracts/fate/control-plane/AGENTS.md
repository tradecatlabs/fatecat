# AGENTS.md - control-plane 协议资产

## 目录用途

`contracts/fate/control-plane/` 存放 FateCat 测算基础设施控制面的资源对账契约。它不保存运行结果，不执行生产动作，只把 Capability、Provider、ReleaseGate、EvaluationRun 等已有资源纳入统一 spec/status/admission/drift 视图。

## 目录结构

```text
control-plane/
├── AGENTS.md
├── registry.json
└── schemas/
    └── control-plane.schema.json
```

## 职责边界

- `registry.json`：控制面资源注册表；只登记已有资源的来源、期望状态、准入策略、验证命令和当前状态口径。
- `schemas/control-plane.schema.json`：控制面资源的机器契约；要求每个资源具备 `spec`、`status`、`links` 和 `metadata`。
- 控制面只做发现、对账和 drift 防护，不替代各资源自己的深度 gate。
- Provider 的供应链、license、trace 和 lifecycle 深度校验仍由 `scripts/provider-lifecycle-gate.sh` 负责。
- ReleaseGate 的当前发布证明仍由 `scripts/current-release-proof.sh` 负责；本目录不保存 run id、digest、token、生产日志或用户报告正文。
- EvaluationRun 只登记可复现入口和门禁口径，不保存 benchmark 答案、完整报告正文或运行结果库。
