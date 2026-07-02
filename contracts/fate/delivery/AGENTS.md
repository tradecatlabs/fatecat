# AGENTS.md - delivery surface resources

## 目录用途

`contracts/fate/delivery/` 是测算基础设施多端交付面和发布证据门禁的资源真相源。这里登记 FastAPI、Web、Telegram Bot、CLI、Agent Skill 和 Hugging Face Space 等 DeliverySurface，并用 ReleaseGate 聚合真实 API、HF Space、Bot、远端 CI、容器 digest、SBOM/provenance 和回滚演练证据；目录内只保存入口发现、同源链路说明、验证命令、输出契约和外部连通边界，不保存用户输入、报告正文、token 或生产运行日志。

## 目录结构

```text
delivery/
├── AGENTS.md
├── release-gate.json
├── registry.json
└── schemas/
    ├── delivery-surface.schema.json
    └── release-gate.schema.json
```

## 职责边界

- `registry.json`：登记 DeliverySurface 资源，记录入口、支持输出、支持报告体系、同源计算链路、验证命令、隐私边界和外部连通状态。
- `release-gate.json`：登记 live release 必需证据，覆盖 local CI、远端 CI、生产 API、HF Space、Telegram Bot、container digest、SBOM/provenance、rollback drill 和 clean git state。
- `schemas/delivery-surface.schema.json`：定义交付面资源字段，覆盖 api、web、bot、cli、skill 和 hosted_web。
- `schemas/release-gate.schema.json`：定义 ReleaseGate 证据项、check 输出、shipGate 状态和不可伪造证据边界。
- 这里不定义命理算法，不渲染 Markdown，不保存运行时 job、真实 Bot token、真实用户记录或生产日志。
- `partial` 表示该交付面只覆盖部分输出契约，例如 CLI 只覆盖 JSON/capability 执行，不承诺生成标准 Markdown。
- `manual` 表示需要用户部署、真实域名、真实 token 或外部平台权限，仓库内不能伪造通过。
- `ReleaseGate` 的本地 contract gate 可以通过，但缺真实外部证据时 `shipGate.status` 必须保持 `blocked`。
- `evidence.local_ci_quick` 只接受 `scripts/local-ci.sh --profile quick` 生成的 `summary.json`，且必须满足 `kind=fatecat.local_ci_summary`、`profile=quick`、`status=passed`、`commit` 匹配当前 `HEAD`；文件存在本身不能作为通过证据。
- 本地 SBOM/provenance 由 `scripts/release-artifacts.sh` 生成，只证明仓库当前 worktree 可产出发布资产 baseline，不等于远端 CI attestation 或 registry signature。
- 本地 rollback drill 由 `scripts/rollback-drill.sh` 生成，只证明 dry-run 回滚路径、候选命令和必需文档可审计；`productionRollbackExecuted=false` 时不能宣称真实生产回滚演练已完成。
- 本地 container evidence 由 `scripts/container-release-evidence.sh` 生成，只证明本地 Docker image build/smoke 和 `imageId`；`registryDigestPresent=false` 或 `pushExecuted=false` 时不能宣称 GHCR/registry 发布已完成。
