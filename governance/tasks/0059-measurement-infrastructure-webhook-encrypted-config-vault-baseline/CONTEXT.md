# Task Context

## Current Facts

- `0056` 已完成 SQLite webhook outbox record baseline，但明确不实现 secret 加密存储。
- `0058` 已完成 SQLite outbox redelivery baseline，通过运行时 `delivery_resolver` 重建 callback config。
- roadmap 当前仍把 `持久 callback secret 加密/轮换` 标为 MI-NEXT-03 剩余缺口。
- `pyproject.toml` 和 requirements 当前没有 `cryptography`；本任务不得自研密码学。

# Repo Evidence

| Evidence | Source |
| --- | --- |
| Roadmap remaining gap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` still lists `持久 callback secret 加密/轮换` under `MI-NEXT-03` remaining work. |
| Current API docs boundary | `docs/reference-materials/operations/测算基础设施 API 接入.md` says encrypted/rotation remains undone after SQLite redelivery baseline. |
| 0058 task package | `governance/tasks/0058-measurement-infrastructure-webhook-outbox-redelivery-baseline/` records resolver-based redelivery without persistent secret storage. |
| Runtime code | `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` owns report job store/outbox/redelivery. |
| Webhook code | `domains/experience-delivery/services/fatecat-delivery/src/webhook_callbacks.py` owns callback validation, HMAC and HTTP dispatch. |
| Dependency files | `pyproject.toml`, `requirements.txt`, `requirements.lock.txt`, `requirements-dev.lock.txt` are the source of dependency truth for bootstrap and CI. |

# Constraints Matrix

| Constraint | Requirement |
| --- | --- |
| Security | No plaintext webhook URL/secret in SQLite raw text, API response, event metadata, logs or smoke summary. |
| Dependency | Use mature `cryptography` / Fernet; no custom cryptography. |
| Compatibility | Existing memory and SQLite stores still work without encrypted vault configured. |
| Runtime | Local smoke must use generated keys and injected transport only; no real network callback. |
| Scope | Do not implement external Vault/KMS, external backend, distributed lease or exactly-once. |

# Change Boundary

In scope:

- dependency declarations for `cryptography`
- delivery service runtime code for encrypted webhook config vault
- local smoke and regression tests
- quick CI, docs, AGENTS and task index

Out of boundary:

- external secret service integrations
- production environment secrets
- live webhook endpoints
- unrelated report rendering or bazi/ziwei logic

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Plaintext leak in SQLite | Blocks production security baseline | Raw DB text assertions and secret scan. |
| Dependency drift | CI/bootstrap failure | Update pyproject, requirements and lock; run bootstrap/quick CI. |
| Rotation breaks old ciphertext | Redelivery regression | Focused test decrypts after key rotation and then redelivers. |
| Behavior change without vault | 0058 regression | Existing redelivery resolver tests remain in focused regression. |

# Assumptions and Falsification

- Assumption: Fernet is acceptable for local encrypted-at-rest baseline. Falsifier: dependency cannot install or CI rejects new dependency.
- Assumption: URL can be stored as ciphertext together with secret for redelivery. Falsifier: raw SQLite text contains host or secret.
- Assumption: successful delivery should delete encrypted config. Falsifier: config row remains after succeeded outbox.

# Critical Ambiguities

- Production KMS/Vault provider is not selected. This does not block local baseline; external provider remains future work.
- Whether URL should be retained after permanent failure is a policy decision. This slice retains ciphertext only for failed/pending delivery so redelivery can work, and deletes it on success.

## Target End State

本轮完成后，单机 SQLite backend 可以在本地证明：

- failed/pending webhook outbox 的 callback config 可被加密保存。
- SQLite 原始表中不出现 webhook URL、webhook secret、报告正文、姓名、出生地区、token、DSN 或生产路径。
- manager 重建后无需外部 resolver 也能解密本地 config 并自动 redelivery。
- 投递成功后 encrypted config 被删除，降低持久化敏感面。
- key rotation 可把旧 key 加密的未完成 config 重新加密到 active key。

## Real Constraints

- 只能使用当前仓库与本地/CI 可验证资源。
- 不读取真实 `.env`、真实 token、真实 webhook endpoint 或生产配置。
- Fernet key 只能来自测试运行时生成或环境变量占位，不得提交真实 key。
- SQLite 仍是单副本本地 baseline，不具备多副本 worker lease。

## Inertia Constraints

- 不能把 0058 的运行时 resolver 当作最终 secret 管理方案。
- 不能为了自动 redelivery 把明文 URL/secret 写入 outbox。
- 不能把本地 encrypted SQLite vault 写成外部 Vault/KMS。

## Kill List

- 持久明文 webhook secret。
- API/event/summary/log 输出完整 webhook URL、secret、密文正文或报告正文。
- 自研加密算法。
- 声称生产级分布式 secret 管理、exactly-once 或公网 live callback 完成。

## Proof Point

使用临时 SQLite、运行时生成 Fernet keys 和本地 transport：

1. 初次 webhook 投递失败后，encrypted config 表存在记录但不含明文。
2. 新 manager 无 `delivery_resolver`，只靠 encrypted config vault 重投成功。
3. 重投成功后 encrypted config 被删除。
4. 旧 key 记录可 rotate 到新 active key 并继续解密投递。

## Falsifier

- 原始 SQLite 文本包含 callback host、secret、姓名、出生地区或报告正文。
- 未提供 external resolver 时无法使用本地 encrypted config 重投。
- key rotation 后无法解密。
- secret scan 或 quick CI 失败。

## Debug Evidence Contract

- 调试模式: Optional
- 若 Fernet 依赖、SQLite schema 或 redelivery 集成失败，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0056/0058、webhook/report job 源码、依赖和测试。 |
| TP-02.01 | 更新依赖并新增 Fernet codec。 |
| TP-02.02 | 修改 SQLite store schema 和 encrypted config 方法。 |
| TP-02.03 | 修改 manager redelivery fallback 和成功删除逻辑。 |
| TP-03.01 | 新增 encrypted config vault smoke。 |
| TP-03.02 | 新增 API contract / smoke regression tests。 |
| TP-03.03 | 修改 `scripts/local-ci.sh`。 |
| TP-04.01 | 修改文档、AGENTS 和 INDEX。 |
| TP-04.02 | 运行 validators、pytest、ruff、secret scan、local-ci 和 git 检查。 |
