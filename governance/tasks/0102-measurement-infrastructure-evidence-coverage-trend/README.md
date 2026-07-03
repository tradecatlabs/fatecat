# Task Overview
- Task ID: `0102`
- Slug: `measurement-infrastructure-evidence-coverage-trend`
- Objective: `执行 0099 Wave A A3：新增八字/紫微 evidence coverage trend gate，把 rule_depth_registry、classics_rule_index、analysisEvidence、Report evidenceRefs、冲突解释和反证字段纳入 tracked baseline，对覆盖率下降、规则引用断链或证据字段回退 fail-fast；不保存完整报告正文、真实用户资料或外部生产证据。`
- Status: `Done`

## In Scope
- 新增 evidence coverage baseline，记录八字/紫微 evidence items、Report evidenceRefs、appliedRules、conflicts 和 combinationStatements 的最低覆盖门槛。
- 新增 evidence coverage trend contract，声明输入来源、必备检查、禁止保存内容和生产边界。
- 新增本地 gate CLI 和 shell wrapper，复用统一 `CapabilityExecutor` 与 `/capabilities/{capability_id}/calculate` Report envelope。
- 接入 `scripts/local-ci.sh`，让 quick CI 生成 `evidence-coverage-trend-gate.json` 并写入 summary artifact。
- 增加 regression tests，覆盖 baseline pass、严格 baseline fail、规则引用断链 fail 和 CLI 输出。
- 更新目录级 `AGENTS.md`、API 接入文档、100% 路线图和任务索引。

## Out of Scope
- 不修改八字、紫微 provider 计算逻辑。
- 不新增真实命例、真实用户样本或完整报告正文 snapshot。
- 不连接真实生产 API、HF Space、Telegram Bot、OIDC、SIEM、OTel backend、Vault/KMS、registry 或第三方账号。
- 不把本地 evidence coverage 通过解释为预测准确率、专业能力 100%、第三方审计通过或外部 live 完成。
- 不输出 token、secret、DSN、私钥、出生地区、报告正文或真实用户 payload。

## Task Package Tree
```text
TP-01 evidence coverage 需求和 baseline 边界
├── TP-01.01 盘点八字/紫微现有 evidence surface
└── TP-01.02 定义 tracked baseline、contract 和隐私边界
TP-02 evidence coverage gate 实现与接线
├── TP-02.01 实现 CLI/wrapper、coverage metrics 和趋势比较
└── TP-02.02 接入 local-ci summary、AGENTS、API 文档和 roadmap
TP-03 验证与审查
├── TP-03.01 增加 regression tests
└── TP-03.02 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan
TP-04 closeout 与版本控制
├── TP-04.01 同步任务文档、INDEX 和验收清单
└── TP-04.02 提交、推送并记录远端状态
```

## Requirement Alignment
| 用户要求 | 本任务响应 |
| --- | --- |
| “调研，制作实现 100% 基础设施所需完整计划” | 复用 0099 已落盘的 infra 同构调研和 Wave A A3，将计划中的 evidence coverage trend 变成可执行门禁。 |
| “100% 基础设施” | 只把证据覆盖趋势纳入机器门禁，避免聊天结论替代 evidence。 |
| “不得伪造生产完成” | 契约和脚本声明本地 pass 不等于外部 live、预测准确率或第三方审计通过。 |
| “任务树落盘” | 本目录记录完整 TP 树、验收标准、验证命令和 closeout 状态。 |

## Task Package Overview
| Node ID | Title | Outcome |
| --- | --- | --- |
| TP-01 | evidence coverage 需求和 baseline 边界 | 明确 gate 只看结构化证据摘要，不保存真实报告或用户资料。 |
| TP-02 | evidence coverage gate 实现与接线 | 新增 contract、baseline、CLI、local-ci artifact 和文档入口。 |
| TP-03 | 验证与审查 | 用 regression、ruff、quick local-ci、secret scan 和 task validator 证明本地闭环。 |
| TP-04 | closeout 与版本控制 | 任务文档与 Git 交付状态一致。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
