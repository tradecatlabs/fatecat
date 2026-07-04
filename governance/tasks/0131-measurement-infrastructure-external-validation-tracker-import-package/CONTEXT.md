# Context

- 调试模式: Optional

## Repo Evidence

- `governance/tasks/0130-measurement-infrastructure-external-validation-issue-export/` 已完成 issue export。
- `scripts/external-validation-issue-export.py` 输出 `issueTemplates[].bodyMarkdown`、labels、title、workItemId 和 blockingItems。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 6.25 指出 0130 后仍需 operator creates tracker issues manually。
- 当前 `main` 在 `535e4b9` 已通过远端 Acceptance 和 Container workflow。

## Constraints Matrix

| Constraint | Handling |
| --- | --- |
| 不连接外部系统 | generator 只读本地 issue export JSON，不调用 network、GitHub API 或 `gh` |
| 不保存敏感值 | 输出只允许 title、labels、body file path、credential 名称、命令文本和 hash |
| 不声明 100% | `packageGate=blocked`，nonClaims 明确不代表 issue created 或 live passed |
| 保持统一证据链 | 输入绑定 issue export sha256、issue export commit 和当前 commit |

## Change Boundary

可改：

- `contracts/fate/audit/external-validation-tracker-import-package.json`
- `scripts/external-validation-tracker-import-package.py`
- `scripts/external-validation-tracker-import-package.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_external_validation_tracker_import_package.py`
- `scripts/AGENTS.md`
- `contracts/fate/audit/AGENTS.md`
- `tests/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/INDEX.md`
- 本任务目录

不可改：

- 不改测算 provider、报告输出、API/Bot/Web 行为。
- 不新增真实 tracker 调用。
- 不改 proof-ref/live-proof gate 接受语义。

## Risk Matrix

| Risk | Control |
| --- | --- |
| import package 被误读成已创建 issue | contract、README、roadmap、nonClaims、`packageGate=blocked` |
| 命令文本被自动执行 | generator 只写 `.txt` 命令清单，不执行 `gh` |
| 输出泄露真实 endpoint 或 token | generator 敏感赋值与 raw URL 拒绝；regression 覆盖 |
| 与 issue export 重复 | tracker package 只做独立 body files 和 command manifest，不重做 issue export 分类 |
| local-ci artifact 不可追踪 | summary.json 写入 package dir、JSON 和 Markdown artifact 路径 |

## Assumptions and Falsification

- 假设：当前下一步需要提升 issue 创建前的可执行性，而不是继续新增术数能力。
- 证伪：如果 tracker package 无法消费 0130 issue export，说明边界错误。
- 证伪：如果输出包含 raw URL、敏感赋值形态，或执行 `gh`，必须失败。

## Critical Ambiguities

- 是否直接创建 GitHub Issues：本任务明确不创建，只生成本地 dry-run package。
- issue tracker 类型：当前生成 GitHub Issues CLI command text，但不绑定真实 repo、token 或 API。

## Debug Evidence Contract

本任务不是 bugfix。若 regression 或 local-ci 失败，必须记录失败命令、stderr 摘要、修复点和复跑证据。

## Task Package Context Map

| Artifact | Role |
| --- | --- |
| `external-validation-issue-export.json` | tracker import package 唯一输入 |
| `external-validation-tracker-import-package.json` | import package manifest |
| `external-validation-tracker-import-package/README.md` | operator review entrypoint |
| `external-validation-tracker-import-package/issues/*.md` | 独立 issue body files |
| `external-validation-tracker-import-package/gh-issue-create-commands.txt` | 人工可复核 command text |
