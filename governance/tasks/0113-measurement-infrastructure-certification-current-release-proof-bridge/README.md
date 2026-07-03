# Task Overview
- Task ID: `0113`
- Slug: `measurement-infrastructure-certification-current-release-proof-bridge`
- Objective: `修复 certification aggregator 的当前发布证据桥接盲区：允许显式消费独立生成的 current-release-proof sidecar JSON，同时保持 live-release-gate 的生产外部连通阻断语义不变。`
- Status: `Done`

## In Scope
- 为 `scripts/measurement-infrastructure-certification.py` 增加 `current-release-proof.json` sidecar 输入。
- 在 certification summary 中记录 `evidenceOverrides`，让审计人员能区分 local-ci 目录证据和外部侧载证据。
- 更新 `contracts/fate/audit/measurement-infrastructure-certification.json` 的生成命令和输出字段。
- 增加回归测试，证明 sidecar release proof 通过时，生产 live release gate 仍可保持 blocked。
- 更新 100% 测算基础设施路线图和任务索引。

## Out of Scope
- 不把 release proof sidecar 写回 repo 或 local-ci 输出目录。
- 不修改 `live-release-gate.json` 的生产 live 语义。
- 不声明生产 API、HF、Bot、OIDC、SIEM、OTel、Vault/KMS 或多副本 live 已完成。
- 不读取、输出或保存真实 token、secret、DSN、URL、报告正文或用户输入。

## Task Package Tree
```text
TP-01 证据桥接盲区确认
TP-02 certification sidecar 输入落地
TP-03 契约、测试和路线图同步
TP-04 验证、自审、提交推送
```

## Future-Optimal Contract
| Field | Value |
| --- | --- |
| Target End State | Certification 聚合器可以消费当前 HEAD 的最终 release proof sidecar，同时不改变 production live gate 的独立阻断职责。 |
| Real Constraints | 最终 release proof 不能写回 Git，否则会制造新 HEAD；local-ci 产物生成时间早于远端 release proof；live 证据必须独立提供。 |
| Inertia Constraints | 旧聚合器只从单一 evidence dir 读文件，导致当前 release proof 与 local-ci artifact 时间线混在一起。 |
| Kill List | 不新增第二套 certification；不复制 release proof 逻辑；不把 blocked live gate 覆盖为 passed。 |
| Proof Point | 使用 sidecar 后，`current-release-proof.json` 证据为 passed/override，但 release domain 仍因 `live-release-gate.json` blocked。 |
| Falsifier | 如果 sidecar 能让 `live-release-gate.json` 被绕过，或 summary 无法追踪证据来源，则任务失败。 |
| Migration Slice | 只新增可选 CLI 参数和 summary 字段，保持默认行为兼容。 |

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 100% 基础设施认证可审计 | 明确区分 local-ci evidence dir 与独立 current release proof sidecar。 |
| 不伪造生产 live | live-release-gate 仍从 evidence dir 读取并独立阻断。 |
| 当前 HEAD 证据闭环 | 可以把最终 HEAD 的 release proof 输入 certification，而不是依赖旧 local-ci 产物。 |
| 最小改动 | 不新增服务、不改变发布流程、不复制 release proof gate。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 当前脚本只从 `evidence_dir / current-release-proof.json` 读取 release proof。 |
| TP-02 | Done | `--current-release-proof-json`、`evidenceOverrides`、`logicalPath/source` 已实现。 |
| TP-03 | Done | 回归测试、契约、路线图和任务索引已同步。 |
| TP-04 | Done | targeted pytest、CLI smoke、ruff、secret scan 和任务文档校验已通过；提交推送待最终 Git 执行。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
