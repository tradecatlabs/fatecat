# Task-Level Acceptance

0064 只有在以下证据同时成立时才能 closeout：

- `contracts/fate/observability/otel-collector.dry-run.yaml` 存在，包含 receivers/processors/exporters/service pipelines，且不包含真实 backend URL、token、secret 或 DSN。
- `contracts/fate/observability/slo-evidence-contract.json` 存在，明确 dry-run evidence、live evidence pending、privacy boundary 和 required external evidence。
- Observability registry/schema/AGENTS、API 文档、roadmap 和 scripts AGENTS 已同步。
- `bash scripts/otel-collector-slo-gate.sh --output-json <path>` 通过。
- Focused regression tests、task validators、ruff/format、secret scan、quick local CI 通过。

# Task Package Acceptance

| Node ID | Verify | Gate |
| --- | --- | --- |
| TP-01.01 | `git status` / `rg` / `sed` / official docs | 当前事实和 0064 边界明确 |
| TP-02.01 | YAML/JSON syntax + gate | collector config 和 SLO evidence contract 可机器读取 |
| TP-02.02 | focused tests / docs diff | registry/schema/AGENTS 链接一致 |
| TP-03.01 | gate CLI | dry-run gate 无外部后端依赖 |
| TP-03.02 | focused pytest | config、contract、privacy、pending 边界断言通过 |
| TP-03.03 | local-ci summary artifact | quick CI 运行新 gate |
| TP-04.01 | docs diff + rg | 文档不夸大 collector/backend/live SLO |
| TP-04.02 | validation evidence | 全部本地门禁通过并收口 |

# Happy Path

- 本地 gate 读取 collector YAML、SLO evidence contract、observability registry/schema、SLO policy 和 alert rules。
- Gate 验证 OTLP receiver、batch/memory_limiter processors、logging/debug exporter、dry-run pipeline、SLO evidence required fields 和 privacy boundary。
- Gate 输出机器可读 summary，并被 quick local CI 记录为 artifact。

# Edge Cases

- 如果 YAML 无法解析，gate 必须失败。
- 如果 config 中出现真实 backend URL、authorization header、token、secret、DSN 或 production endpoint，gate 必须失败。
- 如果 SLO evidence 写成 live passed，但没有外部证据，gate 必须失败。
- 如果 registry 把 collector/backend 写成已生产，gate 必须失败。

# Validation Plan

| 验证项 | 命令 | 预期 |
| --- | --- | --- |
| YAML/JSON syntax | `python3 -m json.tool contracts/fate/observability/slo-evidence-contract.json` + gate YAML parse | passed |
| Gate CLI | `bash scripts/otel-collector-slo-gate.sh --output-json <path>` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_observability_trace_slo.py tests/regression/test_capability_protocol.py -k 'otel or observability'` | passed |
| Lint/format | `.venv/bin/python -m ruff check ...` / `.venv/bin/python -m ruff format --check ...` | passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json <path>` | 0 findings |
| Task validators | `validate_task_docs.py --phase closeout` + `validate_tasks_tree.py` | passed |
| Quick local CI | `bash scripts/local-ci.sh --profile quick --output <dir>` | passed |

# Review Gate

- Review must confirm no production backend, collector runtime, alert live, dashboard or real error budget is claimed.
- Review must confirm no real endpoint, token, secret, DSN, user input, birth place, report body, logs, metrics snapshot or trace data is committed.
- Review must confirm docs and contracts use the same dry-run / external pending wording.

# Runtime Verification Gate

- Runtime verification is limited to local dry-run contract checks and existing local trace smoke.
- Any claim requiring real collector, trace backend, alert platform, production traffic or live SLO evidence remains `外部连通验证待执行`.

# Ship Readiness

- 0064 can ship after local validation, quick local CI, commit/push and current-commit remote Acceptance pass.
- 0064 cannot be used as proof that production monitoring is complete.

# Anti-Goals

- 不启动真实 collector。
- 不伪造 trace backend、SLO dashboard、alert live、incident drill 或 production traffic。
- 不读取真实 `.env` 或生产凭证。
- 不保存真实 logs、metrics、traces、用户输入、报告正文或 webhook payload。
