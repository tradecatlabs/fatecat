# Task-Level Acceptance

本任务完成必须满足：

- 使用成熟 `cryptography` / Fernet；不得自研密码学。
- SQLite backend 可选启用 encrypted webhook delivery config vault。
- 初次 webhook outbox 创建时，如果 vault 启用，callback config 以密文保存。
- SQLite 原始密文表不包含 webhook URL、webhook secret、Markdown 正文、姓名、出生地区、token、DSN 或生产路径。
- manager 重建后，在没有外部 `delivery_resolver` 时，可从 encrypted vault 恢复 config 并完成 redelivery。
- redelivery 成功后 encrypted config 被删除。
- key rotation 可把旧 key 记录迁移到 active key，并保持可解密。
- quick local CI 执行 webhook encrypted config vault smoke。
- 文档明确当前是本地 baseline，不是外部 Vault/KMS、external backend、分布式 worker、真实公网 live smoke 或 exactly-once。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| dependency install | `.venv/bin/python -m pip install -q -e '.[dev]'` | pass |
| smoke CLI | `bash scripts/webhook-config-vault-smoke.sh --output-json /tmp/webhook-config-vault-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_webhook_config_vault_smoke.py tests/regression/test_api_contracts.py` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/webhook_config_store.py scripts/webhook-config-vault-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0059.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | encrypted vault redelivery 成功；resolver 仍优先；无 vault 时兼容 0058。 |
| 可读性 | codec/store/manager glue 边界清晰，不隐藏 external Vault/KMS 未完成事实。 |
| 架构 | 不把 secret 存储塞进 outbox record；encrypted config 是可替换后端。 |
| 安全 | 不持久化明文 secret、完整 URL、报告正文或真实用户隐私；成功后删除密文。 |
| 性能 | manager 重建只扫描 redeliverable outbox；rotation 只处理 vault 表。 |

# Runtime Verification Gate

- 本地可验证：Fernet key runtime 生成、SQLite 密文保存、manager rebuild redelivery、success delete、key rotation、privacy boundary。
- 外部连通验证待执行：外部 Vault/KMS、external backend、multi-worker lock、真实 webhook live smoke。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0059。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明外部 Vault/KMS、external backend、分布式 worker、exactly-once、生产级 secret storage 或真实 webhook live smoke 完成。
