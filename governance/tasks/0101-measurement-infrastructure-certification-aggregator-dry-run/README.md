# Task Overview
- Task ID: `0101`
- Slug: `measurement-infrastructure-certification-aggregator-dry-run`
- Objective: `执行 0099 Wave A A2：新增 100% 测算基础设施 certification aggregator dry-run，聚合 local-ci 产物中的 release、audit、provider trend、core quality、security、SRE、runtime、developer 和 external pending 证据，输出 passed/blocked/pending/in-progress 分域结论；默认不得把本地 dry-run 或 pending external live 伪装成 100% 完成。`
- Status: `Done`

## In Scope
- 新增 `MeasurementInfrastructureCertification` 契约，声明必备 local-ci evidence 文件、输出字段、禁止声明和隐私边界。
- 新增 certification aggregator dry-run CLI，聚合 provider、core quality、event、developer、security/privacy、observability/SRE、runtime、release、audit 九个分域。
- 接入 `scripts/local-ci.sh`，让 quick CI 生成 `measurement-infrastructure-certification.json` 并写入 summary artifact。
- 补 regression tests，覆盖 blocked dry-run、require-certified 拒绝、缺证据失败和合成全通过路径。
- 更新目录级 `AGENTS.md`、API 接入文档、100% 路线图和任务索引。

## Out of Scope
- 不连接真实生产 API、HF Space、Telegram Bot、OIDC、SIEM、OTel backend、Vault/KMS、registry 或第三方账号。
- 不把 `blocked`、`pending` 或本地 dry-run 结果包装成 100% 基础设施完成。
- 不修改八字、紫微或其他 capability 的计算逻辑。
- 不替代第三方审计，只生成可供审计前自检的本地聚合证据。
- 不输出 token、secret、DSN、私钥、出生地区、报告正文或真实用户 payload。

## Task Package Tree
```text
TP-01 certification 需求和契约边界
├── TP-01.01 盘点 local-ci 现有 gate evidence 与不可声明边界
└── TP-01.02 定义 certification contract、必备证据和分域状态
TP-02 certification aggregator 实现与接线
├── TP-02.01 实现 CLI/wrapper、分域聚合、blocked/pending/failed 语义
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
| “调研，制作实现 100% 基础设施所需完整计划” | 复用 0099 已落盘的 infra 同构调研和 Wave A A2，将计划中的 certification aggregator 变成可执行门禁。 |
| “100% 基础设施” | 用机器可读 aggregator 明确哪些域 passed、blocked、pending、failed，避免聊天结论替代证据。 |
| “不得伪造生产完成” | 契约和脚本默认在外部 live/release/audit 未闭合时输出 `blocked`，`canClaim100Percent=false`。 |
| “任务树落盘” | 本目录记录完整 TP 树、验收标准、验证命令和 closeout 状态。 |

## Task Package Overview
| Node ID | Title | Outcome |
| --- | --- | --- |
| TP-01 | certification 需求和契约边界 | 明确 aggregator 只消费 local-ci 证据，不连接外部系统，不声明 100%。 |
| TP-02 | certification aggregator 实现与接线 | 新增 contract、CLI、local-ci artifact 和文档入口。 |
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
