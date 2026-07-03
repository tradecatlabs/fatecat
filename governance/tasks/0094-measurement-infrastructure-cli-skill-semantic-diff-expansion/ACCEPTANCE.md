# Task-Level Acceptance
- `multi-surface-semantic-diff` 输出 `nonMarkdownSurfaceEvidence`，包含 `surface.cli` 和 `surface.agent_skill`。
- API/Web/Bot 继续做标准 Markdown normalized semantic hash 相等检查。
- CLI evidence 必须来自 capability CLI smoke，并证明 bazi/ziwei/almanac/meihua production capability 和 planned liuyao 拒绝。
- Skill evidence 必须验证 `SKILL.md`、`references/commands.md`、`references/io-contract.md` 的 canonical command chain。
- Contract/registry/AGENTS/tests/commands/io-contract/roadmap 同步更新。
- 证据不得保存完整 Markdown 报告正文、真实用户输入、token、secret、DSN、webhook URL 或生产日志。

# Validation Plan
| Validation | Command | Result |
| --- | --- | --- |
| Semantic diff gate | `bash scripts/multi-surface-semantic-diff.sh --output-json /tmp/fatecat-multi-surface-0094.json` | Passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_multi_surface_semantic_diff.py tests/regression/test_capability_cli_smoke.py` | 6 passed |
| Ruff check | `.venv/bin/python -m ruff check scripts/multi-surface-semantic-diff.py tests/regression/test_multi_surface_semantic_diff.py` | Passed |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/multi-surface-semantic-diff.py tests/regression/test_multi_surface_semantic_diff.py` | Passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0094.json` | findingCount 0 |
| Local CI quick | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0094` | Passed; 267 tests passed |
| Task closeout validator | `validate_task_docs.py --phase closeout` | Passed |

# Review Gate
- No Markdown overclaim: pass so far; CLI/Skill are not in `comparisons[].surfaces`.
- No raw report evidence: pass so far; payload stores hash/key/status only.
- No external live claim: pass so far; external pending remains explicit.
- Docs sync: pending final validator.

# Runtime Verification Gate
- Local semantic diff and focused tests passed.
- Full local quick gate passed.
- External live verification remains out of scope and pending.

# Ship Readiness
- Ready for Git delivery; final clean commit and push evidence must be checked after commit.

# Task Package Acceptance
## TP-01 复核 0090/0093 现状

Accepted. Existing gate and CLI smoke were read and reused.

## TP-02 实现 non-Markdown evidence surfaces

Accepted. Script now outputs CLI and Skill evidence surfaces.

## TP-03 契约、文档和测试接线

Accepted pending final validation. Contract, registry, docs, AGENTS and tests updated.

## TP-04 验证与 closeout

Accepted. Focused validation, quick gate and closeout validator passed; Git delivery evidence is checked after commit.

# Anti-Goals
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把 CLI/Skill 写成标准 Markdown hash surfaces
- 不得声明真实外部 live 已完成
