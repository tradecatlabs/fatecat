# Task Overview
- Task ID: `0103`
- Slug: `measurement-infrastructure-current-audit-bundle-refresh`
- Objective: `执行 0099 Wave A A4：基于最新 commit 重新聚合 current audit bundle，并让审计证据包显式纳入 local-ci gate artifact 摘要，尤其是 0102 新增的 evidence coverage trend gate；输出 audit markdown/json、evidence index、risk register 和 external pending list，不伪造外部 live 或第三方审计完成。`
- Status: `Done`

## In Scope
- 为 `current-audit-bundle.py` 增加 `--local-ci-output-dir`，从 local-ci output dir 读取 gate artifact 摘要。
- 将 `evidence-coverage-trend-gate.json` 作为独立 evidence item 写入 current audit bundle evidence index。
- 更新 local-ci 调用、current bundle contract、目录级 `AGENTS.md` 和回归测试。
- 基于当前 HEAD 重新生成 current audit bundle，确认 auditGate 在 local mode 下如实 blocked，而不是伪造 100% 或外部 live。
- 更新路线图和任务索引，记录 A4 本地切片状态。

## Out of Scope
- 不连接真实生产 API、HF Space、Telegram Bot、OIDC、SIEM、OTel backend、Vault/KMS、registry 或第三方账号。
- 不把本地 blocked audit bundle 写成第三方审计通过。
- 不新增完整报告正文、真实用户输入、真实生产日志 payload 或敏感凭证输出。
- 不重写 audit handoff、dry-run、current release proof、release artifacts 或 rollback drill 的既有语义。

## Task Package Tree
```text
TP-01 current audit bundle 需求和证据边界
├── TP-01.01 盘点当前 bundle 输入和 0102 evidence artifact 缺口
└── TP-01.02 定义 local-ci gate artifact 纳入策略和 non-claim
TP-02 current audit bundle 刷新实现与接线
├── TP-02.01 实现 local-ci output dir artifact evidence
└── TP-02.02 接入 local-ci、contract、AGENTS、tests 和 roadmap
TP-03 验证与审查
├── TP-03.01 增加/更新 regression tests
└── TP-03.02 执行 focused tests、bundle generation、ruff、secret scan 和必要 local-ci
TP-04 closeout 与版本控制
├── TP-04.01 同步任务文档、INDEX 和验收清单
└── TP-04.02 提交、推送并记录远端状态
```

## Requirement Alignment
| 用户要求 | 本任务响应 |
| --- | --- |
| “任务树全部推进” | 继续执行 0099 Wave A A4，并创建 0103 可验证任务包。 |
| “100% 基础设施” | 增强审计证据包，让 0102 evidence coverage gate 能进入第三方可复核 evidence index。 |
| “不伪造生产完成” | auditGate 保持 local blocked，外部 live 与第三方审计仍明确 pending。 |
| “可落地、可验收” | 以 current audit bundle JSON/Markdown、evidence index 和 regression tests 作为证据。 |

## Task Package Overview
| Node ID | Title | Outcome |
| --- | --- | --- |
| TP-01 | current audit bundle 需求和证据边界 | 明确 A4 是审计包刷新，不是外部 live 或第三方审计。 |
| TP-02 | current audit bundle 刷新实现与接线 | local-ci gate artifact 可进入 evidence index。 |
| TP-03 | 验证与审查 | current bundle regression、生成命令、ruff、secret scan 形成证据。 |
| TP-04 | closeout 与版本控制 | 任务文档与 Git 交付状态一致。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
