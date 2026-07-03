# Repo Evidence
| Evidence | Result |
| --- | --- |
| `git status --short --branch` before implementation | `main...origin/main` with 0093 skeleton untracked and task index modified |
| Existing CLI chain | `fate_core.cli::_run_capability_execute` calls `CapabilityExecutor().execute(CapabilityInput(...))` |
| Existing CLI tests | `tests/regression/test_fate_core_cli.py` covers registry listing, bazi/almanac/meihua execution and planned liuyao rejection |
| Delivery registry before 0093 | `surface.cli` existed but only had unit-level verification and no root script/smoke/contract artifact |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_capability_cli_smoke.py tests/regression/test_fate_core_cli.py` -> 16 passed |
| Quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0093` -> passed; 267 focused regression tests passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0093.json` -> findingCount 0 |

# Constraints Matrix
| Constraint | Meaning |
| --- | --- |
| Reuse executor | CLI capability command 必须继续进入统一 `CapabilityExecutor` 和 provider admission。 |
| No algorithm fork | 根级脚本和 smoke 只能做入口、验证和摘要，不得实现测算核心。 |
| Privacy summary only | smoke summary 只保存 hash、字节数、字段名和状态，不保存完整报告正文或真实敏感信息。 |
| Partial CLI surface | CLI 只支持 JSON capability 命令，不能替代 Markdown 多端同源 gate。 |
| No fake live | 真实 API/Bot/HF/Postgres/webhook/OIDC/SIEM/OTel/Vault 仍是外部连通验证待执行。 |

# Change Boundary
Allowed:
- `scripts/capability-cli.sh`
- `scripts/capability-cli-smoke.py`
- `scripts/capability-cli-smoke.sh`
- `contracts/fate/delivery/cli-capability-command.json`
- `contracts/fate/delivery/registry.json`
- `scripts/local-ci.sh`
- `tests/regression/test_capability_cli_smoke.py`
- `scripts/AGENTS.md`
- `tests/AGENTS.md`
- `contracts/fate/delivery/AGENTS.md`
- `governance/tasks/0093-measurement-infrastructure-cli-capability-command-baseline/`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Incidental allowed fix:
- `governance/tasks/0092-measurement-infrastructure-100-post-0091-deep-research-plan/RESEARCH.md` only to remove secret scan false positive shape.

Not allowed:
- 修改八字、紫微、黄历、梅花计算逻辑。
- 修改 Web/API/Bot Markdown renderer。
- 将 planned capability 改为 production。
- 添加真实 token、DSN、webhook URL 或生产账号。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| CLI 绕过统一 executor | 交付面与 capability 协议分叉 | wrapper 只调用 `python -m fate_core.cli capability`；smoke/测试锁 `canonicalChain`。 |
| smoke 保存完整报告 | 泄露用户输入或报告正文 | summary 只保存 hash、字节数和 key 列表；临时完整输出存在 `TemporaryDirectory` 中。 |
| CLI 通过被误读成 Markdown 多端同源 | 审计结论过度声明 | registry 保持 `status=partial`，contract `nonClaims` 明确不替代 semantic diff。 |
| planned 能力误执行 | 未生产能力流入用户 | smoke 验证 `liuyao` 必须 exit 1 且包含 `尚未生产化`。 |
| 文档 secret scan 误报阻断 quick | 本地门禁无法闭环 | 将 0092 中类似配置赋值的 webhook 链接文字改成 Markdown 链接。 |

# Assumptions and Falsification
- Assumption: 生产化 capability 当前是 `bazi`、`ziwei`、`almanac`、`meihua`。
- Falsifier: 若 registry 新增 production capability，而 `capability-cli-smoke.py` 缺 fixture，provider dependency 或 smoke 应失败并要求补 fixture。
- Assumption: CLI surface 是开发者本地 JSON 能力入口，不是标准报告交付面。
- Falsifier: 若文档或 registry 把 CLI 写成 Markdown 同源证明，0093 结论必须回滚。
- Assumption: 0092 文档误报修复不改变调研语义。
- Falsifier: 若 secret scan 仍出现 finding，quick gate 不得通过。

# Critical Ambiguities
- CLI 是否未来需要标准 Markdown 输出：本任务不解决；后续 0094 才考虑 CLI/Skill semantic diff expansion。
- 本任务不处理真实外部生产验证；相关内容继续保持 `外部连通验证待执行`。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务不是 bug 修复；唯一门禁问题是 secret scan 文档误报，已用最小文档改写消除。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | `fate_core.cli`、`CapabilityExecutor`、`test_fate_core_cli.py` |
| TP-02 | `scripts/capability-cli.sh`、`scripts/capability-cli-smoke.py/.sh` |
| TP-03 | `contracts/fate/delivery/cli-capability-command.json`、`registry.json`、`scripts/local-ci.sh`、AGENTS |
| TP-04 | `/tmp/fatecat-capability-cli-smoke-0093.json`、`/tmp/fatecat-local-ci-0093/summary.json`、secret scan output |
