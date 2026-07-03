# Execution Checklist
[x] TP-01.01 | P0 | 读取 multi-surface semantic diff 脚本/契约/测试 | Verify: existing script, contract and tests reviewed | Gate: 0090 CLI/Skill not_in_scope gap identified | Parallelizable: No
[x] TP-01.02 | P0 | 读取 CLI capability smoke 与 Skill 命令文档 | Verify: `scripts/capability-cli-smoke.py`、`SKILL.md`、`references/commands.md`、`references/io-contract.md` | Gate: reusable CLI smoke and static Skill command chain confirmed | Parallelizable: No
[x] TP-02.01 | P0 | 在 diff 脚本中新增 CLI capability evidence | Verify: `nonMarkdownSurfaceEvidence.surface.cli` | Gate: production capabilities passed and planned liuyao rejected | Parallelizable: No
[x] TP-02.02 | P0 | 在 diff 脚本中新增 Skill command chain evidence | Verify: `nonMarkdownSurfaceEvidence.surface.agent_skill` | Gate: tracked Skill docs contain canonical command snippets | Parallelizable: No
[x] TP-03.01 | P0 | 更新 semantic diff contract 和 registry | Verify: `contracts/fate/delivery/multi-surface-semantic-diff.json` and `registry.json` | Gate: `requiredLocalEvidenceSurfaces` present | Parallelizable: No
[x] TP-03.02 | P0 | 更新 commands/io-contract/AGENTS/roadmap | Verify: docs mention capability CLI and non-Markdown evidence boundary | Gate: no CLI Markdown overclaim | Parallelizable: No
[x] TP-03.03 | P0 | 更新 regression tests | Verify: focused pytest | Gate: 6 tests passed | Parallelizable: No
[x] TP-04.01 | P0 | 运行 semantic diff gate 和 focused tests | Verify: semantic diff output and focused pytest | Gate: CLI/Skill evidence passed | Parallelizable: No
[x] TP-04.02 | P0 | 运行 ruff/format/secret/quick gate | Verify: ruff, secret scan, local-ci quick | Gate: all exit 0 | Parallelizable: No
[x] TP-04.03 | P0 | 回填任务包并提交推送 | Verify: task validator, git status, commit, push, gh run check | Gate: clean pushed branch; no fake CI claim | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
