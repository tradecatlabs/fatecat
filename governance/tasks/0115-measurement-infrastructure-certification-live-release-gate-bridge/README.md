# Task Overview
- Task ID: `0115`
- Slug: `measurement-infrastructure-certification-live-release-gate-bridge`
- Objective: `修复 certification aggregator 的 live-release-gate 当前证据时间线盲区：允许显式消费独立生成的 live-release-gate sidecar JSON，同时保持生产 API/HF/Bot 外部 live 阻断语义不变。`
- Status: `Done`

## In Scope
- 为 `scripts/measurement-infrastructure-certification.py` 增加 `live-release-gate.json` sidecar 输入。
- 在 certification summary 的 `evidenceOverrides` 中记录 live release gate override。
- 增加回归测试，证明 live gate sidecar 不会覆盖 current release proof 或 current audit bundle。
- 更新 certification contract、scripts/audit AGENTS、路线图和任务索引。

## Out of Scope
- 不重写 `scripts/live-release-gate.py`。
- 不把生产 API、HF Space、Telegram Bot live smoke 改写成 passed。
- 不把 current live gate sidecar 写回 repo 或 local-ci output dir。
- 不声明 FateCat 已达到 100% 测算基础设施。
- 不读取、输出或保存真实 token、secret、DSN、URL、报告正文或用户输入。

## Task Package Tree
```text
TP-01 live gate 盲区确认
TP-02 certification live gate sidecar 输入落地
TP-03 契约、测试和文档同步
TP-04 验证、自审、提交推送
```

## Future-Optimal Contract
| Field | Value |
| --- | --- |
| Target End State | Certification 可以同时消费最终 live-release-gate、current-release-proof 和 current-audit-bundle sidecar，且每个逻辑证据来源可追踪。 |
| Real Constraints | local-ci live gate 生成时间早于最终 release proof、最终 audit bundle 与最终远端 release evidence；最终 evidence 不能写回 Git，否则制造新 HEAD。 |
| Inertia Constraints | 旧 certification release domain 只从 `evidence_dir/live-release-gate.json` 读取 live gate。 |
| Wrong Concept / Wrong Boundary | 把 local-ci 早期 live gate 当成最终 live release gate。 |
| Kill List | 不新增第二套 live gate 生成器；不复制 release gate 判断逻辑；不把外部 live pending 改写为 passed。 |
| Proof Point | 使用 live gate sidecar 后，release domain 可读取 override source；release proof 与 audit bundle 仍按自身 sidecar 或 evidence dir 独立判断。 |
| Falsifier | 如果 live gate sidecar 能覆盖 `current-release-proof.json` 或 `current-audit-bundle/current-audit-bundle.json`，任务失败。 |
| Migration Slice | 只新增可选 CLI 参数和 override map 条目，默认 local-ci 行为保持兼容。 |
| Rejected Short-Term Patches | 不修改 local-ci 生成顺序；不把 certification 变成 orchestration runner；不硬编码当前临时路径。 |
| Future-Optimal Review Owner | `auto-review` document-drift + future-optimal-drift。 |

## Ponytail Contract
| Field | Value |
| --- | --- |
| Existence Check | 当前 certification 已有两个 sidecar，第三个 release domain 文件存在同类时间线盲区；新增精确 override 比复制证据或改 local-ci 顺序更低成本。 |
| Selected Ladder Rung | 项目原生能力复用：沿用现有 `evidence_overrides` map。 |
| Skipped Scope | 不新增 live gate 规则、不接真实生产凭证、不实现 artifact registry。 |
| Ceiling / Upgrade Path | 若未来 evidence 不再是单 JSON 文件，应升级为 immutable evidence bundle manifest。 |
| Do-not-simplify | 不得弱化 live gate blocked/pending 语义，不得隐藏外部连通验证待执行。 |
| Minimal Runnable Check | targeted pytest + CLI sidecar smoke + task docs validator。 |
| Complexity Review Owner | `auto-review` ponytail-complexity。 |

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 当前提交 live gate 证据可复核 | Certification 可以引用最终 live-release-gate sidecar，而不是只引用 stale local-ci gate。 |
| 不伪造 live | live sidecar 只替换证据路径；生产 API/HF/Bot 缺失时仍 blocked。 |
| 不绕过 release/audit | live sidecar 只覆盖 `live-release-gate.json`。 |
| 最小改动 | 复用 0113/0114 的 evidence override 机制，不新增证据格式。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | Source scan confirmed certification has no `--live-release-gate-json` input before this task. |
| TP-02 | Done | `--live-release-gate-json` and override mapping added. |
| TP-03 | Done | Regression tests, contract, AGENTS, roadmap and task index updated. |
| TP-04 | Done | Targeted pytest, local-ci quick, sidecar smoke, ruff, secret scan and task docs validator passed; Git ship handled by final delivery step. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
