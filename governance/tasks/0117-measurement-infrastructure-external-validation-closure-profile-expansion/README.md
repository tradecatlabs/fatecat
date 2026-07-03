# Task Overview
- Task ID: `0117`
- Slug: `measurement-infrastructure-external-validation-closure-profile-expansion`
- Objective: `扩展 external validation closure gate 的自动分类 profile，把 0116 中大量 manual_triage 的政策、provider、evaluation、event、runtime、release、certification 类 occurrence 自动映射到可分派 owner，同时保留真正未知项为 manual_triage。`
- Status: `Done`

## In Scope
- 扩展 `scripts/external-validation-closure-gate.py` 的 closure profiles。
- 增加回归测试，证明新类别可自动分类且未知项仍进入 `manual_triage`。
- 更新 roadmap 和任务索引。
- 验证 closure gate 输出仍保持 `shipGate.status=blocked`，不伪造外部 live。

## Out of Scope
- 不连接真实外部系统。
- 不关闭任何生产 API、Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 或第三方审计 live 阻断。
- 不把 policy guardrail 写成 live passed evidence。

## Task Package Tree
```text
TP-01 manual triage 剩余项分析
TP-02 closure profile 扩展
TP-03 回归测试和 smoke 验证
TP-04 文档、任务索引和交付
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 降低人工分派噪音 | manual triage 目标从 184 降到接近仅保留真实未知项。 |
| 不吞未知项 | 回归测试保留一个未知样例，必须继续输出 `manual_triage`。 |
| 不伪造 live | ship gate 仍 blocked。 |
| 可审计 | 新类别均有 owner、credential dependencies、required evidence 和 verification commands。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | Manual triage sampled from 0116 local-ci artifact. |
| TP-02 | Done | Profiles added for delivery/event/provider/evaluation/runtime/security/release/governance. |
| TP-03 | Done | Ruff, format, focused pytest, closure smoke and secret scan passed. |
| TP-04 | Done | Task docs decompose gate passed; git delivery handled by follow-up version-control step. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
