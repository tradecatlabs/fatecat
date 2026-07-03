# 测算基础设施 API 接入

本文是 FateCat 面向 Agent 与应用开发者的最小接入说明。当前生产默认报告只支持综合八字 `bazi`，其他生产或规划体系必须通过独立 capability 调用，不得混入默认 Markdown。

## 发现入口

| 入口 | 方法 | 用途 |
| --- | --- | --- |
| `/metadata` | GET | 服务定位、开发者入口、质量门禁、隐私口径 |
| `/openapi.json` | GET | FastAPI OpenAPI 机器契约 |
| `/docs` | GET | 本地交互式 API 文档 |
| `/capabilities` | GET | 统一 capability 注册表 |
| `/capabilities/{capability_id}` | GET | 单个 capability 资源详情、schema、links、准入状态 |
| `/capabilities/{capability_id}/calculate` | POST | 执行生产化 capability |
| `/sandbox/capabilities/{capability_id}/calculate` | POST | 本地 sandbox gateway，验证 sandbox token scope 后执行白名单 capability |
| `/providers` | GET | production provider 资源注册表 |
| `/providers/{provider_id}` | GET | 单个 Provider resource 详情、metadata、health、links |
| `/evaluations` | GET | Dataset 与 EvaluationRun 评测资源注册表 |
| `/evaluations/{evaluation_id}` | GET | 单个 Dataset 或 EvaluationRun 资源详情 |
| `/observability` | GET | health、ready、metrics、logs、planned trace/SLO 观测资源注册表 |
| `/observability/{signal_id}` | GET | 单个 ObservabilitySignal 资源详情 |
| `/security` | GET | token、CORS、限流、隐私、source hygiene、release gate、production readiness 安全控制注册表 |
| `/security/{control_id}` | GET | 单个 SecurityControl 资源详情 |
| `/surfaces` | GET | Web、FastAPI、Telegram Bot、CLI、Agent Skill、托管 Web 交付面注册表 |
| `/surfaces/{surface_id}` | GET | 单个 DeliverySurface 资源详情 |
| `/reports` | GET | 报告 profile、Markdown、异步 job 入口 |
| `/api/v1/report/jobs` | POST | 提交异步 Markdown 报告任务，支持 `Idempotency-Key` |
| `/api/v1/report/jobs/{job_id}` | GET | 查询异步报告任务状态 |
| `/api/v1/report/jobs/{job_id}/cancel` | POST | 取消异步报告任务 |
| `/errors` | GET | 标准错误码字典 |
| `/health` | GET | 存活检查 |
| `/ready` | GET | 数据库与 capability registry 就绪检查 |
| `/metrics` | GET | Prometheus 文本指标 |

## 开发者 OpenAPI 与 Sandbox

本地 OpenAPI 导出：

```bash
bash scripts/export-openapi.sh \
  --output infra/runtime/local-state/exports/developer/openapi.json
```

开发者 sandbox fixture 位于：

```text
contracts/fate/developer/sandbox.json
```

当前 sandbox 只提供本地、确定性、隐私安全的北京/测试样本，用于 docs smoke 与 SDK 示例，不代表已经存在公网 sandbox token 服务。

开发者平台机器契约：

```text
contracts/fate/developer/developer-platform.json
contracts/fate/developer/developer-portal.json
```

SDK/package baseline、SDK release baseline、sandbox token contract、fixed snapshot 与 API changelog：

```text
docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md
docs/reference-materials/developer/SDK_RELEASE_BASELINE.md
contracts/fate/developer/sdk-release-baseline.json
contracts/fate/developer/sandbox-access-gateway.json
contracts/fate/developer/sandbox-output-snapshot.json
contracts/fate/developer/sandbox-token-contract.json
contracts/fate/developer/api-changelog.json
docs/reference-materials/developer/API_CHANGELOG.md
```

当前只是本地开发者平台与 SDK release-readiness baseline；不代表 PyPI/npm SDK 已发布，也不代表公网 developer portal 或 sandbox token 服务已上线。

本地开发者文档 smoke：

```bash
bash scripts/developer-docs-smoke.sh \
  --output-json infra/runtime/local-state/exports/developer/docs-smoke.json \
  --openapi-json infra/runtime/local-state/exports/developer/openapi.json
```

本地开发者平台 gate：

```bash
bash scripts/developer-platform-gate.sh \
  --output-json infra/runtime/local-state/exports/developer/developer-platform-gate.json
```

本地开发者门户与 SDK release baseline gate：

```bash
bash scripts/developer-portal-gate.sh \
  --output-json infra/runtime/local-state/exports/developer/developer-portal-gate.json
```

本地 sandbox access gateway gate：

```bash
bash scripts/sandbox-access-gateway-gate.sh \
  --output-json infra/runtime/local-state/exports/developer/sandbox-access-gateway-gate.json
```

该 gate 会临时设置环境变量形式的本地 smoke token，验证缺 token 拒绝、错 scope 拒绝、白名单 capability 执行、限流和 audit 脱敏。它不代表公网 sandbox token issuer、revocation service 或生产 API gateway 已上线。

SDK 与 Agent 示例位于：

```text
docs/reference-materials/developer/examples/
```

示例只使用 `http://127.0.0.1:8001`、北京和测试样本；不得写入真实 token、生产 URL、真实用户输入或报告正文。

## Capability 调用

```bash
curl -sS http://127.0.0.1:8001/capabilities \
  | jq '.data.capabilities[] | {capabilityId,status,defaultVisibility,maturity,testGate}'
```

```bash
curl -sS http://127.0.0.1:8001/capabilities/bazi \
  | jq '.data | {resourceType,capabilityId,status,admission,provider,schemas,links}'
```

```bash
curl -sS http://127.0.0.1:8001/providers \
  | jq '.data.providers[] | {providerId,engineVersion,capabilities,health}'
```

```bash
curl -sS http://127.0.0.1:8001/providers/fate_core.usecases.calculate_pure_analysis \
  | jq '.data | {resourceType,providerId,engineVersion,interfaceVersion,health,links}'
```

```bash
curl -sS -X POST http://127.0.0.1:8001/capabilities/almanac/calculate \
  -H 'Content-Type: application/json' \
  -d '{"dateRange":{"start":"2026-05-08","end":"2026-05-08"},"eventType":"出行","place":"北京"}'
```

本地 sandbox gateway 调用示例：

```bash
export FATE_SANDBOX_TOKENS='sandbox-test-user:<local-smoke-token>:capability:calculate:almanac'

curl -sS -X POST http://127.0.0.1:8001/sandbox/capabilities/almanac/calculate \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <local-smoke-token>' \
  -d '{"dateRange":{"start":"2026-05-08","end":"2026-05-08"},"eventType":"出行","place":"北京"}'
```

`FATE_SANDBOX_TOKENS` 仅用于本地 smoke，格式为 `subject:<local-smoke-credential>:scope1|scope2`；不得把本地凭证当成公网发行证据或生产密钥治理证据。

返回结构固定包含：

| 字段 | 含义 |
| --- | --- |
| `capabilityId` | 执行的能力 ID |
| `status` | 能力生产状态 |
| `reportProfile` | 输出 profile |
| `data` | 盘面或计算结果 |
| `evidence` | 证据字段与规则 ID |
| `risk` | 免责声明和禁止断语边界 |
| `metadata` | maturity、engine、provider、evidencePolicy、testGate |
| `report` | Report resource envelope，包含 profile、formats、sections、evidenceRefs、policyGate、links |

生产 capability 的 `provider` / `metadata.provider` 固定包含 `providerId`、`engineVersion`、`deterministic`、`interfaceVersion`、`adapterType`、`versionLock`、`lifecycle`、`sourcePolicy`、`licensePolicy`、`resourceManifest`、`promotionGate`、`deprecation` 与进程内 `health`。当前 provider health 只代表本地 usecase adapter 可用，不代表真实外部域名、token、Bot、webhook 或第三方外部依赖连通验证完成。

`/providers` 只列 production provider registry 中的 provider；planned capability 的 `planned.*` provider 只在 capability registry 中作为未来能力登记，不会出现在 production Provider resource 集合。

Provider lifecycle gate：

```bash
bash scripts/provider-lifecycle-gate.sh \
  --output-json infra/runtime/local-state/exports/providers/lifecycle-gate.json
```

该 gate 会验证：

| 检查 | 含义 |
| --- | --- |
| production provider coverage | 每个 `production` capability 必须有且只能有一个 production provider。 |
| versionLock | `engineVersion`、`interfaceVersion`、`deterministic` 必须与 provider resource 一致。 |
| sourcePolicy | provider 必须声明 source refs 与 supply-chain refs，自研代码只能作为 adapter/usecase 编排。 |
| licensePolicy | provider 必须声明许可证、生产使用许可、分发许可和证据路径。 |
| resourceManifest | provider 必须登记 runtime、contract、test 和供应链引用。 |
| promotionGate | provider 必须声明本地 promotion 验证命令，且 status 为 `passing`。 |
| deprecation | provider 必须有 active/deprecated 策略；deprecated 时必须有 replacement 或 removal window。 |

Provider dependency smoke：

```bash
bash scripts/provider-dependency-smoke.sh \
  --output-json infra/runtime/local-state/exports/providers/dependency-smoke.json
```

该 smoke 通过统一 `CapabilityExecutor` 和脱敏固定样例执行每个 production capability 的 `validate/calculate` 链路，验证 provider 的本地依赖、样例输入、输出关键字段和 evidence 最小结构。它不访问公网、不读取真实 `.env`、token、secret、DSN 或生产账号。

Provider drift scanner：

```bash
bash scripts/provider-drift-scanner.sh \
  --output-json infra/runtime/local-state/exports/providers/drift-report.json
```

该 scanner 会复用 provider lifecycle gate、dependency smoke、本地 `provider.validate` / `provider.calculate` trace span 和 `vendor_sources.json`，输出 dependency/source/license drift report。任何 production provider 缺失 source refs、license evidence、vendor production permission、dependency smoke 结果或 provider trace span，都会形成 drift finding 并阻断本地门禁。它不连接外部 trace backend、不访问真实公网依赖、不读取真实 `.env`、token、secret、DSN 或生产账号。

Provider drift trend gate：

```bash
bash scripts/provider-drift-trend-gate.sh \
  --output-json infra/runtime/local-state/exports/providers/drift-trend.json
```

该 gate 会复用当前 provider drift scanner 输出，并对比 `contracts/fate/capabilities/provider-drift-baseline.json` 中的 provider/source/license/vendor 指纹。任何 provider 集合变化、source refs 变化、license evidence/许可状态回退、vendor snapshot hash 漂移或 scanner finding 未清零，都会形成 trend finding 并阻断本地门禁。合法的 provider 依赖升级或 license/source 变化必须在同一个受审变更中显式更新 baseline。

当前已完成本地 provider lifecycle baseline、本地 dependency smoke baseline、provider drift scanner baseline 和 provider/source/license drift trend baseline；真实公网外部依赖 live smoke、许可证人工法律复核和跨版本升级策略仍是后续任务。

## 测算基础设施认证 dry-run

100% 测算基础设施认证聚合器：

```bash
bash scripts/measurement-infrastructure-certification.sh \
  --evidence-dir <local-ci-output-dir> \
  --output-json infra/runtime/local-state/exports/certification/measurement-infrastructure-certification.json
```

该聚合器只消费 local-ci 产物目录中的机器可读 gate summary，覆盖 provider、core quality、event、developer、security/privacy、observability/SRE、runtime、release 和 audit 九个分域。缺少必备证据时输出 `failed`；release/audit/live evidence 未闭合时输出 `blocked` 或 `pending`，并保持 `certificationGate.canClaim100Percent=false`。只有所有分域均 `passed` 时，才允许配合 `--require-certified` 作为 100% 基础设施声明前置证据。

它不连接真实外部系统，不读取真实 `.env`、token、secret、DSN 或生产账号，不复制报告正文、出生地区或用户 payload；真实 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/多副本 live 仍需要独立外部连通验证。

## 数据供应链门禁

数据、典籍、vendor、benchmark 与导出边界的机器契约位于：

```text
contracts/fate/data-supply-chain/registry.json
contracts/fate/data-supply-chain/schemas/data-supply-chain.schema.json
```

本地供应链门禁：

```bash
bash scripts/data-supply-chain-gate.sh \
  --output-json infra/runtime/local-state/exports/supply-chain/data-supply-chain-gate.json
```

该 gate 会验证：

| 检查 | 含义 |
| --- | --- |
| registry assets | 每个资产必须声明 raw/canonical/derived/reference/runtime/export 分层、usageRole、状态、隐私边界、生产资格和导出策略。 |
| canonical classics | `classics/*.txt` 必须同时进入 `source_manifest.tsv` 与 `copyright_review.tsv`，并且 bytes / sha256 与文件一致。 |
| solar terms source manifest | 原始交节时间表只通过 source manifest 追溯，不读取私有 raw 文件。 |
| vendor production dependency | `vendor_sources.json` 中 production dependency 必须是 SPDX license 且 `productionUseAllowed=true`。 |

该 gate 不提供法律意见，不生成 SBOM/provenance，不证明外部 raw 资料可公开分发，也不改变 production provider 算法或运行时依赖。

八字/紫微 L4 golden evidence smoke：

```bash
bash scripts/bazi-ziwei-l4-golden-smoke.sh \
  --profile quick \
  --output-json infra/runtime/local-state/exports/golden/bazi-ziwei-l4.json
```

该 smoke 复用仓库内匿名北京/测试 fixture，通过统一 `CapabilityExecutor` 和 Markdown API 同时验证：

| 检查 | 含义 |
| --- | --- |
| 八字矩阵代表样本 | 覆盖节气边界、早晚子时代表样本、起运日期、规则深度字段。 |
| 八字规则深度 | 验证格局、强弱、规则 ID、组合主题、冲突解释和反证字段。 |
| 八字断语样本 | 验证默认综合八字关键 evidence rules 不断链。 |
| 紫微 golden | 验证十二宫、命身宫、四化、运限链接和规则 ID。 |
| 紫微规则深度 | 验证星曜组合、四化/运限主题、冲突解释和反证字段。 |
| Markdown profile gate | 验证 `bazi` 与 `ziwei` Markdown 的 `policyGate` 与 `snapshotGate`。 |

`--profile quick` 只执行代表样本，进入本地 quick CI；`--profile full` 执行当前 fixture 全量样本，适合作为发布前加严检查。该 smoke 不读取真实用户、不新增真实命例、不锁定全文断语正文、不宣称八字/紫微专业能力 100%。

`report.evidenceRefs` 是从原始 `evidence` 中抽取的可跳转引用摘要；它不替代完整 `evidence`。

`report.policyGate` 是当前 capability Report envelope 的最小禁止性断语门禁：它使用 `risk.forbiddenClaims` 作为策略来源，扫描 `report.sections` 和 `report.metadata` 摘要字段，并显式排除 `risk.forbiddenClaims` 清单自身，避免风险清单自触发。Markdown 成功结果另有正文 `policyGate` 与 heading `snapshotGate`；完整全文 golden diff、阈值和人工审核仍属于后续发布门禁。

## 评测资源入口

```bash
curl -sS http://127.0.0.1:8001/evaluations \
  | jq '.data.resources[] | {id,resourceType,localAvailability,metadata}'
```

```bash
curl -sS http://127.0.0.1:8001/evaluations/run.local_ci_quick \
  | jq '.data | {resourceType,id,runType,gateType,datasetIds,commands,releaseRequired,lastKnownStatusPolicy}'
```

`/evaluations` 当前只做资源发现和审计说明，不启动评测任务，不内联大型 golden 文件，也不返回 benchmark 标准答案。核心字段：

| 字段 | 含义 |
| --- | --- |
| `Dataset` | 历法、八字、紫微、benchmark 等评测数据资产索引 |
| `EvaluationRun` | 本地回归、golden、benchmark 或 release gate 的可复现运行入口 |
| `usageRole` | 当前均为 `evaluation_only`，不得作为 production provider 业务输入 |
| `localAvailability` | `tracked_in_repo` 可本地直接验证；`requires_reference_repo` 依赖本地参考仓 |
| `lastKnownStatusPolicy` | registry 不伪造当前 commit 运行结果，真实结果来自任务 evidence、CI 或本地命令 |

本地执行入口由 runner 负责，不通过 API 启动：

```bash
bash scripts/run-evaluations.sh \
  --run-id run.solar_terms_golden \
  --output-json infra/runtime/local-state/exports/evaluations/solar-terms-summary.json
```

```bash
bash scripts/run-evaluations.sh \
  --all-local-required \
  --output-json infra/runtime/local-state/exports/evaluations/local-required-summary.json
```

runner 默认选择 `releaseRequired=true` 且 `localAvailability=tracked_in_repo` 的本地必跑集合，输出 summary JSON。它只白名单执行 `bash scripts/*.sh` 和 `python -m pytest`，不使用 `shell=True`；`requires_reference_repo` 的可选 benchmark 必须显式追加 `--allow-reference-repo`。

如需把本地结果留痕并更新 latest 指针：

```bash
bash scripts/run-evaluations.sh \
  --run-id run.solar_terms_golden \
  --record-history \
  --output-json infra/runtime/local-state/exports/evaluations/solar-terms-summary.json
```

如需比较两次本地结果并按 policy 判定是否回归：

```bash
bash scripts/compare-evaluations.sh \
  --baseline-json infra/runtime/local-state/exports/evaluations/history/latest.json \
  --current-json infra/runtime/local-state/exports/evaluations/solar-terms-summary.json \
  --output-json infra/runtime/local-state/exports/evaluations/diff.json
```

diff policy 位于 `contracts/fate/evaluations/diff-policy.json`。当前策略只允许 0 个新增失败、0 个缺失 run、0 个失败命令；它只比较 run 状态与命令 exit code，不解析 benchmark 标准答案。

如需生成本地静态 HTML dashboard：

```bash
bash scripts/evaluation-dashboard.sh \
  --summary-json infra/runtime/local-state/exports/evaluations/local-required-summary.json \
  --output-html infra/runtime/local-state/exports/evaluations/dashboard/index.html
```

如需执行本地 nightly baseline、保留 history/latest、生成 diff 和 dashboard artifact：

```bash
bash scripts/evaluation-nightly.sh \
  --output-dir infra/runtime/local-state/exports/evaluations/nightly/manual
```

dashboard 只展示 summary、run、命令、exit code、duration 和 diff 摘要；不展示 stdout/stderr tail、benchmark 标准答案、报告正文、真实 token、secret、DSN 或真实用户输入。GitHub 定时入口为 `.github/workflows/evaluation-nightly.yml`，仅上传 artifact，不自动部署，不访问真实生产凭证。

MingLi-Bench 被登记为 offline/evaluation_only benchmark：`bash scripts/mingli-bench-gate.sh --year 2025 --sample 5` 不联网，输出脱敏聚合 gate summary；`run-mingli-bench.sh` 和 `generate-mingli-predictions.sh` 仍可用于本地临时 prompt/predictions/accuracy 调试，但逐题结果和 benchmark 标准答案不得进入 CI、dashboard 或生产报告。

## 观测资源入口

```bash
curl -sS http://127.0.0.1:8001/observability \
  | jq '.data.signals[] | {id,signalType,status,endpoint,externalConnectivity}'
```

```bash
curl -sS http://127.0.0.1:8001/observability/signal.http_request_metrics \
  | jq '.data | {resourceType,id,fields,privacyBoundary,localVerification}'
```

`/observability` 当前只做观测信号发现和审计说明，不返回真实日志、指标快照、请求体、用户输入或 trace 数据。核心字段：

| 字段 | 含义 |
| --- | --- |
| `ObservabilitySignal` | health、readiness、metric、log、trace、SLO、alert 等观测信号 |
| `signalType` | `health` / `readiness` / `metric` / `log` / `trace` / `slo` / `alert` |
| `status` | `available` 表示本地已有端点或验证命令；`planned` 表示只做路线登记 |
| `fields` | 当前信号暴露的字段或指标名 |
| `privacyBoundary` | 该信号不得包含的敏感内容边界 |
| `externalConnectivity` | 是否需要 collector、生产流量或外部监控平台 |

当前 available signals 包括 `/health`、`/ready`、HTTP 请求指标、report job/Bot 队列指标、`X-Request-ID`、`traceparent` / `X-Trace-ID`、结构化 JSON 日志字段、本地 API/provider/report span 日志、SLO policy 和 alert rules。外部 OpenTelemetry exporter/collector、trace backend、Prometheus/Alertmanager、生产监控平台和真实生产流量 error budget 仍是外部连通验证待执行。

本地观测 smoke：

```bash
bash scripts/observability-smoke.sh \
  --output-json infra/runtime/local-state/exports/observability/smoke.json
```

该 smoke 使用 FastAPI `TestClient` 验证 `/health`、`/ready`、`/metrics`、`X-Request-ID` 回传、结构化 `http_request` 日志字段、`traceId` 字段和 `/observability` registry metadata。它不接入 OpenTelemetry collector、dashboard、生产监控平台，也不保存真实日志、请求体或用户数据。

本地 trace/SLO/alert smoke：

```bash
bash scripts/observability-trace-slo-smoke.sh \
  --output-json infra/runtime/local-state/exports/observability/trace-slo-smoke.json
```

本地 SLO/alert policy gate：

```bash
bash scripts/observability-slo-gate.sh \
  --output-json infra/runtime/local-state/exports/observability/slo-gate.json
```

当前 trace baseline 使用 W3C `traceparent` 和 OpenTelemetry 语义兼容的本地结构化 span 日志，覆盖 `http.request`、`capability.execute`、`provider.validate`、`provider.calculate`、`report.calculate` 和 `report.render_markdown`。Span 只允许记录 trace/span ID、span 名称、耗时、状态、错误类别和白名单聚合属性；不得记录用户出生信息、报告正文、token、secret 或 DSN。

OTel collector / SLO adapter dry-run contract gate：

```bash
bash scripts/otel-collector-slo-gate.sh \
  --output-json infra/runtime/local-state/exports/observability/otel-collector-slo-gate.json
```

0064 新增 `contracts/fate/observability/otel-collector.dry-run.yaml` 和 `contracts/fate/observability/slo-evidence-contract.json`，用于描述 OTLP receiver、memory/batch/resource processors、debug/prometheus exporter、traces/metrics/logs pipelines、dry-run evidence 和 live evidence pending 清单。该 gate 只解析本地 YAML/JSON contract，并复用本地 SLO/alert policy gate；它不启动真实 OpenTelemetry Collector，不连接 trace backend、metrics backend、Alertmanager、Grafana、PagerDuty 或云监控，也不证明真实生产流量 error budget 已计算。

OTel backend / SLO staged evidence gate：

```bash
bash scripts/otel-backend-slo-gate.sh \
  --output-json infra/runtime/local-state/exports/observability/otel-backend-slo-gate.json
```

0082 新增 `contracts/fate/observability/otel-backend-slo-evidence-contract.json`，用于描述外部 collector runtime、trace backend、metrics backend、SLO dashboard、alert route、production traffic window、error budget 和 incident drill 的脱敏 proof refs。该 gate 默认只输出 `外部连通验证待执行`，并拒绝 localhost、placeholder、raw URL、token/secret、生产指标快照、trace payload 或缺失关键 proof 的伪证；它不连接真实监控平台，也不证明 production SLO、alert live 或 incident drill 已完成。

## 安全控制资源入口

```bash
curl -sS http://127.0.0.1:8001/security \
  | jq '.data.controls[] | {id,controlType,status,externalConnectivity}'
```

```bash
curl -sS http://127.0.0.1:8001/security/control.production_readiness_external \
  | jq '.data | {resourceType,id,status,envVars,localVerification,externalConnectivity}'
```

`/security` 当前只做安全、隐私与发布门禁发现和审计说明，不返回真实 token、secret、DSN、私钥、证书、webhook、用户输入或生产验证结果。核心字段：

| 字段 | 含义 |
| --- | --- |
| `SecurityControl` | token 权限、scoped RBAC、生产身份/OIDC 准入、CORS、限流、请求体限制、响应安全头、隐私扫描、source hygiene、secret scan、audit log、SIEM、retention、secret provider、OWASP API 回归包、release gate、production readiness 等控制资源 |
| `controlType` | `audit_log` / `auth` / `cors` / `rate_limit` / `request_limit` / `headers` / `identity` / `siem` / `owasp_api_regression` / `privacy` / `rbac` / `retention` / `secret_provider` / `source_hygiene` / `secret_scan` / `release_gate` / `production_readiness` |
| `status` | `available` 表示仓库内已有实现和本地验证命令；`manual` 表示必须由真实外部环境执行 |
| `envVars` | 控制相关环境变量名，只列变量名，不列真实值 |
| `implementationRefs` | 代码或脚本入口 |
| `localVerification` | 可复现本地验证命令；涉及真实域名或真实 Bot 时只登记命令口径 |
| `privacyBoundary` | 该控制不得泄露的内容边界 |
| `externalConnectivity` | 是否需要真实域名、真实凭证、人工权限或外部生产验证 |

当前 available controls 包括记录接口 token、scoped RBAC、CORS allowlist、限流、请求体大小限制、响应安全头、结构化 audit_event、retention policy baseline、OWASP API security regression gate、隐私示例扫描、source hygiene、secret scan 和 public release policy。`control.production_identity_oidc`、`control.external_siem_immutable_audit`、`control.retention_cleanup_plan`、`control.external_secret_provider_kms` 和 `control.production_readiness_external` 是 manual controls：必须使用真实 OIDC/IdP、真实 SIEM/不可变审计存储、真实 retention 清理实现、真实 Vault/KMS/secret manager、真实 API 域名、真实 token、真实 Bot 权限执行外部验证，否则只能标注外部连通验证待执行。

本地 RBAC baseline：

- admin token：`FATE_API_TOKEN` 或 `FATE_API_ADMIN_TOKEN`，拥有 `record.read`、`record.list`、`record.write`、`record.delete`。
- 兼容 user token：`FATE_API_USER_TOKENS` 的值可使用 `用户ID:占位令牌` 形态，默认拥有全部 record scopes，但仍只能访问自己的记录。
- scoped user token：`FATE_API_USER_TOKENS` 的值可使用 `用户ID:占位令牌:record.read|record.list` 形态，只拥有声明的 record scopes，且仍受 owner 边界限制。
- 缺少对应 scope 时返回 403 `权限不足`；跨 owner 访问返回 403 `无权访问该记录`。
- 这只是本地 scoped token RBAC baseline，不是 OAuth/OIDC、外部 IdP、组织级多租户权限或生产 IAM。

生产身份 / SIEM / retention / OWASP API regression contract：

```bash
bash scripts/production-security-gate.sh \
  --output-json infra/runtime/local-state/exports/security/production-security-gate.json
```

该 gate 验证 `contracts/fate/security/production-security-policy.json` 与 `/security` registry 是否一致，覆盖：

- `control.production_identity_oidc`：公网多租户身份必须外部化到 OIDC/IdP；当前 scoped token 只是本地 baseline。
- `control.external_siem_immutable_audit`：生产审计需要外部 SIEM 或不可变审计存储；当前不连接真实 SIEM。
- `control.retention_cleanup_plan`：记录按年龄自动清理需要独立清理器、回归测试和审计事件；当前记录默认显式删除。
- `control.external_secret_provider_kms`：公网多副本和外部 backend 的生产密钥生命周期必须外部化到 Vault/KMS/secret manager；当前 Fernet key ring 只是本地 encrypted-at-rest baseline。
- `control.owasp_api_security_regression`：把 OWASP API Security Top 10 2023 的 10 个风险项映射到本地检查或明确外部待验证项。

gate output 只保存检查名、状态和摘要，不输出真实 token、secret、DSN、SIEM endpoint、请求体、用户输入或报告正文。

安全外部化 evidence contract / negative gate：

```bash
bash scripts/security-externalization-gate.sh \
  --output-json infra/runtime/local-state/exports/security/security-externalization-gate.json
```

0065 新增 `contracts/fate/security/externalization-evidence-contract.json`，用于定义 OIDC/IdP、SIEM/不可变审计存储和 retention cleaner 的 live evidence 必备字段、隐私边界和负向伪造样例。该 gate 会先复用 `production-security-gate`，再验证：

- 本地 scoped token、`FATE_API_TOKEN`、`FATE_API_USER_TOKENS` 不能作为 OIDC/IdP live proof。
- placeholder SIEM、明文 endpoint、日志 payload、请求体或报告正文不能作为不可变审计 evidence。
- 没有 smoke summary、delete mode 和 audit action 的 retention cleaner 不能写成 live evidence。

默认不提供 `--evidence-json` 时，该 gate 只证明仓库内 contract 和反伪造样例可验证，并输出 `外部连通验证待执行`。真实 OIDC、SIEM、不可变审计存储和 retention cleaner live evidence 必须由外部环境单独提供；仓库内不得用本地 token、策略文件或占位 URL 替代。

Retention production cleanup staged gate：

```bash
bash scripts/retention-production-cleanup-gate.sh \
  --output-json infra/runtime/local-state/exports/security/retention-production-cleanup-gate.json
```

0098 新增 `contracts/fate/security/retention-production-cleanup-staged.json`，用于聚合 production scheduler、Postgres cleanup 和 SIEM/log retention 的脱敏 staged evidence contract。默认不提供 `--evidence-json` 时只输出 `shipGate=blocked` 与 `外部连通验证待执行`；提供脱敏 evidence 时也只验证 proof-ref 结构和反伪造边界，不连接真实 Postgres、scheduler 或 SIEM，不执行生产删除，不保存真实 DSN、endpoint、token、secret、用户输入、报告正文、生产日志或真实删除结果。

外部 secret provider evidence contract / negative gate：

```bash
bash scripts/external-secret-provider-gate.sh \
  --output-json infra/runtime/local-state/exports/security/external-secret-provider-gate.json
```

0079 新增 `contracts/fate/security/external-secret-provider-contract.json`，用于定义外部 Vault/KMS/secret manager 的 live evidence 必备字段、隐私边界和负向伪造样例。该 gate 验证：

- 本地 Fernet key ring、`FATE_WEBHOOK_CONFIG_FERNET_KEYS` 或环境变量不能作为外部 Vault/KMS live proof。
- placeholder key reference、dummy proof、明文 `secret=` / `token=` / `password=` 不能进入 evidence。
- 缺少 key reference、rotation、access audit 或 application injection proof 的证据不能写成生产密钥生命周期已完成。

默认不提供 `--evidence-json` 时，该 gate 只证明仓库内 contract 和反伪造样例可验证，并输出 `外部连通验证待执行`。真实外部 secret provider live evidence 必须由外部环境单独提供；仓库内不得用本地 Fernet、静态文件、环境变量或占位 provider 替代。

本地安全 smoke：

```bash
bash scripts/security-smoke.sh \
  --output-json infra/runtime/local-state/exports/security/smoke.json
```

该 smoke 使用 FastAPI `TestClient` 验证记录接口 token/owner 边界、响应安全头、请求体限制、限流和 `/security` registry metadata，并串联 privacy/source/public-release 本地文件门禁。它不会输出真实 token、secret、DSN、请求体、用户输入或报告正文，也不伪造真实生产域名、真实 token 或 Bot live smoke。

本地 secret scan：

```bash
bash scripts/secret-scan.sh \
  --output-json infra/runtime/local-state/exports/security/secret-scan.json
```

该 scanner 扫描 tracked 与未跟踪但未被 gitignore 排除的一线文本文件，排除 reference repos、archive 和二进制/大文件。输出 JSON 只包含路径、行号、规则、severity、短指纹和脱敏长度，不输出疑似密钥原文；发现高置信疑似真实 token、API key、私钥、DSN 或 webhook 时返回失败。

本地 webhook callback smoke：

```bash
bash scripts/webhook-smoke.sh \
  --output-json infra/runtime/local-state/exports/webhook/smoke.json
```

该 smoke 使用可注入 transport 模拟 report job 终态 callback，不访问公网；验证 `WebhookEvent` payload、`X-FateCat-Webhook-Signature: sha256=...`、终态状态，以及 payload 不包含 Markdown 正文、姓名、出生地区或 webhook secret。

本地 audit / retention baseline：

- 记录创建、读取、列表、删除，以及报告 job 提交、取消，会输出结构化 `audit_event` 日志。
- `audit_event` 只记录 action、actor role、短哈希 target、outcome、requestId 和安全 metadata；不得记录真实 token、请求体、报告正文、姓名、出生地区、recordId、jobId 或 userId 原文。
- `FATE_REPORT_JOB_TTL_SECONDS` 控制报告 job TTL；`FATE_REPORT_JOB_STORE=memory|sqlite|postgres` 控制 report job store backend；`FATE_REPORT_JOB_DB_PATH` 仅在 `sqlite` backend 下生效；`FATE_REPORT_JOB_DATABASE_URL` 仅在 `postgres` backend 下生效且不得写入文档、日志或 artifact；`FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE` 指向 `postgres-job-store-live-smoke.sh` 生成的脱敏 JSON，生产预检不能只靠 `FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED=1`；`FATE_REPORT_JOB_MAX_ATTEMPTS`、`FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS`、`FATE_REPORT_JOB_RETRY_BACKOFF_SECONDS` 控制本地 report job retry/timeout policy；`FATE_WEBHOOK_MAX_ATTEMPTS`、`FATE_WEBHOOK_RETRY_BACKOFF_SECONDS` 控制本地 webhook callback retry policy；`FATE_WEBHOOK_REDELIVERY_LEASE_SECONDS` 控制 SQLite/Postgres webhook outbox redelivery 的 lease TTL；`FATE_WEBHOOK_CONFIG_FERNET_KEYS` 使用 `key-id:<fernet-key>[,next-id:<fernet-key>]` 格式，`FATE_WEBHOOK_CONFIG_ACTIVE_KEY_ID` 使用 `<key-id>`，在 SQLite/Postgres backend 下启用 encrypted webhook delivery config vault，用于 failed/pending callback 的 URL/secret 加密恢复和 key rotation。
- `FATE_AUDIT_EVENT_RETENTION_DAYS` 只登记审计事件留存口径；`FATE_RECORD_RETENTION_DAYS=0` 表示记录当前默认显式删除模式。
- 外部 SIEM、不可变审计存储、生产日志留存平台和记录按年龄自动清理已有本地准入 contract、evidence contract 和反伪造 gate；真实平台连通、清理器实现和生产 live evidence 仍属于外部连通验证待执行。

## 交付面资源入口

```bash
curl -sS http://127.0.0.1:8001/surfaces \
  | jq '.data.surfaces[] | {id,surfaceType,status,externalConnectivity}'
```

```bash
curl -sS http://127.0.0.1:8001/surfaces/surface.web \
  | jq '.data | {resourceType,id,entrypoints,supportedOutputs,canonicalChain,localVerification}'
```

`/surfaces` 当前只做交付面发现和审计说明，不返回用户输入、报告正文、真实 token、运行时日志或生产任务状态。核心字段：

| 字段 | 含义 |
| --- | --- |
| `DeliverySurface` | FastAPI、Web、Telegram Bot、CLI、Agent Skill、Hosted Web 等交付入口 |
| `surfaceType` | `api` / `web` / `bot` / `cli` / `skill` / `hosted_web` |
| `status` | `available` 表示本地已有入口和验证命令；`partial` 表示只覆盖部分输出契约；`manual` 表示必须由真实外部环境验证 |
| `entrypoints` | 人类或程序调用入口 |
| `supportedOutputs` | JSON、Markdown、report job、document 等输出形态 |
| `supportedReportSystems` | 当前交付面支持的报告体系或 capability |
| `canonicalChain` | 同源计算链路；Web/API/Bot 的 Markdown 必须经过 `calculate_delivery_result` 与 `generate_full_report` |
| `outputContracts` | 输出契约、文档或测试入口 |
| `localVerification` | 仓库内可执行验证命令 |
| `externalConnectivity` | 是否需要真实 Bot token、真实域名或托管平台 |

当前 `surface.fastapi`、`surface.web`、`surface.telegram_bot` 是可用交付面，其中 Bot live 仍需要真实 Telegram token。`surface.cli` 和 `surface.agent_skill` 是 partial：它们是本地 JSON/capability 或安装运行入口，不承诺直接生成标准 Markdown。`surface.huggingface_space` 是 manual：必须有真实 Space URL 和外部生产验证证据。

发布准入证据由 `releaseGate` 单独声明，不混进某个交付面：

```bash
bash scripts/live-release-gate.sh \
  --output-json infra/runtime/local-state/exports/release/live-release-gate.json
```

默认模式只验证本地 release gate 契约，并把真实 API、HF Space、Bot、远端 CI、container digest、SBOM/provenance、rollback drill 和 clean release git state 标为 `pending` 或 `blocked`。真实发布前必须使用：

本地 quick CI 会生成可交给 release gate 校验的 summary：

```bash
bash scripts/local-ci.sh \
  --profile quick \
  --output infra/runtime/local-state/exports/release/local-ci-quick
```

该命令成功或失败都会写 `summary.json`。只有当 `summary.json` 中 `kind=fatecat.local_ci_summary`、`profile=quick`、`status=passed` 且 `commit` 等于当前 `HEAD` 时，`live-release-gate` 才会把 `evidence.local_ci_quick` 判为 `pass`：

```bash
bash scripts/live-release-gate.sh \
  --local-ci-summary infra/runtime/local-state/exports/release/local-ci-quick/summary.json \
  --output-json infra/runtime/local-state/exports/release/live-release-gate.json
```

这只证明本地 quick CI，不代表远端 GitHub Actions 当前 commit 已通过。

本地可先生成 SBOM/provenance baseline：

```bash
bash scripts/release-artifacts.sh \
  --output-dir infra/runtime/local-state/exports/release/artifacts \
  --summary-json infra/runtime/local-state/exports/release/release-artifacts-summary.json
```

该脚本会生成 `sbom.cyclonedx.json`、`provenance.slsa.json` 和 `release-artifacts-manifest.json`。这些文件可以让 `evidence.sbom_artifact` 和 `evidence.provenance_artifact` 在本地 release gate 中通过；它们不是远端 CI attestation，也不包含 container registry digest 或签名。

本地还可以生成 dry-run rollback drill evidence：

```bash
bash scripts/rollback-drill.sh \
  --release-artifacts-dir infra/runtime/local-state/exports/release/artifacts \
  --local-ci-summary infra/runtime/local-state/exports/release/local-ci-quick/summary.json \
  --output-json infra/runtime/local-state/exports/release/rollback-drill.json
```

该 evidence 必须满足 `kind=fatecat.rollback_drill_evidence`、`status=passed`、`mode=dry-run`、`productionRollbackExecuted=false`。它只证明回滚路径、候选命令和必需文档可审计，不代表真实生产流量已经回滚。

如果本机具备 Docker，也可以生成本地 container release evidence：

```bash
bash scripts/container-release-evidence.sh \
  --image fatecat-delivery:release-local \
  --port 8021 \
  --output-json infra/runtime/local-state/exports/release/container-release-evidence.json
```

该 evidence 必须满足 `kind=fatecat.container_release_evidence`、`status=passed`、`imageId=sha256:<64 hex>`、`smokeStatus=passed`。它只证明本地镜像构建和烟雾验证，不代表 GHCR/registry digest 已推送。

真实 registry release proof 必须走 GitHub 手动容器 workflow：

```bash
gh workflow run container.yml -f push_image=true
```

该 workflow 会构建并 smoke delivery image，上传 `release-artifacts.sh` 生成的 SBOM/provenance/manifest，推送 `ghcr.io/<owner>/fatecat-delivery`，读取 `sha256:<64 hex>` registry digest，使用 `actions/attest@v4` 生成 GitHub artifact attestation，并执行：

```bash
gh attestation verify oci://ghcr.io/<owner>/fatecat-delivery@sha256:<64-hex> \
  --repo <owner>/<repo>
```

只有 GitHub Actions run 对当前 commit 成功，且 summary 中记录 immutable image digest 与 attestation verify 通过，才能把 registry digest/attestation 作为生产 release proof。本地 `container-release-evidence.json` 不能替代这个远端证据。

```bash
bash scripts/live-release-gate.sh \
  --require-live \
  --api-url https://your-domain.example \
  --hf-space-url https://your-space.hf.space \
  --github-run-url https://github.com/<owner>/<repo>/actions/runs/<run-id> \
  --github-commit <current-commit-sha> \
  --container-digest sha256:<64-hex> \
  --container-evidence-path <container-release-evidence.json> \
  --local-ci-summary <local-ci-summary.json> \
  --sbom-path <sbom-file-or-https-url> \
  --provenance-path <provenance-file-or-https-url> \
  --rollback-evidence-path <rollback-evidence-file-or-https-url> \
  --run-live-bot \
  --output-json <release-evidence.json>
```

没有真实外部证据时，`shipGate.status` 必须保持 `blocked`；仓库内不得把本地 gate 通过写成 live release 已通过。

## 错误码字典

```bash
curl -sS http://127.0.0.1:8001/errors \
  | jq '.data.errors[] | {code,httpStatus,category,retryable}'
```

## 报告入口

同步 Markdown：

```bash
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/markdown \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"测试样本",
    "gender":"male",
    "birthDate":"1990-01-01",
    "birthTime":"08:00:00",
    "birthPlace":{"name":"北京市","longitude":116.4074,"latitude":39.9042,"timezone":"Asia/Shanghai"},
    "options":{"useTrueSolarTime":true,"daylightSaving":"auto","midnightMode":"early","calendarType":"solar"}
  }'
```

同步 Markdown、标准异步报告任务和 Web 异步报告任务的成功结果固定包含：

| 字段 | 含义 |
| --- | --- |
| `reportSystem` | 当前报告体系，现阶段可用 `bazi` / `ziwei` |
| `markdown` | 用户可复制的 Markdown 正文 |
| `policyGate` | Markdown 正文禁止性断语扫描结果，扫描 `report.markdown` |
| `snapshotGate` | Markdown heading 结构快照门禁，当前锁核心标题，不做全文 hash diff |

`policyGate` 会允许风险边界里的否定上下文，例如“不输出确定未来”，但正文直接断言禁止词时会返回 `fail`。`snapshotGate` 当前只验证核心 heading 是否存在，完整正文 golden diff、阈值和人工审核仍是后续门禁。

Web 异步报告：

```bash
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/jobs/web \
  -H 'Idempotency-Key: demo-web-report-001' \
  -H 'Content-Type: application/json' \
  -d '{"birthDate":"1990-01-01","birthTime":"08:00:00","birthPlace":"北京","gender":"male","name":"测试样本","reportSystem":"bazi"}'
```

取消任务：

```bash
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/jobs/<job_id>/cancel
```

任务状态固定为：`queued`、`running`、`succeeded`、`failed`、`expired`、`cancelled`。

Report job store：

| 后端 | 配置 | 能力边界 |
| --- | --- | --- |
| `memory` | `FATE_REPORT_JOB_STORE=memory` | 默认后端；只在当前进程 TTL 生命周期内保留任务状态和幂等键。 |
| `sqlite` | `FATE_REPORT_JOB_STORE=sqlite`，`FATE_REPORT_JOB_DB_PATH=infra/runtime/local-state/database/report_jobs.sqlite` | 单副本本地持久化；可在 manager 重建后查询已完成、失败、取消和过期任务，并保留幂等键。带 `task_payload` 且存在注册 factory 的 Web/Markdown 报告任务可在本地重新入队执行。配置 `FATE_WEBHOOK_CONFIG_FERNET_KEYS` 后，failed/pending webhook outbox 的 callback URL/secret 会以 Fernet ciphertext 写入本地 encrypted config vault，manager 重建后可在无运行时 resolver 时重投，并在成功后删除。SQLite outbox redelivery 会先 claim 本地 lease，避免同一 outbox 在本地重复重投；该 lease 不属于生产级分布式 worker lease。 |
| `postgres` | `FATE_REPORT_JOB_STORE=postgres`，`FATE_REPORT_JOB_DATABASE_URL=<secret-env>`，`FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE=<live-smoke.json>` | Postgres ReportJobStore worker heartbeat/polling smoke baseline；使用 tracked DDL、job/event/outbox/config 表、job execution lease、execution heartbeat、持久队列轮询和 webhook outbox conditional claim/release SQL。缺少 `psycopg` 或 DSN 时启动 fail-fast，不会静默 fallback。当前 live smoke、outbox worker lease negative smoke、job worker lease primitive smoke、external worker restart smoke 与 worker heartbeat/polling smoke 只证明真实数据库 schema/job/outbox/config 路径、outbox duplicate claim 负例、job execution worker lease primitive、过期 lease stale running job 可被重启 manager 恢复执行且双 manager 只有一个执行、长任务 lease heartbeat 续租和 persisted queued/running job polling；不证明 production ready、exactly-once、公网 webhook live passed、外部 Vault/KMS 或长期多副本运行。 |

RuntimeBackend contract：

| 资源 | 路径 | 说明 |
| --- | --- | --- |
| registry | `contracts/fate/delivery/runtime-backends.json` | 登记 `memory`、`sqlite`、`postgres`、`temporal`、`redis_queue` 的 mature level、生产资格、证据要求和迁移路径。 |
| schema | `contracts/fate/delivery/schemas/runtime-backend.schema.json` | 定义 RuntimeBackend 字段、状态、生产资格、外部连通边界和禁止伪造声明。 |
| gate | `bash scripts/runtime-backend-gate.sh --output-json <path>` | 本地校验 contract：`backend.postgres` 已有 worker heartbeat/polling smoke baseline 但仍只能是 planned external candidate，`backend.sqlite` 只能 single-replica，`backend.redis_queue` 不能作为 source of truth。 |
| postgres dry-run | `bash scripts/postgres-job-store-dry-run.sh --output-json <path>` | 本地校验 Postgres DDL、required tables/indexes、upsert、job execution lease SQL、webhook outbox conditional claim/release SQL 和隐私边界；不连接真实数据库，不读取或输出 DSN。 |
| postgres live smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-job-store-live-smoke.sh --output-json <path>` | 连接真实或一次性 Postgres，验证 schema 初始化、job/event/idempotency/task payload、webhook outbox claim/release 和 encrypted delivery config 基本读写；summary 只输出 hash 和检查结果，不输出 DSN、用户名、密码、callback URL、webhook secret 或报告正文。无 DSN 的本地巡检可用 `--allow-missing` 生成 blocked artifact。 |
| postgres worker lease smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-worker-lease-smoke.sh --output-json <path>` | 用两个独立 `PostgresReportJobStore`/连接模拟多 worker 竞争同一 webhook outbox，验证 duplicate claim 只能一个成功、失败 worker 不能错误 release、lease 过期后可被其他 worker 重新 claim；summary 只输出 hash 和检查结果，不输出 DSN、用户名、密码、callback URL、secret 或报告正文。无 DSN 的本地巡检可用 `--allow-missing` 生成 blocked artifact。 |
| postgres job worker lease smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-job-worker-lease-smoke.sh --output-json <path>` | 用两个独立 `PostgresReportJobStore`/连接模拟多 worker 竞争同一 queued/running job，验证 duplicate job claim 只能一个成功、错误 owner 不能 release、lease 过期后可被其他 worker 重新 claim，terminal job 不可 claim；summary 只输出 hash 和检查结果，不输出 DSN、用户名、密码、callback URL、secret 或报告正文。无 DSN 的本地巡检可用 `--allow-missing` 生成 blocked artifact；不证明 exactly-once、公网 webhook live 或外部 Vault/KMS。 |
| postgres external worker restart smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-external-worker-restart-smoke.sh --output-json <path>` | 用一次性 Postgres schema、stale running job、过期 execution lease、两个 `ReportJobManager` 和 task factory 模拟 external backend worker crash/restart；验证恢复入队、终态成功、`executionCount=1`、lease terminal 后清理和 summary 脱敏。无 DSN 的本地巡检可用 `--allow-missing` 生成 blocked artifact；不证明 production ready、exactly-once、公网 webhook live、外部 Vault/KMS、worker heartbeat/polling 或长期多副本运行。 |
| postgres worker heartbeat/polling smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> bash scripts/postgres-worker-heartbeat-polling-smoke.sh --output-json <path>` | 用一次性 Postgres schema、`ReportJobManager`、`PostgresReportJobStore`、task factory 和短 execution lease 验证三条 worker runtime baseline：空闲 worker 可轮询 persisted queued job 并执行、长任务期间 heartbeat 可续租避免重复 claim、expired running job 可被 polling worker 恢复执行。summary 只输出 hash、检查结果和执行计数，不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入。无 DSN 的本地巡检可用 `--allow-missing` 生成 blocked artifact；不证明 production ready、exactly-once、公网 webhook live passed、外部 Vault/KMS 或长期多副本运行。 |
| postgres public webhook live smoke | `FATE_REPORT_JOB_DATABASE_URL=<secret-env> FATE_WEBHOOK_LIVE_URL=<public-https-url> bash scripts/postgres-public-webhook-live-smoke.sh --output-json <path>` | 用一次性 Postgres schema、`ReportJobManager`、`PostgresReportJobStore`、`HttpWebhookDispatcher` 和公网 HTTPS endpoint 投递真实 report job 终态 callback，验证 job succeeded、outbox succeeded 和 `webhook.delivery_succeeded` 事件；summary 只输出 hash、状态码和检查结果，不输出 DSN、URL、secret、报告正文或用户输入。无 DSN/URL 的本地巡检可用 `--allow-missing` 生成 blocked artifact；即使 live 通过，也不证明 production ready、exactly-once、外部 Vault/KMS、receiver SLA、heartbeat/polling worker 或长期多副本运行。 |
| multi-replica runtime evidence assembler | `bash scripts/multi-replica-runtime-evidence-assembler.sh --pending --output-json <path>`；真实外部证据装配需 `--external-live --ack-external-live` 与完整 proof refs | 生成 `kind=fatecat.multi_replica_runtime_evidence` 的脱敏 evidence JSON，并立即复用 `multi-replica-runtime-gate.py` 校验。默认 pending 不访问外部环境；external-live 模式只封装 operator 提供的脱敏 proof refs，不保存真实 DSN、URL、secret、报告正文或用户输入，不证明 proof refs 真实性、production ready 或 exactly-once。 |
| multi-replica runtime gate | `bash scripts/multi-replica-runtime-gate.sh --output-json <path>` | 校验 `contracts/fate/delivery/multi-replica-runtime-contract.json`、runtime registry 接线、长期多副本 live evidence schema 和反伪造负例；默认只输出 `外部连通验证待执行`，不连接真实数据库、webhook receiver、secret provider 或监控平台，不证明 production ready、exactly-once 或真实多副本 soak 已通过。 |

当前选型口径：Postgres 是第一个 external ReportJobStore adapter 候选，因为 job state、event history、idempotency、outbox 和 worker claim 可以进入同一个事务型外部 source of truth；Temporal 只登记为未来长流程 orchestrator；Redis queue 只能作为未来辅助队列，不得替代 durable job source of truth。0062 完成 contract baseline，0070 完成 Postgres adapter baseline 与 dry-run，0071 完成 Postgres migration/job live smoke 入口与 evidence contract，0072 完成 Postgres webhook outbox worker lease negative smoke，0074 新增 Postgres job execution worker lease primitive smoke，0075 新增 Postgres external worker restart smoke，0076 新增 Postgres public webhook live smoke gate，0078 新增 Postgres worker heartbeat/polling smoke baseline，0079 新增外部 secret provider evidence gate，0080 新增长期多副本 runtime evidence gate，0081 新增多副本 runtime evidence assembler；exactly-once、公网 webhook live passed evidence、外部 Vault/KMS live passed 和生产多副本长期运行 live evidence 仍未完成。

Async event contract：

| 资源 | 路径 | 说明 |
| --- | --- | --- |
| registry | `contracts/fate/delivery/events.json` | 登记 `job`、`webhook`、`evaluation`、`release` 事件域，包含 CloudEvents envelope、AsyncAPI 风格 channel/operation/message、producer、consumer contract、payload schema、replay/DLQ 策略、脱敏示例和外部连通边界。 |
| AsyncAPI | `contracts/fate/delivery/events.asyncapi.json` | 静态 AsyncAPI 3.1 风格文档，供开发者和 Agent 发现事件通道；不证明外部 broker 或公网 webhook live delivery。 |
| schema | `contracts/fate/delivery/schemas/async-event.schema.json` | 定义 AsyncEvent 字段、CloudEvents 必备上下文字段 `id/source/specversion/type`、事件域枚举和隐私不变量。 |
| examples | `contracts/fate/delivery/examples/events/*.json` 与 `contracts/fate/delivery/examples/event-replay/*.json` | 只保存合成脱敏 CloudEvents、replay request 和 dead-letter record 示例，不包含真实 webhook URL、secret、token、用户输入、出生地区、报告正文或生产日志。 |
| gate | `bash scripts/event-contract-gate.sh --output-json <path>` | 本地校验 registry、AsyncAPI 文档、producer path、required consumer、additive compatibility、replay/DLQ 策略、示例、delivery registry 和 resource schema 链接。 |

0063 完成事件契约 baseline，0097 补齐本地 producer/consumer compatibility、replay request 与 dead-letter record contract baseline：`event.webhook.delivery` 仍标记为 `requires_real_receiver`，公网接收端、签名验证日志、外部 broker、真实事件订阅和 live delivery 仍属外部连通验证待执行。

`running` 任务取消后不能强杀线程，但完成后会丢弃结果并保持 `cancelled`。如果 SQLite backend 在 manager 重建时发现旧 `queued` / `running` 任务：带 `task_payload` 且存在注册 factory 的任务会标记为 `queued`、写入 `job.recovered_requeued` 并重新入队；无 payload 或无 factory 的任务会标记为 `failed`、写入 `job.recovered_failed` 并保留错误原因。该能力只是本地可重建执行 baseline，不是 external backend、分布式 worker、生产多副本锁或 exactly-once。多副本生产不能使用本地 `memory` / `sqlite` job store 假装分布式任务系统，后续需要外部队列或数据库任务系统。

本地 restart recovery smoke：

```bash
bash scripts/report-job-restart-recovery-smoke.sh \
  --output-json infra/runtime/local-state/exports/report-jobs/restart-recovery-smoke.json
```

该 smoke 使用临时 SQLite 和固定脱敏样例，只证明 manager 重建后旧 `queued` / `running` 任务会安全失败、保留幂等键并产生 `job.recovered_failed` 事件；不证明任务跨进程继续执行、external backend、多副本 worker 或生产队列恢复。

本地 replayable recovery smoke：

```bash
bash scripts/report-job-replayable-recovery-smoke.sh \
  --output-json infra/runtime/local-state/exports/report-jobs/replayable-recovery-smoke.json
```

该 smoke 使用临时 SQLite 和固定脱敏样例，证明带 `task_payload` 和 factory 的 active 任务在 manager 重建后可重新入队并成功完成；同时证明无 payload 的 active 任务仍安全失败。它不证明 external backend、分布式 worker lease、多副本锁、真实公网 webhook live smoke 或 exactly-once。

Report job event history：

| 项 | 说明 |
| --- | --- |
| API 字段 | `/api/v1/report/jobs/{job_id}` 返回的 `CalculationJob.data.events[]`。 |
| 事件资源 | 每项为 `CalculationJobEvent`，包含 `eventId`、`jobId`、`eventType`、`status`、`createdAt`、`message`、`metadata`。 |
| 本地持久化 | `memory` 后端保留当前进程内事件；`sqlite` 后端写入 `report_job_events` 并按写入顺序返回。 |
| 当前事件 | `job.queued`、`job.running`、`job.succeeded`、`job.failed`、`job.cancelled`、`job.expired`、`job.recovered_failed`、`job.recovered_requeued`、`job.attempt_failed`、`job.attempt_timed_out`、`job.retry_scheduled`、`webhook.delivery_attempt_failed`、`webhook.delivery_retry_scheduled`、`webhook.delivery_succeeded`、`webhook.delivery_failed`、`webhook.redelivery_scheduled`、`webhook.redelivery_skipped`、`webhook.redelivery_succeeded`、`webhook.redelivery_failed`。 |
| 隐私 | event metadata 不包含 Markdown 正文、姓名、出生地区、请求体、webhook URL、webhook secret 或原始异常文本。 |
| 边界 | 事件历史只证明任务生命周期可审计；本地 webhook retry/outbox trail、SQLite persistent outbox record baseline、restart-safe failure smoke、replayable recovery smoke、SQLite outbox redelivery baseline、SQLite encrypted webhook delivery config vault baseline、SQLite outbox lease claim/release baseline、Postgres outbox worker lease negative smoke、Postgres job worker lease primitive smoke、Postgres external worker restart smoke 与 Postgres worker heartbeat/polling smoke baseline 已有；真实公网 webhook live passed evidence、外部 Vault/KMS、生产密钥生命周期、长期多副本运行和 exactly-once 仍未完成。 |

Report job retry / timeout policy：

| 项 | 说明 |
| --- | --- |
| API 字段 | `CalculationJob.data.attempts`、`maxAttempts`、`attemptTimeoutSeconds`、`retryBackoffSeconds`。 |
| 默认值 | `FATE_REPORT_JOB_MAX_ATTEMPTS=1`，`FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS=0`，`FATE_REPORT_JOB_RETRY_BACKOFF_SECONDS=0`；默认不重试、不启用 attempt timeout。 |
| retry | retryable exception 在 `attempt < maxAttempts` 时重试，并写入 `job.attempt_failed` 与 `job.retry_scheduled`。 |
| non-retryable | `ReportJobNonRetryableError` 不重试，直接进入 `failed`，事件 metadata 标记 `retryable=false`。 |
| timeout | `attemptTimeoutSeconds>0` 时，当前进程会把超时 attempt 标记为 `job.attempt_timed_out` 并按 policy 失败或重试。 |
| 边界 | 当前 timeout 是本地任务状态 baseline，不能保证强杀底层 Python callable；若 timeout 后继续重试，底层 callable 仍需保持幂等；生产硬 timeout、多副本协调和长流程恢复需要 external backend。 |

Report job webhook callback：

| 项 | 说明 |
| --- | --- |
| 开关 | `FATE_REPORT_JOB_WEBHOOKS_ENABLED=1` 后，异步报告任务才接受 callback URL；默认关闭。 |
| 请求头 | `X-FateCat-Webhook-Url`，可选 `X-FateCat-Webhook-Secret`。 |
| URL 边界 | 默认只允许 `https`；`http` 仅在 `FATE_WEBHOOK_ALLOW_HTTP=1` 时用于本地调试。内网、本机、保留地址和带用户名/密码的 URL 会被拒绝。 |
| allowlist | `FATE_WEBHOOK_ALLOWED_HOSTS=callback.example,*.partner.example` 可限制接收端 host。 |
| 签名 | 如果提供 secret，发送 `X-FateCat-Webhook-Signature: sha256=<hmac>`，HMAC 输入是排序后的 JSON body。 |
| 事件 | 只在 `succeeded` / `failed` / `cancelled` 终态发送 `report_job.terminal`。 |
| retry | 默认 `FATE_WEBHOOK_MAX_ATTEMPTS=1` 不重试；显式配置 `>1` 时，本地 manager 会记录 `webhook.delivery_attempt_failed`、`webhook.delivery_retry_scheduled`，最终写入 `webhook.delivery_succeeded` 或 `webhook.delivery_failed`；接收方必须按 `eventId` 做幂等处理。 |
| outbox | SQLite backend 会写入 `CalculationJob.data.webhookOutbox[]` 脱敏摘要，包含 outboxId、eventType、jobStatus、status、attempts、maxAttempts、signature、targetHostHash、时间字段、lastErrorType 和 resultStatusCode。内部 lease owner、lease acquired time 和 lease expiry 不进入 API payload。 |
| encrypted config vault | SQLite backend 配置 `FATE_WEBHOOK_CONFIG_FERNET_KEYS` 后，会把 failed/pending webhook 的 callback URL/secret 加密写入 `report_job_webhook_delivery_config`；manager 重建后可用该 encrypted config 重投，成功后删除，`FATE_WEBHOOK_CONFIG_ACTIVE_KEY_ID` 用于新写入和本地 rotation。 |
| 隐私 | webhook payload 不包含 Markdown 正文、姓名、出生地区、请求体或 secret；只包含 jobId、状态、时间戳、statusUrl/cancelUrl 和 `resultAvailable`。 |

示例：

```bash
# 服务启动前配置：FATE_REPORT_JOB_WEBHOOKS_ENABLED=1
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/jobs \
  -H 'Idempotency-Key: demo-webhook-report-001' \
  -H 'X-FateCat-Webhook-Url: https://callback.example/webhook' \
  -H 'X-FateCat-Webhook-Secret: 占位示例值-请勿提交真实密钥' \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"测试样本",
    "gender":"male",
    "birthDate":"1990-01-01",
    "birthTime":"08:00:00",
    "birthPlace":{"name":"北京市","longitude":116.4074,"latitude":39.9042,"timezone":"Asia/Shanghai"},
    "options":{"useTrueSolarTime":true,"daylightSaving":"auto","midnightMode":"early","calendarType":"solar"}
  }'
```

本地 webhook outbox smoke：

```bash
bash scripts/webhook-outbox-smoke.sh \
  --output-json infra/runtime/local-state/exports/webhook/outbox-smoke.json
```

本地 webhook outbox redelivery smoke：

```bash
bash scripts/webhook-outbox-redelivery-smoke.sh \
  --output-json infra/runtime/local-state/exports/webhook/redelivery-smoke.json
```

本地 webhook encrypted config vault smoke：

```bash
bash scripts/webhook-config-vault-smoke.sh \
  --output-json infra/runtime/local-state/exports/webhook/config-vault-smoke.json
```

该 smoke 使用临时 SQLite 和运行时生成的 Fernet key，证明 failed outbox 的 callback URL/secret 只以 ciphertext 落库、raw SQLite 和 summary 不包含 URL/secret/报告正文/姓名/地区、key rotation 会把旧 key id 切到 active key，manager 重建后不依赖外部 `delivery_resolver` 也能重投，成功后 encrypted config 被删除。

0079 之后，外部 Vault/KMS/secret manager 的证据不再只停留在文档描述，而由 `external-secret-provider-gate` 定义统一 evidence schema 和反伪造负例。注意：`webhook-config-vault-smoke.sh` 仍只证明本地 Fernet encrypted-at-rest baseline，不证明外部 Vault/KMS、生产 key rotation、access audit 或 application secret injection 已完成。

本地 webhook outbox lease smoke：

```bash
bash scripts/webhook-outbox-lease-smoke.sh \
  --output-json infra/runtime/local-state/exports/webhook/outbox-lease-smoke.json
```

该 smoke 使用临时 SQLite、运行时生成的 Fernet key 和可注入 transport，证明 failed outbox 只能被一个本地 lease owner claim、错误 owner release 无效、release 后可重新 claim、manager 重建后通过 encrypted config 只重投一次，并且 summary 不包含 URL/secret/lease owner/报告正文/姓名/地区。

当前 webhook 是本地可验证 callback baseline，已包含有限 retry、事件轨迹、SQLite persistent outbox record baseline、SQLite manager 重建后的 resolver redelivery baseline、本地 encrypted config vault baseline、SQLite outbox lease claim/release baseline、Postgres outbox worker lease negative smoke、Postgres job worker lease primitive smoke、Postgres external worker restart smoke 和 Postgres worker heartbeat/polling smoke baseline；outbox 摘要不包含完整 webhook URL、webhook secret、lease owner、报告正文、姓名、出生地区或请求体。它仍不包含公网 live passed evidence、接收端 SLA、外部 Vault/KMS、生产密钥生命周期、长期多副本运行或 exactly-once，这些仍是外部连通验证待执行。

## 准入规则

| 能力状态 | 准入要求 |
| --- | --- |
| `production` | `maturity.level` 至少 L3，`testGate.status=passing`，必须声明本地回归命令，不得使用 `planned.*` provider |
| `planned` | `maturity.level=L0`，`testGate.status=blocked`，必须使用 `planned.*` provider 和 `planned-v0` engineVersion |
| 默认 Markdown | 必须且只能是 `bazi` |

## 错误与限流

| 状态码 | 含义 |
| --- | --- |
| 400 | capability 未知、未生产化或 payload 业务字段不合法 |
| 413 | 请求体超过 `FATE_MAX_REQUEST_BYTES` |
| 422 | FastAPI/Pydantic 参数校验失败 |
| 429 | 频率限制或报告队列已满 |
| 503 | 计算并发槽耗尽或 ready 检查失败 |
| 504 | 请求处理超过 `FATE_REQUEST_TIMEOUT_SECONDS` |

## 安全与隐私

- 公开 Web 示例和用户界面不得展示北京以外的真实地区名称。
- 记录接口需要 `FATE_API_TOKEN`、`FATE_API_ADMIN_TOKEN` 或 `FATE_API_USER_TOKENS`；`FATE_API_USER_TOKENS` 支持 `用户ID:占位令牌` 和 `用户ID:占位令牌:record.read|record.list` 两类值形态；禁用时返回 403。
- 文档、响应样例和日志不得输出真实 token、secret、DSN、私钥或服务账号内容。
- 外部 API 域名、真实 token、Bot webhook、远程服务器和生产数据库均属于：外部连通验证待执行。

## 本地验证

```bash
.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py
bash scripts/local-ci.sh --profile quick
python3 governance/tools/validate_governance_package.py --project-root . --strict
```
