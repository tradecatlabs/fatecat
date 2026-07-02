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
├── data-supply-chain/
│   ├── registry.json
│   └── schemas/
├── delivery/
│   ├── registry.json
│   └── schemas/
├── developer/
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
│   └── schemas/
├── classics_rule_index.json
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
- `data-supply-chain/`：数据、典籍、vendor、benchmark 与导出边界注册表；只登记来源、分层、许可状态、usageRole、productionEligibility、exportPolicy 和验证命令，不保存原始大文件。
- `data-supply-chain/registry.json`：登记 raw/canonical/derived/reference/runtime/export 分层资产；`review_required`、`source_archive_only`、`evaluation_only` 和 `reference_only` 不得被文档写成默认生产输入。
- `delivery/`：多端交付资源注册表，登记 DeliverySurface，只做 FastAPI/Web/Bot/CLI/Skill/HF Space 的入口、同源链路、输出契约和验证边界说明，不保存用户输入或运行态报告。
- `delivery/registry.json`：登记 available/partial/manual surfaces；partial surface 必须说明同源范围和未覆盖输出边界。
- `developer/`：开发者接入契约与 sandbox fixture；只保存本地可验证的北京/测试样本，不保存真实 token、生产 URL、报告正文或真实用户数据。
- `developer/sandbox.json`：开发者文档 smoke 与 SDK 示例的固定输入源；它不是公网 sandbox token 服务。
- `evaluations/`：评测资源注册表，登记 Dataset 与 EvaluationRun，只做发现、审计和发布门禁说明，不保存运行时评测结果库。
- `evaluations/registry.json`：登记 golden fixture、benchmark 和本地评测运行入口；evaluation-only 数据不得被 production provider 当成业务输入。
- `observability/`：观测资源注册表，登记 ObservabilitySignal，只做 health、ready、metrics、logs、trace/SLO/alert 的发现和边界说明，不保存运行时观测数据。
- `observability/registry.json`：登记 available/planned signals；planned 信号不得被文档写成生产已验证能力。
- `security/`：安全、隐私与发布门禁资源注册表，登记 SecurityControl，只做 token/CORS/限流/请求体/响应头/隐私扫描/source hygiene/release gate/production readiness 的发现和边界说明，不保存真实凭证。
- `security/registry.json`：登记 available/manual controls；需要真实域名、真实 token、Bot live smoke 或云端权限的控制必须标注外部连通验证待执行。
- `future_features.json`：记录不再进入标准报告、后续需按新功能重新设计契约的候选能力。
- `evidence_schema.json`：综合八字机器可读 evidence 字段契约；默认不渲染到 Markdown。
- `weight_policy.json`：综合八字核心、动态、辅助、民俗权重边界。
- `classics_rule_index.json`：典籍规则索引种子，只保存短规则与来源，不保存大段原文。
- `rule_depth_registry.json`：八字/紫微规则深度配置，只保存规则条件、证据字段、冲突策略与风险边界。
- `owner` / `governance.extensionPolicy`：规则和候选能力的变更口径；新增规则必须有来源、适用条件、不适用条件和风险边界，不得写入确定性断语字段。
- `profiles/`：定义某个输出 profile 允许返回哪些字段。
- 这里不放算法代码，不依赖 Telegram / FastAPI / 数据库。
- 新增字段时，先更新这里的 profile，再更新 `domains/fate-analysis/services/fate-core/` 的 provider / usecase。
