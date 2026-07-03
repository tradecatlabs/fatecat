# Task-Level Acceptance
- 根级 `bash scripts/capability-cli.sh <capability_id>` 可执行 production capability。
- `scripts/capability-cli-smoke.sh` 生成 `kind=fatecat.capability_cli_smoke` 的机器可读 summary。
- bazi、ziwei、almanac、meihua 均通过 smoke；planned liuyao 必须拒绝执行。
- `surface.cli` registry 挂上 `cli-capability-command.json` 和 smoke 验证命令，但仍保持 `partial`。
- local-ci quick 包含 CLI capability smoke 和 `test_capability_cli_smoke.py`。
- summary 不保存完整报告正文、姓名、真实出生地区、token、secret、DSN、webhook URL 或生产账号。

# Validation Plan
| Validation | Command | Result |
| --- | --- | --- |
| CLI smoke | `bash scripts/capability-cli-smoke.sh --output-json /tmp/fatecat-capability-cli-smoke-0093.json` | Passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_capability_cli_smoke.py tests/regression/test_fate_core_cli.py` | 16 passed |
| Ruff check | `.venv/bin/python -m ruff check scripts/capability-cli-smoke.py tests/regression/test_capability_cli_smoke.py` | Passed |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/capability-cli-smoke.py tests/regression/test_capability_cli_smoke.py` | Passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0093.json` | findingCount 0 |
| Local CI quick | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0093` | Passed; 267 focused regression tests passed |

# Review Gate
- No algorithm fork: pass.
- Privacy summary only: pass.
- Non-claim boundary: pass; registry `surface.cli.status=partial` and contract `nonClaims` both explicit.
- Docs sync: pass; scripts/tests/delivery AGENTS updated.

# Runtime Verification Gate
- Local runtime verified.
- External API/Bot/HF/Postgres/webhook/OIDC/SIEM/OTel/Vault live verification remains out of scope and pending.

# Ship Readiness
- Local ship readiness for this slice: passed.
- Production live readiness: not claimed; external connected systems remain `外部连通验证待执行`.

# Task Package Acceptance
## TP-01 现有 CLI 能力链路复核

Accepted. Existing CLI executes through `CapabilityExecutor`; planned capability rejection exists.

## TP-02 根级入口与机器可读 smoke

Accepted. Wrapper and smoke added; smoke passed for four production capabilities and liuyao planned rejection.

## TP-03 Delivery contract、local-ci 和文档接线

Accepted. Contract, registry, local-ci artifact, AGENTS and regression tests updated.

## TP-04 验证、误报修复和 closeout

Accepted. Secret scan false positive fixed; quick local CI passed.

# Anti-Goals
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把 CLI baseline 写成 Markdown 多端同源或外部 live 证据
