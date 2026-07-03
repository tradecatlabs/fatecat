# Repo Evidence
| Evidence | Result |
| --- | --- |
| `git status --short --branch` before task | `main...origin/main` clean |
| 0093 | `scripts/capability-cli.sh` and `capability-cli-smoke.py` already production local baseline |
| 0090 gate | `multi-surface-semantic-diff.py` compared API/Web/Bot Markdown and left CLI/Skill as `not_in_scope` |
| 0094 semantic diff | `bash scripts/multi-surface-semantic-diff.sh --output-json /tmp/fatecat-multi-surface-0094.json` -> passed |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_multi_surface_semantic_diff.py tests/regression/test_capability_cli_smoke.py` -> 6 passed |
| Ruff | `ruff check` and `ruff format --check` on changed Python files -> passed |

# Constraints Matrix
| Constraint | Meaning |
| --- | --- |
| Markdown hash scope | 只让 API/Web/Bot 标准 Markdown surfaces 进入 hash equality 集合。 |
| CLI evidence scope | CLI 用 capability JSON smoke 证明 `CapabilityExecutor` 同源，不声明 Markdown 输出。 |
| Skill evidence scope | Skill 用文档和命令链证明调用仓库标准入口，不自行拼报告。 |
| Privacy | 证据只保存 hash、长度、行数、字段名、surface id 和错误计数，不保存完整报告正文或真实敏感信息。 |
| No fake live | Bot live、HF Space、公网 API、外部 webhook 仍是外部连通验证待执行。 |

# Change Boundary
Allowed:
- `scripts/multi-surface-semantic-diff.py`
- `contracts/fate/delivery/multi-surface-semantic-diff.json`
- `contracts/fate/delivery/registry.json`
- `tests/regression/test_multi_surface_semantic_diff.py`
- `references/commands.md`
- `references/io-contract.md`
- `scripts/AGENTS.md`
- `tests/AGENTS.md`
- `contracts/fate/delivery/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0094-measurement-infrastructure-cli-skill-semantic-diff-expansion/`
- `governance/tasks/INDEX.md`

Not allowed:
- 修改测算核心算法。
- 将 CLI/Skill 伪装为标准 Markdown surface。
- 保存完整 Markdown 报告正文。
- 引入真实 token、DSN、webhook URL 或生产外部账号。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 CLI JSON 误当 Markdown 同源 | 语义边界错误 | 新增 `nonMarkdownSurfaceEvidence`，不加入 `comparisons[].surfaces`。 |
| Skill 静态检查过弱 | 文档漂移仍可能漏掉 | 检查 `SKILL.md`、`references/commands.md`、`references/io-contract.md` 的 canonical command snippets。 |
| 输出证据泄露报告正文 | 隐私风险 | 继续使用 forbidden marker 和 hash-only summary。 |
| 复用 0093 smoke 造成双跑成本 | quick gate 略变慢 | smoke 是本地 1 秒级，收益高于成本。 |
| 远端 CI 未触发 | 不能声明当前提交 CI pass | 本地证据与远端证据分开记录。 |

# Assumptions and Falsification
- Assumption: CLI 未来若要生成 Markdown，必须单独任务定义输出契约，不能混进本轮 non-Markdown evidence。
- Falsifier: 若 payload 中 `surface.cli` 出现在 `comparisons[].surfaces`，则本任务失败。
- Assumption: Skill 作为安装/调用说明，不是运行时 renderer。
- Falsifier: 若 Skill 文档出现自行拼接标准 Markdown 的说明，Skill evidence 必须失败。
- Assumption: 0094 不需要外部网络或真实凭证。
- Falsifier: 若 gate 依赖 Telegram/HF/API live 才能通过，则本任务越界。

# Critical Ambiguities
- CLI 是否应未来支持 Markdown：本轮不判断，只记录为后续可能任务。
- Skill strict validator 是否一定存在：本轮不用外部 validator 作为必过项，避免 CI 环境路径依赖；用 tracked 文档静态证据。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务不是 bugfix；若 quick gate 后续发现回归，再升级为 debug-required。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 0090 script/contract/tests, 0093 CLI smoke, Skill docs |
| TP-02 | `scripts/multi-surface-semantic-diff.py` evidence expansion |
| TP-03 | contracts, registry, docs, AGENTS, tests |
| TP-04 | `/tmp/fatecat-multi-surface-0094.json`, focused pytest, local-ci quick |
