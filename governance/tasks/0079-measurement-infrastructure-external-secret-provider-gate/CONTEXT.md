# Repo Evidence

| Evidence | Observation |
| --- | --- |
| `domains/experience-delivery/services/fatecat-delivery/src/webhook_config_store.py` | 当前只提供本地 Fernet encrypted-at-rest baseline；文件注释明确外部 Vault/KMS 是后续能力。 |
| `scripts/webhook-config-vault-smoke.py` | 已证明本地 SQLite encrypted config vault、key rotation、manager 重建 redelivery 和脱敏 summary。 |
| `contracts/fate/delivery/runtime-backends.json` | `backend.postgres` 仍把 `external_vault_kms` 作为 blocked claim。 |
| `contracts/fate/security/externalization-evidence-contract.json` | 已有 OIDC/SIEM/retention 外部化证据契约，但不覆盖 secret provider / Vault / KMS。 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0078 已完成 worker heartbeat/polling；后续仍缺外部 Vault/KMS、生产密钥生命周期、长期多副本和 exactly-once。 |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不接真实 secret manager | 本任务只做 evidence contract、negative gate 和 local-ci artifact。 |
| 不引入外部 SDK | 复用 JSON contract + gate 模式，不新增 Vault/KMS dependency。 |
| 不伪造 live evidence | 默认输出 `外部连通验证待执行`；只有 `--evidence-json` 提供脱敏 evidence 时才验证 live schema。 |
| 不把 local Fernet 写成 external | negative cases 必须拒绝 `local_fernet`、env var、placeholder proof。 |
| 文档驱动 | security registry/schema/policy、runtime backend note、operations docs、AGENTS 和 task docs 必须同步。 |

# Change Boundary

- 允许新增 `contracts/fate/security/external-secret-provider-contract.json`。
- 允许新增 `scripts/external-secret-provider-gate.py` 和 `.sh`。
- 允许修改 security schema/registry/policy、production-security gate、local-ci、runtime backend contract 文案、operations docs、AGENTS、task docs 和 regression tests。
- 不修改八字/紫微算法。
- 不读取、不写入、不提交真实 secret、token、DSN、webhook URL、KMS key、provider endpoint 或生产审计日志。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 本地 Fernet 伪装外部 Vault/KMS | 生产安全结论失真 | gate negative cases 拒绝 `local_fernet`、`FATE_WEBHOOK_CONFIG_FERNET_KEYS` 和 placeholder proof。 |
| gate 输出敏感值 | 安全事故 | gate 对 contract/evidence/summary 做 sensitive fragment 检查，只允许 evidence refs。 |
| 只写 contract 不接 CI | 文档漂移 | 接入 production-security gate、local-ci 和 focused regression tests。 |
| runtime backend blocked claim 被误删 | 误宣 production ready | 仅增加 gate baseline 说明，不移除 `external_vault_kms` blocked claim。 |

# Assumptions and Falsification

- Assumption: 当前没有真实 HashiCorp Vault、AWS KMS、GCP KMS、Azure Key Vault 或其他 secret manager 权限。
- Assumption: 生产级 secret lifecycle 需要 key reference、rotation、access audit 和 application injection 四类证据。
- Falsifier: `local_fernet` 或 `FATE_WEBHOOK_CONFIG_FERNET_KEYS` evidence 被 gate 接受。
- Falsifier: gate summary 或 contract 输出命中 secret/token/password assignment marker、私钥或 URL 原值。
- Falsifier: production-security gate 没有把 secret provider 纳入 controls。

# Critical Ambiguities

- 真实外部 secret provider 选型未指定；本任务支持 provider type 枚举和通用 evidence refs。
- 真实生产部署注入方式未指定；本任务只定义 `applicationInjectionProofRef`，不规定具体平台。
- 本任务不解决真实 key rotation 操作，只验证未来 evidence 的结构和反伪造边界。

# Debug Evidence Contract

- 调试模式: Optional

若 gate、focused tests 或 CI 失败，记录最小失败命令、根因、修复和回归证据；不得把失败环境写成 live evidence 通过。

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0059 local Fernet vault、0078 runtime backend docs。 |
| TP-01.02 | security schema/registry/policy、production-security gate、local-ci。 |
| TP-02.01 | `external-secret-provider-contract.json`。 |
| TP-02.02 | negative evidence cases and live evidence schema。 |
| TP-03.01 | `security-control.schema.json`、`registry.json`、`production-security-policy.json`。 |
| TP-03.02 | `external-secret-provider-gate.py/.sh`。 |
| TP-03.03 | `local-ci.sh` and summary artifact map。 |
| TP-04.01 | `tests/regression/test_external_secret_provider_gate.py` and related security tests。 |
| TP-04.02 | roadmap、operations docs、`contracts/fate/security/AGENTS.md`、`scripts/AGENTS.md`。 |
| TP-05.01 | focused gates、ruff/format、quick CI。 |
| TP-05.02 | task closeout、Git/GitHub delivery evidence。 |
