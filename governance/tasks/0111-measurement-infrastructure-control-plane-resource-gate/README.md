# Task Overview
- Task ID: `0111`
- Slug: `measurement-infrastructure-control-plane-resource-gate`
- Objective: `执行 0109 后续 W1 切片：新增 control-plane 资源注册表、schema 与 gate，把 Capability、Provider、ReleaseGate、EvaluationRun 纳入统一 spec/status/admission/drift 对账视图；复用既有 capability/provider/evaluation/release 契约和 provider lifecycle gate，不保存运行结果、生产凭证或报告正文，并接入 local-ci quick 与回归测试。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/control-plane/` 契约目录、schema、registry 和目录说明。
- 新增 `scripts/control-plane-gate.py/.sh`，对账 Capability、Provider、ReleaseGate、EvaluationRun 四类资源。
- 新增 `tests/regression/test_control_plane_gate.py`。
- 将 control-plane gate 接入 `scripts/local-ci.sh --profile quick`。
- 更新 `contracts/fate/AGENTS.md` 与主路线图 W1 状态。

## Out of Scope
- 不实现 Kubernetes controller、数据库 controller 或后台 reconciliation loop。
- 不修改生产 API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS。
- 不把 control-plane gate pass 写成生产 live pass。
- 不复制已有 registries 的完整内容，不保存运行结果、真实凭证、报告正文或用户输入。

## Task Package Tree
```text
TP-01 资源事实扫描
TP-02 control-plane 契约落盘
TP-03 gate 与 local-ci 接入
TP-04 回归测试与文档同步
TP-05 提交推送与交付证据
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| W1 Control plane | 以 control-plane registry/gate 实现 spec/status/admission/drift 对账基线。 |
| 复用现有资源 | Capability、Provider、ReleaseGate、EvaluationRun 均指向现有 registry/gate。 |
| planned 不可执行 | control-plane gate 重新校验 planned provider、engineVersion、testGate 和 markdownDefault。 |
| Provider 深度复用 | control-plane gate 调用 provider lifecycle gate，不重写 source/license/vendor 检查。 |
| 不伪造生产 live | ReleaseGate 保持 `pending_external`，live shipGate blocked 不是 gate 失败。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 扫描 `contracts/fate/*`、相关 scripts 和 regression tests。 |
| TP-02 | Done | 新增 `contracts/fate/control-plane/registry.json` 与 schema。 |
| TP-03 | Done | 新增 `scripts/control-plane-gate.py/.sh` 并接入 local-ci quick。 |
| TP-04 | Done | 新增回归测试，更新 AGENTS 和路线图。 |
| TP-05 | Done | 提交推送和远端 CI 证据由最终汇报记录。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
