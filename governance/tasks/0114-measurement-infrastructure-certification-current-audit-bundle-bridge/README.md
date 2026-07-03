# Task Overview
- Task ID: `0114`
- Slug: `measurement-infrastructure-certification-current-audit-bundle-bridge`
- Objective: `修复 certification aggregator 的 current audit bundle 证据时间线盲区：允许显式消费独立生成的 current-audit-bundle sidecar JSON，同时保持 release/live/certification 外部阻断语义不变。`
- Status: `Done`

## In Scope
- 为 `scripts/measurement-infrastructure-certification.py` 增加 `current-audit-bundle/current-audit-bundle.json` sidecar 输入。
- 在 certification summary 的 `evidenceOverrides` 中记录 current audit bundle override。
- 增加回归测试，证明 audit bundle sidecar 不会覆盖 release domain 的 current release proof 或 live release gate。
- 更新 certification contract、scripts/audit AGENTS、路线图和任务索引。

## Out of Scope
- 不重写 `scripts/current-audit-bundle.py`。
- 不把 current audit bundle 写回 repo 或 local-ci output dir。
- 不声明第三方审计通过。
- 不声明生产 API、HF、Bot、OIDC、SIEM、OTel、Vault/KMS、多副本 runtime 或真实生产 rollback 已完成。
- 不读取、输出或保存真实 token、secret、DSN、URL、报告正文或用户输入。

## Task Package Tree
```text
TP-01 audit bundle 盲区确认
TP-02 certification audit bundle sidecar 输入落地
TP-03 契约、测试和文档同步
TP-04 验证、自审、提交推送
```

## Future-Optimal Contract
| Field | Value |
| --- | --- |
| Target End State | Certification 可以同时消费最终 current-release-proof sidecar 和最终 current-audit-bundle sidecar，且每个逻辑证据来源可追踪。 |
| Real Constraints | local-ci audit bundle 生成时间早于最终远端 release proof；最终 audit bundle 不能写回 Git，否则制造新 HEAD。 |
| Inertia Constraints | 旧 certification audit domain 只从 `evidence_dir/current-audit-bundle/current-audit-bundle.json` 读取。 |
| Kill List | 不新增第二套审计包生成器；不复制 audit bundle 逻辑；不把第三方审计或外部 live 改写为 passed。 |
| Proof Point | 使用 audit bundle sidecar 后，audit domain 可读取 override source；release domain 仍按自身证据独立判断。 |
| Falsifier | 如果 audit bundle sidecar 能覆盖 `current-release-proof.json` 或 `live-release-gate.json`，任务失败。 |
| Migration Slice | 只新增可选 CLI 参数和 override map 条目，默认 local-ci 行为保持兼容。 |

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 当前提交审计证据可复核 | Certification 可以引用最终 audit bundle sidecar，而不是只引用 stale local-ci bundle。 |
| 不伪造 live | Release/live gate 仍由各自逻辑文件独立判断。 |
| 不伪造第三方审计 | audit bundle sidecar 只代表证据包生成，不代表外部审计完成。 |
| 最小改动 | 复用 0113 的 evidence override 机制，不新增服务或新证据格式。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | local-ci current audit bundle 引用旧 `current-release-proof.json`，commit 为旧 HEAD。 |
| TP-02 | Done | `--current-audit-bundle-json` 与 audit bundle override 映射已实现。 |
| TP-03 | Done | 回归测试、契约、AGENTS、路线图和任务索引已同步。 |
| TP-04 | Done | targeted pytest、sidecar smoke、ruff、secret scan 和任务文档校验已通过；提交推送待最终 Git 执行。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
