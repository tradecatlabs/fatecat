# AGENTS.md - contracts/fate

## 目录用途

`contracts/fate/` 存放 FateCat 测算基础设施的能力协议、字段、profile、权重和规则深度契约，是输出字段口径的配置真相源。

## 目录结构

```text
contracts/fate/
├── AGENTS.md
├── capabilities/
│   ├── registry.json
│   ├── errors.json
│   ├── schemas/
│   └── profiles/
├── audit/
│   ├── current-bundle.json
│   ├── dry-run.json
│   ├── handoff.json
│   └── AGENTS.md
├── data-supply-chain/
│   ├── registry.json
│   └── schemas/
├── delivery/
│   ├── multi-surface-semantic-diff.json
│   ├── registry.json
│   └── schemas/
├── developer/
│   ├── api-changelog.json
│   ├── developer-portal.json
│   ├── developer-platform.json
│   ├── sandbox-output-snapshot.json
│   ├── sandbox-token-contract.json
│   ├── sdk-release-baseline.json
│   ├── sandbox.json
│   └── AGENTS.md
├── evaluations/
│   ├── registry.json
│   └── schemas/
├── observability/
│   ├── registry.json
│   └── schemas/
├── security/
│   ├── registry.json
│   ├── retention-cleanup.json
│   └── schemas/
├── classics_rule_index.json
├── evidence-coverage-baseline.json
├── evidence-coverage-trend-contract.json
├── evidence_schema.json
├── future_features.json
├── rule_depth_registry.json
├── weight_policy.json
└── profiles/
    └── pure_analysis.json
```

## 职责边界

- `capabilities/`：统一测算能力协议与注册表；默认能力只能是 `bazi`，其他体系必须独立输出或保持 planned。
- `capabilities/registry.json` 的每个能力必须声明 `maturity`、`engine.engineVersion`、`evidencePolicy` 和 `testGate`；这些字段是测算基础设施成熟度、可复现计算和发布门禁的审计入口。
- `capabilities/errors.json`：标准错误码字典，服务层只负责读取和映射，不在业务代码里另起一套错误事实源。
- `audit/`：第三方审计交接契约；只登记 audit handoff bundle 输出结构、证据来源和外部待验证项策略，不保存真实生产证据或用户报告正文。
- `audit/handoff.json`：审计包 generator 的机器真相源；要求 Markdown/JSON 输出完整列出 tracked 和 untracked non-ignored `外部连通验证待执行` occurrence。
- `audit/dry-run.json`：审计包 dry-run verifier 的机器真相源；要求本地预检结构完整，同时在外部 live 证据缺失时保持 ship gate blocked。
- `audit/current-bundle.json`：当前 commit 审计证据包机器真相源；要求聚合 release proof、audit handoff、dry-run、release artifacts、rollback drill、evidence index、risk register 和 pending external validations，并在 required 模式拒绝不完整当前发布证据。
- `data-supply-chain/`：数据、典籍、vendor、benchmark 与导出边界注册表；只登记来源、分层、许可状态、usageRole、productionEligibility、exportPolicy 和验证命令，不保存原始大文件。
- `data-supply-chain/registry.json`：登记 raw/canonical/derived/reference/runtime/export 分层资产；`review_required`、`source_archive_only`、`evaluation_only` 和 `reference_only` 不得被文档写成默认生产输入。
- `delivery/`：多端交付资源注册表，登记 DeliverySurface，只做 FastAPI/Web/Bot/CLI/Skill/HF Space 的入口、同源链路、输出契约和验证边界说明，不保存用户输入或运行态报告。
- `delivery/registry.json`：登记 available/partial/manual surfaces；partial surface 必须说明同源范围和未覆盖输出边界。
- `delivery/multi-surface-semantic-diff.json`：标准 Markdown 多交付面语义一致性 gate 契约；只证明本地 API/Web/Bot dry-run normalized hash 同源，不证明真实 Bot/HF/公网 live。
- `developer/`：开发者接入契约、SDK/package baseline、sandbox fixture、sandbox token contract 与 API changelog；只保存本地可验证的北京/测试样本和发布边界，不保存真实 token、生产 URL、报告正文或真实用户数据。
- `developer/developer-platform.json`：开发者平台机器真相源；登记 OpenAPI、SDK/package baseline、sandbox、API changelog 与 validation gate，不代表 SDK 已发布。
- `developer/developer-portal.json`：开发者门户机器真相源；登记本地 portal release baseline、入口、机器契约和外部未上线边界，不代表公网门户上线。
- `developer/sdk-release-baseline.json`：SDK release-readiness manifest；登记 package candidates、local smoke 和未来 registry publish 证据要求。
- `developer/sandbox-output-snapshot.json`：sandbox 固定输出 hash 与结构断言；只保存脱敏摘要，不保存完整响应正文。
- `developer/api-changelog.json`：API 兼容策略和变更记录；公开 breaking change 必须登记迁移说明和兼容窗口。
- `developer/sandbox-token-contract.json`：未来公网 sandbox token 的 claim/scope/rate-limit/revocation contract；当前不发行真实 token。
- `developer/sandbox.json`：开发者文档 smoke 与 SDK 示例的固定输入源；它不是公网 sandbox token 服务。
- `evaluations/`：评测资源注册表，登记 Dataset 与 EvaluationRun，只做发现、审计和发布门禁说明，不保存运行时评测结果库。
- `evaluations/registry.json`：登记 golden fixture、benchmark 和本地评测运行入口；evaluation-only 数据不得被 production provider 当成业务输入。
- `observability/`：观测资源注册表，登记 ObservabilitySignal，只做 health、ready、metrics、logs、trace/SLO/alert 的发现和边界说明，不保存运行时观测数据。
- `observability/registry.json`：登记 available/planned signals；planned 信号不得被文档写成生产已验证能力。
- `security/`：安全、隐私与发布门禁资源注册表，登记 SecurityControl，只做 token/CORS/限流/请求体/响应头/隐私扫描/source hygiene/release gate/production readiness 的发现和边界说明，不保存真实凭证。
- `security/registry.json`：登记 available/manual controls；需要真实域名、真实 token、Bot live smoke 或云端权限的控制必须标注外部连通验证待执行。
- `security/retention-cleanup.json`：登记本地 SQLite retention cleanup baseline 的命令、summary、smoke 与脱敏边界；不代表生产 scheduler、生产数据库或外部 SIEM retention 已验证。
- `future_features.json`：记录不再进入标准报告、后续需按新功能重新设计契约的候选能力。
- `evidence-coverage-baseline.json`：八字/紫微 evidence coverage trend 的 tracked baseline；只保存覆盖率门槛、计数和隐私边界，不保存报告正文或真实用户资料。
- `evidence-coverage-trend-contract.json`：evidence coverage trend gate 契约；要求 rule depth registry、classics rule index、analysisEvidence、Report evidenceRefs、冲突解释和反证字段不回退。
- `evidence_schema.json`：综合八字机器可读 evidence 字段契约；默认不渲染到 Markdown。
- `weight_policy.json`：综合八字核心、动态、辅助、民俗权重边界。
- `classics_rule_index.json`：典籍规则索引种子，只保存短规则与来源，不保存大段原文。
- `rule_depth_registry.json`：八字/紫微规则深度配置，只保存规则条件、证据字段、冲突策略与风险边界。
- `owner` / `governance.extensionPolicy`：规则和候选能力的变更口径；新增规则必须有来源、适用条件、不适用条件和风险边界，不得写入确定性断语字段。
- `profiles/`：定义某个输出 profile 允许返回哪些字段。
- 这里不放算法代码，不依赖 Telegram / FastAPI / 数据库。
- 新增字段时，先更新这里的 profile，再更新 `domains/fate-analysis/services/fate-core/` 的 provider / usecase。
