# Task-Level Acceptance

- 新增 smoke 脚本必须复用现有 `ReportJobManager`、`PostgresReportJobStore`、`HttpWebhookDispatcher` 和 `WebhookConfig`。
- `--allow-missing` 在缺少 DSN/URL/psycopg 时必须输出 `status=blocked`，exit 0。
- live 模式只有在真实 Postgres DSN 与公网 HTTPS webhook URL 都可用时才允许 `status=passed`。
- summary 不得包含 DSN、URL、secret、报告正文、姓名、出生地区、token、生产路径或私钥。
- runtime backend contract 必须登记 public webhook live smoke，但 Postgres 仍保持 `status=planned`。
- docs/AGENTS/roadmap 必须写清：该 smoke 不证明 exactly-once、多副本 production ready、外部 Vault/KMS 或接收端 SLA。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| Python/shell 语法 | `.venv/bin/python -m py_compile scripts/postgres-public-webhook-live-smoke.py` / `bash -n scripts/postgres-public-webhook-live-smoke.sh` | 通过 |
| blocked preflight | `bash scripts/postgres-public-webhook-live-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-public-webhook-live-smoke-blocked.json` | `status=blocked` 且不泄密 |
| runtime backend gate | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate-0076.json` | 通过 |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_postgres_public_webhook_live_smoke.py tests/regression/test_runtime_backend_gate.py` | 通过 |
| lint/format | `.venv/bin/python -m ruff check .` / `.venv/bin/python -m ruff format --check .` | 通过 |
| quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0076` | 通过 |
| live smoke | `FATE_REPORT_JOB_DATABASE_URL=... FATE_WEBHOOK_LIVE_URL=... bash scripts/postgres-public-webhook-live-smoke.sh` | 外部连通验证待执行，除非本环境有真实 endpoint |

# Review Gate

- future-optimal-drift：脚本必须推进“生产 live evidence”终态，不能把 mock 当 live。
- ponytail-complexity：不新增 webhook 协议、不新增后台 scheduler、不引入新依赖。
- document-drift：contracts/docs/local-ci/AGENTS/task closeout 必须同步。
- security/privacy：summary 和 docs 不输出 runtime secrets。

# Runtime Verification Gate

Operating model update: not needed；不改变项目定位。
Toolchain model update: updated；新增脚本和 quick CI gate。
Process update: not needed；沿用现有 runtime backend gate 流程。
Source-of-truth updates: updated；runtime backend contract、roadmap、operations docs、AGENTS、task index。
Local README/AGENTS impact: updated；`scripts/AGENTS.md` 和 `contracts/fate/delivery/AGENTS.md`。
Contract/catalog/schema impact: updated；`contracts/fate/delivery/runtime-backends.json` 与 schema/gate。
ADR/Gate/module-context impact: updated；runtime backend gate 和 regression tests。
Documentation exemption reason: none。
Validation evidence: TP-04/TP-05 写入真实命令输出摘要。

# Ship Readiness

- 本地 blocked preflight 和 quick CI 必须通过。
- live passed 不能作为本地默认要求；缺真实 endpoint 时必须写 `外部连通验证待执行`。
- 提交前 `git diff --check`、task validators 必须通过。
- 推送后触发远端 Acceptance 并记录 URL/结论。

# Task Package Acceptance

| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口、边界、敏感信息和 non-claims 已写入任务文档。 |
| TP-02 | 脚本、wrapper、blocked summary、live path 和脱敏检查完成。 |
| TP-03 | contract/schema/gate/local-ci/docs/AGENTS/tests 接线。 |
| TP-04 | 本地验证通过；live 证据若缺失必须明确 blocked。 |
| TP-05 | closeout、提交推送、远端 CI 证据完成。 |

# Anti-Goals

- 不得虚构证据
- 不得越权补全未确认信息
- 不得把本地/mock callback 写成公网 live 通过
- 不得输出真实 DSN、URL、secret、token、报告正文或用户输入
