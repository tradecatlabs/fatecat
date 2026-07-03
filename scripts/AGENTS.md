# AGENTS.md - scripts

## 目录用途

`scripts/` 是本地可重复执行入口。GitHub Actions 只触发这些入口，不复制另一套流水线逻辑。

## 目录结构

```text
scripts/
├── AGENTS.md
├── acceptance.sh
├── audit-handoff-dry-run.sh
├── audit-handoff-dry-run.py
├── audit-handoff.sh
├── audit-handoff.py
├── bazi-ziwei-l4-golden-smoke.sh
├── bazi-ziwei-l4-golden-smoke.py
├── check-public-release-policy.sh
├── core-quality-corpus-gate.sh
├── core-quality-corpus-gate.py
├── container-build.sh
├── container-release.sh
├── container-smoke.sh
├── data-supply-chain-gate.sh
├── data-supply-chain-gate.py
├── event-contract-gate.sh
├── event-contract-gate.py
├── developer-docs-smoke.sh
├── developer-docs-smoke.py
├── developer-platform-gate.sh
├── developer-platform-gate.py
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
├── otel-collector-slo-gate.sh
├── otel-collector-slo-gate.py
├── preflight.sh
├── postgres-job-store-dry-run.sh
├── postgres-job-store-dry-run.py
├── postgres-job-store-live-smoke.sh
├── postgres-job-store-live-smoke.py
├── postgres-external-worker-restart-smoke.sh
├── postgres-external-worker-restart-smoke.py
├── postgres-worker-heartbeat-polling-smoke.sh
├── postgres-worker-heartbeat-polling-smoke.py
├── postgres-public-webhook-live-smoke.sh
├── postgres-public-webhook-live-smoke.py
├── multi-replica-runtime-gate.sh
├── multi-replica-runtime-gate.py
├── provider-dependency-smoke.sh
├── provider-dependency-smoke.py
├── report-job-restart-recovery-smoke.sh
├── report-job-restart-recovery-smoke.py
├── provider-lifecycle-gate.sh
├── provider-lifecycle-gate.py
├── production-security-gate.sh
├── production-security-gate.py
├── security-externalization-gate.sh
├── security-externalization-gate.py
├── public-release-gate.sh
├── report-job-replayable-recovery-smoke.sh
├── report-job-replayable-recovery-smoke.py
├── runtime-backend-gate.sh
├── runtime-backend-gate.py
├── release-artifacts.sh
├── release-artifacts.py
├── secret-scan.sh
├── secret-scan.py
├── security-smoke.sh
├── security-smoke.py
├── webhook-outbox-smoke.sh
├── webhook-outbox-smoke.py
├── webhook-outbox-redelivery-smoke.sh
├── webhook-outbox-redelivery-smoke.py
├── webhook-config-vault-smoke.sh
├── webhook-config-vault-smoke.py
├── webhook-outbox-lease-smoke.sh
├── webhook-outbox-lease-smoke.py
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
- `audit-handoff.sh` / `audit-handoff.py` 是第三方审计交接包生成器；聚合 Git、任务索引、关键 contract、local-ci/CI 证据入口和所有 tracked + untracked non-ignored `外部连通验证待执行` occurrences，输出 Markdown/JSON，不证明外部 live 已完成。
- `audit-handoff-dry-run.sh` / `audit-handoff-dry-run.py` 是审计交接包 dry-run verifier；消费 handoff JSON/Markdown，验证字段、区块、pending、risk、non-claim 和敏感赋值防护，输出预检报告，不替代真实第三方审计。
- `container-build.sh`：构建 FateCat delivery 镜像。
- `container-smoke.sh`：启动临时容器并验证 `/health` 与真实排盘 API。
- `container-release.sh`：构建、smoke，并在显式 `--push` 时推送 registry。
- `data-supply-chain-gate.sh` / `data-supply-chain-gate.py` 是数据供应链门禁；校验 data supply chain registry、canonical classics source/copyright manifest、solar terms source manifest 和 vendor production dependency 许可边界。
- `event-contract-gate.sh` / `event-contract-gate.py` 是异步事件 contract gate；校验 AsyncEvent registry、CloudEvents 必备字段、AsyncAPI 风格 channel/operation/message、脱敏示例和 delivery/resource schema 链接，不连接真实 broker 或公网 webhook 接收端。
- `runtime-backend-gate.sh` / `runtime-backend-gate.py` 是 durable runtime 后端 contract gate；校验 RuntimeBackend registry、memory/sqlite 本地边界、Postgres external backend 候选、Temporal future orchestrator、Redis queue 非 source-of-truth 约束和隐私边界，不连接真实数据库或服务。
- `postgres-job-store-dry-run.sh` / `postgres-job-store-dry-run.py` 是 Postgres ReportJobStore adapter baseline dry-run；校验 tracked Postgres DDL、required tables/indexes、upsert、webhook outbox conditional claim/release SQL、optional dependency 边界和隐私边界，不连接真实 Postgres、不读取或输出 DSN。
- `postgres-job-store-live-smoke.sh` / `postgres-job-store-live-smoke.py` 是 Postgres ReportJobStore migration/job live smoke；只从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN，用一次性 schema 验证真实数据库 schema 初始化、job/event/idempotency/task payload、webhook outbox claim/release 和 encrypted delivery config 基本读写，输出脱敏 JSON，不证明 production ready、多副本 worker、公网 webhook live 或外部 Vault/KMS。
- `postgres-worker-lease-smoke.sh` / `postgres-worker-lease-smoke.py` 是 Postgres webhook outbox worker lease negative smoke；只从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN，用两个独立 `PostgresReportJobStore`/连接模拟多 worker 竞争同一 outbox，验证 duplicate claim 只能一个成功、错误 owner release 无效、lease 过期后可重新 claim，输出脱敏 JSON，不证明 job execution worker lease、exactly-once、公网 webhook live 或外部 Vault/KMS。
- `postgres-job-worker-lease-smoke.sh` / `postgres-job-worker-lease-smoke.py` 是 Postgres job execution worker lease primitive smoke；只从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN，用两个独立 `PostgresReportJobStore`/连接模拟多 worker 竞争同一 queued/running job，验证 duplicate claim 只能一个成功、错误 owner release 无效、lease 过期后可重新 claim、terminal job 不可 claim，输出脱敏 JSON，不证明 exactly-once、crash/restart external worker、公网 webhook live 或外部 Vault/KMS。
- `postgres-external-worker-restart-smoke.sh` / `postgres-external-worker-restart-smoke.py` 是 Postgres external worker restart smoke；只从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN，用一次性 schema、stale running job、过期 execution lease、两个 `ReportJobManager` 和 task factory 模拟 worker restart 竞争恢复，验证 `executionCount=1`、终态成功和 terminal lease 清理，输出脱敏 JSON，不证明 production ready、exactly-once、公网 webhook live、外部 Vault/KMS、heartbeat/polling worker 或长期多副本运行。
- `postgres-worker-heartbeat-polling-smoke.sh` / `postgres-worker-heartbeat-polling-smoke.py` 是 Postgres worker heartbeat/polling smoke；只从 `FATE_REPORT_JOB_DATABASE_URL` 读取 DSN，用一次性 schema、`ReportJobManager`、`PostgresReportJobStore` 和 task factory 验证 persisted queued job 轮询执行、长任务 execution lease heartbeat 续租、expired running job polling 恢复和 terminal lease 清理，输出脱敏 JSON，不证明 production ready、exactly-once、公网 webhook live、外部 Vault/KMS 或长期多副本运行。
- `postgres-public-webhook-live-smoke.sh` / `postgres-public-webhook-live-smoke.py` 是 Postgres public webhook live smoke gate；只从 `FATE_REPORT_JOB_DATABASE_URL`、`FATE_WEBHOOK_LIVE_URL` 和可选 `FATE_WEBHOOK_LIVE_SECRET` 读取外部配置，用一次性 schema、`ReportJobManager`、`PostgresReportJobStore` 和 `HttpWebhookDispatcher` 向公网 HTTPS endpoint 投递一条真实终态 callback，输出脱敏 JSON。无外部配置时只能 `--allow-missing` blocked，不证明 production ready、exactly-once、外部 Vault/KMS、receiver SLA、heartbeat/polling worker 或长期多副本运行。
- `multi-replica-runtime-gate.sh` / `multi-replica-runtime-gate.py` 是长期多副本 runtime evidence gate；校验 `multi-replica-runtime-contract.json`、runtime registry 接线、反伪造负例和可选脱敏 live evidence。默认不连接真实数据库、webhook receiver、secret provider 或监控平台，不证明 exactly-once。
- `export-openapi.sh` / `export-openapi.py`：导出本地 OpenAPI JSON，并校验开发者接入必备路径。
- `developer-docs-smoke.sh` / `developer-docs-smoke.py`：执行开发者 OpenAPI、sandbox fixture 和 SDK 示例 smoke；只保存检查摘要，不保存报告正文或真实凭证。
- `developer-platform-gate.sh` / `developer-platform-gate.py`：校验 developer platform contract、SDK/package baseline、sandbox token contract 与 API changelog；只证明本地契约和示例自洽，不证明 PyPI/npm SDK 发布或公网 token 服务上线。
- `check-public-release-policy.sh`：检查公开 Web 工作台发布策略，防止 GitHub 自动验收回潮、HF 免费 Space 误开记录存储、container workflow 丢失 registry digest/attestation verify 或文档口径缺失。
- `hf-space-deploy.sh`：生成 Hugging Face Docker Space 分发包，并通过 `hf` CLI 上传到指定 Space；默认目标 `tradecatlabs/fatecat`，默认拒绝非 `tradecatlabs` 认证。
- `local-ci.sh`：本地 CI/CD 调度入口；只编排本仓脚本，不调用 GitHub Actions；成功或失败都会写 `summary.txt` 与机器可读 `summary.json`，其中 `summary.json` 是 live release gate 的 `evidence.local_ci_quick` 输入。
- `live-release-gate.sh` / `live-release-gate.py` 是 live release evidence gate；聚合 local CI、远端 CI、生产 API、HF Space、Telegram Bot、container digest、SBOM/provenance、rollback drill 和 clean git state，输出机器可读 JSON。默认只做本地合同检查并标注外部连通验证待执行；`--local-ci-summary` 必须指向 `kind=fatecat.local_ci_summary`、`profile=quick`、`status=passed` 且 commit 匹配当前 HEAD 的 JSON；`--require-live` 才要求真实外部证据全部通过。
- `bazi-ziwei-l4-golden-smoke.sh` / `bazi-ziwei-l4-golden-smoke.py` 是八字/紫微 L4 golden evidence 本地 smoke；`quick` 跑代表样本并进入本地 quick CI，`full` 跑当前 fixture 全量样本，不访问真实用户或外部账号。
- `core-quality-corpus-gate.sh` / `core-quality-corpus-gate.py` 是八字/紫微核心质量语料门禁；校验 evaluation manifest、report diff policy、匿名 fixture 数量、北京测试样本和 registry 链接，不读取真实用户或生产数据。
- `observability-smoke.sh` / `observability-smoke.py` 是本地观测 smoke；用 TestClient 验证 health、ready、metrics、request-id、结构化日志和 observability registry metadata。
- `observability-slo-gate.sh` / `observability-slo-gate.py` 是本地 SLO/alert policy gate；校验 observability registry、SLO objectives、alert rules、runbook 引用和隐私边界，不读取真实生产指标或日志。
- `observability-trace-slo-smoke.sh` / `observability-trace-slo-smoke.py` 是本地 trace/SLO smoke；验证 W3C `traceparent` 传播、OpenTelemetry 语义兼容 span 日志、API/provider/report trace、SLO policy 和 alert rules，不接外部 collector。
- `otel-collector-slo-gate.sh` / `otel-collector-slo-gate.py` 是 OTel collector/SLO adapter contract gate；校验 dry-run collector config、SLO evidence contract、registry/schema 链接和外部 pending 边界，不启动真实 collector 或访问 trace backend。
- `provider-dependency-smoke.sh` / `provider-dependency-smoke.py` 是 production provider 本地依赖执行 smoke；通过统一 `CapabilityExecutor` 和脱敏固定样例验证 provider validate/calculate 链路，不访问公网或真实账号。
- `provider-lifecycle-gate.sh` / `provider-lifecycle-gate.py` 是 production provider 生命周期门禁；校验 versionLock、source/license/resource manifest、promotionGate、deprecation 和 vendor source 生产使用许可。
- `production-security-gate.sh` / `production-security-gate.py` 是生产安全 contract gate；验证生产身份外部化、OIDC/IdP 准入、SIEM/不可变审计存储、retention 自动清理计划、外部 secret provider / Vault / KMS 准入和 OWASP API Security Top 10 回归包，不连接真实外部账号、SIEM、Vault 或 KMS。
- `security-externalization-gate.sh` / `security-externalization-gate.py` 是安全外部化 evidence gate；先复用 production security gate，再验证 OIDC/SIEM/retention cleaner evidence contract 和反伪造负例，拒绝把本地 scoped token、placeholder SIEM 或缺 smoke 的 retention cleaner 写成 live evidence。
- `external-secret-provider-gate.sh` / `external-secret-provider-gate.py` 是外部 secret provider evidence gate；验证 Vault/KMS/secret manager evidence contract 和反伪造负例，拒绝把本地 Fernet key ring、环境变量或 placeholder proof 写成 external live evidence。
- `public-release-gate.sh`：公开 Web 工作台发布前本地门禁；串联 quick CI、发布策略、delivery smoke、生产静态准入和 live release evidence gate，可选验证线上 API URL。
- `release-artifacts.sh` / `release-artifacts.py` 生成本地发布资产 baseline：CycloneDX 兼容 SBOM、SLSA/in-toto 风格 provenance 和 manifest；只读取 lockfile、Dockerfile、关键 contracts/scripts 和 git metadata，不生成远端 CI attestation、registry signature 或 container digest。
- `rollback-drill.sh` / `rollback-drill.py` 生成本地 dry-run rollback drill evidence：校验回滚相关脚本、部署文档、release artifacts 和候选命令，输出 `kind=fatecat.rollback_drill_evidence` 的 JSON；不执行真实生产回滚、registry 切换或 HF/Bot 外部操作。
- `container-release-evidence.sh` / `container-release-evidence.py` 生成本地 container release evidence：复用 `container-build.sh` 与 `container-smoke.sh`，记录 imageId、build/smoke 状态、RepoDigests、commit 和 `pushExecuted=false`；不推送 registry，不把本地 imageId 当成 GHCR digest。真实 GHCR digest 与 GitHub artifact attestation 由 `.github/workflows/container.yml` 在手动 `push_image=true` 时生成并 verify。
- `secret-scan.sh` / `secret-scan.py` 是本地 secret scanner；扫描 tracked 与未跟踪非忽略的一线文本文件，输出脱敏 JSON summary，发现疑似真实密钥时阻断。
- `security-smoke.sh` / `security-smoke.py` 是本地安全 smoke；验证 token/owner 边界、响应安全头、请求体限制、限流、registry metadata，并可串联 privacy/source/public-release 文件门禁。
- `webhook-smoke.sh` / `webhook-smoke.py` 是 report job webhook 本地模拟器；使用可注入 transport 验证终态事件、HMAC 签名和正文/secret 不外发，不访问公网。
- `webhook-outbox-smoke.sh` / `webhook-outbox-smoke.py` 是 report job webhook SQLite outbox 本地 smoke；验证 success/failure outbox record、attempts、manager 重建可读和 summary 脱敏边界，不证明公网 live callback、跨进程自动重投或 external backend。
- `webhook-outbox-redelivery-smoke.sh` / `webhook-outbox-redelivery-smoke.py` 是 report job webhook SQLite outbox 自动重投本地 smoke；验证 failed outbox record 可在 manager 重建后通过运行时 resolver 自动重投成功，resolver 缺失时跳过且 summary 脱敏，不证明公网 live callback、external backend、分布式 worker lease、多副本锁、持久明文 secret 或 exactly-once。
- `webhook-config-vault-smoke.sh` / `webhook-config-vault-smoke.py` 是 report job webhook encrypted config vault 本地 smoke；验证 failed outbox 的 callback URL/secret 只以 Fernet ciphertext 落库、manager 重建可在无运行时 resolver 时重投、成功后删除 encrypted config，并覆盖 key rotation 与 summary 脱敏；不证明外部 Vault/KMS、external backend、分布式 worker lease、多副本锁、真实公网 live callback 或 exactly-once。
- `webhook-outbox-lease-smoke.sh` / `webhook-outbox-lease-smoke.py` 是 report job webhook SQLite outbox lease 本地 smoke；验证 failed outbox 只能被一个本地 lease owner claim，错误 owner release 无效，release 后可重新 claim，manager 重建后通过 encrypted config 只重投一次；不证明 external backend、生产级分布式 worker lease、多副本锁、真实公网 live callback、外部 Vault/KMS 或 exactly-once。
- `report-job-replayable-recovery-smoke.sh` / `report-job-replayable-recovery-smoke.py` 是 report job SQLite 可重建执行本地 smoke；验证带 `task_payload` 和 factory 的 active 任务重建后重新入队成功，无 payload 任务仍安全失败；不证明 external backend、分布式 worker lease、多副本锁或 exactly-once。
- `report-job-restart-recovery-smoke.sh` / `report-job-restart-recovery-smoke.py` 是 report job SQLite 重建恢复本地 smoke；验证旧 `queued` / `running` 任务被安全标记为 failed、写入 `job.recovered_failed`、保留幂等键且 summary 不泄露报告正文、姓名、出生地区或 secret；不证明跨进程继续执行、external backend 或多副本 worker。
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
- `scripts/developer-platform-gate.py -> contracts/fate/developer + docs/reference-materials/developer`
- `scripts/audit-handoff.py -> contracts/fate/audit + governance/tasks + contracts/fate + git`
- `scripts/audit-handoff-dry-run.py -> contracts/fate/audit + scripts/audit-handoff.py output`
- `scripts/postgres-job-store-dry-run.py -> domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/postgres-job-store-live-smoke.py -> domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/postgres-external-worker-restart-smoke.py -> domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `scripts/postgres-public-webhook-live-smoke.py -> domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py + domains/experience-delivery/services/fatecat-delivery/src/webhook_callbacks.py`
- `scripts/multi-replica-runtime-gate.py -> contracts/fate/delivery/multi-replica-runtime-contract.json + contracts/fate/delivery/runtime-backends.json`
- 禁止脚本直接隐藏 secret、运行态或旧路径 fallback。
