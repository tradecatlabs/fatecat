# Context

- 调试模式: Optional

## Repo Evidence

- `governance/tasks/0129-measurement-infrastructure-third-party-audit-rehearsal/` 已完成第三方审计预演包。
- `scripts/external-validation-closure-work-queue.py` 已生成 owner/category work items。
- `scripts/external-validation-category-runbooks.py` 已生成 category runbooks。
- `scripts/external-validation-operator-execution-packet.py` 已生成 operator execution packet。
- `scripts/external-validation-closure-evidence-summary.py` 已生成外部验证关闭证据摘要。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 6.24 指出 0129 后真实外部执行和独立审计仍未闭合。

## Constraints Matrix

| Constraint | Handling |
| --- | --- |
| 不连接外部系统 | generator 只读本地 JSON，不调用 network 或 tracker API |
| 不保存敏感值 | 输出只允许 credential 名称、命令模板、hash 指令和 proof-ref pattern |
| 不声明 100% | `issueGate=blocked`，nonClaims 明确不代表 live passed |
| 保持统一证据链 | 输入绑定 work queue/runbooks/operator/closure summary sha256 |

## Change Boundary

可改：

- `contracts/fate/audit/external-validation-issue-export.json`
- `scripts/external-validation-issue-export.py`
- `scripts/external-validation-issue-export.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_external_validation_issue_export.py`
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
| issue export 被误读成已创建 issue | contract、README、roadmap、nonClaims、`issueGate=blocked` |
| 输出泄露真实 endpoint 或 token | generator 敏感赋值与 raw URL 拒绝；regression 覆盖 |
| 与 operator packet 重复 | issue export 只做 tracker/import 卡片，不替代 operator packet |
| local-ci artifact 不可追踪 | summary.json 写入 JSON/Markdown artifact 路径 |

## Assumptions and Falsification

- 假设：当前下一步需要提升外部验证可分派性，而不是继续新增术数能力。
- 证伪：如果 issue export 无法消费现有 work queue/operator/closure summary，说明边界错误。
- 证伪：如果输出包含 raw URL 或敏感赋值形态，必须失败。

## Critical Ambiguities

- 是否直接创建 GitHub Issues：本任务明确不创建，只生成可复制/导入模板。
- issue tracker 类型：当前使用通用 GitHub Markdown copy-paste 结构，不绑定 GitHub API。

## Debug Evidence Contract

本任务不是 bugfix。若 regression 或 local-ci 失败，必须记录失败命令、stderr 摘要、修复点和复跑证据。

## Task Package Context Map

| Artifact | Role |
| --- | --- |
| `external-validation-closure-work-queue.json` | work item 真相源 |
| `external-validation-category-runbooks.json` | required credential / command / closure condition 真相源 |
| `external-validation-operator-execution-packet.json` | operator step / proof-ref template 真相源 |
| `external-validation-closure-evidence-summary.json` | pending/blocking status 真相源 |
