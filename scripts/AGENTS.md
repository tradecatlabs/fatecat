# AGENTS.md - scripts

## 目录用途

`scripts/` 是本地可重复执行入口。GitHub Actions 只触发这些入口，不复制另一套流水线逻辑。

## 目录结构

```text
scripts/
├── AGENTS.md
├── acceptance.sh
├── bazi-ziwei-l4-golden-smoke.sh
├── bazi-ziwei-l4-golden-smoke.py
├── check-public-release-policy.sh
├── container-build.sh
├── container-release.sh
├── container-smoke.sh
├── data-supply-chain-gate.sh
├── data-supply-chain-gate.py
├── developer-docs-smoke.sh
├── developer-docs-smoke.py
├── export-openapi.sh
├── export-openapi.py
├── evaluation-dashboard.sh
├── evaluation-dashboard.py
├── evaluation-dashboard-smoke.sh
├── evaluation-nightly.sh
├── hf-space-deploy.sh
├── local-ci.sh
├── live-release-gate.sh
├── live-release-gate.py
├── observability-smoke.sh
├── observability-smoke.py
├── observability-slo-gate.sh
├── observability-slo-gate.py
├── observability-trace-slo-smoke.sh
├── observability-trace-slo-smoke.py
├── preflight.sh
├── provider-dependency-smoke.sh
├── provider-dependency-smoke.py
├── provider-lifecycle-gate.sh
├── provider-lifecycle-gate.py
├── production-security-gate.sh
├── production-security-gate.py
├── public-release-gate.sh
├── release-artifacts.sh
├── release-artifacts.py
├── secret-scan.sh
├── secret-scan.py
├── security-smoke.sh
├── security-smoke.py
├── webhook-smoke.sh
├── webhook-smoke.py
├── export-runtime.sh
├── compare-evaluations.sh
├── compare-evaluations.py
├── run-evaluations.sh
├── run-evaluations.py
├── generate-mingli-predictions.sh
├── run-mingli-bench.sh
└── ...
```

## 职责边界

- 根脚本负责 bootstrap、preflight、acceptance、delivery smoke、容器 smoke、导出卫生和生产就绪检查。
- `container-build.sh`：构建 FateCat delivery 镜像。
- `container-smoke.sh`：启动临时容器并验证 `/health` 与真实排盘 API。
- `container-release.sh`：构建、smoke，并在显式 `--push` 时推送 registry。
- `data-supply-chain-gate.sh` / `data-supply-chain-gate.py` 是数据供应链门禁；校验 data supply chain registry、canonical classics source/copyright manifest、solar terms source manifest 和 vendor production dependency 许可边界。
- `export-openapi.sh` / `export-openapi.py`：导出本地 OpenAPI JSON，并校验开发者接入必备路径。
- `developer-docs-smoke.sh` / `developer-docs-smoke.py`：执行开发者 OpenAPI、sandbox fixture 和 SDK 示例 smoke；只保存检查摘要，不保存报告正文或真实凭证。
- `check-public-release-policy.sh`：检查公开 Web 工作台发布策略，防止 GitHub 自动验收回潮、HF 免费 Space 误开记录存储或文档口径缺失。
- `hf-space-deploy.sh`：生成 Hugging Face Docker Space 分发包，并通过 `hf` CLI 上传到指定 Space；默认目标 `tradecatlabs/fatecat`，默认拒绝非 `tradecatlabs` 认证。
- `local-ci.sh`：本地 CI/CD 调度入口；只编排本仓脚本，不调用 GitHub Actions；成功或失败都会写 `summary.txt` 与机器可读 `summary.json`，其中 `summary.json` 是 live release gate 的 `evidence.local_ci_quick` 输入。
- `live-release-gate.sh` / `live-release-gate.py` 是 live release evidence gate；聚合 local CI、远端 CI、生产 API、HF Space、Telegram Bot、container digest、SBOM/provenance、rollback drill 和 clean git state，输出机器可读 JSON。默认只做本地合同检查并标注外部连通验证待执行；`--local-ci-summary` 必须指向 `kind=fatecat.local_ci_summary`、`profile=quick`、`status=passed` 且 commit 匹配当前 HEAD 的 JSON；`--require-live` 才要求真实外部证据全部通过。
- `bazi-ziwei-l4-golden-smoke.sh` / `bazi-ziwei-l4-golden-smoke.py` 是八字/紫微 L4 golden evidence 本地 smoke；`quick` 跑代表样本并进入本地 quick CI，`full` 跑当前 fixture 全量样本，不访问真实用户或外部账号。
- `observability-smoke.sh` / `observability-smoke.py` 是本地观测 smoke；用 TestClient 验证 health、ready、metrics、request-id、结构化日志和 observability registry metadata。
- `observability-slo-gate.sh` / `observability-slo-gate.py` 是本地 SLO/alert policy gate；校验 observability registry、SLO objectives、alert rules、runbook 引用和隐私边界，不读取真实生产指标或日志。
- `observability-trace-slo-smoke.sh` / `observability-trace-slo-smoke.py` 是本地 trace/SLO smoke；验证 W3C `traceparent` 传播、OpenTelemetry 语义兼容 span 日志、API/provider/report trace、SLO policy 和 alert rules，不接外部 collector。
- `provider-dependency-smoke.sh` / `provider-dependency-smoke.py` 是 production provider 本地依赖执行 smoke；通过统一 `CapabilityExecutor` 和脱敏固定样例验证 provider validate/calculate 链路，不访问公网或真实账号。
- `provider-lifecycle-gate.sh` / `provider-lifecycle-gate.py` 是 production provider 生命周期门禁；校验 versionLock、source/license/resource manifest、promotionGate、deprecation 和 vendor source 生产使用许可。
- `production-security-gate.sh` / `production-security-gate.py` 是生产安全 contract gate；验证生产身份外部化、OIDC/IdP 准入、SIEM/不可变审计存储、retention 自动清理计划和 OWASP API Security Top 10 回归包，不连接真实外部账号或 SIEM。
- `public-release-gate.sh`：公开 Web 工作台发布前本地门禁；串联 quick CI、发布策略、delivery smoke、生产静态准入和 live release evidence gate，可选验证线上 API URL。
- `release-artifacts.sh` / `release-artifacts.py` 生成本地发布资产 baseline：CycloneDX 兼容 SBOM、SLSA/in-toto 风格 provenance 和 manifest；只读取 lockfile、Dockerfile、关键 contracts/scripts 和 git metadata，不生成远端 CI attestation、registry signature 或 container digest。
- `rollback-drill.sh` / `rollback-drill.py` 生成本地 dry-run rollback drill evidence：校验回滚相关脚本、部署文档、release artifacts 和候选命令，输出 `kind=fatecat.rollback_drill_evidence` 的 JSON；不执行真实生产回滚、registry 切换或 HF/Bot 外部操作。
- `container-release-evidence.sh` / `container-release-evidence.py` 生成本地 container release evidence：复用 `container-build.sh` 与 `container-smoke.sh`，记录 imageId、build/smoke 状态、RepoDigests、commit 和 `pushExecuted=false`；不推送 registry，不把本地 imageId 当成 GHCR digest。
- `secret-scan.sh` / `secret-scan.py` 是本地 secret scanner；扫描 tracked 与未跟踪非忽略的一线文本文件，输出脱敏 JSON summary，发现疑似真实密钥时阻断。
- `security-smoke.sh` / `security-smoke.py` 是本地安全 smoke；验证 token/owner 边界、响应安全头、请求体限制、限流、registry metadata，并可串联 privacy/source/public-release 文件门禁。
- `webhook-smoke.sh` / `webhook-smoke.py` 是 report job webhook 本地模拟器；使用可注入 transport 验证终态事件、HMAC 签名和正文/secret 不外发，不访问公网。
- `common.sh` 负责解析 runtime root；只允许已就绪的企业根作为运行根。
- `run-evaluations.sh` / `run-evaluations.py` 是 `contracts/fate/evaluations/registry.json` 的本地 EvaluationRun 执行器；默认跑本地必跑评测，输出 summary JSON，只允许白名单命令。
- `compare-evaluations.sh` / `compare-evaluations.py` 是本地 Evaluation summary diff 工具；按 `contracts/fate/evaluations/diff-policy.json` 判定新增失败、缺失 run 和失败命令。
- `evaluation-dashboard.sh` / `evaluation-dashboard.py` 把 EvaluationRun summary 与可选 diff 渲染为静态 HTML dashboard；只展示状态、命令、exit code、duration 和 diff 摘要，不渲染 stdout/stderr tail、benchmark 标准答案、报告正文或真实凭证。
- `evaluation-dashboard-smoke.sh` 使用 dry-run EvaluationRun summary 验证 dashboard renderer 和隐私边界；进入 quick CI，不执行重型评测。
- `evaluation-nightly.sh` 执行 releaseRequired EvaluationRun、记录 history/latest、生成 diff 和 dashboard artifact；默认不执行 reference repo benchmark，不访问外部模型 API。
- `generate-mingli-predictions.sh` 是 `fate_core.evaluation.mingli_baseline` 的薄封装，不承载领域评测规则。
- `run-mingli-bench.sh` 负责离线 FortuneTellingBench 统计、提示词生成和预测结果评估，不调用外部模型 API。
- 脚本不得保活退役路径；任何旧路径只能出现在防回潮门禁、历史证据或迁移账本中。

## Principle Gate Evidence

- target end state: scripts are thin local CI/CD and runtime entrypoints around canonical roots.
- real constraints: container smoke uses short-lived containers and local ports for self-host checks.
- inertia constraints: historical script names and smoke helpers must not become alternate platforms.
- kill list: hidden old root fallback, secret persistence, and live-production claims without inputs.
- proof point: `local-ci.sh --profile all` passes through shell, pytest, export, Docker, and readiness.
- falsifier: any script writes secrets, hides runtime state, or claims live API/Bot without real inputs.
- migration slice: keep root scripts as stable wrappers while domains/contracts own implementation logic.

## 依赖方向

- `scripts -> domains + contracts + infra + governance`
- `scripts/generate-mingli-predictions.sh -> fate_core.evaluation.mingli_baseline`
- `scripts/hf-space-deploy.sh -> infra/huggingface-space + hf CLI`
- `scripts/live-release-gate.py -> contracts/fate/delivery/release-gate.json + contracts/fate/delivery/registry.json + .github/workflows`
- `scripts/release-artifacts.py -> pyproject.toml + requirements.lock.txt + requirements-dev.lock.txt + infra/docker + contracts/fate/delivery`
- `scripts/developer-docs-smoke.py -> contracts/fate/developer + docs/reference-materials/developer + FastAPI TestClient`
- 禁止脚本直接隐藏 secret、运行态或旧路径 fallback。
