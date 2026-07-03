# AGENTS.md - delivery surface resources

## 目录用途

`contracts/fate/delivery/` 是测算基础设施多端交付面、durable runtime 后端、异步事件契约和发布证据门禁的资源真相源。这里登记 FastAPI、Web、Telegram Bot、CLI、Agent Skill 和 Hugging Face Space 等 DeliverySurface；登记 CalculationJob RuntimeBackend 候选和外部 backend 迁移边界；登记 job/webhook/evaluation/release 的 AsyncEvent 契约；并用 ReleaseGate 聚合真实 API、HF Space、Bot、远端 CI、容器 digest、SBOM/provenance 和回滚演练证据。目录内只保存入口发现、同源链路说明、验证命令、输出契约和外部连通边界，不保存用户输入、报告正文、token、DSN、webhook URL、secret 或生产运行日志。

## 目录结构

```text
delivery/
├── AGENTS.md
├── events.json
├── events.asyncapi.json
├── examples/
│   └── events/
├── multi-replica-runtime-contract.json
├── multi-surface-semantic-diff.json
├── release-gate.json
├── registry.json
├── runtime-backends.json
└── schemas/
    ├── async-event.schema.json
    ├── delivery-surface.schema.json
    ├── release-gate.schema.json
    └── runtime-backend.schema.json
```

## 职责边界

- `registry.json`：登记 DeliverySurface 资源，记录入口、支持输出、支持报告体系、同源计算链路、验证命令、隐私边界和外部连通状态。
- `events.json`：登记 AsyncEvent 资源，记录 job/webhook/evaluation/release 事件的 CloudEvents envelope、AsyncAPI 风格 channel/operation/message、脱敏示例、隐私边界和外部连通状态。
- `events.asyncapi.json`：AsyncAPI 3.1 风格静态事件文档；供开发者和 Agent 发现事件通道，不证明外部 broker 或公网 webhook live delivery。
- `examples/events/`：只保存合成脱敏事件示例；禁止写入真实 webhook URL、secret、token、用户输入、报告正文或生产日志。
- `release-gate.json`：登记 live release 必需证据，覆盖 local CI、远端 CI、生产 API、HF Space、Telegram Bot、container digest、SBOM/provenance、rollback drill 和 clean git state。
- `multi-replica-runtime-contract.json`：定义 Postgres 长期多副本 runtime evidence 的 live schema、最小副本数、最小 soak 时长、反伪造负例和 exactly-once 非声明边界。
- `multi-surface-semantic-diff.json`：定义标准 Markdown 多交付面语义一致性 gate；要求 API direct/API job/Web direct/Web job/Bot dry-run canonical renderer 在八字与紫微报告上的 normalized semantic hash 一致，证据不得保存完整报告正文。
- `runtime-backends.json`：登记 CalculationJob durable runtime 后端候选，当前 memory/sqlite 是本地 baseline，Postgres 已有 live smoke、outbox worker lease smoke、job worker lease primitive smoke、external worker restart smoke baseline、worker heartbeat/polling smoke baseline 与 public webhook live smoke gate baseline 但仍是 planned external backend 候选，Temporal 是 future workflow orchestrator，Redis queue 只允许作为辅助队列。
- `schemas/async-event.schema.json`：定义 AsyncEvent 字段、CloudEvents 必备上下文字段、AsyncAPI 风格 channel/operation 字段、事件域枚举和隐私不变量。
- `schemas/delivery-surface.schema.json`：定义交付面资源字段，覆盖 api、web、bot、cli、skill 和 hosted_web。
- `schemas/release-gate.schema.json`：定义 ReleaseGate 证据项、check 输出、shipGate 状态和不可伪造证据边界。
- `schemas/runtime-backend.schema.json`：定义 RuntimeBackend 字段、状态、成熟度、生产资格、外部连通边界和禁止伪造声明。
- 这里不定义命理算法，不渲染 Markdown，不保存运行时 job、真实 Bot token、真实用户记录或生产日志。
- `partial` 表示该交付面只覆盖部分输出契约，例如 CLI 只覆盖 JSON/capability 执行，不承诺生成标准 Markdown。
- `manual` 表示需要用户部署、真实域名、真实 token 或外部平台权限，仓库内不能伪造通过。
- `ReleaseGate` 的本地 contract gate 可以通过，但缺真实外部证据时 `shipGate.status` 必须保持 `blocked`。
- `DeliverySemanticDiffGate` 的本地 gate 可以通过，但只能证明 API/Web/Bot dry-run 的标准 Markdown 同源；真实 Telegram Bot live、Hugging Face Space hosted Web、公网 API 和浏览器兼容性仍需独立 live evidence。
- `RuntimeBackend` 的本地 gate 可以通过，但 `backend.postgres` 即使已有 live smoke、outbox worker lease smoke、job worker lease primitive smoke、external worker restart smoke baseline、worker heartbeat/polling smoke baseline、public webhook live smoke gate baseline 与 multi-replica runtime evidence contract baseline，也必须在外部 Vault/KMS、公网 webhook passed evidence、长期多副本 live evidence 和 exactly-once 证据完成前保持 `status=planned`，不能声明 external backend 已生产。
- `multi-replica-runtime-contract.json` 可以验证证据格式和拒绝伪证据；`scripts/multi-replica-runtime-evidence-assembler.sh` 只能装配脱敏 evidence JSON 并复用 gate 校验，不能证明 proof refs 真实性。无真实外部多副本运行、公共 webhook、外部 secret provider 与外部 metrics 证据时必须保持 `外部连通验证待执行`。
- `AsyncEvent` 的本地 gate 可以通过，但 `event.webhook.delivery` 在真实接收端 live smoke 完成前必须保持 `externalConnectivity=requires_real_receiver`，不能声明公网 webhook live delivery 已生产。
- `events.asyncapi.json` 是静态契约文档，不得被解释为 Kafka、NATS、RabbitMQ、Redis Streams 或其他外部 broker 已接入。
- `backend.redis_queue` 不得登记为 `CalculationJob` source of truth；只能作为未来辅助队列候选。
- `evidence.local_ci_quick` 只接受 `scripts/local-ci.sh --profile quick` 生成的 `summary.json`，且必须满足 `kind=fatecat.local_ci_summary`、`profile=quick`、`status=passed`、`commit` 匹配当前 `HEAD`；文件存在本身不能作为通过证据。
- 本地 SBOM/provenance 由 `scripts/release-artifacts.sh` 生成，只证明仓库当前 worktree 可产出发布资产 baseline，不等于远端 CI attestation 或 registry signature。
- 本地 rollback drill 由 `scripts/rollback-drill.sh` 生成，只证明 dry-run 回滚路径、候选命令和必需文档可审计；`productionRollbackExecuted=false` 时不能宣称真实生产回滚演练已完成。
- 本地 container evidence 由 `scripts/container-release-evidence.sh` 生成，只证明本地 Docker image build/smoke 和 `imageId`；`registryDigestPresent=false` 或 `pushExecuted=false` 时不能宣称 GHCR/registry 发布已完成。
- 当前 commit release proof 由 `scripts/current-release-proof.sh` 聚合远端 acceptance、container workflow、GHCR digest、GitHub attestation、release artifact、rollback drill 和 git clean 状态；缺任一证据时必须保持 blocked/failed，不得用历史 commit 的 release proof 替代当前 commit。
