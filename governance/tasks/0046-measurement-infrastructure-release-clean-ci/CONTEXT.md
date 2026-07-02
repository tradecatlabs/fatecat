# Repo Evidence
- 当前分支：`main...origin/main`。
- 当前 HEAD：`930aecf feat: harden measurement infrastructure gates`。
- 当前远端：`origin https://github.com/tradecatlabs/fatecat.git`。
- 当前工作树：dirty，大量 tracked 修改与 395 个 untracked 文件，主要来自 0009-0046 测算基础设施任务链、contracts、scripts、tests、docs。
- 0045 计划明确 0046 必须取得 `git status clean`、commit hash、push 结果、GitHub Actions run URL/head SHA。
- TP-01.01 审计结果：395 个 untracked 文件主要为 `governance/tasks`、`contracts/fate`、`scripts`、`tests/regression`、`docs/reference-materials/developer`；未发现未跟踪 `.env`、私钥、DB、压缩包等直接误提交信号。
- TP-02.01 本地门禁：
  - `python3 .../validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` -> `46/46 valid`。
  - `git diff --check` -> pass。
  - `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0046-prestage.json` -> `status=passed,findingCount=0`。
  - `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0046` -> `132 passed in 78.59s`，summary 为 `status=passed,profile=quick,commit=930aecf2032cf708ab78748a2178a2923bc78d04`。
  - `bash scripts/live-release-gate.sh ... --output-json /tmp/fatecat-live-release-gate-0046-precommit.json` -> `passed=6,pending=4,failed=0`；pending 为 remote CI、Bot live、container digest、clean git。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 当前分支必须保持 main | 不切分支，不切 worktree |
| 不能破坏历史 | 不 rebase、不 amend、不 reset、不 force push |
| worktree 大量 dirty | 先审计，再整体或分组提交 |
| release gate 不可伪造 | Bot、registry、OIDC/SIEM 继续 pending |
| 用户目标要求连续推进 | 能执行的本地门禁和 Git/GitHub 证据继续推进 |

# Change Boundary
- 允许：任务文档、已有基础设施改动的提交/推送、验证证据落盘。
- 禁止：删除用户资产、清理未确认文件、重写 Git 历史、输出 secret。

# Risk Matrix
| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 大量 untracked 混入运行态/敏感文件 | 高 | 已执行 untracked 分类与 secret scan，未发现直接阻断 |
| quick CI 太慢或失败 | 中 | 记录真实失败，不伪造通过 |
| push 后远端 CI 失败 | 中 | 记录 run URL 和失败原因，后续修复 |
| commit 过大难审 | 中 | 使用语义清晰的批次提交；如难以拆分则说明原因 |

# Assumptions and Falsification
- 假设：当前 dirty worktree 主要是 0009-0046 基础设施工作成果，应整体收口。
- 反证：若发现 `.env`、token、runtime DB、大型缓存或无关用户资产，则不得提交，必须隔离。
- 假设：当前环境有权限 push 到 `origin/main`。
- 反证：若 `git push` 或 `gh run list` 权限不足，则记录为外部权限阻塞，不伪造远端 CI。
- 调试模式: `Optional`

# Critical Ambiguities
- 当前 395 个 untracked 文件已归类为基础设施批次；GitHub CLI 是否已登录、Actions 是否可查询仍需 TP-04.01 验证。

# Debug Evidence Contract
Not Required。若 CI 或测试失败，再切换为 Required 并记录最小失败证据。

# Task Package Context Map
- TP-01.01：只做事实审计，不修改。
- TP-02.01：本地验证和 release evidence。
- TP-03.01：版本控制交付。
- TP-04.01：远端 CI 当前 commit 证据。
- TP-05.01：任务 closeout。
